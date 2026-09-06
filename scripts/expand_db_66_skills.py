import json

db_path = r"D:\ai-studio\Zaggers\web\zaggers_database.json"

with open(db_path, "r", encoding="utf-8") as f:
    db = json.load(f)

# Update existing 5 classes with lore and advancementRequirements
db["classes"]["vanguard"].update({
    "lore": "Frontline vanguard legion who stand as unyielding walls of iron and shield.",
    "advancementRequirements": { "vit": 20, "str": 20 }
})
db["classes"]["spellweaver"].update({
    "lore": "Mages of the spellweaver syndicate channeling raw elemental forces to obliterate enemy formations.",
    "advancementRequirements": { "int": 25, "dex": 15 }
})
db["classes"]["shadowblade"].update({
    "lore": "Shadowy assassins of the brotherhood, striking unseen from the dark with lethal efficiency.",
    "advancementRequirements": { "agi": 25, "str": 15 }
})
db["classes"]["cleric"].update({
    "lore": "Holy priests of the Order, weaving sacred blessings and restorative rites for their companions.",
    "advancementRequirements": { "int": 20, "vit": 20 }
})
db["classes"]["ranger"].update({
    "lore": "Wilderness marksmen of the Ranger Corps, wielding composite bows and mechanical traps with lethal precision.",
    "advancementRequirements": { "dex": 25, "agi": 15 }
})

