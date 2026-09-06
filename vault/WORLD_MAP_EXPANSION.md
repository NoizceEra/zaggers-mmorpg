# WORLD MAP EXPANSION — Aethelgard & the Five Realms

**Status:** Design spec for Phase 3. Companion to `BESTIARY_EXPANSION.md` and `CLASS_SKILL_ITEM_EXPANSION.md`.
**Implements:** `DESIGN_AUDIT.md` §1.7 (town has no layout) and §1.8 (zones are flat).

The design principle throughout: **no sub-region exists only to be walked across.** Each one carries at least one of — a distinct monster set, a shortcut, a vista, a gathering cluster, an elite camp, or a secret. If a sub-region has none of those, it is a corridor and should be merged into its neighbour.

---

## 0. Topology at a glance

```
                        ╔══════════════════════════╗
                        ║  AETHELGARD  (Lv 1-99)   ║
                        ║   master town, safe      ║
                        ╚═══╦════╦═══════╦════╦════╝
                            ║    ║       ║    ║
              ┌─────────────┘    ║       ║    └──────────────┐
              │                  ║       ║                   │
     ┌────────▼────────┐  ┌──────▼──┐ ┌──▼───────┐  ┌────────▼────────┐
     │ GATEWATCH       │  │ WETSTONE│ │ ASHROAD  │  │  RIMEWIND       │
     │ COMMONS  (1-5)  │  │ DOCKS   │ │ CARAVAN  │  │  TRAMWAY        │
     │ tutorial fields │  │ (ferry) │ │ (wagon)  │  │  (ice-tram)     │
     └────────┬────────┘  └────┬────┘ └────┬─────┘  └────────┬────────┘
              │                │           │                 │
     ┌────────▼────────┐  ┌────▼─────┐ ┌───▼──────┐  ┌───────▼────────┐
     │  I. WHISPERING  │  │ II.SUNKEN│ │III.OBSID.│  │ IV. GLACIAL    │
     │     MEADOWS     │─▶│  SANCTUM │ │  SPIRE   │  │     CHASM      │
     │      1-16       │  │  15-32   │ │  30-52   │  │    50-72       │
     └─────────────────┘  └────┬─────┘ └───┬──────┘  └───────┬────────┘
              ▲                │           │                 │
              └────────────────┘           │                 │
              (Hollowroot ↔ Tidebreak,     │                 │
               one-way scenic descent)     └────────┬────────┘
                                                    │
                                          ┌─────────▼──────────┐
                                          │ V. UMBRAL ROOTWAYS │
                                          │       70-99        │
                                          │  (endgame, no      │
                                          │   town portal in)  │
                                          └────────────────────┘
```

**Rules of the topology**
- Aethelgard is the only hub. Every realm has exactly one *town-side* gateway (the four transit stubs above), so the town always feels central.
- **Realms I↔II and III↔IV** are additionally linked by in-world routes, so a player can travel the world laterally without returning to town. This is what makes the map feel like a *place* rather than a spoke diagram.
- **Umbral Rootways has no direct town link.** It is reached only through the Glacial Chasm's Thronehall or the Obsidian Spire's Collapsed Skybridge. Endgame should require a commute.
- Level ranges **overlap by ~2** at every boundary so players are never forced to grind a gap.

---

## 1. AETHELGARD — Master Town

**Grid:** 64×64 (per `ROADMAP.md`). Default tile `tile_town_cobble`.
**Light:** `#ffffff`. **Combat:** disabled. **Level range:** 1–99.

Built as a wheel: the Obelisk at the hub, five districts as wedges, a ring road (`tile_town_brick`) separating them, and the outer wall (`tile_town_border`) with four gates. A player standing at the Obelisk can see the entrance arch of every district — that legibility is the whole point of a social hub.

