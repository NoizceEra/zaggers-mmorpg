# ITEM ICONS REPORT — Task C

**Status:** Complete. Generated 2026-09-06.  
**Script:** `scripts/generate_item_icons.py` (PIL only, idempotent).

## Generated

24 icons at **32×32 RGBA**, dual-written to:

- `assets/sprites_ff/`
- `web/assets/sprites_ff/`

### Required 23 (`ASSET_MANIFEST.md` Task C)

| File | Subject |
|---|---|
| `potion_mana_ff.png` | Blue mana flask (mirrors red health potion) |
| `food_bread_ff.png` | Meadow loaf |
| `potion_aetherite_ff.png` | Holy gold draught + sparkles |
| `key_thawstone_ff.png` | Melting ice key |
| `wpn_shortsword_ff.png` | Bellflower shortsword |
| `wpn_cleaver_ff.png` | Snagtooth cleaver |
| `wpn_trident_ff.png` | Tidebreak trident |
| `wpn_emberglass_ff.png` | Emberglass jagged blade |
| `wpn_longbow_ff.png` | Hoarfrost longbow |
| `wpn_staff_root_ff.png` | Rootfang shadow staff |
| `shd_targe_ff.png` | Oaken targe |
| `shd_aegis_ff.png` | Nave aegis (heater) |
| `shd_bulwark_ff.png` | Forgewrought tower shield |
| `arm_jerkin_ff.png` | Traveller's leather jerkin |
| `arm_mythril_ff.png` | Mythril plate |
| `arm_slagplate_ff.png` | Slagworks plate (ember seams) |
| `arm_shroud_ff.png` | Umbral shroud |
| `hat_kettle_ff.png` | Militia kettle helm |
| `hat_circlet_ff.png` | Coral circlet |
| `hat_diadem_ff.png` | Aurora diadem |
| `acc_charm_ff.png` | Hedgerow leaf charm |
| `acc_pendant_ff.png` | Glasslight crystal pendant |
| `acc_signet_ff.png` | Sovereign's signet ring |

### Optional bonus

| File | Notes |
|---|---|
| `wpn_lance_dragon_ff.png` | New lance art; `dragon_lance.icon` updated off `excalibur_ff.png` placeholder |

## Verification

- All 24 files present in both target dirs at 32×32 RGBA.
- Every `items[].icon` in `web/zaggers_database.json` (25 entries) resolves to an on-disk file.
- Existing sprites (`potion_health_ff.png`, `excalibur_ff.png`, monster sheets) left untouched.

## Regenerate

```bash
python scripts/generate_item_icons.py
```
