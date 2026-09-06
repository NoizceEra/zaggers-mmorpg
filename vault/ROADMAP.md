# ZAGGERS MMORPG - MASTER DEVELOPMENT ROADMAP

## Executive Vision
Zaggers is a 2.5D Isometric Tactical Action MMORPG combining Ragnarok Online's stat customization and camera perspective with Final Fantasy 6's rich sprite aesthetics and class depth.

---

## Phase 1: Engine Foundation (Completed)
- [x] **2.5D Diamond Iso Canvas Renderer**: Depth-sorted rendering with sub-pixel seam prevention.
- [x] **360° Free Camera Controls**: Q/E rotation, mouse right-drag orbit, scroll zoom, WASD / click movement.
- [x] **Visual Level & Map Editor (`web/editor.html`)**: Tile painting, prop stamping, entity placement, JSON serialization.
- [x] **RO-Style HUD**: Status bars (HP/SP/Base Level), Minimap, Chat log, Floating combat numbers, Stat allocation window, Shop modal.
- [x] **Sprite Engine**: Support for hero classes, NPCs (Kafra, Blacksmith, Merchant, Elder), and animated monsters (Slime, Goblin, Skeleton, Cactuar, Bomb, Baphomet).

---

## Phase 2: Database & Class Engine (Completed)
- [x] **Obsidian Knowledge Vault**: Interconnected docs for lore, system registries, pipelines, and roadmap.
- [x] **Database & Class Editor (`web/db_editor.html`)**: In-browser engine for tweaking classes, skills, item drop rates, and monster stats.
- [x] **Dynamic Schema (`zaggers_database.json`)**: Exportable/Importable JSON database backing game client and editor.
- [x] **5 Core Original Classes**: Vanguard, Spellweaver, Shadowblade, Cleric, Ranger.

---

## Phase 3: World Expansion & Content (Current)

Design work is **complete** — see `DESIGN_AUDIT.md`, `WORLD_MAP_EXPANSION.md`, `BESTIARY_EXPANSION.md`, `CLASS_SKILL_ITEM_EXPANSION.md`, `ASSET_MANIFEST.md`. `zaggers_database.json` has been expanded to schema v2 (5 classes / 30 skills / 25 items / 54 monsters / 7 zones / 35 sub-regions). What remains is implementation and art.

### 3.0 Client wiring — **DONE** (2026-09-06 expansion pass)
See `CLIENT_DB_WIRING_REPORT.md`. `ensureGameDB()` fetches `zaggers_database.json` at boot.
- [x] Fetch `zaggers_database.json` at client boot; fail loudly if it 404s.
- [x] Replace the hardcoded `HERO_CLASSES` block with `db.classes`.
- [x] Drive monster spawns from `db.monsters` + map enrichment (`enrichMonsterFromDB`).
- [x] Drive the shop modal from `db.items` (filter on `slot` / `reqLevel`).
- [x] Keep `db_editor.html` working against the same file — no field renames.

### 3.1 Elemental combat system
- [x] Implement `finalDamage = base × skillMultiplier × elements.modifiers[atk][def]`.
- [x] Resolve attack element: skill `element` → weapon `element` → `Neutral`.
- [x] Show element affinity on the monster nameplate and in floating combat numbers.
- [ ] Add `mdef` to the DEF formula path in `DATABASE_REGISTRY.md`.
- [ ] *(Open)* Give monsters `flee`/`hit` so the HIT/FLEE formulas are evaluable (`DESIGN_AUDIT.md` §2H).

### 3.2 Bestiary rollout — 54 monsters
- [x] Execute the six sprite renames (`ASSET_MANIFEST.md` §0) — unblocks the current data.
- [x] P0 art: Gatewatch (4) + Meadows (8) → Lv 1–16 fully playable.
- [x] P1 art: Sunken Sanctum (8) → Lv 15–32.
- [x] P2 art: Obsidian Spire (9) → Lv 30–52.
- [x] P3 art: Glacial Chasm (10) → Lv 50–72.
- [x] P4 art: Umbral Rootways (9) + Task A2 redraw touch-ups (`touchup_renamed_sprites.py`).
- [x] Wire `rank` (normal/elite/rare/boss) on map instances (nameplate/HP styling partial).

