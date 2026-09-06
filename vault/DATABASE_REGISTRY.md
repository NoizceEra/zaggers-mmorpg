# DATABASE REGISTRY SPECIFICATION

This document outlines the JSON schema format used by `zaggers_database.json` and consumed by both `web/index.html` (Game Client) and `web/db_editor.html` (Database Engine Editor).

---

## 1. Class Schema (`classes`)
```json
{
  "vanguard": {
    "id": "vanguard",
    "name": "Vanguard",
    "role": "Tank / Melee DPS",
    "sprite": "hero_knight.png",
    "baseStats": { "str": 14, "agi": 10, "vit": 16, "int": 6, "dex": 12, "luk": 8 },
    "hpGrowth": 18,
    "spGrowth": 4,
    "primaryWeapon": "Sword / Lance",
    "description": "Stalwart frontline defender commanding heavy armor and devastating melee strikes."
  }
}
```

### Stat Formulas:
- **Max HP**: `BaseHP + (VIT * 15) + (Level * hpGrowth)`
- **Max SP**: `BaseSP + (INT * 8) + (Level * spGrowth)`
- **ATK**: `STR + (DEX / 5) + WeaponATK`
- **MATK**: `INT + (DEX / 5) + StaffMATK`
- **DEF**: `VIT / 2 + ArmorDEF`
- **FLEE**: `100 + Level + AGI`
- **HIT**: `175 + Level + DEX`
- **CRIT**: `1 + (LUK / 3)`

---

## 2. Skill Schema (`skills`)
```json
{
  "bash": {
    "id": "bash",
    "name": "Bash",
    "classId": "vanguard",
    "spCost": 8,
    "cooldownMs": 1500,
    "multiplier": 2.5,
    "targetType": "single_enemy",
    "description": "Deliver a heavy blow dealing 250% physical damage with a chance to stun."
  }
}
```

---

## 3. Item & Equipment Schema (`items`)
```json
{
  "red_potion": {
    "id": "red_potion",
    "name": "Red Potion",
    "type": "consumable",
    "price": 50,
    "healHp": 100,
    "icon": "potion_health_ff.png"
  },
  "dragon_lance": {
    "id": "dragon_lance",
    "name": "Dragon Lance",
    "type": "weapon",
    "price": 600,
    "atk": 35,
    "crit": 10,
    "icon": "excalibur_ff.png"
  }
}
```

---

## 4. Monster Schema (`monsters`)
```json
{
  "slime_green": {
    "id": "slime_green",
    "name": "Green Slime",
    "sprite": "slime_green_ff.png",
    "hp": 45,
    "atk": 8,
    "def": 2,
    "exp": 12,
    "zeny": 15,
    "drops": [
      { "itemId": "red_potion", "chance": 0.45 }
    ]
  }
}
```
