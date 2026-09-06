# ASSET MANIFEST — Zaggers Phase 3

**Purpose:** a flat, self-contained checklist for the art-generation agent. Every filename here is the exact target the database already points at — **no derivation required, no cross-referencing other docs.** Tick items off as they land.

**Verified against `web/zaggers_database.json` on 2026-09-06.** Every sprite/icon filename below is referenced by a live database row, and every database reference appears below. The two lists are in sync.

### Target directories
| Category | Path |
|---|---|
| Monsters, heroes, NPCs, item icons | `web/assets/sprites_ff/` |
| Tiles and environmental props | `web/assets/tiles_ff/` |

### Conventions (from `PIPELINE_AND_TOOLS.md`)
- **Character/monster sheets:** 64×64 px cells. Row 0 = South, Row 1 = West, Row 2 = East, Row 3 = North.
- **Iso floor tiles:** 64×32 px diamond (2:1).
- **Props:** variable, with an explicit anchor point — see §4 for the anchor table.
- **Palette:** 16- or 32-colour indexed, 16-bit JRPG register.
- **Item icons:** 32×32 px, single frame, transparent background.
- **Naming:** monsters `<monster_id>_ff.png`; item icons by category prefix (`wpn_`, `shd_`, `arm_`, `hat_`, `acc_`, `potion_`, `food_`, `key_`).

---

## 0. TASK A — Renames (do these first, 10 minutes, zero art)

Six sprites already exist and are being reused under new ids (`BESTIARY_EXPANSION.md` §9). **Rename the file; keep the pixels.** The database already points at the new names, so the game is broken until these are done.

- [ ] `slime_green_ff.png` → **`gloopling_bellflower_ff.png`**
- [ ] `goblin_ff.png` → **`snagtooth_raider_ff.png`**
- [ ] `skeleton_ff.png` → **`drowned_marrowguard_ff.png`**
- [ ] `cactuar_ff.png` → **`pricklespine_thornmarch_ff.png`**
- [ ] `bomb_ff.png` → **`cinderpuff_ff.png`**
- [ ] `boss_baphomet_ff.png` → **`verrocaine_sovereign_ff.png`**

Rename the matching `.png.import` sidecar alongside each, **or** delete all `.import` files if the Godot branch is being retired (`DESIGN_AUDIT.md` §5).

### TASK A2 — Optional touch-up passes on the renamed six
Not blocking; improves the fit of reused art to its new identity.
- [ ] `gloopling_bellflower_ff.png` — recolour green → meadow-blue
- [ ] `snagtooth_raider_ff.png` — add a tusk highlight
- [ ] `drowned_marrowguard_ff.png` — algae / waterline tint pass
- [ ] `pricklespine_thornmarch_ff.png` — **redraw head/face** (current silhouette is a recognisable FF lift)
- [ ] `cinderpuff_ff.png` — **redraw face** (same reason; keep the floating ember sphere)
- [ ] `verrocaine_sovereign_ff.png` — **redraw head** off the goat-motif; keep scale, horns, throne posture

---

## 1. TASK B — Monster sprites (48 new, 64×64 4-row sheets)

Grouped by production priority: ship complete level bands, not scattered singles.

### P0 — Gatewatch Commons (Lv 1–5) · 4 sheets
- [ ] `dustmote_wisp_ff.png` — Wind. Knot of chaff and sunlight drifting over stubble.
- [ ] `gutter_ratkin_ff.png` — Neutral. Knee-high ratkin in a coin-purse hood.
- [ ] `thatch_beetle_ff.png` — Earth. Fat iridescent roof-eating beetle.
- [ ] `straw_effigy_ff.png` — Fire, *rare*. Scarecrow that turned to watch you.

