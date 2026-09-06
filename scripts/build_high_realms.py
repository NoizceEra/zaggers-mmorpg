#!/usr/bin/env python3
"""Build Obsidian Spire, Glacial Chasm, and Umbral Rootways to meadows/sanctum quality.

Regenerates web/maps/{spire,chasm,rootways}.json with distinct sub-region tiles,
Phase 3 bestiary sprites, ~18-25 monster spawns each, props, and correct exits.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / "web" / "maps"
SPRITES = ROOT / "web" / "assets" / "sprites_ff"

MIN_W, MAX_W = -31, 31
MIN_H, MAX_H = -31, 31


def hp(level: int, rank: str = "normal") -> int:
    mult = {"normal": 1.0, "elite": 2.5, "rare": 3.5, "boss": 12.0}[rank]
    return int(round(14.0 * (level ** 1.05) * mult))


def fill_rect(tiles: dict, x0, x1, y0, y1, tile: str):
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            if MIN_W <= x <= MAX_W and MIN_H <= y <= MAX_H:
                tiles[f"{x},{y}"] = tile


def sprinkle(tiles: dict, x0, x1, y0, y1, tile: str, every: int, offset: int = 0):
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            if MIN_W <= x <= MAX_W and MIN_H <= y <= MAX_H:
                if (abs(x) * 3 + abs(y) * 5 + offset) % every == 0:
                    tiles[f"{x},{y}"] = tile


def path_ns(tiles: dict, x: int, y0: int, y1: int, tile: str, half_w: int = 1):
    for y in range(min(y0, y1), max(y0, y1) + 1):
        for dx in range(-half_w, half_w + 1):
            wx = x + dx
            if MIN_W <= wx <= MAX_W and MIN_H <= y <= MAX_H:
                tiles[f"{wx},{y}"] = tile


def path_ew(tiles: dict, y: int, x0: int, x1: int, tile: str, half_h: int = 1):
    for x in range(min(x0, x1), max(x0, x1) + 1):
        for dy in range(-half_h, half_h + 1):
            wy = y + dy
            if MIN_W <= x <= MAX_W and MIN_H <= wy <= MAX_H:
                tiles[f"{x},{wy}"] = tile


def prop(ptype, wx, wy, w, h, ax, ay, name=None, animated=False):
    p = {
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
    if animated:
        p["animated"] = True
    return p


def mon(mid, name, sprite, level, wx, wy, *, rank="normal", speed=0.03, aggro=True):
    h = hp(level, rank)
    m = {
        "id": mid,
        "name": name,
        "sprite": sprite,
        "hp": h,
        "maxHp": h,
        "speed": speed,
        "isAggro": aggro,
        "wx": wx,
        "wy": wy,
    }
    if rank != "normal":
        m["rank"] = rank
    return m


# ---------------------------------------------------------------------------
# SPIRE
# ---------------------------------------------------------------------------

def build_spire():
    tiles = {}
    # Defaults + sub-region paints
    fill_rect(tiles, MIN_W, MAX_W, MIN_H, MAX_H, "tile_dungeon_obsidian")
    # Cinderfall Approach (entry south)
    fill_rect(tiles, MIN_W, MAX_W, -31, -16, "tile_spire_ash")
    sprinkle(tiles, MIN_W, MAX_W, -31, -16, "tile_dungeon_lava", 11, 1)
    path_ns(tiles, 0, -31, -16, "tile_spire_basalt", 2)
    # Emberglass Terraces (west mid)
    fill_rect(tiles, -31, -8, -15, 5, "tile_spire_emberglass")
    sprinkle(tiles, -31, -8, -15, 5, "tile_dungeon_obsidian", 7, 2)
    # Ashfall Overlook (east mid, vista)
    fill_rect(tiles, 10, 31, -15, 5, "tile_spire_basalt")
    sprinkle(tiles, 10, 31, -15, 5, "tile_spire_ash", 9, 3)
    # Central corridor mid-band
    fill_rect(tiles, -7, 9, -15, 5, "tile_dungeon_obsidian")
    path_ns(tiles, 0, -15, 5, "tile_spire_basalt", 2)
    sprinkle(tiles, -7, 9, -15, 5, "tile_dungeon_lava", 13, 4)
    # The Slagworks
    fill_rect(tiles, MIN_W, MAX_W, 6, 16, "tile_dungeon_obsidian")
    sprinkle(tiles, MIN_W, MAX_W, 6, 16, "tile_dungeon_lava", 6, 5)
    path_ns(tiles, 0, 6, 16, "tile_spire_basalt", 2)
    # Collapsed Skybridge
    fill_rect(tiles, MIN_W, MAX_W, 17, 22, "tile_spire_basalt")
    sprinkle(tiles, MIN_W, MAX_W, 17, 22, "tile_dungeon_lava", 5, 6)
    # pillar stepping stones across caldera gap
    for x in (-10, -5, 0, 5, 10):
        fill_rect(tiles, x - 1, x + 1, 18, 21, "tile_spire_basalt")
    fill_rect(tiles, -2, 2, 17, 22, "tile_dungeon_lava")
    for x in (-8, -3, 3, 8):
        fill_rect(tiles, x, x, 19, 20, "tile_spire_basalt")
    # Spire Crown
    fill_rect(tiles, -16, 16, 23, 31, "tile_dungeon_obsidian")
    sprinkle(tiles, -16, 16, 23, 31, "tile_dungeon_lava", 8, 7)
    fill_rect(tiles, -4, 4, 24, 30, "tile_spire_basalt")

    env = [
        prop("env_crystal", 0, -26, 64, 96, 32, 82, "Cinderfall Save Crystal"),
        prop("env_torch_brazier", -5, -24, 64, 64, 32, 54, animated=True),
        prop("env_torch_brazier", 5, -24, 64, 64, 32, 54, animated=True),
        prop("env_lava_channel", -8, -22, 64, 64, 32, 40, animated=True),
        prop("env_lava_channel", 8, -20, 64, 64, 32, 40, animated=True),
        prop("env_lava_channel", -12, -18, 64, 64, 32, 40, animated=True),
        prop("env_barrel_crate", -4, -27, 64, 64, 32, 48, "Caravan Supplies"),
        # Emberglass gathering cluster
        prop("env_rock", -22, -8, 64, 64, 32, 48, "Emberglass Node Cluster"),
        prop("env_rock", -18, -4, 64, 64, 32, 48),
        prop("env_rock", -26, 0, 64, 64, 32, 48),
        prop("env_rock", -20, 3, 64, 64, 32, 48),
        prop("env_torch_brazier", -14, -10, 64, 64, 32, 54, animated=True),
        # Ashfall Overlook vista camp
        prop("env_campfire", 22, -6, 64, 64, 32, 52, "Windbreak Camp", animated=True),
        prop("env_cairn_waypoint", 26, -10, 64, 96, 32, 84, "Ashfall Vista Marker"),
        prop("env_rock", 18, -2, 64, 64, 32, 48),
        # Slagworks foundry
        prop("env_forge_anvil", -10, 10, 64, 64, 32, 50, "Slagworks Anvil"),
        prop("env_bellows_great", 8, 12, 128, 128, 64, 116, "Great Bellows"),
        prop("env_chimney_stack", -14, 8, 64, 160, 32, 148),
        prop("env_chimney_stack", 14, 8, 64, 160, 32, 148),
        prop("env_lava_channel", -4, 12, 64, 64, 32, 40, animated=True),
        prop("env_lava_channel", 4, 14, 64, 64, 32, 40, animated=True),
        prop("env_torch_brazier", -8, 14, 64, 64, 32, 54, animated=True),
        prop("env_torch_brazier", 8, 14, 64, 64, 32, 54, animated=True),
        prop("env_barrel_crate", -6, 9, 64, 64, 32, 48),
        # Skybridge pillars / vault door to rootways
        prop("env_dungeon_pillar", -8, 19, 64, 128, 32, 116, "Skybridge Pillar"),
        prop("env_dungeon_pillar", -3, 20, 64, 128, 32, 116),
        prop("env_dungeon_pillar", 3, 20, 64, 128, 32, 116),
        prop("env_dungeon_pillar", 8, 19, 64, 128, 32, 116),
        prop("env_vault_door", -26, 20, 128, 160, 64, 148, "Skybridge Gate → Rootways"),
        prop("env_torch_brazier", -22, 19, 64, 64, 32, 54, animated=True),
        # Spire Crown
        prop("env_dungeon_pillar", -8, 26, 64, 128, 32, 116),
        prop("env_dungeon_pillar", 8, 26, 64, 128, 32, 116),
        prop("env_torch_brazier", -5, 28, 64, 64, 32, 54, animated=True),
        prop("env_torch_brazier", 5, 28, 64, 64, 32, 54, animated=True),
        prop("env_crystal", 0, 25, 64, 96, 32, 82, "Spire Crown Altar"),
    ]

    npcs = [
        {
            "id": "caravan_vendor",
            "name": "[NPC] Caravan Quartermaster",
            "title": "Cinderfall Merchant",
            "wx": -4,
            "wy": -27,
            "dir": 0,
            "frame": 1,
            "sprite": "npc_merchant",
            "dialogHeader": "Caravan Quartermaster",
            "dialogText": "Ash falls heavy up here on the Spire! Restock potions and fire-resist elixirs before the Slagworks.",
            "options": [
                {"text": "🧪 Open Caravan Supplies", "action": "open_shop"},
                {"text": "❌ Cancel", "action": "close"},
            ],
        }
    ]

    monsters = [
        # Cinderfall Approach
        mon("spire_cinderpuff_1", "Cinderpuff", "cinderpuff_ff", 32, -8, -22, speed=0.028, aggro=True),
        mon("spire_cinderpuff_2", "Cinderpuff", "cinderpuff_ff", 32, 10, -20, speed=0.028, aggro=True),
        mon("spire_cinderpuff_3", "Cinderpuff", "cinderpuff_ff", 33, -12, -17, speed=0.028, aggro=True),
        mon("spire_shard_1", "Emberglass Shard", "emberglass_shard_ff", 34, 6, -18, speed=0.02, aggro=False),
        # Emberglass Terraces
        mon("spire_shard_2", "Emberglass Shard", "emberglass_shard_ff", 35, -20, -10, speed=0.02, aggro=False),
        mon("spire_shard_3", "Emberglass Shard", "emberglass_shard_ff", 36, -24, -2, speed=0.02, aggro=False),
        mon("spire_harrier_1", "Ashfall Harrier", "ashfall_harrier_ff", 37, -16, 2, speed=0.04, aggro=True),
        mon("spire_harrier_2", "Ashfall Harrier", "ashfall_harrier_ff", 38, -28, -6, speed=0.04, aggro=True),
        # Slagworks
        mon("spire_hulk_1", "Magma Hulk", "magma_hulk_ff", 42, -14, 10, speed=0.022, aggro=True),
        mon("spire_hulk_2", "Magma Hulk", "magma_hulk_ff", 43, 12, 12, speed=0.022, aggro=True),
        mon("spire_soot_1", "Soot Revenant", "soot_revenant_ff", 43, -6, 8, speed=0.03, aggro=True),
        mon("spire_soot_2", "Soot Revenant", "soot_revenant_ff", 44, 6, 15, speed=0.03, aggro=True),
        mon("spire_sentinel_1", "Forgewrought Sentinel", "forgewrought_sentinel_ff", 45, -10, 14, speed=0.026, aggro=True),
        mon("spire_sentinel_2", "Forgewrought Sentinel", "forgewrought_sentinel_ff", 46, 10, 9, speed=0.026, aggro=True),
        mon(
            "spire_bellowmaster",
            "Bellowmaster Grukk",
            "bellowmaster_grukk_ff",
            49,
            6,
            12,
            rank="elite",
            speed=0.038,
        ),
        # Collapsed Skybridge
        mon("spire_harrier_3", "Ashfall Harrier", "ashfall_harrier_ff", 40, -12, 18, speed=0.04, aggro=True),
        mon("spire_imp_1", "Pyrelash Imp", "pyrelash_imp_ff", 47, 10, 20, speed=0.042, aggro=True),
        mon("spire_imp_2", "Pyrelash Imp", "pyrelash_imp_ff", 48, -6, 21, speed=0.042, aggro=True),
        # Spire Crown
        mon("spire_imp_3", "Pyrelash Imp", "pyrelash_imp_ff", 49, -8, 26, speed=0.042, aggro=True),
        mon(
            "spire_unquenched",
            "The Unquenched",
            "the_unquenched_ff",
            50,
            8,
            27,
            rank="rare",
            speed=0.036,
        ),
        mon(
            "spire_boss_vashkar",
            "Vashkar the Spire Crown",
            "vashkar_spire_crown_ff",
            52,
            0,
            29,
            rank="boss",
            speed=0.045,
        ),
    ]

    sub_regions = [
        {
            "id": "cinderfall_approach",
            "name": "Cinderfall Approach",
            "type": "field",
            "minLv": 30,
            "maxLv": 36,
            "minWx": -31,
            "maxWx": 31,
            "minWy": -31,
            "maxWy": -16,
        },
        {
            "id": "emberglass_terraces",
            "name": "Emberglass Terraces",
            "type": "field",
            "minLv": 33,
            "maxLv": 40,
            "minWx": -31,
            "maxWx": -8,
            "minWy": -15,
            "maxWy": 5,
        },
        {
            "id": "ashfall_overlook",
            "name": "Ashfall Overlook",
            "type": "vista",
            "minLv": 30,
            "maxLv": 52,
            "minWx": 10,
            "maxWx": 31,
            "minWy": -15,
            "maxWy": 5,
        },
        {
            "id": "the_slagworks",
            "name": "The Slagworks",
            "type": "field",
            "minLv": 36,
            "maxLv": 45,
            "minWx": -31,
            "maxWx": 31,
            "minWy": 6,
            "maxWy": 16,
        },
        {
            "id": "collapsed_skybridge",
            "name": "Collapsed Skybridge",
            "type": "shortcut",
            "minLv": 45,
            "maxLv": 52,
            "minWx": -31,
            "maxWx": 31,
            "minWy": 17,
            "maxWy": 22,
        },
        {
            "id": "the_spire_crown",
            "name": "The Spire Crown",
            "type": "boss",
            "minLv": 48,
            "maxLv": 52,
            "minWx": -16,
            "maxWx": 16,
            "minWy": 23,
            "maxWy": 31,
        },
    ]

    exits = [
        {
            "id": "to_aethelgard",
            "wx": 0,
            "wy": -31,
            "radius": 2.0,
            "targetMap": "aethelgard",
            "targetWx": -26,
            "targetWy": 0,
            "label": "Ashroad Caravan → Aethelgard",
        },
        {
            "id": "to_rootways",
            "wx": -26,
            "wy": 20,
            "radius": 2.0,
            "targetMap": "rootways",
            "targetWx": -20,
            "targetWy": -28,
            "label": "Collapsed Skybridge → Umbral Rootways",
            "minLevel": 45,
        },
    ]

    return {
        "id": "spire",
        "name": "Obsidian Spire",
        "gridWidth": 64,
        "gridHeight": 64,
        "bounds": {"minWx": MIN_W, "maxWx": MAX_W, "minWy": MIN_H, "maxWy": MAX_H},
        "defaultTile": "tile_dungeon_obsidian",
        "light": "#ffebee",
        "minLv": 30,
        "maxLv": 52,
        "boss": "vashkar_spire_crown",
        "spawn": {"wx": 0, "wy": -28},
        "tiles": tiles,
        "envStructures": env,
        "npcs": npcs,
        "monsters": monsters,
        "subRegions": sub_regions,
        "exits": exits,
    }


# ---------------------------------------------------------------------------
# CHASM
# ---------------------------------------------------------------------------

def build_chasm():
    tiles = {}
    fill_rect(tiles, MIN_W, MAX_W, MIN_H, MAX_H, "tile_dungeon_slate")
    # Rimewind Pass
    fill_rect(tiles, MIN_W, MAX_W, -31, -16, "tile_ice_packed")
    sprinkle(tiles, MIN_W, MAX_W, -31, -16, "tile_ice_crevasse", 12, 1)
    path_ns(tiles, 0, -31, -16, "tile_ice_blue", 2)
    # Statuary of the Fallen (west)
    fill_rect(tiles, -31, -6, -15, 5, "tile_ice_mirror")
    sprinkle(tiles, -31, -6, -15, 5, "tile_ice_packed", 8, 2)
    # Crevasse Undershelf (south-east pocket)
    fill_rect(tiles, 8, 31, -15, -2, "tile_ice_crevasse")
    sprinkle(tiles, 8, 31, -15, -2, "tile_ice_blue", 6, 3)
    # Aurora Shelf (east vista, higher)
    fill_rect(tiles, 8, 31, -1, 5, "tile_ice_blue")
    sprinkle(tiles, 8, 31, -1, 5, "tile_ice_mirror", 9, 4)
    # Central corridor
    fill_rect(tiles, -5, 7, -15, 5, "tile_dungeon_slate")
    path_ns(tiles, 0, -15, 5, "tile_ice_packed", 2)
    # Hoarfrost Vault (hidden)
    fill_rect(tiles, -20, 20, 6, 16, "tile_ice_mirror")
    sprinkle(tiles, -20, 20, 6, 16, "tile_dungeon_slate", 7, 5)
    fill_rect(tiles, -4, 4, 6, 16, "tile_ice_blue")
    # Thronehall of Ice
    fill_rect(tiles, -16, 16, 17, 31, "tile_ice_mirror")
    sprinkle(tiles, -16, 16, 17, 31, "tile_ice_blue", 5, 6)
    fill_rect(tiles, -5, 5, 22, 30, "tile_ice_mirror")

    env = [
        prop("env_crystal", 0, -26, 64, 96, 32, 82, "Rimewind Save Crystal"),
        prop("env_cairn_waypoint", -6, -24, 64, 96, 32, 84),
        prop("env_cairn_waypoint", 6, -22, 64, 96, 32, 84),
        prop("env_cairn_waypoint", -4, -18, 64, 96, 32, 84),
        prop("env_guide_rope", -3, -24, 96, 64, 48, 30, "Guide Rope"),
        prop("env_guide_rope", 2, -20, 96, 64, 48, 30),
        prop("env_guide_rope", -2, -17, 96, 64, 48, 30),
        # Statuary
        prop("env_ice_statue", -22, -10, 64, 128, 32, 116, "Fallen Hero"),
        prop("env_ice_statue", -18, -6, 64, 128, 32, 116),
        prop("env_ice_statue", -26, -2, 64, 128, 32, 116),
        prop("env_ice_statue", -14, 2, 64, 128, 32, 116),
        prop("env_ice_statue", -20, 4, 64, 128, 32, 116),
        prop("env_ice_colossus_shell", -24, 0, 128, 192, 64, 178, "Colossus Shell"),
        # Crevasse Undershelf smuggler camp
        prop("env_barrel_crate", 18, -10, 64, 64, 32, 48, "Smuggler's Cache"),
        prop("env_campfire", 22, -8, 64, 64, 32, 52, animated=True),
        prop("env_crate_stack_tall", 20, -12, 64, 96, 32, 82),
        prop("env_torch_brazier", 16, -6, 64, 64, 32, 54, animated=True),
        # Aurora Shelf
        prop("env_cairn_waypoint", 24, 2, 64, 96, 32, 84, "Aurora Vista Marker"),
        prop("env_campfire", 20, 0, 64, 64, 32, 52, "Aurora Rest", animated=True),
        prop("env_crystal", 26, 4, 64, 96, 32, 82, "Aurora Ice"),
        # Hoarfrost Vault
        prop("env_vault_door", 0, 8, 128, 160, 64, 148, "Hoarfrost Vault Door"),
        prop("env_reliquary_casket", -6, 12, 64, 64, 32, 52),
        prop("env_reliquary_casket", 6, 14, 64, 64, 32, 52),
        prop("env_dungeon_pillar", -10, 10, 64, 128, 32, 116),
        prop("env_dungeon_pillar", 10, 10, 64, 128, 32, 116),
        # Thronehall
        prop("env_dungeon_pillar", -8, 24, 64, 128, 32, 116),
        prop("env_dungeon_pillar", 8, 24, 64, 128, 32, 116),
        prop("env_crystal", 0, 22, 64, 96, 32, 82, "Throne Crystal"),
        prop("env_ice_statue", -10, 26, 64, 128, 32, 116),
        prop("env_ice_statue", 10, 26, 64, 128, 32, 116),
        prop("env_vault_door", 0, 30, 128, 160, 64, 148, "Thronehall Gate → Rootways"),
    ]

    npcs = [
        {
            "id": "rimewind_merchant",
            "name": "[NPC] Rimewind Merchant",
            "title": "Glacial Trader",
            "wx": -3,
            "wy": -27,
            "dir": 0,
            "frame": 1,
            "sprite": "npc_merchant",
            "dialogHeader": "Rimewind Merchant",
            "dialogText": "Brr! Stock cold-resist gear before the Statuary. The Undershelf smugglers sell what I won't.",
            "options": [
                {"text": "🧪 Open Glacial Gear Shop", "action": "open_shop"},
                {"text": "❌ Cancel", "action": "close"},
            ],
        },
        {
            "id": "crevasse_smuggler",
            "name": "[NPC] Ice-Runner",
            "title": "Crevasse Smuggler",
            "wx": 20,
            "wy": -9,
            "dir": 0,
            "frame": 1,
            "sprite": "npc_merchant",
            "dialogHeader": "Ice-Runner",
            "dialogText": "Tram never comes this deep. I move what the Rimewind won't — cold-resist, thawstones, quiet exits.",
            "options": [
                {"text": "🧪 Browse Smuggler Wares", "action": "open_shop"},
                {"text": "❌ Cancel", "action": "close"},
            ],
        },
    ]

    monsters = [
        # Rimewind Pass
        mon("chasm_sprite_1", "Rimewind Sprite", "rimewind_sprite_ff", 52, -8, -22, speed=0.034, aggro=True),
        mon("chasm_sprite_2", "Rimewind Sprite", "rimewind_sprite_ff", 53, 10, -20, speed=0.034, aggro=True),
        mon("chasm_stalker_1", "Hoarfrost Stalker", "hoarfrost_stalker_ff", 54, -12, -17, speed=0.036, aggro=True),
        mon("chasm_stalker_2", "Hoarfrost Stalker", "hoarfrost_stalker_ff", 55, 6, -18, speed=0.036, aggro=True),
        # Statuary
        mon("chasm_penitent_1", "Frozen Penitent", "frozen_penitent_ff", 56, -20, -10, speed=0.024, aggro=True),
        mon("chasm_penitent_2", "Frozen Penitent", "frozen_penitent_ff", 57, -16, -2, speed=0.024, aggro=True),
        mon("chasm_penitent_3", "Frozen Penitent", "frozen_penitent_ff", 58, -24, 2, speed=0.024, aggro=True),
        mon("chasm_shade_1", "Snowveil Shade", "snowveil_shade_ff", 60, -18, 4, speed=0.032, aggro=True),
        mon("chasm_shade_2", "Snowveil Shade", "snowveil_shade_ff", 61, -12, -6, speed=0.032, aggro=True),
        mon(
            "chasm_colossus",
            "Statuary Colossus",
            "statuary_colossus_ff",
            69,
            -22,
            0,
            rank="elite",
            speed=0.028,
        ),
        # Crevasse Undershelf
        mon("chasm_stalker_3", "Hoarfrost Stalker", "hoarfrost_stalker_ff", 56, 14, -12, speed=0.036, aggro=True),
        mon("chasm_drake_1", "Glacier Drake Whelp", "glacier_drake_whelp_ff", 58, 24, -10, speed=0.038, aggro=True),
        mon("chasm_drake_2", "Glacier Drake Whelp", "glacier_drake_whelp_ff", 59, 18, -4, speed=0.038, aggro=True),
        # Aurora Shelf ambience (passive until higher level — keep passive)
        mon("chasm_seraphon_1", "Aurora Seraphon", "aurora_seraphon_ff", 65, 22, 2, speed=0.02, aggro=False),
        # Hoarfrost Vault
        mon("chasm_lich_1", "Permafrost Lich", "permafrost_lich_ff", 66, -8, 12, speed=0.028, aggro=True),
        mon("chasm_lich_2", "Permafrost Lich", "permafrost_lich_ff", 67, 8, 14, speed=0.028, aggro=True),
        mon(
            "chasm_vault_keeper",
            "The Vault Keeper",
            "the_vault_keeper_ff",
            70,
            0,
            12,
            rank="rare",
            speed=0.036,
        ),
        # Thronehall
        mon("chasm_seraphon_2", "Aurora Seraphon", "aurora_seraphon_ff", 66, -6, 22, speed=0.03, aggro=True),
        mon("chasm_lich_3", "Permafrost Lich", "permafrost_lich_ff", 68, 8, 24, speed=0.028, aggro=True),
        mon(
            "chasm_boss_sylveth",
            "Sylveth, Queen of the Silent Thaw",
            "sylveth_silent_thaw_ff",
            72,
            0,
            28,
            rank="boss",
            speed=0.045,
        ),
    ]

    sub_regions = [
        {
            "id": "rimewind_pass",
            "name": "Rimewind Pass",
            "type": "field",
            "minLv": 50,
            "maxLv": 56,
            "minWx": -31,
            "maxWx": 31,
            "minWy": -31,
            "maxWy": -16,
        },
        {
            "id": "statuary_of_the_fallen",
            "name": "Statuary of the Fallen",
            "type": "field",
            "minLv": 54,
            "maxLv": 62,
            "minWx": -31,
            "maxWx": -6,
            "minWy": -15,
            "maxWy": 5,
        },
        {
            "id": "crevasse_undershelf",
            "name": "Crevasse Undershelf",
            "type": "cave",
            "minLv": 56,
            "maxLv": 63,
            "minWx": 8,
            "maxWx": 31,
            "minWy": -15,
            "maxWy": -2,
        },
        {
            "id": "aurora_shelf",
            "name": "Aurora Shelf",
            "type": "vista",
            "minLv": 50,
            "maxLv": 72,
            "minWx": 8,
            "maxWx": 31,
            "minWy": -1,
            "maxWy": 5,
        },
        {
            "id": "hoarfrost_vault",
            "name": "Hoarfrost Vault",
            "type": "hidden",
            "minLv": 60,
            "maxLv": 68,
            "minWx": -20,
            "maxWx": 20,
            "minWy": 6,
            "maxWy": 16,
        },
        {
            "id": "thronehall_of_ice",
            "name": "Thronehall of Ice",
            "type": "boss",
            "minLv": 66,
            "maxLv": 72,
            "minWx": -16,
            "maxWx": 16,
            "minWy": 17,
            "maxWy": 31,
        },
    ]

    exits = [
        {
            "id": "to_aethelgard",
            "wx": 0,
            "wy": -31,
            "radius": 2.0,
            "targetMap": "aethelgard",
            "targetWx": 26,
            "targetWy": 0,
            "label": "Rimewind Tramway → Aethelgard",
        },
        {
            "id": "to_rootways",
            "wx": 0,
            "wy": 30,
            "radius": 2.0,
            "targetMap": "rootways",
            "targetWx": 20,
            "targetWy": -28,
            "label": "Thronehall Gate → Umbral Rootways",
            "minLevel": 66,
        },
    ]

    return {
        "id": "chasm",
        "name": "Glacial Chasm",
        "gridWidth": 64,
        "gridHeight": 64,
        "bounds": {"minWx": MIN_W, "maxWx": MAX_W, "minWy": MIN_H, "maxWy": MAX_H},
        "defaultTile": "tile_dungeon_slate",
        "light": "#e8eaf6",
        "minLv": 50,
        "maxLv": 72,
        "boss": "sylveth_silent_thaw",
        "spawn": {"wx": 0, "wy": -28},
        "tiles": tiles,
        "envStructures": env,
        "npcs": npcs,
        "monsters": monsters,
        "subRegions": sub_regions,
        "exits": exits,
    }


# ---------------------------------------------------------------------------
# ROOTWAYS
# ---------------------------------------------------------------------------

def build_rootways():
    tiles = {}
    fill_rect(tiles, MIN_W, MAX_W, MIN_H, MAX_H, "tile_root_bark")
    # Nethergate Descent
    fill_rect(tiles, MIN_W, MAX_W, -31, -16, "tile_dungeon_obsidian")
    sprinkle(tiles, MIN_W, MAX_W, -31, -16, "tile_dungeon_rune", 8, 1)
    path_ns(tiles, 0, -31, -16, "tile_root_bark", 2)
    fill_rect(tiles, -24, -16, -31, -24, "tile_spire_basalt")  # spire approach pocket
    fill_rect(tiles, 16, 24, -31, -24, "tile_ice_packed")  # chasm approach pocket
    # Bonemeal Hollows
    fill_rect(tiles, MIN_W, MAX_W, -15, 4, "tile_root_bonemeal")
    sprinkle(tiles, MIN_W, MAX_W, -15, 4, "tile_root_bark", 7, 2)
    path_ns(tiles, 0, -15, 4, "tile_dungeon_rune", 2)
    # Weeping Boughs (west)
    fill_rect(tiles, -31, -6, 5, 16, "tile_root_sap")
    sprinkle(tiles, -31, -6, 5, 16, "tile_root_bark", 6, 3)
    # Sanguine Terrace (hidden west pocket)
    fill_rect(tiles, -31, -14, 17, 24, "tile_root_terrace")
    sprinkle(tiles, -31, -14, 17, 24, "tile_root_sap", 9, 4)
    # Thorncradle Vault (east elite)
    fill_rect(tiles, 8, 31, 5, 20, "tile_root_bark")
    sprinkle(tiles, 8, 31, 5, 20, "tile_dungeon_obsidian", 7, 5)
    # Central approach to throne
    fill_rect(tiles, -5, 7, 5, 20, "tile_dungeon_rune")
    path_ns(tiles, 0, 5, 20, "tile_root_bark", 2)
    # Throne of the Horned Sovereign
    fill_rect(tiles, -16, 16, 21, 31, "tile_dungeon_obsidian")
    sprinkle(tiles, -16, 16, 21, 31, "tile_dungeon_rune", 6, 6)
    fill_rect(tiles, -4, 4, 24, 30, "tile_root_bark")

    env = [
        prop("env_crystal", 0, -26, 64, 96, 32, 82, "Nethergate Save Crystal"),
        prop("env_dungeon_pillar", -8, -24, 64, 128, 32, 116),
        prop("env_dungeon_pillar", 8, -24, 64, 128, 32, 116),
        prop("env_torch_brazier", -5, -22, 64, 64, 32, 54, animated=True),
        prop("env_torch_brazier", 5, -22, 64, 64, 32, 54, animated=True),
        prop("env_vault_door", -20, -28, 128, 160, 64, 148, "Ascent → Obsidian Spire"),
        prop("env_vault_door", 20, -28, 128, 160, 64, 148, "Ascent → Glacial Chasm"),
        # Bonemeal Hollows
        prop("env_root_hair", -12, -10, 64, 128, 32, 24),
        prop("env_root_hair", 10, -8, 64, 128, 32, 24),
        prop("env_root_hair", -6, -2, 64, 128, 32, 24),
        prop("env_root_hair", 8, 2, 64, 128, 32, 24),
        prop("env_root_hair", -16, 0, 64, 128, 32, 24),
        prop("env_dungeon_pillar", -10, -4, 64, 128, 32, 116),
        prop("env_dungeon_pillar", 10, -4, 64, 128, 32, 116),
        # Weeping Boughs
        prop("env_weeping_branch", -22, 8, 128, 160, 64, 40, "Weeping Branch"),
        prop("env_weeping_branch", -14, 12, 128, 160, 64, 40),
        prop("env_weeping_branch", -26, 14, 128, 160, 64, 40),
        prop("env_root_hair", -18, 10, 64, 128, 32, 24),
        # Sanguine Terrace
        prop("env_reliquary_casket", -24, 20, 64, 64, 32, 52, "Table Set for Eight"),
        prop("env_prayer_candles", -20, 18, 64, 64, 32, 54),
        prop("env_prayer_candles", -28, 22, 64, 64, 32, 54),
        prop("env_torch_brazier", -22, 22, 64, 64, 32, 54, animated=True),
        # Thorncradle Vault
        prop("env_briar_wall", 14, 8, 96, 128, 48, 116),
        prop("env_briar_wall", 22, 10, 96, 128, 48, 116),
        prop("env_briar_wall", 18, 16, 96, 128, 48, 116),
        prop("env_briar_wall", 26, 14, 96, 128, 48, 116),
        prop("env_torch_brazier", 16, 12, 64, 64, 32, 54, animated=True),
        prop("env_torch_brazier", 24, 18, 64, 64, 32, 54, animated=True),
        # Throne
        prop("env_dungeon_pillar", -8, 26, 64, 128, 32, 116),
        prop("env_dungeon_pillar", 8, 26, 64, 128, 32, 116),
        prop("env_briar_wall", -12, 24, 96, 128, 48, 116),
        prop("env_briar_wall", 12, 24, 96, 128, 48, 116),
        prop("env_torch_brazier", -5, 28, 64, 64, 32, 54, animated=True),
        prop("env_torch_brazier", 5, 28, 64, 64, 32, 54, animated=True),
        prop("env_crystal", 0, 24, 64, 96, 32, 82, "Sovereign Throne Marker"),
    ]

    monsters = [
        # Nethergate Descent
        mon("root_creeper_1", "Nethergate Creeper", "nethergate_creeper_ff", 72, -8, -22, speed=0.03, aggro=True),
        mon("root_creeper_2", "Nethergate Creeper", "nethergate_creeper_ff", 73, 10, -20, speed=0.03, aggro=True),
        mon("root_hound_1", "Umbral Houndkin", "umbral_houndkin_ff", 76, -12, -17, speed=0.038, aggro=True),
        mon("root_hound_2", "Umbral Houndkin", "umbral_houndkin_ff", 77, 8, -18, speed=0.038, aggro=True),
        # Bonemeal Hollows
        mon("root_hound_3", "Umbral Houndkin", "umbral_houndkin_ff", 78, -14, -8, speed=0.038, aggro=True),
        mon("root_hound_4", "Umbral Houndkin", "umbral_houndkin_ff", 79, 12, -4, speed=0.038, aggro=True),
        mon("root_devourer_1", "Rootfang Devourer", "rootfang_devourer_ff", 82, -6, 0, speed=0.032, aggro=True),
        mon("root_devourer_2", "Rootfang Devourer", "rootfang_devourer_ff", 83, 8, 2, speed=0.032, aggro=True),
        mon("root_choir_1", "Hollow Penitent Choir", "hollow_penitent_choir_ff", 80, -10, -2, speed=0.026, aggro=True),
        mon("root_choir_2", "Hollow Penitent Choir", "hollow_penitent_choir_ff", 81, 4, -10, speed=0.026, aggro=True),
        # Weeping Boughs
        mon("root_bough_1", "Weeping Bough", "weeping_bough_ff", 75, -20, 8, speed=0.018, aggro=False),
        mon("root_bough_2", "Weeping Bough", "weeping_bough_ff", 76, -26, 12, speed=0.018, aggro=False),
        mon("root_devourer_3", "Rootfang Devourer", "rootfang_devourer_ff", 84, -14, 14, speed=0.032, aggro=True),
        mon("root_thorncaller_1", "Sanguine Thorncaller", "sanguine_thorncaller_ff", 79, -18, 16, speed=0.024, aggro=False),
        # Sanguine Terrace (pacifist gate — non-hostile)
        mon("root_thorncaller_2", "Sanguine Thorncaller", "sanguine_thorncaller_ff", 82, -24, 20, speed=0.022, aggro=False),
        # Thorncradle Vault
        mon("root_herald_1", "Abyssal Heraldon", "abyssal_heraldon_ff", 86, 16, 10, speed=0.034, aggro=True),
        mon("root_herald_2", "Abyssal Heraldon", "abyssal_heraldon_ff", 88, 24, 14, speed=0.034, aggro=True),
        mon(
            "root_warden",
            "Thorncradle Warden",
            "thorncradle_warden_ff",
            90,
            20,
            16,
            rank="elite",
            speed=0.038,
        ),
        mon(
            "root_apostate",
            "The Pale Apostate",
            "the_pale_apostate_ff",
            92,
            26,
            12,
            rank="rare",
            speed=0.036,
        ),
        # Throne
        mon("root_herald_3", "Abyssal Heraldon", "abyssal_heraldon_ff", 90, -8, 24, speed=0.034, aggro=True),
        mon("root_choir_3", "Hollow Penitent Choir", "hollow_penitent_choir_ff", 84, 8, 25, speed=0.026, aggro=True),
        mon(
            "root_boss_verrocaine",
            "Verrocaine, the Horned Sovereign",
            "verrocaine_sovereign_ff",
            99,
            0,
            29,
            rank="boss",
            speed=0.045,
        ),
    ]

    sub_regions = [
        {
            "id": "nethergate_descent",
            "name": "Nethergate Descent",
            "type": "field",
            "minLv": 70,
            "maxLv": 76,
            "minWx": -31,
            "maxWx": 31,
            "minWy": -31,
            "maxWy": -16,
        },
        {
            "id": "bonemeal_hollows",
            "name": "Bonemeal Hollows",
            "type": "field",
            "minLv": 74,
            "maxLv": 82,
            "minWx": -31,
            "maxWx": 31,
            "minWy": -15,
            "maxWy": 4,
        },
        {
            "id": "the_weeping_boughs",
            "name": "The Weeping Boughs",
            "type": "field",
            "minLv": 78,
            "maxLv": 86,
            "minWx": -31,
            "maxWx": -6,
            "minWy": 5,
            "maxWy": 16,
        },
        {
            "id": "sanguine_terrace",
            "name": "Sanguine Terrace",
            "type": "hidden",
            "minLv": 80,
            "maxLv": 88,
            "minWx": -31,
            "maxWx": -14,
            "minWy": 17,
            "maxWy": 24,
        },
        {
            "id": "thorncradle_vault",
            "name": "Thorncradle Vault",
            "type": "elite",
            "minLv": 86,
            "maxLv": 93,
            "minWx": 8,
            "maxWx": 31,
            "minWy": 5,
            "maxWy": 20,
        },
        {
            "id": "throne_of_the_horned_sovereign",
            "name": "Throne of the Horned Sovereign",
            "type": "boss",
            "minLv": 93,
            "maxLv": 99,
            "minWx": -16,
            "maxWx": 16,
            "minWy": 21,
            "maxWy": 31,
        },
    ]

    exits = [
        {
            "id": "to_spire",
            "wx": -20,
            "wy": -28,
            "radius": 2.0,
            "targetMap": "spire",
            "targetWx": -26,
            "targetWy": 20,
            "label": "Ascent → Obsidian Spire (Skybridge)",
        },
        {
            "id": "to_chasm",
            "wx": 20,
            "wy": -28,
            "radius": 2.0,
            "targetMap": "chasm",
            "targetWx": 0,
            "targetWy": 28,
            "label": "Ascent → Glacial Chasm (Thronehall)",
        },
    ]

    return {
        "id": "rootways",
        "name": "Umbral Rootways",
        "gridWidth": 64,
        "gridHeight": 64,
        "bounds": {"minWx": MIN_W, "maxWx": MAX_W, "minWy": MIN_H, "maxWy": MAX_H},
        "defaultTile": "tile_dungeon_rune",
        "light": "#ede7f6",
        "minLv": 70,
        "maxLv": 99,
        "boss": "verrocaine_sovereign",
        "spawn": {"wx": 0, "wy": -28},
        "tiles": tiles,
        "envStructures": env,
        "npcs": [],
        "monsters": monsters,
        "subRegions": sub_regions,
        "exits": exits,
    }


def validate(maps: dict[str, dict]):
    errors = []
    map_ids = set(maps) | {"aethelgard", "gatewatch", "meadows", "sanctum"}
    legacy = {"bomb_ff", "goblin_ff", "skeleton_ff", "cactuar_ff", "boss_baphomet_ff"}
    for mid, data in maps.items():
        try:
            json.dumps(data)
        except Exception as e:
            errors.append(f"{mid}: JSON serialize failed: {e}")
        for m in data.get("monsters", []):
            sprite = m["sprite"]
            if sprite in legacy:
                errors.append(f"{mid}: legacy sprite {sprite} on {m['id']}")
            path = SPRITES / f"{sprite}.png"
            if not path.exists():
                errors.append(f"{mid}: missing sprite file {path.name} for {m['id']}")
            if m.get("rank") in ("elite", "rare", "boss") and "rank" not in m:
                errors.append(f"{mid}: missing rank on {m['id']}")
        for ex in data.get("exits", []):
            if ex["targetMap"] not in map_ids:
                errors.append(f"{mid}: exit {ex['id']} -> unknown map {ex['targetMap']}")
        # rootways must not portal to town
        if mid == "rootways":
            for ex in data["exits"]:
                if ex["targetMap"] == "aethelgard":
                    errors.append("rootways must not have town portal")
        # tile coverage
        expected = (MAX_W - MIN_W + 1) * (MAX_H - MIN_H + 1)
        if len(data["tiles"]) != expected:
            errors.append(f"{mid}: tile count {len(data['tiles'])} != {expected}")
        # subregion ids vs db if present
    return errors


def main():
    maps = {
        "spire": build_spire(),
        "chasm": build_chasm(),
        "rootways": build_rootways(),
    }
    MAPS.mkdir(parents=True, exist_ok=True)
    for mid, data in maps.items():
        out = MAPS / f"{mid}.json"
        with out.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
        print(
            f"Wrote {out.relative_to(ROOT)} — "
            f"tiles={len(data['tiles'])} props={len(data['envStructures'])} "
            f"npcs={len(data['npcs'])} monsters={len(data['monsters'])} "
            f"subs={len(data['subRegions'])} exits={len(data['exits'])}"
        )

    errors = validate(maps)
    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(" -", e)
        raise SystemExit(1)
    print("Validation OK: sprites exist, no legacy ids, exits resolve, tile grids full.")


if __name__ == "__main__":
    main()
