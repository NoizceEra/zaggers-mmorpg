import json
import random
import os

def generate_spire_map():
    map_data = {
        "id": "spire",
        "name": "Obsidian Spire",
        "gridWidth": 64,
        "gridHeight": 64,
        "bounds": { "minWx": -31, "maxWx": 31, "minWy": -31, "maxWy": 31 },
        "defaultTile": "tile_dungeon_obsidian",
        "light": "#ffebee",
        "minLv": 30,
        "maxLv": 52,
        "boss": "vashkar_spire_crown",
        "spawn": { "wx": 0, "wy": -28 },
        "tiles": {},
        "envStructures": [
            { "type": "env_house_shop", "wx": -18, "wy": -24, "width": 128, "height": 128, "anchorX": 64, "anchorY": 98, "name": "Slagworks Foundry Base" },
            { "type": "env_dungeon_pillar", "wx": -10, "wy": -15, "width": 64, "height": 128, "anchorX": 32, "anchorY": 116 },
            { "type": "env_dungeon_pillar", "wx": 10, "wy": -15, "width": 64, "height": 128, "anchorX": 32, "anchorY": 116 },
            { "type": "env_dungeon_pillar", "wx": -10, "wy": 0, "width": 64, "height": 128, "anchorX": 32, "anchorY": 116 },
            { "type": "env_dungeon_pillar", "wx": 10, "wy": 0, "width": 64, "height": 128, "anchorX": 32, "anchorY": 116 },
            { "type": "env_torch_brazier", "wx": -6, "wy": -20, "width": 64, "height": 64, "anchorX": 32, "anchorY": 54, "animated": True },
            { "type": "env_torch_brazier", "wx": 6, "wy": -20, "width": 64, "height": 64, "anchorX": 32, "anchorY": 54, "animated": True },
            { "type": "env_torch_brazier", "wx": -6, "wy": 10, "width": 64, "height": 64, "anchorX": 32, "anchorY": 54, "animated": True },
            { "type": "env_torch_brazier", "wx": 6, "wy": 10, "width": 64, "height": 64, "anchorX": 32, "anchorY": 54, "animated": True },
            { "type": "env_crystal", "wx": 0, "wy": 24, "width": 64, "height": 96, "anchorX": 32, "anchorY": 82, "name": "Spire Crown Altar" }
        ],
        "npcs": [
            {
                "id": "caravan_vendor",
                "name": "[NPC] Caravan Quartermaster",
                "title": "Cinderfall Merchant",
                "wx": -4, "wy": -26, "dir": 0, "frame": 1, "sprite": "npc_merchant",
                "dialogHeader": "Caravan Quartermaster",
                "dialogText": "Ash falls heavy up here on the Spire! Restock your potions and fire resistance elixirs before ascending to the Slagworks.",
                "options": [
                    { "text": "🧪 Open Caravan Supplies", "action": "open_shop" },
                    { "text": "❌ Cancel", "action": "close" }
                ]
            }
        ],
        "monsters": [
            { "id": 501, "name": "Fire Bomb", "wx": -12, "wy": -18, "speed": 0.03, "dir": 0, "frame": 1, "hp": 240, "maxHp": 240, "sprite": "bomb_ff", "isAggro": True, "zone": "spire" },
            { "id": 502, "name": "Fire Bomb", "wx": 12, "wy": -18, "speed": 0.03, "dir": 0, "frame": 1, "hp": 240, "maxHp": 240, "sprite": "bomb_ff", "isAggro": True, "zone": "spire" },
            { "id": 503, "name": "Fire Bomb", "wx": -10, "wy": -5, "speed": 0.03, "dir": 0, "frame": 1, "hp": 240, "maxHp": 240, "sprite": "bomb_ff", "isAggro": True, "zone": "spire" },
            { "id": 504, "name": "Goblin Raider", "wx": 8, "wy": 4, "speed": 0.035, "dir": 0, "frame": 1, "hp": 300, "maxHp": 300, "sprite": "goblin_ff", "isAggro": True, "zone": "spire" },
            { "id": 505, "name": "Skeleton Warrior", "wx": -8, "wy": 12, "speed": 0.03, "dir": 0, "frame": 1, "hp": 380, "maxHp": 380, "sprite": "skeleton_ff", "isAggro": True, "zone": "spire" },
            { "id": 506, "name": "Vashkar Spire Crown (Boss)", "wx": 0, "wy": 22, "speed": 0.04, "dir": 0, "frame": 1, "hp": 1200, "maxHp": 1200, "sprite": "boss_baphomet_ff", "isAggro": True, "zone": "spire" }
        ],
        "subRegions": [
            { "id": "cinderfall_approach", "name": "Cinderfall Approach", "type": "entry", "minLv": 30, "maxLv": 36, "minWx": -31, "maxWx": 31, "minWy": -31, "maxWy": -16 },
            { "id": "emberglass_terraces", "name": "Emberglass Terraces", "type": "gathering", "minLv": 33, "maxLv": 40, "minWx": -31, "maxWx": -10, "minWy": -15, "maxWy": 5 },
            { "id": "ashfall_overlook", "name": "Ashfall Overlook", "type": "vista", "minLv": 30, "maxLv": 52, "minWx": 10, "maxWx": 31, "minWy": -15, "maxWy": 5 },
            { "id": "slagworks", "name": "The Slagworks", "type": "combat", "minLv": 36, "maxLv": 45, "minWx": -31, "maxWx": 31, "minWy": 6, "maxWy": 18 },
            { "id": "spire_crown", "name": "The Spire Crown", "type": "boss", "minLv": 48, "maxLv": 52, "minWx": -20, "maxWx": 20, "minWy": 19, "maxWy": 31 }
        ],
        "exits": [
            { "id": "to_aethelgard", "wx": 0, "wy": -31, "radius": 2.0, "targetMap": "aethelgard", "targetWx": -26, "targetWy": 0, "label": "Ashroad Caravan → Aethelgard" },
            { "id": "to_rootways", "wx": 0, "wy": 31, "radius": 2.0, "targetMap": "rootways", "targetWx": 0, "targetWy": -28, "label": "Collapsed Skybridge → Umbral Rootways", "minLevel": 45 }
        ]
    }

    # Generate tiles grid
    for x in range(-31, 32):
        for y in range(-31, 32):
            if abs(x) <= 3 or abs(y) == 6 or abs(y) == 18:
                tile = "tile_dungeon_lava"
            elif (abs(x) + abs(y)) % 4 == 0:
                tile = "tile_dungeon_rune"
            else:
                tile = "tile_dungeon_obsidian"
            map_data["tiles"][f"{x},{y}"] = tile

    return map_data

