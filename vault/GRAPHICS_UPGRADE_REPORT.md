# GRAPHICS UPGRADE PASS

Scope: `web/index.html` only. Additive graphics/juice pass on top of the prior
animation work documented in `vault/ENGINE_INFRA_AUDIT.md` (walk-cycle,
attack windup, hit-flash, monster death fade, torch/water shimmer) — nothing
here replaces or duplicates that work, it layers on top of it. No changes to
`web/zaggers_database.json`, `web/maps/*.json`, `web/editor.html`, or
`web/db_editor.html`.

All new behavior is gated behind a single `GFX` settings object
(`window.ZaggersGraphics`) so a future "low graphics mode" toggle only needs
to flip booleans/call `setLowGraphicsMode(true)` — no structural rework
required.

```js
const GFX = {
  ambientTint: true,   // per-zone color-grade overlay
  particles: true,     // ambient zone particles + skill impact bursts
  vignette: true,      // screen-edge darkening
  lowGraphics: false   // halves particle caps when true
};
window.ZaggersGraphics = GFX;          // toggle any flag live from devtools
window.setLowGraphicsMode(true/false); // convenience switch for #4 below
```

---

## 1. Per-zone ambient atmosphere (color-grade overlay)

`ZONE_ATMOSPHERE` maps each `currentMapId` (already tracked by
`applyZoneMapData()`/`loadZoneMap()`) to a tint color/alpha/composite-mode,
matching `vault/WORLD_LORE.md`:

| Zone | Tint | Composite mode | Rationale |
|---|---|---|---|
| `aethelgard` (town) | none | — | Neutral hub, no atmosphere needed |
| `gatewatch` | warm `255,224,178` @ 0.05 | `source-over` | Faint dawn/hub warmth, barely visible |
| `meadows` | warm `255,238,170` @ 0.10 | `source-over` | Vibrant sunlight — additive-ish warmth doesn't darken |
| `sanctum` | teal `30,110,120` @ 0.22 | `multiply` | Cool damp bioluminescent, darkens without graying out |
| `spire` | crimson `160,40,20` @ 0.20 | `multiply` | Fiery/ash-fall mood |
| `chasm` | icy `150,195,255` @ 0.20 | `multiply` | Cold blue-white mist |
| `rootways` | purple `80,25,105` @ 0.30 | `multiply` | Eerie twilight (Realm of Baphomet) |

Implementation: `drawZoneAtmosphere()` — one `ctx.createLinearGradient` +
one `ctx.fillRect` per frame, drawn full-canvas after the depth-sorted
entity list and ambient particles, before floating combat text (so damage
numbers stay legible on top). `multiply` is used for the darker/cooler
zones so sprite colors underneath aren't washed to white; the two bright
daylight zones (`meadows`, `gatewatch`) use plain low-alpha `source-over`
layering instead since `multiply` would just darken sunlight, not warm it.

**Cost:** 1 gradient + 1 fillRect per frame when in a tinted zone (0 cost
in `aethelgard`, where `tint: null`). Negligible on mobile — same order of
cost as the existing water-shimmer diamond fill.

