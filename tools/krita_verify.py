#!/usr/bin/env python3
"""Krita touch-up verifier (research gate, NOT a painter).

Checks, with PIL, the defects described in tools/krita_touchup_guide.md:
  - 256x256 / 32x32 (/ tile 128x64) sizes + RGBA
  - faces present on Down/Left/Right rows, Up row faceless (heroes)
  - slime rows 2-3 face presence (row3 must not be blank)
  - outline color still present (hero #101020, slime #0C461C families)
  - tile_town_cobble not too dark navy (lum + blue-cast)
  - 27 icons not flat (unique colors + luminosity spread)
  - assets/ <-> web/assets/ dual-write byte identity
  - hero_monk/thief mirror history (thief must be exact mirror; monk warns)

Usage:
  python tools/krita_verify.py [--icons] [--root .]
Exit code 1 when any FAIL is present. WARNs never fail the build.
"""
import argparse
import filecmp
import glob
import os
import statistics
import sys

try:
    from PIL import Image, ImageChops
except ImportError:
    print("FAIL: Pillow (PIL) is required: pip install pillow")
    sys.exit(2)

CELL = 64
FACE_BAND = (20, 20, 44, 36)  # inside one 64x64 cell
EYE_DARK = 60                  # RGB all < 60 => eye-like dark pixel
FACE_PRESENT_MIN = 10          # per-cell FAIL threshold (face must exist)
FACE_WARN_MIN = 50             # per-cell WARN threshold (face looks weak)

HERO_OUTLINE = (16, 16, 32)    # measured hero_knight edge color
SLIME_OUTLINE = (12, 70, 28)   # measured slime edge color
OUTLINE_TOL = 10

ICON_MIN_COLORS = 12
ICON_MIN_LUM_STD = 45.0

TILE_MIN_LUM = 45.0            # cobble must reach at least this mean luminosity
TILE_MAX_BLUE_CAST = 6         # B-R must be <= this (neutral, not navy)

FAILURES = []
WARNS = []


def fail(msg):
    FAILURES.append(msg)
    print(f"FAIL: {msg}")


def warn(msg):
    WARNS.append(msg)
    print(f"WARN: {msg}")


def ok(msg):
    print(f"OK:   {msg}")


def band_dark_count(cell):
    band = cell.crop(FACE_BAND)
    n = 0
    for p in band.getdata():
        if p[3] > 128 and p[0] < EYE_DARK and p[1] < EYE_DARK and p[2] < EYE_DARK:
            n += 1
    return n


def row_cells(path, row):
    im = Image.open(path).convert("RGBA")
    return [im.crop((c * CELL, row * CELL, (c + 1) * CELL, (row + 1) * CELL)) for c in range(4)]


def check_size(path, expect, label):
    if not os.path.exists(path):
        fail(f"{label} missing: {path}")
        return False
    try:
        im = Image.open(path)
    except Exception as e:
        fail(f"{label} unreadable {path}: {e}")
        return False
    if im.size != expect:
        fail(f"{label} size {im.size} != {expect}: {path}")
        return False
    if im.mode != "RGBA":
        fail(f"{label} mode {im.mode} != RGBA: {path}")
        return False
    ok(f"{label} {expect[0]}x{expect[1]} RGBA: {os.path.basename(path)}")
    return True


def has_outline(path, target, label):
    im = Image.open(path).convert("RGBA")
    px = [p for p in im.crop((0, 0, 64, 64)).getdata() if p[3] > 128]
    for p in px:
        if all(abs(p[i] - target[i]) <= OUTLINE_TOL for i in range(3)):
            ok(f"{label} outline rgb{target} present")
            return True
    fail(f"{label} outline rgb{target} (tol {OUTLINE_TOL}) not found in first cell")
    return False


