# Learnings — Skill Tree + Paperdoll

- Live client is a single `web/index.html`; additive HUD panels are safer than rewriting combat/movement.
- `getDbClasses()` previously only read localStorage; skill/item UI needs `ensureGameDB()` fetch of `zaggers_database.json` (HTTP required).
- DB class sprites include `.png` suffix; normalize before looking up `sprites{}` keys.
- Shop `#shop-window` was missing a closing `</div>` (NPC dialog nested inside) — fixed while adding panels.
- Hotbar must not rebuild DOM every frame; only update cooldown sweep heights.
- Most gear icons (`wpn_*`, `shd_*`, `arm_*`) are not on disk yet; use text + optional `onerror`-hidden img.
- `party_buff` / `ally_*` can only affect self until multiplayer exists; keep stubs non-throwing.