### P0 — Whispering Meadows (Lv 1–16) · 8 sheets
- [ ] `bramblehop_ff.png` — Earth. Hare of thorn-scrub, permanently mid-bounce.
- [ ] `hornhaste_wasp_ff.png` — Wind. Fist-sized furious wasp; spawns in threes.
- [ ] `mossback_tortin_ff.png` — Earth. Two-foot moss-grown shell with legs.
- [ ] `fen_lurker_ff.png` — Water. Reed-ambusher; mostly submerged silhouette.
- [ ] `rot_capling_ff.png` — Poison. Child-sized walking mushroom, spore puff on hit.
- [ ] `snagtooth_warchanter_ff.png` — Neutral, *elite*. Snagtooth with a stacked-shield totem drum.
- [ ] `grovewarden_thistle_ff.png` — Earth, *rare*. Briar-and-antler guardian shape.
- [ ] `ordwin_palisade_tyrant_ff.png` — Neutral, **BOSS Lv16**. Chieftain in oversized stolen Legion plate.

### P1 — Sunken Sanctum (Lv 15–32) · 8 sheets
- [ ] `brinemaw_eel_ff.png` — Water. Six feet of muscle and hinge-jaw.
- [ ] `silt_creeper_ff.png` — Poison. Sediment that reaches; near-invisible idle pose.
- [ ] `glasslight_mote_ff.png` — Holy. Shard of living Aetherite light (escort/puzzle NPC-like).
- [ ] `reliquary_husk_ff.png` — Undead. Kneeling pilgrim that got back up.
- [ ] `coralbound_acolyte_ff.png` — Water. Robed figure grown through with pink coral.
- [ ] `warden_of_the_nave_ff.png` — Undead, *elite*. 12ft ceremonial armour full of black water.
- [ ] `pale_choirmaster_ff.png` — Holy, *rare*. Conductor, arms raised, conducting nothing.
- [ ] `hallowdeep_warden_ff.png` — Water, **BOSS Lv32**. Wearing the last warden's vestments.

### P2 — Obsidian Spire (Lv 30–52) · 9 sheets
- [ ] `emberglass_shard_ff.png` — Fire. Volcanic glass with intent and uncooled edges.
- [ ] `ashfall_harrier_ff.png` — Wind. Ash-column raptor, dive pose.
- [ ] `magma_hulk_ff.png` — Fire. Slag given shoulders; leaves burning footprints.
- [ ] `soot_revenant_ff.png` — Undead. Foundry-hand outlined in settled ash.
- [ ] `forgewrought_sentinel_ff.png` — Earth. Automaton still guarding a dead foundry.
- [ ] `pyrelash_imp_ff.png` — Fire. Small, quick, whip of live flame.
- [ ] `bellowmaster_grukk_ff.png` — Fire, *elite*. Works the great bellows alone.
- [ ] `the_unquenched_ff.png` — Fire, *rare*. Pre-Shattering fire, roughly humanoid.
- [ ] `vashkar_spire_crown_ff.png` — Fire, **BOSS Lv52**. Obsidian, crowned, molten at every joint.

### P3 — Glacial Chasm (Lv 50–72) · 10 sheets
- [ ] `rimewind_sprite_ff.png` — Wind. The blizzard, locally; face only when looked at.
- [ ] `hoarfrost_stalker_ff.png` — Water. White on white, low stalking posture.
- [ ] `frozen_penitent_ff.png` — Undead. Kneeling statue mid-thaw, ice sloughing.
- [ ] `glacier_drake_whelp_ff.png` — Water. Cat-sized cobalt-scaled drake.
- [ ] `snowveil_shade_ff.png` — Shadow. A shadow with nothing casting it.
- [ ] `aurora_seraphon_ff.png` — Holy. Aurora ribbon folded into six wings.
- [ ] `permafrost_lich_ff.png` — Undead. Vault-keeper with a ledger.
- [ ] `statuary_colossus_ff.png` — Water, *elite*. 30ft frozen hero, no longer still.
- [ ] `the_vault_keeper_ff.png` — Undead, *rare*. Holds the only key.
- [ ] `sylveth_silent_thaw_ff.png` — Water, **BOSS Lv72**. Queen of the Silent Thaw.