def check_hero_faces(path, label, up_must_be_faceless=True):
    """Rows 0-2 must have faces; row3 (Up) must be faceless for heroes."""
    for row in (0, 1, 2):
        counts = [band_dark_count(c) for c in row_cells(path, row)]
        if all(v < FACE_PRESENT_MIN for v in counts):
            fail(f"{label} row{row} faceless (band dark {counts}, need >= {FACE_PRESENT_MIN} in a cell)")
        elif any(v < FACE_WARN_MIN for v in counts):
            warn(f"{label} row{row} weak face (band dark {counts}, want >= {FACE_WARN_MIN}/cell)")
            ok(f"{label} row{row} face present (weak): {counts}")
        else:
            ok(f"{label} row{row} face present: {counts}")
    counts = [band_dark_count(c) for c in row_cells(path, 3)]
    if up_must_be_faceless:
        if any(v >= FACE_PRESENT_MIN for v in counts):
            fail(f"{label} row3 (Up) still has eyes: band dark {counts} (want all < {FACE_PRESENT_MIN})")
        else:
            ok(f"{label} row3 (Up) faceless: {counts}")
    else:
        if all(v < FACE_PRESENT_MIN for v in counts):
            fail(f"{label} row3 faceless (band dark {counts})")
        else:
            ok(f"{label} row3 face present: {counts}")


def check_slime(path):
    label = "slime_green_ff"
    for row in (0, 1, 2):
        counts = [band_dark_count(c) for c in row_cells(path, row)]
        if all(v < FACE_PRESENT_MIN for v in counts):
            fail(f"{label} row{row} faceless (band dark {counts})")
        elif any(v < FACE_WARN_MIN for v in counts):
            warn(f"{label} row{row} weak/thin face (band dark {counts}, want >= {FACE_WARN_MIN}/cell)")
            ok(f"{label} row{row} face present (weak): {counts}")
        else:
            ok(f"{label} row{row} face present: {counts}")
    counts = [band_dark_count(c) for c in row_cells(path, 3)]
    if all(v < FACE_PRESENT_MIN for v in counts):
        fail(f"{label} row3 faceless (band dark {counts}) — blob needs eyes on every row")
    else:
        ok(f"{label} row3 face present: {counts}")


def mirror_diff(path):
    im = Image.open(path).convert("RGBA")
    r1 = im.crop((0, 64, 256, 128))
    r2 = im.crop((0, 128, 256, 192))
    mirrored = Image.new("RGBA", (256, 64))
    for c in range(4):
        cell = r1.crop((c * 64, 0, (c + 1) * 64, 64)).transpose(Image.FLIP_LEFT_RIGHT)
        mirrored.paste(cell, (c * 64, 0))
    d = ImageChops.difference(r2.convert("RGB"), mirrored.convert("RGB"))
    return sum(r + g + b for r, g, b in d.getdata())


def check_mirror(path, label, exact=True):
    diff = mirror_diff(path)
    if exact:
        if diff != 0:
            fail(f"{label} row2 is not an exact mirror of row1 (diff {diff})")
        else:
            ok(f"{label} row2 exact mirror of row1")
    else:
        if diff == 0:
            ok(f"{label} row2 exact mirror of row1")
        else:
            warn(f"{label} row2 not exact mirror of row1 (diff {diff}) — OK only if intentional detail-swap, see guide Card C")


def check_tile(path):
    label = "tile_town_cobble"
    im = Image.open(path).convert("RGB")
    px = list(im.getdata())
    avg = tuple(sum(c[i] for c in px) // len(px) for i in range(3))
    lums = [0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2] for p in px]
    mean = sum(lums) / len(lums)
    cast = avg[2] - avg[0]
    if mean < TILE_MIN_LUM:
        fail(f"{label} too dark: lum-mean {mean:.1f} < {TILE_MIN_LUM} (avg rgb {avg})")
    else:
        ok(f"{label} brightness lum-mean {mean:.1f} (avg rgb {avg})")
    if cast > TILE_MAX_BLUE_CAST:
        fail(f"{label} navy cast: B-R = {cast} > {TILE_MAX_BLUE_CAST} (avg rgb {avg})")
    else:
        ok(f"{label} neutral cast B-R = {cast}")


