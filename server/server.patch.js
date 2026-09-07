'use strict';
/**
 * Zaggers server hardening patch — DROP-IN, does NOT modify server.js by itself.
 *
 * What this fixes (see server/HARDENING_NOTES.md for full audit):
 *  1. Single-data-event framing assumption  -> per-socket buffering + frame loop
 *  2. No fragmentation support              -> FIN + continuation (0x0) reassembly
 *  3. No ping/pong                          -> auto-reply to 0x9, track 0xA, server ping timer
 *  4. Jumbo (127 / 64-bit) frames dropped   -> 64-bit length via readBigUInt64BE + cap
 *  5. Trust client x/y                       -> clamp 0..2000, finite-number check, dir whitelist
 *  6. No rate limit                         -> 100 ms move throttle per socket (+ attack/chat caps)
 *  7. Chat no sanitize / length cap         -> 200-char cap + HTML escape
 *  8. Hardcoded 5 monsters vs DB 54         -> loadMonstersFromDB(web/zaggers_database.json)
 *
 * HOW TO APPLY (manual, 3 edits in server.js):
 *  A. const Hard = require('./server.patch.js');
 *     Replace initMonsters() body with: Hard.loadMonstersFromDB(monsters, { max: 54 });
 *  B. Replace `socket.on('data', ...)` body with:
 *        socket._rxBuf = Buffer.alloc(0);
 *        socket.on('data', (chunk) => Hard.feedSocket(socket, chunk, (pkt) => {
 *          try { Hard.handleClientPacketHardened(socket, player, JSON.parse(pkt), ctx); }
 *          catch (e) { /* ignore invalid packet *\/ }
 *        }));
 *     where ctx = { clients, monsters, sendPacket, broadcast };
 *  C. (optional) start heartbeat: Hard.startHeartbeat(clients);
 *     Or copy/paste the functions below directly into server.js.
 */

const fs = require('fs');
const path = require('path');

// ---------------------------------------------------------------- tuning
const WORLD_MIN_X = 0;
const WORLD_MAX_X = 2000;
const WORLD_MIN_Y = 0;
const WORLD_MAX_Y = 2000;
const MOVE_THROTTLE_MS = 100;
const ATTACK_THROTTLE_MS = 250;
const CHAT_THROTTLE_MS = 800;
const CHAT_MAX_LEN = 200;
const MAX_PAYLOAD_BYTES = 1 << 20; // 1 MiB — hard cap, larger => drop + close
const VALID_DIRS = new Set(['up', 'down', 'left', 'right']);
const VALID_STATS = new Set(['str', 'agi', 'vit', 'int', 'dex', 'luk']);

const _lastMoveBySock = new WeakMap();   // socket -> timestamp ms
const _lastAttackBySock = new WeakMap();
const _lastChatBySock = new WeakMap();
const _fragBufBySock = new WeakMap();    // socket -> Buffer (continuation reassembly)
const _fragOpBySock = new WeakMap();     // socket -> initial opcode (1 or 2)
const _aliveBySock = new WeakMap();      // socket -> bool (pong tracking)

// ---------------------------------------------------------------- helpers
function clamp(n, lo, hi, fallback) {
  const v = Number(n);
  if (!Number.isFinite(v)) return fallback;
  if (v < lo) return lo;
  if (v > hi) return hi;
  return v;
}

function escapeChat(s) {
  return String(s)
    .slice(0, CHAT_MAX_LEN)
    .replace(/[&<>"']/g, (c) => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
    }[c]));
}

function throttled(map, sock, intervalMs) {
  const now = Date.now();
  const last = map.get(sock) || 0;
  if (now - last < intervalMs) return true; // throttled => drop
  map.set(sock, now);
  return false;
}

// ---------------------------------------------------------------- hardened frame codec

/**
 * Encode a server->client text frame, including 64-bit (jumbo) lengths.
 * Returns Buffer, or null only if payload exceeds MAX_PAYLOAD_BYTES.
 */