```
                    N — Rampart Gate → Gatewatch Commons
        ╔═══════════════════╤═══════════════════╗
        ║   LANTERN ROWS    │    ASHEN WARD     ║
        ║   (residential)   │  (guilds/smithy)  ║
   W ───╫───────┐  ╔═════════════╗  ┌──────────╫─── E
 Ashroad║ KESTREL│  ║  OBELISK    ║  │          ║ Rimewind
  Cara- ║ MARKET │  ║   PLAZA     ║  │ HIGH     ║ Tramway
   van  ║        │  ╚═════════════╝  │ TEMPLE   ║
        ║────────┘                   └──────────╫
        ║        WETSTONE DOCKS (outskirts)     ║
        ╚═══════════════════╤═══════════════════╝
                    S — Dockgate → Sunken Sanctum ferry
```

### 1.1 Obelisk Plaza — *the centre*
The Aetherite Obelisk stands on a raised octagonal dais ringed by the Grand Fountain's four basins. Party recruiters shout from the fountain steps; the Obelisk itself is the respawn anchor and the world-map interface. Every district arch is visible from the dais.
**Contains:** Aetherite Obelisk (save/respawn/world map), Grand Fountain, Recruiter's Steps (party board), Herald's Post (server announcements).
**Props:** `env_fountain`, `env_crystal`, `env_torch_brazier`, *new:* `env_obelisk_aetherite`, `env_notice_board`.

### 1.2 Kestrel Market District — *west wedge, commerce*
Awning-shaded lanes of stall rows, loudest district in the game. General goods, potion vendors, the auction hall, and the **Kestrel Consignment House** — the renamed storage/teleport service formerly styled "Kafra" (`DESIGN_AUDIT.md` §3). Reuses `npc_kafra.png` and `npc_merchant.png`.
**Contains:** Consignment House (storage vault, teleport, world maps), Potion Row, Auction Hall, Traveller's Larder (food buffs).
**Props:** `env_market_stall`, `env_barrel_crate`, `env_house_shop`, *new:* `env_awning_stall`, `env_crate_stack_tall`.

### 1.3 Ashen Ward — *north-east wedge, guilds & craft*
Soot-black brickwork, chimney smoke, the constant ring of hammers. Home to **The Obsidian Smithy** (Master Blacksmith Ironhide) and the five class guild halls, each a narrow tower with its faction banner. This is where the skill-tree trainers stand.
**Contains:** Obsidian Smithy (refinement, weapon craft), Vanguard Legion Hall, Spellweaver Syndicate Spire, Shadowblade Brotherhood (unmarked door, alley side), Cleric Order annex, Ranger Corps Lodge, Guild Registry (player guild creation).
**Props:** `env_house_shop`, `env_torch_brazier`, `env_barrel_crate`, *new:* `env_forge_anvil`, `env_guild_banner`, `env_chimney_stack`.

