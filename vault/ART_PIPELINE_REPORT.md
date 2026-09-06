# ART PIPELINE REPORT — Phase 3 Bestiary & Environment Expansion

**Status:** Complete. Generated 2026-09-06.
**Scripts:** `scripts/generate_bestiary_expansion.py` (monsters), `scripts/generate_env_expansion.py` (tiles + props).

---

## 1. What was generated

### Monsters (`assets/sprites_ff/` + `web/assets/sprites_ff/`)

| Task | Count | Detail |
|---|---|---|
| A — Renames | 6 | `slime_green_ff`→`gloopling_bellflower_ff`, `goblin_ff`→`snagtooth_raider_ff`, `skeleton_ff`→`drowned_marrowguard_ff`, `cactuar_ff`→`pricklespine_thornmarch_ff`, `bomb_ff`→`cinderpuff_ff`, `boss_baphomet_ff`→`verrocaine_sovereign_ff`. Pixels copied byte-for-byte (re-saved through PIL as RGBA, no redraw) — the three "recommend a redraw" flags in `BESTIARY_EXPANSION.md` §9 (Thornmarch/Cinderpuff/Verrocaine head silhouettes) are **not** addressed here; they were marked optional/non-blocking touch-ups (`ASSET_MANIFEST.md` Task A2) and were left for a follow-up pass. |
| B — New monsters | 48 | Full 4-row × 4-col (Down/Left/Right/Up × Walk0/Idle/Walk1/Attack) 256×256 RGBA sheets, one per zone band P0–P4. |
| **Total** | **54** | Matches `BESTIARY_EXPANSION.md` §10 total and the 54 `monsters` entries in `web/zaggers_database.json` exactly — verified programmatically (see §4). |

### Environment (`assets/tiles_ff/` + `web/assets/tiles_ff/`)

| Task | Count | Detail |
|---|---|---|
| D — New iso floor tiles | 19 | 128×64 diamond, alpha-masked to match `generate_terrain_tilesets.py`'s existing tile format exactly (the pipeline doc's 64×32 spec is superseded by the shipped 128×64 convention already in use — confirmed against the on-disk `tile_meadow_grass.png` etc.). Covers meadow (4), sanctum (4), spire (3), and two brand-new categories `ice` (4) and `root` (4). |
| E — New environmental props | 38 | Variable-size RGBA sprites with ground-contact drop shadows, sized and anchored exactly per the `ASSET_MANIFEST.md` Task E table (16 Aethelgard district props + 14 wilderness + 8 chasm/rootways). |
| **Total** | **57** | |

**Grand total new/changed art files:** 54 (monsters) + 57 (env) = **111**, each written to both `assets/` and `web/assets/` (222 files on disk total).

---

## 2. Pipeline approach

Both scripts follow the exact conventions of the pre-existing generators studied before writing any code:

- `generate_clean_monsters.py` → monster sheet layout (256×256, 4×4 grid, `normalize_and_center_cell()` re-used **verbatim** so every new sprite is bounded to 44–52px and centered at (32,32), identical to the legacy six), PIL primitive drawing (ellipse/polygon/line, no external assets), flat-shaded palette with a dark outline + light highlight per shape, oval drop shadow at the base.
- `generate_terrain_tilesets.py` → 128×64 isometric diamond tiles, `is_inside_diamond` / diamond alpha-masking, per-pixel noise-shaded fill with a blended border, reused as-is.
- `generate_env_assets.py` → variable-size prop canvases, oval ground shadow at the anchor point, flat polygon/ellipse construction.