function encodeFrameHardened(text) {
  const payload = Buffer.from(text, 'utf8');
  const len = payload.length;
  if (len > MAX_PAYLOAD_BYTES) return null;
  let header;
  if (len <= 125) {
    header = Buffer.from([0x81, len]);
  } else if (len <= 65535) {
    header = Buffer.alloc(4);
    header[0] = 0x81;
    header[1] = 126;
    header.writeUInt16BE(len, 2);
  } else {
    header = Buffer.alloc(10); // 64-bit jumbo path (old code returned null here)
    header[0] = 0x81;
    header[1] = 127;
    header.writeBigUInt64BE(BigInt(len), 2);
  }
  return Buffer.concat([header, payload]);
}

function encodePong(pingPayload) {
  const p = Buffer.isBuffer(pingPayload) ? pingPayload : Buffer.alloc(0);
  const len = Math.min(p.length, 125);
  return Buffer.concat([Buffer.from([0x8a, len]), p.slice(0, len)]);
}

function encodePing() {
  return Buffer.from([0x89, 0x00]);
}

/**
 * Parse as many complete frames as possible from `buf`.
 * Returns { messages: string[], leftover: Buffer, control: { ping, pong, close } }.
 * Handles: fragmentation (FIN + opcode 0x0), masked/unmasked, 16-bit + 64-bit
 * lengths, ping (auto-reply frame included in control.pongReply), pong, close.
 * Never throws on truncated input — short reads stay in `leftover`.
 */
function parseFrames(buf, sock) {
  const messages = [];
  const control = { pingCount: 0, gotPong: false, gotClose: false, pongReply: null };
  let offset = 0;

  while (buf.length - offset >= 2) {
    const b0 = buf[offset];
    const b1 = buf[offset + 1];
    const fin = (b0 & 0x80) !== 0;
    const opcode = b0 & 0x0f;
    const masked = (b1 & 0x80) !== 0;
    let payloadLen = b1 & 0x7f;
    let headLen = 2;

    if (payloadLen === 126) {
      if (buf.length - offset < 4) break; // need more bytes
      payloadLen = buf.readUInt16BE(offset + 2);
      headLen = 4;
    } else if (payloadLen === 127) {
      if (buf.length - offset < 10) break; // need more bytes
      const big = buf.readBigUInt64BE(offset + 2); // old code: `return null` here
      if (big > BigInt(MAX_PAYLOAD_BYTES)) {
        control.gotClose = true; // oversize => signal caller to close
        break;
      }
      payloadLen = Number(big);
      headLen = 10;
    }

    if (payloadLen > MAX_PAYLOAD_BYTES) {
      control.gotClose = true;
      break;
    }

    const maskLen = masked ? 4 : 0;
    if (buf.length - offset < headLen + maskLen + payloadLen) break; // fragmented TCP read

    let payload = buf.slice(offset + headLen + maskLen, offset + headLen + maskLen + payloadLen);
    if (masked) {
      const mask = buf.slice(offset + headLen, offset + headLen + 4);
      const out = Buffer.alloc(payload.length);
      for (let i = 0; i < payload.length; i++) out[i] = payload[i] ^ mask[i % 4];
      payload = out;
    }
    offset += headLen + maskLen + payloadLen;

    if (opcode === 0x8) { control.gotClose = true; break; }
    if (opcode === 0x9) { // ping -> queue pong reply
      control.pingCount += 1;
      control.pongReply = encodePong(payload);
      continue;
    }
    if (opcode === 0xa) { // pong
      control.gotPong = true;
      if (sock) _aliveBySock.set(sock, true);
      continue;
    }
    if (opcode === 0x0) { // continuation
      const prev = _fragBufBySock.get(sock) || Buffer.alloc(0);
      const next = Buffer.concat([prev, payload]);
      if (next.length > MAX_PAYLOAD_BYTES) {
        _fragBufBySock.delete(sock); _fragOpBySock.delete(sock);
        control.gotClose = true; break;
      }
      if (fin) {
        _fragBufBySock.delete(sock); _fragOpBySock.delete(sock);
        messages.push(next.toString('utf8'));
      } else {
        _fragBufBySock.set(sock, next);
      }
      continue;
    }
    if (opcode === 0x1 || opcode === 0x2) { // text | binary (accept binary as utf8 JSON)
      if (!fin) { // start of fragmented message
        _fragBufBySock.set(sock, payload);
        _fragOpBySock.set(sock, opcode);
      } else {
        messages.push(payload.toString('utf8'));
      }
      continue;
    }
    // Other opcodes (e.g. reserved) — ignore per RFC.
  }

  return { messages, leftover: buf.slice(offset), control };
}

