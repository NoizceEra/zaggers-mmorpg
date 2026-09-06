# ENGINE & INFRASTRUCTURE AUDIT

**Scope:** `web/index.html` (2.5D iso renderer/HUD/combat), `web/editor.html`, `web/db_editor.html`, `server/server.js`, `scripts/*.gd` (Godot client). Written before the animation/juice pass so the fixes below can be cross-referenced against what shipped.

---

## 1. Godot vs. Web: which is the real game?

**Conclusion: the web client (`web/index.html` + `web/editor.html` + `web/maps/*.json`) is the actively developed game. The Godot project (`scripts/*.gd`, `scenes/*.tscn`, `server/server.js`) is a legacy/aspirational prototype that has been abandoned since the very first commit.** Evidence:

- **Git history.** The repo has exactly 3 commits. Commit 1 (`2a4065c`) introduced *both* the web engine and the entire Godot/server tree in one shot. Commits 2 and 3 (`edc2846`, `94e2444`) — the art expansion and the world-map build — touched **only** `web/**` and `vault/**`. Not a single byte of `scripts/*.gd` or `server/server.js` has changed since the initial commit. All six `.gd` files and `server.js` are frozen at their day-1 state while `web/index.html` has been rewritten twice.
- **Deployment config.** `vercel.json` sets `"outputDirectory": "web"` and only rewrites `/assets`, `/editor`, `/db_editor` into `web/`. There is no build step, asset pipeline, or hosting path for the Godot project at all — it cannot ship via the configured deploy.
- **Content divergence.** The Godot server (`server/server.js`) still spawns the original placeholder bestiary — `Poring`, `Goblin`, `Skeleton`, `Baphomet (Boss)` — using the pre-rename sprite filenames (`slime_green_ff`, `goblin_ff`, `skeleton_ff`, `boss_baphomet_ff`) that the art pass explicitly renamed away from (see `vault/ART_PIPELINE_REPORT.md` Task A: `slime_green_ff`→`gloopling_bellflower_ff`, `boss_baphomet_ff`→`verrocaine_sovereign_ff`, etc.). `scripts/monster.gd` hardcodes `if "Poring" in monster_name` / `if "Goblin" in monster_name` string matching against those same four legacy names. None of the 54-monster bestiary, the 7-zone map system, `zaggers_database.json`, or the class/skill/item expansion touched the Godot side at all — it has no knowledge any of that work exists.
- **`Play_Game.bat`** launches the Godot editor/project directly (`Godot_v4.6.2 --path ...`), and **`Run_Server.bat`** starts `server/server.js` — so there *is* a launcher path to the Godot game, but it boots into the frozen day-1 prototype (fixed 800x600 top-down 32px-grid `world.gd`, not the isometric engine), not the current game.
- **Networking is real but pointed at a toy backend.** `network_manager.gd` does correctly implement the RFC 6455 handshake/framing client-side and *is* wired to `server/server.js` (same message vocabulary: `welcome`/`player_move`/`player_attack`/`monster_hit`/`chat`/`stat_add`). It's not dead code in the sense of "never connects" — it's a complete, functional minimal multiplayer loop. But it's a parallel, disconnected toy: no shop UI wired to real items, no class data beyond the day-1 7 hero defs, no map/zone concept at all (`world.gd`'s `_build_isometric_terrain()` just tiles a fixed 900x700px rectangle with one texture region), and the web client has zero equivalent networking (no WebSocket client exists in `web/index.html` — `player.zeny`/HP/combat are entirely local/client-authoritative there).

**Recommendation:** Treat `scripts/*.gd`, `scenes/*.tscn`, and `server/server.js` as a shelved prototype, not a parallel production target. Continued investment should go into `web/index.html`. If real-time multiplayer is wanted for the web game eventually, the *protocol* in `server/server.js` (simple JSON-over-WS, zero dependencies) is a reasonable starting skeleton to port to a browser WebSocket client — but it would need the monster/zone data model rebuilt from scratch against `zaggers_database.json` and `web/maps/*.json`, not extended in place. Per the task brief, no Godot `.gd` changes were made in this pass since the audit shows it is not being pursued in parallel with the web client.

---

## 2. Correctness bugs found (web client)

### 2.1 Click-to-move ignored the loaded zone's bounds (FIXED)
`canvas.addEventListener('mousedown', ...)` clamped the click-to-move target with **hardcoded** `Math.max(-15, Math.min(15, worldPos.wx))` / `Math.max(-45, Math.min(45, worldPos.wy))` — leftover from the old single-map engine. Every other bounds check in the file (`checkCollision`, camera clamp, player WASD clamp, monster wander clamp) already reads the dynamic `currentMapBounds` set by `loadZoneMap()`. Aethelgard is a 64×64 map (`-31..31` both axes); this bug meant a player could never click-to-move (or click an NPC to walk to it) more than 15 tiles east/west or 45 tiles... actually less than the map's real 31/31 extent on X, silently clipping valid clicks in every zone. **Fixed** to clamp against `currentMapBounds` like everything else.

