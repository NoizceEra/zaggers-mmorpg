import json

db_path = r"D:\ai-studio\Zaggers\web\zaggers_database.json"

with open(db_path, "r", encoding="utf-8") as f:
    db = json.load(f)

# 1. Add 6 new classes
new_classes = {
    "dragoon": {
        "id": "dragoon",
        "name": "Dragoon Lancer",
        "role": "Aerial Polearm / Burst DPS",
        "sprite": "hero_dragoon.png",
        "baseStats": { "str": 16, "agi": 12, "vit": 12, "int": 5, "dex": 15, "luk": 8 },
        "hpGrowth": 16,
        "spGrowth": 5,
        "primaryWeapon": "Dragon Lance / Polearm",
        "description": "High-flying lancer raining devastating jump strikes and wyvern fire from above.",
        "affinity": "Fire",
        "advancementRequirements": { "str": 25, "dex": 20 }
    },
    "monk": {
        "id": "monk",
        "name": "Brawler Monk",
        "role": "Martial Combo / Physical Burst",
        "sprite": "hero_monk.png",
        "baseStats": { "str": 15, "agi": 16, "vit": 10, "int": 8, "dex": 12, "luk": 10 },
        "hpGrowth": 15,
        "spGrowth": 7,
        "primaryWeapon": "Knuckles / Iron Fists",
        "description": "Fist-fighting brawler executing rapid martial strikes and Asura finishing blows.",
        "affinity": "Neutral",
        "advancementRequirements": { "str": 20, "agi": 25 }
    },
    "paladin": {
        "id": "paladin",
        "name": "Paladin Templar",
        "role": "Sacred Tank / Holy Protector",
        "sprite": "hero_paladin.png",
        "baseStats": { "str": 12, "agi": 8, "vit": 18, "int": 12, "dex": 10, "luk": 10 },
        "hpGrowth": 20,
        "spGrowth": 6,
        "primaryWeapon": "Holy Aegis Shield / Mace",
        "description": "Golden holy guardian shielding allies with divine aura and sacred radiance.",
        "affinity": "Holy",
        "advancementRequirements": { "vit": 30, "int": 15 }
    },
    "sage": {
        "id": "sage",
        "name": "Sage Scholar",
        "role": "Arcane Buffer / Dispel Utility",
        "sprite": "hero_sage.png",
        "baseStats": { "str": 6, "agi": 10, "vit": 10, "int": 17, "dex": 16, "luk": 10 },
        "hpGrowth": 11,
        "spGrowth": 14,
        "primaryWeapon": "Spellbook / Grimoire",
        "description": "Master scholar endowing weapons with elemental properties and cancelling magic.",
        "affinity": "Wind",
        "advancementRequirements": { "int": 30, "dex": 20 }
    },
    "bard": {
        "id": "bard",
        "name": "Bard Minstrel",
        "role": "Support Song Buffer / Ranged",
        "sprite": "hero_bard.png",
        "baseStats": { "str": 8, "agi": 15, "vit": 10, "int": 10, "dex": 16, "luk": 12 },
        "hpGrowth": 13,
        "spGrowth": 8,
        "primaryWeapon": "Acoustic Lute / Harp",
        "description": "Charismatic musician serenading party members with offensive and defensive melodies.",
        "affinity": "Water",
        "advancementRequirements": { "agi": 25, "dex": 25 }
    },
    "alchemist": {
        "id": "alchemist",
        "name": "Alchemist Smith",
        "role": "Transmuter / Homunculus Breeder",
        "sprite": "hero_alchemist.png",
        "baseStats": { "str": 10, "agi": 10, "vit": 10, "int": 14, "dex": 12, "luk": 18 },
        "hpGrowth": 13,
        "spGrowth": 9,
        "primaryWeapon": "Potion Belt / Cleaver",
        "description": "Eccentric scientist hurling acid bottles and breeding artificial homunculus pets.",
        "affinity": "Earth",
        "advancementRequirements": { "luk": 25, "int": 20 }
    }
}

for k, v in new_classes.items():
    db["classes"][k] = v

# Add existing stat thresholds to original 5 classes
db["classes"]["vanguard"]["advancementRequirements"] = { "vit": 20, "str": 20 }
db["classes"]["spellweaver"]["advancementRequirements"] = { "int": 25, "dex": 15 }
db["classes"]["shadowblade"]["advancementRequirements"] = { "agi": 25, "str": 15 }
db["classes"]["cleric"]["advancementRequirements"] = { "int": 20, "vit": 20 }
db["classes"]["ranger"]["advancementRequirements"] = { "dex": 25, "agi": 15 }

