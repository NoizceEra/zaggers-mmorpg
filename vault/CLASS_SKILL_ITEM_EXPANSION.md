# CLASS, SKILL & ITEM EXPANSION

**Status:** Design spec for Phase 3.
**Implements:** `DESIGN_AUDIT.md` §1.3 (3 skills for 5 classes), §1.5 (no slots, no progression), §1.4 (elements).
**Companion:** elemental modifier table lives in `BESTIARY_EXPANSION.md` §1.1.

---

## 1. Skill system — 30 skills, 6 per class

### 1.1 Schema

Existing fields (**must not change** — `db_editor.html:581-618` binds all of them):
`id`, `name`, `classId`, `spCost`, `cooldownMs`, `multiplier`, `targetType`, `description`

Additive fields (safe; the editor ignores unknown keys):
```jsonc
{
  "element": "Fire",      // one of the nine, or "Neutral"
  "reqLevel": 25,         // job level gate
  "tier": 3,              // 1..3 — skill-tree depth
  "requires": "fireball", // prerequisite skill id, or null for tier-1
  "damageType": "magic"   // physical | magic | none
}
```

`targetType` values in use: `single_enemy`, `aoe_enemy`, `ally_heal`, `self_buff`, `party_buff`, `ally_single`, `ground_trap`.

**Tree shape per class:** 2 skills at tier 1 (available from Lv 1 and Lv 8), 2 at tier 2 (Lv 18/28), 2 at tier 3 (Lv 40/55). This gives the roadmap's Skill Tree Visualizer a real 2-3-2 lattice to draw, and fills the F1–F6 hotbar by Lv 40.

### 1.2 Vanguard — *Tank / Melee DPS*, physical, Neutral & Holy

| id | Name | Tier | Lv | SP | CD | Mult | Target | Element | Description |
|---|---|---|---|---|---|---|---|---|---|
| `bash` *(existing)* | Bash | 1 | 1 | 8 | 1200 | 2.2 | single_enemy | Neutral | Strike an enemy with powerful physical force. |
| `provoke_roar` | Provoke Roar | 1 | 8 | 10 | 6000 | 0.5 | aoe_enemy | Neutral | Bellow a challenge, forcing nearby enemies to target you and lowering their DEF. |
| `shield_bulwark` | Shield Bulwark | 2 | 18 | 14 | 12000 | 0 | self_buff | Neutral | Plant your shield. Damage taken is reduced by 40% while you hold position. |
| `cleaving_sweep` | Cleaving Sweep | 2 | 28 | 22 | 3500 | 2.8 | aoe_enemy | Neutral | A wide arcing swing that strikes every enemy in front of you. |
| `iron_stance` | Iron Stance | 3 | 40 | 30 | 30000 | 0 | self_buff | Earth | Root yourself in the earth: immune to knockback, +50% DEF, movement halved. |
| `aegis_of_the_legion` | Aegis of the Legion | 3 | 55 | 45 | 45000 | 0 | party_buff | Holy | Extend the Legion's oath over your party, granting every ally a damage shield. |

### 1.3 Spellweaver — *Elemental Ranged DPS*, magic, all elements

| id | Name | Tier | Lv | SP | CD | Mult | Target | Element | Description |
|---|---|---|---|---|---|---|---|---|---|
| `fireball` *(existing)* | Fireball | 1 | 1 | 15 | 2000 | 3.0 | aoe_enemy | Fire | Hurl an exploding ball of fire dealing high elemental damage. |
| `frost_lance` | Frost Lance | 1 | 8 | 13 | 1800 | 2.6 | single_enemy | Water | Impale a single target on a spear of ice, slowing its movement. |
| `chain_lightning` | Chain Lightning | 2 | 18 | 24 | 4000 | 2.4 | aoe_enemy | Wind | Loose an arc that leaps between up to four enemies, weakening with each jump. |
| `arcane_siphon` | Arcane Siphon | 2 | 28 | 18 | 8000 | 1.8 | single_enemy | Neutral | Drain a target's essence, converting a portion of the damage dealt into SP. |
| `mana_shield` | Mana Shield | 3 | 40 | 35 | 20000 | 0 | self_buff | Neutral | Spend SP instead of HP for incoming damage until your reserves run dry. |
| `meteor_fall` | Meteor Fall | 3 | 55 | 60 | 15000 | 6.5 | aoe_enemy | Fire | Call down burning stone across a wide area. The Spire's signature, stolen. |

### 1.4 Shadowblade — *Agile Assassin*, physical, Shadow & Poison

*(Had **zero** skills before this document — `DESIGN_AUDIT.md` §1.3.)*

