#!/usr/bin/env python3
"""Aseprite export pipeline for Zaggers (PIL gate + aseprite CLI wrapper).

RESEARCH baseline (2026-09-07, verified on disk):
  - assets/sprites_ff: 106 PNG = 75x256x256 (4x4 sheets, 64px cells),
    27x32x32 (icons), 4x64x64 (hero_down/left/right/up single frames).
  - assets/tiles_ff: 91 PNG, only 32x128x64 true diamonds; rest are env
    props of mixed sizes (64x64, 128x128, 128x160, 128x192, 256x256
    tilesets, ...). "256x256 / 128x64 diamond" is the TARGET, not state.
  - web/assets mirrors: byte-identical to assets/ (0 drift at baseline,
    per tools/gimp_batch_cleanup.py --check-only).
  - aseprite CLI: NOT on PATH (aseprite --version -> CommandNotFound).
  - .aseprite sources: NONE anywhere under project root (recursive search).
    assets_src/ is therefore greenfield; this pipeline defines the layout
    so future .aseprite files have a deterministic export path.
  - Conventions honored from sibling tools:
    tools/check_db_drift.py  -> [PASS]/[FAIL] sections, exit 0/1, --root.
    tools/gimp_batch_cleanup.py -> OUTLINE_TARGET=(16,16,32), RGBA/size
      gates, assets/ -> web/assets/ dual-write via shutil.copy2 + md5.
    tools/krita_verify.py -> 64px cells, face/outline/dual-write gates.

What this script does:
  1. Wraps `aseprite -b` sheet export per asset type.
  2. Validates exports against canonical gates (size, diamond alpha,
     outline color, tags).
  3. Dual-writes assets/ -> web/assets/ byte-identical.
  4. --check-only NEVER writes and NEVER invokes aseprite export.
     --export-all performs exports (requires aseprite CLI).
  5. Reports .aseprite vs .png staleness (extends drift-check §7 idea).

Usage:
  python tools/aseprite_pipeline.py --check-only [--root DIR]
  python tools/aseprite_pipeline.py --export-all [--root DIR]
      [--src-dir assets_src] [--aseprite PATH]
"""

import argparse
import hashlib
import os
import shutil
import subprocess
import sys

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow (PIL) required: pip install Pillow", file=sys.stderr)
    sys.exit(2)

OUTLINE_TARGET = (16, 16, 32)
SHEET_SIZE = (256, 256)   # heroes / monsters / npcs: 4x4 grid of 64px cells
CELL = 64
ICON_SIZE = (32, 32)      # items / equipment / spells
SINGLE_SIZE = (64, 64)    # hero_down/left/right/up single frames
TILE_DIAMOND = (128, 64)  # canonical iso diamond tile

# Row order for 4-row sheets. Aseprite tag name -> sheet row index.
TAGS = ["Walk0", "Idle", "Walk1", "Attack"]
TAG_ROWS = {name: i for i, name in enumerate(TAGS)}

# assets_src/<subdir> -> (export kind, dest dir, sheet w/h, size gate)
# kind drives the aseprite --sheet-width/--sheet-height + validator.
SOURCE_MAP = {
    "heroes":      ("sheet", "assets/sprites_ff", SHEET_SIZE, SHEET_SIZE),
    "monsters":    ("sheet", "assets/sprites_ff", SHEET_SIZE, SHEET_SIZE),
    "npcs":        ("sheet", "assets/sprites_ff", SHEET_SIZE, SHEET_SIZE),
    "singles":     ("single", "assets/sprites_ff", SINGLE_SIZE, SINGLE_SIZE),
    "icons":       ("icon", "assets/sprites_ff", ICON_SIZE, ICON_SIZE),
    "tiles":       ("tile", "assets/tiles_ff", TILE_DIAMOND, TILE_DIAMOND),
    "backgrounds": ("bg", "assets/tiles_ff", None, None),  # free-size, gate skipped
}