### 1.4 The High Temple — *east wedge, sanctuary*
Pale stone and stained glass, the only quiet district. Resurrection rites, blessings, status-cure services, and the Cleric Order's cloister garden. Also the tutorial destination for new Clerics.
**Contains:** High Temple nave (buffs, resurrection), Cloister Garden, Ossuary Steps (quest hook: the Sanctum's drowned dead).
**Props:** `env_torch_brazier`, `env_bush`, *new:* `env_temple_pillar`, `env_stained_arch`, `env_prayer_candles`.

### 1.5 Lantern Rows — *north-west wedge, residential*
Tight terraced housing under strung paper lanterns; washing lines between upper storeys. No shops — this is atmosphere, ambient NPC life, and the future site of player housing. The **Elder's House** (`npc_elder.png`) sits at the top of the Rows and dispenses the opening questline.
**Contains:** Elder's House (main questline hub), Rooftop Walk (shortcut to Ashen Ward, skips the ring road), Lamplighter's Yard.
**Props:** *new:* `env_lantern_string`, `env_house_terrace`, `env_washing_line`, `env_well_stone`.

### 1.6 Wetstone Docks — *south, outskirts*
Wet flagstones, tide-stained pilings, cargo cranes and the ferry berth. Grittier than the rest of town: this is where the Silt Warrens smugglers land goods they shouldn't. Not a combat zone, but the only district with a visible criminal element.
**Contains:** Ferry Berth (→ Sunken Sanctum), Cargo Cranes, The Barnacle (tavern, rumours/quest board), Bilge Steps (hidden: unmarked stair to the Silt Warrens, opens at Lv 18).
**Props:** `env_barrel_crate`, *new:* `env_dock_piling`, `env_cargo_crane`, `env_fishing_net`, `env_rowboat`.

### 1.7 Town transit stubs
| Stub | Gate | Leads to | Unlock |
|---|---|---|---|
| Rampart Gate | N | Gatewatch Commons → Whispering Meadows | open |
| Dockgate Ferry | S | Tidebreak Stair (Sunken Sanctum) | Lv 15 |
| Ashroad Caravan | W | Cinderfall Approach (Obsidian Spire) | Lv 30 |
| Rimewind Tramway | E | Rimewind Pass (Glacial Chasm) | Lv 50 |

---

## 2. GATEWATCH COMMONS — tutorial fields (Lv 1–5)

**Light:** `#fffdf2`. Technically part of Whispering Meadows' watershed, but authored as its own small map so the first fifteen minutes are hand-tuned.

Cropped fields and rabbit-fences immediately outside the Rampart Gate, patrolled by bored town militia. Everything here is passive or near-passive; the only aggressive spawn is the Straw Effigy, which is deliberately placed at the far fence so a new player *chooses* their first real fight.
**Points of interest:** Militia Picket (tutorial NPC), Scarecrow Field, the Broken Fence (visible gap leading into Bellflower Downs — the "the world continues that way" moment).
**Monsters:** `dustmote_wisp`, `gutter_ratkin`, `thatch_beetle`, `straw_effigy` *(rare)*.

---

## 3. REALM I — WHISPERING MEADOWS (Lv 1–16)

**Light:** `#fff8e7`. Tileset: meadow. Boss: **Ordwin the Palisade Tyrant** (Lv 16).

```
  [Rampart Gate]
        │
  Bellflower Downs (3-8) ──── Windmill Ridge (vista, any lv)
        │                          │
        ├──────────────────────────┘
        │
  Thistlemarch Fen (7-12) ──▶ Hollowroot Grove (10-16, HIDDEN)
        │                          │
        │                          └──▶ [one-way descent → Tidebreak Stair, Realm II]
        │
  Raider's Palisade (12-16, ELITE CAMP + BOSS)
```

### 3.1 Bellflower Downs — Lv 3–8
Rolling blue-flowered meadow that runs from the Broken Fence to the first tree line. Gentle, generous, and full of sightlines — the zone that teaches players the camera. Gloopling and Bramblehop territory, with wasp nests in the hedgerows.
**Draw:** Hedgerow gathering cluster (herbs), first Save Crystal.
**Monsters:** `gloopling_bellflower`, `bramblehop`, `hornhaste_wasp`.

### 3.2 Windmill Ridge — vista, no level gate
A single stone windmill on the highest ground in the realm, reachable by a switchback path. The sails still turn. From the platform you can see the Obelisk to the south and, on a clear render, the Obsidian Spire smoking on the far horizon — the game's first "look how big this is" beat.
**Draw:** Vista (world-map reveal for the whole realm), Miller's Rest (rest buff, +10% EXP for 10 min).
**Monsters:** none (safe pocket).

### 3.3 Thistlemarch Fen — Lv 7–12
Where the Downs turn to standing water and yellow reed. Footing is slow, sightlines are short, and Fen Lurkers ambush from the water. The tonal step up: the first area that feels genuinely unfriendly.
**Draw:** Sunken Cart (chest, respawning), reed-cutter gathering cluster.
**Monsters:** `fen_lurker`, `mossback_tortin`, `rot_capling`, `hornhaste_wasp`.

### 3.4 Hollowroot Grove — Lv 10–16 — **HIDDEN**
Entered by walking *through* the waterfall curtain at the north end of the Fen; there is no map marker until you do. Inside: a ring of enormous hollow trees around a still pool of Aetherite-clear water, silent apart from dripping. Home to `grovewarden_thistle`, the realm's rare spawn.
**Draw:** Secret area; rare spawn; the **Scenic Descent** — a root-tunnel behind the pool that drops one-way into Tidebreak Stair in Realm II, letting a level-15 player skip the Dockgate ferry.
**Monsters:** `grovewarden_thistle` *(rare)*, `rot_capling`.

### 3.5 Raider's Palisade — Lv 12–16 — **ELITE CAMP / BOSS**
A Snagtooth war camp thrown up against the eastern tree line: sharpened log walls, cook-fires, a totem of stacked shields. Patrols are aggressive and pull in groups of three — the realm's difficulty spike and the first content that wants a party.
**Draw:** Elite camp, first boss, first real gear drops.
**Monsters:** `snagtooth_raider`, `snagtooth_warchanter` *(elite)*, **`ordwin_palisade_tyrant`** *(boss, Lv 16)*.

---

## 4. REALM II — SUNKEN SANCTUM (Lv 15–32)

**Light:** `#e0f7fa`. Tileset: dungeon (slate) + water. Boss: **Hallowdeep, the Choirfall Warden** (Lv 32).

```
  [Dockgate Ferry] ──▶ Tidebreak Stair (15-19) ◀── [Hollowroot descent, Realm I]
                              │
                              ├──▶ Silt Warrens (19-24, SMUGGLER CAVE)
                              │          │
                              │          └──▶ [Bilge Steps shortcut → Wetstone Docks]
                              │
                       Drowned Nave (18-25)
                              │
                    ┌─────────┴─────────┐
                    │                   │
      Glasslight Reliquary        Choirfall Deep
        (20-28, HIDDEN)             (25-32, BOSS)
```

### 4.1 Tidebreak Stair — Lv 15–19
A vast spiral of submerged steps descending from the ferry berth into the ruin proper, water to the knee and rising as you go down. Bioluminescent algae in the joints of the stone provides the only light.
**Draw:** Entry hub, Save Crystal, the descent set-piece.
**Monsters:** `drowned_marrowguard`, `pricklespine_thornmarch`.

### 4.2 Silt Warrens — Lv 19–24 — **SMUGGLER CAVE**
Not part of the original ruin: a network of silt-cut tunnels that Wetstone smugglers widened into a warehouse. Crates of untaxed goods, tallow lamps, and things that got in through the flooded end and never left.
**Draw:** Smuggler's cache vendor (buys stolen goods, sells otherwise-unavailable reagents), and the **Bilge Steps** — a two-way shortcut straight back to Wetstone Docks, skipping the ferry entirely once found.
**Monsters:** `silt_creeper`, `brinemaw_eel`.

### 4.3 Drowned Nave — Lv 18–25
The cathedral heart of the Sanctum, its vaulted ceiling half-collapsed and open to a column of green water-light. Pews float. The Marrowguard here still keep formation.
**Draw:** Central crossroads, the realm's signature vista *from below*.
**Monsters:** `drowned_marrowguard`, `reliquary_husk`, `coralbound_acolyte`, `warden_of_the_nave` *(elite)*.

### 4.4 Glasslight Reliquary — Lv 20–28 — **HIDDEN**
Sealed behind a wall of fused Aetherite glass in the Nave's north transept; opens only when three Glasslight Motes are led into the alcove braziers. Inside is a dry, warm, gold-lit room — the only dry room in the realm — full of intact reliquary caskets.
**Draw:** Secret puzzle area; Holy-element gathering cluster (Aetherite shards); best pre-30 accessory drops.
**Monsters:** `glasslight_mote`, `pale_choirmaster` *(rare)*.

### 4.5 Choirfall Deep — Lv 25–32 — **BOSS**
The lowest chamber, where an underground fall pours endlessly into darkness and the sound of it resolves, if you stand still, into something like singing.
**Monsters:** `coralbound_acolyte`, `reliquary_husk`, **`hallowdeep_warden`** *(boss, Lv 32)*.

---

## 5. REALM III — OBSIDIAN SPIRE (Lv 30–52)

**Light:** `#ffebee`. Tileset: dungeon (obsidian + lava). Boss: **Vashkar the Spire Crown** (Lv 52).

```
  [Ashroad Caravan] ──▶ Cinderfall Approach (30-36)
                                │
                     ┌──────────┼──────────┐
                     │          │          │
             The Slagworks  Emberglass   Ashfall Overlook
              (36-45)       Terraces     (vista, any lv)
                     │      (33-40, NODES)
                     │
              Collapsed Skybridge (45-52, SHORTCUT)
                     │           └──▶ [→ Nethergate Descent, Realm V]
                     │
              The Spire Crown (48-52, BOSS)
```

### 5.1 Cinderfall Approach — Lv 30–36
The switchback road up the volcano's flank, where the caravan drops you. Ash falls constantly and settles on everything; visibility is deliberately reduced. Lava channels run beside the path in cut stone gutters.
**Draw:** Entry hub, Save Crystal, caravan vendor (repair/restock without returning to town).
**Monsters:** `cinderpuff`, `emberglass_shard`.

### 5.2 Emberglass Terraces — Lv 33–40 — **GATHERING CLUSTER**
Stepped shelves where cooling lava has sheeted into fields of black volcanic glass. The richest resource area in the game: emberglass, obsidian, and fire-salt nodes, densely packed. Deliberately under-defended and over-rewarded — a gathering destination players return to for a hundred levels.
**Draw:** Dense node cluster (3 reagent types), low aggro density.
**Monsters:** `emberglass_shard`, `ashfall_harrier`.

### 5.3 Ashfall Overlook — vista, no level gate
A basalt finger jutting from the mountainside above the ash line, clear air above and grey soup below. From here the entire realm topology is visible, and at night the Glacial Chasm glitters to the east.
**Draw:** Vista (world-map reveal), Windbreak Camp (rest buff), the game's best screenshot spot.
**Monsters:** none (safe pocket).

### 5.4 The Slagworks — Lv 36–45
Someone built a foundry here, long ago, and the mountain reclaimed it. Half-melted machinery, crucible pits still glowing, and the Forgewrought Sentinels that were left running with no one to serve.
**Draw:** Dungeon-dense combat, the realm's mechanical/lore set-piece.
**Monsters:** `magma_hulk`, `forgewrought_sentinel`, `soot_revenant`, `bellowmaster_grukk` *(elite)*.

### 5.5 Collapsed Skybridge — Lv 45–52 — **SHORTCUT**
A basalt arch that once spanned the caldera, now broken in the middle. The gap is crossable — barely — by a chain of standing pillars. Crossing it is a movement challenge, not a combat one.
**Draw:** Shortcut across the caldera (saves ~2 min of travel), and the **only route from Realm III to the Umbral Rootways** — the endgame back door.
**Monsters:** `ashfall_harrier`, `pyrelash_imp`.

### 5.6 The Spire Crown — Lv 48–52 — **BOSS**
The jagged obsidian tower at the summit, hollow, with the whole caldera visible through cracks in its walls.
**Monsters:** `pyrelash_imp`, `the_unquenched` *(rare)*, **`vashkar_spire_crown`** *(boss, Lv 52)*.

---

## 6. REALM IV — GLACIAL CHASM (Lv 50–72)

**Light:** `#e8eaf6`. Tileset: dungeon (slate) + new ice set. Boss: **Sylveth, Queen of the Silent Thaw** (Lv 72).

```
  [Rimewind Tramway] ──▶ Rimewind Pass (50-56)
                                │
                    ┌───────────┼───────────┐
                    │           │           │
          Statuary of the   Crevasse    Aurora Shelf
          Fallen (54-62)    Undershelf  (vista, any lv)
                    │       (56-63, SMUGGLER)
                    │
          Hoarfrost Vault (60-68, HIDDEN)
                    │
          Thronehall of Ice (66-72, BOSS)
                    │
                    └──▶ [→ Nethergate Descent, Realm V]
```

### 6.1 Rimewind Pass — Lv 50–56
Where the tram line ends. A canyon floor under permanent blizzard, wind loud enough to mask footsteps, guide-ropes strung between waypoint cairns because the visibility is genuinely low.
**Draw:** Entry hub, Save Crystal, the guide-rope navigation gimmick.
**Monsters:** `rimewind_sprite`, `hoarfrost_stalker`.

### 6.2 Statuary of the Fallen — Lv 54–62
The lore promise from `WORLD_LORE.md`, delivered: hundreds of ice-encased figures in the poses they died in, arranged in ranks down a mile of canyon. Some are recognisable as historical heroes. Some are still moving, very slowly.
**Draw:** The realm's identity set-piece; lore-plaque collectibles; `frozen_penitent` spawns *out of* statues when approached.
**Monsters:** `frozen_penitent`, `snowveil_shade`, `statuary_colossus` *(elite)*.

### 6.3 Crevasse Undershelf — Lv 56–63 — **SMUGGLER CAVE**
A shelf of blue ice beneath the canyon floor, reached down a crevasse. Warmer than the surface, lit by lamps, and occupied by the people who run goods over the ice where no tram goes.
**Draw:** Second smuggler vendor (cold-resist gear, otherwise unobtainable), safe rest point deep in a hostile realm.
**Monsters:** `hoarfrost_stalker`, `glacier_drake_whelp`.

### 6.4 Aurora Shelf — vista, no level gate
A wind-scoured plateau above the blizzard line where the sky is clear and the aurora is permanently visible. Utterly silent. The tonal opposite of everything below it.
**Draw:** Vista (world-map reveal), Aurora Rest (rest buff), Holy-element gathering (aurora-ice).
**Monsters:** none (safe pocket) — though `aurora_seraphon` circles overhead as non-hostile ambience until Lv 63.

### 6.5 Hoarfrost Vault — Lv 60–68 — **HIDDEN**
The "lost frozen vaults" of the lore. Sealed doors at the back of the Statuary, openable only by carrying a Thawstone (drops from `statuary_colossus`) the length of the canyon before it melts — a timed traversal secret.
**Draw:** Timed-secret puzzle; the realm's best gear; the vault ledger that seeds the Umbral Rootways questline.
**Monsters:** `permafrost_lich`, `the_vault_keeper` *(rare)*.

### 6.6 Thronehall of Ice — Lv 66–72 — **BOSS**
A natural cathedral of blue ice at the canyon's head, floor polished to a mirror.
**Monsters:** `aurora_seraphon`, `permafrost_lich`, **`sylveth_silent_thaw`** *(boss, Lv 72)*.

---

## 7. REALM V — UMBRAL ROOTWAYS (Lv 70–99)

**Light:** `#ede7f6`. Tileset: dungeon (rune + obsidian) + new root set. Boss: **Verrocaine, the Horned Sovereign** (Lv 99).
*Formerly "Realm of Baphomet" — renamed per `DESIGN_AUDIT.md` §1.2. See `BESTIARY_EXPANSION.md` §7.*

No town portal leads here. Entry is by the Collapsed Skybridge (Realm III) or the Thronehall (Realm IV) only.

```
   [Skybridge, R.III] ──┐
                        ├──▶ Nethergate Descent (70-76)
   [Thronehall, R.IV] ──┘           │
                                    │
                         Bonemeal Hollows (74-82)
                                    │
                        ┌───────────┼───────────┐
                        │           │           │
              The Weeping      Sanguine    Thorncradle Vault
              Boughs (78-86)   Terrace     (86-93, ELITE)
                               (80-88,          │
                                HIDDEN)         │
                                    │           │
                                    └─────┬─────┘
                                          │
                          Throne of the Horned Sovereign
                                    (93-99, BOSS)
```

### 7.1 Nethergate Descent — Lv 70–76
Both approach routes converge on a shaft that goes down past the roots of the world tree, lit purple by nothing identifiable. Gravity feels wrong near the walls.
**Draw:** Entry hub, last Save Crystal before the endgame, the convergence beat (two routes, one door).
**Monsters:** `nethergate_creeper`, `umbral_houndkin`.

### 7.2 Bonemeal Hollows — Lv 74–82
Chambers where the soil is not soil. Root-hair the thickness of rope hangs from the ceiling and twitches toward warmth.
**Draw:** Main progression corridor; the realm's horror register established.
**Monsters:** `umbral_houndkin`, `rootfang_devourer`, `hollow_penitent_choir`.

### 7.3 The Weeping Boughs — Lv 78–86
Enormous downward-growing branches weeping a slow amber sap that is not sap. Poison-element saturated; standing still costs HP.
**Draw:** Environmental-hazard zone (the game's only DoT terrain); Poison reagent nodes for endgame crafting.
**Monsters:** `weeping_bough`, `rootfang_devourer`, `sanguine_thorncaller`.

### 7.4 Sanguine Terrace — Lv 80–88 — **HIDDEN**
A terraced garden, immaculately kept, red-lit, with a table set for eight. Someone maintains it. Entered only by *not* fighting the `sanguine_thorncaller` that guards the stair — the game's one pacifist gate.
**Draw:** Secret area; the single best lore payload in the game; unique accessory set.
**Monsters:** `sanguine_thorncaller` *(non-hostile unless struck)*.

### 7.5 Thorncradle Vault — Lv 86–93 — **ELITE CAMP**
A briar-walled bowl where the Sovereign's honour guard drills. Everything here is elite-tier; pulls are unforgiving. Full-party content and the last gear check before the throne.
**Draw:** Elite camp; the pre-boss gear gate.
**Monsters:** `abyssal_heraldon`, `thorncradle_warden` *(elite)*, `the_pale_apostate` *(rare)*.

### 7.6 Throne of the Horned Sovereign — Lv 93–99 — **BOSS**
A chamber of roots grown into the shape of a hall, and at the end of it a throne that was never built.
**Monsters:** `abyssal_heraldon`, `hollow_penitent_choir`, **`verrocaine_sovereign`** *(boss, Lv 99)*.

---

## 8. Sub-region draw summary

| Draw type | Count | Instances |
|---|---|---|
| Vista / lookout | 3 | Windmill Ridge, Ashfall Overlook, Aurora Shelf |
| Hidden / secret | 4 | Hollowroot Grove, Glasslight Reliquary, Hoarfrost Vault, Sanguine Terrace |
| Smuggler cave | 2 | Silt Warrens, Crevasse Undershelf |
| Elite camp | 2 | Raider's Palisade, Thorncradle Vault |
| Shortcut | 4 | Rooftop Walk (town), Hollowroot descent, Bilge Steps, Collapsed Skybridge |
| Gathering cluster | 5 | Bellflower hedgerows, Glasslight, Emberglass Terraces, Aurora Shelf, Weeping Boughs |
| Boss chamber | 5 | one per realm |
| **Total sub-regions** | **28** | 6 town districts + 1 tutorial + 21 wilderness |

---

## 9. Data representation

Sub-regions are added to `zaggers_database.json` as a **`subRegions` array on each zone object**. This is purely additive: `db_editor.html:748-750` reads only `z.id`, `z.name`, `z.minLv`, `z.maxLv`, `z.light`, `z.monsters`, and ignores unknown keys, so the zone table keeps rendering unchanged.

```jsonc
{
  "id": "meadows",
  "name": "Whispering Meadows",
  "minLv": 1, "maxLv": 16,
  "light": "#fff8e7",
  "monsters": "Bellflower Gloopling, Snagtooth Raider, Hornhaste Wasp, ...",  // display string — DO NOT structure
  "element": "Earth",
  "tileset": "meadow",
  "boss": "ordwin_palisade_tyrant",
  "connections": ["aethelgard", "sanctum"],
  "subRegions": [
    {
      "id": "bellflower_downs",
      "name": "Bellflower Downs",
      "minLv": 3, "maxLv": 8,
      "type": "field",                       // field | vista | hidden | cave | elite | boss | shortcut | district
      "draw": ["gathering", "save_crystal"],
      "monsters": ["gloopling_bellflower", "bramblehop", "hornhaste_wasp"],
      "connections": ["gatewatch_commons", "windmill_ridge", "thistlemarch_fen"],
      "description": "Rolling blue-flowered meadow ..."
    }
  ]
}
```

**Compatibility contract (do not break):** `zones[].monsters` stays a comma-joined **string**. Structured monster references live at `subRegions[].monsters` (array of monster ids). Aethelgard's `subRegions` use `"type": "district"`.

---

## 10. Open questions

Recorded in `.omc/plans/open-questions.md`:
- Is `zeny` kept as the currency name, or renamed alongside "Kafra"→"Kestrel Consignment"?
- Do vistas grant a persistent world-map reveal (needs a player-flags system) or a temporary buff only?
- Are the four transit stubs separate 64×64 maps, or edge-triggers on the town map?
- Instanced vs. open-world boss chambers — Phase 4 multiplayer will force this decision.