# 36 New Skills (6 for each of the 6 new classes)
new_skills = {
    # Dragoon
    "dragon_jump": { "id": "dragon_jump", "name": "Dragon Jump", "classId": "dragoon", "spCost": 12, "cooldownMs": 2500, "multiplier": 3.2, "targetType": "single_enemy", "description": "Leap high into the sky and strike from above with crushing physical force.", "element": "Neutral", "reqLevel": 1, "tier": 1, "requires": None, "damageType": "physical" },
    "wyvern_breath": { "id": "wyvern_breath", "name": "Wyvern Breath", "classId": "dragoon", "spCost": 18, "cooldownMs": 4000, "multiplier": 2.8, "targetType": "aoe_enemy", "description": "Exhale dragon fire, scorching all enemies in a cone before you.", "element": "Fire", "reqLevel": 8, "tier": 1, "requires": None, "damageType": "magic" },
    "skypierce_thrust": { "id": "skypierce_thrust", "name": "Skypierce Thrust", "classId": "dragoon", "spCost": 22, "cooldownMs": 3500, "multiplier": 3.5, "targetType": "single_enemy", "description": "Drive a heavy polearm thrust through target defense, ignoring a portion of ARM.", "element": "Wind", "reqLevel": 18, "tier": 2, "requires": "dragon_jump", "damageType": "physical" },
    "dragon_heart": { "id": "dragon_heart", "name": "Dragon Heart", "classId": "dragoon", "spCost": 25, "cooldownMs": 18000, "multiplier": 0.0, "targetType": "self_buff", "description": "Awaken dragon spirit, boosting ATK, Critical rate, and Fire resistance.", "element": "Fire", "reqLevel": 28, "tier": 2, "requires": "wyvern_breath", "damageType": "none" },
    "comet_dive": { "id": "comet_dive", "name": "Comet Dive", "classId": "dragoon", "spCost": 38, "cooldownMs": 12000, "multiplier": 5.2, "targetType": "aoe_enemy", "description": "Plunge from cloud height, creating a fiery shockwave upon impact.", "element": "Fire", "reqLevel": 40, "tier": 3, "requires": "skypierce_thrust", "damageType": "physical" },
    "wyrmlord_fury": { "id": "wyrmlord_fury", "name": "Wyrmlord Fury", "classId": "dragoon", "spCost": 55, "cooldownMs": 30000, "multiplier": 6.8, "targetType": "single_enemy", "description": "Unleash an unbroken series of dragon polearm strikes.", "element": "Fire", "reqLevel": 55, "tier": 3, "requires": "dragon_heart", "damageType": "physical" },

    # Monk
    "iron_fist": { "id": "iron_fist", "name": "Iron Fist Combo", "classId": "monk", "spCost": 6, "cooldownMs": 800, "multiplier": 2.0, "targetType": "single_enemy", "description": "Deliver a rapid 3-hit knuckle strike.", "element": "Neutral", "reqLevel": 1, "tier": 1, "requires": None, "damageType": "physical" },
    "ki_blast": { "id": "ki_blast", "name": "Ki Blast", "classId": "monk", "spCost": 14, "cooldownMs": 2200, "multiplier": 2.4, "targetType": "single_enemy", "description": "Project spiritual energy outward to strike foes from distance.", "element": "Holy", "reqLevel": 8, "tier": 1, "requires": None, "damageType": "magic" },
    "guillotine_fist": { "id": "guillotine_fist", "name": "Guillotine Strike", "classId": "monk", "spCost": 20, "cooldownMs": 4000, "multiplier": 3.6, "targetType": "single_enemy", "description": "Target vital pressure points with a crushing strike.", "element": "Neutral", "reqLevel": 18, "tier": 2, "requires": "iron_fist", "damageType": "physical" },
    "body_relocation": { "id": "body_relocation", "name": "Body Relocation", "classId": "monk", "spCost": 18, "cooldownMs": 6000, "multiplier": 0.0, "targetType": "self_buff", "description": "Instantly step through martial focus, boosting FLEE and movement speed.", "element": "Wind", "reqLevel": 28, "tier": 2, "requires": "ki_blast", "damageType": "none" },
    "zen_meditation": { "id": "zen_meditation", "name": "Zen Meditation", "classId": "monk", "spCost": 30, "cooldownMs": 25000, "multiplier": 0.0, "targetType": "self_buff", "description": "Enter deep focus, instantly restoring SP and increasing ATK.", "element": "Holy", "reqLevel": 40, "tier": 3, "requires": "body_relocation", "damageType": "none" },
    "asura_strike": { "id": "asura_strike", "name": "Asura Strike", "classId": "monk", "spCost": 60, "cooldownMs": 40000, "multiplier": 7.5, "targetType": "single_enemy", "description": "Channel all remaining spiritual energy into an ultimate fatal punch.", "element": "Neutral", "reqLevel": 55, "tier": 3, "requires": "guillotine_fist", "damageType": "physical" },

    # Paladin
    "sacred_aegis": { "id": "sacred_aegis", "name": "Sacred Aegis", "classId": "paladin", "spCost": 15, "cooldownMs": 8000, "multiplier": 0.0, "targetType": "self_buff", "description": "Raise a holy shield reducing all incoming damage by 50%.", "element": "Holy", "reqLevel": 1, "tier": 1, "requires": None, "damageType": "none" },
    "shield_boomerang": { "id": "shield_boomerang", "name": "Shield Boomerang", "classId": "paladin", "spCost": 10, "cooldownMs": 2000, "multiplier": 2.2, "targetType": "single_enemy", "description": "Hurl your shield at an enemy, scaling damage with defense.", "element": "Neutral", "reqLevel": 8, "tier": 1, "requires": None, "damageType": "physical" },
    "holy_cross": { "id": "holy_cross", "name": "Holy Cross", "classId": "paladin", "spCost": 20, "cooldownMs": 3000, "multiplier": 3.0, "targetType": "single_enemy", "description": "Carve a sacred cross into the target with holy energy.", "element": "Holy", "reqLevel": 18, "tier": 2, "requires": "shield_boomerang", "damageType": "physical" },
    "devotion_guard": { "id": "devotion_guard", "name": "Devotion Guard", "classId": "paladin", "spCost": 28, "cooldownMs": 20000, "multiplier": 0.0, "targetType": "party_buff", "description": "Bind party members to your oath, absorbing damage meant for allies.", "element": "Holy", "reqLevel": 28, "tier": 2, "requires": "sacred_aegis", "damageType": "none" },
    "grand_cross": { "id": "grand_cross", "name": "Grand Cross", "classId": "paladin", "spCost": 40, "cooldownMs": 12000, "multiplier": 4.8, "targetType": "aoe_enemy", "description": "Erupt a massive cross of holy light beneath your feet.", "element": "Holy", "reqLevel": 40, "tier": 3, "requires": "holy_cross", "damageType": "magic" },
    "martyrs_reckoning": { "id": "martyrs_reckoning", "name": "Martyr's Reckoning", "classId": "paladin", "spCost": 50, "cooldownMs": 35000, "multiplier": 6.2, "targetType": "aoe_enemy", "description": "Sacrifice HP to inflict devastating Holy retributive damage.", "element": "Holy", "reqLevel": 55, "tier": 3, "requires": "devotion_guard", "damageType": "physical" },

    # Sage
    "spell_endow": { "id": "spell_endow", "name": "Elemental Endow", "classId": "sage", "spCost": 14, "cooldownMs": 10000, "multiplier": 0.0, "targetType": "party_buff", "description": "Enchant party weapons with elemental power, boosting party damage.", "element": "Wind", "reqLevel": 1, "tier": 1, "requires": None, "damageType": "none" },
    "freecast_bolt": { "id": "freecast_bolt", "name": "Freecast Bolt", "classId": "sage", "spCost": 12, "cooldownMs": 1500, "multiplier": 2.5, "targetType": "single_enemy", "description": "Cast an elemental bolt while moving without casting interruption.", "element": "Wind", "reqLevel": 8, "tier": 1, "requires": None, "damageType": "magic" },
    "magic_dispel": { "id": "magic_dispel", "name": "Magic Dispel", "classId": "sage", "spCost": 20, "cooldownMs": 6000, "multiplier": 1.5, "targetType": "single_enemy", "description": "Cancel enemy magical buffs and deal arcane damage.", "element": "Neutral", "reqLevel": 18, "tier": 2, "requires": "freecast_bolt", "damageType": "magic" },
    "deluge_field": { "id": "deluge_field", "name": "Deluge Field", "classId": "sage", "spCost": 26, "cooldownMs": 15000, "multiplier": 1.8, "targetType": "aoe_enemy", "description": "Summon a watery field that increases Water magic damage.", "element": "Water", "reqLevel": 28, "tier": 2, "requires": "spell_endow", "damageType": "magic" },
    "spell_breaker": { "id": "spell_breaker", "name": "Spell Breaker", "classId": "sage", "spCost": 32, "cooldownMs": 12000, "multiplier": 3.5, "targetType": "single_enemy", "description": "Shatter casting focus of enemy, absorbing their SP.", "element": "Neutral", "reqLevel": 40, "tier": 3, "requires": "magic_dispel", "damageType": "magic" },
    "volcano_zone": { "id": "volcano_zone", "name": "Volcano Zone", "classId": "sage", "spCost": 55, "cooldownMs": 25000, "multiplier": 5.5, "targetType": "aoe_enemy", "description": "Transform ground into lava fissures, boosting Fire damage and burning targets.", "element": "Fire", "reqLevel": 55, "tier": 3, "requires": "deluge_field", "damageType": "magic" },

    # Bard
    "dissonance": { "id": "dissonance", "name": "Dissonance Song", "classId": "bard", "spCost": 10, "cooldownMs": 1200, "multiplier": 2.1, "targetType": "aoe_enemy", "description": "Play a harsh chord dealing sonic area damage.", "element": "Water", "reqLevel": 1, "tier": 1, "requires": None, "damageType": "magic" },
    "unruly_melody": { "id": "unruly_melody", "name": "Unruly Melody", "classId": "bard", "spCost": 12, "cooldownMs": 1800, "multiplier": 2.4, "targetType": "single_enemy", "description": "Fire a musical arrow that disorients the enemy target.", "element": "Neutral", "reqLevel": 8, "tier": 1, "requires": None, "damageType": "physical" },
    "poem_of_bragi": { "id": "poem_of_bragi", "name": "Poem of Bragi", "classId": "bard", "spCost": 25, "cooldownMs": 20000, "multiplier": 0.0, "targetType": "party_buff", "description": "Play an inspiring anthem reducing party skill cooldowns and cast time.", "element": "Neutral", "reqLevel": 18, "tier": 2, "requires": "dissonance", "damageType": "none" },
    "frost_joker": { "id": "frost_joker", "name": "Frost Joker", "classId": "bard", "spCost": 22, "cooldownMs": 8000, "multiplier": 2.6, "targetType": "aoe_enemy", "description": "Tell a joke so terrible it freezes enemies around you.", "element": "Water", "reqLevel": 28, "tier": 2, "requires": "unruly_melody", "damageType": "magic" },
    "apple_of_idun": { "id": "apple_of_idun", "name": "Apple of Idun", "classId": "bard", "spCost": 35, "cooldownMs": 30000, "multiplier": 0.0, "targetType": "party_buff", "description": "Sing a restorative lullaby increasing Max HP and regeneration for all allies.", "element": "Holy", "reqLevel": 40, "tier": 3, "requires": "poem_of_bragi", "damageType": "none" },
    "great_echo": { "id": "great_echo", "name": "Great Echo", "classId": "bard", "spCost": 50, "cooldownMs": 18000, "multiplier": 5.8, "targetType": "aoe_enemy", "description": "Release a powerful acoustic shockwave reverberating across the battlefield.", "element": "Wind", "reqLevel": 55, "tier": 3, "requires": "frost_joker", "damageType": "magic" },

    # Alchemist
    "acid_terror": { "id": "acid_terror", "name": "Acid Terror", "classId": "alchemist", "spCost": 12, "cooldownMs": 2000, "multiplier": 2.5, "targetType": "single_enemy", "description": "Hurl a bottle of concentrated acid eroding enemy armor.", "element": "Earth", "reqLevel": 1, "tier": 1, "requires": None, "damageType": "physical" },
    "potion_pitcher": { "id": "potion_pitcher", "name": "Potion Pitcher", "classId": "alchemist", "spCost": 10, "cooldownMs": 1000, "multiplier": 2.2, "targetType": "ally_heal", "description": "Toss healing potion brews directly onto an injured ally.", "element": "Neutral", "reqLevel": 8, "tier": 1, "requires": None, "damageType": "none" },
    "demon_demonstration": { "id": "demon_demonstration", "name": "Demon Demonstration", "classId": "alchemist", "spCost": 22, "cooldownMs": 4000, "multiplier": 3.0, "targetType": "aoe_enemy", "description": "Throw a bottle of volatile fuel creating a flaming floor patch.", "element": "Fire", "reqLevel": 18, "tier": 2, "requires": "acid_terror", "damageType": "magic" },
    "transmute_gold": { "id": "transmute_gold", "name": "Transmute Gold", "classId": "alchemist", "spCost": 20, "cooldownMs": 15000, "multiplier": 1.8, "targetType": "single_enemy", "description": "Transmute enemy armor into gold, slowing them and increasing item drop value.", "element": "Earth", "reqLevel": 28, "tier": 2, "requires": "potion_pitcher", "damageType": "magic" },
    "summon_homunculus": { "id": "summon_homunculus", "name": "Summon Homunculus", "classId": "alchemist", "spCost": 35, "cooldownMs": 30000, "multiplier": 0.0, "targetType": "self_buff", "description": "Create an artificial pet companion to fight by your side.", "element": "Neutral", "reqLevel": 40, "tier": 3, "requires": "transmute_gold", "damageType": "none" },
    "acid_demonstration": { "id": "acid_demonstration", "name": "Acid Demonstration", "classId": "alchemist", "spCost": 55, "cooldownMs": 20000, "multiplier": 6.5, "targetType": "single_enemy", "description": "Combine acid bomb and fire bottle for an explosive chemical reaction.", "element": "Fire", "reqLevel": 55, "tier": 3, "requires": "demon_demonstration", "damageType": "physical" }
}

for k, v in new_skills.items():
    db["skills"][k] = v

with open(db_path, "w", encoding="utf-8") as f:
    json.dump(db, f, indent=2)

print("Updated zaggers_database.json. Total Classes:", len(db["classes"]), "Total Skills:", len(db["skills"]))
