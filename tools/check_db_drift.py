#!/usr/bin/env python3
"""DB source-of-truth drift check for Zaggers.

Source of truth: web/zaggers_database.json (schemaVersion, classes,
skills, items, monsters). This script cross-checks the JSON against
hardcoded duplicates in GDScript/JS/HTML and sprite files on disk.

Checked:
  1. Schema version + top-level section counts
  2. Classes: DB `classes` vs HERO_DEFS in scripts/party_data.gd
  3. Skills: DB `skills` count (expected baseline 66)
  4. Shop: DB `items` vs SHOP_CATALOG in scripts/shop_ui.gd
  5. Monsters: DB `monsters` vs initMonsters() in server/server.js
  6. Web spriteNames in web/index.html vs DB-referenced sprites
  7. Sprite file existence in assets/sprites_ff, web/assets/sprites_ff,
     assets/tiles_ff (+ web mirror)

Usage: python3 tools/check_db_drift.py [--root DIR]
Exit code: 0 if every section PASSes, 1 otherwise.
"""

import argparse
import json
import os
import re
import sys

EXPECTED_SCHEMA_VERSION = 2
EXPECTED_CLASS_COUNT = 11
EXPECTED_SKILL_COUNT = 66
EXPECTED_MONSTER_COUNT = 54

SPRITE_DIRS = [
    "assets/sprites_ff",
    "web/assets/sprites_ff",
    "assets/tiles_ff",
    "web/assets/tiles_ff",
]