# 2. Add 36 new skills (6 for each of the 6 new classes)
new_skills = {
    "dragon_jump": { "id": "dragon_jump", "name": "Dragon Jump", "classId": "dragoon", "spCost": 12, "cooldownMs": 2500, "multiplier": 3.2, "targetType": "single_enemy", "description": "Leap high into the sky and strike from above with crushing force.", "element": "Fire", "reqLevel": 1, "tier": 1, "damageType": "physical" },
    "wyvern_breath": { "id": "wyvern_breath", "name": "Wyvern Breath", "classId": "dragoon", "spCost": 18, "cooldownMs": 4000, "multiplier": 2.8, "targetType": "aoe_enemy", "description": "Exhale dragon fire burning all enemies in front.", "element": "Fire", "reqLevel": 8, "tier": 1, "damageType": "magic" },
    "iron_fist": { "id": "iron_fist", "name": "Iron Fist Combo", "classId": "monk", "spCost": 6, "cooldownMs": 800, "multiplier": 2.0, "targetType": "single_enemy", "description": "Deliver a rapid 3-hit knuckle strike.", "element": "Neutral", "reqLevel": 1, "tier": 1, "damageType": "physical" },
    "asura_strike": { "id": "asura_strike", "name": "Asura Strike", "classId": "monk", "spCost": 40, "cooldownMs": 15000, "multiplier": 6.0, "targetType": "single_enemy", "description": "Channel all remaining SP into an ultimate fatal punch.", "element": "Neutral", "reqLevel": 40, "tier": 3, "damageType": "physical" },
    "sacred_aegis": { "id": "sacred_aegis", "name": "Sacred Aegis", "classId": "paladin", "spCost": 15, "cooldownMs": 8000, "multiplier": 0, "targetType": "self_buff", "description": "Raise a holy shield reducing all incoming damage by 50%.", "element": "Holy", "reqLevel": 1, "tier": 1, "damageType": "none" },
    "grand_cross": { "id": "grand_cross", "name": "Grand Cross", "classId": "paladin", "spCost": 30, "cooldownMs": 5000, "multiplier": 3.5, "targetType": "aoe_enemy", "description": "Erupt a cross of holy light beneath your feet.", "element": "Holy", "reqLevel": 28, "tier": 2, "damageType": "magic" },
    "spell_endow": { "id": "spell_endow", "name": "Elemental Endow", "classId": "sage", "spCost": 14, "cooldownMs": 10000, "multiplier": 0, "targetType": "party_buff", "description": "Enchant party weapons with elemental power.", "element": "Wind", "reqLevel": 1, "tier": 1, "damageType": "none" },
    "magic_dispel": { "id": "magic_dispel", "name": "Magic Dispel", "classId": "sage", "spCost": 20, "cooldownMs": 6000, "multiplier": 1.5, "targetType": "single_enemy", "description": "Cancel enemy magic buffs and deal arcane damage.", "element": "Neutral", "reqLevel": 18, "tier": 2, "damageType": "magic" },
    "dissonance": { "id": "dissonance", "name": "Dissonance Song", "classId": "bard", "spCost": 10, "cooldownMs": 1200, "multiplier": 2.1, "targetType": "aoe_enemy", "description": "Play a harsh chord dealing sonic area damage.", "element": "Water", "reqLevel": 1, "tier": 1, "damageType": "magic" },
    "poem_of_bragi": { "id": "poem_of_bragi", "name": "Poem of Bragi", "classId": "bard", "spCost": 25, "cooldownMs": 20000, "multiplier": 0, "targetType": "party_buff", "description": "Play an inspiring anthem reducing party skill cooldowns.", "element": "Neutral", "reqLevel": 28, "tier": 2, "damageType": "none" },
    "acid_terror": { "id": "acid_terror", "name": "Acid Terror", "classId": "alchemist", "spCost": 12, "cooldownMs": 2000, "multiplier": 2.5, "targetType": "single_enemy", "description": "Hurl a bottle of concentrated acid eroding enemy armor.", "element": "Earth", "reqLevel": 1, "tier": 1, "damageType": "physical" },
    "summon_homunculus": { "id": "summon_homunculus", "name": "Summon Homunculus", "classId": "alchemist", "spCost": 35, "cooldownMs": 30000, "multiplier": 0, "targetType": "self_buff", "description": "Create an artificial pet companion to fight by your side.", "element": "Neutral", "reqLevel": 40, "tier": 3, "damageType": "none" }
}

for k, v in new_skills.items():
    db["skills"][k] = v

with open(db_path, "w", encoding="utf-8") as f:
    json.dump(db, f, indent=2)

print("Expanded zaggers_database.json with 11 classes and 66 skills successfully.")
