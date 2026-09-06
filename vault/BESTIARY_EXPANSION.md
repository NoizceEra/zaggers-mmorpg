# BESTIARY EXPANSION — The Creatures of Zaggers

**Status:** Design spec for Phase 3. Companion to `WORLD_MAP_EXPANSION.md`.
**Implements:** `DESIGN_AUDIT.md` §1.1 (roster too thin), §1.2 (names borrowed), §1.4 (no elemental system).
**Total roster:** 54 entries — 4 tutorial, 35 realm regulars, 10 elite/rare, 5 bosses.

---

## 1. The Elemental System

The Great Shattering split the world into elemental microclimates (`WORLD_LORE.md`). Nine elements, chosen so that each of the five realms has a signature and the Holy/Shadow/Undead triangle carries the endgame.

| Element | Symbol colour | Realm signature | Reads as |
|---|---|---|---|
| **Neutral** | `#bdbdbd` | — (town, beasts, bandits) | no affinity; the default |
| **Earth** | `#8d6e63` | Whispering Meadows | stone, root, chitin, growth |
| **Wind** | `#aed581` | (secondary, all realms) | flight, speed, air, sound |
| **Water** | `#4fc3f7` | Sunken Sanctum, Glacial Chasm | flood, ice, tide, cold |
| **Fire** | `#ff7043` | Obsidian Spire | flame, ash, magma, forge |
| **Poison** | `#9ccc65` | Umbral Rootways (secondary) | rot, sap, spore, venom |
| **Shadow** | `#7e57c2` | Umbral Rootways | umbral, void, the Sovereign |
| **Holy** | `#fff59d` | (rare, all realms) | Aetherite, aurora, the Temple |
| **Undead** | `#90a4ae` | (cross-realm) | the returned; *a state, not a place* |

**Element ≠ zone.** Every realm carries a signature element for ~60% of its roster, with the rest deliberately off-theme so no zone can be cleared with a single elemental weapon. Holy and Undead are seeded across all five realms for exactly this reason.

### 1.1 Damage modifier table

Rows = **attacking** element, columns = **defending** element. Value multiplies final damage.

|  ATK ↓ / DEF → | Neutral | Earth | Wind | Water | Fire | Poison | Shadow | Holy | Undead |
|---|---|---|---|---|---|---|---|---|---|
| **Neutral** | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.75 | 1.00 | 0.75 |
| **Earth**   | 1.00 | 0.50 | **1.50** | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| **Wind**    | 1.00 | 0.50 | 0.50 | **1.50** | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| **Water**   | 1.00 | 1.00 | 1.00 | 0.50 | **1.75** | 1.00 | 1.00 | 1.00 | 1.00 |
| **Fire**    | 1.00 | **1.50** | 1.00 | 0.25 | 0.50 | **1.25** | 1.00 | 1.00 | **1.25** |
| **Poison**  | **1.25** | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 | 0.75 | 0.25 |
| **Shadow**  | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.25 | **1.75** | 0.50 |
| **Holy**    | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | **1.75** | 0.25 | **2.00** |
| **Undead**  | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.50 | 0.75 | **1.50** | 0.50 |

**Design intent baked into the numbers**
- Classic RO cycle preserved: Fire→Earth→Wind→Water→Fire.
- **Water vs Fire is 1.75** and **Fire vs Water is 0.25** — the sharpest asymmetry in the table. Bringing fire into the Sunken Sanctum should feel like a mistake.
- **Holy vs Undead 2.00** is the single largest number; it is the Cleric's entire identity payoff and the reason Undead is seeded into every realm.
- **Poison vs Poison 0.00** — poison cannot poison poison. Weeping Boughs (`WORLD_MAP_EXPANSION.md` §7.3) is unclearable by a poison build, forcing a loadout change at Lv 78.
- Neutral is never resisted below 0.75, so an unoptimised player is never hard-walled.

### 1.2 Schema

