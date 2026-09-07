// ============================================================
// Zaggers Projectile Engine — web/fx/Projectiles.js
// Travel-time shots for ranged single-target skills. Melee stays
// instant (lunge). Additive: castSkill calls fire(), render() calls
// updateAndDraw(). Zero cost when no shots in flight.
// Respects GFX.lowGraphics (no trails, smaller glow).
// ============================================================
(function () {
  'use strict';

  var projectiles = [];
  var MAX_IN_FLIGHT = 24;

  // World-units per second by visual kind.
  var SPEEDS = { arrow: 11, bolt: 8, orb: 7 };
  var RANGED_CLASSES = { ranger: 'arrow', bard: 'arrow', alchemist: 'orb' };

  // Melee physical stays hitscan; everything else with a damage
  // component travels. Buffs/heals/traps never reach here.
  function kindFor(skill) {
    if (!skill) return null;
    if (skill.damageType === 'magic') return 'bolt';
    if (RANGED_CLASSES[skill.classId]) return RANGED_CLASSES[skill.classId];
    return null;
  }

  function isRanged(skill) {
    return kindFor(skill) !== null;
  }

  // onArrive(target) is called once at impact; the caller applies
  // damage (keeps all damage math in index.html, not here).
  function fire(x0, y0, target, opts) {
    if (!target) return false;
    if (projectiles.length >= MAX_IN_FLIGHT) projectiles.shift(); // oldest fizzle
    opts = opts || {};
    var kind = opts.kind || kindFor(opts.skill) || 'bolt';
    var dist = Math.hypot(target.wx - x0, target.wy - y0);
    var speed = SPEEDS[kind] || 8;
    projectiles.push({
      x0: x0, y0: y0, target: target,
      color: opts.color || '#ffffff', kind: kind,
      t: 0, dur: Math.max(0.12, dist / speed),
      onArrive: opts.onArrive || null
    });
    return true;
  }

  // Advance all shots; returns count still in flight.
  function update(dt) {
    for (var i = projectiles.length - 1; i >= 0; i--) {
      var p = projectiles[i];
      p.t += dt;
      if (p.t >= p.dur) {
        projectiles.splice(i, 1);
        var tgt = p.target;
        // Fizzle if the target died or despawned mid-flight.
        if (tgt && tgt.hp > 0 && !tgt.dying && p.onArrive) {
          try { p.onArrive(tgt); } catch (e) {}
        }
      }
    }
    return projectiles.length;
  }

  // Draw glowing heads (+short trails unless lowGraphics).
  function draw(ctx, worldToIso, cameraZoom, GFX) {
    var low = !!(GFX && GFX.lowGraphics);
    for (var i = 0; i < projectiles.length; i++) {
      var p = projectiles[i];
      var f = Math.min(1, p.t / p.dur);
      // Track living targets; fall back to snapshot at fire time.
      var tx = (p.target && p.target.hp > 0) ? p.target.wx : p.x0;
      var ty = (p.target && p.target.hp > 0) ? p.target.wy : p.y0;
      var wx = p.x0 + (tx - p.x0) * f;
      var wy = p.y0 + (ty - p.y0) * f - Math.sin(f * Math.PI) * 0.35; // slight arc
      var s = worldToIso(wx, wy);
      var r = (p.kind === 'arrow' ? 3.2 : 4.2) * cameraZoom * (low ? 0.8 : 1);
      ctx.save();
      ctx.globalAlpha = 0.95;
      ctx.fillStyle = p.color;
      ctx.shadowColor = p.color;
      ctx.shadowBlur = (low ? 4 : 8) * cameraZoom;
      ctx.beginPath();
      if (p.kind === 'arrow') {
        // Small elongated head along travel dir (screen-space approx).
        var ang = Math.atan2(ty - p.y0, tx - p.x0);
        ctx.ellipse(s.x, s.y, r * 1.6, r * 0.7, ang, 0, Math.PI * 2);
      } else {
        ctx.arc(s.x, s.y, r, 0, Math.PI * 2);
      }
      ctx.fill();
      if (!low) {
        ctx.globalAlpha = 0.45;
        ctx.shadowBlur = 0;
        ctx.beginPath();
        var back = 0.12; // trail segment behind head
        var f0 = Math.max(0, f - back);
        var bx = p.x0 + (tx - p.x0) * f0;
        var by = p.y0 + (ty - p.y0) * f0 - Math.sin(f0 * Math.PI) * 0.35;
        var bs = worldToIso(bx, by);
        ctx.moveTo(s.x, s.y);
        ctx.lineTo(bs.x, bs.y);
        ctx.strokeStyle = p.color;
        ctx.lineWidth = Math.max(1, r * 0.6);
        ctx.stroke();
      }
      ctx.restore();
    }
  }

  function updateAndDraw(ctx, worldToIso, cameraZoom, GFX, dt) {
    if (!projectiles.length) return 0;
    update(dt == null ? 1 / 60 : dt);
    draw(ctx, worldToIso, cameraZoom, GFX);
    return projectiles.length;
  }

  function clear() { projectiles.length = 0; }
  function activeCount() { return projectiles.length; }

  var api = {
    fire: fire, update: update, draw: draw,
    updateAndDraw: updateAndDraw, isRanged: isRanged,
    kindFor: kindFor, clear: clear, activeCount: activeCount
  };
  if (typeof window !== 'undefined') window.ZaggersProjectiles = api;
  if (typeof globalThis !== 'undefined') globalThis.ZaggersProjectiles = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})();