### P4 — Umbral Rootways (Lv 70–99) · 9 sheets
- [ ] `nethergate_creeper_ff.png` — Shadow. Root-hair body walking upside-down on walls.
- [ ] `weeping_bough_ff.png` — Poison. Low branch weeping amber; closes on warmth.
- [ ] `umbral_houndkin_ff.png` — Shadow. Pack hunter that casts no shadow.
- [ ] `sanguine_thorncaller_ff.png` — Shadow. Immaculately dressed, seated, non-hostile idle.
- [ ] `hollow_penitent_choir_ff.png` — Undead. Hollow singing figure (spawns as nine).
- [ ] `rootfang_devourer_ff.png` — Poison. The mouth at the end of the root.
- [ ] `abyssal_heraldon_ff.png` — Shadow. Horned armoured herald.
- [ ] `thorncradle_warden_ff.png` — Shadow, *elite*. Drilled honour guard.
- [ ] `the_pale_apostate_ff.png` — Holy, *rare*. Fallen High Temple Cleric, still technically holy.

*(Verrocaine reuses the renamed Baphomet sheet — see §0.)*

**Monster sheet total: 48 new + 6 renamed = 54.**

---

## 2. TASK C — Item icons (23 new, 32×32)

`potion_health_ff.png` already exists. `excalibur_ff.png` exists but is a placeholder standing in for a lance (`DESIGN_AUDIT.md` §2E) — flagged, not blocking.

### Consumables · 4
- [ ] `potion_mana_ff.png` — Blue Potion
- [ ] `food_bread_ff.png` — Meadow Bread
- [ ] `potion_aetherite_ff.png` — Aetherite Draught (Holy, tier 4)
- [ ] `key_thawstone_ff.png` — Thawstone (quest key, visibly melting)

### Weapons · 6
- [ ] `wpn_shortsword_ff.png` — Bellflower Shortsword (T1, Neutral)
- [ ] `wpn_cleaver_ff.png` — Snagtooth Cleaver (T1, Neutral)
- [ ] `wpn_trident_ff.png` — Tidebreak Trident (T2, Water, two-handed)
- [ ] `wpn_emberglass_ff.png` — Emberglass Edge (T3, Fire)
- [ ] `wpn_longbow_ff.png` — Hoarfrost Longbow (T4, Water, two-handed)
- [ ] `wpn_staff_root_ff.png` — Rootfang Staff (T5, Shadow, two-handed)
- [ ] *(optional)* `wpn_lance_dragon_ff.png` — replaces the `excalibur_ff.png` placeholder on Dragon Lance

### Shields · 3
- [ ] `shd_targe_ff.png` — Oaken Targe (T1, Earth)
- [ ] `shd_aegis_ff.png` — Nave Aegis (T2, Water)
- [ ] `shd_bulwark_ff.png` — Forgewrought Bulwark (T3, Fire)

### Armor · 4
- [ ] `arm_jerkin_ff.png` — Traveller's Jerkin (T1, Neutral)
- [ ] `arm_mythril_ff.png` — Mythril Armor (T2) — **retargeted** from the `prop_crystal_save.png` placeholder
- [ ] `arm_slagplate_ff.png` — Slagworks Plate (T3, Fire)
- [ ] `arm_shroud_ff.png` — Umbral Shroud (T5, Shadow)

### Headgear · 3
- [ ] `hat_kettle_ff.png` — Militia Kettle Helm (T1)
- [ ] `hat_circlet_ff.png` — Coral Circlet (T2, Water)
- [ ] `hat_diadem_ff.png` — Aurora Diadem (T4, Holy)

### Accessories · 3
- [ ] `acc_charm_ff.png` — Hedgerow Charm (T1, Earth)
- [ ] `acc_pendant_ff.png` — Glasslight Pendant (T2, Holy)
- [ ] `acc_signet_ff.png` — Sovereign's Signet (T6, Shadow)

---

## 3. TASK D — New iso floor tiles (64×32 diamond)