Additive fields on each monster (`db_editor.html` ignores unknown keys, so this is safe):
```jsonc
{
  "id": "cinderpuff",
  "element": "Fire",       // one of the nine
  "level": 32,             // representative level, mid-band
  "zone": "spire",         // zone id
  "rank": "normal"         // normal | elite | rare | boss
}
```

---

## 2. Naming conventions

- **ids** are `snake_case`, unique, and never contain the realm name (monsters may be reused).
- **Names** avoid the four borrowed lifts. Coinage rules for the Zaggers register: Anglo-Saxon compounding (*Hoarfrost Stalker*, *Snagtooth Raider*), archaic occupational suffixes (*-guard*, *-caller*, *-warden*, *-master*), and *-kin* / *-ling* / *-on* for creature families.
- Named uniques (elites, rares, bosses) get a **personal name plus an epithet** — *Ordwin the Palisade Tyrant* — in the FF6 boss register.
- Sprite filenames follow `<id>_ff.png` in `web/assets/sprites_ff/`.

---

## 3. Roster — Tutorial: Gatewatch Commons (Lv 1–5)

Zone `gatewatch` · element mix: Neutral/Wind/Earth · **all sprites NEW**

| id | Name | Lv | Element | Rank | Flavour |
|---|---|---|---|---|---|
| `dustmote_wisp` | Dustmote Wisp | 1–3 | Wind | normal | A knot of chaff and sunlight that drifts where the threshing was; harmless until it isn't. |
| `gutter_ratkin` | Gutter Ratkin | 1–4 | Neutral | normal | Knee-high, wearing a scrap of someone's coin-purse as a hood, entirely unimpressed by you. |
| `thatch_beetle` | Thatch Beetle | 2–5 | Earth | normal | Fat, iridescent, and eating the roof; the militia pay a copper a shell. |
| `straw_effigy` | Straw Effigy | 3–6 | Fire | rare | A scarecrow that turned to watch you. It burns beautifully, which it seems to know. |

---

## 4. Roster — Realm I: Whispering Meadows (Lv 1–16)

Zone `meadows` · signature **Earth** · boss **Ordwin the Palisade Tyrant**

| id | Name | Lv | Element | Rank | Sprite | Flavour |
|---|---|---|---|---|---|---|
| `gloopling_bellflower` | Bellflower Gloopling | 1–5 | Water | normal | **REUSE** `slime_green_ff.png` | A pint of blue meadow-water that got ideas; leaves a trail of crushed petals. |
| `bramblehop` | Bramblehop | 3–7 | Earth | normal | NEW | A hare made mostly of thorn-scrub, and it does not stop bouncing while you fight it. |
| `hornhaste_wasp` | Hornhaste Wasp | 4–8 | Wind | normal | NEW | Fist-sized, furious, and always in threes. The Downs' hedgerows hum with them. |
| `mossback_tortin` | Mossback Tortin | 7–12 | Earth | normal | NEW | A shield with legs. Two feet of moss-grown shell that has outlived four generations of raiders. |
| `fen_lurker` | Fen Lurker | 8–12 | Water | normal | NEW | You will see the reeds part before you see the Lurker. That is the only warning offered. |
| `rot_capling` | Rot Capling | 10–15 | Poison | normal | NEW | A mushroom the size of a child that walks on its own stalk and coughs spores when struck. |
| `snagtooth_raider` | Snagtooth Raider | 6–11 | Neutral | normal | **REUSE** `goblin_ff.png` | Wiry, tusked, and armed with whatever the last caravan was carrying. Never travels alone. |
| `snagtooth_warchanter` | Snagtooth Warchanter | 13–15 | Neutral | **elite** | NEW | Beats a shield-totem to a rhythm that makes the whole palisade hit harder. Kill the drum first. |
| `grovewarden_thistle` | Grovewarden Thistle | 14–16 | Earth | **rare** | NEW | The Hollowroot's keeper: a briar-and-antler shape that was standing there before the trees were. |
| `ordwin_palisade_tyrant` | **Ordwin the Palisade Tyrant** | 16 | Neutral | **BOSS** | NEW | Snagtooth chieftain in stolen Legion plate three sizes too large, and it has not slowed him down once. |