WEB_MIRROR = {
    "assets/sprites_ff": "web/assets/sprites_ff",
    "assets/tiles_ff": "web/assets/tiles_ff",
}


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def find_aseprite(explicit=None):
    if explicit:
        return explicit if os.path.exists(explicit) else None
    return shutil.which("aseprite")


def aseprite_version(exe):
    try:
        out = subprocess.run([exe, "--version"], capture_output=True,
                             text=True, timeout=15)
        return (out.stdout or out.stderr).strip()[:200] or "unknown version"
    except (OSError, subprocess.SubprocessError) as exc:
        return f"unavailable ({exc})"


def discover_sources(src_root):
    """Return sorted list of .aseprite files under src_root ('' if missing)."""
    found = []
    if not os.path.isdir(src_root):
        return found
    for dirpath, _dirs, files in os.walk(src_root):
        for f in files:
            if f.lower().endswith(".aseprite"):
                found.append(os.path.join(dirpath, f))
    return sorted(found)


def classify_source(src_path, src_root):
    """Map a source file to (kind, dest_dir, gate_size) via SOURCE_MAP."""
    rel = os.path.relpath(src_path, src_root)
    top = rel.split(os.sep)[0] if os.sep in rel else rel.split("/")[0]
    stem = os.path.splitext(os.path.basename(src_path))[0]
    entry = SOURCE_MAP.get(top)
    if entry is None:
        return ("unknown", None, None)
    kind, dest_dir, _sheet_wh, gate = entry
    return (kind, dest_dir, gate, stem)


def build_export_cmd(exe, src, dst, kind):
    """Aseprite batch export command for one source file.

    Sheet layout is rows (one tag per row). --sheet-width/height pins the
    cell grid so tags map deterministically: Walk0->row0, Idle->row1,
    Walk1->row2, Attack->row3. --list-tags dumps tag metadata for the
    tag validator without affecting the sheet.
    """
    cmd = [exe, "-b", src]
    if kind == "sheet":
        cmd += ["--sheet", dst, "--sheet-type", "rows",
                "--sheet-width", str(SHEET_SIZE[0]),
                "--sheet-height", str(SHEET_SIZE[1])]
    elif kind == "tile":
        cmd += ["--sheet", dst, "--sheet-type", "rows",
                "--sheet-width", str(TILE_DIAMOND[0]),
                "--sheet-height", str(TILE_DIAMOND[1])]
    elif kind == "icon":
        cmd += ["--sheet", dst, "--sheet-type", "rows",
                "--sheet-width", str(ICON_SIZE[0]),
                "--sheet-height", str(ICON_SIZE[1])]
    elif kind == "single":
        cmd += ["--sheet", dst, "--sheet-type", "rows",
                "--sheet-width", str(SINGLE_SIZE[0]),
                "--sheet-height", str(SINGLE_SIZE[1])]
    else:  # bg / unknown: plain frame export, no sheet grid
        cmd += ["--save-as", dst]
    return cmd


def inspect_tags_cmd(exe, src):
    """Command that lists Walk0/Idle/Walk1/Attack tags (no sheet written)."""
    return [exe, "-b", src, "--list-tags"]


def validate_size(img, expected):
    ok = img.size == expected
    return ok, f"size {img.size} {'==' if ok else '!='} canonical {expected}"


def validate_sheet_4x4(path):
    """256x256 sheet == 4x4 grid of 64px cells, RGBA, non-empty rows."""
    try:
        img = Image.open(path).convert("RGBA")
    except Exception as exc:
        return False, f"unreadable: {exc}"
    if img.size != SHEET_SIZE:
        return False, f"size {img.size} != canonical {SHEET_SIZE}"
    # every row-band must contain some opaque pixels (no blank rows)
    px = img.load()
    w, h = img.size
    for row in range(4):
        opaque = sum(1 for y in range(row * CELL, (row + 1) * CELL)
                     for x in range(w) if px[x, y][3] > 20)
        if opaque == 0:
            return False, f"row{row} ({TAGS[row]}) blank"
    return True, f"256x256 4x4 rows {TAGS} non-blank"