Existing tiles cover town, meadow and generic dungeon. These fill the gaps the new sub-regions create. Add each new key to `editor.html`'s `TILE_TYPES` palette and its `category`.

### Meadow set — for the Fen and the Grove · 4
- [ ] `tile_meadow_reed.png` — reed/marsh, category `meadow`
- [ ] `tile_meadow_mud.png` — churned wet mud, `meadow`
- [ ] `tile_meadow_path.png` — trodden dirt path, `meadow`
- [ ] `tile_grove_moss.png` — deep moss, Hollowroot Grove, `meadow`

### Sanctum / water set · 4
- [ ] `tile_sanctum_flooded.png` — shallow water over flagstone, `dungeon`
- [ ] `tile_sanctum_marble.png` — pale cracked nave marble, `dungeon`
- [ ] `tile_sanctum_algae.png` — algae-slick stone, `dungeon`
- [ ] `tile_sanctum_glass.png` — fused Aetherite glass (Reliquary), `dungeon`

### Spire set · 3
- [ ] `tile_spire_ash.png` — deep ash drift, `dungeon`
- [ ] `tile_spire_emberglass.png` — black volcanic glass sheet, `dungeon`
- [ ] `tile_spire_basalt.png` — hexagonal basalt column tops, `dungeon`

### Chasm / ice set · 4 — **new category `ice`**
- [ ] `tile_ice_packed.png` — packed snow
- [ ] `tile_ice_blue.png` — clear blue glacier ice
- [ ] `tile_ice_crevasse.png` — dark crevasse edge
- [ ] `tile_ice_mirror.png` — polished throne-hall mirror ice

### Rootways set · 4 — **new category `root`**
- [ ] `tile_root_bark.png` — walkable root bark
- [ ] `tile_root_bonemeal.png` — pale bonemeal soil
- [ ] `tile_root_sap.png` — amber sap pool (hazard terrain)
- [ ] `tile_root_terrace.png` — cut red stone (Sanguine Terrace)

**New tiles: 19.**

---

## 4. TASK E — New environmental props

Follow the existing `ENV_PROPS` entry shape in `editor.html` — `{ type, name, width, height, anchorX, anchorY }`. Anchor is the ground-contact point in sprite pixels.

### Aethelgard districts · 16
| Prop file | W×H | anchorX,Y | District |
|---|---|---|---|
| - [ ] `env_obelisk_aetherite.png` | 96×192 | 48,176 | Obelisk Plaza |
| - [ ] `env_notice_board.png` | 64×64 | 32,52 | Obelisk Plaza |
| - [ ] `env_awning_stall.png` | 96×96 | 48,64 | Kestrel Market |
| - [ ] `env_crate_stack_tall.png` | 64×96 | 32,82 | Kestrel Market |
| - [ ] `env_forge_anvil.png` | 64×64 | 32,50 | Ashen Ward |
| - [ ] `env_guild_banner.png` | 64×128 | 32,116 | Ashen Ward |
| - [ ] `env_chimney_stack.png` | 64×160 | 32,148 | Ashen Ward |
| - [ ] `env_temple_pillar.png` | 64×160 | 32,148 | High Temple |
| - [ ] `env_stained_arch.png` | 128×160 | 64,146 | High Temple |
| - [ ] `env_prayer_candles.png` | 64×64 | 32,54 | High Temple |
| - [ ] `env_lantern_string.png` | 128×64 | 64,20 | Lantern Rows *(overhead — anchor high)* |
| - [ ] `env_house_terrace.png` | 128×128 | 64,98 | Lantern Rows |
| - [ ] `env_washing_line.png` | 96×64 | 48,24 | Lantern Rows *(overhead)* |
| - [ ] `env_well_stone.png` | 64×64 | 32,50 | Lantern Rows |
| - [ ] `env_dock_piling.png` | 64×96 | 32,84 | Wetstone Docks |
| - [ ] `env_cargo_crane.png` | 128×192 | 64,178 | Wetstone Docks |