def load_text(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def extract_bracket_block(text, anchor_regex):
    """Return the [...] block following the first match of anchor_regex."""
    m = re.search(anchor_regex, text)
    if not m:
        return None
    start = text.find("[", m.end() - 1 if text[m.end() - 1] == "[" else m.end())
    if start == -1:
        # anchor itself may end with the bracket
        start = text.find("[", m.start())
    if start == -1:
        return None
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "[":
            depth += 1
        elif text[i] == "]":
            depth -= 1
            if depth == 0:
                return text[start : i + 1]
    return None


def stem(filename):
    """Strip .png (and .import) to get the asset key used in index.html."""
    base = os.path.basename(filename or "")
    if base.endswith(".import"):
        base = base[: -len(".import")]
    if base.lower().endswith(".png"):
        base = base[: -len(".png")]
    return base


def main():
    ap = argparse.ArgumentParser(description="Zaggers DB drift check")
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    help="Project root (default: parent of tools/)")
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    db_path = os.path.join(root, "web", "zaggers_database.json")
    party_path = os.path.join(root, "scripts", "party_data.gd")
    shop_path = os.path.join(root, "scripts", "shop_ui.gd")
    server_path = os.path.join(root, "server", "server.js")
    index_path = os.path.join(root, "web", "index.html")

    results = []  # (section, passed, detail)

    def report(section, passed, detail):
        results.append((section, passed, detail))
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {section}: {detail}")

    # ---- Load DB ----
    try:
        with open(db_path, "r", encoding="utf-8") as fh:
            db = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[FAIL] database-load: cannot load {db_path}: {exc}")
        return 1

    schema_version = db.get("schemaVersion")
    classes = db.get("classes", {}) or {}
    skills = db.get("skills", {}) or {}
    items = db.get("items", {}) or {}
    monsters = db.get("monsters", {}) or {}

    # ---- 1. Schema ----
    report(
        "schema-version",
        schema_version == EXPECTED_SCHEMA_VERSION,
        f"schemaVersion={schema_version} (expected {EXPECTED_SCHEMA_VERSION}), "
        f"sections={{classes:{len(classes)}, skills:{len(skills)}, "
        f"items:{len(items)}, monsters:{len(monsters)}}}",
    )

    # ---- 2. Classes vs HERO_DEFS ----
    try:
        party_src = load_text(party_path)
        hero_block = extract_bracket_block(party_src, r"HERO_DEFS[^=]*=")
        hero_names = re.findall(r'"name"\s*:\s*"([^"]+)"', hero_block or "")
        hero_icons = re.findall(r'"icon"\s*:\s*"([^"]+)"', hero_block or "")
        hero_icon_files = [os.path.basename(p) for p in hero_icons]
        db_class_sprites = sorted({c.get("sprite", "") for c in classes.values()})
        missing_icons = [s for s in db_class_sprites if s and s not in hero_icon_files]
        passed = len(classes) == len(hero_names) == EXPECTED_CLASS_COUNT and not missing_icons
        report(
            "classes-vs-hero-defs",
            passed,
            f"DB classes={len(classes)} (expected {EXPECTED_CLASS_COUNT}), "
            f"HERO_DEFS={len(hero_names)} {hero_names}, "
            f"DB class sprites missing from HERO_DEFS icons={missing_icons or 'none'}",
        )
    except OSError as exc:
        report("classes-vs-hero-defs", False, f"cannot read party_data.gd: {exc}")

    # ---- 3. Skills count ----
    report(
        "skills-count",
        len(skills) == EXPECTED_SKILL_COUNT,
        f"DB skills={len(skills)} (expected {EXPECTED_SKILL_COUNT})",
    )

    # ---- 4. Shop catalog vs DB items ----
    try:
        shop_src = load_text(shop_path)
        shop_block = extract_bracket_block(shop_src, r"SHOP_CATALOG[^=]*=")
        shop_names = re.findall(r'"name"\s*:\s*"([^"]+)"', shop_block or "")
        shop_icons = re.findall(r'"icon"\s*:\s*"([^"]+)"', shop_block or "")
        db_item_names = {str(v.get("name", "")).lower(): k for k, v in items.items()}
        matched = [n for n in shop_names if n.lower() in db_item_names]
        unmatched = [n for n in shop_names if n.lower() not in db_item_names]
        # Shop is intentionally a subset of DB items; PASS requires every
        # shop entry to resolve to a DB item.
        passed = len(shop_names) > 0 and not unmatched
        report(
            "shop-vs-db-items",
            passed,
            f"DB items={len(items)}, SHOP_CATALOG={len(shop_names)} {shop_names}, "
            f"matched={len(matched)}, unmatched={unmatched or 'none'}, "
            f"shop icons={[os.path.basename(p) for p in shop_icons]}",
        )
    except OSError as exc:
        report("shop-vs-db-items", False, f"cannot read shop_ui.gd: {exc}")

    # ---- 5. Monsters vs server initMonsters ----
    try:
        server_src = load_text(server_path)
        db_backed = ("zaggers_database.json" in server_src and "db.monsters" in server_src)
        types_block = extract_bracket_block(server_src, r"const types\s*=")
        if types_block is None:
            # fall back to the initMonsters function body
            m = re.search(r"function initMonsters\(\)\s*\{(.*?)\n\}", server_src, re.S)
            types_block = m.group(1) if m else ""
        server_monster_names = re.findall(r"name\s*:\s*['\"]([^'\"]+)['\"]", types_block or "")
        # strip "(Boss)" suffix for comparison, e.g. "Baphomet (Boss)"
        normalized_server = {re.sub(r"\s*\(.*\)\s*$", "", n).lower() for n in server_monster_names}
        db_monster_names = {str(v.get("name", "")).lower() for v in monsters.values()}
        db_monster_ids = {str(k).lower() for k in monsters.keys()}
        matched = [n for n in normalized_server if n in db_monster_names or n in db_monster_ids]
        unmatched = [n for n in normalized_server if n not in db_monster_names and n not in db_monster_ids]
        if db_backed and len(monsters) == EXPECTED_MONSTER_COUNT:
            # Server loads full DB at runtime (with legacy fallback); static fallback list is not the source.
            report(
                "monsters-vs-server",
                True,
                f"DB monsters={len(monsters)} (expected {EXPECTED_MONSTER_COUNT}), "
                f"server DB-backed loader present, fallback spawns={len(server_monster_names)}",
            )
        else:
            passed = (
                len(monsters) == EXPECTED_MONSTER_COUNT
                and len(server_monster_names) == len(monsters)
                and not unmatched
            )
            report(
                "monsters-vs-server",
                passed,
                f"DB monsters={len(monsters)} (expected {EXPECTED_MONSTER_COUNT}), "
                f"server initMonsters spawns={len(server_monster_names)} {server_monster_names}, "
                f"matched={len(matched)}, unmatched={unmatched or 'none'}",
            )
    except OSError as exc:
        report("monsters-vs-server", False, f"cannot read server.js: {exc}")

    # ---- 6. Web spriteNames vs DB sprites ----
    try:
        html = load_text(index_path)

        def parse_js_list(var):
            m = re.search(r"const\s+" + re.escape(var) + r"\s*=\s*\[(.*?)\];", html, re.S)
            if not m:
                return []
            return re.findall(r"'([^']+)'", m.group(1))

        sprite_names = parse_js_list("spriteNames")
        env_names = parse_js_list("envSpriteNames")
        terrain_names = parse_js_list("terrainSpriteNames")
        known = set(sprite_names) | set(env_names) | set(terrain_names)
        # index.html loader strips a trailing "_ff" for monster lookups and
        # also maps tileset_town_ff to tiles; accept both suffixed/unsuffixed.
        known_variants = set(known) | {n[:-3] if n.endswith("_ff") else n + "_ff" for n in known}

        db_sprite_stems = set()
        for section in (classes, monsters, items):
            for entry in section.values():
                if isinstance(entry, dict):
                    for key in ("sprite", "icon"):
                        if entry.get(key):
                            db_sprite_stems.add(stem(entry[key]))
        missing_from_web = sorted(s for s in db_sprite_stems if s and s not in known_variants)
        passed = not missing_from_web
        report(
            "web-spritenames-vs-db",
            passed,
            f"spriteNames={len(sprite_names)}, env={len(env_names)}, "
            f"terrain={len(terrain_names)}, DB sprite refs={len(db_sprite_stems)}, "
            f"DB sprites missing from web lists={missing_from_web or 'none'}",
        )
    except OSError as exc:
        report("web-spritenames-vs-db", False, f"cannot read web/index.html: {exc}")

    # ---- 7. Sprite file existence ----
    file_refs = set()
    for section in (classes, monsters, items):
        for entry in section.values():
            if isinstance(entry, dict):
                for key in ("sprite", "icon"):
                    if entry.get(key):
                        file_refs.add(os.path.basename(entry[key]))
    try:
        hero_icons
    except NameError:
        hero_icons = []
    try:
        shop_icons
    except NameError:
        shop_icons = []
    for p in list(hero_icons) + list(shop_icons):
        file_refs.add(os.path.basename(p))
    try:
        for n in sprite_names + env_names + terrain_names:
            file_refs.add(n + ".png")
    except NameError:
        pass
    file_refs = {f for f in file_refs if f}
    # .import sidecar files are Godot artifacts, not real sprites
    file_refs = {f for f in file_refs if not f.endswith(".import")}

    dir_listings = {}
    for d in SPRITE_DIRS:
        full = os.path.join(root, d.replace("/", os.sep))
        try:
            dir_listings[d] = set(os.listdir(full))
        except OSError:
            dir_listings[d] = None

    missing_any = {}
    for f in sorted(file_refs):
        found_in = [d for d, listing in dir_listings.items() if listing is not None and f in listing]
        if not found_in:
            # tiles live in tiles_ff, sprites in sprites_ff — a file only
            # needs to exist in ONE appropriate dir, but report per-dir.
            missing_any[f] = [d for d in SPRITE_DIRS if dir_listings.get(d) is not None]

    all_dirs_ok = all(v is not None for v in dir_listings.values())
    passed = all_dirs_ok and not missing_any
    missing_show = sorted(missing_any)[:20]
    detail = (
        f"sprite refs={len(file_refs)}, "
        + ", ".join(
            f"{d}={'MISSING DIR' if v is None else str(len(v)) + ' files'}"
            for d, v in dir_listings.items()
        )
        + f", refs found nowhere={missing_show or 'none'}"
        + (f" (+{len(missing_any) - len(missing_show)} more)" if len(missing_any) > len(missing_show) else "")
    )
    report("sprite-files-exist", passed, detail)

    # ---- Summary ----
    failed = [s for s, ok, _ in results if not ok]
    print(f"\nDrift check: {len(results) - len(failed)}/{len(results)} sections PASS")
    if failed:
        print("Failing sections: " + ", ".join(failed))
        return 1
    print("All sections PASS — DB is in sync with runtime code and assets.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
