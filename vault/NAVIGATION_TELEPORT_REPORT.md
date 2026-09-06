# NAVIGATION_TELEPORT_REPORT — Fast-Travel, Save-Crystal Binding & Pathfinding-Assisted Movement

**Scope owned by this pass:** MOVEMENT-TARGETING and TRAVEL/TELEPORT logic, plus the new travel UI panel — `web/index.html` only. No changes to collision-detection code, wall/door prop types, sprite/animation frame logic, or general HUD CSS styling (those remain sibling-owned).

Base: rebased onto `integration` (387f1de, which already carries master's tip plus the mobile-compatibility and graphics/VFX passes), then merged the two newer `master` commits (`377f7fa` 6 new hero classes + Stat-Driven Class Advancement, `50dde27` 66-skill/11-class DB schema) that landed after `integration` was cut. See "Merge notes" below for how that merge was resolved.

## 1. Fast-Travel / Teleportation System

- **Visited-zone tracking**: a `visitedZones` `Set` persisted to `localStorage` (`zaggers_visited_zones`). `applyZoneMapData()` calls `markZoneVisited(currentMapId)` every time a zone loads, so the travel list only ever offers realms the player has actually reached — never the full realm roster up front.
- **Travel UI**: a new `#travel-window` modal ("Kestrel Consignment — Travel Map") reusing the existing `.window-modal` / `.window-header` / `.shop-items` / `.shop-item` / `.buy-btn` classes verbatim for visual consistency with the Shop window — no new CSS component classes were introduced. `openTravelWindow()` populates one row per visited zone (current zone shown as "(here)" with no Warp button), and `travelToZone(mapId)` closes the modal and calls `loadZoneMap()`, using the player's bound save-crystal position in that zone if one exists (see §2), else the zone's default `spawn` point from its map JSON.
- **Entry point**: interacting with the existing Kafra NPC (`kafra_kestrel` in `aethelgard.json`) and choosing "🌀 Teleport to Wilderness Fields" now opens the travel window instead of the old hardcoded `loadZoneMap('meadows')` call. The "💾 Save Position & Heal" option now also calls `bindRespawnPoint()` (see §2) rather than only healing.

## 2. Save-Point / Respawn-Crystal Binding

- Confirmed via `web/maps/*.json` that every wilderness zone (`gatewatch`, `meadows`, `sanctum`, `spire`, `chasm`, `rootways`) already ships `env_crystal` envStructure props (e.g. "Bellflower Save Crystal", "Tidebreak Save Crystal", "Cinderfall Save Crystal", "Rimewind Save Crystal", "Nethergate Save Crystal", plus a few lore-marker crystals). Aethelgard has no `env_crystal` — its save/teleport interface is the Kafra NPC instead, matching `WORLD_LORE.md`.
- Clicking (or tapping, on touch) an `env_crystal` prop now hit-tests it the same way NPCs are hit-tested. Within interact range (≤2.2 world units) it opens `openCrystalDialog()` — a synthetic dialog reusing the existing `#npc-dialog-window` markup — offering "💠 Bind Respawn Point Here" and "🗺️ Open Travel Map". Clicking from farther away walks the player to it first (`pendingCrystalTarget`, mirroring the existing `pendingNpcTarget` pattern) and auto-opens the dialog on arrival.
- `bindRespawnPoint(mapId, wx, wy, label)` persists `{ mapId, wx, wy, name }` to `localStorage` (`zaggers_respawn_bind`) as `respawnBinding`.
- `respawnAtKafra()` (the existing death/respawn flow, unchanged in every other respect) now teleports to `respawnBinding` if one is set, falling back to Aethelgard (0,0) exactly as before when it isn't. This integrates with the existing `#player-death-modal` / `triggerPlayerDeath()` / `reviveOnSpot()` flow without modifying it.

## 3. Light Pathfinding (Grid A* + Waypoint Following)

- No `checkCollision` function exists anywhere in `web/index.html` today (confirmed by grep), and no envStructure carries a solidity/blocking flag — collision detection is explicitly a sibling pass's ownership per the task brief, so this pass does **not** invent its own wall/door solidity rules.
- Instead, `findPath(startWx, startWy, goalWx, goalWy)` is a self-contained, dependency-free grid A* over a coarse 1-world-unit grid clamped to `currentMapBounds`. Its walkability check, `isWalkableCell(wx, wy)`, consults `typeof checkCollision === 'function'` and defers to it when present — so the moment a sibling's collision system lands (via a future rebase/merge), obstacle-avoidance activates automatically with zero further changes here. Until then it degrades to the previous straight-line behavior via a `hasLineOfSight()` fast path (returns a single-waypoint path immediately when the direct line is clear, which is the common case with no collision grid registered).
- When a route isn't a straight line, the raw per-cell A* path is string-pulled down to the minimal set of line-of-sight waypoints, so movement stays smooth/diagonal rather than stair-stepping through every grid cell.
- **Stall watchdog** (the "at minimum" fallback requested in the brief): the main render-loop movement branch tracks how much closer the player has gotten to `player.targetWx/Wy` each frame; if that distance hasn't meaningfully changed for ~45 frames, it calls `recomputePlayerPath()` to get a fresh route rather than looping forever against an obstacle.
- `setMovementTarget(tx, ty)` is the single entry point used by every click/tap/minimap-click path: it clamps to `currentMapBounds` (preserving the `ENGINE_INFRA_AUDIT.md` §2.1 bounds-clamp fix verbatim — same `Math.max(min, Math.min(max, …))` clamp, just centralized instead of duplicated four times), computes the route via `findPath()`, and resets the stall watchdog. Manual WASD movement still clears any queued path immediately, as before.

## 4. Minimap Click-to-Travel

- The minimap (`#minimap-canvas`) previously had no click handling. A new `click` listener inverts the same padding/scale math `renderMinimap()` already uses internally for `worldToMinimap()`, converts the click to world coordinates, and calls `setMovementTarget()` — so a minimap click sets the same movement target (and gets the same pathfinding + click-ripple feedback) as clicking the main world view. Cursor is set to `pointer` via a JS property (not a new CSS rule) to hint at the new interaction.

## 5. Validation

- Extracted the single `<script>` block and ran `node --check`. Found one **pre-existing, unrelated** issue on `integration`: `getClassSkills(classId)` is declared twice (lines ~659 and ~2465 after this pass's edits) — a merge artifact from a prior pass, not touched or introduced by this one. Verified it predates this pass via `git show HEAD:web/index.html`. Worked around it only inside a throwaway validation copy (never in the real file) to confirm the rest of the script — including every addition in this report — has no syntax errors. Flagged as a separate follow-up task (`task_40eaea1d`) rather than fixed here, since the skill/class system is outside this pass's scope.
- Re-read the zone-exit (`checkZoneExits`) and click-to-move bounds-clamp code paths after editing; both are unchanged in behavior for the straight-line case (the §2.1 audit fix is preserved, just centralized in `setMovementTarget`).

## Merge notes

`master` had advanced two commits past `integration`'s base (`377f7fa` hero-class/sprite expansion, `50dde27` skills/classes DB schema) by the time this pass finished. Both touch `web/index.html` (~136 lines, mostly class-roster/creator-screen and skill-tree data, no overlap with the movement/travel/minimap/NPC-dialog regions this pass touched) and `web/db/zaggers_database.json`. Merged additively — see the merge commit for exact conflict resolution, if any arose.
