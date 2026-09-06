/**
 * Zaggers MMORPG - Zero-Dependency Node.js WebSocket Server (RFC 6455)
 * Manages real-time player movement, combat hits, chat, stat points, and monster state.
 */

const http = require('http');
const crypto = require('crypto');

const PORT = 8080;
const WS_GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11';

// Server State
const clients = new Map(); // socket -> { id, name, class_id, x, y, dir, hp, max_hp, sp, max_sp, zeny, str, agi, vit, int, dex, luk }
const monsters = new Map(); // id -> { id, name, type, x, y, hp, max_hp, target_id }
let nextPlayerId = 100;
let nextMonsterId = 500;

// Initialize World Monsters (Poring, Goblin, Skeleton, Baphomet)
function initMonsters() {
  const types = [
    { name: 'Poring', hp: 50, x: 200, y: 150 },
    { name: 'Poring', hp: 50, x: 280, y: 220 },
    { name: 'Goblin', hp: 120, x: 450, y: 300 },
    { name: 'Skeleton', hp: 180, x: 520, y: 180 },
    { name: 'Baphomet (Boss)', hp: 500, x: 800, y: 400 },
  ];
  types.forEach(m => {
    const id = `m_${nextMonsterId++}`;
    monsters.set(id, { id, name: m.name, x: m.x, y: m.y, hp: m.hp, max_hp: m.hp });
  });
}
initMonsters();

// Create HTTP Server
const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Zaggers MMORPG WebSocket Server Running\n');
});

// Upgrade HTTP to WebSocket
server.on('upgrade', (req, socket) => {
  const key = req.headers['sec-websocket-key'];
  if (!key) {
    socket.destroy();
    return;
  }
  const acceptKey = crypto
    .createHash('sha1')
    .update(key + WS_GUID)
    .digest('base64');

  const headers = [
    'HTTP/1.1 101 Switching Protocols',
    'Upgrade: websocket',
    'Connection: Upgrade',
    `Sec-WebSocket-Accept: ${acceptKey}`,
    '\r\n'
  ];
  socket.write(headers.join('\r\n'));

  // Create Player State
  const playerId = `p_${nextPlayerId++}`;
  const player = {
    id: playerId,
    name: `Novice_${playerId}`,
    class_id: 'knight',
    x: 320,
    y: 240,
    dir: 'down',
    hp: 180,
    max_hp: 180,
    sp: 50,
    max_sp: 50,
    zeny: 500,
    str: 10,
    agi: 10,
    vit: 10,
    int: 10,
    dex: 10,
    luk: 10
  };
  clients.set(socket, player);
  console.log(`[Server] Player connected: ${player.name} (${playerId})`);

  // Send Welcome & Initial State
  sendPacket(socket, {
    type: 'welcome',
    self: player,
    players: Array.from(clients.values()).filter(p => p.id !== playerId),
    monsters: Array.from(monsters.values())
  });

  // Broadcast Join to Others
  broadcast({ type: 'player_join', player }, socket);

  // Incoming Data Handler
  socket.on('data', buffer => {
    const message = decodeFrame(buffer);
    if (!message) return;
    try {
      const data = JSON.parse(message);
      handleClientPacket(socket, player, data);
    } catch (err) {
      // Ignore invalid packet
    }
  });

  // Disconnect Handler
  socket.on('close', () => {
    console.log(`[Server] Player disconnected: ${player.name}`);
    clients.delete(socket);
    broadcast({ type: 'player_leave', id: playerId });
  });

  socket.on('error', () => {
    clients.delete(socket);
    broadcast({ type: 'player_leave', id: playerId });
  });
});

// Packet Handler
function handleClientPacket(socket, player, data) {
  switch (data.type) {
    case 'move':
      player.x = data.x ?? player.x;
      player.y = data.y ?? player.y;
      player.dir = data.dir ?? player.dir;
      broadcast({ type: 'player_move', id: player.id, x: player.x, y: player.y, dir: player.dir }, socket);
      break;

    case 'attack':
      broadcast({ type: 'player_attack', id: player.id, target_id: data.target_id, dir: player.dir }, socket);
      if (data.target_id && monsters.has(data.target_id)) {
        const m = monsters.get(data.target_id);
        const dmg = Math.floor(15 + player.str * 1.5 + Math.random() * 8);
        m.hp = Math.max(0, m.hp - dmg);
        broadcast({ type: 'monster_hit', id: m.id, hp: m.hp, max_hp: m.max_hp, dmg, attacker_id: player.id });
        if (m.hp <= 0) {
          player.zeny += 50;
          sendPacket(socket, { type: 'zeny_update', zeny: player.zeny });
          setTimeout(() => {
            m.hp = m.max_hp;
            broadcast({ type: 'monster_respawn', id: m.id, hp: m.hp, x: m.x, y: m.y });
          }, 5000);
        }
      }
      break;

    case 'chat':
      broadcast({ type: 'chat', id: player.id, name: player.name, text: String(data.text || '') });
      break;

    case 'stat_add':
      if (data.stat && player[data.stat] !== undefined) {
        player[data.stat] += 1;
        if (data.stat === 'vit') player.max_hp += 15;
        if (data.stat === 'int') player.max_sp += 10;
        sendPacket(socket, { type: 'stats_update', player });
      }
      break;
  }
}

// WebSocket Framing Utilities (RFC 6455)
function decodeFrame(buffer) {
  if (buffer.length < 2) return null;
  const secondByte = buffer[1];
  const isMasked = (secondByte & 0x80) === 0x80;
  let payloadLen = secondByte & 0x7f;
  let offset = 2;

  if (payloadLen === 126) {
    payloadLen = buffer.readUInt16BE(2);
    offset += 2;
  } else if (payloadLen === 127) {
    return null; // Skip jumbo frames for simplicity
  }

  let maskKeys = null;
  if (isMasked) {
    maskKeys = buffer.slice(offset, offset + 4);
    offset += 4;
  }

  const payload = buffer.slice(offset, offset + payloadLen);
  if (isMasked && maskKeys) {
    for (let i = 0; i < payload.length; i++) {
      payload[i] ^= maskKeys[i % 4];
    }
  }

  return payload.toString('utf8');
}

function encodeFrame(text) {
  const payload = Buffer.from(text, 'utf8');
  const len = payload.length;
  let header;

  if (len <= 125) {
    header = Buffer.from([0x81, len]);
  } else if (len <= 65535) {
    header = Buffer.alloc(4);
    header[0] = 0x81;
    header[1] = 126;
    header.writeUInt16BE(len, 2);
  } else {
    return null;
  }

  return Buffer.concat([header, payload]);
}

function sendPacket(socket, packet) {
  if (socket.writable) {
    const frame = encodeFrame(JSON.stringify(packet));
    if (frame) socket.write(frame);
  }
}

function broadcast(packet, excludeSocket = null) {
  const frame = encodeFrame(JSON.stringify(packet));
  if (!frame) return;
  for (const [sock] of clients) {
    if (sock !== excludeSocket && sock.writable) {
      sock.write(frame);
    }
  }
}

server.listen(PORT, () => {
  console.log(`[Server] Zaggers WebSocket Server listening on port ${PORT}`);
});
