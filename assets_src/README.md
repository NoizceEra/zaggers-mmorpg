# assets_src — Aseprite sources (authoring originals)

Exported PNGs in `assets/sprites_ff`, `assets/tiles_ff` (mirrored to
`web/assets/...`) are **build artifacts**. The originals live here as
`.aseprite` files. `tools/aseprite_pipeline.py` exports them
deterministically; `tools/gimp_batch_cleanup.py` and
`tools/krita_verify.py` gate the results.

Status (2026-09-07): **greenfield** — no `.aseprite` files committed yet.
Layout below is normative so the first sources land in the right place.

## File layout

```text
assets_src/
  README.md            (this file)
  heroes/*.aseprite    -> assets/sprites_ff/*.png   (256x256, 4x4 x 64px cells)
  monsters/*.aseprite  -> assets/sprites_ff/*.png   (256x256, 4x4 x 64px cells)
  npcs/*.aseprite      -> assets/sprites_ff/*.png   (256x256, 4x4 x 64px cells)
  singles/*.aseprite   -> assets/sprites_ff/*.png   (64x64 single frames,
                          e.g. hero_down/left/right/up)
  icons/*.aseprite     -> assets/sprites_ff/*.png   (32x32, items/equipment)
  tiles/*.aseprite     -> assets/tiles_ff/*.png     (128x64 iso diamonds)
  backgrounds/*.aseprite -> assets/tiles_ff/*.png   (free-size, no size gate)
```

Stem rule: `assets_src/heroes/hero_knight.aseprite` exports to
`assets/sprites_ff/hero_knight.png` (same stem, `.png`), then dual-writes
to `web/assets/sprites_ff/hero_knight.png` byte-identical.

## Tags (frame tags, one row each)

Every `heroes / monsters / npcs` sheet **must** define exactly these tags
in this order (row = tag index):

| Tag    | Row | Frames | Direction / use |
|--------|-----|--------|-----------------|
| Walk0  | 0   | 4      | Down / front    |
| Idle   | 1   | 4      | Left (mirrored for Right at runtime) |
| Walk1  | 2   | 4      | Right-side stride set |
| Attack | 3   | 4      | Up / back (faceless for heroes) |

Inspect with (no output written):

```bat
aseprite -b assets_src\heroes\hero_knight.aseprite --list-tags
```

## Layers (naming)

```text
outline   - 1px edge stroke, color #101020 (16,16,32); heroes/sheets only
base      - flat fills
shading   - soft shade pass
face      - eyes/features (rows 0-2 only for heroes; row 3 Up stays faceless;
            slime/blob needs eyes on EVERY row)
shadow    - leave EMPTY; shadow is standardized downstream at 40% black oval
            (see gimp_batch_cleanup.py), do not bake shadows in Aseprite
text      - FORBIDDEN on tiles (no baked sign text; env_house_shop-style
            signs are stripped in GIMP per TEXT_STRIP_GUIDE)
```

## Export commands

Check (never writes, never runs aseprite export):

```bat
python tools\aseprite_pipeline.py --check-only
```

Export everything (requires `aseprite` on PATH) + validate + dual-write:

```bat
python tools\aseprite_pipeline.py --export-all
```

Per-type equivalents (what `--export-all` runs internally):

```bat
:: 256x256 character sheet (heroes/monsters/npcs)
aseprite -b assets_src\heroes\hero_knight.aseprite --sheet assets\sprites_ff\hero_knight.png --sheet-type rows --sheet-width 256 --sheet-height 256

:: 32x32 icon
aseprite -b assets_src\icons\potion_health_ff.aseprite --sheet assets\sprites_ff\potion_health_ff.png --sheet-type rows --sheet-width 32 --sheet-height 32

:: 64x64 single frame
aseprite -b assets_src\singles\hero_down.aseprite --sheet assets\sprites_ff\hero_down.png --sheet-type rows --sheet-width 64 --sheet-height 64

:: 128x64 iso diamond tile
aseprite -b assets_src\tiles\tile_town_cobble.aseprite --sheet assets\tiles_ff\tile_town_cobble.png --sheet-type rows --sheet-width 128 --sheet-height 64
```

## Canonical gates (enforced by the pipeline)

- sheet: exactly 256x256, 4 non-blank rows, RGBA.
- tile: exactly 128x64, transparent corners + opaque center (diamond alpha).
- icon: exactly 32x32, RGBA.
- outline: edge-adjacent dark pixels converge on (16,16,32); drift is a
  WARN-grade issue fixed by `gimp_batch_cleanup.py --fix-outline`.
- dual-write: `assets/` and `web/assets/` copies must be byte-identical
  (md5); drift fails the gate.
- staleness: `.aseprite` newer than its `.png` output = STALE, re-export.
