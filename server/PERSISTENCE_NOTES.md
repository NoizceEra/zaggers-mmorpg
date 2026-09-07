# Zaggers server persistence — Research + Notes

Source: `server/server.js` (in-memory `clients`/`monsters` Maps, `welcome`/`player_*`
objects, zeny + `stat_add` handling). Patch: `server/persist.js` (drop-in,
non-destructive). `server/server.js` was **not modified**.
DB: `web/zaggers_database.json` → `schemaVersion: 2`, 11 classes, 66 skills,
~26 items, 54 monsters (see `tools/check_db_drift.py` conventions).

## 1. What server.js keeps in memory today (with line refs)

| State | Location | Shape | Lost on restart? |
|---|---|---|---|
| `clients` | server.js:15, 105, 133–141 | `Map<socket, player>` where player = `{id, name, class_id, x, y, dir, hp, max_hp, sp, max_sp, zeny, str, agi, vit, int, dex, luk}`; defaults `p_100+`, `Novice_*`, class `knight`, pos 320/240, hp 180/180, sp 50/50, zeny 500, all stats 10 | Yes — entire map is RAM-only |
| `monsters` | server.js:16, 21–55 | `Map<id, {id, key, name, x, y, hp, max_hp, atk, zeny, level}>`, seeded from `db.monsters` (first 54, deterministic spread) with 5-entry legacy fallback | Yes — respawned from DB each boot |
| `welcome` packet | server.js:109–114 | `{type:'welcome', self: player, players: [...], monsters: [...]}` — the rejoin point: a returning player currently gets a **fresh** `player` object, never their old zeny/stats/position | Yes |
| zeny | server.js:162–163 | `player.zeny += (m.zeny \|\| 50)` on kill + `zeny_update` push; hardened patch caps at 999999 (`server.patch.js`) | Yes |
| stats | server.js:176–183 | `stat_add` → `player[stat] += 1`; `vit` → `max_hp += 15`, `int` → `max_sp += 10` | Yes |
| disconnect | server.js:132–141 | `close`/`error` → `clients.delete + player_leave` broadcast; **no save** | n/a |

## 2. What persist.js provides (`server/persist.js`, zero-dep)

- **Store:** `server/data/players.json` (`{[id]: record}`) + `server/data/sessions.json`
  (`{[token]: {playerId, createdAt, lastSeen}}`) + `server/data/snapshots/monsters-<ts>.json`
  (plus `monsters-latest.json`). Dirs/files created on demand.
- **Atomic writes:** tmp file in same dir → `fsync` (best-effort) → `renameSync`.
  Corrupt JSON on boot is backed up to `*.corrupt-<ts>.bak` and treated as empty —
  boot never crashes on a half-written file.
- **Session tokens:** `crypto.randomUUID()` (fallback `randomBytes(16)`), persisted,
  `resolveSession` refreshes `lastSeen`, `deleteSession(token)` on disconnect.
- **Save triggers:** explicit `savePlayer(p)` on disconnect/kill/stat-change +
  `startAutosave(clients, 30000)` (unref'd 30 s interval over the live `clients` Map,
  optional `{monsters}` snapshot alongside).
- **Load on boot:** lazy-hydrated caches; `loadPlayer(id)` / `loadAll()` return deep
  copies so callers can't mutate the cache without saving.
- **Sanitization:** positions clamped 0..2000, zeny 0..999999, stats 1..999,
  `dir` whitelisted, `class_id` passthrough (DB has 11 classes; server default is
  `knight`). Forward-compat extras pass through: `level`/`exp`/`inventory[{id,qty}]`
  (max 200, item ids validated against 64-char strings — full `items` dict check is a
  future SQLite FK) / `equip{}` / `createdAt` preserved, `updatedAt` stamped.
- **Drift conventions** (per `tools/check_db_drift.py`): DB JSON stays the source of
  truth for classes/skills/items/monsters; `players.json` never duplicates DB stat
  definitions, only per-player values + item-id references.

API: `loadPlayer(id)` · `loadAll()` · `savePlayer(p)` · `saveAll(clientsMap)` ·
`createSession(playerId)` · `resolveSession(token)` · `deleteSession(token)` ·
`deleteSessionsForPlayer(playerId)` · `snapshotMonsters(monstersMap)` ·
`loadLatestMonsterSnapshot()` · `startAutosave(clients, ms, {monsters})` · `stopAutosave(t)`.

