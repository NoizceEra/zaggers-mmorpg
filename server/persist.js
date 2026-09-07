'use strict';
/**
 * Zaggers server persistence — DROP-IN, does NOT modify server.js by itself.
 *
 * Zero-dependency JSON file store (no sqlite3 / better-sqlite3 required).
 * Uses only Node built-ins: fs / path / crypto.
 *
 * Layout (created on demand):
 *   server/data/players.json            — { [playerId]: playerRecord }
 *   server/data/sessions.json           — { [token]: { playerId, createdAt, lastSeen } }
 *   server/data/snapshots/monsters-<ts>.json (+ monsters-latest.json)
 *
 * Guarantees:
 *  - Atomic writes via tmp file + rename (crash-safe, no half-written JSON).
 *  - Load on boot (players + sessions caches hydrated lazily / via loadAll()).
 *  - Save on disconnect (call savePlayer + deleteSession from close handler).
 *  - Periodic save via startAutosave(clientsMap, 30_000) (saveAll every 30 s).
 *  - Session tokens via crypto.randomUUID() (uuid v4).
 *
 * Player shape mirrors server/server.js upgrade handler:
 *   { id, name, class_id, x, y, dir,
 *     hp, max_hp, sp, max_sp, zeny,
 *     str, agi, vit, int, dex, luk,
 *     ...extras (level, exp, inventory[], equip{}, updatedAt passthrough) }
 * zeny / stats are persisted verbatim so kills + stat_add survive restarts.
 *
 * API:
 *   loadPlayer(id) -> record|null (deep copy)
 *   savePlayer(p)  -> persisted record (deep copy); throws on missing p.id
 *   loadAll()      -> { [id]: record } (deep copy of cache, hydrates from disk)
 *   saveAll(clientsMap|iterable) -> count saved
 *   createSession(playerId) -> token (uuid, persisted)
 *   resolveSession(token)   -> playerId|null (updates lastSeen)
 *   deleteSession(token)    -> true if removed
 *   snapshotMonsters(monstersMap) -> snapshot file path
 *   loadLatestMonsterSnapshot()   -> array|null
 *   startAutosave(clientsMap, intervalMs=30000) -> timer (unref'd)
 *   stopAutosave(timer)
 *
 * HOW TO HOOK INTO server.js (manual, see server/PERSISTENCE_NOTES.md):
 *   const Persist = require('./persist.js');
 *   // on upgrade: player = Persist.loadPlayer(savedId) || freshDefault; token = Persist.createSession(player.id)
 *   // on close/error: Persist.savePlayer(player); Persist.deleteSession(token);
 *   // on boot + interval: Persist.startAutosave(clients, 30000);
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const DATA_DIR = process.env.PERSIST_DATA_DIR
  ? path.resolve(process.env.PERSIST_DATA_DIR)
  : path.join(__dirname, 'data');
const PLAYERS_FILE = path.join(DATA_DIR, 'players.json');
const SESSIONS_FILE = path.join(DATA_DIR, 'sessions.json');
const SNAPSHOT_DIR = path.join(DATA_DIR, 'snapshots');
const LATEST_SNAPSHOT_FILE = path.join(SNAPSHOT_DIR, 'monsters-latest.json');

const AUTOSAVE_DEFAULT_MS = 30000;
const MAX_ZENY = 999999;
const VALID_STATS = ['str', 'agi', 'vit', 'int', 'dex', 'luk'];
const VALID_DIRS = new Set(['up', 'down', 'left', 'right']);

// ---------------------------------------------------------------------------
// In-memory caches (hydrated from disk on first use = "load on boot")
// ---------------------------------------------------------------------------
let _playersCache = null;  // { [id]: record }
let _sessionsCache = null; // { [token]: { playerId, createdAt, lastSeen } }

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function readJsonFile(filePath, fallback) {
  try {
    const raw = fs.readFileSync(filePath, 'utf8');
    if (!raw.trim()) return fallback;
    return JSON.parse(raw);
  } catch (err) {
    if (err && err.code === 'ENOENT') return fallback;
    // Corrupt JSON: back it up once, then start fresh rather than crash boot.
    try {
      ensureDir(path.dirname(filePath));
      const bak = `${filePath}.corrupt-${Date.now()}.bak`;
      fs.copyFileSync(filePath, bak);
    } catch (_) { /* best effort */ }
    return fallback;
  }
}

