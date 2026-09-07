#!/usr/bin/env python3
"""GIMP batch cleanup for Zaggers sprites/tiles (PIL implementation).

GIMP-compatible logic, no GIMP install needed: every operation below maps
1:1 to a GIMP pdb call (noted in docstrings) so the same pass can later run
inside GIMP batch mode if desired.

What it does:
  1. Verifies RGBA + canonical size (sprites_ff -> 256x256, tiles_ff -> 128x64).
  2. Baked-text guidance: flags warm sign-text pixels inside known sign bands
     (e.g. tiles_ff/env_house_shop.png y~48-80) for manual GIMP text-strip.
  3. Normalizes outline to OUTLINE_TARGET=(16,16,32).
  4. Standardizes drop shadow: 40% black oval at y+4 in bottom band.
  5. Dual-writes assets/ -> web/assets/ mirrors, reports md5 drift.

RESEARCH baseline (2026-09-07, PIL sample):
  - assets/sprites_ff: 106 PNG (NOT 119) = 75x256x256, 27x32x32, 4x64x64.
  - assets/tiles_ff: 91 PNG, only 32x128x64 diamonds; rest are env props
    (64x64, 128x128, 128x160, 128x192, ...). "Mostly 256x256 / 128x64
    diamonds" is the TARGET, not current state.
  - web/assets mirrors: 106 + 91 files, 0 drift, 0 missing at baseline.
  - env_house_shop.png lives in tiles_ff (not sprites_ff), 128x128.
    Baked warm sign text concentrated y48-80 (~240 warm px, bands y48-64=65,
    y64-80=169). Edge-outline colors brownish (90,25,20), (60,50,40)...,
    NOT (16,16,32).
  - Shadow alpha variance (bottom 18% band, 12-sprite sample): semi-transparent
    frac 7-33%, uniq alpha values 3-5, mean alpha 38-126 -> non-standardized.
  - slime_green_ff.png 256x256: face band shows 5 dark shading-stripe
    groups (gaps at x~64,128,192), no two-eye signature -> flagged FACELESS.
  - Outline sampling (25 sprites): dominant edge colors (3,5,8), (45,48,55),
    (2,3,5)... -> drift vs target (16,16,32) confirmed.

Usage:
  python tools/gimp_batch_cleanup.py --check-only [--root DIR]
  python tools/gimp_batch_cleanup.py [--root DIR] [--strip-text] [--fix-shadow] [--fix-outline] [--fix-all]
  --check-only NEVER writes. Fix mode dual-writes assets/ + web/assets/.

GIMP pdb mapping (for future GIMP batch port):
  outline remap  -> gimp-image-select-color + gimp-drawable-set-pixel / bucket-fill
  text strip     -> gimp-image-select-rectangle + gimp-edit-clear + feather
  shadow oval    -> gimp-image-select-ellipse + gimp-edit-fill FG (0,0,0,102)
  mode/size      -> gimp-image-convert-rgba + gimp-image-scale
"""

import argparse
import hashlib
import os
import shutil
import sys

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("ERROR: Pillow (PIL) required: pip install Pillow", file=sys.stderr)
    sys.exit(2)

OUTLINE_TARGET = (16, 16, 32)
SPRITE_SIZE = (256, 256)
TILE_SIZE = (128, 64)
SHADOW_ALPHA = int(round(255 * 0.40))  # 40% black -> 102
SHADOW_BAND_FRAC = 0.18  # bottom 18% of image is the shadow zone
SHADOW_Y_OFFSET = 4  # oval center shifted y+4 from bottom-center baseline

# Relative (x0, y0, x1, y1) sign-text regions needing manual GIMP text-strip.
# env_house_shop.png measured: warm text y48-80 of 128px -> y 0.375-0.625.
TEXT_STRIP_GUIDE = {
    "env_house_shop.png": (0.05, 0.375, 0.95, 0.625),
    "env_house_inn.png": (0.05, 0.35, 0.95, 0.65),
    "env_house_guild.png": (0.05, 0.35, 0.95, 0.65),
    "env_house_smithy.png": (0.05, 0.35, 0.95, 0.65),
    "env_market_stall.png": (0.05, 0.30, 0.95, 0.60),
    "env_awning_stall.png": (0.05, 0.30, 0.95, 0.60),
    "env_notice_board.png": (0.10, 0.20, 0.90, 0.80),
    "env_guild_banner.png": (0.10, 0.20, 0.90, 0.80),
}
GENERIC_SIGN_BAND = (0.35, 0.65)  # fallback y-fraction band for env_* heuristic


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def is_warm_text(px):
    r, g, b, a = px
    return a > 200 and r > 190 and g > 150 and b < 150


