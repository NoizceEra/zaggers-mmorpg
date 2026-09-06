# UX/UI Improvements Pass

Scope: `web/index.html` only. HUD layout/styling and general UX affordances
(tooltips, feedback, discoverability, modal polish) — additive on top of the
mobile pass (`vault/MOBILE_COMPATIBILITY_REPORT.md`) and the graphics pass
(`vault/GRAPHICS_UPGRADE_REPORT.md`, which already shipped HUD panel
glow/border polish — not duplicated here). No changes to movement/pathfinding,
collision, sprite-animation logic, or any `render()`/game-loop function body;
all edits are confined to UI-construction/event-binding functions and CSS, per
scope ownership for this pass (sibling agents own movement, collision, and
sprite/animation work on this same file).

Confirmed against current `master`/`integration` before starting: Phase 3's
Skill Tree Visualizer and Equipment Paperdoll (`vault/ROADMAP.md` §3.5/3.6)
were already shipped in `c40ef6b` — this pass builds UX polish on top of that
existing UI rather than re-implementing it.

---

## 1. Tooltips

Added a single shared tooltip engine (`initTooltipEngine()`, an IIFE near
`chatSystem()`) rather than per-widget tooltip code:

- One `#ui-tooltip` div, positioned in JS from the hovered/focused/
  long-pressed element's coordinates, shown for any element carrying a
  `data-tip` attribute — delegated at `document` level so newly rendered
  shop/inventory/skill/hotbar markup (all rebuilt via `innerHTML` on every
  state change) picks it up automatically with no per-render rebinding.
- **Desktop**: `mouseover`/`mouseout`/`mousemove` (follows the cursor) and
  `focusin`/`focusout` (keyboard users tabbing between controls see the same
  tooltip, positioned under the focused element).
- **Mobile**: a 450ms long-press (`touchstart` timer, cleared on
  `touchmove`/`touchend`/`touchcancel`) shows the tooltip. This listener only
  ever attaches to DOM widgets (buttons, rows, panels) — never the
  `<canvas>` itself — so it cannot conflict with the existing tap-to-move
  touch handling documented in `MOBILE_COMPATIBILITY_REPORT.md` §2/§3.
- Applied `data-tip` to:
  - The 6 core stat rows in the Stats window, each with a short
    plain-language blurb (STR/AGI/VIT/INT/DEX/LUK — none of these existed in
    `zaggers_database.json`, so these were authored fresh; every other
    tooltip below pulls its text from the DB's own `description` field where
    one exists, per the brief).
  - Every equipment paperdoll slot (`refreshEquipPanel()`) — shows the
    equipped item's description via `itemTooltipText()`, or a slot-role blurb
    (what Weapon/Shield/Armor/Headgear/Accessory each do, including the 2H
    shield-lock rule) when empty.
  - Every inventory row and shop row — `itemTooltipText()` prefers the item's
    DB `description`, falls back to the existing stat-line summary
    (`itemShortDesc()`), and appends the level requirement when present.
  - Every hotbar slot (F1–F9) — skill description + SP cost + cooldown via
    `itemTooltipTextForSkill()`, or "empty slot" guidance; the existing
    native `title` attribute is kept alongside as a redundant fallback.
  - Every skill-tree node — same `itemTooltipTextForSkill()` helper (kept the
    existing native `title` too), so a skill reads identically whether shown
    in the tree or bound to the hotbar.

## 2. Combat/status feedback

- **Low-HP warning state**: `updateHUD()` now toggles a `.active` class on a
  new `#low-hp-vignette` overlay and a `.hp-critical` class on
  `#status-window` whenever HP drops below 25% (and the player is still
  alive). Both use a `1.6s` pulsing red animation — the vignette darkens the
  play area's edges further (layered above the game canvas, below all
  modals) and the status panel's border/glow pulses in sync, so a low-HP
  state is unmissable without a screen-filling flash. This is additive to,
  not a replacement of, the graphics pass's static `drawVignette()` — that
  one is a permanent depth cue; this one is a state-driven warning.
