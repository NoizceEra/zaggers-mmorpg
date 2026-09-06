# Sprite Direction / Class Completeness / Monster Animation Fixes

Scope owned by this pass: sprite assets (hero/class + monster) and directional-facing /
animation-frame rendering logic in `web/index.html`. Movement/pathfinding, collision, and
general HUD CSS were left untouched (sibling agents' territory).

## Bug 1: "Some class sprites are facing backwards"

### Convention (vault/PIPELINE_AND_TOOLS.md)
All character/monster sheets are 64x64 cells; row 0=Down/South, row 1=Left/West,
row 2=Right/East, row 3=Up/North.

### Row-index mapping audit (web/index.html)
The dx/dy -> row mapping is implemented identically in three places (player, NPC,
monster facing logic) and all three already match the vault convention correctly:

```js
if (dry > 0 && Math.abs(dry) >= Math.abs(drx)) dir = 0; // Down
else if (drx < 0 && Math.abs(drx) >= Math.abs(dry)) dir = 1; // Left
else if (drx > 0 && Math.abs(drx) >= Math.abs(dry)) dir = 2; // Right
else if (dry < 0 && Math.abs(dry) >= Math.abs(drx)) dir = 3; // Up
```

The draw code reads `sy = dir * 64` for both player and monster sprites — so the
row-index-to-direction **code mapping is correct and was not the bug**.

### Pixel-content audit (all 7 hero_*.png sheets, cropped row-by-row with PIL)
Diffed every pair of rows within each 256x256 (4 frames x 4 dirs) hero sheet to find
rows that were accidentally duplicated instead of drawn as distinct poses:

| Class | Row0 (Down) vs Row2 (Right) diff | Verdict |
|---|---|---|
| hero_knight | ~2.46M (in line with other pairs) | OK - genuinely distinct rows |
| hero_dragoon | ~0.95M (in line with other pairs) | OK - genuinely distinct rows |
| hero_redmage | ~0.77M (in line with other pairs) | OK - genuinely distinct rows |
| hero_whitemage | high (row2 is the true side-profile) | OK - genuinely distinct rows |
| hero_blackmage | high, all rows distinct | OK |
| **hero_monk** | **~193k (~4x lower than any other pair)** | **BUG - row2 (Right) is a pixel-for-pixel near-duplicate of row0 (Down)** |
| **hero_thief** | **~193k (~4x lower than any other pair)** | **BUG - row2 (Right) is a pixel-for-pixel near-duplicate of row0 (Down)** |

Visual confirmation: for `hero_monk` and `hero_thief`, the "Right"-facing row rendered
as an exact copy of the front-facing "Down" pose (same weapon side, same headband
position), instead of a mirror of the "Left" row. Moving right/east, both classes
visibly showed their front-facing sprite — this is the "facing backwards" symptom.

### Root cause
This is an **asset generation bug**, not a code bug — the East row was copy/pasted from
the Down row during original sprite-sheet authoring for these two classes only. All
other classes' four rows are legitimately distinct per-direction art.

### Fix
Regenerated row 2 (Right/East) for `hero_monk.png` and `hero_thief.png` as a
horizontal mirror of row 1 (Left/West), frame-by-frame (each of the 4 animation
columns mirrored in place, not the whole row flipped end-to-end — flipping the whole
256-wide row would have also reversed frame order). Applied identically to both
`assets/sprites_ff/` and `web/assets/sprites_ff/` copies (verified byte-identical
before and after). No code changes were needed for this half of bug 1.

Affected files:
- `assets/sprites_ff/hero_monk.png`, `web/assets/sprites_ff/hero_monk.png`
- `assets/sprites_ff/hero_thief.png`, `web/assets/sprites_ff/hero_thief.png`

Classes verified as already correct and left untouched: Vanguard (hero_knight),
Dragoon (hero_dragoon - not a playable core class but shares the sheet format),
Ranger (hero_redmage), Cleric (hero_whitemage), Spellweaver (hero_blackmage).

The four standalone `hero_down.png` / `hero_left.png` / `hero_right.png` /
`hero_up.png` files (64x64 each) are legacy/orphaned - grepped the whole repo
(`web/index.html`, all `scripts/*.py`, `*.gd`) and found zero references. Left as-is
since they are dead weight, not a live bug.

## Bug 2: "We don't have full classes showing"

### (a) Does the DB list all 5 core classes?
Yes. `web/zaggers_database.json` -> `classes` already has `vanguard`, `spellweaver`,
`shadowblade`, `cleric`, `ranger` - matching vault/WORLD_LORE.md's Faction & Class
Guilds exactly, each with a `sprite` field.

### (b) Do all 5 sprite files exist on disk?
Yes, verified all 5 exist in both `assets/sprites_ff/` and `web/assets/sprites_ff/`:
`hero_knight.png` (Vanguard), `hero_blackmage.png` (Spellweaver), `hero_thief.png`
(Shadowblade), `hero_whitemage.png` (Cleric), `hero_redmage.png` (Ranger).

### (c) Does the character-creator UI iterate/render all classes?
`renderCreatorClassCards()` calls `Object.values(getDbClasses()).forEach(...)` with no
slicing, filtering, or fixed-size grid — every class in the DB gets a card, and the
container (`#creator-class-cards`) is a scrollable flex column (`overflow-y: auto`),
not clipped. **This code path was already correct** and was not the bug.

### Root cause actually found: stale localStorage cache shadows a fresher DB file
`ensureGameDB()` had this priority order:
1. in-memory `gameDB` if already populated
2. **`localStorage['zaggers_db']` if it has any skills** <- checked before ever fetching
3. network fetch of `zaggers_database.json`

Once a browser had cached any DB snapshot (e.g. from an earlier build with fewer
classes, or a build where a class's `sprite` field was missing/wrong), step 2 always
won and the client would **never re-fetch** the corrected/expanded on-disk JSON,
since the cache is never invalidated (there's a `schemaVersion` field in the JSON but
it was never read or compared anywhere). This exactly matches "we don't have full
classes showing" for anyone (dev or player) who had loaded the game before all 5
classes/sprites were finalized.

### Fix
Reordered `ensureGameDB()` to always fetch the on-disk `zaggers_database.json` first;
the cached `localStorage` copy is now used only as a fallback when the network fetch
itself fails (offline/404), and a console warning flags that fallback as potentially
stale. The successful-fetch path still re-writes `localStorage['zaggers_db']` as
before, so offline fallback still works after at least one successful load.

File: `web/index.html`, function `ensureGameDB()`.

## Bug 3: Monster animation upgrade

### Starting point (prior animation pass, ENGINE_INFRA_AUDIT.md)
Already in place before this pass: per-monster `dir`/`frame`/`attackCooldown`/
`wanderPhaseOffset`/`hitFlashTimer`/`dying`/`deathTimer` state, a 4-phase walk cycle
(`WALK_CYCLE = [0,1,2,1]` stepped by `walkFrame()`), an idle frame (col 1), an attack
frame (col 3), hit-flash brightness filter, and a death fade+sink. All monster sprite
sheets (`assets/sprites_ff/*_ff.png`) are uniformly 256x256 = 4 columns x 4 rows, so
**every monster already has the 4 frames needed for a real walk-cycle + idle + attack
pose** - no sheet needed additional frames generated; the gap was purely in how the
existing frames were being driven, not in asset availability.

### What was broken/missing, and what was extended
1. **Attack pose was getting clobbered same-tick.** When an aggro monster attacked
   while still pursuing the player (the common case - `distToTarget` rarely reaches
   the `<= 0.15` "arrived" threshold while chasing a moving player), `m.frame = 3`
   (attack) was set, then the very same tick's movement branch immediately overwrote
   it with `walkFrame(...)`, so the attack frame was effectively never visible.
   Fixed by adding `m.attackPoseTimer` (16-tick hold, decremented every tick like the
   existing `attackCooldown`/`hitFlashTimer`): the walk-cycle and idle-frame branches
   now both check `attackPoseTimer <= 0` before overwriting `m.frame`, so a strike
   pose is guaranteed to actually render for ~16 frames after triggering.
2. **No idle bob/breathe for anything but the slime.** The only "alive-but-idle"
   animation was a hardcoded `if (m.sprite === 'slime_green_ff')` bounce. Added a
   general idle bob for every other monster: while `frame === 1` (idle) and not
   attacking/dying, a small (1.6px * cameraZoom), slow (0.06 rad/tick) vertical
   sine bob runs, phase-offset per monster via the existing `wanderPhaseOffset` so a
   pack of monsters doesn't breathe in visible lockstep. Slimes keep their original,
   more exaggerated squash-bounce untouched.
3. **Attack had no visual "impact" read.** Added a brief forward scale-pop
   (up to +15% size, decaying over the attack-pose window) on the strike frame,
   mirroring the player's existing windup/impact treatment but simplified (monsters
   have no windup phase in their AI, only an instant strike), so a hit reads as an
   impact rather than a static frame swap.

### Coverage
Because every monster sprite sheet already ships all 4 columns, **all monsters get
the full idle-bob + walk-cycle + attack-pose treatment uniformly** - there was no need
to prioritize "zone regulars" over rare monsters or generate any additional frames
with `scripts/generate_clean_monsters.py`; the fix was entirely in the shared
animation-driving logic in `web/index.html`, so it applies to every monster in
`zaggers_database.json` without per-monster special-casing (aside from the slime's
intentionally-preserved unique bounce).

## Validation
- Extracted the page's inline `<script>` block and ran `node --check` on it (wrapped
  in a throwaway function to sidestep an unrelated pre-existing top-level duplicate
  `function getClassSkills(classId)` declaration at lines 613 and 2041 of
  `web/index.html`, which Node's module-scope check flags but which is harmless in an
  actual classic-script browser context since a later `function` declaration simply
  overrides an earlier one at the same scope - not touched, as it's unrelated to
  sprite/animation logic and outside this pass's scope). Result: syntax OK both
  before and after every change in this pass.
- Verified via PIL that every sprite sheet referenced by the frame-advance code
  (`64x64` cell, up to 4 columns, 4 rows) matches its on-disk PNG dimensions: all
  `hero_*.png` and all monster `*_ff.png` files are exactly 256x256.
- Re-rendered and visually diffed the fixed `hero_monk.png`/`hero_thief.png` row
  strips to confirm Right is now a proper mirror of Left and distinct from Down, and
  that Up (back-facing, no face) was unaffected by the fix.

## Files changed
- `assets/sprites_ff/hero_monk.png`, `assets/sprites_ff/hero_thief.png`
- `web/assets/sprites_ff/hero_monk.png`, `web/assets/sprites_ff/hero_thief.png`
- `web/index.html` (`ensureGameDB`, `initMonsterState`, monster AI tick, monster draw)