## 3. Integration snippet (3-line hook — apply manually, server.js untouched)

```js
const Persist = require('./persist.js');                       // (1) require once at top
// in upgrade handler, after building `player`: restore or resume session
// const saved = Persist.loadPlayer(clientSavedId); if (saved) Object.assign(player, saved);
// const token = Persist.createSession(player.id);
// on close/error, replace bare `clients.delete(socket)` with:
Persist.savePlayer(player); Persist.deleteSession(token); clients.delete(socket);
// on boot, after initMonsters(): start 30 s autosave (+ monster snapshots):
Persist.startAutosave(clients, 30000, { monsters });
```

Close-handler sketch (mirrors server.js:132–141):

```js
socket.on('close', () => {
  try { Persist.savePlayer(player); } catch (e) { console.error('[Persist]', e.message); }
  try { Persist.deleteSession(token); } catch (e) { /* noop */ }
  clients.delete(socket);
  broadcast({ type: 'player_leave', id: playerId });
});
```

Optional durability upgrades: `savePlayer(player)` after `zeny_update` and after
`stats_update`; `snapshotMonsters(monsters)` on `SIGINT`/`SIGTERM` before exit.

## 4. SQLite-upgrade path (better-sqlite3, when zero-dep is outgrown)

JSON is fine for dev/single-process (< few hundred players, 30 s full-file rewrites).
Move to SQLite when: concurrent writers, >1k players, item-dupe/clone exploits matter,
or crash-during-rename windows become unacceptable (WAL > tmp+rename).

```bash
npm i better-sqlite3
```

```sql
PRAGMA journal_mode = WAL;
CREATE TABLE IF NOT EXISTS players (
  id        TEXT PRIMARY KEY,
  name      TEXT NOT NULL,
  class_id  TEXT NOT NULL REFERENCES classes(id),  -- classes stay in zaggers_database.json until migrated
  x INTEGER NOT NULL DEFAULT 320, y INTEGER NOT NULL DEFAULT 240, dir TEXT NOT NULL DEFAULT 'down',
  hp INTEGER NOT NULL, max_hp INTEGER NOT NULL, sp INTEGER NOT NULL, max_sp INTEGER NOT NULL,
  zeny INTEGER NOT NULL DEFAULT 0 CHECK (zeny BETWEEN 0 AND 999999),
  level INTEGER NOT NULL DEFAULT 1, exp INTEGER NOT NULL DEFAULT 0,
  str INTEGER NOT NULL, agi INTEGER NOT NULL, vit INTEGER NOT NULL,
  int INTEGER NOT NULL, dex INTEGER NOT NULL, luk INTEGER NOT NULL,
  created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS inventory (
  player_id TEXT NOT NULL REFERENCES players(id) ON DELETE CASCADE,
  item_id   TEXT NOT NULL,            -- FK to items dict once items table exists
  qty       INTEGER NOT NULL CHECK (qty BETWEEN 1 AND 9999),
  PRIMARY KEY (player_id, item_id)
);
CREATE TABLE IF NOT EXISTS sessions (
  token TEXT PRIMARY KEY, player_id TEXT NOT NULL REFERENCES players(id) ON DELETE CASCADE,
  created_at TEXT NOT NULL, last_seen TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_sessions_player ON sessions(player_id);
```

Migration sketch: on first SQLite boot, `loadAll()` from `players.json` → `INSERT OR
REPLACE` per player + per-`inventory[]` row; keep writing a periodic JSON snapshot for
a rollback window. Keep `sanitizePlayer` as the validation boundary and swap
`atomicWriteJson` for prepared statements inside `BEGIN IMMEDIATE; … COMMIT;`.
Zeny ledger (append-only `zeny_events(player_id, delta, reason, at)`) is the next step
if dupe investigations need auditability.

## 5. Files created

- `server/persist.js` — drop-in JSON persistence module (CommonJS, zero new deps).
- `server/PERSISTENCE_NOTES.md` — this file.

`server/server.js` was **not modified**.

## 6. Verification

- `node --check server/persist.js` → exit 0.
- Runtime smoke (isolated temp dir via `PERSIST_DATA_DIR`, never port 8080):
  save → load roundtrip (zeny/stats/position/inventory), session create/resolve/delete,
  monster snapshot + latest reload, autosave timer start/stop. See task test output.
- No-overwrite check: `server.js` mtime/size unchanged; only `persist.js` +
  `PERSISTENCE_NOTES.md` (+ `data/` at runtime) added.
