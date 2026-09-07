/* ZaggersAudio.js — procedural WebAudio synth, zero audio files.
 * Additive: no existing index.html logic is touched. Integration is:
 *   1x <script src="audio/ZaggersAudio.js"></script> tag in web/index.html
 *   + 3 guarded call sites (attack hit, purchase, zone change — see footer).
 * GFX.lowGraphics (window.ZaggersGraphics, index.html ~L988) halves voices.
 */
(function () {
  'use strict';

  var ctx = null;          // lazy AudioContext (autoplay policy: init on gesture)
  var masterGain = null;
  var sfxGain = null;
  var bgmGain = null;
  var noiseBuf = null;     // shared 1s white-noise buffer
  var ambientNodes = null; // { src, filter, gain, lfo, lfoGain } for current zone pad
  var currentZone = null;
  var muted = false;
  var volume = 0.8;        // master 0..1
  var activeVoices = 0;

  function maxVoices() {
    // GFX.lowGraphics halves voices (mirrors AMBIENT_PARTICLE_CAP halving).
    var low = window.ZaggersGraphics && window.ZaggersGraphics.lowGraphics;
    return low ? 6 : 12;
  }

  function ensureCtx() {
    if (ctx) {
      if (ctx.state === 'suspended') ctx.resume().catch(function () {});
      return ctx;
    }
    var AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return null;
    ctx = new AC();
    masterGain = ctx.createGain();
    masterGain.gain.value = muted ? 0 : volume;
    masterGain.connect(ctx.destination);
    sfxGain = ctx.createGain();
    sfxGain.gain.value = 0.9;
    sfxGain.connect(masterGain);
    bgmGain = ctx.createGain();
    bgmGain.gain.value = 0.35;
    bgmGain.connect(masterGain);
    // Shared white-noise buffer (1s, reused by swing/hit + ambient pads).
    noiseBuf = ctx.createBuffer(1, ctx.sampleRate, ctx.sampleRate);
    var d = noiseBuf.getChannelData(0);
    for (var i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
    if (ctx.state === 'suspended') ctx.resume().catch(function () {});
    return ctx;
  }

  // Lazy init on first click/keydown/touch (autoplay policy). Safe to call often.
  function unlock() { ensureCtx(); }
  if (typeof window !== 'undefined') {
    ['pointerdown', 'keydown', 'touchstart'].forEach(function (ev) {
      window.addEventListener(ev, unlock, { once: true, passive: true });
    });
  }

  // --- primitive voices -------------------------------------------------
  function blip(opts) {
    // opts: { type, f0, f1, t, dur, vol, when }
    if (!ensureCtx()) return;
    if (activeVoices >= maxVoices()) return; // lowGraphics voice cap
    activeVoices++;
    var t0 = ctx.currentTime + (opts.when || 0);
    var osc = ctx.createOscillator();
    var g = ctx.createGain();
    osc.type = opts.type || 'sine';
    osc.frequency.setValueAtTime(opts.f0, t0);
    if (opts.f1 && opts.f1 !== opts.f0) {
      osc.frequency.exponentialRampToValueAtTime(Math.max(1, opts.f1), t0 + (opts.t || opts.dur || 0.15));
    }
    var dur = opts.dur || 0.15;
    var vol = opts.vol != null ? opts.vol : 0.5;
    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime(vol, t0 + 0.008);
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
    osc.connect(g);
    g.connect(sfxGain);
    osc.start(t0);
    osc.stop(t0 + dur + 0.05);
    osc.onended = function () { activeVoices = Math.max(0, activeVoices - 1); };
  }

  function noiseBurst(opts) {
    // opts: { dur, vol, fType, f0, f1, q, when }
    if (!ensureCtx()) return;
    if (activeVoices >= maxVoices()) return;
    activeVoices++;
    var t0 = ctx.currentTime + (opts.when || 0);
    var src = ctx.createBufferSource();
    src.buffer = noiseBuf;
    src.loop = true;
    var flt = ctx.createBiquadFilter();
    flt.type = opts.fType || 'bandpass';
    flt.frequency.setValueAtTime(opts.f0 || 1200, t0);
    if (opts.f1) flt.frequency.exponentialRampToValueAtTime(Math.max(10, opts.f1), t0 + (opts.dur || 0.2));
    flt.Q.value = opts.q || 1.0;
    var g = ctx.createGain();
    var dur = opts.dur || 0.2;
    var vol = opts.vol != null ? opts.vol : 0.4;
    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime(vol, t0 + 0.01);
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
    src.connect(flt);
    flt.connect(g);
    g.connect(sfxGain);
    src.start(t0);
    src.stop(t0 + dur + 0.05);
    src.onended = function () { activeVoices = Math.max(0, activeVoices - 1); };
  }

  // --- SFX set (oscillator/noise recipes, no files) ----------------------
  var SFX = {
    swing: function () { noiseBurst({ dur: 0.18, vol: 0.30, fType: 'bandpass', f0: 3000, f1: 500, q: 1.2 }); },
    hit: function () {
      blip({ type: 'square', f0: 220, f1: 80, dur: 0.14, vol: 0.45 });
      noiseBurst({ dur: 0.08, vol: 0.25, fType: 'highpass', f0: 1800 });
    },
    crit: function () {
      blip({ type: 'sawtooth', f0: 440, f1: 110, dur: 0.22, vol: 0.55 });
      noiseBurst({ dur: 0.12, vol: 0.30, fType: 'highpass', f0: 2200 });
      blip({ type: 'sine', f0: 880, f1: 1320, dur: 0.12, vol: 0.25, when: 0.03 });
    },
    coin: function () {
      blip({ type: 'sine', f0: 988, dur: 0.09, vol: 0.4 });          // B5
      blip({ type: 'sine', f0: 1319, dur: 0.22, vol: 0.4, when: 0.08 }); // E6
    },
    levelup: function () {
      var seq = [523, 659, 784, 1047]; // C5 E5 G5 C6
      seq.forEach(function (f, i) {
        blip({ type: 'triangle', f0: f, dur: 0.22, vol: 0.45, when: i * 0.11 });
      });
    },
    ui: function () { blip({ type: 'sine', f0: 660, f1: 660, dur: 0.06, vol: 0.25 }); }
  };

  function play(name) {
    var fn = SFX[name];
    if (fn) { try { fn(); } catch (e) { /* audio must never break gameplay */ } }
    return !!fn;
  }

  // --- per-zone ambient pad (looped filtered noise + slow LFO) -----------
  // Keys match MAP_REGISTRY / ZONE_ATMOSPHERE ids in index.html exactly.
  var ZONE_PAD = {
    aethelgard: { filterFreq: 600,  type: 'lowpass', baseGain: 0.05, lfoRate: 0.07, lfoDepth: 150 },
    gatewatch:  { filterFreq: 700,  type: 'lowpass', baseGain: 0.05, lfoRate: 0.08, lfoDepth: 150 },
    meadows:    { filterFreq: 1200, type: 'bandpass', baseGain: 0.06, lfoRate: 0.10, lfoDepth: 300 },
    sanctum:    { filterFreq: 500,  type: 'lowpass', baseGain: 0.08, lfoRate: 0.05, lfoDepth: 120 },
    spire:      { filterFreq: 300,  type: 'lowpass', baseGain: 0.09, lfoRate: 0.04, lfoDepth: 90 },
    chasm:      { filterFreq: 2000, type: 'highpass', baseGain: 0.05, lfoRate: 0.12, lfoDepth: 400 },
    rootways:   { filterFreq: 350,  type: 'lowpass', baseGain: 0.09, lfoRate: 0.06, lfoDepth: 110 }
  };

  function stopAmbient() {
    if (!ambientNodes) return;
    try {
      var n = ambientNodes;
      ambientNodes = null;
      n.gain.gain.cancelScheduledValues(ctx.currentTime);
      n.gain.gain.setTargetAtTime(0.0001, ctx.currentTime, 0.4);
      var nodes = n;
      setTimeout(function () {
        try { nodes.src.stop(); } catch (e) {}
        try { nodes.lfo.stop(); } catch (e) {}
        try { nodes.src.disconnect(); nodes.filter.disconnect(); nodes.gain.disconnect(); } catch (e) {}
      }, 1200);
    } catch (e) { ambientNodes = null; }
  }

  function playBgm(zone) {
    if (!ensureCtx()) return false;
    if (zone === currentZone && ambientNodes) return true;
    stopAmbient();
    currentZone = zone || null;
    var cfg = ZONE_PAD[currentZone];
    if (!cfg) return true; // unknown/silent zone: just stop previous pad
    // lowGraphics: thinner pad (lower gain, no LFO depth) to save CPU.
    var low = window.ZaggersGraphics && window.ZaggersGraphics.lowGraphics;
    var src = ctx.createBufferSource();
    src.buffer = noiseBuf;
    src.loop = true;
    var filter = ctx.createBiquadFilter();
    filter.type = cfg.type;
    filter.frequency.value = cfg.filterFreq;
    filter.Q.value = 0.8;
    var gain = ctx.createGain();
    gain.gain.value = 0.0001;
    gain.gain.setTargetAtTime(low ? cfg.baseGain * 0.5 : cfg.baseGain, ctx.currentTime, 1.2);
    var lfo = ctx.createOscillator();
    lfo.type = 'sine';
    lfo.frequency.value = cfg.lfoRate;
    var lfoGain = ctx.createGain();
    lfoGain.gain.value = low ? cfg.lfoDepth * 0.4 : cfg.lfoDepth;
    lfo.connect(lfoGain);
    lfoGain.connect(filter.frequency);
    src.connect(filter);
    filter.connect(gain);
    gain.connect(bgmGain);
    src.start();
    lfo.start();
    ambientNodes = { src: src, filter: filter, gain: gain, lfo: lfo, lfoGain: lfoGain };
    return true;
  }

  // --- master controls ----------------------------------------------------
  function setVolume(v) {
    volume = Math.max(0, Math.min(1, Number(v) || 0));
    if (masterGain && ctx) masterGain.gain.setTargetAtTime(muted ? 0 : volume, ctx.currentTime, 0.05);
  }
  function setMuted(m) {
    muted = !!m;
    if (masterGain && ctx) masterGain.gain.setTargetAtTime(muted ? 0 : volume, ctx.currentTime, 0.02);
  }
  function toggleMute() { setMuted(!muted); return muted; }

  window.ZaggersAudio = {
    unlock: unlock,
    play: play,
    playBgm: playBgm,
    stopAmbient: stopAmbient,
    setVolume: setVolume,
    setMuted: setMuted,
    toggleMute: toggleMute,
    get muted() { return muted; },
    get zone() { return currentZone; },
    // aliases for call-site readability
    swing: function () { return play('swing'); },
    hit: function () { return play('hit'); },
    crit: function () { return play('crit'); },
    coin: function () { return play('coin'); },
    levelup: function () { return play('levelup'); },
    ui: function () { return play('ui'); }
  };
})();

/* ---- index.html integration (3 calls + 1 script tag, additive) ----
 * 1. In <head> or before the main <script>: <script src="audio/ZaggersAudio.js"></script>
 *
 * 2a. Attack hit — end of applyMonsterHit(), after spawnSkillImpact(...):
 *       if (window.ZaggersAudio) ZaggersAudio.play(result && result.crit ? 'crit' : 'hit');
 *     (or always 'hit' if result.crit is unavailable) + ZaggersAudio.play('swing') in triggerAttack().
 *
 * 2b. Purchase — end of buyItem() / buyItemById() success branch:
 *       if (window.ZaggersAudio) ZaggersAudio.play('coin');
 *     (+ 'levelup' wherever grantXp()/level-up chat message fires.)
 *
 * 2c. Zone change — end of applyZoneMapData(), after showDistrictBanner(...):
 *       if (window.ZaggersAudio) ZaggersAudio.playBgm(mapId);
 */