**Tune/disable:** set `GFX.ambientTint = false`, or edit/add entries in
`ZONE_ATMOSPHERE` (e.g. add `gatewatch`'s own distinct mood later).

---

## 2. Ambient particles (per-zone)

A single generic capped particle pool (`ambientParticles`, cap
`AMBIENT_PARTICLE_CAP = 36`, halved to 18 under `GFX.lowGraphics`) drives
four zone-specific looks via `spawnAmbientParticle(type)`:

- `pollen` (Whispering Meadows) — warm drifting dust/pollen, slow upward drift
- `motes` (Sunken Sanctum) — bioluminescent turquoise motes, slow float + pulse
- `ash` (Obsidian Spire) — falling grey/ember ash with horizontal sway
- `snow` (Glacial Chasm) — falling white flakes with sway
- `rootmotes` (Realm of Baphomet/Rootways) — purple eerie floating motes

Particles are **screen-space**, not world-space: they drift across the
canvas and respawn/recycle when they expire or drift off-screen
(`updateAmbientParticles()`), so there's no per-particle world→screen
transform or camera-relative culling to pay for — just an `x/y` drift and a
bounds check. `aethelgard` and `gatewatch` (town hubs) have `particles: null`
and spawn nothing. Switching zones swaps the pool immediately (compares
`currentMapId`'s atmosphere type against the pool's current type and clears
on mismatch).

**Cost:** ≤36 (≤18 low-graphics) simple `arc()+fill()` draws per frame,
capped hard — never grows unbounded. Well within "a few dozen dots" budget
from the brief; verified in-browser with no dropped-frame console warnings.

**Tune/disable:** `GFX.particles = false` disables both ambient particles
and skill-impact bursts (§3). Lower `AMBIENT_PARTICLE_CAP` for a smaller
constant budget, or call `setLowGraphicsMode(true)` to halve it at runtime.

---

## 3. Combat/skill elemental impact bursts

`spawnSkillImpact(wx, wy, color)` fires a small burst (8 particles normal,
4 under `lowGraphics`, hard-capped at `IMPACT_PARTICLE_CAP = 48` in flight
across all bursts) using the **existing elemental color system**
(`getElementColor()` / `zaggers_database.json`'s `elements.colors`) so a
Fire skill bursts orange/red, Ice bursts blue, etc. — reusing data already
defined for damage-number tinting, not a new color table.

Wired into both damage paths without touching their damage math:
- `applyMonsterHit()` (the DB-driven skill/attack path) — burst colored by
  `result.atkEl` via `getElementColor()`.
- `applyDamageToMonster()` (the ground-trap path) — burst colored by the
  same `color` already used for that hit's floating text.

This **builds on** the existing white hit-flash (`m.hitFlashTimer`/
`ctx.filter = 'brightness(2.4) saturate(0.3)'`) rather than replacing it —
both fire together on the same hit.

**Cost:** short-lived (≈16–26 frames, under half a second), capped pool,
zero cost when no combat is happening (array stays empty).

**Tune/disable:** gated by the same `GFX.particles` flag as ambient
particles; `IMPACT_PARTICLE_CAP` / the `n = lowGraphics ? 4 : 8` burst size
are the two knobs if a future pass wants punchier or cheaper hits.

---

## 4. Lighting/depth polish (vignette)

`drawVignette()` — one `ctx.createRadialGradient` + `fillRect` per frame,
darkening the screen edges (transparent center out to ~42% black at the
corners). Composited **after** the zone atmosphere tint and particles but
**before** floating combat text, so text stays fully readable. Pure
gradient math, no per-pixel shader — same cost class as the atmosphere
tint.

**Tune/disable:** `GFX.vignette = false`, or adjust the two color stops /
radii in `drawVignette()`.

### Draw-order summary (additive layers only — no existing draw calls reordered)
```
tiles → depth-sorted entities (player/npc/monster/env, unchanged)
  → ground traps (unchanged)
  → ambient particles + impact bursts   [NEW]
  → zone atmosphere tint                [NEW]
  → vignette                            [NEW]
  → floating combat text (now with glow + spawn-pop, see §5)
  → minimap (unchanged)
```

---

## 5. HUD/UI visual polish

Layout is untouched — only styling/finish:

- **HP/SP bars**: added `box-shadow` glow (red/blue respectively) plus an
  inset highlight, and a `.bar-pulse` CSS keyframe (`bar-hit-pulse`,
  0.4s brightness flash) that `updateHUD()` now triggers automatically via
  `flashBarOnDrop()` whenever HP or SP **decreases** since the last call
  (tracked with `_prevHudHp`/`_prevHudSp`). No new elements — just a
  classList toggle + forced reflow so the animation can restart on repeated
  hits.
- **Minimap**: added a soft outer glow + inner vignette on `#minimap-canvas`
  and a text-shadow on the zone title so it doesn't look flat.
- **Hotbar slots**: subtle gradient background + inset hairline + a
  slightly stronger hover glow (was a flat fill before).
- **Floating combat numbers**: now drawn with a drop-shadow for legibility
  over any background, and a brief scale-up "pop" on spawn (`ft.maxLife`
  captured lazily on first frame, `pop` eases back to 1x over the first 15%
  of the text's life) — cheap, no new allocations beyond the one field.

**Cost:** CSS transitions/box-shadows are compositor-cheap; the floating
text glow is one extra `ctx.save/shadowBlur/restore` per active text (there
are only ever a handful on screen at once, per the existing perf audit).

**Tune/disable:** the CSS effects are static (no runtime toggle needed —
they're cheap enough to always be on); the floating-text pop/glow could be
gated behind `GFX` later if desired, but was left always-on since it's pure
`ctx` state churn on an already-small array.

---

## 6. Low-graphics-mode readiness (§6 of the brief)

Everything above reads from `GFX` at call time, not at boot, so a future
settings panel just needs to flip flags:

```js
GFX.ambientTint = false;   // kill the per-zone tint
GFX.particles = false;     // kill ambient particles AND impact bursts
GFX.vignette = false;      // kill the vignette
setLowGraphicsMode(true);  // halve particle caps (ambient 36→18, impact burst 8→4) without killing the effect outright
```

No per-frame branch was hoisted out of the hot loop in a way that would
require restructuring later — the checks are simple boolean guards at the
top of each `draw*`/`update*` function, matching the existing code's style
(e.g. `if (env.animated && ...)` guards already in the file).

---

## Verification performed

- Extracted the `<script>` block and ran `node --check` (via a `.cjs` copy,
  since the extraction directory's `package.json` sets `"type": "module"`
  and ESM's strict-mode duplicate-function-declaration rule otherwise
  false-flags a **pre-existing** duplicate `getClassSkills()` in the
  original file, unrelated to this pass) — syntax OK on both the modified
  file and confirmed the same duplicate exists in `HEAD` unmodified, so it's
  not a regression introduced here.
- Grepped for all `render()`/`draw*`/`animate*` call sites touched — every
  new function (`updateAmbientParticles`, `drawAmbientParticles`,
  `updateAndDrawImpactParticles`, `drawZoneAtmosphere`, `drawVignette`,
  `spawnSkillImpact`, `flashBarOnDrop`) is defined exactly once and called
  from exactly the intended site(s) inside `render()`/`applyMonsterHit()`/
  `applyDamageToMonster()`/`updateHUD()`.
- Served `web/` over a local static server and drove the game in a real
  browser end-to-end: character creation → Aethelgard town (neutral, no
  tint, HUD glow visible) → teleported to Obsidian Spire via
  `loadZoneMap('spire')` (crimson tint + vignette clearly visible, sprite
  colors still read correctly, no wash-out) → triggered an attack on a
  monster and confirmed `spawnSkillImpact` populated 8 particles, the
  floating damage number popped/glowed, and the HP bar pulsed on the
  return hit. Confirmed `setLowGraphicsMode(true)` halves the ambient cap
  (36→18) live. Checked browser console: zero errors attributable to the
  new code (only pre-existing 404s for a couple of not-yet-generated art
  assets, unrelated to this pass).

## Files changed

- `web/index.html` — all changes described above (CSS in `<head>`, new JS
  in the main `<script>` block, three call sites added into existing
  functions).