- **HP/SP bar transitions**: bumped `.bar-fill`'s CSS transition from a bare
  `width 0.2s` to `width 0.25s ease-out, filter 0.2s ease-out` so a bar
  change (including the existing `bar-hit-pulse` flash from the graphics
  pass) eases rather than snaps.
- Floating combat numbers / crit-style indicators: verified the existing
  system (`pushDamageFloat()`) already differentiates heals (green, `+`
  prefix), normal hits (red/gold by damage size), and elemental
  advantage/resistance (gold `▲` / blue `▼` suffix) — this pass did not touch
  `render()`'s floating-text draw loop (out of scope per the render/game-loop
  restriction) and left that system as-is since it already reads as distinct
  categories rather than one undifferentiated number stream.

## 3. Inventory/shop UX

- **Item icon alt text**: `itemIconHtml()` now sets `alt="<item name>"`
  instead of `alt=""`.
- **Quantity indicators**: already present (`×{qty}` in each inventory row) —
  verified, not touched.
- **Can't-afford state**: `populateShopFromDB()` now computes affordability
  (zeny **and** level requirement) per row, adds a `.cant-afford` class
  (dimmed row, muted buy button) and `disabled` on the buy button when either
  check fails, and sets the row's tooltip to explain *why* ("Requires Lv. X"
  / "Not enough Zeny"). Previously every row looked identical regardless of
  whether the purchase was possible.
- **Purchase confirmation feedback**: `buyItemById()` now re-renders the shop
  list (so affordability states refresh immediately after a purchase) and
  flashes the purchased row green for 650ms (`.just-purchased` /
  `shop-purchase-flash` keyframe) as a lightweight, non-blocking confirmation
  beyond the existing chat-log line.

## 4. Onboarding/discoverability

Added a small dismissible hint panel (`#onboarding-hint`), shown once via a
`localStorage` flag (`zaggers_onboarding_seen_v1`), triggered at the end of
`confirmCharacterCreation()` (the game's single entry point into actual
gameplay — the client currently always shows the character creator on boot,
so this is the correct/only hook point). It:

- Explains click-to-move / click-an-NPC, F1–F9 + Space/click-to-attack, the
  Skills/Equip/Stats/Shop buttons, the new tooltip system itself, and the
  Kestrel Consignment House (Kafra) save/travel point.
- Is non-blocking: no backdrop, doesn't cover the canvas, can be dismissed
  (`dismissOnboarding()`) or ignored while playing.
- Never reappears once dismissed (checked via `localStorage` before showing).

## 5. Chat log / notification polish

- `chatSystem(msg, color, kind)` gained an optional third `kind` parameter
  that stamps a `data-kind` attribute on the message `<div>`; new CSS rules
  give `levelup`, `death`, and `zone` kinds a colored left-border + tinted
  background so they visually pop out of ordinary combat/system spam instead
  of scrolling by identically styled. Wired into: level-up messages (both
  `grantXp()`'s and `grantKillRewards()`'s level-up paths — the latter
  previously only floated combat text with no chat-log record at all),
  the death message (`triggerPlayerDeath()`), and zone-arrival messages
  (`applyZoneMapData()`). A `drop` kind/style also exists for when monster
  drop tables are wired (`ROADMAP.md` §3.6, still open) — forward-compatible,
  currently unused.
- **Scrollback cap**: added `trimChatLog()` (keeps the last 120 messages),
  called after every append site that was reachable without touching
  `render()` — `chatSystem()`, the player chat-input handler, zone arrival,
  death, and the character-creation welcome message — so a long play session
  no longer grows the chat DOM unbounded. (A handful of minor NPC-dialogue
  flavor lines elsewhere in the file still append directly without going
  through `chatSystem()`; those are far lower frequency than combat/system
  spam and were left alone to keep this pass surgical.)
- **XSS fix as a side effect of polish**: the player's own typed chat text
  was being inserted via `innerHTML` unescaped; `handleChatInput()` now
  HTML-escapes it before insertion. Every other chat line in the file is a
  trusted template string, so this was the one real gap.

## 6. Accessibility basics