/** Atomic write: tmp in same dir + fsync + rename (POSIX + Win safe). */
function atomicWriteJson(filePath, value) {
  ensureDir(path.dirname(filePath));
  const tmp = `${filePath}.${process.pid}.${Date.now()}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(value, null, 2), 'utf8');
  try {
    const fd = fs.openSync(tmp, 'r');
    try { fs.fsyncSync(fd); } catch (_) { /* fsync best-effort on Win */ }
    fs.closeSync(fd);
  } catch (_) { /* noop */ }
  fs.renameSync(tmp, filePath);
  return filePath;
}

function _players() {
  if (_playersCache === null) {
    const raw = readJsonFile(PLAYERS_FILE, {});
    _playersCache = (raw && typeof raw === 'object' && !Array.isArray(raw)) ? raw : {};
  }
  return _playersCache;
}

function _sessions() {
  if (_sessionsCache === null) {
    const raw = readJsonFile(SESSIONS_FILE, {});
    _sessionsCache = (raw && typeof raw === 'object' && !Array.isArray(raw)) ? raw : {};
  }
  return _sessionsCache;
}

function _flushPlayers() {
  atomicWriteJson(PLAYERS_FILE, _players());
}

function _flushSessions() {
  atomicWriteJson(SESSIONS_FILE, _sessions());
}

function deepCopy(v) {
  return JSON.parse(JSON.stringify(v));
}

function num(v, fallback) {
  const n = Number(v);
  return Number.isFinite(n) ? n : fallback;
}

function clampInt(v, lo, hi, fallback) {
  const n = Math.floor(num(v, fallback));
  if (!Number.isFinite(n)) return fallback;
  if (n < lo) return lo;
  if (n > hi) return hi;
  return n;
}

/**
 * Sanitize a player record to the server.js shape + forward-compat extras.
 * Unknown extra keys (level/exp/inventory/equip/createdAt) pass through so a
 * future inventory system does not lose data. Numbers are clamped to sane
 * bounds; zeny capped at MAX_ZENY (matches hardened patch cap).
 */
function sanitizePlayer(p) {
  if (!p || typeof p !== 'object') throw new Error('savePlayer: player object required');
  const id = String(p.id || '');
  if (!id) throw new Error('savePlayer: player.id required');
  const rec = {
    id,
    name: String(p.name || `Novice_${id}`).slice(0, 32),
    class_id: String(p.class_id || 'knight').slice(0, 32),
    x: clampInt(p.x, 0, 2000, 320),
    y: clampInt(p.y, 0, 2000, 240),
    dir: VALID_DIRS.has(p.dir) ? p.dir : 'down',
    hp: clampInt(p.hp, 0, 99999, 180),
    max_hp: clampInt(p.max_hp, 1, 99999, 180),
    sp: clampInt(p.sp, 0, 99999, 50),
    max_sp: clampInt(p.max_sp, 1, 99999, 50),
    zeny: clampInt(p.zeny, 0, MAX_ZENY, 0),
    updatedAt: new Date().toISOString(),
  };
  for (const s of VALID_STATS) rec[s] = clampInt(p[s], 1, 999, 10);
  // Forward-compat extras (DB items/inventory, level/exp) — passthrough.
  if (p.level !== undefined) rec.level = clampInt(p.level, 1, 999, 1);
  if (p.exp !== undefined) rec.exp = clampInt(p.exp, 0, 999999999, 0);
  if (Array.isArray(p.inventory)) {
    rec.inventory = p.inventory
      .filter((e) => e && typeof e === 'object')
      .slice(0, 200)
      .map((e) => ({ id: String(e.id || '').slice(0, 64), qty: clampInt(e.qty, 1, 9999, 1) }))
      .filter((e) => e.id);
  }
  if (p.equip && typeof p.equip === 'object' && !Array.isArray(p.equip)) {
    rec.equip = {};
    for (const [slot, itemId] of Object.entries(p.equip).slice(0, 16)) {
      rec.equip[String(slot).slice(0, 32)] = String(itemId).slice(0, 64);
    }
  }
  // Preserve createdAt across saves; stamp on first save.
  try {
    const prev = _players()[id];
    if (prev && prev.createdAt) rec.createdAt = prev.createdAt;
  } catch (_) { /* cache not ready — ignore */ }
  if (!rec.createdAt) rec.createdAt = rec.updatedAt;
  return rec;
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/** Load one player by id. Returns deep copy or null. */
function loadPlayer(id) {
  if (!id) return null;
  const rec = _players()[String(id)];
  return rec ? deepCopy(rec) : null;
}

/** Load every persisted player. Returns deep copy map. */
function loadAll() {
  return deepCopy(_players());
}

/** Persist one player (insert or update). Returns persisted deep copy. */
function savePlayer(p) {
  const rec = sanitizePlayer(p);
  _players()[rec.id] = rec;
  _flushPlayers();
  return deepCopy(rec);
}

/**
 * Persist every live player from the server's `clients` Map
 * (socket -> player) or any iterable of player objects.
 * Returns number of players saved.
 */
function saveAll(clientsOrPlayers) {
  if (!clientsOrPlayers) return 0;
  const players = typeof clientsOrPlayers.values === 'function'
    ? Array.from(clientsOrPlayers.values())
    : Array.from(clientsOrPlayers);
  let n = 0;
  for (const p of players) {
    if (p && p.id) {
      const rec = sanitizePlayer(p);
      _players()[rec.id] = rec;
      n += 1;
    }
  }
  if (n > 0) _flushPlayers();
  return n;
}

/** Issue a uuid session token bound to playerId. Persisted to sessions.json. */
function createSession(playerId) {
  const pid = String(playerId || '');
  if (!pid) throw new Error('createSession: playerId required');
  const token = (typeof crypto.randomUUID === 'function')
    ? crypto.randomUUID()
    : crypto.randomBytes(16).toString('hex');
  const now = new Date().toISOString();
  _sessions()[token] = { playerId: pid, createdAt: now, lastSeen: now };
  _flushSessions();
  return token;
}

/** Resolve token -> playerId (updates lastSeen). Returns null if unknown. */
function resolveSession(token) {
  if (!token) return null;
  const s = _sessions()[String(token)];
  if (!s) return null;
  s.lastSeen = new Date().toISOString();
  _flushSessions();
  return s.playerId;
}

/** Delete a session token (call on disconnect). Returns true if removed. */
function deleteSession(token) {
  if (!token) return false;
  const k = String(token);
  if (Object.prototype.hasOwnProperty.call(_sessions(), k)) {
    delete _sessions()[k];
    _flushSessions();
    return true;
  }
  return false;
}

/** Remove all sessions belonging to a player (e.g. duplicate login). */
function deleteSessionsForPlayer(playerId) {
  const pid = String(playerId || '');
  if (!pid) return 0;
  let n = 0;
  for (const [tok, s] of Object.entries(_sessions())) {
    if (s && s.playerId === pid) {
      delete _sessions()[tok];
      n += 1;
    }
  }
  if (n > 0) _flushSessions();
  return n;
}

/**
 * Snapshot monster world state for crash recovery / debugging.
 * Accepts the server's `monsters` Map (id -> monster) or a plain object.
 * Writes snapshots/monsters-<timestamp>.json + monsters-latest.json.
 * Returns the timestamped file path.
 */
function snapshotMonsters(monstersMap) {
  ensureDir(SNAPSHOT_DIR);
  const entries = monstersMap && typeof monstersMap.values === 'function'
    ? Array.from(monstersMap.values())
    : Object.values(monstersMap || {});
  const payload = {
    takenAt: new Date().toISOString(),
    count: entries.length,
    monsters: entries.map((m) => ({
      id: String(m.id || ''),
      key: String(m.key || m.id || ''),
      name: String(m.name || 'Monster').slice(0, 64),
      x: clampInt(m.x, 0, 2000, 0),
      y: clampInt(m.y, 0, 2000, 0),
      hp: clampInt(m.hp, 0, 9999999, 0),
      max_hp: clampInt(m.max_hp, 1, 9999999, 50),
      atk: clampInt(m.atk, 0, 99999, 5),
      zeny: clampInt(m.zeny, 0, MAX_ZENY, 50),
      level: clampInt(m.level, 1, 999, 1),
    })).filter((m) => m.id),
  };
  const fname = `monsters-${Date.now()}.json`;
  const file = path.join(SNAPSHOT_DIR, fname);
  atomicWriteJson(file, payload);
  atomicWriteJson(LATEST_SNAPSHOT_FILE, payload);
  // Best-effort retention: keep newest 20 timestamped snapshots.
  try {
    const files = fs.readdirSync(SNAPSHOT_DIR)
      .filter((f) => /^monsters-\d+\.json$/.test(f))
      .sort()
      .reverse();
    for (const old of files.slice(20)) {
      try { fs.unlinkSync(path.join(SNAPSHOT_DIR, old)); } catch (_) { /* noop */ }
    }
  } catch (_) { /* noop */ }
  return file;
}

/** Load the most recent monster snapshot (array of monsters) or null. */
function loadLatestMonsterSnapshot() {
  const payload = readJsonFile(LATEST_SNAPSHOT_FILE, null);
  if (payload && Array.isArray(payload.monsters)) return deepCopy(payload.monsters);
  return null;
}

/**
 * Periodic autosave over the live `clients` Map (socket -> player).
 * "Save on 30 s interval" requirement. Timer is unref'd so it never
 * keeps the process alive on its own. Also snapshots monsters if a
 * monsters Map is supplied via opts.
 */
function startAutosave(clientsMap, intervalMs, opts) {
  const ms = num(intervalMs, AUTOSAVE_DEFAULT_MS) > 0 ? Math.floor(num(intervalMs, AUTOSAVE_DEFAULT_MS)) : AUTOSAVE_DEFAULT_MS;
  const o = opts || {};
  const timer = setInterval(() => {
    try {
      saveAll(clientsMap);
    } catch (err) {
      console.error('[Persist] autosave players failed:', err && err.message);
    }
    if (o.monsters) {
      try {
        snapshotMonsters(o.monsters);
      } catch (err) {
        console.error('[Persist] autosave monster snapshot failed:', err && err.message);
      }
    }
  }, ms);
  if (timer.unref) timer.unref();
  return timer;
}

function stopAutosave(timer) {
  if (timer) clearInterval(timer);
}

/** Test helper: clear in-memory caches so next call re-reads from disk. */
function _resetCacheForTests() {
  _playersCache = null;
  _sessionsCache = null;
}

module.exports = {
  DATA_DIR,
  PLAYERS_FILE,
  SESSIONS_FILE,
  SNAPSHOT_DIR,
  AUTOSAVE_DEFAULT_MS,
  loadPlayer,
  loadAll,
  savePlayer,
  saveAll,
  createSession,
  resolveSession,
  deleteSession,
  deleteSessionsForPlayer,
  snapshotMonsters,
  loadLatestMonsterSnapshot,
  startAutosave,
  stopAutosave,
  sanitizePlayer,
  _resetCacheForTests,
};