---

## 5. Roster — Realm II: Sunken Sanctum (Lv 15–32)

Zone `sanctum` · signature **Water** · boss **Hallowdeep, the Choirfall Warden**

| id | Name | Lv | Element | Rank | Sprite | Flavour |
|---|---|---|---|---|---|---|
| `drowned_marrowguard` | Drowned Marrowguard | 15–19 | Undead | normal | **REUSE** `skeleton_ff.png` | Still at its post, still in formation, four centuries after the water came in. |
| `pricklespine_thornmarch` | Thornmarch Pricklespine | 16–20 | Earth | normal | **REUSE** `cactuar_ff.png` | A bristling green thing that stands perfectly still until it is suddenly somewhere else. |
| `brinemaw_eel` | Brinemaw Eel | 18–23 | Water | normal | NEW | Six feet of muscle and hinge-jaw that lives in the flooded pews and considers them home. |
| `silt_creeper` | Silt Creeper | 19–24 | Poison | normal | NEW | It looks like sediment until the sediment reaches for your ankle. The Warrens are full of them. |
| `glasslight_mote` | Glasslight Mote | 20–25 | Holy | normal | NEW | A shard of living Aetherite light. Lead three to the braziers and the Reliquary opens. |
| `reliquary_husk` | Reliquary Husk | 23–28 | Undead | normal | NEW | A pilgrim who reached the reliquary, knelt, and never got back up — and then did. |
| `coralbound_acolyte` | Coralbound Acolyte | 25–30 | Water | normal | NEW | Robed, kneeling, and grown through with pink coral. It still tries to finish the rite. |
| `warden_of_the_nave` | Warden of the Nave | 28–30 | Undead | **elite** | NEW | Twelve feet of ceremonial armour full of black water. It patrols the transept on a schedule. |
| `pale_choirmaster` | The Pale Choirmaster | 29–31 | Holy | **rare** | NEW | Conducts nothing, in an empty nave, and the Husks all stop moving when it raises its hands. |
| `hallowdeep_warden` | **Hallowdeep, the Choirfall Warden** | 32 | Water | **BOSS** | NEW | What the Sanctum was built to contain, wearing the last warden's vestments as an apology. |

---

## 6. Roster — Realm III: Obsidian Spire (Lv 30–52)

Zone `spire` · signature **Fire** · boss **Vashkar the Spire Crown**

| id | Name | Lv | Element | Rank | Sprite | Flavour |
|---|---|---|---|---|---|---|
| `cinderpuff` | Cinderpuff | 30–35 | Fire | normal | **REUSE** `bomb_ff.png` | A grinning sphere of contained detonation that drifts closer while you decide what to do. |
| `emberglass_shard` | Emberglass Shard | 33–38 | Fire | normal | NEW | Volcanic glass that cooled into a shape with intent, and edges that have not cooled at all. |
| `ashfall_harrier` | Ashfall Harrier | 36–41 | Wind | normal | NEW | A raptor that nests in the ash column; you hear the dive a half-second before it lands. |
| `magma_hulk` | Magma Hulk | 39–45 | Fire | normal | NEW | Slag given shoulders. Slow, enormous, and it leaves the floor burning where it walked. |
| `soot_revenant` | Soot Revenant | 41–46 | Undead | normal | NEW | A foundry-hand who never clocked off, outlined in the shape of the ash that settled on him. |
| `forgewrought_sentinel` | Forgewrought Sentinel | 43–48 | Earth | normal | NEW | Built to guard the Slagworks. Nobody told it the Slagworks ended. It is still guarding. |
| `pyrelash_imp` | Pyrelash Imp | 45–50 | Fire | normal | NEW | Small, quick, and armed with a whip of live flame it clearly enjoys using. |
| `bellowmaster_grukk` | Bellowmaster Grukk | 48–50 | Fire | **elite** | NEW | Works the great bellows alone. Every pump makes the crucibles — and the Hulks — flare. |
| `the_unquenched` | The Unquenched | 49–51 | Fire | **rare** | NEW | A fire that has been burning in the Crown's hollow since before the Shattering, and resents interruption. |
| `vashkar_spire_crown` | **Vashkar the Spire Crown** | 52 | Fire | **BOSS** | NEW | The mountain's own idea of a king: obsidian, crowned, and molten at every joint. |

