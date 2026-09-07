# Isometric Blender renders → game sprites

Source models: `../models_3d/` (all Z-up, base at z=0; heights measured
2026-09-06: fountain 4.5 / brazier 5.7 / shop 6.81 / clocktower 22.0).
Output: this folder (`assets/renders/<name>_iso.png`) + identical web-parity
copies in `web/assets/tiles_ff/` (e.g. `env_house_shop.png`).

## 1. Camera (canonical — do not eyeball)

| Setting | Value |
|---|---|
| Camera type | **Orthographic** (`cam_data.type = 'ORTHO'`) |
| Rotation X | **54.73561°** (0.95532 rad — true 2:1 dimetric tilt) |
| Rotation Y | 0° |
| Rotation Z | **45°** (0.78540 rad) |
| Position | back along azimuth-45° diagonal at `dist = max(30, h*3+20)`, aimed at `(0,0,h/2)` |
| Ortho scale (baseline) | brazier **7.5** / fountain **8.0** / shop **9.5** / clocktower **24.0**; script auto-grows to `(h+2)*1.25` if taller |
| Lens / shift / DOF | irrelevant for ORTHO — leave default, DOF off |

Why these numbers: `web/index.html` (`TILE_W=48, TILE_H=24`, `worldToIso`)
is a 2:1 projection, so the render camera must be the matching 2:1 dimetric
(`arctan(1/2) ≈ 26.565°` elevation ⇔ `54.736°` X-tilt, 45° around Z).
Any perspective camera or wrong tilt will visibly clash with the
`128×64` diamond tiles.

## 2. Framing / export (matches existing `tiles_ff` conventions)

| Model | Canvas | Web-parity name |
|---|---|---|
| `prontera_fountain.obj` | 96×96 (`env_fountain.png` convention) | `env_fountain.png` |
| `dungeon_brazier.obj` | 96×128 (tall prop) | `env_torch_brazier.png` |
| `shop_building.obj` | 128×128 (`env_house_shop/row/terrace` convention) | `env_house_shop.png` |
| `guild_clocktower.obj` | 128×256 (tallest; cf. `env_house_guild` 128×176) | `env_guild_clocktower.png` |
| Tile reference | 128×64 diamond (`tile_meadow_grass` / `ART_PIPELINE_REPORT.md` spec) | — |

Export: PNG, **RGBA 8-bit, Film → Transparent ON**, 100%, square pixels,
~8px padding inside frame. Web runtime draws the 128×64 source scaled to the
`48×24` footprint (`image-rendering: pixelated`), so author at full res and
let the engine downscale — never pre-shrink the source.

## 3. Lighting / grounding (consistent across all four)

- Key: Sun, azimuth 45°, elevation ~50°, strength 3.0, soft shadows.
- Fill: second Sun from opposite side, 0.4, so shadow sides stay readable
  (matches the flat-shaded PIL sprites + `.mtl` `Kd` palette).
- EEVEE: 32 TAA samples + GTAO on (or Cycles 32 samples + denoise).
- AO: optional Cycles **Bake → Ambient Occlusion** pass (`--bake-ao`); the
  script never fails the batch if the bake is unavailable.
- Ground ellipse: mesh Circle at z=0.01, **scale Y ×0.5**, black alpha **0.35**,
  blend = Alpha Blend — the shared contact-shadow language with the
  `generate_env_expansion.py` props (oval shadow at base-centre anchor).

## 4. Run

```bat
:: needs Blender 3.6+ on PATH (bpy only exists inside Blender)
blender --background --python tools\blender_iso_render.py -- --models assets\models_3d --out assets\renders --web-out web\assets\tiles_ff
blender --background --python tools\blender_iso_render.py -- --list-jobs
blender --background --python tools\blender_iso_render.py -- --only shop_building --engine CYCLES --bake-ao
```

Plain `python tools\blender_iso_render.py` (no Blender) prints the manual
click-through steps and exits 2 — the full step list is embedded at the top
of the script (`MANUAL_STEPS`).

## 5. Web parity check

Rendered PNG keeps its source size; `web/index.html` loads it via
`envSpriteNames`/`terrainSpriteNames` from `assets/tiles_ff/`. After rendering,
verify the parity copy exists and is byte-identical:

```bat
fc assets\renders\shop_building_iso.png web\assets\tiles_ff\env_house_shop.png
```