def check_icon(path):
    name = os.path.basename(path)
    im = Image.open(path).convert("RGB")
    px = list(im.getdata())
    uniq = len(set(px))
    lums = [0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2] for p in px]
    std = statistics.pstdev(lums) if len(lums) > 1 else 0.0
    bad = []
    if uniq < ICON_MIN_COLORS:
        bad.append(f"only {uniq} colors (< {ICON_MIN_COLORS})")
    if std < ICON_MIN_LUM_STD:
        bad.append(f"lum-std {std:.1f} (< {ICON_MIN_LUM_STD})")
    if bad:
        fail(f"icon flat {name}: {'; '.join(bad)}")
        return False
    ok(f"icon shaded {name}: {uniq} colors, lum-std {std:.1f}")
    return True


def check_dual(a, b, label):
    if not os.path.exists(a):
        fail(f"{label} missing authoring copy: {a}")
        return
    if not os.path.exists(b):
        fail(f"{label} missing web mirror: {b}")
        return
    if filecmp.cmp(a, b, shallow=False):
        ok(f"{label} dual-write identical")
    else:
        fail(f"{label} dual-write MISMATCH: {a} vs {b}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--icons", action="store_true", help="also run the 27-icon flatness pass")
    ap.add_argument("--all", action="store_true", help="run everything including icons")
    args = ap.parse_args()
    root = args.root
    run_icons = args.icons or args.all or True  # default: full gate

    a = lambda *p: os.path.join(root, *p)  # noqa: E731

    knight = a("assets", "sprites_ff", "hero_knight.png")
    slime = a("assets", "sprites_ff", "slime_green_ff.png")
    monk = a("assets", "sprites_ff", "hero_monk.png")
    thief = a("assets", "sprites_ff", "hero_thief.png")
    cobble = a("assets", "tiles_ff", "tile_town_cobble.png")

    print("== sizes ==")
    for p, exp, label in [
        (knight, (256, 256), "hero_knight"),
        (slime, (256, 256), "slime_green_ff"),
        (monk, (256, 256), "hero_monk"),
        (thief, (256, 256), "hero_thief"),
        (cobble, (128, 64), "tile_town_cobble"),
    ]:
        check_size(p, exp, label)

    print("== hero faces / Up faceless ==")
    if os.path.exists(knight):
        check_hero_faces(knight, "hero_knight", up_must_be_faceless=True)
    if os.path.exists(slime):
        print("== slime faces ==")
        check_slime(slime)

    print("== outlines ==")
    if os.path.exists(knight):
        has_outline(knight, HERO_OUTLINE, "hero_knight")
    if os.path.exists(slime):
        has_outline(slime, SLIME_OUTLINE, "slime_green_ff")

    print("== mirror history (monk/thief) ==")
    if os.path.exists(thief):
        check_mirror(thief, "hero_thief", exact=True)
    if os.path.exists(monk):
        check_mirror(monk, "hero_monk", exact=False)

    print("== tile brightness ==")
    if os.path.exists(cobble):
        check_tile(cobble)

    if run_icons:
        print("== icons (27x 32x32) ==")
        icons = sorted(glob.glob(os.path.join(root, "assets", "sprites_ff", "*.png")))
        icons = [f for f in icons if Image.open(f).size == (32, 32)]
        print(f"found {len(icons)} 32x32 icons")
        if len(icons) != 27:
            warn(f"expected 27 icons, found {len(icons)}")
        for f in icons:
            check_size(f, (32, 32), "icon")
            check_icon(f)

    print("== dual-write ==")
    check_dual(knight, a("web", "assets", "sprites_ff", "hero_knight.png"), "hero_knight")
    check_dual(slime, a("web", "assets", "sprites_ff", "slime_green_ff.png"), "slime_green_ff")
    check_dual(monk, a("web", "assets", "sprites_ff", "hero_monk.png"), "hero_monk")
    check_dual(thief, a("web", "assets", "sprites_ff", "hero_thief.png"), "hero_thief")
    check_dual(cobble, a("web", "assets", "tiles_ff", "tile_town_cobble.png"), "tile_town_cobble")

    print(f"\nSUMMARY: {len(FAILURES)} FAIL, {len(WARNS)} WARN")
    for m in FAILURES:
        print(f"  FAIL: {m}")
    for m in WARNS:
        print(f"  WARN: {m}")
    sys.exit(1 if FAILURES else 0)


if __name__ == "__main__":
    main()
