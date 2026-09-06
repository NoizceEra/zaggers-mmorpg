# WORLD BUILD REPORT — Phase 3 Map Expansion

**Status:** Aethelgard + Gatewatch Commons + Realms I & II fully built. Realms III–V shipped as connected entry-hub stubs (topology complete, sub-regions pending). Companion to `WORLD_MAP_EXPANSION.md`, `BESTIARY_EXPANSION.md`, `DATABASE_REGISTRY.md`, `ASSET_MANIFEST.md`.

---

## 1. What was built

Seven map JSON files were authored under `web/maps/`, each conforming exactly to the mapData schema `web/editor.html` saves/loads (`gridWidth`, `gridHeight`, `defaultTile`, `tiles` dict keyed `"wx,wy"`, `envStructures[]`, `npcs[]`, `monsters[]`), plus additive fields the editor safely ignores (`id`, `name`, `light`, `minLv`/`maxLv`, `boss`, `spawn`, `bounds`, `subRegions[]`, `exits[]`, `status`/`statusNote` on stubs). A generator script built them deterministically; the design content (layout, monster placement, prop clusters) was authored by hand against `WORLD_MAP_EXPANSION.md` / `BESTIARY_EXPANSION.md`.

**Zone ids, `gridWidth`/`gridHeight`/`defaultTile`, and every `subRegions[].id` match `web/zaggers_database.json`'s `zones[]` array exactly** (that array was already expanded with the full sub-region list by an earlier pass, per `DATABASE_REGISTRY.md`) — verified programmatically: every map's `id` equals its filename, every `subRegions[].id` this pass built is present in the DB's `zones[].subRegions[]`, and `gridWidth`/`gridHeight`/`defaultTile` match the DB row for that zone.

| Map file | Zone id | Dimensions (bounds) | Tiles painted | Props | NPCs | Monster spawns | Status |
|---|---|---|---|---|---|---|---|
| `aethelgard.json` | `aethelgard` | 64×64 (`-31..31` both axes) | 3,969 | 28 | 5 | 0 (safe hub, combat disabled) | **Full** |
| `gatewatch.json` | `gatewatch` | 32×32 (`-15..15`) | 961 | 8 | 1 | 7 | **Full** |
| `meadows.json` | `meadows` | 64×64 (`-31..31`) | 3,969 | 21 | 0 | 21 | **Full** |
| `sanctum.json` | `sanctum` | 64×64 (`-31..31`) | 3,969 | 15 | 0 | 21 | **Full** |
| `spire.json` | `spire` | 64×64 nominal / `-14..14, -2..30` built | 957 | 7 | 0 | 4 | **Stub hub** (Cinderfall Approach only) |
| `chasm.json` | `chasm` | 64×64 nominal / `-14..14, -2..30` built | 957 | 7 | 0 | 4 | **Stub hub** (Rimewind Pass only) |
| `rootways.json` | `rootways` | 64×64 nominal / `-14..14, -2..30` built | 957 | 6 | 0 | 4 | **Stub hub** (Nethergate Descent only) |

All seven files were validated with `node -e "JSON.parse(...)"` (all valid), cross-checked so every `exits[].targetMap` resolves to an existing map id, and cross-checked against `zaggers_database.json` as described above. The three stub realms' `gridWidth`/`gridHeight` are set to their DB-declared full size (64×64) as nominal metadata, while the actual playable `bounds` field (which is what the game client enforces for collision/camera) is restricted to the built entry-hub area — the difference is deliberate and documented in each file's `statusNote`.