### 2.2 Monsters with `isAggro: false` never wander (FIXED)
Map JSON monster entries (`web/maps/*.json`) only carry `id/name/sprite/hp/maxHp/speed/isAggro/wx/wy` — no `targetWx/targetWy/dir/frame/attackCooldown/homeWx/homeWy`. The per-frame monster AI in `render()` reads `m.targetWx - m.wx` before any of those fields are ever initialized anywhere in the codebase. With `m.targetWx === undefined`, `Math.hypot(NaN, NaN)` is `NaN`, and the "pick a new wander target when close to the current one" condition (`... < 0.2`) is `false` forever (NaN comparisons are always false) — so a passive monster's wander target is never seeded and it never picks one, freezing it in place for its entire lifetime unless/until it becomes aggro. Every "safe hub" and passive monster in Gatewatch/Meadows/Sanctum was affected. **Fixed** by initializing `targetWx/targetWy/homeWx/homeWy/dir/frame/attackCooldown` on every monster the moment it's loaded (`applyZoneMapData()` and `loadCustomMapData()`), matching how NPCs already ship `dir`/`frame` pre-set in their JSON.

### 2.3 `env_campfire` / `env_lava_channel` marked `animated: true` but never animate
Both `web/index.html` and `web/editor.html` only special-case `env.animated && env.type === 'env_torch_brazier'` for frame-stepped animation. `env_campfire` and `env_lava_channel` map entries also set `animated: true` (see `web/editor.html` lines ~626/632 and the `ASSET_MANIFEST.md`-driven map data), but since their art (per `vault/ART_PIPELINE_REPORT.md`) is a single static 64×64 frame — not a 4-frame sheet like the brazier's 256×64 — there is nothing to frame-step. This isn't a crash, just a documented gap (`WORLD_BUILD_REPORT.md` §4.5). **Addressed in the animation pass** below via a procedural (no-new-art) flicker/glow overlay instead of frame-stepping, so the `animated: true` flag on these props now does something visible.

### 2.4 No player-death / monster-death handling
- Player `hp` can be driven to 0 by aggro monsters (`player.hp = Math.max(0, player.hp - dmg)`), but nothing reads `player.hp <= 0` — there's no death state, no respawn, no UI feedback. The player just keeps existing at 0 HP, immune to further visible harm (bar reads 0/max) but fully controllable. Not fixed in this pass (out of the animation/juice scope and would need a design decision — respawn point? game-over screen? — beyond "surgical"), but flagged here as the top correctness gap for a future pass.
- Monsters at `hp <= 0` were simply excluded from the draw list (`monsters.forEach(m => { if (m.hp > 0) ... })`) — an instant vanish with no death feedback. **Fixed** in the animation pass (see §4 below) with a fade/sink-out instead of a hard cut, without changing the respawn timer or zeny-award logic.

### 2.5 Minor: boss detection hardcodes a stale sprite name
`triggerAttack()`, the minimap dot renderer, and the in-render HP-bar color all check `m.rank === 'boss' || m.sprite === 'boss_baphomet_ff'`. The `|| m.sprite === 'boss_baphomet_ff'` half is dead weight now that every real boss in `web/maps/*.json` carries `rank: 'boss'` (per `WORLD_BUILD_REPORT.md` §3) and `boss_baphomet_ff` was renamed to `verrocaine_sovereign_ff` in the art pass — no monster in the shipped maps can ever match that sprite string anymore. Harmless (short-circuits to the `rank` check first) — left as-is since it's not incorrect, just vestigial; not worth touching under "surgical changes only."

---

## 3. Dead / duplicate code

- **`server/server.js` + all of `scripts/*.gd`** — see §1. Not "dead" in the sense of unreachable, but dead relative to the product: nothing in `web/**` references or loads them, and they encode an entirely superseded data model (4 hardcoded monsters, no zones, no bestiary/class/item DB).
- **`checkDistrictTransition()`** was previously defined-but-uncalled (noted as already fixed by the prior map-build pass — confirmed still wired into `render()` correctly, no regression).
- No other dead functions found in `web/index.html`/`web/editor.html` in this pass; the file is fairly lean for its size.

## 4. Architectural risks