| id | Name | Tier | Lv | SP | CD | Mult | Target | Element | Description |
|---|---|---|---|---|---|---|---|---|---|
| `venom_edge` | Venom Edge | 1 | 1 | 7 | 1000 | 1.9 | single_enemy | Poison | Coat both blades and strike, leaving a wound that bleeds venom over time. |
| `shadow_step` | Shadow Step | 1 | 8 | 12 | 5000 | 1.6 | single_enemy | Shadow | Vanish and reappear behind your target, striking before they turn. |
| `fan_of_blades` | Fan of Blades | 2 | 18 | 20 | 3000 | 2.3 | aoe_enemy | Neutral | Spin through a crowd, cutting everything within a dagger's reach. |
| `cloak_of_dusk` | Cloak of Dusk | 2 | 28 | 25 | 18000 | 0 | self_buff | Shadow | Fade from sight. Your next strike from concealment is a guaranteed critical. |
| `exploit_weakness` | Exploit Weakness | 3 | 40 | 22 | 9000 | 3.4 | single_enemy | Neutral | Read the gap in their guard and put a blade through it. Ignores most DEF. |
| `thousand_cuts` | Thousand Cuts | 3 | 55 | 48 | 25000 | 7.0 | single_enemy | Shadow | An unbroken flurry. Damage scales with how long you remain unhit. |

### 1.5 Cleric — *Support / Healer*, magic, Holy

| id | Name | Tier | Lv | SP | CD | Mult | Target | Element | Description |
|---|---|---|---|---|---|---|---|---|---|
| `heal` *(existing)* | Heal | 1 | 1 | 12 | 1500 | 2.5 | ally_heal | Holy | Restore target ally's HP based on INT stat. |
| `holy_light` | Holy Light | 1 | 8 | 14 | 1800 | 2.7 | single_enemy | Holy | A lance of Aetherite light. Devastating against the returned dead. |
| `sanctuary_ward` | Sanctuary Ward | 2 | 18 | 26 | 15000 | 1.4 | party_buff | Holy | Consecrate the ground beneath your party, healing all who stand within it. |
| `purge_affliction` | Purge Affliction | 2 | 28 | 16 | 6000 | 0 | ally_single | Holy | Burn poison, curse, and freeze out of an ally in a single searing moment. |
| `blessing_of_valor` | Blessing of Valor | 3 | 40 | 34 | 30000 | 0 | party_buff | Holy | The Order's oath made manifest: +ATK, +HIT and +MDEF for the whole party. |
| `resurrection_rite` | Resurrection Rite | 3 | 55 | 70 | 60000 | 0 | ally_single | Holy | The rite performed in the High Temple, spoken over the fallen where they lie. |

### 1.6 Ranger — *Marksman / Trapper*, physical, Wind & Earth

*(Also had **zero** skills before this document.)*

| id | Name | Tier | Lv | SP | CD | Mult | Target | Element | Description |
|---|---|---|---|---|---|---|---|---|---|
| `piercing_shot` | Piercing Shot | 1 | 1 | 9 | 1300 | 2.4 | single_enemy | Neutral | A drawn-through shot that punches past armour and out the other side. |
| `snare_trap` | Snare Trap | 1 | 8 | 11 | 7000 | 1.2 | ground_trap | Earth | Set a hidden snare. The first thing to cross it is held fast and bleeding. |
| `volley_of_thorns` | Volley of Thorns | 2 | 18 | 21 | 3200 | 2.5 | aoe_enemy | Earth | Loose a spread of barbed shafts across a cone of ground. |
| `hawk_eye` | Hawk Eye | 2 | 28 | 18 | 20000 | 0 | self_buff | Wind | Steady the breath and the wind. Greatly increased range, HIT and critical rate. |
| `beast_bond` | Beast Bond | 3 | 40 | 40 | 45000 | 2.0 | self_buff | Wind | Call the hawk that has been following you since the Corps took you in. |
| `rain_of_arrows` | Rain of Arrows | 3 | 55 | 55 | 18000 | 5.8 | aoe_enemy | Wind | Empty the quiver skyward. Everything in the marked ground is under it. |

---

## 2. Equipment slot system

### 2.1 Five slots

| Slot | `slot` value | `type` value | Primary stat | Notes |
|---|---|---|---|---|
| Weapon | `weapon` | `weapon` | `atk` or `matk` | one per character; drives the ATK/MATK formula |
| Shield | `shield` | `shield` | `def`, `mdef` | Vanguard/Cleric only; conflicts with two-handed weapons |
| Armor | `armor` | `armor` | `def`, `hp` | body slot |
| Headgear | `headgear` | `headgear` | `def`, small stat riders | the RO cosmetic-identity slot |
| Accessory | `accessory` | `accessory` | stat riders, `element` | two slots eventually; **one** in Phase 3 |