def generate_chasm_map():
    map_data = {
        "id": "chasm",
        "name": "Glacial Chasm",
        "gridWidth": 64,
        "gridHeight": 64,
        "bounds": { "minWx": -31, "maxWx": 31, "minWy": -31, "maxWy": 31 },
        "defaultTile": "tile_dungeon_slate",
        "light": "#e8eaf6",
        "minLv": 50,
        "maxLv": 72,
        "boss": "sylveth_silent_thaw",
        "spawn": { "wx": 0, "wy": -28 },
        "tiles": {},
        "envStructures": [
            { "type": "env_crystal", "wx": -12, "wy": -20, "width": 64, "height": 96, "anchorX": 32, "anchorY": 82, "name": "Glacial Ice Pillar" },
            { "type": "env_crystal", "wx": 12, "wy": -20, "width": 64, "height": 96, "anchorX": 32, "anchorY": 82, "name": "Glacial Ice Pillar" },
            { "type": "env_dungeon_pillar", "wx": -8, "wy": -4, "width": 64, "height": 128, "anchorX": 32, "anchorY": 116 },
            { "type": "env_dungeon_pillar", "wx": 8, "wy": -4, "width": 64, "height": 128, "anchorX": 32, "anchorY": 116 },
            { "type": "env_crystal", "wx": 0, "wy": 24, "width": 64, "height": 96, "anchorX": 32, "anchorY": 82, "name": "Aurora Throne Crystal" }
        ],
        "npcs": [
            {
                "id": "smuggler_vendor",
                "name": "[NPC] Rimewind Merchant",
                "title": "Glacial Trader",
                "wx": -3, "wy": -25, "dir": 0, "frame": 1, "sprite": "npc_merchant",
                "dialogHeader": "Rimewind Merchant",
                "dialogText": "Brr! The blizzard howls out on the Aurora Shelf. Make sure you are equipped with high DEF gear before facing Sylveth's frost shades.",
                "options": [
                    { "text": "🧪 Open Glacial Gear Shop", "action": "open_shop" },
                    { "text": "❌ Cancel", "action": "close" }
                ]
            }
        ],
        "monsters": [
            { "id": 601, "name": "Cactuar", "wx": -10, "wy": -16, "speed": 0.03, "dir": 0, "frame": 1, "hp": 350, "maxHp": 350, "sprite": "cactuar_ff", "isAggro": True, "zone": "chasm" },
            { "id": 602, "name": "Skeleton Warrior", "wx": 10, "wy": -16, "speed": 0.03, "dir": 0, "frame": 1, "hp": 400, "maxHp": 400, "sprite": "skeleton_ff", "isAggro": True, "zone": "chasm" },
            { "id": 603, "name": "Goblin Raider", "wx": -8, "wy": 2, "speed": 0.035, "dir": 0, "frame": 1, "hp": 420, "maxHp": 420, "sprite": "goblin_ff", "isAggro": True, "zone": "chasm" },
            { "id": 604, "name": "Skeleton Warrior", "wx": 8, "wy": 12, "speed": 0.03, "dir": 0, "frame": 1, "hp": 450, "maxHp": 450, "sprite": "skeleton_ff", "isAggro": True, "zone": "chasm" },
            { "id": 605, "name": "Sylveth Silent Thaw (Boss)", "wx": 0, "wy": 22, "speed": 0.04, "dir": 0, "frame": 1, "hp": 1500, "maxHp": 1500, "sprite": "boss_baphomet_ff", "isAggro": True, "zone": "chasm" }
        ],
        "subRegions": [
            { "id": "rimewind_pass", "name": "Rimewind Pass", "type": "entry", "minLv": 50, "maxLv": 56, "minWx": -31, "maxWx": 31, "minWy": -31, "maxWy": -16 },
            { "id": "statuary_fallen", "name": "Statuary of the Fallen", "type": "lore", "minLv": 54, "maxLv": 62, "minWx": -31, "maxWx": -5, "minWy": -15, "maxWy": 5 },
            { "id": "aurora_shelf", "name": "Aurora Shelf", "type": "vista", "minLv": 50, "maxLv": 72, "minWx": 6, "maxWx": 31, "minWy": -15, "maxWy": 5 },
            { "id": "hoarfrost_vault", "name": "Hoarfrost Vault", "type": "hidden", "minLv": 60, "maxLv": 68, "minWx": -31, "maxWx": 31, "minWy": 6, "maxWy": 18 },
            { "id": "thronehall_ice", "name": "Thronehall of Ice", "type": "boss", "minLv": 66, "maxLv": 72, "minWx": -20, "maxWx": 20, "minWy": 19, "maxWy": 31 }
        ],
        "exits": [
            { "id": "to_aethelgard", "wx": 0, "wy": -31, "radius": 2.0, "targetMap": "aethelgard", "targetWx": 26, "targetWy": 0, "label": "Rimewind Tramway → Aethelgard" },
            { "id": "to_rootways", "wx": 0, "wy": 31, "radius": 2.0, "targetMap": "rootways", "targetWx": 0, "targetWy": -28, "label": "Thronehall Gate → Umbral Rootways", "minLevel": 66 }
        ]
    }

    for x in range(-31, 32):
        for y in range(-31, 32):
            if abs(x) <= 2 or abs(y) == 5:
                tile = "tile_dungeon_rune"
            elif (abs(x) + abs(y)) % 5 == 0:
                tile = "tile_meadow_water"
            else:
                tile = "tile_dungeon_slate"
            map_data["tiles"][f"{x},{y}"] = tile

    return map_data