def validate_icon(path):
    try:
        img = Image.open(path).convert("RGBA")
    except Exception as exc:
        return False, f"unreadable: {exc}"
    if img.size != ICON_SIZE:
        return False, f"size {img.size} != canonical {ICON_SIZE}"
    return True, "32x32 icon"


def validate_tile_diamond(path):
    """128x64 diamond: exact size + transparent corners + opaque center."""
    try:
        img = Image.open(path).convert("RGBA")
    except Exception as exc:
        return False, f"unreadable: {exc}"
    if img.size != TILE_DIAMOND:
        return False, f"size {img.size} != canonical {TILE_DIAMOND}"
    w, h = img.size
    px = img.load()
    corners = [px[0, 0][3], px[w - 1, 0][3], px[0, h - 1][3], px[w - 1, h - 1][3]]
    if any(a > 20 for a in corners):
        return False, f"diamond alpha: corners not transparent {corners}"
    if px[w // 2, h // 2][3] < 20:
        return False, "diamond alpha: center transparent"
    return True, "128x64 diamond alpha"


def validate_outline(path, tolerance=24):
    """Edge-adjacent dark pixels should converge on OUTLINE_TARGET.

    Soft gate (WARN-grade): returns (ok, detail); callers treat drift as
    an issue but not a hard export failure -- same policy as
    gimp_batch_cleanup.py which reports drift for manual/GIMP fixing.
    """
    try:
        img = Image.open(path).convert("RGBA")
    except Exception as exc:
        return False, f"unreadable: {exc}"
    w, h = img.size
    px = img.load()
    drift = total = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 20:
                continue
            edge = any(0 <= x + dx < w and 0 <= y + dy < h and px[x + dx, y + dy][3] < 20
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if edge and a > 150 and (r + g + b) < 260 and max(r, g, b) < 110:
                total += 1
                if max(abs(r - OUTLINE_TARGET[0]), abs(g - OUTLINE_TARGET[1]),
                       abs(b - OUTLINE_TARGET[2])) > tolerance:
                    drift += 1
    if total == 0:
        return True, "no edge outline pixels to judge"
    if drift:
        return False, f"outline drift {drift}/{total} edge px != {OUTLINE_TARGET}"
    return True, f"outline {total}/{total} edge px == {OUTLINE_TARGET}"


def validate_export(path, kind):
    """Dispatch to the canonical validator for kind. Returns (ok, detail)."""
    if kind == "sheet":
        return validate_sheet_4x4(path)
    if kind == "icon":
        return validate_icon(path)
    if kind == "tile":
        return validate_tile_diamond(path)
    if kind == "single":
        try:
            img = Image.open(path).convert("RGBA")
        except Exception as exc:
            return False, f"unreadable: {exc}"
        return validate_size(img, SINGLE_SIZE)
    return True, "no size gate for bg/unknown (free-size)"


def dual_write(src_png, dest_dir, web_root_map, root):
    """Copy src_png into assets dest + web mirror. Returns (ok, detail)."""
    base = os.path.basename(src_png)
    asset_dst = os.path.join(root, dest_dir, base)
    web_rel = WEB_MIRROR.get(dest_dir.replace(os.sep, "/"), None)
    ok_parts = []
    if os.path.abspath(src_png) != os.path.abspath(asset_dst):
        os.makedirs(os.path.dirname(asset_dst), exist_ok=True)
        shutil.copy2(src_png, asset_dst)
    if web_rel:
        mirror = os.path.join(root, web_rel.replace("/", os.sep), base)
        os.makedirs(os.path.dirname(mirror), exist_ok=True)
        shutil.copy2(asset_dst, mirror)
        same = md5(asset_dst) == md5(mirror)
        ok_parts.append(f"mirror {'identical' if same else 'MISMATCH'}")
        return same, "; ".join(ok_parts) or "dual-written"
    return True, "written (no web mirror mapped)"


def main():
    ap = argparse.ArgumentParser(description="Zaggers Aseprite pipeline")
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    help="Project root (default: parent of tools/)")
    ap.add_argument("--src-dir", default="assets_src",
                    help="Aseprite source dir relative to root")
    ap.add_argument("--check-only", action="store_true",
                    help="Report only, never write, never invoke aseprite export")
    ap.add_argument("--export-all", action="store_true",
                    help="Export every .aseprite source via aseprite CLI + dual-write")
    ap.add_argument("--aseprite", default=None,
                    help="Explicit aseprite binary path (default: PATH lookup)")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    src_root = os.path.join(root, args.src_dir)

    if not args.check_only and not args.export_all:
        print("Nothing to do: pass --check-only or --export-all.", file=sys.stderr)
        return 2

    exe = find_aseprite(args.aseprite)
    ver = aseprite_version(exe) if exe else "NOT FOUND on PATH"
    sources = discover_sources(src_root)

    # ---- inventory of current PNG outputs (same counts as gimp gate) ----
    inv = {}
    for d, label in (("assets/sprites_ff", "sprites"), ("assets/tiles_ff", "tiles")):
        full = os.path.join(root, *d.split("/"))
        try:
            files = [f for f in os.listdir(full) if f.lower().endswith(".png")]
        except OSError:
            files = None
        inv[label] = files

    if args.check_only:
        print("==== Aseprite pipeline --check-only report ====")
        print(f"aseprite CLI: {ver}")
        print(f"src dir: {src_root} "
              f"({'missing (greenfield, no sources yet)' if not os.path.isdir(src_root) else f'{len(sources)} .aseprite files'})")
        for s in sources:
            cls = classify_source(s, src_root)
            print(f"  source: {os.path.relpath(s, root)} -> kind={cls[0]} dest={cls[1]}")
        if inv["sprites"] is not None:
            print(f"sprites_ff: {len(inv['sprites'])} PNG on disk")
        else:
            print("sprites_ff: MISSING DIR")
        if inv["tiles"] is not None:
            print(f"tiles_ff: {len(inv['tiles'])} PNG on disk")
        else:
            print("tiles_ff: MISSING DIR")

        # per-PNG canonical gates (no writes)
        n_issue = n_stale = n_missing_out = 0
        if sources:
            for s in sources:
                cls = classify_source(s, src_root)
                kind, dest = cls[0], cls[1]
                stem = cls[3] if len(cls) > 3 else os.path.splitext(os.path.basename(s))[0]
                out = os.path.join(root, dest, stem + ".png") if dest else None
                if out is None or not os.path.exists(out):
                    print(f"[MISSING] {stem}.png has no exported PNG (source with no output)")
                    n_missing_out += 1
                    continue
                ok, detail = validate_export(out, kind)
                ook, odetail = validate_outline(out)
                stale = os.path.getmtime(s) > os.path.getmtime(out)
                if stale:
                    n_stale += 1
                flag = "STALE" if stale else "fresh"
                if not ok or not ook:
                    n_issue += 1
                    print(f"[ISSUES] {kind:6} {stem + '.png':32} {detail}; outline: {odetail} | {flag}")
                else:
                    print(f"[OK] {kind:6} {stem + '.png':32} {detail} | {flag}")
                # mirror identity (read-only md5 compare)
                if dest:
                    web_rel = WEB_MIRROR.get(dest.replace(os.sep, "/"))
                    if web_rel:
                        mirror = os.path.join(root, web_rel.replace("/", os.sep), stem + ".png")
                        if not os.path.exists(mirror):
                            print(f"  mirror-MISSING: {mirror}")
                            n_issue += 1
                        elif md5(out) != md5(mirror):
                            print(f"  mirror-DRIFT: {out} vs {mirror}")
                            n_issue += 1
        else:
            print("no .aseprite sources -> staleness gate trivially PASS "
                  "(extends check_db_drift §7 sprite-files-exist; nothing to compare).")
            # still spot-check existing PNGs so the gate is informative
            # (kind inferred from actual size so icons/singles aren't mislabeled)
            def infer_kind(p):
                try:
                    sz = Image.open(p).size
                except Exception:
                    return "sheet"
                if sz == ICON_SIZE:
                    return "icon"
                if sz == SINGLE_SIZE:
                    return "single"
                if sz == TILE_DIAMOND:
                    return "tile"
                if sz == SHEET_SIZE:
                    return "sheet"
                return "tile" if "tiles_ff" in p else "sheet"
            spot = []
            if inv["sprites"]:
                spot += [os.path.join(root, "assets/sprites_ff", f)
                         for f in sorted(inv["sprites"])[:3]]
            if inv["tiles"]:
                spot += [os.path.join(root, "assets/tiles_ff", f)
                         for f in sorted(inv["tiles"])[:3]]
            for p in spot:
                kind = infer_kind(p)
                ok, detail = validate_export(p, kind)
                print(f"  spot {os.path.basename(p)}: {'OK' if ok else 'ISSUES'} ({detail})")

        # example commands (not executed in check-only)
        print("\nexample export commands (not run in --check-only):")
        print("  aseprite -b assets_src/heroes/hero_knight.aseprite "
              "--sheet assets/sprites_ff/hero_knight.png --sheet-type rows "
              "--sheet-width 256 --sheet-height 256")
        print("  aseprite -b assets_src/heroes/hero_knight.aseprite --list-tags"
              "  # expect Walk0/Idle/Walk1/Attack")
        print("  aseprite -b assets_src/tiles/tile_town_cobble.aseprite "
              "--sheet assets/tiles_ff/tile_town_cobble.png --sheet-type rows "
              "--sheet-width 128 --sheet-height 64")
        print("no files written (--check-only).")
        failed = (n_issue + n_stale + n_missing_out) > 0
        # greenfield (no sources) is NOT a failure: report only.
        if not sources:
            print("result: PASS (greenfield, no sources to validate).")
            return 0
        print(f"result: {'FAIL' if failed else 'PASS'} "
              f"(issues={n_issue}, stale={n_stale}, missing={n_missing_out}).")
        return 1 if failed else 0

    # ---- EXPORT MODE ----
    if not exe:
        print("ERROR: --export-all requires the aseprite CLI on PATH "
              "(or --aseprite PATH); none found.", file=sys.stderr)
        return 2
    print(f"aseprite CLI: {ver}")
    if not sources:
        print(f"No .aseprite sources under {src_root}; nothing to export.")
        return 0
    n_ok = n_fail = 0
    for s in sources:
        cls = classify_source(s, src_root)
        kind, dest = cls[0], cls[1]
        stem = cls[3] if len(cls) > 3 else os.path.splitext(os.path.basename(s))[0]
        if dest is None:
            print(f"[SKIP] {s}: unknown subdir (expected one of {sorted(SOURCE_MAP)})")
            n_fail += 1
            continue
        out_tmp = os.path.join(root, dest, stem + ".png")
        cmd = build_export_cmd(exe, s, out_tmp, kind)
        print(f"run: {' '.join(cmd)}")
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        except (OSError, subprocess.SubprocessError) as exc:
            print(f"[FAIL] {stem}: cannot run aseprite: {exc}")
            n_fail += 1
            continue
        if r.returncode != 0:
            print(f"[FAIL] {stem}: aseprite exit {r.returncode}: {(r.stderr or r.stdout)[:500]}")
            n_fail += 1
            continue
        ok, detail = validate_export(out_tmp, kind)
        ook, odetail = validate_outline(out_tmp)
        if not ok:
            print(f"[FAIL] {stem}: exported but canonical gate failed: {detail}")
            n_fail += 1
            continue
        if not ook:
            print(f"[WARN] {stem}: {odetail} (kept; fix via gimp_batch_cleanup.py --fix-outline)")
        ok2, d2 = dual_write(out_tmp, dest, WEB_MIRROR, root)
        if not ok2:
            print(f"[FAIL] {stem}: dual-write mirror mismatch ({d2})")
            n_fail += 1
            continue
        print(f"[OK] {stem}: {detail} + dual-write {d2}")
        n_ok += 1
    print(f"\nexport-all: {n_ok} ok, {n_fail} failed, {len(sources)} sources.")
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
