# Open Questions

## Zaggers Phase 3 World & Data Expansion - 2026-09-06

### Naming / identity
- [ ] Keep `zeny` as the currency name, or rename it? — It is a direct Ragnarok Online term. The audit recommends keeping it (genre furniture), but it should be a decision, not an accident. `DESIGN_AUDIT.md` §3
- [ ] Confirm the "Kafra" → **Kestrel Consignment House** rename. — Baked into `npc_kafra.png`, `WORLD_LORE.md` and `ROADMAP.md`; renaming touches all three. Sprite is reused either way.
- [ ] Approve the three recommended sprite redraws (Pricklespine, Cinderpuff, Verrocaine). — Their current silhouettes are recognisable FF/RO lifts; the renames alone do not fix that. `BESTIARY_EXPANSION.md` §9

### Systems not yet designed
- [ ] Quest + NPC data model (`quests{}`, `npcs{}`). — Deferred out of Phase 3, but it is the largest remaining content system and the sub-regions already seed hooks for it. Designing it late risks reworking zone data.
- [ ] Do vistas grant a **persistent** world-map reveal or a temporary buff? — Persistent requires a player-flags/progress system that does not exist yet. Affects 3 sub-regions.
- [ ] Are the four transit stubs separate maps, or edge-triggers on the 64×64 town map? — Changes the map count for Phase 3.4 by four.
- [ ] Instanced vs. open-world boss chambers. — Phase 4 multiplayer will force this; deciding now avoids re-authoring the five boss sub-regions.

### Schema / formula gaps
- [ ] Monsters carry no `flee` / `hit`, so the HIT and FLEE formulas in `DATABASE_REGISTRY.md` cannot be evaluated against them. — Combat accuracy is currently undefined. `DESIGN_AUDIT.md` §2H
- [ ] `DATABASE_REGISTRY.md` references `BaseHP` / `BaseSP` constants that exist nowhere in the data. — Max HP/SP are not actually computable as specified.
- [ ] Two asset trees (`assets/` and `web/assets/`) with overlapping contents plus Godot `.import` sidecars. — Ambiguous source of truth; blocks a clean art handoff. Is the Godot branch retired? `DESIGN_AUDIT.md` §2G
- [ ] Accessory slot count — one in Phase 3, two later? — Affects the paperdoll layout if changed after the UI is built.

### Class roster
- [ ] Ranger sprite: swap `hero_redmage.png` → `hero_dragoon.png`? — The red mage reads as a caster, not a marksman; the dragoon sheet already exists unused. `DESIGN_AUDIT.md` §2F
- [ ] Sixth class (Monk / Warden) using the orphaned `hero_monk.png`? — Deliberately deferred to Phase 4 so Phase 3 ships five complete classes rather than six thin ones. `CLASS_SKILL_ITEM_EXPANSION.md` §4
