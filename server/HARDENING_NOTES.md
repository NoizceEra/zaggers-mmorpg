# Zaggers server.js — Hardening Audit + Patch Notes

Source: `server/server.js` (233 lines, zero-dep RFC 6455 server).
Patch (drop-in, non-destructive): `server/server.patch.js` — `server.js` is untouched.
DB: `web/zaggers_database.json` → `monsters` dict, **54 entries** (verified).
Godot client: `scripts/network_manager.gd` (125 lines).

## 1. Bugs found (with line refs)

| # | Bug | Location | Impact |
|---|-----|----------|--------|
| B1 | **Single-`data`-event framing assumption.** `socket.on('data', buffer => decodeFrame(buffer))` (server.js:97-106) treats each TCP chunk as exactly one frame. TCP coalesces/splits: two chat+move frames in one chunk → second silently lost; one frame split across chunks → `decodeFrame` returns garbage/`null` and packet is dropped. | server.js:97-99, 165-193 | Lost moves/attacks, phantom disconnects under load. |
| B2 | **No fragmentation support.** `decodeFrame` ignores FIN/opcode 0x0; a fragmented client message is parsed as independent frames → JSON parse fails → dropped. | server.js:165-193 | Breaks large chat/welcome payloads and any fragmenting proxy. |
| B3 | **No ping/pong.** Opcodes 0x9/0xA never handled; no server heartbeat. Dead peers stay in `clients` forever and keep receiving `broadcast`. | server.js:165-229 | Ghost players, memory/FD leak. |
| B4 | **Jumbo (127 / 64-bit) frames dropped.** `payloadLen === 127 → return null` (server.js:175-177); `encodeFrame` also `return null` for len > 65535 (server.js:207-209). | server.js:175-177, 200-209 | Any payload > 64 KiB (large `welcome` with 54 monsters) is silently dropped. |
| B5 | **Trust client x/y.** `player.x = data.x ?? player.x` (server.js:125-126), no finite/clamp check; `dir` unvalidated. | server.js:124-129 | Teleport hacks, NaN poisoning (`{"x": 1e999}` → Infinity, `{"x":"pwn"}`), map escape. |
| B6 | **No rate limiting.** `move`/`attack`/`chat` have no throttle; attacker can flood `broadcast` (O(N) sockets per packet). | server.js:122-162, 221-229 | Move spam = every client gets spammed; chat flood; trivial DoS. |
| B7 | **Chat: no sanitize / length cap.** `String(data.text \|\| '')` rebroadcast verbatim, unbounded (server.js:150). | server.js:149-151 | HTML/JS injection in web client, oversized frames, broadcast amplification. |
| B8 | **Hardcoded 5 monsters vs DB 54.** `initMonsters()` (server.js:19-32) spawns Poring×2/Goblin/Skeleton/Baphomet; DB has 54 keyed monsters (`dustmote_wisp` …). Names/stats/positions diverge from DB. | server.js:19-32 | World empty vs design; client bestiary mismatch. |
| B9 | **Godot missing `monster_respawn` / `stats_update` handlers.** Server emits both (server.js:143, 158) but `scripts/network_manager.gd` `_parse_packet` only matches `welcome/player_join/player_move/player_attack/player_leave/monster_hit/chat/zeny_update` — respawn + stat updates are silently ignored. | network_manager.gd:73-100 | Killed monsters never visually respawn; stat-point UI never refreshes. Needs two new signals + match arms (snippet in §3). |

Also noted: `stat_add` accepts any `player[key]` (only guarded by `!== undefined`, server.js:154) — patch whitelists `str/agi/vit/int/dex/luk`; `zeny` gain is fixed 50 regardless of monster (patch uses `m.zeny || 50`, capped at 999999).

## 2. What the patch provides (`server/server.patch.js`)

- `parseFrames(buf, sock)` / `feedSocket(sock, chunk, onMessage)` — per-socket buffer (`sock._rxBuf`), multi-frame loop, bounds-checked 16-bit + **64-bit** (`readBigUInt64BE`, capped at 1 MiB), FIN + continuation (0x0) reassembly, ping→auto-pong, pong liveness, close handling, oversize/flood → close.
- `encodeFrameHardened` — 64-bit header path for > 65535 B (old code returned `null`).
- `startHeartbeat(clients)` — 30 s ping, destroys peers that never pong.
- `handleClientPacketHardened(socket, player, data, ctx)` — clamp x/y to **0..2000** (non-finite → keep old), `dir` whitelist, **move throttle 100 ms** / attack 250 ms / chat 800 ms per socket, **chat cap 200 chars + `&<>"'` escape**, `stat_add` whitelist, zeny cap.
- `loadMonstersFromDB(monsters, {max: 54})` — reads `web/zaggers_database.json`, clears the 5 hardcoded entries, spawns up to 54 with deterministic spread positions; preserves `{id, name, x, y, hp, max_hp}` shape clients already parse.

## 3. Proposed unified diff (summary — apply manually, `server.js` untouched)

```
 server/server.js | ~45 lines changed across 4 hunks (proposal only, not applied)
 - Hunk 1 (initMonsters, ~19-32): delete 5-entry literal; call
+   Hard.loadMonstersFromDB(monsters, { max: 54 });
 - Hunk 2 (data handler, ~96-106): replace single decodeFrame call; add per-socket buffer
+   socket._rxBuf = Buffer.alloc(0);
+   socket.on('data', (chunk) => Hard.feedSocket(socket, chunk, (msg) => {
+     try { Hard.handleClientPacketHardened(socket, player, JSON.parse(msg), ctx); }
+     catch (e) { /* ignore invalid packet */ }
+   }));
 - Hunk 3 (move/chat/stat_add, ~124-160): clamp + throttle + escape + whitelist
-    player.x = data.x ?? player.x;  →  + player.x = Hard.clamp(data.x, 0, 2000, player.x);
-    text: String(data.text||'')     →  + text: Hard.escapeChat(data.text) // 200-char cap
-    if (data.stat && player[data.stat] !== undefined) → + whitelist str/agi/vit/int/dex/luk
 - Hunk 4 (encodeFrame, ~200-209): add 64-bit branch
+   } else { header = Buffer.alloc(10); header[1] = 127; header.writeBigUInt64BE(BigInt(len), 2); }
```

Godot follow-up (not in this patch — needs `network_manager.gd` edit):

```gdscript
signal monster_respawned(id: String, hp: int, x: float, y: float)
signal stats_updated(player_data: Dictionary)
# in _parse_packet match:
    "monster_respawn":
        monster_respawned.emit(String(data.get("id","")), int(data.get("hp",0)), float(data.get("x",0)), float(data.get("y",0)))
    "stats_update":
        stats_updated.emit(data.get("player", {}))
```

## 4. Files created

- `server/server.patch.js` — drop-in hardened module (CommonJS, zero new deps).
- `server/HARDENING_NOTES.md` — this file.

`server/server.js` was **not modified**.

## 5. Verification

- `node --check server/server.patch.js` → exit 0 (syntax OK).
- `node --check server/server.js` → exit 0 (untouched, still parses).
- DB check: `monsters` dict length = **54**.
- No overwrite check: `git status`-equivalent / `Get-ChildItem server/` shows `server.js` mtime unchanged; only two new files added.
- Runtime wiring is intentionally **not** auto-applied — `feedSocket`/`handleClientPacketHardened`/`loadMonstersFromDB` require the 3 manual edits in §2/§3 (or a `require('./server.patch.js')` line) so behavior can't change silently.