### 2.2 Schema

Existing fields (**must not change** — `db_editor.html:641-676` binds all of them):
`id`, `name`, `type`, `price`, `atk`, `matk`, `def`, `healHp`, `icon`

Additive fields:
```jsonc
{
  "slot": "headgear",       // weapon|shield|armor|headgear|accessory|null (consumables)
  "reqLevel": 30,
  "element": "Fire",        // weapons: attack element. armor/accessory: defence element. null = Neutral
  "mdef": 8,
  "twoHanded": false,
  "bonus": { "str": 2, "agi": 0, "vit": 0, "int": 0, "dex": 3, "luk": 0, "crit": 5, "flee": 0 },
  "healSp": 0,
  "tier": 3,                // 1..6, matches the level band
  "source": "spire"         // zone id, or "shop" / "craft"
}
```

**Compatibility note:** `type` keeps carrying the same string as `slot` for equipment so the existing editor dropdown still classifies items correctly; `slot` is the field the future paperdoll binds to. Consumables keep `type: "consumable"` and `slot: null`.

### 2.3 Progression tiers

Six tiers pinned to the realm bands, so every realm has a visible gear reward:

| Tier | Level band | Realm | Weapon ATK | Armor DEF |
|---|---|---|---|---|
| 1 | 1–15 | Meadows / town shop | 8–20 | 4–10 |
| 2 | 15–30 | Sunken Sanctum | 25–40 | 12–20 |
| 3 | 30–50 | Obsidian Spire | 45–70 | 22–34 |
| 4 | 50–70 | Glacial Chasm | 75–105 | 36–50 |
| 5 | 70–90 | Umbral Rootways | 110–150 | 52–70 |
| 6 | 90–99 | Verrocaine drops | 160–200 | 72–90 |

The three existing items slot in as: `red_potion` (consumable), `mythril_armor` → tier 2 armor, `dragon_lance` → tier 3 weapon. **No existing stats are changed** — only `slot`/`reqLevel`/`element` are added, and `mythril_armor`'s placeholder crystal icon is retargeted to a real armor icon (`DESIGN_AUDIT.md` §2E).

---

## 3. Item roster — 25 entries (3 existing + 22 new)

### 3.1 Consumables (5)

| id | Name | Price | Effect | Tier | Icon |
|---|---|---|---|---|---|
| `red_potion` *(existing)* | Red Potion | 50 | `healHp` 100 | 1 | `potion_health_ff.png` |
| `blue_potion` | Blue Potion | 80 | `healSp` 60 | 1 | `potion_mana_ff.png` **NEW** |
| `meadow_bread` | Meadow Bread | 25 | `healHp` 45, cheap field food | 1 | `food_bread_ff.png` **NEW** |
| `aetherite_draught` | Aetherite Draught | 900 | `healHp` 800, `healSp` 300 | 4 | `potion_aetherite_ff.png` **NEW** |
| `thawstone` | Thawstone | — | quest key; melts on a timer (`WORLD_MAP_EXPANSION.md` §6.5) | 4 | `key_thawstone_ff.png` **NEW** |

### 3.2 Weapons (7)

| id | Name | Slot | Lv | Price | ATK | MATK | Element | Tier | Source | Icon |
|---|---|---|---|---|---|---|---|---|---|---|
| `bellflower_shortsword` | Bellflower Shortsword | weapon | 1 | 90 | 14 | 0 | Neutral | 1 | shop | `wpn_shortsword_ff.png` **NEW** |
| `snagtooth_cleaver` | Snagtooth Cleaver | weapon | 12 | 260 | 22 | 0 | Neutral | 1 | meadows | `wpn_cleaver_ff.png` **NEW** |
| `tidebreak_trident` | Tidebreak Trident | weapon | 22 | 700 | 38 | 0 | Water | 2 | sanctum | `wpn_trident_ff.png` **NEW** |
| `dragon_lance` *(existing)* | Dragon Lance | weapon | 34 | 600 | 35 | 0 | Neutral | 3 | shop | `excalibur_ff.png` ⚠️ placeholder |
| `emberglass_edge` | Emberglass Edge | weapon | 40 | 1800 | 62 | 0 | Fire | 3 | spire | `wpn_emberglass_ff.png` **NEW** |
| `hoarfrost_longbow` | Hoarfrost Longbow | weapon | 58 | 4200 | 92 | 0 | Water | 4 | chasm | `wpn_longbow_ff.png` **NEW** |
| `rootfang_staff` | Rootfang Staff | weapon | 76 | 9500 | 30 | 118 | Shadow | 5 | rootways | `wpn_staff_root_ff.png` **NEW** |

### 3.3 Shields (3)

