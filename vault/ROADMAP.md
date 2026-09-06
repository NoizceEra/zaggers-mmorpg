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

## Phase 2: Database & Class Engine (Current)
- [x] **Obsidian Knowledge Vault**: Interconnected docs for lore, system registries, pipelines, and roadmap.
- [x] **Database & Class Editor (`web/db_editor.html`)**: In-browser engine for tweaking classes, skills, item drop rates, and monster stats.
- [x] **Dynamic Schema (`zaggers_database.json`)**: Exportable/Importable JSON database backing game client and editor.
- [x] **5 Core Original Classes**: Vanguard, Spellweaver, Shadowblade, Cleric, Ranger.

---

## Phase 3: World Expansion & Content (Next)
- [ ] **Aethelgard World Map Expansion**: 64x64 master town grid with interactive NPC questlines and shopkeepers.
- [ ] **Subterranean & Wilderness Dungeons**: 4 instanced zones with unique boss spawns.
- [ ] **Skill Tree Visualizer**: In-game interactive skill tree window with active skill hotbars (F1-F9).
- [ ] **Equipment Paperdoll**: Visual equipment gear slots (Weapon, Armor, Shield, Headgear, Accessory).

---

## Phase 4: Multiplayer & Live Services (Future)
- [ ] **WebSockets / Socket.IO Server**: Multi-player real-time sync for movement, chat, and combat.
- [ ] **Guild War & GvG Systems**: Castle siege battlegrounds in Aethelgard realm.
- [ ] **Crafting & Player Vending**: Player-run shops and blacksmith item refinement (+1 to +10 upgrading).