### 3.3 Aethelgard master town — 64×64
- [x] Build the district wheel: Obelisk Plaza, Kestrel Market, Ashen Ward, High Temple, Lantern Rows, Wetstone Docks.
- [x] Rename the "Kafra" service → **Kestrel Consignment House** (sprite reused, livery recolour).
- [x] Place the four transit stubs (Rampart Gate, Dockgate Ferry, Ashroad Caravan, Rimewind Tramway) with level gates.
- [ ] Rooftop Walk shortcut, Lantern Rows → Ashen Ward.
- [ ] Elder's House opening questline hook.

### 3.4 Wilderness sub-regions — 21 maps across 5 realms + tutorial
- [x] Gatewatch Commons (32×32 tutorial field).
- [x] Whispering Meadows: Bellflower Downs, Windmill Ridge, Thistlemarch Fen, Hollowroot Grove, Raider's Palisade.
- [x] Sunken Sanctum: Tidebreak Stair, Silt Warrens, Drowned Nave, Glasslight Reliquary, Choirfall Deep.
- [x] Obsidian Spire: Cinderfall Approach, Emberglass Terraces, Ashfall Overlook, The Slagworks, Collapsed Skybridge, The Spire Crown.
- [x] Glacial Chasm: Rimewind Pass, Statuary of the Fallen, Crevasse Undershelf, Aurora Shelf, Hoarfrost Vault, Thronehall of Ice.
- [x] Umbral Rootways: Nethergate Descent, Bonemeal Hollows, The Weeping Boughs, Sanguine Terrace, Thorncradle Vault, Throne of the Horned Sovereign.
- [ ] Implement the sub-region *draws*: 3 vistas, 4 hidden areas, 2 smuggler vendors, 2 elite camps, 4 shortcuts, 5 gathering clusters.
- [ ] Hazard terrain (Weeping Boughs poison DoT) and the Thawstone timed-carry secret.

### 3.5 Skill Tree Visualizer — 30 skills
- [x] In-game skill window drawing the 2–2–2 tier lattice from `tier` / `requires`.
- [x] Skill point allocation gated on `reqLevel`.
- [x] F1–F9 hotbar binding, cooldown sweep from `cooldownMs`.
- [x] Implement the seven `targetType` behaviours incl. the new `self_buff`, `party_buff`, `ally_single`, `ground_trap`.

### 3.6 Equipment Paperdoll — 5 slots
- [x] Paperdoll UI bound to the new `slot` field (Weapon, Shield, Armor, Headgear, Accessory).
- [x] Enforce `twoHanded` → shield slot lockout.
- [x] Apply `bonus` stat riders and `mdef` to the character sheet.
- [ ] Monster drop tables wired from `monsters[].drops`.
- [x] Retarget the two placeholder icons (`mythril_armor`, `dragon_lance`).

### 3.7 Deferred out of Phase 3 (tracked, not started)
- NPC dialogue + quest data model (`quests{}`, `npcs{}` collections) — the largest remaining content system; sub-region quest hooks are seeded but the schema is undesigned.
- Sixth class (Monk / Warden) — `hero_monk.png` is orphaned on disk. Phase 4.

---

## Phase 4: Multiplayer & Live Services (Future)
- [ ] **WebSockets / Socket.IO Server**: Multi-player real-time sync for movement, chat, and combat.
- [ ] **Guild War & GvG Systems**: Castle siege battlegrounds in Aethelgard realm.
- [ ] **Crafting & Player Vending**: Player-run shops and blacksmith item refinement (+1 to +10 upgrading).
