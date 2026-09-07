/* Zaggers Starter Quests — 3-quest tutorial arc for Aethelgard newcomers.
 *
 * Arc (vault/WORLD_LORE.md: Aethelgard sanctuary, Kafra Supply Depot):
 *   Q1 "First Papers"   — Talk to the Kestrel Consignment Steward (Kafra) in
 *                          Aethelgard Grand Plaza (npc id kafra_kestrel).
 *   Q2 "Downs Patrol"   — Defeat 3 Bellflower Glooplings (Whispering Meadows /
 *                          Gatewatch fields). Reward: Bellflower Shortsword.
 *   Q3 "Oath of the Bell" — Equip the Bellflower Shortsword and reach Base Lv 5.
 *                          Reward: Lv5 induction ceremony + supplies.
 *
 * Hooks (existing web/index.html globals — no edits to index.html required
 * beyond the one start() call + script tag, see scripts/tutorial_quests.md):
 *   chatSystem(msg, color, kind), addToInventory(itemId, qty), player.level,
 *   player.equipment, openNpcDialog(npc), grantKillRewards(m), equipItem(id).
 * Progress persists in localStorage under STORE_KEY so reloads resume.
 *
 * Loading: classic script (not a module) so bare globals resolve:
 *   <script src="tutorial/StarterQuests.js"></script>
 * Auto-wraps runtime hooks on DOMContentLoaded (with retries while the main
 * inline script is still booting); start() begins the arc after character
 * creation. Safe no-ops when index.html globals are absent (e.g. node --check
 * or Godot webview preload).
 */