| id | Name | Lv | Price | DEF | MDEF | Element | Tier | Source | Icon |
|---|---|---|---|---|---|---|---|---|---|
| `oaken_targe` | Oaken Targe | 5 | 120 | 6 | 2 | Earth | 1 | shop | `shd_targe_ff.png` **NEW** |
| `nave_aegis` | Nave Aegis | 26 | 850 | 18 | 10 | Water | 2 | sanctum | `shd_aegis_ff.png` **NEW** |
| `forgewrought_bulwark` | Forgewrought Bulwark | 46 | 3600 | 34 | 14 | Fire | 3 | spire | `shd_bulwark_ff.png` **NEW** |

### 3.4 Armor (4)

| id | Name | Lv | Price | DEF | MDEF | Element | Tier | Source | Icon |
|---|---|---|---|---|---|---|---|---|---|
| `travellers_jerkin` | Traveller's Jerkin | 1 | 70 | 5 | 1 | Neutral | 1 | shop | `arm_jerkin_ff.png` **NEW** |
| `mythril_armor` *(existing)* | Mythril Armor | 20 | 300 | 15 | 5 | Neutral | 2 | shop | `arm_mythril_ff.png` **NEW** *(retargeted from `prop_crystal_save.png`)* |
| `slagworks_plate` | Slagworks Plate | 44 | 3200 | 32 | 10 | Fire | 3 | spire | `arm_slagplate_ff.png` **NEW** |
| `umbral_shroud` | Umbral Shroud | 74 | 11000 | 58 | 40 | Shadow | 5 | rootways | `arm_shroud_ff.png` **NEW** |

### 3.5 Headgear (3)

| id | Name | Lv | Price | DEF | Bonus | Element | Tier | Source | Icon |
|---|---|---|---|---|---|---|---|---|---|
| `militia_kettle_helm` | Militia Kettle Helm | 3 | 60 | 4 | VIT +1 | Neutral | 1 | shop | `hat_kettle_ff.png` **NEW** |
| `coral_circlet` | Coral Circlet | 27 | 1100 | 9 | INT +3 | Water | 2 | sanctum | `hat_circlet_ff.png` **NEW** |
| `aurora_diadem` | Aurora Diadem | 64 | 7800 | 22 | INT +6, MDEF +18 | Holy | 4 | chasm | `hat_diadem_ff.png` **NEW** |

### 3.6 Accessories (3)

| id | Name | Lv | Price | Bonus | Element | Tier | Source | Icon |
|---|---|---|---|---|---|---|---|---|---|
| `hedgerow_charm` | Hedgerow Charm | 6 | 150 | LUK +2, FLEE +5 | Earth | 1 | meadows | `acc_charm_ff.png` **NEW** |
| `glasslight_pendant` | Glasslight Pendant | 24 | 1400 | INT +4, MDEF +8 | Holy | 2 | sanctum *(Reliquary secret)* | `acc_pendant_ff.png` **NEW** |
| `sovereigns_signet` | Sovereign's Signet | 90 | 40000 | STR +8, DEX +8, CRIT +15 | Shadow | 6 | rootways *(Verrocaine)* | `acc_signet_ff.png` **NEW** |

**Totals:** 5 consumable + 7 weapon + 3 shield + 4 armor + 3 headgear + 3 accessory = **25 items**, 22 of them new, 23 new icon files required (`dragon_lance` keeps its placeholder pending a lance redraw; `red_potion` is done).

---

## 4. Class notes

No class stats change in this pass. Two follow-ups recorded as open questions (`DESIGN_AUDIT.md` §2F):

- **Ranger sprite mismatch** — `hero_redmage.png` reads as a caster. `hero_dragoon.png` exists unused and reads far closer to a Ranger Corps marksman. Recommend swapping.
- **`hero_monk.png` is orphaned** — a sixth class (Monk / Warden, unarmed, Earth-element bruiser) is already half-funded by existing art. Deliberately **not** designed here; flagged for Phase 4 so Phase 3 ships five complete classes rather than six thin ones.

---

## 5. Formula integration

The elemental table (`BESTIARY_EXPANSION.md` §1.1) slots into the existing `DATABASE_REGISTRY.md` formulas as a final multiplier:

```
finalDamage = baseDamage × skillMultiplier × elementModifier[atkElement][defElement]
```

where `atkElement` is the skill's `element` if the skill has one, otherwise the equipped weapon's `element`, otherwise `Neutral`; and `defElement` is the target monster's `element`.

Two formula gaps from `DESIGN_AUDIT.md` §2H remain open and are **not** resolved here — monsters still carry no `flee`/`hit`, so the HIT/FLEE formulas cannot yet be evaluated against them. Tracked as an open question.
