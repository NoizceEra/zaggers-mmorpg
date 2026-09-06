# DESIGN AUDIT — Zaggers (Phase 2 → Phase 3 gate)

**Audited:** 2026-09-06
**Scope:** `vault/*.md`, `web/zaggers_database.json`, `web/db_editor.html` (consumer), `web/index.html` (consumer), `web/editor.html` (map format), `web/assets/`
**Verdict:** The *engine* is ahead of the *content*. Phase 1 and 2 shipped a competent renderer, editor and schema, but the data layer behind them is a placeholder that cannot support the exploration loop the roadmap promises. Phase 3 should not start as "build 4 dungeons" — it should start as "author a world worth walking through."

---

## 1. Critical gaps

### 1.1 The bestiary cannot fill the world
Four monsters exist in the database (`slime_green`, `goblin_raider`, `skeleton_warrior`, `lord_baphomet`). Six sprites exist on disk (adds `cactuar_ff`, `bomb_ff`). Five zones span levels 1–99.

- **Levels 30–70 have zero monster entries.** `zones[]` names *Fire Bomb, Lava Golem, Frost Lich, Snow Specter* as inhabitants, but none of those ids exist in `monsters{}`. The zone table is advertising content that isn't there.
- **Whispering Meadows lists "Horn Hornet"** — also not in the database. The `zones[].monsters` string and the `monsters{}` map have already drifted apart, and nothing validates them against each other.
- At the current density a player clears the entire visual variety of the game in roughly ninety seconds.

### 1.2 Names are borrowed, not owned
`slime_green`, `goblin`, `skeleton`, `cactuar`, `bomb`, `baphomet` are, in order, a genre generic and four direct lifts from Final Fantasy and Ragnarok Online. This is fine as programmer-art shorthand; it is not fine as a shipping identity, and it makes the project legally and tonally derivative rather than *inspired by*. The sprites themselves are mostly fine — it is the naming layer that needs to be replaced. Rename first, before quest text, item names and drop tables harden around the placeholders. **See `BESTIARY_EXPANSION.md` §7 for the mapping table.**

### 1.3 Three skills for five classes
`skills{}` contains `bash`, `fireball`, `heal`. Shadowblade and Ranger — two of the five advertised classes — have **no skills at all**. A player who picks Shadowblade at character creation currently gets an empty hotbar. The roadmap's "Skill Tree Visualizer (F1–F9)" is a UI for content that does not exist; the tree needs ~6 nodes per class before the visualizer is worth building.

### 1.4 No elemental system despite the lore requiring one
`WORLD_LORE.md` is built on elements: the Great Shattering created "five distinct elemental microclimates," the Spellweaver Syndicate is defined as "masters of elemental magic (Fire, Ice, Lightning, Arcane)," and every zone has an elemental theme (meadow/water/fire/ice/shadow). Yet:
- No `element` field on monsters.
- No `element` field on skills or weapons.
- No damage modifier table anywhere.
- The Spellweaver's one skill, `fireball`, is mechanically identical to a bigger `bash` — a flat `multiplier` with no elemental interaction.

The zones were *designed* around elements. The data model forgot to implement them. This is the single highest-leverage missing system: it retroactively gives meaning to zone choice, gear choice, party composition and the entire monster roster.

### 1.5 Equipment is three items and no slots
`items{}` holds one potion, one armor, one weapon. `ROADMAP.md` Phase 3 promises an "Equipment Paperdoll (Weapon, Armor, Shield, Headgear, Accessory)" — but the item schema has no `slot` field, so there is nothing for a paperdoll to bind to. There is also no progression: `mythril_armor` (DEF 15) and `dragon_lance` (ATK 35) have no tier below or above them. A level 70 player and a level 5 player shop from the same three rows.

### 1.6 No quests, no NPCs in data, no questlines
`npc_kafra`, `npc_blacksmith`, `npc_merchant`, `npc_elder` exist as sprites and can be stamped in `editor.html`. They exist nowhere in `zaggers_database.json` — no `npcs{}` collection, no dialogue, no `quests{}` collection. Roadmap Phase 3 says "interactive NPC questlines" as a single unchecked box covering what is realistically the largest content system in the game.

### 1.7 Aethelgard has landmarks but no layout
`WORLD_LORE.md` names four landmarks (Fountain Plaza, Kafra Depot, Obsidian Smithy, High Temple). It does not say where any of them are relative to each other, how big the town is, where players spawn, where the exits to each realm are, or what the walking distance between the bank and the shop feels like. A social hub is a *floorplan* problem, not a landmark list. `editor.html` defaults to a 30×30 grid; the roadmap says 64×64. Nothing reconciles them.