---

## 7. Roster — Realm IV: Glacial Chasm (Lv 50–72)

Zone `chasm` · signature **Water** · boss **Sylveth, Queen of the Silent Thaw**

| id | Name | Lv | Element | Rank | Sprite | Flavour |
|---|---|---|---|---|---|---|
| `rimewind_sprite` | Rimewind Sprite | 50–55 | Wind | normal | NEW | The blizzard, locally. It has a face for as long as you look directly at it. |
| `hoarfrost_stalker` | Hoarfrost Stalker | 52–57 | Water | normal | NEW | White on white, patient, and it has been pacing you since the second cairn. |
| `frozen_penitent` | Frozen Penitent | 54–59 | Undead | normal | NEW | One of the Statuary. Ice sloughs off it as it remembers how to kneel, then how to stand. |
| `glacier_drake_whelp` | Glacier Drake Whelp | 56–61 | Water | normal | NEW | Cat-sized, cobalt-scaled, and its breath frosts your armour solid in one pass. |
| `snowveil_shade` | Snowveil Shade | 58–63 | Shadow | normal | NEW | A shadow with nothing casting it, sliding between the statues at the edge of the lamp-light. |
| `aurora_seraphon` | Aurora Seraphon | 63–68 | Holy | normal | NEW | A ribbon of aurora folded into six wings. It circles the Shelf and does not care about you until it does. |
| `permafrost_lich` | Permafrost Lich | 65–70 | Undead | normal | NEW | Vault-keeper, ledger-keeper, and it will tell you exactly which shelf your death goes on. |
| `statuary_colossus` | Statuary Colossus | 68–70 | Water | **elite** | NEW | A hero of the old war, thirty feet of them, still frozen and no longer still. Drops the Thawstone. |
| `the_vault_keeper` | The Vault Keeper | 69–71 | Undead | **rare** | NEW | It has the only key, and it has been waiting a very long time for someone to ask politely. |
| `sylveth_silent_thaw` | **Sylveth, Queen of the Silent Thaw** | 72 | Water | **BOSS** | NEW | She stopped the blizzard once, for a heartbeat, and the silence is what people remember. |

---

## 8. Roster — Realm V: Umbral Rootways (Lv 70–99)

Zone `rootways` · signature **Shadow** · boss **Verrocaine, the Horned Sovereign**
*Formerly "Realm of Baphomet."*

