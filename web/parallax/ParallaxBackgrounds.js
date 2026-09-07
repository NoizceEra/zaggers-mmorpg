// ============================================================
// Zaggers Web Parallax Background Engine
// web/parallax/ParallaxBackgrounds.js
//
// Screen-space 3-layer parallax painted BEHIND the iso tile grid.
// See vault/WORLD_LORE.md for the per-zone art direction and
// web/index.html render() (~line 3832) for the integration point.
//
// Design constraints (from the render-loop research):
// - canvas is 640x360 (canvas.width/height are read live, so it
//   also adapts if the canvas ever changes size).
// - worldToIso uses TILE_W 48 / TILE_H 24; parallax intentionally
//   does NOT use iso projection - it is a screen-space backdrop,
//   so it stays correct across camera pans/rotations by construction.
// - Draw order in render(): tiles -> entities -> particles ->
//   atmosphere -> vignette -> floating text. drawParallax() goes
//   FIRST (right after the bg fillRect, before the tile loop).
// - Respects the GFX flags + setLowGraphicsMode() convention from
//   the Graphics Upgrade Pass (GRAPHICS_UPGRADE_REPORT.md):
//   far layer is skipped when GFX.particles is off or lowGraphics
//   is on; detail counts are halved under lowGraphics.
// - Zero cost when the zone has no bg (town hubs): config is null
//   and drawParallax() returns 0 without touching the canvas.
// - Fully procedural (no image assets required) with OPTIONAL
//   image-strip support per layer (see ASSET PRELOAD note below).
// ============================================================
(function () {
  'use strict';

  // Relative scroll factors vs cameraX/cameraY (world units -> px).
  var FAR_FACTOR = 0.15;
  var MID_FACTOR = 0.35;
  var NEAR_FACTOR = 0.60;

  // Horizontal wrap period in px (per layer, multiplied below).
  // Each layer tiles seamlessly: offset wraps with modulo, and
  // shapes are placed by deterministic hash inside one period.
  var WRAP_PX = 480;

  // Pixels of screen scroll per world unit at zoom 1.
  var PX_PER_UNIT = 24;

  // Deterministic 0..1 hash - identical layout every frame, so the
  // wrap is seamless and there is no per-frame allocation/randomness.
  function hash(n, seed) {
    var x = Math.sin(n * 127.1 + seed * 311.7) * 43758.5453;
    return x - Math.floor(x);
  }

  function mod(a, n) {
    return ((a % n) + n) % n;
  }

  // Camera-angle-aware scroll vector. Mirrors the relX/relY rotation
  // in worldToIso (index.html): angle 1 swaps/negates, 2 negates
  // both, 3 mirrors angle 1. Only the X component scrolls the
  // backdrop (vertical is fixed to the horizon by design).
  function angleScrollX(cameraX, cameraY, cameraAngle) {
    switch (cameraAngle % 4) {
      case 1: return -cameraY;
      case 2: return -cameraX;
      case 3: return cameraY;
      default: return cameraX;
    }
  }

  // ------------------------------------------------------------
  // Per-zone config table (keys match MAP_REGISTRY ids in
  // loadZoneMap + ZONE_ATMOSPHERE keys in index.html).
  // Lore mapping (vault/WORLD_LORE.md):
  // - meadows  : vibrant sunlight - sky, clouds, rolling hills
  // - sanctum  : submerged ruins - teal cavern glow + stalactites
  // - spire    : volcanic peak - ember sky + volcano silhouette
  // - chasm    : blizzard canyon - ice peaks + aurora
  // - rootways : world-tree roots - purple canopy + hanging roots
  // - aethelgard/gatewatch (town hubs): neutral -> null = zero cost
  //
  // Layer fields:
  //   factor : scroll factor (use FAR/MID/NEAR_* constants)
  //   ridge  : { color, amp, base, seed } silhouette band hanging
  //            from the horizon (amp/base in px at 360p, seed=hash)
  //   detail : { kind, colors[], count, seed, band:[topFrac,botFrac],
  //              size:[min,max], drift } decorative shapes.
  //            band is a fraction of horizonY (0=top .. 1=horizon).
  //   img    : OPTIONAL sprite key (window `sprites` map). When the
  //            image is loaded it is tiled instead of the procedural
  //            ridge; otherwise the procedural fallback is used.
  // ------------------------------------------------------------
  var PARALLAX_ZONES = {
    aethelgard: null,
    gatewatch: null,

    meadows: {
      sky: ['#7ec8f0', '#e8f6d8'],
      horizonFrac: 0.46,
      layers: [
        { factor: FAR_FACTOR,
          ridge: { color: '#a8d4b8', amp: 26, base: 44, seed: 11 },
          detail: { kind: 'cloud', colors: ['rgba(255,255,255,0.85)'], count: 7, seed: 12, band: [0.08, 0.55], size: [18, 42], drift: 0.08 } },
        { factor: MID_FACTOR,
          ridge: { color: '#7cb86e', amp: 34, base: 30, seed: 21 },
          detail: { kind: 'cloud', colors: ['rgba(255,255,255,0.7)'], count: 5, seed: 22, band: [0.25, 0.7], size: [14, 30], drift: 0.12 } },
        { factor: NEAR_FACTOR,
          ridge: { color: '#4e8f4a', amp: 22, base: 14, seed: 31 },
          detail: { kind: 'dots', colors: ['#fff6c8', '#ffffff'], count: 10, seed: 32, band: [0.4, 0.95], size: [1, 2.4], drift: 0.15 } }
      ]
    },

    sanctum: {
      sky: ['#062a33', '#0e5a63'],
      horizonFrac: 0.44,
      layers: [
        { factor: FAR_FACTOR,
          ridge: { color: '#0d3f4a', amp: 30, base: 46, seed: 41 },
          detail: { kind: 'glow', colors: ['rgba(91,232,216,0.5)', 'rgba(64,180,200,0.4)'], count: 8, seed: 42, band: [0.2, 0.9], size: [6, 18], drift: 0.05 } },
        { factor: MID_FACTOR,
          ridge: { color: '#093038', amp: 26, base: 30, seed: 51 },
          detail: { kind: 'stalactite', colors: ['#0a2e36'], count: 7, seed: 52, band: [0, 0.35], size: [14, 42], drift: 0 } },
        { factor: NEAR_FACTOR,
          ridge: { color: '#061e24', amp: 20, base: 14, seed: 61 },
          detail: { kind: 'dots', colors: ['#5be8d8', '#b2fff4'], count: 12, seed: 62, band: [0.3, 0.95], size: [1, 2.6], drift: 0.1 } }
      ]
    },

    spire: {
      sky: ['#2b0d0d', '#a03c1a'],
      horizonFrac: 0.48,
      layers: [
        { factor: FAR_FACTOR,
          ridge: { color: '#4a1a12', amp: 40, base: 48, seed: 71 },
          detail: { kind: 'dots', colors: ['#ff8a50', '#c8c8c8'], count: 10, seed: 72, band: [0.1, 0.9], size: [1, 2.4], drift: 0.3 } },
        { factor: MID_FACTOR,
          ridge: { color: '#33100c', amp: 34, base: 30, seed: 81 },
          detail: { kind: 'cone', colors: ['#200a08'], count: 3, seed: 82, band: [0.55, 0.9], size: [60, 110], drift: 0 } },
        { factor: NEAR_FACTOR,
          ridge: { color: '#180605', amp: 22, base: 14, seed: 91 },
          detail: { kind: 'dots', colors: ['#ffb060', '#ff6a30'], count: 14, seed: 92, band: [0.4, 1.0], size: [1.2, 3], drift: 0.45 } }
      ]
    },

    chasm: {
      sky: ['#0d1626', '#33507a'],
      horizonFrac: 0.44,
      layers: [
        { factor: FAR_FACTOR,
          ridge: { color: '#5a7396', amp: 44, base: 50, seed: 101 },
          detail: { kind: 'aurora', colors: ['rgba(120,255,190,0.35)', 'rgba(120,180,255,0.3)'], count: 3, seed: 102, band: [0.05, 0.5], size: [26, 60], drift: 0.06 } },
        { factor: MID_FACTOR,
          ridge: { color: '#3d5478', amp: 34, base: 30, seed: 111 },
          detail: { kind: 'dots', colors: ['#ffffff'], count: 6, seed: 112, band: [0.05, 0.4], size: [0.8, 1.8], drift: 0 } },
        { factor: NEAR_FACTOR,
          ridge: { color: '#22344f', amp: 22, base: 14, seed: 121 },
          detail: { kind: 'dots', colors: ['#ffffff', '#d8ecff'], count: 16, seed: 122, band: [0.1, 1.0], size: [1, 2.8], drift: 0.35 } }
      ]
    },

    rootways: {
      sky: ['#160a24', '#3d1554'],
      horizonFrac: 0.42,
      layers: [
        { factor: FAR_FACTOR,
          ridge: { color: '#2a1240', amp: 28, base: 46, seed: 131 },
          detail: { kind: 'blob', colors: ['rgba(60,20,90,0.9)'], count: 6, seed: 132, band: [0, 0.4], size: [40, 90], drift: 0 } },
        { factor: MID_FACTOR,
          ridge: { color: '#1d0b2e', amp: 24, base: 30, seed: 141 },
          detail: { kind: 'root', colors: ['#150821'], count: 8, seed: 142, band: [0, 0.45], size: [20, 60], drift: 0 } },
        { factor: NEAR_FACTOR,
          ridge: { color: '#100614', amp: 18, base: 14, seed: 151 },
          detail: { kind: 'dots', colors: ['#c17be0', '#8e4fb0'], count: 12, seed: 152, band: [0.3, 0.95], size: [1, 2.6], drift: 0.1 } }
      ]
    }
  };

  function getParallaxConfig(mapId) {
    if (!mapId) return null;
    return Object.prototype.hasOwnProperty.call(PARALLAX_ZONES, mapId)
      ? PARALLAX_ZONES[mapId]
      : null; // unknown zone -> zero cost, same as town hubs
  }

  // Paint the vertical sky gradient (2 stops, 1 fillRect - same cost
  // class as drawZoneAtmosphere's gradient in index.html).
  function paintSky(ctx, W, H, sky) {
    var grad = ctx.createLinearGradient(0, 0, 0, H);
    grad.addColorStop(0, sky[0]);
    grad.addColorStop(1, sky[1]);
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, W, H);
  }

  // Silhouette ridge band whose top edge is a sum of sines over the
  // wrap period (periodic -> tiles seamlessly). Hangs from horizonY
  // down past it by `base` px so it always covers the tile grid seam.
  function paintRidge(ctx, W, horizonY, period, scrollPx, ridge) {
    var step = 8;
    ctx.fillStyle = ridge.color;
    ctx.beginPath();
    ctx.moveTo(0, horizonY + ridge.base + ridge.amp + 4);
    for (var x = 0; x <= W + step; x += step) {
      var t = ((x + scrollPx) / period) * Math.PI * 2;
      var y = horizonY
        - ridge.amp * (0.55 * Math.sin(t + ridge.seed) + 0.3 * Math.sin(2 * t + ridge.seed * 1.7) + 0.15 * Math.sin(3 * t));
      ctx.lineTo(x, y);
    }
    ctx.lineTo(W, horizonY + ridge.base + ridge.amp + 4);
    ctx.closePath();
    ctx.fill();
  }

  // Optional image strip tiling. Returns true when an image was
  // drawn (caller then skips the procedural ridge for that layer).
  function paintImageStrip(ctx, W, horizonY, period, scrollPx, img, imgH) {
    if (!img || !img.complete || !img.naturalWidth) return false;
    var scale = imgH / img.height;
    var dw = img.width * scale;
    if (dw <= 0) return false;
    var startX = -mod(scrollPx, dw);
    for (var x = startX; x < W; x += dw) {
      ctx.drawImage(img, x, horizonY - imgH, dw, imgH);
    }
    return true;
  }

  // Decorative shapes, all positioned by hash() inside one wrap
  // period so horizontal tiling wraps seamlessly. `density` is 1
  // normally, 0.5 under lowGraphics (halves draws).
  function paintDetails(ctx, W, horizonY, period, scrollPx, detail, frame, density) {
    if (!detail || !detail.count) return 0;
    var count = Math.ceil(detail.count * density);
    var drawn = 0;
    var n;
    for (n = 0; n < count; n++) {
      var slot = hash(n, detail.seed) * period;
      var x = mod(slot - scrollPx + (detail.drift ? frame * detail.drift : 0), period);
      // Replicate the period across the screen width.
      for (var rep = x; rep < W + period; rep += period) {
        if (rep < -80 || rep > W + 80) continue;
        var bandY = detail.band[0] + hash(n + 0.5, detail.seed) * (detail.band[1] - detail.band[0]);
        var y = bandY * horizonY;
        var size = detail.size[0] + hash(n + 0.7, detail.seed) * (detail.size[1] - detail.size[0]);
        var color = detail.colors[Math.floor(hash(n + 0.9, detail.seed) * detail.colors.length) % detail.colors.length];
        drawDetailShape(ctx, detail.kind, rep, y, size, color, horizonY, frame, n, detail.seed);
        drawn++;
      }
    }
    return drawn;
  }

  function drawDetailShape(ctx, kind, x, y, size, color, horizonY, frame, n, seed) {
    ctx.fillStyle = color;
    switch (kind) {
      case 'cloud': {
        // 3-ellipse puff. y wobble is time-based, not camera-based,
        // so clouds never fight the fixed-horizon rule.
        var wob = Math.sin(frame * 0.01 + n) * 2;
        ctx.globalAlpha = 0.85;
        ctx.beginPath();
        ctx.ellipse(x, y + wob, size, size * 0.38, 0, 0, Math.PI * 2);
        ctx.ellipse(x - size * 0.55, y + size * 0.12 + wob, size * 0.6, size * 0.28, 0, 0, Math.PI * 2);
        ctx.ellipse(x + size * 0.55, y + size * 0.12 + wob, size * 0.62, size * 0.3, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1;
        break;
      }
      case 'glow': {
        var pulse = 0.7 + 0.3 * Math.sin(frame * 0.03 + n * 1.7);
        ctx.globalAlpha = 0.5 * pulse;
        ctx.beginPath();
        ctx.arc(x, y, size, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1;
        break;
      }
      case 'dots': {
        ctx.globalAlpha = 0.8;
        ctx.beginPath();
        ctx.arc(x, y, size * 0.5, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1;
        break;
      }
      case 'stalactite': {
        // Hangs from the top of the screen (cavern ceiling).
        ctx.beginPath();
        ctx.moveTo(x - size * 0.3, 0);
        ctx.lineTo(x + size * 0.3, 0);
        ctx.lineTo(x, size);
        ctx.closePath();
        ctx.fill();
        break;
      }
      case 'root': {
        // Tapered hanging root from the canopy top, slight sway.
        var sway = Math.sin(frame * 0.008 + n) * 4;
        ctx.beginPath();
        ctx.moveTo(x - size * 0.16, 0);
        ctx.lineTo(x + size * 0.16, 0);
        ctx.lineTo(x + sway, size);
        ctx.closePath();
        ctx.fill();
        break;
      }
      case 'blob': {
        // Canopy mass along the top edge.
        ctx.globalAlpha = 0.95;
        ctx.beginPath();
        ctx.ellipse(x, 0, size, size * 0.32, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1;
        break;
      }
      case 'cone': {
        // Volcano cone silhouette rising to just under the horizon.
        var h = size;
        var w = size * 0.9;
        ctx.beginPath();
        ctx.moveTo(x - w / 2, horizonY + 4);
        ctx.lineTo(x, horizonY - h);
        ctx.lineTo(x + w / 2, horizonY + 4);
        ctx.closePath();
        ctx.fill();
        // Snow/ash cap notch.
        ctx.fillStyle = 'rgba(255,120,50,0.85)';
        ctx.beginPath();
        ctx.moveTo(x - w * 0.12, horizonY - h * 0.82);
        ctx.lineTo(x, horizonY - h);
        ctx.lineTo(x + w * 0.12, horizonY - h * 0.82);
        ctx.closePath();
        ctx.fill();
        break;
      }
      case 'aurora': {
        // Translucent diagonal band high in the sky.
        ctx.save();
        ctx.globalAlpha = 0.5 + 0.15 * Math.sin(frame * 0.01 + n * 2.1);
        ctx.translate(x, y);
        ctx.rotate(-0.35);
        ctx.fillRect(-size * 2.2, -size * 0.28, size * 4.4, size * 0.56);
        ctx.restore();
        break;
      }
      default: {
        ctx.beginPath();
        ctx.arc(x, y, size * 0.5, 0, Math.PI * 2);
        ctx.fill();
        break;
      }
    }
  }

  // ------------------------------------------------------------
  // Main entry. `state` may be omitted when running inside
  // index.html (falls back to the page globals); pass it
  // explicitly from tests or other hosts.
  // Returns the number of layer draws (0 = zero cost, no bg).
  // ------------------------------------------------------------
  function drawParallax(ctx, canvas, state) {
    var g = (typeof globalThis !== 'undefined') ? globalThis : this;
    state = state || {};
    var cameraX = (state.cameraX != null) ? state.cameraX : (g.cameraX || 0);
    var cameraY = (state.cameraY != null) ? state.cameraY : (g.cameraY || 0);
    var cameraAngle = (state.cameraAngle != null) ? state.cameraAngle : (g.cameraAngle || 0);
    var cameraZoom = (state.cameraZoom != null) ? state.cameraZoom : (g.cameraZoom || 1);
    var mapId = (state.currentMapId !== undefined) ? state.currentMapId : g.currentMapId;
    var GFX = state.GFX || g.GFX || null;
    var frame = (state.frameCount != null) ? state.frameCount : (g.frameCount || 0);

    var cfg = getParallaxConfig(mapId);
    if (!cfg || !cfg.layers || !cfg.layers.length) return 0; // town hubs / unknown: zero cost

    var W = canvas.width, H = canvas.height;
    var horizonY = Math.floor(H * (cfg.horizonFrac || 0.44)); // vertical fixed to horizon
    var low = !!(GFX && GFX.lowGraphics);
    var particlesOn = !GFX || GFX.particles !== false;
    var density = low ? 0.5 : 1;

    var scrollBase = angleScrollX(cameraX, cameraY, cameraAngle) * PX_PER_UNIT * cameraZoom;
    var sprites = (typeof window !== 'undefined' && window.sprites) || g.sprites || null;

    paintSky(ctx, W, H, cfg.sky);

    var draws = 1; // sky gradient
    for (var i = 0; i < cfg.layers.length; i++) {
      var layer = cfg.layers[i];
      var isFar = (i === 0);
      // GFX gate: far layer is ambient-grade decor - skip it when
      // particles are off or lowGraphics is on (same convention as
      // the ambient particle pool in index.html).
      if (isFar && (!particlesOn || low)) continue;
      var period = WRAP_PX * (1 + i * 0.35);
      var scrollPx = mod(scrollBase * layer.factor, period);

      var imgDrawn = false;
      if (layer.img && sprites && sprites[layer.img]) {
        imgDrawn = paintImageStrip(ctx, W, horizonY, period, scrollPx, sprites[layer.img], Math.floor(H * 0.30));
      }
      if (!imgDrawn && layer.ridge) {
        paintRidge(ctx, W, horizonY, period, scrollPx, layer.ridge);
        draws++;
      } else if (imgDrawn) {
        draws++;
      }
      if (layer.detail) {
        draws += paintDetails(ctx, W, horizonY, period, scrollPx, layer.detail, frame, density);
      }
    }
    return draws;
  }

  // Public surface + test hook.
  var api = {
    FAR_FACTOR: FAR_FACTOR,
    MID_FACTOR: MID_FACTOR,
    NEAR_FACTOR: NEAR_FACTOR,
    PARALLAX_ZONES: PARALLAX_ZONES,
    getParallaxConfig: getParallaxConfig,
    drawParallax: drawParallax
  };

  if (typeof window !== 'undefined') window.ZaggersParallax = api;
  if (typeof globalThis !== 'undefined') globalThis.ZaggersParallax = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})();