### 1.1 Aethelgard — master town
Rebuilt as the 64×64 wheel layout from `WORLD_MAP_EXPANSION.md` §1: Obelisk Plaza at the hub, a square ring-road (`tile_town_brick`) separating six districts (Obelisk Plaza, Kestrel Market, Ashen Ward, High Temple, Lantern Rows, Wetstone Docks), and an outer wall (`tile_town_border`) with four gate breaks matching the four transit stubs table. NPCs were relocated into their lore-correct districts (Kestrel Consignment kafra in Kestrel Market, Obsidian Smithy blacksmith in Ashen Ward, Elder's House in Lantern Rows, a new tavern-keeper NPC in Wetstone Docks). Combat is disabled here (`combatDisabled: true`), matching the design doc.

### 1.2 Gatewatch Commons — tutorial fields (Lv 1–5)
Small hand-tuned map with a dirt path leading from the town gate to the "broken fence" north edge. Populated with the 4 tutorial monsters (`dustmote_wisp`, `gutter_ratkin`, `thatch_beetle`, `straw_effigy` rare) and a militia NPC.

### 1.3 Whispering Meadows (Lv 1–16) — Realm I, full build
All 5 sub-regions from the design doc are laid out along the wy-axis with Windmill Ridge as an eastward vista pocket: Bellflower Downs → Windmill Ridge (safe vista) → Thistlemarch Fen → Hollowroot Grove (hidden pocket, grovewarden_thistle rare) → Raider's Palisade (elite camp + Ordwin the Palisade Tyrant boss). 21 monster spawns use the correct bestiary ids for each sub-region. The Hollowroot one-way descent exit connects directly into Sunken Sanctum's Tidebreak Stair, matching the doc's realm-to-realm lateral route.

### 1.4 Sunken Sanctum (Lv 15–32) — Realm II, full build
Tidebreak Stair (entry) → Silt Warrens (smuggler cave, branches west) → Drowned Nave (central crossroads) → Glasslight Reliquary (hidden pocket, east) → Choirfall Deep (Hallowdeep boss). 21 monster spawns. The Bilge Steps shortcut exits back to Aethelgard's Wetstone Docks, and the main Dockgate Ferry exit returns to the town's south gate.

### 1.5 Realms III–V — connected stub hubs
Obsidian Spire, Glacial Chasm, and Umbral Rootways each ship as a single entry-hub sub-region (Cinderfall Approach / Rimewind Pass / Nethergate Descent) with a save crystal, a couple of representative monster spawns, and full exit wiring so the topology in `WORLD_MAP_EXPANSION.md` §0 is navigable end-to-end today:
- Aethelgard's Ashroad Caravan (W gate) → Obsidian Spire → (future Collapsed Skybridge) → Umbral Rootways
- Aethelgard's Rimewind Tramway (E gate) → Glacial Chasm → (future Thronehall) → Umbral Rootways
- Umbral Rootways has no town portal (per lore) — only reachable via the two stub hubs above.

Each stub map carries `"status": "stub_hub_only"` and a `statusNote` field pointing back to this report. **Remaining work:** the 3–5 named sub-regions per realm from `WORLD_MAP_EXPANSION.md` §5–§7 (Emberglass Terraces, The Slagworks, Collapsed Skybridge, Statuary of the Fallen, Crevasse Undershelf, Hoarfrost Vault, Bonemeal Hollows, The Weeping Boughs, Sanguine Terrace, Thorncradle Vault) plus their bosses (Vashkar, Sylveth, Verrocaine) still need to be laid out and populated — the palette entries for all their monsters already exist in `editor.html`'s `MONSTER_TYPES`, so this is pure level-layout work, not data-modeling work.

---

## 2. How zone transitions / portals work

The editor's map schema has no native "portal" entity type, so an additive `exits[]` array was introduced on the map JSON (ignored harmlessly by `editor.html`'s loader, which only requires `.tiles` and `.envStructures`):

```jsonc
"exits": [
  { "id": "rampart_gate", "wx": 0, "wy": -31, "radius": 2,
    "targetMap": "gatewatch", "targetWx": 0, "targetWy": 12,
    "label": "Rampart Gate → Gatewatch Commons", "minLevel": 15 }
]
```