| id | Name | Lv | Element | Rank | Sprite | Flavour |
|---|---|---|---|---|---|---|
| `nethergate_creeper` | Nethergate Creeper | 70–74 | Shadow | normal | NEW | Root-hair braided into a body, walking upside-down along the shaft wall beside you. |
| `umbral_houndkin` | Umbral Houndkin | 75–80 | Shadow | normal | NEW | Hunts in fours, casts no shadow of its own, and is always closer than it was. |
| `weeping_bough` | Weeping Bough | 73–78 | Poison | normal | NEW | A branch that hangs low, weeps amber, and closes when something warm passes underneath. |
| `rootfang_devourer` | Rootfang Devourer | 81–86 | Poison | normal | NEW | The mouth at the end of the root. There is nothing else to it, and nothing else is needed. |
| `hollow_penitent_choir` | Hollow Penitent Choir | 79–84 | Undead | normal | NEW | Nine hollow figures that only move while singing, and only sing while you are looking away. |
| `sanguine_thorncaller` | Sanguine Thorncaller | 77–82 | Shadow | normal | NEW | Immaculately dressed, seated on the Terrace stair, and will not rise unless you strike first. |
| `abyssal_heraldon` | Abyssal Heraldon | 84–90 | Shadow | normal | NEW | The Sovereign's messenger: horned, armoured, and it announces you before it kills you. |
| `thorncradle_warden` | Thorncradle Warden | 88–92 | Shadow | **elite** | NEW | Honour guard of the briar-bowl, drilled to the second, and it fights three of you at once. |
| `the_pale_apostate` | The Pale Apostate | 90–95 | Holy | **rare** | NEW | A Cleric of the High Temple who walked down here on purpose and is still, technically, holy. |
| `verrocaine_sovereign` | **Verrocaine, the Horned Sovereign** | 99 | Shadow | **BOSS** | **REUSE** `boss_baphomet_ff.png` | Sovereign of the abyss beneath the world tree. He has been expecting you since Aethelgard was founded. |

---

## 9. Rename mapping — existing sprites

**For the art team:** these six sprites already exist in `web/assets/sprites_ff/`. The *concepts* survive the rename; only the ids and display names change. **Do not regenerate art for these — rename the file, keep the pixels.**

| Old id | Old name | Old sprite | → New id | → New name | → New sprite filename | Concept compatible? |
|---|---|---|---|---|---|---|
| `slime_green` | Green Slime | `slime_green_ff.png` | `gloopling_bellflower` | Bellflower Gloopling | `gloopling_bellflower_ff.png` | ✅ Yes — recolour green→meadow-blue optional, not required |
| `goblin_raider` | Goblin Raider | `goblin_ff.png` | `snagtooth_raider` | Snagtooth Raider | `snagtooth_raider_ff.png` | ✅ Yes — direct reuse, add a tusk highlight if convenient |
| `skeleton_warrior` | Skeleton Warrior | `skeleton_ff.png` | `drowned_marrowguard` | Drowned Marrowguard | `drowned_marrowguard_ff.png` | ✅ Yes — add algae/waterline tint pass to sell "drowned" |
| *(sprite only, no db entry)* | Cactuar | `cactuar_ff.png` | `pricklespine_thornmarch` | Thornmarch Pricklespine | `pricklespine_thornmarch_ff.png` | ⚠️ Partial — silhouette is a recognisable FF lift. **Recommend a redraw**: keep green bristling biped, change the head/face shape. |
| *(sprite only, no db entry)* | Bomb | `bomb_ff.png` | `cinderpuff` | Cinderpuff | `cinderpuff_ff.png` | ⚠️ Partial — floating grinning sphere is likewise a lift. **Recommend a redraw**: keep floating ember sphere, replace the face. |
| `lord_baphomet` | Lord Baphomet | `boss_baphomet_ff.png` | `verrocaine_sovereign` | Verrocaine, the Horned Sovereign | `verrocaine_sovereign_ff.png` | ⚠️ Partial — horned demon lord reads fine, but "Baphomet" silhouette is RO-specific. **Recommend a redraw**: keep scale/horns/throne posture, change goat-head to something original. |

**Migration note:** renaming the file is a two-line change in `web/assets/sprites_ff/` plus the `sprite` field in `zaggers_database.json`. Godot `.import` sidecars must be renamed alongside, or deleted if the Godot branch is being retired (`DESIGN_AUDIT.md` §5).

---

## 10. Brand-new sprites required — 48

Every monster **not** in the table above needs original art. The full checklist with target filenames lives in `ASSET_MANIFEST.md`; the summary count is:

| Zone | New normal | New elite/rare | New boss | Subtotal |
|---|---|---|---|---|
| Gatewatch Commons | 4 | 0 | 0 | 4 |
| Whispering Meadows | 5 | 2 | 1 | 8 |
| Sunken Sanctum | 5 | 2 | 1 | 8 |
| Obsidian Spire | 6 | 2 | 1 | 9 |
| Glacial Chasm | 7 | 2 | 1 | 10 |
| Umbral Rootways | 7 | 2 | 0¹ | 9 |
| **Total** | **34** | **10** | **4** | **48** |

