# Mobile Compatibility Report

Date: 2026-09-06
Scope: `web/index.html` only (single-file client). All changes are additive CSS/JS layered
alongside the existing desktop mouse/keyboard code — no existing input handling, game
logic, or CSS rules were removed or rewritten.

## Summary

The client now runs full-viewport on phones (portrait and landscape), supports
tap-to-move, two-finger camera rotate/zoom, and an on-screen action bar for the
F1–F9 hotbar / attack / stat / shop / skill / equip actions, with modals and HUD
panels resized to fit small screens. Desktop mouse+keyboard play is unaffected —
every addition is gated behind a `touch-mode` class (set only when a touch-capable
device is detected) or a `max-width` media query.

## 1. Viewport & responsive canvas

- `<meta viewport>` updated to `width=device-width, initial-scale=1, maximum-scale=1,
  user-scalable=no, viewport-fit=cover` — disables native pinch/double-tap page zoom
  (our own touch gesture code handles camera zoom instead) and respects notch safe areas.
- `#game-container` gets a `@media (max-width: 900px)` override that drops the old
  `aspect-ratio: 16/9; max-width: 1280px` desktop letterboxing and instead goes
  `width: 100vw; height: 100dvh` (with a `100vh` fallback for browsers without `dvh`
  support) — the canvas now fills the real device viewport instead of a desktop-shaped
  box squeezed into a tall screen.
- New `resizeGameCanvas()` (JS) sets `canvas.width`/`canvas.height` (the actual raster
  resolution, not just CSS size) to match `canvas.parentElement.getBoundingClientRect()`
  on load, `resize`, and `orientationchange` (debounced 250ms for iOS's late-firing
  viewport metrics after rotation). This was safe to add with zero risk to the existing
  isometric math: `worldToIso`/`isoToWorld` and the mousedown hit-testing already read
  `canvas.width`/`canvas.height` live every frame rather than hardcoded constants, so
  resizing the raster is transparent to the rest of the renderer.
- One-time zoom adaptation: if the first resize produces a portrait aspect
  (`height > width`), `cameraZoom` is set once to `clamp(0.65, width/480, 1.0)` so a
  narrow phone screen shows a wider slice of the world instead of the default desktop
  zoom level. This only fires once (`hasSetInitialMobileZoom` flag) so it never fights
  the player's own pinch-zoom or scroll-wheel zoom afterward.

## 2. Touch movement (tap-to-move)

Added a parallel `touchstart`/`touchmove`/`touchend`/`touchcancel` listener set on
`canvas`, independent of the existing `mousedown`/`mousemove`/`mouseup` listeners
(which are untouched). A single-finger touch that doesn't move more than 12px is
treated as a tap and routed through `handleTouchTap()`, which mirrors the existing
left-click NPC-hit-test + move-to logic byte-for-byte (duplicated intentionally
rather than refactoring the shared mouse handler, per the collision-minimization
goal — it reuses the same `isoToWorld`/`worldToIso` helpers, so it can't drift out of
sync with the projection math). A tap on an NPC within interaction range opens the
NPC dialog; otherwise it walks the player to the tapped world position, exactly like
a left-click.

## 3. Touch camera control

The same touch listener set tracks two-finger gestures:
- **Pinch** (change in distance between the two touch points) drives `cameraZoom`,
  clamped `[0.5, 2.0]` — a touch-equivalent of the existing mouse-wheel handler.
- **Two-finger horizontal drag** accumulates a delta and calls the existing
  `rotateCamera(±1)` function once per ~55px of drag — a touch-equivalent of the
  existing right-mouse-drag rotate handler.

`touch-action: none` is set on `canvas` via CSS so the browser never intercepts these
gestures for native pinch-zoom or scroll, and every touch listener calls
`preventDefault()`. Scrollable inner panels (`#chat-messages`, `.shop-items`,
`.inventory-list`, `.window-scroll-body`) are explicitly given `touch-action: pan-y`
so list scrolling inside modals still works with native touch scrolling.

