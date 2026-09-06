# UI Skill Tree & Paperdoll Report (Phase 3.5 / 3.6)

**Client:** `web/index.html`  
**Data:** `web/zaggers_database.json` (30 skills, 25 items, `equipSlots`)  
**Status:** Playable skill tree + paperdoll shipped additively on the live RO-style HUD.

---

## Controls

| Input | Action |
|---|---|
| **K** / Skills button | Toggle skill tree window |
| **I** / Equip button | Toggle equipment paperdoll + inventory |
| **S** | Shop (now populated from DB items) |
| **C** | Character stats |
| **F1–F9** | Cast skill bound to hotbar slot |
| Hotbar click | Same as F-key for that slot |
| Space / J | Basic attack (unchanged) |

Skill tree nodes: **Learn** spends 1 skill point when `reqLevel` + `requires` are met. **F1–F6** buttons bind a learned skill to the hotbar.

---

## Data flow

```
zaggers_database.json
        │
        ▼
ensureGameDB() ──► gameDB (memory)
        │              ▲
        │              │
        └── localStorage `zaggers_db` (cache)
        
player runtime ──► localStorage `zaggers_player_save`
  learnedSkills, skillHotbar, inventory, equipment,
  level / xp / skillPoints, base stats
```

1. Boot: `ensureGameDB()` prefers in-memory `gameDB`, then `localStorage.zaggers_db`, then `fetch('zaggers_database.json')`.
2. Classes for the creator still go through `getDbClasses()` (now backed by the same DB helpers).
3. Skills / items are read via `getDbSkills()` / `getDbItems()`.
4. Shop rebuilds from items with `source === 'shop'` or tier ≤ 2.
5. Purchases call `buyItemById` → inventory stack → Equip [I] to equip/use.
6. Combat ATK/MATK/DEF/MDEF fold in equipment `atk`/`matk`/`def`/`mdef` + `bonus` riders and active buffs.

---

## Skill tree (§3.5)

- Per-class **2–2–2** lattice from skill `tier` (rows) with two nodes per tier.
- Lock state: not learned AND (level &lt; `reqLevel` OR missing `requires` OR no points).
- Available nodes are gold-bordered; learned nodes are green.
- Level-ups (monster XP) grant +1 skill point, HP/SP growth from class `hpGrowth`/`spGrowth`.
- Hotbar shows name stub + **cooldown sweep** from `cooldownMs` (`performance.now()` ready timestamps).

### targetType behaviour

| targetType | Behaviour |
|---|---|
| `single_enemy` | Damage nearest monster in range |
| `aoe_enemy` | Damage all monsters in radius |
| `ally_heal` | Heal self (solo client) |
| `self_buff` | Timed self modifiers (dmg taken / ATK / move) |
| `party_buff` | Same as self buffs in solo; no party sync yet |
| `ally_single` | Purge / rite heal on self (safe stubs) |
| `ground_trap` | Places a temporary ground hazard marker; first monster to enter is damaged + slowed |

Unknown types fail soft (floating text, no throw).

---

## Equipment paperdoll (§3.6)

- Five slots: **Weapon, Shield, Armor, Headgear, Accessory** bound to item `slot`.
- **`twoHanded` weapon** unequips shield and locks the shield slot until the 2H weapon is removed.
- Inventory lists stacks; Equip / Use (consumables with `healHp`/`healSp`).
- Stat line shows live ATK / MATK / DEF / MDEF including gear.
- Item icons: `assets/sprites_ff/{icon}` when the file exists (`onerror` hides broken images → name text remains). Task C icons (`wpn_*`, `shd_*`, `arm_*`, `hat_*`, `acc_*`, potions/food/key) are on disk via `scripts/generate_item_icons.py` — all 25 `items[].icon` paths resolve.

---

## Persistence

- `localStorage.zaggers_player_save` stores class, level, XP, skill points, learned skills, hotbar, inventory, equipment, and core stats on learn/equip/buy/level-up.
- `loadPlayerState()` exists for resume wiring; character creator still starts a fresh kit on confirm (does not auto-load mid-creator).

---

## Known limitations

1. **No multiplayer party** — `party_buff` / `ally_*` apply to the local player only.
2. **Element matrix** not applied in skill damage yet (Phase 3.1); skills use physical/magic base × multiplier.
3. **Item icon art** for most gear is still missing under `web/assets/sprites_ff/` (Task C).
4. **Monster drop → inventory** not wired (roadmap §3.6 drop tables still pending).
5. **Skill points** only from level-up (1 at create + 1 per level); no job-level split.
6. **Buff UX** is combat-effect only (no buff icon strip).
7. Must serve `web/` over HTTP so `fetch('zaggers_database.json')` succeeds; file:// will fall back to empty skills unless `localStorage.zaggers_db` was seeded by the DB editor.

---

## Files touched

- `web/index.html` — HUD CSS/HTML, DB helpers, skill tree, hotbar, paperdoll, shop wiring, combat hooks, XP.
- `vault/UI_SKILL_PAPERDOLL_REPORT.md` — this document.