¹ Verrocaine reuses the Baphomet sprite (redraw recommended but not blocking).

**Priority order for art production** — ship playable bands, not scattered singles:
1. **P0** — Gatewatch (4) + Meadows new (8). Covers Lv 1–16, the entire first session.
2. **P1** — Sanctum new (8). Covers Lv 15–32.
3. **P2** — Spire new (9). Covers Lv 30–52.
4. **P3** — Chasm new (10). Covers Lv 50–72.
5. **P4** — Rootways new (9) + the three recommended redraws.

---

## 11. Stat philosophy

The curves below were **fitted to the existing data**, not invented. Three of the four legacy monsters — Green Slime (L3), Goblin Raider (L8), Skeleton Warrior (L17) — turned out to sit on a single clean power law, so that law was extracted and extended across all 54 entries.

**Base curves (rank `normal`):**

| Stat | Formula | Fit check |
|---|---|---|
| HP | `14 × level^1.05` | L3→44 (actual 45), L8→124 (120), L17→276 (280) |
| ATK | `2.7 × level` | L3→8 (8), L8→22 (22), L17→46 (45) |
| DEF | `0.7 × level` | L3→2 (2), L8→6 (6), L17→12 (12) |
| EXP | `2.7 × level^1.33` | L3→12 (12), L8→44 (45), L17→119 (120) |
| ZENY | `EXP × max(0.85, 1.30 − 0.025×level)` | L3→15 (15), L8→50 (50), L17→105 (110) |

**Rank multipliers:**

| Rank | HP | ATK | DEF | EXP | ZENY |
|---|---|---|---|---|---|
| normal | ×1.0 | ×1.0 | ×1.0 | ×1.0 | ×1.0 |
| elite | ×2.5 | ×1.3 | ×1.4 | ×3.5 | ×3 |
| rare | ×3.5 | ×1.4 | ×1.4 | ×5 | ×5 |
| boss | ×12 | ×1.6 | ×2.0 | ×12 | ×10 |

**Resulting boss ladder:**

| Boss | Lv | HP | ATK | EXP | ZENY |
|---|---|---|---|---|---|
| Ordwin the Palisade Tyrant | 16 | 3,088 | 69 | 1,294 | 971 |
| Hallowdeep, the Choirfall Warden | 32 | 6,393 | 138 | 3,254 | 2,305 |
| Vashkar the Spire Crown | 52 | 10,644 | 225 | 6,206 | 4,396 |
| Sylveth, Queen of the Silent Thaw | 72 | 14,980 | 311 | 9,567 | 6,777 |
| Verrocaine, the Horned Sovereign | 99 | 20,928 | 428 | 14,613 | 10,351 |

**`aggro`** — `passive` for slow/ambient spawns (Gloopling, Tortin, Rot Capling, Glasslight Mote, Emberglass Shard, Aurora Seraphon, Weeping Bough, Sanguine Thorncaller), `aggressive` for hunters and every elite/rare, `boss` for the five.

### 11.1 One deliberate stat change

Three legacy stat lines are preserved **exactly**: `gloopling_bellflower` 45/8/2/12/15, `snagtooth_raider` 120/22/6/45/50, `drowned_marrowguard` 280/45/12/120/110.

The fourth is not. `lord_baphomet` carried 5000 HP at an implied level 99 — but a level-90 *rare* on the fitted curve has ~5,900 HP, which would have made the final boss of the game squishier than a trash rare spawn standing two rooms away. **`verrocaine_sovereign` is therefore raised to 20,928 HP** (curve × boss multiplier). His zeny lands at 10,351, within 4% of the original 10,000 — so the economy-facing number is effectively unchanged and only the health bar was broken.

