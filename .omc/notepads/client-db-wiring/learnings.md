# Learnings — Client DB Wiring

- Serve from `web/`; relative `fetch('zaggers_database.json')` 404s on `file://` and must show `#db-fail-banner`.
- Boot must `await` DB before `loadZoneMap` or `enrichMonsterFromDB` runs with empty indexes.
- DB sprites use `.png` suffix; map sprites do not — normalize with `assetKey` / `normalizeSpriteKey`.
- Skill `damageType` in schema v2 is `magic` (not `magical`); accept both in combat math.
- Basic attack and `castSkill` must share one elemental path (`applyMonsterHit`) or affinity UI never appears.
- Keep `localStorage.zaggers_db` sync so `db_editor.html` and the client share one schema without renames.