1. **Two divergent clients maintained (nominally) in parallel.** Per §1, this is more "one abandoned prototype" than "two live clients," but the risk is real if anyone picks the Godot side back up without realizing how far it has drifted (different bestiary names, no zone/map system, no DB-driven items/skills). Whoever revives it should budget for a full rebuild of the data layer, not an incremental sync.
2. **No shared source of truth between `web/index.html`'s hardcoded `HERO_CLASSES` character-creator table and `zaggers_database.json`'s class definitions** (per `vault/CLASS_SKILL_ITEM_EXPANSION.md`) — the creator screen's 5 classes (Vanguard/Spellweaver/Shadowblade/Cleric/Ranger) are a separate, independently-maintained literal object, not sourced from the DB the DB editor edits. Any class balance change made in `db_editor.html` silently doesn't reach the character creator. Out of scope to refactor here (would touch a working, just-shipped feature), but worth flagging for a future consolidation pass.
3. **Client-authoritative combat.** All damage math, zeny rewards, and HP are computed and trusted entirely client-side in `web/index.html`. Fine for a single-player-feeling prototype; would need a real server (or a genuine rebuild of `server/server.js`'s protocol against the current data model) before any real multiplayer trust boundary matters.
4. **Level-gating on exits is advisory only** (already flagged in `WORLD_BUILD_REPORT.md` §4.3) — `minLevel` on `exits[]` is stored but never enforced. Confirmed still true; not touched (out of scope, needs a level-gate mechanic that doesn't exist yet).

## 5. Missing error handling

- `loadZoneMap()` / `applyZoneMapData()` catch fetch/parse failures (`try { ... } catch (err) { console.error(...) }`) but leave the game in whatever state it was in before the failed load — no user-facing "map failed to load" fallback. Low risk (the 7 registered maps are static files shipped with the build), not touched.
- Sprite draws are already guarded everywhere with `img && img.complete && img.naturalWidth > 0` before `drawImage` — this convention is applied consistently across players/NPCs/monsters/env/tiles. No missing guards found.
- `handleMapFileUpload` → `loadCustomMapData` has a try/catch around `JSON.parse` for string input but the resulting `mapData` object is never structurally validated (a malformed-but-parseable JSON blob, e.g. `tiles` as a non-object, would throw uncaught deeper in `applyZoneMapData`/`drawIsoDiamondTile`). Low risk since this is a developer-facing "Load Map" debug feature, not player-facing; not touched.

## 6. Performance concerns in the render/depth-sort loop

- `drawList` is rebuilt and fully re-sorted **every frame** (`Array.sort` each `render()` call) rather than only re-sorting when something moves. At current entity counts (a few dozen monsters/NPCs/props per zone) this is a non-issue — `Array.sort` on <100 elements is sub-millisecond — but it would not scale gracefully if zone population grows an order of magnitude. Not touched (premature to optimize at current scale; flagging for awareness).
- Per-monster the AI/movement loop does a fresh `Math.hypot` distance check against the player every frame per monster (fine at current counts) and the minimap redraws every entity every frame with fresh `Math.arc` calls (also fine at current counts, would want dirty-rect/offscreen-canvas caching only if the population or minimap size grows substantially).
- Tile draw range is already correctly bounded to `currentMapBounds ∩ (camera ± 20)` and frustum-culled (`iso.x/y` on-screen check) before drawing — this is the right pattern and scales fine even on the largest 64×64 maps.
- No object pooling for `floatingTexts`/`clickRipples` — they're spliced out of arrays every frame, which is fine at their small expected counts (a handful of live damage numbers at once) but would start to matter under heavy combat spam (e.g., a full 5-person party AoE-farming a boss). Not touched — genuinely not a problem yet.

## 7. Editor / DB Editor consistency

- `web/editor.html`'s depth-sort (`drawList.sort((a, b) => a.isoY - b.isoY)`) and tile-seam handling mirror `web/index.html` correctly (both use the `+ 0.5` seam-prevention pattern from `PIPELINE_AND_TOOLS.md` §2, both sort primarily on `isoY` per §3). No divergence found between the live game's render conventions and the editor's preview/playtest rendering.
- `web/db_editor.html` is a standalone CRUD panel over `zaggers_database.json` (classes/skills/items/monsters/zones) with local-storage persistence + JSON import/export; no correctness issues found in a functional read-through — every `render*()`/`load*Form()`/`update*()`/`delete*()` function set follows the same consistent pattern per entity type.

---

## 8. Summary of fixes shipped in this pass

See the accompanying commit for the full diff. In short:
1. Click-to-move/NPC-approach target now clamps to `currentMapBounds` instead of the old hardcoded `±15/±45`.
2. Monsters get their `targetWx/targetWy/homeWx/homeWy/dir/frame/attackCooldown` initialized on load so passive (`isAggro: false`) monsters actually wander instead of freezing forever.
3. Walk-cycle timing tightened for readability (see commit / README changes in `web/index.html` comments near the animation constants).
4. Attack got a windup + impact-frame feel instead of a single held frame.
5. Hit-flash (white flash) added on both monsters and the player when they take damage, alongside the existing floating combat numbers.
6. Monster death is now a fade + sink instead of an instant vanish.
7. Torch braziers, campfires, and lava channels get a procedural flicker/glow pulse (no new art needed); water tiles get a cheap animated shimmer highlight.

No changes were made to `web/zaggers_database.json` data, `vault/BESTIARY_EXPANSION.md`, `vault/WORLD_MAP_EXPANSION.md`, any `web/maps/*.json` file, or any `scripts/*.gd` file.
