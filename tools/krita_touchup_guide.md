# Krita Touch-Up Guide — Zaggers sprite / tile / icon pass

**Scope:** manual Krita touch-ups only. Do NOT repaint binaries by script — this guide + `tools/krita_verify.py` only.
**Source of truth (PIL research, 2026-09-07):** all hero/monster sheets are 256×256 RGBA (4 cols × 4 rows of 64×64 cells; row0=Down, row1=Left, row2=Right, row3=Up). Icons are 32×32 RGBA (27 files). `tile_town_cobble.png` is 128×64 RGBA. `assets/` and `web/assets/` copies are currently byte-identical — keep them so (dual-write on every export).
**History:** `hero_monk` / `hero_thief` Right-row duplication was fixed by mirroring Left (see `vault/SPRITE_ANIMATION_FIXES_REPORT.md` Bug 1; master later replaced `hero_monk` with a simpler placeholder — see Card C).

**Global Krita setup (do once):**
- `Settings → Configure Krita → General → Zoom`: enable HiDPI pixel-grid; `View → Show Pixel Grid` ON when editing 32×32 icons.
- Image interpolation: `Image → Scale Image To New Size` filter = Nearest Neighbour (never Mitchell/Hermite on pixel art).
- Keep a reference layer: open the matching `web/assets/...` copy side-by-side for before/after compare.
- Export: `File → Export → PNG`, no metadata, sRGB, no scaling. Then dual-write (see bottom of every card).

---

## Card A — `hero_knight.png` — row3 (Up) still has eyes/face

- **File:** `assets/sprites_ff/hero_knight.png` (+ mirror `web/assets/sprites_ff/hero_knight.png`)
- **Cells affected:** row3 only = `r3c0..r3c3` → pixel boxes `(0..256, 192..256)`, each cell 64×64. Do NOT touch rows 0–2 (verified distinct: row diffs r0–r1 ≈ 1.72M, r0–r2 ≈ 1.96M — genuinely different poses).
- **Defect (measured):** face-band probe `(x 20–44, y 20–36 inside each 64px cell)`, eye-dark = RGB all < 60 & alpha > 128:
  row0 = [59,85,59,56] · row1 = [83,87,83,80] · row2 = [83,89,83,76] · **row3 = [32,34,32,31] (should be 0)**. Row3 white highlight px = 20 vs row0 = 241 — the Up cells kept eye pixels but lost the front highlight = back-of-head with leftover face.
- **Krita brush/settings:**
  - Clone/cover: `Pixel Art → Pixel Hard Edge`, size 2–3px, opacity 100%, composite `Source Over`. Sample surrounding helmet-back fill (≈ steel `#5F8CD7` highlight, mid `#2D4B8C`, shadow `#1B2A52`) with `Ctrl+click`.
  - Outline repair: 1px `Pixel Hard Edge`, outline color `#101020` (measured most-common dark edge, 348 px in reference cell). Keep 1px unbroken silhouette.
  - Hair/back detail: 1–2px hard edge, plume shadow `#8A6D1F` over gold `#EBAF23` where the crest wraps to the back; no skin tone on row3.
  - Zoom 400–800%, Pixel Grid ON, `Isolate Layer` on the paint layer (keep original as locked reference layer below).
- **Steps:** 1) duplicate layer, lock original. 2) In each r3 cell, paint over the two eye clusters + brow shadow in the face band with helmet-back gradient (dark at edges → mid center). 3) Remove the 20 stray white px (front glint) — replace with steel highlight `#B9D7FF` single-pixel edge only. 4) Restore 1px `#101020` outline where the erase softened it.
- **Before checklist:** ☐ r3c0–c3 each show ≥30 eye-dark px in the probe band ☐ back-of-head reads as face at 2× zoom.
- **After checklist:** ☐ probe band eye-dark = 0 in all four r3 cells (run `tools/krita_verify.py`) ☐ rows 0–2 untouched (row diffs unchanged ±1%) ☐ silhouette still 1px `#101020` ☐ 256×256 RGBA preserved.
- **Export + dual-write:** export to `assets/sprites_ff/hero_knight.png`, then `copy assets\sprites_ff\hero_knight.png web\assets\sprites_ff\hero_knight.png` (byte-identical required).

## Card B — `slime_green_ff.png` — rows 2–3 faceless / weak face