/**
 * Per-socket buffered feed: accumulates TCP chunks, emits complete messages.
 * Drop-in replacement for the old `socket.on('data', buf => decodeFrame(buf))`.
 *
 * @param {net.Socket} sock
 * @param {Buffer} chunk
 * @param {(text: string) => void} onMessage
 */
function feedSocket(sock, chunk, onMessage) {
  const acc = Buffer.concat([
    sock._rxBuf && sock._rxBuf.length ? sock._rxBuf : Buffer.alloc(0),
    Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk),
  ]);
  if (acc.length > MAX_PAYLOAD_BYTES + 14) { // headroom for header; flood guard
    try { sock.destroy(); } catch (e) { /* noop */ }
    return;
  }
  const { messages, leftover, control } = parseFrames(acc, sock);
  sock._rxBuf = leftover;
  if (control.pongReply && sock.writable) {
    try { sock.write(control.pongReply); } catch (e) { /* noop */ }
  }
  if (control.gotClose) {
    try { sock.end(Buffer.from([0x88, 0x00])); } catch (e) { /* noop */ }
    try { sock.destroy(); } catch (e) { /* noop */ }
    return;
  }
  for (const m of messages) onMessage(m);
}

/** Server-side heartbeat: pings clients every 30 s, destroys silent ones. */
function startHeartbeat(clientsMap, intervalMs) {
  const ms = intervalMs || 30000;
  const timer = setInterval(() => {
    for (const [sock] of clientsMap) {
      if (!sock.writable) continue;
      if (_aliveBySock.get(sock) === false) {
        try { sock.destroy(); } catch (e) { /* noop */ }
        continue;
      }
      _aliveBySock.set(sock, false);
      try { sock.write(encodePing()); } catch (e) { /* noop */ }
    }
  }, ms);
  if (timer.unref) timer.unref();
  return timer;
}

// ---------------------------------------------------------------- hardened packet handler

/**
 * Hardened replacement for handleClientPacket(socket, player, data).
 * ctx = { monsters: Map, sendPacket: fn, broadcast: fn }
 * Adds: coord clamp, move throttle, chat cap+escape, stat/attack validation.
 */