def is_outline_candidate(px):
    r, g, b, a = px
    return a > 150 and (r + g + b) < 260 and max(r, g, b) < 110


def detect_outline_drift(img):
    """Count edge-adjacent dark pixels that are NOT the target outline color.

    GIMP equiv: select-by-color on near-black edge, histogram vs (16,16,32).
    """
    w, h = img.size
    px = img.load()
    drift = 0
    total = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 20:
                continue
            # edge-adjacent: touches transparency
            edge = False
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and px[nx, ny][3] < 20:
                    edge = True
                    break
            if edge and is_outline_candidate((r, g, b, a)):
                total += 1
                if (r, g, b) != OUTLINE_TARGET:
                    drift += 1
    return drift, total


def normalize_outline(img):
    """Remap edge-adjacent dark outline pixels to OUTLINE_TARGET.

    GIMP equiv: gimp-image-select-color (edge dark) + bucket-fill (16,16,32).
    Returns number of pixels remapped.
    """
    w, h = img.size
    px = img.load()
    changed = 0
    # precompute transparency mask for speed
    alpha = [[px[x, y][3] for x in range(w)] for y in range(h)]
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a <= 150 or not is_outline_candidate((r, g, b, a)):
                continue
            edge = False
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and alpha[ny][nx] < 20:
                    edge = True
                    break
            if edge and (r, g, b) != OUTLINE_TARGET:
                px[x, y] = (OUTLINE_TARGET[0], OUTLINE_TARGET[1], OUTLINE_TARGET[2], a)
                changed += 1
    return changed


def detect_baked_text(img, filename):
    """Count warm sign-text pixels inside the guided region.

    GIMP equiv: rect-select TEXT_STRIP_GUIDE box + histogram.
    """
    w, h = img.size
    box = TEXT_STRIP_GUIDE.get(filename)
    if box is None:
        if not os.path.basename(filename).startswith("env_"):
            return 0, None
        box = (0.05, GENERIC_SIGN_BAND[0], 0.95, GENERIC_SIGN_BAND[1])
    x0, y0, x1, y1 = int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)
    n = 0
    px = img.load()
    for y in range(max(0, y0), min(h, y1)):
        for x in range(max(0, x0), min(w, x1)):
            if is_warm_text(px[x, y]):
                n += 1
    return n, (x0, y0, x1, y1)


def detect_shadow_stats(img):
    """Bottom-band alpha stats. GIMP equiv: rect-select bottom band + histogram."""
    w, h = img.size
    band_h = max(1, int(h * SHADOW_BAND_FRAC))
    px = img.load()
    alphas = []
    for y in range(h - band_h, h):
        for x in range(w):
            alphas.append(px[x, y][3])
    semi = sum(1 for a in alphas if 5 < a < 235)
    return {
        "band_h": band_h,
        "semi_frac": semi / max(1, len(alphas)),
        "uniq": len(set(alphas)),
        "semi_count": semi,
    }


