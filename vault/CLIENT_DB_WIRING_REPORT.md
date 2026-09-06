# Client DB Wiring Report

**Date:** 2026-09-06  
**Target:** `web/index.html` + `web/zaggers_database.json`  
**Implements:** `ROADMAP.md` §3.0 (client wiring) and §3.1 (elemental combat core)

---

## Summary

The live web client now boots against `zaggers_database.json` instead of treating the DB as editor-only data. Classes, skills, shop items, and monster metadata are resolved from `gameDB`. Combat applies the elemental modifier table from `gameDB.elements.modifiers`.

---

## What changed (`web/index.html`)

### Boot / `gameDB`
- `fetch('zaggers_database.json')` via `ensureGameDB()` / `loadGameDatabase()` at `DOMContentLoaded`.
- On HTTP failure: `console.error` + on-screen `#db-fail-banner`.
- Successful load syncs to `localStorage.zaggers_db` (keeps `db_editor.html` path working; **no field renames**).
- Zone load (`loadZoneMap('aethelgard')`) waits for DB so monster enrichment sees indexes.

### Classes
- Character creator / spawn stats / sprites come from `getDbClasses()` → `gameDB.classes` (fallback only if fetch+storage miss).
- Sprite keys normalized (strip `.png`) before `sprites{}` lookup.
- `player.classId` set on create; starter `reqLevel <= 1` skills auto-learned and bound to F-keys.

### Skills / hotbar
- Skill tree (`K`) draws from `gameDB.skills` filtered by `classId`, gated by `reqLevel` / `requires` / skill points.
- Hotbar F1–F9 casts via `castSkill`, spending `spCost` and applying `cooldownMs`.
- Damage skills use DB `multiplier`, `targetType`, `element`, `damageType`.

### Shop / items
- Shop list rebuilt by `populateShopFromDB()` from `gameDB.items` (`source === 'shop'` / low-tier stock), respecting `reqLevel` and showing `slot` / element / bonuses.
- Purchases go to inventory; Equip (`I`) paperdoll binds `slot` including `twoHanded` shield lockout.
- Weapon `element` feeds attack-element resolution.

### Monsters
- On zone/custom map load, each spawn is `enrichMonsterFromDB()`-merged by sprite/id: `name`, `element`, `rank`, `level`, `drops`, atk/def/zeny/exp when present.
- Nameplates show element label + tint from `gameDB.elements.colors`.

### Elemental combat
- `finalDamage = base × skillMultiplier × elements.modifiers[atk][def]`
- Attack element: `skill.element` → equipped weapon `element` → `Neutral`
- Floating numbers append affinity marker (`Fire▲` / `Water▼`) and recolor when modifier ≠ 1.0
- Basic attack (`Space`/`J`) and skill hits share `applyMonsterHit` / `calcCombatDamage`

### Preserved
- `MAP_REGISTRY`, exits, `subRegions`, map loading path unchanged in behavior.
- `db_editor.html` still reads/writes the same JSON schema keys.

---

## Verification

- `web/zaggers_database.json` present next to `index.html` (correct relative fetch path when serving `web/`).
- HTML tag balance: OK (script/style stripped structural check).
- JS `{`/`}` balance: 0.
- No leftover `console.log` / `TODO` / `HACK` / `debugger` in `index.html`.

**How to run locally:** serve the `web/` directory over HTTP (e.g. `python -m http.server` from `web/`), then open `/index.html`. Opening the file via `file://` will 404 the DB fetch and show the fail banner.

---

## Known follow-ups (out of this pass)
- Full skill-tree UX polish / more targetType VFX.
- Trap ticks could re-roll elemental mod vs each monster instead of cached Neutral roll.
- Deduplicate overlapping helpers (`loadGameDatabase` vs `ensureGameDB`, `assetKey` vs `normalizeSpriteKey`) in a later cleanup.