**Monsters** are produced through a library of 7 parametric archetypes (`BLOB`, `BIPED`, `QUAD`, `FLYER`, `PLANT`, `CONSTRUCT`, `BOSS`) rather than 48 fully bespoke hand-painted functions. Each of the 48 new monsters gets its own config (element-derived palette from `BESTIARY_EXPANSION.md` §1's 9-element color table, silhouette proportions, accessories, weapon type) so no two sheets are identical, but the shape-composition code is shared. This was a deliberate scope trade-off to cover all 48 sheets at production quality within the pass — **flagged as a deviation** from "fully bespoke art per monster"; see §5.

**Environment props** similarly use 8 shared archetypes (`PILLAR`, `BANNER`, `ORGANIC`, `FIGURE`, `HAZARD-GLOW`, `OVERHEAD`, `CONTAINER`, `WALL`) parametrized per the manifest's exact filename/size/anchor/district.

Element → color mapping (from `BESTIARY_EXPANSION.md` §1.1) drives monster palettes so zone signature elements read visually (Fire=orange/red Spire monsters, Water=blue Sanctum/Chasm, Shadow=purple Rootways, etc.), and boss configs get a larger scale, crown, cape, and glowing eyes to read as endgame-tier silhouettes.

---

## 3. Deviations from the manifest

1. **Tile size**: `PIPELINE_AND_TOOLS.md` specifies 64×32 diamond tiles; the actual on-disk convention (and `generate_terrain_tilesets.py`) is **128×64**. Followed the shipped convention, not the doc, since matching existing pixels was the explicit instruction.
2. **Task A2 touch-ups** (recolor/redraw passes on the 3 renamed sprites with recognizable FF silhouettes) were **not done** — they're explicitly optional/non-blocking in the manifest. Flagged here for a follow-up pass if wanted.
3. **Monster/prop art is procedural/parametric**, not 54+38 fully unique hand-authored paintings (see §2). Every sheet is still original composition-per-monster (unique proportions/colors/accessories/weapon), matches the sheet format and centering rules exactly, and is visually distinguishable at a glance — but archetypes are reused across some monsters within the same family (e.g. all "robed caster" monsters share a construction skeleton). This was necessary to deliver full 54/38 coverage within the pass.
4. **Item icons (Task C)** — completed in a follow-up pass via `scripts/generate_item_icons.py` (see §6). **Optional NPC/hero sheets (Task F, 4 files)** remain out of scope.
5. Godot `.png.import` sidecars for the 6 renamed files were **not** created/renamed — only the `.png` files themselves were written under the new names; the old originals and their `.import` sidecars remain on disk untouched (not deleted).

---

## 4. Verification performed

- Both generator scripts run their own post-generation check: every expected filename exists in both target directories at 256×256 RGBA (monsters) / correct declared W×H (props) / valid diamond tile (tiles).
- Cross-checked every `sprite` field in the `monsters` object of `web/zaggers_database.json` (54 entries) against `web/assets/sprites_ff/` — **0 missing files, 0 mismatches**.
- Manual visual spot-check of a sample from each monster archetype (blob/wisp, boss, construct, serpent, flyer, overhead plant) and a sample of the new tiles rendered correctly as distinct, readable diamond/sprite art.

## 5. How to regenerate or extend

```bash
python scripts/generate_bestiary_expansion.py   # renames + all 48 new monster sheets
python scripts/generate_env_expansion.py        # 19 tiles + 38 props
python scripts/generate_item_icons.py           # Task C: 23 item icons (+ optional dragon lance)
```

Both scripts are idempotent (safe to re-run; they overwrite their own output only). To add a new monster: add an entry to the `MONSTERS` dict in `generate_bestiary_expansion.py` picking one of the 7 archetype factories (`make_blob`/`make_biped`/`make_quad`/`make_flyer`/`make_plant`/`make_construct`/`make_boss`) and a config dict (body color, scale, weapon, accessories). To add a new tile or prop, add a tuple to `TILES` or `PROPS` in `generate_env_expansion.py`.

---

## 6. Item icons follow-up (Task C) — 2026-09-06

**Script:** `scripts/generate_item_icons.py`  
**Output:** 24 × 32×32 RGBA icons dual-written to `assets/sprites_ff/` and `web/assets/sprites_ff/` (23 required + optional `wpn_lance_dragon_ff.png`).

| Category | Files |
|---|---|
| Consumables | `potion_mana_ff`, `food_bread_ff`, `potion_aetherite_ff`, `key_thawstone_ff` |
| Weapons | `wpn_shortsword_ff`, `wpn_cleaver_ff`, `wpn_trident_ff`, `wpn_emberglass_ff`, `wpn_longbow_ff`, `wpn_staff_root_ff`, (+ `wpn_lance_dragon_ff`) |
| Shields | `shd_targe_ff`, `shd_aegis_ff`, `shd_bulwark_ff` |
| Armor | `arm_jerkin_ff`, `arm_mythril_ff`, `arm_slagplate_ff`, `arm_shroud_ff` |
| Headgear | `hat_kettle_ff`, `hat_circlet_ff`, `hat_diadem_ff` |
| Accessories | `acc_charm_ff`, `acc_pendant_ff`, `acc_signet_ff` |

Style matched to existing `potion_health_ff.png`: flat fills, outline `(16,16,32)`, soft drop shadow, highlight speck. `dragon_lance.icon` retargeted from `excalibur_ff.png` → `wpn_lance_dragon_ff.png`. `mythril_armor` already pointed at `arm_mythril_ff.png`. Cross-check: all 25 `items[].icon` paths in `web/zaggers_database.json` resolve on disk.