- **File:** `assets/sprites_ff/slime_green_ff.png` (+ mirror `web/assets/sprites_ff/slime_green_ff.png`)
- **Cells affected:** row2 `(0..256, 128..192)` touch-up + row3 `(0..256, 192..256)` full face paint. Rows 0–1 are the reference (row0 opaque 6404, white-hi 180, dark 378).
- **Defect (measured):** per-row totals (opaque 6404 all rows): row0 white 180 / dark 378 · row1 white 158 / dark 186 · row2 white 158 / dark 186 · **row3 white 135 / dark 0**. Face-band per-cell dark: row0 [110,102,86,80] · row1 [55,39,18,39] · row2 [36,39,37,39] · **row3 [0,0,0,0]**. Row3 has zero eye/mouth pixels (fully faceless); row2 keeps palette but at ~1/3 the row0 eye density and reads flat at 2×. (Row1c2 = 18 dark px is the weakest keeper — inspect it in the same pass.)
- **Krita brush/settings:**
  - Body match: fills body `#198C32` (751 px, dominant), light `#32D74B` (406 px), outline dark green `#0C461C` (253 px). Eye dark `#142319`-ish (measured `(20,35,25)` family), glint white `#F0FFF5` (44 px in reference).
  - Brush: `Pixel Hard Edge` 1–2px for eyes/mouth, `Airbrush Soft` 8–12px @ 20% for body volume behind the face (never over the outline).
  - Symmetry: use `Mirror → Horizontal` guides per 64px cell when placing the two oval eyes so Left/Right rows stay consistent.
- **Steps:** 1) Copy row0c1 eyes (oval ~8×10px + 2px white glint top-left of each eye) as a floating selection template. 2) Row3: stamp/paint both eyes + small mouth arc centered `(32,30)` per cell, recolor edge 1px to `#0C461C`. 3) Row2: darken/thicken existing eye ovals to row0 density (≈80–110 dark px per cell in the probe band), restore glints. 4) Never touch the squash-bounce silhouette (cols 0–3 are Walk0/Idle/Walk1/Attack widths — keep them).
- **Before checklist:** ☐ row3 probe = 0/0/0/0 ☐ row2 probe ≤ 40/cell ☐ row2/row3 look blank vs row0 at 2×.
- **After checklist:** ☐ every cell rows 0–3 probe dark ≥ 10 (FAIL threshold) and rows 0–2 ≥ 50 (WARN threshold — run verifier) ☐ white glint present each cell ☐ outline still `#0C461C` family ☐ 256×256 RGBA.
- **Export + dual-write:** export to `assets/sprites_ff/slime_green_ff.png`, then copy to `web/assets/sprites_ff/slime_green_ff.png`.

## Card C — `hero_monk.png` / `hero_thief.png` — mirror history (verify, do not repaint yet)

- **Files:** `assets/sprites_ff/hero_monk.png`, `assets/sprites_ff/hero_thief.png` (+ `web/` mirrors).
- **History (from `vault/SPRITE_ANIMATION_FIXES_REPORT.md`):** original bug = row2 (Right) was a copy of row0 (Down) for both classes (row0-vs-row2 diff ≈ 193k, ~4× lower than any other pair). Fix = regenerate row2 as a per-frame horizontal mirror of row1 (each 64px column mirrored in place, NOT the whole 256px row flipped). Later, master replaced `hero_monk.png` with a simpler placeholder (~2.2 KB, only 5–6 unique colors per cell vs thief's 24–25) that carries an intentional hair/detail swap breaking exact mirroring.
- **Cells affected:** none unless verifier FAILs — this card is verify-only. If you must repaint: row2 only, `r2c0..r2c3`.
- **Measured now:** mirror-check `diff(mirror_frames(row1), row2)`: **thief = 0 (perfect mirror, PASS)** · monk = 259,400 (near-mirror with detail swap, WARN-level) · knight = 721,863 (fully distinct art, expected). Monk row diffs: r0–r1 93,900 / r1–r2 60,480 / r0–r3 109,440 — structurally consistent placeholder, no Down-duplication relapse. Thief row diffs all 419k–845k (distinct).
- **Krita brush/settings (only if a relapse is found):** select row1 frame `c` → `Layer → Transform → Mirror Horizontal` on that 64×64 selection only → paste into row2 same column. Brush touch-up `Pixel Hard Edge` 1px for the headband knot side-swap. Do NOT flip the whole row (would reverse Walk0/Idle/Walk1/Attack order).
- **Before checklist:** ☐ read the vault report §Bug 1 + post-merge note ☐ run verifier mirror section.
- **After checklist:** ☐ thief mirror diff stays 0 ☐ monk: either exact mirror (0) or documented detail-swap with both side views reading correctly at 2× ☐ row0-vs-row2 diff stays >> 200k (no Down-copy relapse) ☐ dual-write byte-identical.

## Card D — `tile_town_cobble.png` — too dark navy

- **File:** `assets/tiles_ff/tile_town_cobble.png` (+ mirror `web/assets/tiles_ff/tile_town_cobble.png`)
- **Cells affected:** whole tile 128×64 (all cobbles + mortar). Reference sibs: `tile_town_cobble2.png`, `tile_town_brick.png`, `tile_town_border.png`.
- **Defect (measured):** cobble avg RGB **(26,30,40)** lum-mean **30.6**, max lum 116.9, 105 unique colors — darkest town tile and blue-cast (B−R = +14). Sibs for comparison: cobble2 avg (37,37,37) lum 37.3 · brick avg (63,34,25) lum 41.9 · border avg (39,44,54) lum 44.0. At 1× in the town map it reads as a navy hole next to the border/brick set.
- **Krita brush/settings:**
  - Non-destructive: add `Filter Layer → Brightness/Contrast` (+18 brightness, +6 contrast) + `Filter Layer → Color Balance` (shadows −10 blue, midtones −5 blue) above the locked original; or `Filter Mask → Levels` lifting gamma to ≈1.25.
  - Stone tops: `Chalk → Chalk Details` 6–10px @ 40% with neutral warm grey `#6B6F7A` stipple on each cobble crown; mortar stays dark `#14161F`.
  - Target: lum-mean **45–55**, avg channel spread |R−G|,|G−B| ≤ 6 (neutral), keep max lum ≤ 170 to avoid bloom against `tile_town_border`.
- **Steps:** 1) duplicate/lock original. 2) Apply brightness + desaturate-blue filter layers. 3) Stipple 1–2 highlight px clusters per cobble, keep 1px dark mortar grid. 4) Check tiling: `Filter → Map → Tile` preview at 2×2 for seams.
- **Before checklist:** ☐ avg (26,30,40) / lum 30.6 ☐ visibly navy vs cobble2/brick in-map.
- **After checklist:** ☐ lum-mean 45–55, B−R ≤ 6 ☐ still 128×64 RGBA, seamless 2×2 ☐ reads as stone next to cobble2 without glowing.
- **Export + dual-write:** export to `assets/tiles_ff/tile_town_cobble.png`, then copy to `web/assets/tiles_ff/tile_town_cobble.png`.

