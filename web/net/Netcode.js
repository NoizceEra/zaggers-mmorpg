'use strict';
/**
 * Netcode.js — P0 netcode for the Zaggers web client (parallax-style standalone).
 *
 * Mirrors scripts/net_snapshot.gd with the same tuning:
 *   SEND 12Hz max  |  heartbeat 250ms  |  move epsilon 2px  |
 *   remote lerp 10/s (framerate-independent)  |  snap past 200px.
 *
 * Zero dependencies, no bundler needed. Browser:
 *   <script src="net/Netcode.js"></script>
 *   const netcode = new SnapshotNetcode();
 * Node (tests): const { SnapshotNetcode } = require('./web/net/Netcode.js');
 *
 * Integration snippet: see scripts/net_snapshot.patch.md §4.
 */
(function (global) {
  var SEND_INTERVAL_MS = 1000 / 12;  // 12Hz accumulator cap
  var HEARTBEAT_MS = 250;            // forced snapshot while idle
  var MOVE_EPSILON_PX = 2;           // min displacement counting as "moved"
  var REMOTE_LERP_RATE = 10;         // per-second exponential lerp
  var REMOTE_SNAP_DIST_PX = 200;     // teleport instead of lerp past this

  function nowMs(clock) {
    if (typeof clock === 'function') return clock();
    if (typeof performance !== 'undefined' && performance.now) return performance.now();
    return Date.now();
  }

  function dist2(ax, ay, bx, by) {
    var dx = ax - bx;
    var dy = ay - by;
    return Math.sqrt(dx * dx + dy * dy);
  }

  /**
   * @param {function} [clock] injectable ms clock (tests); defaults to performance.now/Date.now.
   */
  function SnapshotNetcode(clock) {
    this._clock = clock || null;
    this._accumMs = SEND_INTERVAL_MS; // first snapshot goes out immediately
    this._sinceSendMs = HEARTBEAT_MS;
    this._lastSendMs = 0;
    this._hasSentOnce = false;
    this._lastX = 0;
    this._lastY = 0;
    this._lastDir = '';
    this._targets = new Map(); // id -> { x, y, dir }
  }

  SnapshotNetcode.SEND_INTERVAL_MS = SEND_INTERVAL_MS;
  SnapshotNetcode.HEARTBEAT_MS = HEARTBEAT_MS;
  SnapshotNetcode.MOVE_EPSILON_PX = MOVE_EPSILON_PX;
  SnapshotNetcode.REMOTE_LERP_RATE = REMOTE_LERP_RATE;
  SnapshotNetcode.REMOTE_SNAP_DIST_PX = REMOTE_SNAP_DIST_PX;

  /** Re-arm after spawn/teleport so the next snapshot goes out immediately. */
  SnapshotNetcode.prototype.resetSender = function (x, y, dir) {
    this._accumMs = SEND_INTERVAL_MS;
    this._sinceSendMs = HEARTBEAT_MS;
    this._lastX = x;
    this._lastY = y;
    this._lastDir = dir || '';
    this._hasSentOnce = true;
  };

  /**
   * Pure gate. dtMs: ms since last call (frame delta).
   * True when a snapshot should be emitted this tick.
   */
  SnapshotNetcode.prototype.shouldSend = function (x, y, dir, dtMs) {
    var dt = dtMs > 0 ? dtMs : 0;
    this._accumMs += dt;
    this._sinceSendMs += dt;
    if (this._accumMs < SEND_INTERVAL_MS) return false;
    if (!this._hasSentOnce) return true;
    if ((dir || '') !== this._lastDir) return true;
    if (this._sinceSendMs >= HEARTBEAT_MS) return true;
    return dist2(x, y, this._lastX, this._lastY) > MOVE_EPSILON_PX;
  };

  /**
   * Throttled sender. Calls sendFn({x, y, dir, t}) when due; returns bool sent.
   * t is the sender timestamp (handy for future server reconciliation).
   */
  SnapshotNetcode.prototype.tickLocal = function (x, y, dir, sendFn, dtMs) {
    if (!this.shouldSend(x, y, dir, dtMs)) return false;
    var t = nowMs(this._clock);
    if (typeof sendFn === 'function') sendFn({ x: x, y: y, dir: dir || 'down', t: t });
    this._accumMs = 0;
    this._sinceSendMs = 0;
    this._lastSendMs = t;
    this._lastX = x;
    this._lastY = y;
    this._lastDir = dir || '';
    this._hasSentOnce = true;
    return true;
  };

  /** Record the latest authoritative position for a remote. */
  SnapshotNetcode.prototype.setRemoteTarget = function (id, x, y, dir) {
    if (id == null) return;
    this._targets.set(String(id), { x: Number(x) || 0, y: Number(y) || 0, dir: dir || 'down' });
  };

  SnapshotNetcode.prototype.hasRemote = function (id) {
    return this._targets.has(String(id));
  };

  SnapshotNetcode.prototype.removeRemote = function (id) {
    this._targets.delete(String(id));
  };

  SnapshotNetcode.prototype.clearRemotes = function () {
    this._targets.clear();
  };

  SnapshotNetcode.prototype.remoteIds = function () {
    return Array.from(this._targets.keys());
  };

  /**
   * One interpolation step. Returns { x, y, snapped } — never mutates inputs.
   * Teleports past SNAP distance (spawn/respawn/loss gap), else exponential
   * lerp at 10/s, framerate-independent via 1 - exp(-10*dt).
   */
  SnapshotNetcode.prototype.stepRemote = function (curX, curY, id, dtSeconds) {
    var tgt = this._targets.get(String(id));
    if (!tgt) return { x: curX, y: curY, snapped: false };
    var dt = dtSeconds > 0 ? dtSeconds : 0;
    var d = dist2(curX, curY, tgt.x, tgt.y);
    if (d > REMOTE_SNAP_DIST_PX) return { x: tgt.x, y: tgt.y, snapped: true };
    var t = 1 - Math.exp(-REMOTE_LERP_RATE * dt);
    if (t < 0) t = 0;
    if (t > 1) t = 1;
    return { x: curX + (tgt.x - curX) * t, y: curY + (tgt.y - curY) * t, snapped: false };
  };

  /**
   * Step every entry of a Map/Object of { x, y } render positions in place.
   * Entries without a known target are left untouched (e.g. locally-spawned
   * predictions). Returns the store for chaining.
   */
  SnapshotNetcode.prototype.stepAll = function (remotes, dtSeconds) {
    var self = this;
    function stepEntry(id, entry) {
      if (!entry || typeof entry.x !== 'number' || typeof entry.y !== 'number') return;
      if (!self._targets.has(String(id))) return;
      var out = self.stepRemote(entry.x, entry.y, id, dtSeconds);
      entry.x = out.x;
      entry.y = out.y;
      var tgt = self._targets.get(String(id));
      if (tgt) entry.dir = tgt.dir;
    }
    if (remotes instanceof Map) {
      remotes.forEach(function (entry, id) { stepEntry(id, entry); });
    } else if (remotes) {
      Object.keys(remotes).forEach(function (id) { stepEntry(id, remotes[id]); });
    }
    return remotes;
  };

  // UMD-ish export: browser global + CommonJS.
  global.SnapshotNetcode = SnapshotNetcode;
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
      SnapshotNetcode: SnapshotNetcode,
      SEND_INTERVAL_MS: SEND_INTERVAL_MS,
      HEARTBEAT_MS: HEARTBEAT_MS,
      MOVE_EPSILON_PX: MOVE_EPSILON_PX,
      REMOTE_LERP_RATE: REMOTE_LERP_RATE,
      REMOTE_SNAP_DIST_PX: REMOTE_SNAP_DIST_PX,
    };
  }
})(typeof window !== 'undefined' ? window : globalThis);