- **Keyboard focus**: added `:focus-visible` outlines (gold, matching the
  theme) to every interactive control that didn't already get one for free
  from being a native `<button>` styled with existing hover states —
  specifically the two custom clickable `<div>`s in the file (`.hotbar-slot`,
  `.skill-node`), which now also carry `tabindex="0"`, `role="button"` /
  `role="group"` + `aria-label`, and (`.hotbar-slot` only, since it has a
  single unambiguous action) a `keydown` handler so **Enter/Space** casts
  the bound skill exactly like a click. `.creator-class-card` also gained a
  focus-visible rule (it was already a clickable div with `onclick`, no
  markup change needed there beyond the CSS).
- **Contrast over zone tints**: reviewed `GRAPHICS_UPGRADE_REPORT.md`'s
  `ZONE_ATMOSPHERE` table — all HUD text lives inside `.hud-panel`/
  `.window-modal` elements with their own opaque-ish dark backgrounds
  (`rgba(18,22,32,0.88)` / `rgba(14,18,26,0.96)`) composited *above* the
  canvas tint/vignette in the DOM stacking order, not tinted by it, so no
  regression was found there. In-canvas floating combat text already carries
  a `shadowBlur` drop-shadow from the graphics pass, which remains legible
  over every zone tint including the darkest (`rootways`, 0.30 alpha
  multiply) per that report's own verification pass.

## Verification performed

- Extracted the `<script>` block (`node -e` regex extraction) and ran
  `node --check` — **passes** with no syntax errors, including the
  pre-existing duplicate `getClassSkills()` declaration flagged (but not
  fixed, per prior passes' notes that it's out of scope and harmless in
  real non-module browser script mode) in `ENGINE_INFRA_AUDIT.md` /
  `MOBILE_COMPATIBILITY_REPORT.md`.
- Extracted the `<style>` block and confirmed brace balance (166 open / 166
  close).
- Served `web/` over a local static HTTP server and drove the game in a real
  browser: character creation → onboarding hint appears once, dismiss
  persists across reload (`localStorage`) → hovered a stat label and
  confirmed the tooltip renders with the correct text and position →
  tab-focused a hotbar slot and confirmed the same tooltip fires on focus →
  set `player.zeny` low and confirmed shop rows gain `.cant-afford` +
  disabled buttons with an explanatory tooltip → set `player.hp` below 25%
  and confirmed both `#low-hp-vignette` and `#status-window.hp-critical`
  activate (and clear when HP is restored) → added an item to inventory and
  confirmed its icon now carries real `alt` text and a description tooltip →
  pushed a `chatSystem(..., 'levelup')` message and confirmed the
  `data-kind="levelup"` styling applies. Checked the browser console: zero
  errors attributable to this pass (only two pre-existing 404s for
  not-yet-generated art assets, unrelated).
- Did not touch `web/zaggers_database.json`, `web/maps/*.json`,
  `web/editor.html`, `web/db_editor.html`, or any movement/collision/
  animation code path.

## Files changed

- `web/index.html` — all changes described above (new CSS block in `<head>`,
  new HTML elements — `#ui-tooltip`, `#low-hp-vignette`, `#onboarding-hint` —
  and new/modified JS in the main `<script>` block; no changes to
  `render()`/game-loop bodies).

## Rebase/merge notes

Started from `integration` (`387f1de`), which already carried master's tip
(`c40ef6b`) merged with the mobile-touch and graphics-upgrade passes. Rebased
this branch onto `integration` before starting work. `master` advanced past
`integration` mid-pass with `377f7fa` ("6 new hero classes (11 total), 2.5D
sprite sheets, and Stat-Driven Class Advancement system"), which touches
`web/index.html` (new hero sprites/classes, character-creator wiring) and
`web/zaggers_database.json`. That commit was merged in before the final
commit on this branch, favoring additive resolution — see the merge commit
for exactly which hunks combined. This pass added no new hero-class or
character-creation logic itself, so the merge surface with `377f7fa` was
almost entirely non-overlapping (its class/sprite additions vs. this pass's
tooltip/onboarding/HUD-polish additions); any conflict markers, if the
automatic merge could not resolve a hunk cleanly, are called out inline in
the merge commit rather than guessed at here.