## Card E — 27 item icons 32×32 — flat (batch shading pass)

- **Files (all in `assets/sprites_ff/` + `web/assets/sprites_ff/` mirrors):** `acc_charm_ff`, `acc_pendant_ff`, `acc_signet_ff`, `arm_jerkin_ff`, `arm_mythril_ff`, `arm_shroud_ff`, `arm_slagplate_ff`, `excalibur_ff`, `food_bread_ff`, `hat_circlet_ff`, `hat_diadem_ff`, `hat_kettle_ff`, `key_thawstone_ff`, `potion_aetherite_ff`, `potion_health_ff`, `potion_mana_ff`, `prop_crystal_save`, `shd_aegis_ff`, `shd_bulwark_ff`, `shd_targe_ff`, `wpn_cleaver_ff`, `wpn_emberglass_ff`, `wpn_lance_dragon_ff`, `wpn_longbow_ff`, `wpn_shortsword_ff`, `wpn_staff_root_ff`, `wpn_trident_ff` (each `.png`, 32×32 RGBA).
- **Defect (measured):** only **5–9 unique RGB colors per icon** (e.g. trident 5, staff_root 7, aetherite 9) and low luminosity spread — flattest: `wpn_staff_root_ff` lum-std 21.3 · `arm_shroud_ff` 32.0 · `arm_slagplate_ff` 32.5; even the best (`potion_aetherite_ff` 96.9) lacks a true outline+shadow+glint triple. At inventory 1× they read as silhouettes. (Count per `vault/ITEM_ICONS_REPORT.md` was 24 generated + `potion_health`/`excalibur`/`prop_crystal_save` = 27 on disk now.)
- **Krita brush/settings (batch, same recipe every icon):**
  - Outline: `Pixel Hard Edge` 1px, near-black of the icon's hue (e.g. blades `#101018`, leather `#1A120C`, glass `#0B1B22`). Close all silhouette gaps first.
  - Shade: 1px inner shadow, multiply @ 50% one step darker than base; 1–2px hard highlight top-left, screen @ 60% (`#FFFFFF` for glass/metal, warm `#FFE9B0` for bread/leather).
  - Dither: `Pixel Hard Edge` 1px checkerboard between base and shadow on curved surfaces (potions, shields) — 3–6 px only.
  - Target per icon: **≥ 12 unique colors**, lum-std **≥ 45**, glint present on metal/glass, readable at 100% and 200%.
  - Grid: `View → Show Pixel Grid`, zoom 800%, `Brush → Spacing 1.0`, opacity 100% (no soft airbrush on 32×32 except 1px glow on aetherite pendant).
- **Steps per icon:** 1) close outline 2) inner shadow bottom-right 3) top-left hard glint 4) 1px dither transition 5) 100%/200% readability check against `potion_aetherite_ff` (current best) as reference.
- **Before checklist:** ☐ each icon 5–9 colors ☐ no consistent light source ☐ outline gaps at 800%.
- **After checklist:** ☐ each icon ≥ 12 colors + lum-std ≥ 45 (verifier lists violators) ☐ 32×32 RGBA preserved ☐ dual-write identical per file.
- **Export + dual-write (per file):** export to `assets/sprites_ff/<name>.png`, then `copy assets\sprites_ff\<name>.png web\assets\sprites_ff\<name>.png`. Batch-check with `python tools/krita_verify.py --icons`.

---

## Dual-write rule (every card)

Game code reads from `web/assets/...`; authoring source is `assets/...`. After each Krita export: copy the file to the mirror path and re-run `python tools/krita_verify.py`. The verifier also asserts byte-identity — never edit only one side.