def standardize_shadow(img):
    """Clear bottom-band semi pixels, draw 40% black oval at y+4.

    GIMP equiv: rect-select bottom band -> feather 1px -> clear semi;
    ellipse-select (centered, y+4) -> fill FG (0,0,0) opacity 40%.
    Returns (cleared, drew) counts.
    """
    w, h = img.size
    band_h = max(1, int(h * SHADOW_BAND_FRAC))
    px = img.load()
    cleared = 0
    for y in range(h - band_h, h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if 5 < a < 235:
                px[x, y] = (r, g, b, 0)
                cleared += 1
    # draw standardized oval on overlay then composite
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    ow, oh = int(w * 0.55), max(2, int(band_h * 0.55))
    cx, cy = w // 2, (h - band_h // 2) + SHADOW_Y_OFFSET
    cy = min(h - oh // 2 - 1, max(oh // 2 + 1, cy))
    d.ellipse([cx - ow // 2, cy - oh // 2, cx + ow // 2, cy + oh // 2],
              fill=(0, 0, 0, SHADOW_ALPHA))
    img.alpha_composite(overlay)
    return cleared, ow * oh


def detect_faceless_slime(img, filename):
    """Heuristic: slime lacks a two-eye signature -> faceless.

    Eyes = EXACTLY 2 dark groups of eye-like width (6-45px) separated by a
    clear gap (>=15px) in the face band. Anything else (0, 1, or 3+ groups,
    e.g. shading stripes) is flagged faceless for a manual GIMP face pass.
    Baseline slime_green_ff.png shows 5 shading-stripe groups -> FACELESS.
    """
    if "slime" not in os.path.basename(filename).lower():
        return False, "n/a (not slime)"
    w, h = img.size
    y0, y1 = int(h * 0.23), int(h * 0.55)
    px = img.load()
    cols = []
    for x in range(w):
        c = 0
        for y in range(y0, y1):
            r, g, b, a = px[x, y]
            if a > 150 and (r + g + b) < 220:
                c += 1
        cols.append(c)
    thr = max(2, (y1 - y0) // 4)
    active = [x for x, c in enumerate(cols) if c > thr]
    if not active:
        return True, "no dark clusters in face band"
    groups = []
    start = prev = active[0]
    for x in active[1:]:
        if x - prev > 4:  # gap -> new group
            groups.append((start, prev))
            start = x
        prev = x
    groups.append((start, prev))
    widths = [b - a + 1 for a, b in groups]
    eye_like = [g for g, wd in zip(groups, widths) if 6 <= wd <= 45]
    gaps = [eye_like[i + 1][0] - eye_like[i][1] for i in range(len(eye_like) - 1)]
    if len(eye_like) == 2 and min(gaps) >= 15:
        return False, f"two eye-like groups {eye_like}"
    return True, f"{len(groups)} dark groups {groups[:5]} (eye-like: {eye_like}) -> FACELESS"


def check_file(path, kind):
    """Full per-file check. Returns dict of issues (no writes)."""
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    base = os.path.basename(path)
    expected = SPRITE_SIZE if kind == "sprite" else TILE_SIZE
    issues = []
    if img.size != expected:
        issues.append(f"size {img.size} != canonical {expected}")
    if img.mode != "RGBA":
        issues.append(f"mode {img.mode} != RGBA")
    drift, total = detect_outline_drift(img)
    if total and drift:
        issues.append(f"outline drift {drift}/{total} edge px != {OUTLINE_TARGET}")
    ntext, box = detect_baked_text(img, base)
    if ntext > 20:
        issues.append(f"baked-text ~{ntext} warm px in guide box {box} -> GIMP text-strip needed")
    sh = detect_shadow_stats(img)
    if sh["semi_frac"] > 0.35 or sh["uniq"] > 6:
        issues.append(f"shadow non-standard semi_frac={sh['semi_frac']:.2%} uniqA={sh['uniq']}")
    face, detail = detect_faceless_slime(img, base)
    if face:
        issues.append(f"faceless-slime: {detail}")
    return {
        "file": base, "path": path, "size": (w, h),
        "outline_drift": (drift, total), "text_px": ntext,
        "shadow": sh, "faceless": face, "issues": issues,
    }


def main():
    ap = argparse.ArgumentParser(description="Zaggers GIMP batch cleanup (PIL, GIMP-compatible)")
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    help="Project root (default: parent of tools/)")
    ap.add_argument("--check-only", action="store_true", help="Report only, never write")
    ap.add_argument("--strip-text", action="store_true", help="Fix mode: clear guided text boxes")
    ap.add_argument("--fix-shadow", action="store_true", help="Fix mode: standardize shadow")
    ap.add_argument("--fix-outline", action="store_true", help="Fix mode: normalize outline")
    ap.add_argument("--fix-all", action="store_true", help="Fix mode: all fixes (except text unless --strip-text)")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    sdir = os.path.join(root, "assets", "sprites_ff")
    tdir = os.path.join(root, "assets", "tiles_ff")
    wsdir = os.path.join(root, "web", "assets", "sprites_ff")
    wtdir = os.path.join(root, "web", "assets", "tiles_ff")

    pairs = []
    for d, kind in ((sdir, "sprite"), (tdir, "tile")):
        if not os.path.isdir(d):
            print(f"ERROR: missing dir {d}", file=sys.stderr)
            return 2
        for f in sorted(os.listdir(d)):
            if f.lower().endswith(".png"):
                pairs.append((os.path.join(d, f), kind))

    if args.check_only:
        n_issue = 0
        n_size = n_outline = n_text = n_shadow = n_face = 0
        drift_pairs = 0
        for path, kind in pairs:
            r = check_file(path, kind)
            base = r["file"]
            mirror = os.path.join(wsdir if kind == "sprite" else wtdir, base)
            mstat = "mirror-OK"
            if not os.path.exists(mirror):
                mstat = "mirror-MISSING"
                drift_pairs += 1
            elif md5(path) != md5(mirror):
                mstat = "mirror-DRIFT"
                drift_pairs += 1
            if r["issues"]:
                n_issue += 1
                for iss in r["issues"]:
                    if iss.startswith("size"):
                        n_size += 1
                    elif iss.startswith("outline"):
                        n_outline += 1
                    elif iss.startswith("baked-text"):
                        n_text += 1
                    elif iss.startswith("shadow"):
                        n_shadow += 1
                    elif iss.startswith("faceless"):
                        n_face += 1
                print(f"[ISSUES] {kind:6} {base:32} {r['size']} | {'; '.join(r['issues'])} | {mstat}")
        print("\n==== GIMP batch cleanup --check-only report ====")
        print(f"files scanned: {len(pairs)} "
              f"(sprites={sum(1 for _, k in pairs if k == 'sprite')}, "
              f"tiles={sum(1 for _, k in pairs if k == 'tile')})")
        print(f"files with issues: {n_issue}/{len(pairs)}")
        print(f"  size != canonical (sprites {SPRITE_SIZE}, tiles {TILE_SIZE}): {n_size}")
        print(f"  outline drift (!= {OUTLINE_TARGET}): {n_outline}")
        print(f"  baked-text guidance hits: {n_text}")
        print(f"  shadow non-standard: {n_shadow}")
        print(f"  faceless slime: {n_face}")
        print(f"mirror drift/missing (assets vs web/assets): {drift_pairs}")
        print("note: env_house_shop.png is tiles_ff/128x128; sign-text band y0.375-0.625.")
        print("no files written (--check-only).")
        return 1 if (n_issue or drift_pairs) else 0

    # ---- FIX MODE (dual-write) ----
    do_outline = args.fix_outline or args.fix_all
    do_shadow = args.fix_shadow or args.fix_all
    if not (do_outline or do_shadow or args.strip_text or args.fix_all):
        print("Nothing to do: pass --fix-all [--strip-text] or run --check-only.", file=sys.stderr)
        return 2
    fixed = 0
    for path, kind in pairs:
        img = Image.open(path).convert("RGBA")
        base = os.path.basename(path)
        expected = SPRITE_SIZE if kind == "sprite" else TILE_SIZE
        changed = False
        if img.size != expected:
            img = img.resize(expected, Image.LANCZOS)  # GIMP: gimp-image-scale
            changed = True
        if do_outline and normalize_outline(img) > 0:  # GIMP: select-color + fill
            changed = True
        if args.strip_text or args.fix_all:
            ntext, box = detect_baked_text(img, base)
            # Only auto-clear when explicitly asked AND text signal is strong,
            # otherwise leave sign art intact for manual GIMP pass.
            if args.strip_text and ntext > 20 and box:
                d = ImageDraw.Draw(img)
                d.rectangle(box, fill=(0, 0, 0, 0))
                changed = True
        if do_shadow and (args.fix_shadow or args.fix_all):
            standardize_shadow(img)  # GIMP: ellipse-select + fill 40%
            changed = True
        if changed or args.fix_all:
            img.save(path)
            mirror = os.path.join(wsdir if kind == "sprite" else wtdir, base)
            os.makedirs(os.path.dirname(mirror), exist_ok=True)
            shutil.copy2(path, mirror)  # dual-write assets/ -> web/assets/
            fixed += 1
    print(f"fixed + dual-written {fixed}/{len(pairs)} files (assets/ -> web/assets/).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