def generate_rootways_map():
    map_data = {
        "id": "rootways",
        "name": "Umbral Rootways",
        "gridWidth": 64,
        "gridHeight": 64,
        "bounds": { "minWx": -31, "maxWx": 31, "minWy": -31, "maxWy": 31 },
        "defaultTile": "tile_dungeon_rune",
        "light": "#ede7f6",
        "minLv": 70,
        "maxLv": 99,
        "boss": "lord_baphomet_verrocaine",
        "spawn": { "wx": 0, "wy": -28 },
        "tiles": {},
        "envStructures": [
            { "type": "env_crystal", "wx": -14, "wy": -18, "width": 64, "height": 96, "anchorX": 32, "anchorY": 82, "name": "Umbral Shadow Crystal" },
            { "type": "env_crystal", "wx": 14, "wy": -18, "width": 64, "height": 96, "anchorX": 32, "anchorY": 82, "name": "Umbral Shadow Crystal" },
            { "type": "env_dungeon_pillar", "wx": -10, "wy": 0, "width": 64, "height": 128, "anchorX": 32, "anchorY": 116 },
            { "type": "env_dungeon_pillar", "wx": 10, "wy": 0, "width": 64, "height": 128, "anchorX": 32, "anchorY": 116 },
            { "type": "env_torch_brazier", "wx": -6, "wy": 16, "width": 64, "height": 64, "anchorX": 32, "anchorY": 54, "animated": True },
            { "type": "env_torch_brazier", "wx": 6, "wy": 16, "width": 64, "height": 64, "anchorX": 32, "anchorY": 54, "animated": True },
            { "type": "env_crystal", "wx": 0, "wy": 24, "width": 64, "height": 96, "anchorX": 32, "anchorY": 82, "name": "Sanctum Abyss Core" }
        ],
        "npcs": [],
        "monsters": [
            { "id": 701, "name": "Skeleton Warrior", "wx": -8, "wy": -14, "speed": 0.035, "dir": 0, "frame": 1, "hp": 600, "maxHp": 600, "sprite": "skeleton_ff", "isAggro": True, "zone": "rootways" },
            { "id": 702, "name": "Goblin Raider", "wx": 8, "wy": -14, "speed": 0.04, "dir": 0, "frame": 1, "hp": 550, "maxHp": 550, "sprite": "goblin_ff", "isAggro": True, "zone": "rootways" },
            { "id": 703, "name": "Fire Bomb", "wx": -10, "wy": 4, "speed": 0.035, "dir": 0, "frame": 1, "hp": 500, "maxHp": 500, "sprite": "bomb_ff", "isAggro": True, "zone": "rootways" },
            { "id": 704, "name": "Lord Baphomet (Sovereign Boss)", "wx": 0, "wy": 22, "speed": 0.045, "dir": 0, "frame": 1, "hp": 3000, "maxHp": 3000, "sprite": "boss_baphomet_ff", "isAggro": True, "zone": "rootways" }
        ],
        "subRegions": [
            { "id": "nethergate_descent", "name": "Nethergate Descent", "type": "entry", "minLv": 70, "maxLv": 76, "minWx": -31, "maxWx": 31, "minWy": -31, "maxWy": -16 },
            { "id": "bonemeal_hollows", "name": "Bonemeal Hollows", "type": "combat", "minLv": 74, "maxLv": 82, "minWx": -31, "maxWx": 31, "minWy": -15, "maxWy": 5 },
            { "id": "weeping_boughs", "name": "The Weeping Boughs", "type": "horror", "minLv": 78, "maxLv": 86, "minWx": -31, "maxWx": 31, "minWy": 6, "maxWy": 18 },
            { "id": "throne_horned_sovereign", "name": "Throne of the Horned Sovereign", "type": "boss", "minLv": 93, "maxLv": 99, "minWx": -20, "maxWx": 20, "minWy": 19, "maxWy": 31 }
        ],
        "exits": [
            { "id": "to_spire", "wx": -28, "wy": -28, "radius": 2.0, "targetMap": "spire", "targetWx": 0, "targetWy": 28, "label": "Ascent → Obsidian Spire" },
            { "id": "to_chasm", "wx": 28, "wy": -28, "radius": 2.0, "targetMap": "chasm", "targetWx": 0, "targetWy": 28, "label": "Ascent → Glacial Chasm" }
        ]
    }

    for x in range(-31, 32):
        for y in range(-31, 32):
            if abs(x) <= 2 or abs(y) == 18:
                tile = "tile_dungeon_lava"
            elif (abs(x) + abs(y)) % 3 == 0:
                tile = "tile_dungeon_obsidian"
            else:
                tile = "tile_dungeon_rune"
            map_data["tiles"][f"{x},{y}"] = tile

    return map_data

os.makedirs(r'D:\ai-studio\Zaggers\web\maps', exist_ok=True)

with open(r'D:\ai-studio\Zaggers\web\maps\spire.json', 'w', encoding='utf-8') as f:
    json.dump(generate_spire_map(), f, indent=2)

with open(r'D:\ai-studio\Zaggers\web\maps\chasm.json', 'w', encoding='utf-8') as f:
    json.dump(generate_chasm_map(), f, indent=2)

with open(r'D:\ai-studio\Zaggers\web\maps\rootways.json', 'w', encoding='utf-8') as f:
    json.dump(generate_rootways_map(), f, indent=2)

print("Generated full map JSON files for spire.json, chasm.json, and rootways.json successfully.")
