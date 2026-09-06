# Collision, Walls & Doors Pass

**Scope owned:** collision detection, wall/door prop types + placement in map data (`web/index.html`, `web/editor.html`, `web/maps/aethelgard.json`). Sibling agents working the same files concurrently owned movement-target/pathfinding/travel-UI, sprite/animation frame logic, and HUD CSS — none of that was touched here.

## 0. Starting-state discovery

`vault/ENGINE_INFRA_AUDIT.md` describes an existing `checkCollision()` (dynamic `currentMapBounds`, `customTileMap` border tiles, type-based `envStructures` radii). On the `integration` branch handed to this pass, **no such function existed** — no collision system of any kind was present in `web/index.html`; the player only clamped to `currentMapBounds`. A leftover historical script (`scripts/update_collision_and_class_fix.py`) shows the audit's description matches an earlier, since-removed implementation. The collision engine below was built fresh to match that described design, then **merged with a second, independently-built `checkCollision()`** that landed on `master` from a parallel "town-buildings" session partway through this work (see §4).

## 1. Entity collision (NPCs & monsters)

Before this pass the player (and monsters) could walk straight through NPCs and live monsters — only tile bounds were enforced. Added:

- `ENTITY_COLLISION_RADIUS` (0.55 world units) + `MOVER_SELF_RADIUS` (0.35) — deliberately kept **below** the existing monster attack range (1.2 tiles, see the aggro-pursuit block in `render()`), so a chasing monster still reaches attack range even though it can no longer stand fully on top of the player.
- `isPositionBlocked(wx, wy, opts)` checks live NPCs and alive monsters (`m.hp > 0`) in addition to env structures/bounds/border tiles. `opts` lets a caller exclude itself (`ignorePlayer`, `excludeMonster`) or skip a category (`ignoreNpcs`, `ignoreMonsters`).
- `moveWithCollision(mover, stepX, stepY, opts)` — the axis-slide helper: tries the full diagonal step, then falls back to sliding along whichever single axis is clear. This is the same "slide along the wall" pattern the pre-existing tile-bounds clamp already used, just generalized so both env structures and entities can block a step without ever producing a hard, un-slidable stop.
- Wired into **both** existing movement paths without changing their shape: the WASD block and the click-to-move/NPC-approach follow block in `render()`. Click-to-move now also cancels a stuck target (`player.targetWx/Wy = player.wx/wy`) if a step is fully blocked on both axes, so the player doesn't grind forever against an obstacle.
- Monster wander/pursuit movement also routes through `moveWithCollision` (env structures + player only — monsters intentionally don't collide with each other or NPCs, keeping the AI simple) so monsters slide along walls instead of clipping through them.
- Floating text / click-ripples / projectiles are untouched — they never call the collision helpers.

## 2. Wall props with real collision

Generated four new sprites via `scripts/generate_wall_door_assets.py` (follows `scripts/generate_env_assets.py` / `generate_env_expansion.py` conventions — flat isometric polygons + oval drop shadow, saved to both `assets/tiles_ff/` and `web/assets/tiles_ff/`):

- `env_wall_curtain.png` (96×128, anchor 48,116) — coursed-stone battlement wall segment, same footprint class as the existing `env_palisade_wall`/`env_briar_wall`.
- `env_wall_corner.png` (96×144, anchor 48,132) — two stone faces meeting at a corner edge.
- `env_gatehouse.png` (128×160, anchor 64,148) — twin-tower gate structure with a dark archway cut through the middle.
- `env_door.png` (128×96, 2-frame sheet: frame 0 closed / frame 1 open) — see §3.

**Mid-pass merge conflict:** a parallel "town-buildings" session landed its own `checkCollision(wx, wy)` on `master` while this work was in progress, referencing sprite names `env_wall_curtain` / `env_wall_corner` / `env_gatehouse` that **did not yet exist as files anywhere in the repo** (their `build_aethelgard_town.py` skips missing optional prop types at runtime, so it silently never placed any). Their code also assumed different pixel dimensions for `env_wall_corner` (96×144) and `env_gatehouse` (128×160) than this pass's first draft (96×128 / 160×192). Resolution: **regenerated both assets at the master-side canonical dimensions** and updated this pass's map-authoring script to match, so there is now exactly one set of dimensions used consistently by `web/editor.html`'s `ENV_PROPS`, `scripts/build_aethelgard_town.py`'s `PROP_META`, and the placed instances in `aethelgard.json`.

Collision radii (`ENV_COLLISION_RADII` in `web/index.html`) were merged from both sessions' independent tuning — master's broader table (which also covers the new `env_house_*` building types) is the base; this pass folds in `env_door`'s open/closed state as a special case rather than a static radius. `env_gatehouse` and `env_stained_arch` are exempted from blocking entirely — their art depicts an open archway through the middle, and the flanking curtain-wall/corner segments are what actually seal the perimeter.

**Placement (Aethelgard):** `scripts/add_aethelgard_walls_doors.py` adds a walled ring around the central Obelisk Plaza district (`subRegions` bounds -9..9 both axes) — `env_wall_curtain` segments every 2 tiles along all four edges, `env_wall_corner` at the four corners, and an `env_gatehouse` marking each of the four plaza entrances (aligned toward Rampart Gate/Gatewatch, Wetstone Docks, Kestrel Market/Lantern Rows, and Ashen Ward/High Temple) with a 3-tile-wide gap left open so the plaza is never sealed. The script is idempotent (re-running replaces only its own marked entries) and targets `web/maps/aethelgard.json` directly. 64 total `envStructures` in Aethelgard after this pass (was 28).

## 3. Interactive doors

Added `env_door` prop type. **Design choice: proximity-based auto-open/close**, not click-to-open — click handling in `render()`'s mousedown listeners is shared territory with the movement-target/travel-UI pass, so this stays self-contained to the env-structures/collision code:

- `updateDoors()` (called once per frame from the same spot `checkZoneExits()` already runs) opens any door within `DOOR_OPEN_RADIUS` (2.0 tiles) of the player and resets its close timer; once the player moves away, a `DOOR_CLOSE_DELAY_FRAMES` (90 frames, ~1.5s) countdown closes it again.
- `initEnvState()` stamps `open`/`doorCloseTimer` onto every `env_door` instance the moment a map loads (mirrors the existing `initMonsterState()` convention), called from both `applyZoneMapData()` and `loadCustomMapData()`.
- Collision: closed doors block (radius 0.9, matching the sprite's frame footprint); open doors are skipped entirely in `isPositionBlocked()`.
- Rendering: `env.type === 'env_door'` slices frame 0 (closed) or frame 1 (open) from the 2-frame sheet based on `env.open`, following the same frame-stepped pattern already used for `env_torch_brazier`.

**Placement (Aethelgard):** 4 doors at building entrances — Kestrel Consignment House (shop), Elder's House (guild-hall/town-elder equivalent), High Temple Nave (temple), and The Barnacle Tavern — each offset ~2 tiles from its building's own collision radius so the door and building footprint don't overlap.

## 4. Rebase / merge notes

- Rebased cleanly onto `integration` (already contains master's tip + mobile/graphics passes; no conflicts).
- `origin/master` moved past `integration` mid-pass (11-class/66-skill DB expansion, new hero sprites, a "town-buildings" pass adding `env_house_smithy/temple/guild/inn/row`, and the parallel `checkCollision()` described in §2). Merged `origin/master` in before the final commit.
- **Non-trivial conflicts resolved** (all in `web/index.html` / `web/editor.html`):
  1. `envSpriteNames` / `allSpriteNames` arrays — both sides added new entries; concatenated additively.
  2. `web/editor.html` `ENV_PROPS` — both sides added `env_wall_curtain`/`env_wall_corner`/`env_gatehouse` with **different dimensions**; adopted master's (already referenced by their generator script) and kept this pass's `env_door` addition alongside their new house types.
  3. Two unrelated features landed adjacent to each other in the same function-boundary region (`flashBarOnDrop` HUD-flash helper from `integration` vs. `updateJobAdvancementUI`/`promoteJobClass` from master) — concatenated both, no logic overlap.
  4. **The real collision conflict**: master's movement-loop hunks called a bare `checkCollision(wx, wy)` (bounds + `tile_town_border` w/ 2.5-tile exit-gap tolerance + env-structure radius table, no entity awareness); this pass's hunks called `moveWithCollision(...)` (this pass's entity+door-aware wrapper). Resolved by **folding master's tile-border/exit-gap/bounds logic into this pass's `isPositionBlocked()`** as its base layers, keeping the entity/door layer on top, and kept `checkCollision(wx, wy)` alive as a thin backward-compatible alias (`isPositionBlocked` with all entity checks disabled) in case anything else still expects that name. There is now exactly one collision function backing both call sites.
- `web/maps/aethelgard.json` and `web/zaggers_database.json` merged cleanly (master never touched the former; this pass never touched the latter).
- Regenerated `env_wall_corner.png`/`env_gatehouse.png` post-merge at the now-canonical dimensions (see §2) and re-ran `add_aethelgard_walls_doors.py` so the placed instances match.

## 5. Regressions checked

- Zone-exit collision-gap logic (`customTileMap` `tile_town_border` + 2.5-tile exit tolerance) — now lives inside the merged `isPositionBlocked()`, unchanged behavior, verified via the merged `checkZoneExits()` still calling into it correctly through the border-tile branch.
- Existing WASD/click-to-move axis-slide feel — preserved; `moveWithCollision()` uses the identical "full diagonal, then per-axis fallback" shape both pre-existing collision drafts already used.
- Monster wander/pursuit and NPC-dialog-proximity logic — untouched aside from routing monster stepping through `moveWithCollision()`.

## 6. Validation performed

- `node --check` on the extracted `<script>` contents of `web/index.html` and `web/editor.html` (both OK) after every structural edit and again post-merge.
- `python -m json.tool` on every `web/maps/*.json` and `web/zaggers_database.json` (all valid) post-merge.
- Manual in-browser smoke test (local static server): character creation → Aethelgard load → gatehouse/wall/fountain render correctly with no console errors beyond two pre-existing missing NPC sprite 404s (`npc_militia.png`, `npc_smuggler.png`, unrelated to this pass); `isPositionBlocked()` confirmed to return `true` at a wall's position and `false` in open plaza; door proximity open + delayed auto-close confirmed via direct function calls; NPC-position entity blocking confirmed.

## Files touched

- `web/index.html` — collision engine (`ENV_COLLISION_RADII`, `isPositionBlocked`, `moveWithCollision`, `checkCollision` alias), door state/update/render, sprite manifest entries.
- `web/editor.html` — `ENV_PROPS` entries for `env_wall_curtain`/`env_wall_corner`/`env_gatehouse`/`env_door`, sprite manifest entries.
- `web/maps/aethelgard.json` — 36 new `envStructures` (walls/corners/gatehouses/doors).
- `scripts/generate_wall_door_assets.py` (new) — asset generator.
- `scripts/add_aethelgard_walls_doors.py` (new) — idempotent map-authoring script.
- `assets/tiles_ff/` + `web/assets/tiles_ff/` — `env_wall_curtain.png`, `env_wall_corner.png`, `env_gatehouse.png`, `env_door.png`.

## Incident: temp write outside the assigned worktree (self-corrected)

Both new scripts initially hardcoded an absolute path to the shared checkout (`D:\ai-studio\Zaggers\...`) instead of this worktree. This briefly wrote 4 PNGs and an `aethelgard.json` edit into the shared checkout used by other live sessions. Caught immediately: the shared-checkout `aethelgard.json` was restored to its exact `HEAD` content (via `git show HEAD:...` read back into a plain file copy — no git operations were run against the shared checkout, only against this worktree), the 4 stray PNGs were deleted from the shared checkout, and both scripts were fixed to target this worktree before re-running. Verified afterward: shared checkout's `aethelgard.json` byte-identical to `HEAD` (28 `envStructures`, matching pre-incident state), and this worktree has its own correct copies of all 4 generated assets.