(function (global) {
  'use strict';

  var STORE_KEY = 'zaggers_starter_quests_v1';

  var KAFRA_IDS = ['kafra_kestrel'];
  var KAFRA_SPRITES = ['npc_kafra'];
  var GLOOP_SPRITES = ['gloopling_bellflower_ff'];
  var GLOOP_NAMES = ['bellflower gloopling'];
  var GLOOP_DB_IDS = ['gloopling_bellflower'];
  var SWORD_ID = 'bellflower_shortsword';
  var KILLS_REQUIRED = 3;
  var LEVEL_REQUIRED = 5;

  var state = load() || fresh();

  function fresh() {
    return { started: false, q1: false, kills: 0, q2: false, q3: false, done: false };
  }

  function load() {
    try {
      var raw = global.localStorage && global.localStorage.getItem(STORE_KEY);
      if (!raw) return null;
      var s = JSON.parse(raw);
      if (!s || typeof s !== 'object') return null;
      return s;
    } catch (e) { return null; }
  }

  function save() {
    try {
      if (global.localStorage) global.localStorage.setItem(STORE_KEY, JSON.stringify(state));
    } catch (e) {}
  }

  function say(msg, color, kind) {
    try {
      if (typeof global.chatSystem === 'function') global.chatSystem(msg, color, kind);
    } catch (e) {}
  }

  function give(itemId, qty) {
    try {
      if (typeof global.addToInventory === 'function') global.addToInventory(itemId, qty || 1);
    } catch (e) {}
  }

  function celebrate(text) {
    try {
      var p = global.player;
      if (p && global.floatingTexts && Array.isArray(global.floatingTexts)) {
        global.floatingTexts.push({ wx: p.wx, wy: p.wy, offsetY: 30, text: text, color: '#ffd54f', life: 70 });
      }
    } catch (e) {}
  }

  function playerLevel() {
    try { return (global.player && global.player.level) || 1; } catch (e) { return 1; }
  }

  function swordEquipped() {
    try {
      var p = global.player;
      return !!(p && p.equipment && p.equipment.weapon === SWORD_ID);
    } catch (e) { return false; }
  }

  function isKafra(npc) {
    if (!npc) return false;
    if (KAFRA_IDS.indexOf(npc.id) !== -1) return true;
    if (KAFRA_SPRITES.indexOf(npc.sprite) !== -1) return true;
    return /kafra|kestrel consignment/i.test(npc.name || npc.dialogHeader || '');
  }

  function isGloopling(m) {
    if (!m) return false;
    if (GLOOP_SPRITES.indexOf(m.sprite) !== -1) return true;
    if (GLOOP_DB_IDS.indexOf(m.id) !== -1) return true;
    return GLOOP_NAMES.indexOf(String(m.name || '').toLowerCase()) !== -1;
  }

  function briefQ1() {
    say('📜 <strong>Starter Quest 1/3 — First Papers:</strong> speak with the <strong>Kestrel Consignment Steward (Kafra)</strong> in Aethelgard Grand Plaza (south-west depot, by the save crystal).', '#ffe082', 'quest');
  }

  function briefQ2() {
    say('📜 <strong>Starter Quest 2/3 — Downs Patrol:</strong> defeat <strong>3 Bellflower Glooplings</strong> past the Gatewatch militia picket, in the Whispering Meadows fields. (' + state.kills + '/' + KILLS_REQUIRED + ')', '#ffe082', 'quest');
  }

  function briefQ3() {
    say('📜 <strong>Starter Quest 3/3 — Oath of the Bell:</strong> open Equip [I], equip the <strong>Bellflower Shortsword</strong>, and reach <strong>Base Lv ' + LEVEL_REQUIRED + '</strong> to swear your oath at the Aetherite Obelisk.', '#ffe082', 'quest');
  }

  function completeQ1() {
    if (state.q1) return;
    state.q1 = true; save();
    say('✅ <strong>First Papers complete!</strong> Your Kafra registration is stamped. The Steward nods toward the Rampart Gate: “The Downs need blades, recruit.”', '#81c784', 'quest');
    celebrate('QUEST 1/3 COMPLETE!');
    briefQ2();
  }

  function completeQ2() {
    if (state.q2) return;
    state.q2 = true; save();
    give(SWORD_ID, 1);
    say('✅ <strong>Downs Patrol complete!</strong> The militia salutes you. Issued: <strong>Bellflower Shortsword</strong> — open Equip [I] to wield it.', '#81c784', 'quest');
    celebrate('QUEST 2/3 COMPLETE!');
    briefQ3();
  }

  function completeQ3() {
    if (state.q3) return;
    state.q3 = true; state.done = true; save();
    give('red_potion', 3);
    celebrate('🎔 OATH SWORN — LV ' + LEVEL_REQUIRED + '!');
    say('🎔 <strong>Oath of the Bell complete!</strong> Beneath the Aetherite Obelisk the plaza falls silent as you swear the adventurer’s oath. Aethelgard stands behind you, recruit — the five realms lie ahead. ' +
      'Supplies issued: <strong>3× Red Potion</strong>. The Elder’s Ordwin hunt (an optional veteran quest) awaits when you feel ready.', '#ffd54f', 'quest');
  }

  function checkQ3() {
    if (!state.started || state.done || !state.q2 || state.q3) return;
    if (swordEquipped() && playerLevel() >= LEVEL_REQUIRED) completeQ3();
  }

  // Wrap a global hook once so quest events flow through the existing systems
  // (openNpcDialog / grantKillRewards / equipItem / grantXp in index.html).
  function wrapOnce(name, wrapper) {
    try {
      var fn = global[name];
      if (typeof fn !== 'function' || fn.__starterQuestsWrapped) return false;
      var wrapped = wrapper(fn);
      wrapped.__starterQuestsWrapped = true;
      global[name] = wrapped;
      return true;
    } catch (e) { return false; }
  }

  function installHooks() {
    wrapOnce('openNpcDialog', function (orig) {
      return function (npc) {
        try {
          if (state.started && !state.q1 && isKafra(npc)) {
            var r = orig.apply(this, arguments);
            completeQ1();
            return r;
          }
        } catch (e) {}
        return orig.apply(this, arguments);
      };
    });
    wrapOnce('grantKillRewards', function (orig) {
      return function (m) {
        var r = orig.apply(this, arguments);
        try {
          if (state.started && state.q1 && !state.q2 && isGloopling(m)) {
            state.kills = Math.min(KILLS_REQUIRED, (state.kills || 0) + 1);
            save();
            if (state.kills >= KILLS_REQUIRED) completeQ2();
            else say('🌸 Gloopling pacified (' + state.kills + '/' + KILLS_REQUIRED + ').', '#81c784', 'quest');
          }
          checkQ3();
        } catch (e) {}
        return r;
      };
    });
    wrapOnce('equipItem', function (orig) {
      return function (itemId) {
        var r = orig.apply(this, arguments);
        try { checkQ3(); } catch (e) {}
        return r;
      };
    });
    wrapOnce('grantXp', function (orig) {
      return function (amount) {
        var r = orig.apply(this, arguments);
        try { checkQ3(); } catch (e) {}
        return r;
      };
    });
  }

  var api = {
    STORE_KEY: STORE_KEY,
    start: function () {
      installHooks();
      if (!state.started) {
        state = fresh();
        state.started = true;
        save();
        say('🛡️ <strong>Starter Quests begun!</strong> The Kafra Steward asked for you by name — a new blade in Aethelgard is always noticed.', '#ffd54f', 'quest');
        briefQ1();
      } else if (!state.done) {
        // Resume after reload: re-brief current step.
        if (!state.q1) briefQ1();
        else if (!state.q2) briefQ2();
        else briefQ3();
      }
      return api.status();
    },
    status: function () { return { started: state.started, q1: state.q1, kills: state.kills, q2: state.q2, q3: state.q3, done: state.done }; },
    reset: function () { state = fresh(); save(); return api.status(); },
    // Exposed for tests / Godot webview bridge.
    _isKafra: isKafra,
    _isGloopling: isGloopling
  };

  global.StarterQuests = api;

  // Self-install hooks as soon as the main inline script's globals exist.
  // The start() call after character creation is still the canonical entry.
  var attempts = 0;
  function boot() {
    installHooks();
    attempts += 1;
    if (attempts < 40 &&
        (typeof global.openNpcDialog !== 'function' || typeof global.grantKillRewards !== 'function')) {
      setTimeout(boot, 500);
    }
  }
  if (typeof global.document !== 'undefined') {
    if (global.document.readyState === 'loading') {
      global.document.addEventListener('DOMContentLoaded', boot);
    } else {
      boot();
    }
  }

  // Node smoke-test entry (node --check only parses; this never runs there).
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})(typeof window !== 'undefined' ? window : globalThis);