In `web/index.html`:
- `MAP_REGISTRY` maps each zone id to its `web/maps/<id>.json` file.
- `loadZoneMap(mapId, spawnOverride)` fetches that file and calls `applyZoneMapData()`, which swaps in `tiles`/`envStructures`/`npcs`/`monsters`, plus the additive `bounds`, `defaultTile`, `exits`, `subRegions`, and `spawn` fields into new global state (`currentMapBounds`, `currentMapExits`, `currentMapSubRegions`, etc.).
- `checkZoneExits()` runs once per frame in the main `render()` loop: if the player is within an exit's `radius`, it calls `loadZoneMap()` for the target with the exit's `targetWx/targetWy` as the new spawn point. A short `exitCooldownFrames` grace period prevents immediately bouncing back through the matching exit on the other side.
- `checkDistrictTransition()` (previously dead code — defined but never called) is now wired into the render loop and shows the floating district banner + updates the minimap title by matching the player's position against the loaded zone's `subRegions[]` bounding boxes, instead of the old hardcoded coordinate thresholds.
- Collision bounds (`checkCollision`), camera clamping, the visible-tile draw range, and monster wander-leash logic all now read from `currentMapBounds` instead of the old hardcoded `-28..28 / -45..45` constants.
- The old single hardcoded procedural tile-painting function (`drawIsoDiamondTile`'s giant if/else chain keyed to fixed world coordinates) was replaced with a plain `customTileMap[key] || currentMapDefaultTile` lookup — this is the literal "replace the placeholder" step.
- The manual "Load Map" JSON upload feature (`loadCustomMapData`, used by the 📁 button and browser localStorage persistence) was extended to apply the same additive fields, so a hand-exported map from `editor.html` picks up its own bounds/exits/subRegions when loaded into the live game too.
- The legacy Elder quest ("defeat Baphomet") was updated to reference Ordwin the Palisade Tyrant (now the reachable Lv-16 boss in Whispering Meadows) via a generalized `defeatedBosses` Set keyed by monster instance id and a `rank: 'boss'` field on boss monster entries — the old check (`monsters.find(m => m.id === 12)`) only worked because everything was one hardcoded map; with realms now separate fetched maps, boss-kill tracking had to survive a zone change.

In `web/editor.html`:
- `TERRAIN_TILES`, `ENV_PROPS`, `MONSTER_TYPES`, `NPC_TYPES`, and `allSpriteNames` were all extended with the new Phase 3 ids from `ASSET_MANIFEST.md` / `BESTIARY_EXPANSION.md` (19 tiles, 38 props, ~50 monsters, 2 NPCs) so the editor's palette can author/inspect the new maps' content, not just view thumbnails for pre-existing assets.
- A new "Load World Zone" panel with 7 buttons (`loadWorldZone(mapId)`) fetches straight from `maps/<id>.json` into the editor's live `mapData`, so any of the shipped zones can be opened, tweaked, and re-exported directly.
- No changes were made to the editor's core paint/select/eraser tools, playtest mode, or JSON export/import — those already handled the additive keys correctly (an unknown top-level key round-trips through `exportMapJSON()`/`importMapFile()` untouched).

Animation/rendering helper functions (`drawSelectionHighlight`, the walk-cycle frame math, floating combat-text formatting, the torch-brazier animated-frame branch) were **not** touched, per the concurrent-agent boundary in the task brief. New animated props (`env_campfire`, `env_lava_channel`) are marked `animated: true` in their map data but currently render as a static single frame — extending the animated-sprite-sheet branch to cover them is a follow-up for whoever owns that code path, not done here.

---

## 3. Monster stat generation

Bestiary monsters don't ship with a `hp`/`speed` field directly — `BESTIARY_EXPANSION.md` §11 gives the formula (`HP = 14 × level^1.05`, rank multipliers ×1/2.5/3.5/12 for normal/elite/rare/boss). Stats for every monster placed in a map (54 entries — the full roster) were computed from that formula at each entry's representative level and hand-checked against the three "preserved exactly" legacy values (`gloopling_bellflower` 45 HP, `snagtooth_raider` 120 HP, `drowned_marrowguard` 280 HP) and the five documented boss HP totals (Ordwin 3,088 → Verrocaine 20,928) — all matched. `speed` values follow the existing game convention (passive ≈0.02, aggressive normal ≈0.03–0.032, elite ≈0.038, rare ≈0.036, boss ≈0.045). A `rank` field (`normal`/`elite`/`rare`/`boss`) was added to every non-normal monster instance so game code (boss zeny bonus, boss-kill tracking, minimap dot size/color, HP-bar color) can key off it generically instead of hardcoding sprite filenames.

---

## 4. Known gaps / next pass

1. **Realms III–V sub-regions.** Only the entry hub of each is built. Next pass should flesh out: Emberglass Terraces + The Slagworks + Ashfall Overlook (vista) + Collapsed Skybridge for the Spire; Statuary of the Fallen + Crevasse Undershelf + Aurora Shelf (vista) + Hoarfrost Vault for the Chasm; Bonemeal Hollows + The Weeping Boughs + Sanguine Terrace (hidden, pacifist gate) + Thorncradle Vault for the Rootways — plus their three remaining bosses.
2. **Art dependencies.** Many tile/prop/monster filenames referenced (per `ASSET_MANIFEST.md`, e.g. `tile_sanctum_flooded.png`, `env_obelisk_aetherite.png`, `dustmote_wisp_ff.png`) do not exist on disk yet — a parallel art-generation pass is producing them. Missing images fail silently (no `img.complete`/`naturalWidth` guard triggers a draw) and fall back to a plain checkerboard tile or simply don't render the prop/monster sprite; nothing crashes.
3. **Level gating is advisory only.** Exits carry an optional `minLevel` field (e.g. Dockgate Ferry `minLevel: 15`) but the client does not currently enforce it — there's no level-gate mechanic in the existing game loop to hook into without expanding scope beyond map data.
4. **Vista sub-regions** (Windmill Ridge, and the still-unbuilt Ashfall Overlook / Aurora Shelf) don't yet grant a persistent world-map reveal or rest buff — that's flagged as an open question in `WORLD_MAP_EXPANSION.md` §10 and needs a player-flags system that doesn't exist yet.
5. **Animated props** placed in the new maps (`env_campfire`, `env_lava_channel`) render as a static frame; only `env_torch_brazier` has an animated-frame branch in both `index.html` and `editor.html`.

---

## 5. Files created / changed

**Created:**
- `web/maps/aethelgard.json`
- `web/maps/gatewatch.json`
- `web/maps/meadows.json`
- `web/maps/sanctum.json`
- `web/maps/spire.json`
- `web/maps/chasm.json`
- `web/maps/rootways.json`
- `vault/WORLD_BUILD_REPORT.md` (this file)

**Changed:**
- `web/index.html` — sprite preload lists; removed hardcoded `npcs`/`envStructures`/`monsters` seed data (now populated from `maps/*.json`); added `MAP_REGISTRY`, `loadZoneMap()`, `applyZoneMapData()`, `checkZoneExits()`, `currentMapBounds`/`currentMapExits`/`currentMapSubRegions`/`currentMapDefaultTile`/`currentMapId`/`currentMapName` state; `checkCollision()`, camera clamp, visible-tile range, and monster-wander bounds now read `currentMapBounds`; `drawIsoDiamondTile()`'s hardcoded procedural placeholder replaced with a data lookup; `checkDistrictTransition()` rewired to use `subRegions` and now actually called from `render()`; `renderMinimap()` rewritten to scale to the loaded zone's bounds/sub-regions instead of a fixed 3-band world; boss-specific checks generalized from `sprite === 'boss_baphomet_ff'` to `rank === 'boss'` (triggerAttack zeny bonus + `defeatedBosses` tracking, minimap dot, HP-bar color); Elder quest text/logic updated to reference Ordwin instead of Baphomet; `loadCustomMapData()` extended to apply the same additive fields; boot sequence now calls `loadZoneMap('aethelgard')`.
- `web/editor.html` — `TERRAIN_TILES`, `ENV_PROPS`, `MONSTER_TYPES`, `NPC_TYPES`, `allSpriteNames` extended with all Phase 3 ids; added a "Load World Zone" panel + `loadWorldZone()` function that fetches directly from `web/maps/*.json`.

No changes were made to `web/zaggers_database.json`, `vault/DATABASE_REGISTRY.md`, combat math, animation helpers, or networking code.