function handleClientPacketHardened(socket, player, data, ctx) {
  if (!data || typeof data !== 'object') return;
  const monsters = ctx && ctx.monsters;
  const sendPacket = ctx && ctx.sendPacket;
  const broadcast = ctx && ctx.broadcast;
  if (!monsters || !sendPacket || !broadcast) throw new Error('ctx { monsters, sendPacket, broadcast } required');

  switch (data.type) {
    case 'move': {
      if (throttled(_lastMoveBySock, socket, MOVE_THROTTLE_MS)) break;
      player.x = clamp(data.x, WORLD_MIN_X, WORLD_MAX_X, player.x);
      player.y = clamp(data.y, WORLD_MIN_Y, WORLD_MAX_Y, player.y);
      if (typeof data.dir === 'string' && VALID_DIRS.has(data.dir)) player.dir = data.dir;
      broadcast({ type: 'player_move', id: player.id, x: player.x, y: player.y, dir: player.dir }, socket);
      break;
    }

    case 'attack': {
      if (throttled(_lastAttackBySock, socket, ATTACK_THROTTLE_MS)) break;
      const targetId = typeof data.target_id === 'string' ? data.target_id.slice(0, 64) : null;
      broadcast({ type: 'player_attack', id: player.id, target_id: targetId, dir: player.dir }, socket);
      if (targetId && monsters.has(targetId)) {
        const m = monsters.get(targetId);
        const dmg = Math.floor(15 + Number(player.str || 0) * 1.5 + Math.random() * 8);
        m.hp = Math.max(0, m.hp - dmg);
        broadcast({ type: 'monster_hit', id: m.id, hp: m.hp, max_hp: m.max_hp, dmg, attacker_id: player.id });
        if (m.hp <= 0) {
          player.zeny = Math.min(999999, (player.zeny || 0) + (m.zeny || 50));
          sendPacket(socket, { type: 'zeny_update', zeny: player.zeny });
          setTimeout(() => {
            m.hp = m.max_hp;
            broadcast({ type: 'monster_respawn', id: m.id, hp: m.hp, x: m.x, y: m.y });
          }, 5000);
        }
      }
      break;
    }

    case 'chat': {
      if (throttled(_lastChatBySock, socket, CHAT_THROTTLE_MS)) break;
      const text = escapeChat(data.text == null ? '' : String(data.text));
      if (!text.trim()) break;
      broadcast({ type: 'chat', id: player.id, name: player.name, text });
      break;
    }

    case 'stat_add': {
      if (typeof data.stat === 'string' && VALID_STATS.has(data.stat) && player[data.stat] !== undefined) {
        player[data.stat] += 1;
        if (data.stat === 'vit') player.max_hp += 15;
        if (data.stat === 'int') player.max_sp += 10;
        sendPacket(socket, { type: 'stats_update', player });
      }
      break;
    }

    default:
      break; // unknown packet types ignored
  }
}

// ---------------------------------------------------------------- monster DB loader

/**
 * Load monsters from web/zaggers_database.json (dict of 54) into the
 * server's monsters Map, replacing the 5 hardcoded entries.
 * Positions are spread deterministically so clients see a populated world.
 * Returns the number of monsters loaded.
 */
function loadMonstersFromDB(monstersMap, opts) {
  const o = opts || {};
  const max = o.max || 54;
  const dbPath = o.dbPath || path.join(__dirname, '..', 'web', 'zaggers_database.json');
  const raw = fs.readFileSync(dbPath, 'utf8');
  const db = JSON.parse(raw);
  const dict = db.monsters || {};
  const entries = Object.values(dict).slice(0, max);
  monstersMap.clear();
  let i = 0;
  for (const e of entries) {
    const id = `m_${500 + i}`;
    const hp = Number(e.hp) > 0 ? Number(e.hp) : 50;
    monstersMap.set(id, {
      id,
      key: e.id || id,
      name: String(e.name || e.id || 'Monster'),
      x: 120 + ((i * 173) % 1760), // deterministic spread across 0..2000
      y: 100 + ((i * 211) % 900),
      hp,
      max_hp: hp,
      atk: Number(e.atk) || 5,
      zeny: Number(e.zeny) || 50,
      level: Number(e.level) || 1,
    });
    i += 1;
  }
  return monstersMap.size;
}

module.exports = {
  WORLD_MIN_X,
  WORLD_MAX_X,
  WORLD_MIN_Y,
  WORLD_MAX_Y,
  MOVE_THROTTLE_MS,
  ATTACK_THROTTLE_MS,
  CHAT_THROTTLE_MS,
  CHAT_MAX_LEN,
  MAX_PAYLOAD_BYTES,
  clamp,
  escapeChat,
  encodeFrameHardened,
  encodePing,
  encodePong,
  parseFrames,
  feedSocket,
  startHeartbeat,
  handleClientPacketHardened,
  loadMonstersFromDB,
};