### Wilderness · 14
| Prop file | W×H | anchorX,Y | Where |
|---|---|---|---|
| - [ ] `env_fishing_net.png` | 64×64 | 32,48 | Docks |
| - [ ] `env_rowboat.png` | 96×64 | 48,52 | Docks / Sanctum |
| - [ ] `env_windmill.png` | 160×224 | 80,206 | Windmill Ridge |
| - [ ] `env_fence_rail.png` | 64×64 | 32,50 | Gatewatch / Meadows |
| - [ ] `env_scarecrow.png` | 64×96 | 32,86 | Gatewatch |
| - [ ] `env_palisade_wall.png` | 96×128 | 48,116 | Raider's Palisade |
| - [ ] `env_campfire.png` | 64×64 | 32,52 | Palisade / Undershelf *(animated)* |
| - [ ] `env_reed_clump.png` | 64×64 | 32,50 | Thistlemarch Fen |
| - [ ] `env_hollow_tree.png` | 128×192 | 64,178 | Hollowroot Grove |
| - [ ] `env_waterfall_curtain.png` | 96×160 | 48,150 | Hollowroot entrance |
| - [ ] `env_pew_floating.png` | 96×64 | 48,50 | Drowned Nave |
| - [ ] `env_reliquary_casket.png` | 64×64 | 32,52 | Glasslight Reliquary |
| - [ ] `env_lava_channel.png` | 64×64 | 32,40 | Spire *(animated)* |
| - [ ] `env_bellows_great.png` | 128×128 | 64,116 | The Slagworks |

### Chasm & Rootways · 8
| Prop file | W×H | anchorX,Y | Where |
|---|---|---|---|
| - [ ] `env_ice_statue.png` | 64×128 | 32,116 | Statuary of the Fallen |
| - [ ] `env_ice_colossus_shell.png` | 128×192 | 64,178 | Statuary *(large)* |
| - [ ] `env_cairn_waypoint.png` | 64×96 | 32,84 | Rimewind Pass |
| - [ ] `env_guide_rope.png` | 96×64 | 48,30 | Rimewind Pass *(overhead)* |
| - [ ] `env_vault_door.png` | 128×160 | 64,148 | Hoarfrost Vault |
| - [ ] `env_root_hair.png` | 64×128 | 32,24 | Bonemeal Hollows *(ceiling — anchor high)* |
| - [ ] `env_weeping_branch.png` | 128×160 | 64,40 | Weeping Boughs *(overhead)* |
| - [ ] `env_briar_wall.png` | 96×128 | 48,116 | Thorncradle Vault |

**New props: 38.**

---

## 5. TASK F — Optional / follow-up

- [ ] `hero_ranger.png` — Ranger currently uses `hero_redmage.png`, which reads as a caster. `hero_dragoon.png` already on disk is a closer fit; either swap the reference or draw a dedicated marksman sheet. (`DESIGN_AUDIT.md` §2F)
- [ ] NPC sheets for the renamed **Kestrel Consignment House** — reuse `npc_kafra.png`, recolour livery only.
- [ ] `npc_militia.png` — Gatewatch tutorial NPC.
- [ ] `npc_smuggler.png` — Silt Warrens + Crevasse Undershelf vendor.
- [ ] `hero_monk.png` is orphaned on disk. A sixth class is half-funded by it; deferred to Phase 4 (`CLASS_SKILL_ITEM_EXPANSION.md` §4).

---

## 6. Totals

| Task | Item | Count |
|---|---|---|
| A | Sprite renames (no art) | 6 |
| A2 | Touch-ups / redraws on renamed six | 6 |
| B | **New monster sheets** | **48** |
| C | New item icons | 23 |
| D | New iso tiles | 19 |
| E | New environmental props | 38 |
| F | Optional NPC / hero sheets | 4 |
| | **New art files total** | **132** |

**Suggested order:** A → B(P0) → C(consumables + T1 gear) → D(meadow) → E(Aethelgard) → then B/C/D/E by priority band P1→P4.