### 1.8 Zones are flat, not explorable
Each realm is a single row in a five-row table: one id, one level range, one light colour. There is no reason to walk to the far corner of Whispering Meadows — every tile of it is level 1–15 and contains the same two monsters. Exploration MMOs are built out of *sub-regions with differential reward*: a hidden grove, a shortcut, a vista, an elite camp, a gathering cluster. None of that structure is expressible in the current `zones[]` schema.

---

## 2. Consistency and schema issues

| # | Issue | Detail |
|---|---|---|
| A | `zones[].monsters` is a **display string**, not a reference | `db_editor.html:750` renders it directly into a `<td>`. It cannot be used as a join key, and it is already out of sync (§1.1). Any structured monster→zone relationship must live in a *new* field; this one must stay a string for backward compatibility. |
| B | `drops` documented but absent | `DATABASE_REGISTRY.md` §4 shows a `drops` array on `slime_green`. The live JSON has no `drops` on any monster. Registry and data disagree. |
| C | `aggro` live but undocumented | Every monster carries `aggro` (`passive`/`aggressive`/`boss`). `DATABASE_REGISTRY.md` §4 does not mention it. |
| D | `index.html` ignores the database entirely | Hero classes are hardcoded at `index.html:878` as `HERO_CLASSES`. The game client never fetches `zaggers_database.json`; only `db_editor.html` reads it. **The database is currently a design document that pretends to be runtime data.** Wiring the client to the JSON is a prerequisite for the whole of Phase 3. |
| E | Placeholder icons | `mythril_armor.icon` is `prop_crystal_save.png` — a save-point crystal standing in for body armour. `dragon_lance.icon` is `excalibur_ff.png`, a sword sprite on a lance. |
| F | Class sprite mismatch | The Ranger uses `hero_redmage.png`; a red mage reads as a caster, not a marksman. `hero_dragoon.png` and `hero_monk.png` exist on disk and are wired to no class at all. |
| G | Two asset trees | `assets/sprites_ff/` and `web/assets/sprites_ff/` both exist with overlapping contents, plus Godot `.import` sidecars in a web project. Ambiguous source of truth for the art pipeline. |
| H | Stat formulas unvalidated | `DATABASE_REGISTRY.md` gives eight formulas (HP, SP, ATK, MATK, DEF, FLEE, HIT, CRIT). None reference `BaseHP`/`BaseSP` values that exist anywhere in the data, and no monster carries `flee`/`hit`, so hit chance cannot be resolved against monsters at all. |
| I | Boss level unrepresentable | `lord_baphomet` has no `level` field; the Realm of Baphomet is "70+" with no upper bound and no other inhabitants. |

---

## 3. Tonal notes

The RO + FF6 blend is working where it has been executed. `WORLD_LORE.md`'s atmosphere lines ("ash falls, heavy percussive battle drums") are the right register — sensory, short, evocative. Keep that voice.

Two drifts to correct:
- **"Zeny"** is a Ragnarok Online currency term used verbatim. Keep or rename deliberately; do not leave it as an accident. *(This audit recommends keeping it — it is genre furniture at this point, unlike a named demon lord.)*
- **`Kafra`** is likewise a direct RO lift and is baked into `npc_kafra.png`, the lore doc and the roadmap. Recommend renaming the *service* while reusing the sprite.

---

## 4. What Phase 3 should actually contain

Ordered by leverage, highest first:

1. **Wire `index.html` to `zaggers_database.json`** (issue D). Until this happens, every hour of data authoring is speculative.
2. **Adopt an elemental system** (§1.4) — it is the cheapest change with the widest downstream effect.
3. **Rename and expand the bestiary** (§1.1, §1.2) — 54 monsters, own identity, elements assigned. → `BESTIARY_EXPANSION.md`
4. **Sub-region the world** (§1.8) and floorplan Aethelgard (§1.7). → `WORLD_MAP_EXPANSION.md`
5. **Skills to ~30, equipment slots + ~25 items** (§1.3, §1.5). → `CLASS_SKILL_ITEM_EXPANSION.md`
6. **Then** build the skill-tree visualizer and paperdoll UI — they are now views over real data.
7. Quests/NPC data model: **deferred**, but the sub-region doc seeds quest hooks so it is not designed in a vacuum. *(Tracked in `open-questions`.)*

---

## 5. Deliberately out of scope for this audit

- Combat tuning / TTK balance passes (needs the client wired to the DB first).
- Multiplayer, guild war, crafting — Phase 4.
- The Godot branch (`scenes/`, `scripts/`, `project.godot`) — the web client is the live target.
