// ============================================================
// Zaggers Web Combat Feel
// web/fx/CombatFeel.js
//
// Additive game-feel layer on top of the existing instant-hit combat
// (web/index.html applyMonsterHit / applyDamageToMonster +
// hitFlashTimer + spawnSkillImpact). Does NOT change damage math,
// balance, or kill/respawn flow - it only adds freeze / shake /
// push / pop / queue juice around the existing calls.
//
// Pairs with the ParallaxBackgrounds.js GFX-gating convention:
//   far layer skipped when GFX.particles is off or lowGraphics is on;
//   detail counts halved under lowGraphics.
// This module follows the same rule:
//   - screen shake amplitude halved under GFX.lowGraphics
//   - hitstop duration halved under GFX.lowGraphics
//   - knockback + GCD queue are gameplay (never gated)
//   - crit pop scale is kept (readability), extra shake is gated
//
// Integration = 2 hooks (see COMBAT_FEEL_SNIPPET below):
//   Hook A: after applyMonsterHit() / applyDamageToMonster()
//   Hook B: in render(), at the camera-lerp block
// ============================================================
(function () {
  'use strict';

  // ----------------------------------------------------------
  // Tuning (single place - see tuning table in the report)
  // ----------------------------------------------------------
  var TUNING = {
    HITSTOP_MS: 60,          // freeze on a landed hit
    HITSTOP_CRIT_MS: 90,     // freeze on a crit (>= CRIT_THRESHOLD)
    SHAKE_MAX_PX: 6,         // peak screen offset at trauma=1, zoom=1
    SHAKE_DECAY_PER_SEC: 1.6,// trauma units drained per second
    HIT_TRAUMA: 0.30,        // trauma added per normal hit
    CRIT_TRAUMA: 0.55,       // trauma added per crit hit
    KNOCKBACK_UNITS: 0.35,   // world-unit push per normal hit
    KNOCKBACK_CRIT_MULT: 1.5,// push multiplier on crit
    KNOCKBACK_FRICTION: 6.0, // residual slide decay (per sec, exp)
    CRIT_THRESHOLD: 30,      // matches pushDamageFloat >30 + monster.gd <30
    CRIT_POP_SCALE: 1.6,     // floating-text scale on crit
    GCD_MS: 500              // global cooldown between skill casts
  };

  // ----------------------------------------------------------
  // Internal state (module-local - no page globals polluted)
  // ----------------------------------------------------------
  var trauma = 0;            // 0..1 screen-shake energy
  var freezeUntilMs = 0;     // performance.now() watermark for hitstop
  var queuedSkillId = null;  // 1-deep skill queue (buffered input)
  var queuedAtMs = 0;
  var lastCastAtMs = -1e9;   // last successful cast (GCD source)

  function globals() {
    if (typeof globalThis !== 'undefined') return globalThis;
    return this;
  }

  // GFX.lowGraphics lookup: explicit hint wins, then the page's live
  // window.ZaggersGraphics (web/index.html Graphics Upgrade Pass),
  // then a bare GFX global (parallax-test convention). Defaults to
  // full-quality when nothing is present (node / tests).
  function isLowGraphics(gfxHint) {
    var g = globals();
    var gfx = gfxHint || g.ZaggersGraphics || g.GFX || null;
    return !!(gfx && gfx.lowGraphics);
  }

  function nowMs() {
    if (typeof performance !== 'undefined' && performance.now) return performance.now();
    return Date.now();
  }

  function clamp01(v) {
    return v < 0 ? 0 : (v > 1 ? 1 : v);
  }

  // ----------------------------------------------------------
  // Hitstop: a ~60ms freeze on impact (game-feel classic).
  // The render loop keeps drawing but skips world updates while
  // isFrozen() is true, so the impact frame "lands" visually.
  // ----------------------------------------------------------
  function triggerHitstop(ms, gfxHint) {
    var base = (ms != null) ? ms : TUNING.HITSTOP_MS;
    if (isLowGraphics(gfxHint)) base *= 0.5;
    var until = nowMs() + base;
    if (until > freezeUntilMs) freezeUntilMs = until;
    return base;
  }

  function triggerHitstopForDamage(dmg, gfxHint) {
    return triggerHitstop(isCrit(dmg) ? TUNING.HITSTOP_CRIT_MS : TUNING.HITSTOP_MS, gfxHint);
  }

  function isFrozen(atMs) {
    var t = (atMs != null) ? atMs : nowMs();
    return t < freezeUntilMs;
  }

  // ----------------------------------------------------------
  // Screen shake: trauma 0..1, decays linearly, offset scales
  // with trauma^2 (small hits whisper, crits thump). Deterministic
  // sin-based noise so tests snapshot identically every run.
  // Returns screen-space px { x, y } - caller adds it to the
  // camera (Hook B) or ctx.translate(). Already scaled by zoom.
  // ----------------------------------------------------------
  function addTrauma(amount, gfxHint) {
    var a = (amount != null) ? amount : TUNING.HIT_TRAUMA;
    if (isLowGraphics(gfxHint)) a *= 0.5;
    trauma = clamp01(trauma + a);
    return trauma;
  }

  function addHitTrauma(dmg, gfxHint) {
    return addTrauma(isCrit(dmg) ? TUNING.CRIT_TRAUMA : TUNING.HIT_TRAUMA, gfxHint);
  }

  // dtSec: seconds since last frame. atMs: timestamp for the noise
  // phase (defaults to now). zoom: page cameraZoom (default 1).
  function update(dtSec, atMs, zoom, gfxHint) {
    if (dtSec > 0 && trauma > 0) {
      trauma = clamp01(trauma - TUNING.SHAKE_DECAY_PER_SEC * dtSec);
    }
    return getShake(atMs, zoom, gfxHint);
  }

  function getShake(atMs, zoom, gfxHint) {
    if (trauma <= 0) return { x: 0, y: 0 };
    var t = (atMs != null) ? atMs : nowMs();
    var z = (zoom != null) ? zoom : 1;
    var mag = TUNING.SHAKE_MAX_PX * trauma * trauma * z;
    if (isLowGraphics(gfxHint)) mag *= 0.5;
    // Two incommensurate sines -> organic jitter, still deterministic.
    var nx = Math.sin(t * 0.09) * 0.6 + Math.sin(t * 0.031 + 1.7) * 0.4;
    var ny = Math.cos(t * 0.083 + 0.6) * 0.6 + Math.cos(t * 0.029 + 3.1) * 0.4;
    return { x: nx * mag, y: ny * mag };
  }

  function getTrauma() { return trauma; }
  function resetFeel() {
    trauma = 0;
    freezeUntilMs = 0;
    queuedSkillId = null;
    lastCastAtMs = -1e9;
  }

  // ----------------------------------------------------------
  // Knockback: immediate world-unit push away from the attacker
  // plus a short residual slide the render loop bleeds off via
  // stepKnockback(). Stored on cfx_* fields so it never collides
  // with the existing wx/wy/homeWx AI fields or hitFlashTimer.
  // ----------------------------------------------------------
  function applyKnockback(target, fromWx, fromWy, powerUnits, dmg) {
    if (!target) return { x: 0, y: 0 };
    var crit = isCrit(dmg == null ? 0 : dmg);
    var power = (powerUnits != null) ? powerUnits : TUNING.KNOCKBACK_UNITS;
    if (crit) power *= TUNING.KNOCKBACK_CRIT_MULT;
    var dx = (target.wx || 0) - (fromWx || 0);
    var dy = (target.wy || 0) - (fromWy || 0);
    var len = Math.hypot(dx, dy);
    if (len < 1e-4) { dx = 1; dy = 0; len = 1; }
    dx /= len; dy /= len;
    target.wx = (target.wx || 0) + dx * power;
    target.wy = (target.wy || 0) + dy * power;
    // Residual slide (world units/sec), decayed by stepKnockback().
    target.cfx_kbx = dx * power * 4;
    target.cfx_kby = dy * power * 4;
    return { x: dx * power, y: dy * power };
  }

  function stepKnockback(target, dtSec) {
    if (!target || dtSec <= 0) return;
    var kx = target.cfx_kbx || 0;
    var ky = target.cfx_kby || 0;
    if (kx === 0 && ky === 0) return;
    var keep = Math.exp(-TUNING.KNOCKBACK_FRICTION * dtSec);
    target.wx = (target.wx || 0) + kx * dtSec;
    target.wy = (target.wy || 0) + ky * dtSec;
    target.cfx_kbx = kx * keep;
    target.cfx_kby = ky * keep;
    if (Math.hypot(target.cfx_kbx, target.cfx_kby) < 0.02) {
      target.cfx_kbx = 0;
      target.cfx_kby = 0;
    }
  }

  // ----------------------------------------------------------
  // Crit pop: threshold mirrors the two existing color splits
  // (pushDamageFloat dmg>30 yellow + monster.gd dmg<30 red). The
  // floating-text renderer already does a generic 1.3x spawn pop;
  // markCritFloat() upgrades crits to CRIT_POP_SCALE + longer life.
  // ----------------------------------------------------------
  function isCrit(dmg) {
    return (dmg || 0) >= TUNING.CRIT_THRESHOLD;
  }

  function critScale(dmg) {
    return isCrit(dmg) ? TUNING.CRIT_POP_SCALE : 1.0;
  }

  function markCritFloat(ft, dmg) {
    if (!ft) return ft;
    if (!isCrit(dmg)) return ft;
    ft.crit = true;
    ft.pop = TUNING.CRIT_POP_SCALE;
    ft.life = Math.max(ft.life || 0, 50);
    ft.maxLife = Math.max(ft.maxLife || 0, 50);
    return ft;
  }

  // ----------------------------------------------------------
  // Skill queue + 500ms GCD: one buffered input so a skill pressed
  // mid-swing/cast fires on the next available frame instead of
  // being swallowed. GCD is gameplay - never GFX-gated.
  // ----------------------------------------------------------
  function queueSkill(skillId, atMs) {
    if (!skillId) return null;
    queuedSkillId = skillId;
    queuedAtMs = (atMs != null) ? atMs : nowMs();
    return queuedSkillId;
  }

  function getQueuedSkill() { return queuedSkillId; }

  function gcdReady(atMs) {
    var t = (atMs != null) ? atMs : nowMs();
    return (t - lastCastAtMs) >= TUNING.GCD_MS;
  }

  function notifyCast(atMs) {
    lastCastAtMs = (atMs != null) ? atMs : nowMs();
    return lastCastAtMs;
  }

  // Returns the skillId to fire, or null. Consumes the queue only
  // when the fighter is free AND the GCD has elapsed.
  function tryConsumeQueued(atMs, busy) {
    if (!queuedSkillId || busy) return null;
    if (!gcdReady(atMs)) return null;
    var id = queuedSkillId;
    queuedSkillId = null;
    notifyCast(atMs);
    return id;
  }

  // One-call convenience for Hook A: freeze + trauma + knockback +
  // crit marking. Returns { frozen, crit } for HUD/chat hooks.
  // entity: monster object, from: { wx, wy } attacker pos,
  // ft: the floating-text entry just pushed (optional).
  function onHitLanded(entity, dmg, from, ft, gfxHint) {
    var crit = isCrit(dmg);
    triggerHitstopForDamage(dmg, gfxHint);
    addHitTrauma(dmg, gfxHint);
    if (entity && from) {
      applyKnockback(entity, from.wx, from.wy, undefined, dmg);
    }
    if (ft) markCritFloat(ft, dmg);
    return { crit: crit };
  }

  var api = {
    TUNING: TUNING,
    triggerHitstop: triggerHitstop,
    triggerHitstopForDamage: triggerHitstopForDamage,
    isFrozen: isFrozen,
    addTrauma: addTrauma,
    addHitTrauma: addHitTrauma,
    update: update,
    getShake: getShake,
    getTrauma: getTrauma,
    resetFeel: resetFeel,
    applyKnockback: applyKnockback,
    stepKnockback: stepKnockback,
    isCrit: isCrit,
    critScale: critScale,
    markCritFloat: markCritFloat,
    queueSkill: queueSkill,
    getQueuedSkill: getQueuedSkill,
    gcdReady: gcdReady,
    notifyCast: notifyCast,
    tryConsumeQueued: tryConsumeQueued,
    onHitLanded: onHitLanded
  };

  if (typeof window !== 'undefined') window.ZaggersCombatFeel = api;
  if (typeof globalThis !== 'undefined') globalThis.ZaggersCombatFeel = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})();