## 4. On-screen action controls

- Touch-device detection: `isTouchDevice()` checks `'ontouchstart' in window`,
  `navigator.maxTouchPoints > 0`, and `matchMedia('(pointer: coarse)')` as a fallback,
  and adds a `touch-mode` class to `<html>`/`<body>` once at load. All new touch-only
  UI is gated behind `body.touch-mode` so desktop mouse/keyboard users see nothing new.
- The existing F1–F9 hotbar (`#skill-hotbar`) already dispatches through `onclick`
  handlers, so it was already tap-compatible; it now gets a `max-width: 900px` media
  query that wraps it into two rows (5+4) with 42px/37px slots (down from 48px) so all
  9 slots fit on a 375–430px-wide phone without being clipped by the container's
  `overflow: hidden`. Slot size stays close to the 44px touch-target guideline.
- Added a new "⚔️ Attack" button (`class="btn-icon touch-only"`) to the existing
  `#controls-hint` bar, calling the existing `triggerAttack()` — the only genuinely
  new on-screen control needed, since Stats/Skills/Equip/Shop toggle buttons already
  existed as tappable buttons in that bar.
- The three desktop-only dev tools in that bar (Map Editor, DB Editor, Load Map file
  input) are tagged `class="dev-only"` and hidden in `touch-mode` to declutter the
  action bar on phones — they remain fully visible/functional on desktop.
- `body.touch-mode .btn-icon` bumps to `min-height: 44px` inside the mobile media
  query so the remaining buttons (camera rotate ×2, angle reset, Stats, Skills, Equip,
  Shop, Attack) meet the 44px+ touch-target guideline; the bar itself is
  repositioned (via the media query) from its desktop top-right anchor to a
  centered, wrapping row just above the hotbar so it can't collide with the
  status/minimap HUD panels on a narrow screen.

## 5. Modal / UI scaling

Under `@media (max-width: 900px)` (with an extra `max-width: 420px` tier for very
small phones):
- `.window-modal` is capped to `max-width: 94vw`; `#stat-window`, `#shop-window`,
  `#skill-window`, `#equip-window`, `#npc-dialog-window` get explicit responsive
  widths (`90–94vw`, capped) instead of their fixed desktop pixel widths.
- `#skill-window`/`#equip-window` get `max-height: 82vh` (they already scroll
  internally via `.window-scroll-body`, so content that doesn't fit scrolls rather
  than overflowing off-screen).
- `.equip-layout` switches from a fixed two-column `flex: row` (paperdoll + inventory
  side by side, ~400px+ combined) to `flex-direction: column`, and `.paperdoll`
  becomes a wrapping 2-up grid of slots instead of a single 200px-wide column, so the
  equipment screen fits a phone's width without horizontal scrolling.
- The character creator's 3-column layout (name/class list, sprite preview, stats/lore)
  is collapsed to a vertical stack on narrow screens via a `> div[style*="flex: 1"]`
  selector targeting its inline-styled row container (it has no id/class of its own in
  the markup), with each column forced to `width: 100%`; the whole modal becomes
  scrollable (`overflow-y: auto`) since a stacked 3-section column is taller than one
  phone screen.
- The death/respawn overlay (`#player-death-modal`) gets a `max-width: 90vw` cap on its
  inner card and reduced heading/paragraph font sizes so its two respawn buttons stay
  fully on-screen and tappable without overflow.
- HUD panels (`#status-window`, `#minimap-container`/`#minimap-canvas`, `#chat-window`)
  shrink to fit alongside each other at the top of a ~375px-wide screen, and get
  `env(safe-area-inset-top)`-aware top offsets for notched devices.

Nothing here redesigns any screen's structure or interaction model — only widths,
flex-direction, font sizes, and positions changed via new CSS rules layered on top of
the existing class/id selectors.

## 6. Performance

