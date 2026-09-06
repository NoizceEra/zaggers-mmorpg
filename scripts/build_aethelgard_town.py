#!/usr/bin/env python3
"""Densify Aethelgard master town envStructures while preserving topology.

Reads web/maps/aethelgard.json, keeps tiles / NPCs / exits / subRegions / meta,
replaces envStructures with a denser district-aware prop set (~80–150).

Only references env_* PNGs present in web/assets/tiles_ff/.
Missing optional types (env_house_inn, env_wall_curtain, env_gatehouse, etc.)
are skipped automatically.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "web" / "maps" / "aethelgard.json"
TILES_FF = ROOT / "web" / "assets" / "tiles_ff"

# Canonical prop footprints used across maps (animated braziers use frame size).
PROP_META: dict[str, tuple[int, int, int, int]] = {
    "env_obelisk_aetherite": (96, 192, 48, 176),
    "env_fountain": (96, 96, 48, 64),
    "env_notice_board": (64, 64, 32, 52),
    "env_barrel_crate": (64, 64, 32, 48),
    "env_house_shop": (128, 128, 64, 98),
    "env_house_terrace": (128, 128, 64, 98),
    "env_awning_stall": (96, 96, 48, 64),
    "env_market_stall": (96, 96, 48, 64),
    "env_crate_stack_tall": (64, 96, 32, 82),
    "env_forge_anvil": (64, 64, 32, 50),
    "env_chimney_stack": (64, 160, 32, 148),
    "env_guild_banner": (64, 128, 32, 116),
    "env_torch_brazier": (64, 64, 32, 54),
    "env_stained_arch": (128, 160, 64, 146),
    "env_temple_pillar": (64, 160, 32, 148),
    "env_prayer_candles": (64, 64, 32, 54),
    "env_lantern_string": (128, 64, 64, 20),
    "env_washing_line": (96, 64, 48, 24),
    "env_well_stone": (64, 64, 32, 50),
    "env_cargo_crane": (128, 192, 64, 178),
    "env_dock_piling": (64, 96, 32, 84),
    "env_fishing_net": (64, 64, 32, 48),
    "env_rowboat": (96, 64, 48, 52),
    "env_bellows_great": (128, 128, 64, 116),
    "env_bush": (64, 64, 32, 48),
    "env_fence_rail": (64, 64, 32, 50),
    # Optional / may be absent — checked at runtime
    "env_house_inn": (128, 144, 64, 130),
    "env_house_smithy": (128, 144, 64, 130),
    "env_house_guild": (128, 176, 64, 160),
    "env_house_temple": (128, 160, 64, 146),
    "env_house_row": (128, 128, 64, 98),
    "env_wall_curtain": (96, 128, 48, 116),
    "env_wall_corner": (96, 144, 48, 132),
    "env_gatehouse": (128, 160, 64, 148),
}

ANIMATED = {"env_torch_brazier"}

# NPC / spawn cells — keep ~2-tile clearance for clutter (landmarks may be adjacent).
NPC_CLEAR = [
    (0, 5),  # spawn
    (-15, 0),  # kafra (in front of consign house)
    (-14, 7),  # merchant (in front of potion stall)
    (17, -13),  # blacksmith
    (-15, -15),  # elder (in front of terrace)
    (-8, 15),  # tavern keeper (in front of Barnacle)
]


def asset_exists(ptype: str) -> bool:
    return (TILES_FF / f"{ptype}.png").is_file()


def prop(ptype: str, wx: int, wy: int, name: str | None = None) -> dict | None:
    if ptype not in PROP_META or not asset_exists(ptype):
        return None
    w, h, ax, ay = PROP_META[ptype]
    p: dict = {
        "type": ptype,
        "wx": wx,
        "wy": wy,
        "width": w,
        "height": h,
        "anchorX": ax,
        "anchorY": ay,
    }
    if name:
        p["name"] = name
    if ptype in ANIMATED:
        p["animated"] = True
    return p


def too_close(
    wx: int,
    wy: int,
    occupied: set[tuple[int, int]],
    radius: int,
    npc_radius: int,
) -> bool:
    if (wx, wy) in occupied:
        return True
    for ox, oy in occupied:
        if abs(wx - ox) <= radius and abs(wy - oy) <= radius:
            return True
    if npc_radius > 0:
        for nx, ny in NPC_CLEAR:
            if abs(wx - nx) <= npc_radius and abs(wy - ny) <= npc_radius:
                return True
    return False


def on_inner_ring(wx: int, wy: int) -> bool:
    """Plaza ring-road band only (keep readable; landmarks may override)."""
    if wx in (-10, -9, 9, 10) and -10 <= wy <= 10:
        return True
    if wy in (-10, -9, 9, 10) and -10 <= wx <= 10:
        return True
    return False


def add(
    props: list[dict],
    occupied: set[tuple[int, int]],
    ptype: str,
    wx: int,
    wy: int,
    name: str | None = None,
    *,
    radius: int = 1,
    npc_radius: int = 2,
    allow_ring: bool = False,
) -> bool:
    if not (-30 <= wx <= 30 and -30 <= wy <= 30):
        return False
    if not allow_ring and on_inner_ring(wx, wy):
        return False
    if too_close(wx, wy, occupied, radius=radius, npc_radius=npc_radius):
        return False
    p = prop(ptype, wx, wy, name)
    if not p:
        return False
    props.append(p)
    occupied.add((wx, wy))
    return True


def build_props() -> list[dict]:
    props: list[dict] = []
    occupied: set[tuple[int, int]] = set()

    # ----- Obelisk Plaza (keep center open) -----
    # Landmarks ignore NPC radius so fountain/obelisk keep authored coords.
    add(props, occupied, "env_obelisk_aetherite", 0, 0, "Aetherite Obelisk", radius=0, npc_radius=0, allow_ring=True)
    add(props, occupied, "env_fountain", 0, 3, "Grand Fountain", radius=1, npc_radius=0)
    add(props, occupied, "env_notice_board", 3, -2, "Herald's Post", radius=1, npc_radius=0)
    for xy in ((-6, -6), (6, -6), (-6, 6), (6, 4)):
        add(props, occupied, "env_torch_brazier", *xy, radius=1)
    for xy in ((-3, -3), (4, -4), (-4, 4)):
        add(props, occupied, "env_barrel_crate", *xy, radius=1)
    add(props, occupied, "env_bush", -7, 2, radius=1)
    add(props, occupied, "env_bush", 7, -3, radius=1)

    # ----- Kestrel Market (west) -----
    add(props, occupied, "env_house_shop", -18, 0, "Kestrel Consignment House", radius=1, npc_radius=0)
    add(props, occupied, "env_awning_stall", -14, 4, "Potion Row", radius=1, npc_radius=0)
    add(props, occupied, "env_awning_stall", -22, -3, "Auction Hall Stall", radius=1)
    add(props, occupied, "env_house_shop", -26, 4, "Traveller's Larder", radius=2)
    add(props, occupied, "env_house_inn", -26, -6, "Market Inn", radius=2)
    add(props, occupied, "env_house_shop", -22, 2, "General Goods", radius=2)
    add(props, occupied, "env_market_stall", -12, -4, "Spice Stall", radius=1)
    add(props, occupied, "env_market_stall", -12, 2, "Cloth Stall", radius=1)
    add(props, occupied, "env_awning_stall", -20, -6, "Trinket Awning", radius=1)
    add(props, occupied, "env_awning_stall", -28, 2, "Fishmonger Awning", radius=1)
    add(props, occupied, "env_market_stall", -16, 7, "Traveller Stall", radius=1)
    add(props, occupied, "env_crate_stack_tall", -16, -6, radius=1)
    add(props, occupied, "env_crate_stack_tall", -28, -2, radius=1)
    add(props, occupied, "env_crate_stack_tall", -22, 6, radius=1)
    for xy in ((-20, 3), (-15, -2), (-24, 7), (-28, 6), (-13, -7), (-19, 8)):
        add(props, occupied, "env_barrel_crate", *xy, radius=1)
    add(props, occupied, "env_torch_brazier", -12, -7, radius=1)
    add(props, occupied, "env_torch_brazier", -12, 7, radius=1)

    # ----- Ashen Ward (NE) -----
    add(props, occupied, "env_forge_anvil", 18, -14, "Obsidian Smithy", radius=1, npc_radius=0)
    add(props, occupied, "env_house_smithy", 24, -14, "Smithy Hall", radius=2)
    add(props, occupied, "env_house_shop", 28, -12, "Obsidian Forge Shop", radius=2)
    add(props, occupied, "env_chimney_stack", 22, -16, radius=1)
    add(props, occupied, "env_chimney_stack", 26, -18, radius=1)
    add(props, occupied, "env_chimney_stack", 14, -26, radius=1)
    add(props, occupied, "env_bellows_great", 20, -12, "Great Bellows", radius=1)
    add(props, occupied, "env_forge_anvil", 26, -14, radius=1)
    add(props, occupied, "env_guild_banner", 14, -20, "Vanguard Legion Hall", radius=1)
    add(props, occupied, "env_guild_banner", 20, -22, "Spellweaver Syndicate Spire", radius=1)
    add(props, occupied, "env_guild_banner", 26, -22, "Shadowblade Brotherhood", radius=1)
    add(props, occupied, "env_guild_banner", 12, -24, "Cleric Order Annex", radius=1)
    add(props, occupied, "env_guild_banner", 28, -26, "Ranger Corps Lodge", radius=1)
    add(props, occupied, "env_house_guild", 16, -28, "Guild Registry", radius=1)
    add(props, occupied, "env_house_shop", 20, -28, "Guild Registry Office", radius=1)
    add(props, occupied, "env_torch_brazier", 16, -18, radius=1)
    add(props, occupied, "env_torch_brazier", 24, -20, radius=1)
    add(props, occupied, "env_torch_brazier", 12, -16, radius=1)
    for xy in ((16, -12), (28, -16), (20, -28), (14, -28)):
        add(props, occupied, "env_barrel_crate", *xy, radius=1)
    add(props, occupied, "env_crate_stack_tall", 28, -12, radius=1)

    # ----- High Temple (east) -----
    add(props, occupied, "env_stained_arch", 18, 0, "High Temple Nave", radius=1, npc_radius=0)
    add(props, occupied, "env_house_temple", 24, 0, "Temple Cloister", radius=2)
    add(props, occupied, "env_temple_pillar", 14, 4, radius=1)
    add(props, occupied, "env_temple_pillar", 14, -4, radius=1)
    add(props, occupied, "env_temple_pillar", 22, 4, radius=1)
    add(props, occupied, "env_temple_pillar", 22, -4, radius=1)
    add(props, occupied, "env_temple_pillar", 18, 6, radius=1)
    add(props, occupied, "env_temple_pillar", 18, -6, radius=1)
    add(props, occupied, "env_prayer_candles", 20, 2, radius=1)
    add(props, occupied, "env_prayer_candles", 20, -2, radius=1)
    add(props, occupied, "env_prayer_candles", 16, 2, radius=1)
    add(props, occupied, "env_prayer_candles", 26, 3, radius=1)
    add(props, occupied, "env_torch_brazier", 12, 3, radius=1)
    add(props, occupied, "env_torch_brazier", 12, -3, radius=1)
    for xy in ((24, 6), (26, 4), (28, 6), (24, -6), (26, -5), (28, -7), (22, 7)):
        add(props, occupied, "env_bush", *xy, radius=1)
    add(props, occupied, "env_notice_board", 16, -7, "Ossuary Steps Notice", radius=1)

    # ----- Lantern Rows (NW) -----
    add(props, occupied, "env_house_terrace", -18, -18, "Elder's House", radius=1, npc_radius=0)
    add(props, occupied, "env_house_row", -24, -18, "Row House A", radius=2)
    add(props, occupied, "env_house_terrace", -24, -18, "Terrace Row West", radius=2)
    add(props, occupied, "env_house_terrace", -18, -24, "Terrace Row North", radius=2)
    add(props, occupied, "env_house_terrace", -26, -24, "Rooftop Walk House", radius=2)
    add(props, occupied, "env_house_terrace", -22, -20, "Lamplighter Cottage", radius=2)
    add(props, occupied, "env_house_terrace", -28, -16, "Quiet Terrace", radius=2)
    add(props, occupied, "env_house_terrace", -22, -28, "North Row End", radius=2)
    add(props, occupied, "env_lantern_string", -14, -22, radius=1)
    add(props, occupied, "env_lantern_string", -20, -26, radius=1)
    add(props, occupied, "env_lantern_string", -26, -20, radius=1)
    add(props, occupied, "env_lantern_string", -16, -28, radius=1)
    add(props, occupied, "env_washing_line", -22, -14, radius=1)
    add(props, occupied, "env_washing_line", -24, -22, radius=1)
    add(props, occupied, "env_washing_line", -28, -28, radius=1)
    add(props, occupied, "env_well_stone", -20, -20, "Lamplighter's Yard", radius=1)
    add(props, occupied, "env_well_stone", -14, -28, radius=1)
    add(props, occupied, "env_torch_brazier", -12, -14, radius=1)
    add(props, occupied, "env_torch_brazier", -28, -22, radius=1)
    for xy in ((-16, -20), (-26, -28), (-12, -26), (-28, -12)):
        add(props, occupied, "env_bush", *xy, radius=1)
    add(props, occupied, "env_fence_rail", -12, -18, radius=1)
    add(props, occupied, "env_fence_rail", -12, -22, radius=1)

    # ----- Wetstone Docks (south) -----
    add(props, occupied, "env_house_shop", -8, 18, "The Barnacle Tavern", radius=1, npc_radius=0)
    add(props, occupied, "env_house_shop", 10, 16, "Chandler's Shop", radius=2)
    add(props, occupied, "env_house_inn", -16, 16, "Dockside Inn", radius=2)
    add(props, occupied, "env_cargo_crane", 0, 22, radius=1, npc_radius=0)
    add(props, occupied, "env_cargo_crane", -14, 24, radius=1)
    add(props, occupied, "env_dock_piling", -6, 26, radius=1)
    add(props, occupied, "env_dock_piling", 6, 26, radius=1)
    add(props, occupied, "env_dock_piling", -12, 28, radius=1)
    add(props, occupied, "env_dock_piling", 12, 28, radius=1)
    add(props, occupied, "env_dock_piling", -18, 26, radius=1)
    add(props, occupied, "env_dock_piling", 18, 26, radius=1)
    add(props, occupied, "env_dock_piling", 0, 28, radius=1)
    add(props, occupied, "env_fishing_net", -3, 20, radius=1)
    add(props, occupied, "env_fishing_net", 3, 20, radius=1)
    add(props, occupied, "env_fishing_net", -8, 24, radius=1)
    add(props, occupied, "env_fishing_net", 14, 22, radius=1)
    add(props, occupied, "env_rowboat", 4, 24, "Ferry Berth", radius=1)
    add(props, occupied, "env_rowboat", -4, 28, radius=1)
    add(props, occupied, "env_rowboat", 8, 26, radius=1)
    for xy in ((-2, 16), (6, 18), (-12, 20), (16, 20), (-20, 22), (20, 18), (2, 14)):
        add(props, occupied, "env_barrel_crate", *xy, radius=1)
    add(props, occupied, "env_crate_stack_tall", -18, 18, radius=1)
    add(props, occupied, "env_crate_stack_tall", 16, 16, radius=1)
    add(props, occupied, "env_torch_brazier", -4, 14, radius=1)
    add(props, occupied, "env_torch_brazier", 4, 14, radius=1)
    add(props, occupied, "env_torch_brazier", -20, 16, radius=1)

    # ----- Outer wall accents (only if assets exist) -----
    for wx, wy, name in (
        (0, -30, "Rampart Gatehouse"),
        (0, 30, "Dockgate Gatehouse"),
        (-30, 0, "Ashroad Gatehouse"),
        (30, 0, "Rimewind Gatehouse"),
    ):
        add(props, occupied, "env_gatehouse", wx, wy, name, radius=1, npc_radius=0, allow_ring=True)

    for wx, wy in ((-30, -30), (30, -30), (-30, 30), (30, 30)):
        add(props, occupied, "env_wall_corner", wx, wy, radius=1, npc_radius=0, allow_ring=True)

    # Sparse curtains so total envStructures stays ~80–150.
    for x in (-25, -13, 13, 25):
        add(props, occupied, "env_wall_curtain", x, -30, radius=1, npc_radius=0, allow_ring=True)
        add(props, occupied, "env_wall_curtain", x, 30, radius=1, npc_radius=0, allow_ring=True)
    for y in (-25, -13, 13, 25):
        add(props, occupied, "env_wall_curtain", -30, y, radius=1, npc_radius=0, allow_ring=True)
        add(props, occupied, "env_wall_curtain", 30, y, radius=1, npc_radius=0, allow_ring=True)

    return props


def main() -> None:
    data = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    before = len(data.get("envStructures", []))
    before_types = Counter(p["type"] for p in data.get("envStructures", []))

    props = build_props()
    data["envStructures"] = props

    # Keep NPCs standing in front of landmark buildings (outside collision radii).
    npc_fronts = {
        "kafra_kestrel": (-15, 0),
        "merchant_potionrow": (-14, 7),
        "elder_lantern": (-15, -15),
        "tavern_barnacle": (-8, 15),
    }
    for n in data.get("npcs", []):
        if n.get("id") in npc_fronts:
            n["wx"], n["wy"] = npc_fronts[n["id"]]

    # Preserve schema / topology keys already present.
    assert data["id"] == "aethelgard"
    assert data["defaultTile"] == "tile_town_cobble"
    assert data["combatDisabled"] is True
    assert data["bounds"] == {"minWx": -31, "maxWx": 31, "minWy": -31, "maxWy": 31}
    assert len(data["exits"]) == 4
    assert len(data["subRegions"]) == 6
    assert data["spawn"] == {"wx": 0, "wy": 5}

    MAP_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    after_types = Counter(p["type"] for p in props)
    print(f"envStructures: {before} -> {len(props)}")
    print("before types:", dict(sorted(before_types.items())))
    print("after types:", dict(sorted(after_types.items())))
    print("exits:", [e["id"] for e in data["exits"]])
    print("subRegions:", [s["id"] for s in data["subRegions"]])
    print("npcs:", [(n["id"], n["wx"], n["wy"]) for n in data["npcs"]])
    missing = [t for t in PROP_META if not asset_exists(t)]
    if missing:
        print("skipped missing assets:", missing)


if __name__ == "__main__":
    main()