All additions are event-driven (`resize`, `orientationchange`, `touchstart/move/end/
cancel`), not polled per animation frame. `resizeGameCanvas()` only writes to
`canvas.width`/`height` when the computed size actually differs from the current one
(prevents redundant raster reallocation firing every call). No new work was added to
the existing `render()` requestAnimationFrame loop.

## Devices / orientations targeted

Reasoned through (no physical device available in this environment):
- **iPhone SE / small phones, 375×667 portrait** — hotbar wraps to 2 rows at 42px
  slots (fits inside the `max-width: 264px` wrap container); modals cap at 94vw.
- **iPhone 14/15-class, 390–430×844+ portrait** — same layout, more headroom.
- **Common Android phones, 360–412×~800 portrait** — covered by the same
  `max-width: 420px` tier for the narrowest (360px) case (37px hotbar slots).
- **Phone landscape, ~700–900×360–430** — falls under the `max-width: 900px` query by
  width in portrait but landscape widths here often exceed 900px on larger phones; in
  that case the container still fills the viewport via the base full-bleed rule (which
  only depends on being ≤900px in *either* the CSS `max-width` breakpoint, evaluated
  against viewport width) — **known gap**: a large-phone landscape viewport wider than
  900px (e.g. some 428×926 phones rotated, ~926px wide) will fall back to the desktop
  16:9 letterboxed layout instead of full-bleed. This is a reasonable degrade (still
  playable, just letterboxed) rather than a break, but is not pixel-verified.
- **Tablets (iPad-class, ~768–1024px)** — treated as desktop layout (above the 900px
  breakpoint) but still gets full touch input support (tap-to-move, pinch/rotate,
  touch-mode action bar) since `isTouchDevice()` is independent of screen width.

## Known gaps / not verified on a real device

- No physical phone/tablet was available in this sandboxed environment. All
  correctness reasoning was done by tracing the code paths (event math, CSS cascade,
  canvas resize math) rather than visual on-device confirmation. Recommend a quick
  manual pass on at least one real iOS and one real Android device before shipping.
- The `100dvh` CSS unit (used for the mobile `#game-container` height, with a `100vh`
  fallback declared first) is not supported on older WebKit/Chromium — on those it
  silently keeps the `100vh` value, which can be a few dozen pixels short/tall on
  iOS Safari when the address bar shows/hides; not fixed with a JS `visualViewport`
  listener in this pass.
- Two-finger rotate/pinch and single-finger tap-to-move share the same canvas
  listeners; a 3+ finger touch is treated the same as 2-finger (only the first two
  touch points are read), which is fine for typical use but not explicitly tested.
- Virtual keyboard behavior for the chat input (`#chat-input`) on mobile (viewport
  resize/jump when the OS keyboard opens) was not specifically addressed — the layout
  should still function (the input is a simple text field) but has not been traced
  step-by-step for keyboard-overlap edge cases.
- No on-screen joystick was added; tap-to-move was chosen as the baseline per the
  task's own fallback guidance, to avoid touching the existing click-to-move movement
  state machine (`player.targetWx/targetWy`) that both mouse and touch now share.
- The pre-existing duplicate top-level `function getClassSkills(classId) { ... }`
  declaration in `web/index.html` (unrelated to this change, already present on
  `master`) is harmless in real browsers (redeclaration of a `function` at script
  scope is legal in non-module/non-strict script mode — the second definition simply
  wins) but trips `node --check`'s stricter module-detection heuristics. Not fixed
  here since it's out of scope and pre-existing; flagged for a future cleanup pass.

## Verification performed

- Extracted the `<script>` block and ran `node --check` after neutralizing the one
  pre-existing unrelated duplicate declaration above — the rest of the script (all
  new code included) parses without error.
- Extracted the `<style>` block and confirmed brace count balance (123 open / 123
  close).
- Manually traced: 375×844 portrait tap-to-move (canvas resize → `isoToWorld` →
  bounds clamp → `player.targetWx/Wy`), two-finger pinch+rotate math, hotbar wrap at
  360px/375px/414px widths, and the character-creator column stack at 375px width.
