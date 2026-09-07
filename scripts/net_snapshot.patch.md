# P0 Netcode — Research + Integration Patch Notes

> `player.gd` / `world.gd` / `network_manager.gd` are **NOT** modified by this
> change. This file is the only integration guide: copy the `OLD → NEW`
> blocks below into the listed line ranges. New files:
> `scripts/net_snapshot.gd`, `scripts/network_ext.gd`, `web/net/Netcode.js`.

---

## §0 Research — current behaviour (read 2026-09-07)

| # | File:line | Finding |
|---|-----------|---------|
| 1 | `scripts/player.gd:143-144`, `:153-154` | `send_move()` fires **every `_physics_process` (~60Hz)** while WASD-moving *and* while click-to-move is active. Zero traffic when idle (no heartbeat → NAT/timeout blind, no liveness). |
| 2 | `scripts/network_manager.gd:103-105` | `send_move()` is an unthrottled `_send_json` — no accumulator, no epsilon, no heartbeat. |
| 3 | `scripts/world.gd:123-127` | `_on_remote_player_moved` **snaps** `r_player.position = Vector2(x, y)` per packet → visible jitter/teleport on any jitter or loss; no interpolation. |
| 4 | `scripts/network_manager.gd:66-100` | `_parse_packet` handles `welcome / player_join / player_move / player_attack / player_leave / monster_hit / chat / zeny_update` only. **`monster_respawn` and `stats_update` are dropped.** |
| 5 | `server/server.js:147-151` | `case 'move'` trusts client coords with **no throttle, no clamp** — every 60Hz packet is rebroadcast to N−1 clients. |
| 6 | `server/server.patch.js:37,271-278` | Hardening patch **already proposes** `MOVE_THROTTLE_MS = 100` + coord clamp + dir whitelist, but is opt-in (manual 3-edit apply, §HOW TO APPLY). `monster_respawn` (:294) and `stats_update` (:314) sends already exist server-side. |
| 7 | `web/index.html` | Single-player canvas client: **no WebSocket, no remote-player rendering at all**. Movement is local (`moveWithCollision(player, …)` ≈ lines 3897/3951). Netcode must be additive (`web/net/Netcode.js` + snippet in §4). |

---

## §1 `player.gd` — route both `send_move` sites through the 12Hz gate

**A. Add the member + init** (near `facing_dir_name`, line 14; init in `_ready`, lines 40-45):

```gdscript
# NEW member (place after `var facing_dir_name …`):
var net_snap: NetSnapshot = null
```

```gdscript
# NEW lines at the end of _ready() (after `set_hero_class(0)`):
net_snap = NetSnapshot.new()
add_child(net_snap)
net_snap.reset_sender(position, facing_dir_name)
```

**B. WASD branch (lines 143-144):**

```gdscript
# OLD:
		if NetworkManager.instance:
			NetworkManager.instance.send_move(position.x, position.y, facing_dir_name)
# NEW:
		if net_snap:
			net_snap.tick_local_sender(delta, position, facing_dir_name)
```

**C. Click-to-move branch (lines 153-154):** same `OLD → NEW` replacement
(substitute the identical two lines inside the `elif is_moving_to_target:` block).

> `tick_local_sender` sends at most every 1/12s, and only when moved > 2px
> since the last snapshot, facing changed, or 250ms elapsed without a send.
> Idle clients emit 4Hz heartbeats instead of 60Hz-or-nothing. `delta` is the
> `_physics_process(delta)` parameter already in scope — no signature changes.

---

## §2 `world.gd` — interpolate remotes instead of snapping

**A. Add members + init** (near `_remote_players`, line 10; end of `_ready`, line 29):

```gdscript
# NEW members:
var _net_snap: NetSnapshot = null
var _net_ext: NetworkExt = null
```

```gdscript
# NEW lines at the end of _ready() (after `_connect_network_handlers()`):
	_net_snap = NetSnapshot.new()
	add_child(_net_snap)
	_net_ext = NetworkExt.new()
	add_child(_net_ext)
	_net_ext.monster_respawned.connect(_on_monster_respawned)
	_net_ext.stats_updated.connect(_on_stats_updated)
```

**B. Store targets instead of snapping (lines 123-127):**

```gdscript
# OLD:
func _on_remote_player_moved(id_str: String, x: float, y: float, dir_str: String) -> void:
	if _remote_players.has(id_str):
		var r_player: ZaggersPlayer = _remote_players[id_str]
		r_player.position = Vector2(x, y)
		r_player.facing_dir_name = dir_str
# NEW:
func _on_remote_player_moved(id_str: String, x: float, y: float, dir_str: String) -> void:
	if _remote_players.has(id_str) and _net_snap:
		_net_snap.set_remote_target(id_str, Vector2(x, y), dir_str)
```

**C. Per-frame interpolation + cleanup (NEW functions):**

```gdscript
func _process(_delta: float) -> void:
	if _net_snap == null:
		return
	for id_str in _remote_players:
		var r_player: ZaggersPlayer = _remote_players[id_str]
		r_player.position = _net_snap.poll_remote(id_str, r_player.position, _delta)
		if _net_snap.has_target(id_str):
			r_player.facing_dir_name = _net_snap.target_dir(id_str, r_player.facing_dir_name)
```

```gdscript
# NEW: also erase snapshot state when a remote leaves (append to existing
# _on_remote_player_left, after `_remote_players.erase(id_str)`):
		if _net_snap:
			_net_snap.clear_remote(id_str)
```

**D. Missing-signal handlers (NEW functions, wired in §2A):**

```gdscript
func _on_monster_respawned(m_id: String, new_hp: int, x: float, y: float) -> void:
	if _monsters.has(m_id):
		var monster: ZaggersMonster = _monsters[m_id]
		monster.position = Vector2(x, y)
		monster.take_damage(0, new_hp) # restore display HP without a damage number
	else:
		_spawn_monster({"id": m_id, "name": "Poring", "hp": new_hp, "max_hp": new_hp, "x": x, "y": y})


func _on_stats_updated(p_data: Dictionary) -> void:
	if _player and not p_data.is_empty():
		_player.hp = int(p_data.get("hp", _player.hp))
		_player.max_hp = int(p_data.get("max_hp", _player.max_hp))
		_player.sp = int(p_data.get("sp", _player.sp))
		_player.max_sp = int(p_data.get("max_sp", _player.max_sp))
		# Extend with str/agi/vit/int/dex/luk + HUD refresh as needed.
```

> `NetSnapshot.interp_step` lerps at 10/s (`1 − e^(−10·δ)`, framerate-independent)
> and teleports only past 200px (spawn/respawn/teleport), so normal 12Hz
> traffic renders smooth while loss-gaps don't rubber-band across the map.

---

## §3 `network_manager.gd` — forward the two missing packet types (6 lines)

Inside `_parse_packet`, after the `"zeny_update"` arm (lines 99-100), insert:

```gdscript
# NEW arms (paste directly after the zeny_update block):
		"monster_respawn":
			if NetworkExt.instance:
				NetworkExt.instance.handle_packet("monster_respawn", data)

		"stats_update":
			if NetworkExt.instance:
				NetworkExt.instance.handle_packet("stats_update", data)
```

> Guarded by `NetworkExt.instance`, so the game still runs when the ext node
> isn't in the tree (packets are dropped exactly as before). No existing arm
> is touched. `world.gd` §2A/§2D consumes the resulting
> `monster_respawned` / `stats_updated` signals.

---

## §4 `web/index.html` — wire `web/net/Netcode.js` (additive, no rewrites)

`index.html` currently has no networking. Add one script tag + ~25 lines:

```html
<!-- NEW: after <script src="parallax/ParallaxBackgrounds.js"></script> -->
<script src="net/Netcode.js"></script>
<script>
  // NEW: one shared instance (12Hz sender + interpolated remotes).
  const netcode = new SnapshotNetcode(); // window.SnapshotNetcode, see web/net/Netcode.js
  const remotePlayers = new Map();       // id -> { x, y, dir, targetX, targetY }
  let netSocket = null;

  function netConnect(url, onRemoteAttack) {
    netSocket = new WebSocket(url || 'ws://localhost:8080');
    netSocket.onmessage = (ev) => {
      let msg; try { msg = JSON.parse(ev.data); } catch (e) { return; }
      if (msg.type === 'player_move' && msg.id) {
        netcode.setRemoteTarget(msg.id, msg.x, msg.y, msg.dir);
        if (!remotePlayers.has(msg.id)) remotePlayers.set(msg.id, { x: msg.x, y: msg.y, dir: msg.dir });
      } else if (msg.type === 'player_leave' && msg.id) {
        remotePlayers.delete(msg.id); netcode.removeRemote(msg.id);
      } else if (msg.type === 'player_attack' && onRemoteAttack) {
        onRemoteAttack(msg);
      }
    };
    return netSocket;
  }

  function netTick(dtSeconds) {
    // (a) throttled local send — call once per frame after player movement:
    if (netSocket && netSocket.readyState === WebSocket.OPEN) {
      netcode.tickLocal(player.wx, player.wy, 'down', (snap) => {
        netSocket.send(JSON.stringify({ type: 'move', x: snap.x, y: snap.y, dir: snap.dir }));
      });
    }
    // (b) interpolate remotes into render positions:
    netcode.stepAll(remotePlayers, dtSeconds);
  }
  // TODO: draw each entry of `remotePlayers` next to the local `player`
  // render in the main draw loop; `dir` mirrors the Godot facing string.
</script>
```

> Call `netConnect()` once at boot (optional — game stays offline-capable when
> skipped) and `netTick(dt)` every frame where `dt` is seconds since last
> frame. Facing/dir mapping is a TODO: `index.html` tracks `player.dir` as an
> int, so map int→`"up/down/left/right"` before `tickLocal` if you want remote
> facing parity with Godot.

---

## §5 Server alignment note (no edit required)

`server/server.patch.js` already throttles `move` at **100ms** per socket.
A 12Hz client sends every **~83ms** while continuously moving, so the server
drops roughly 1 in 6 of those packets — effective rate ≈ **10Hz**, which the
10/s interpolator absorbs cleanly. Options if exact 12Hz end-to-end is wanted:
lower `MOVE_THROTTLE_MS` to `80`, or run the client at 10Hz
(`SEND_INTERVAL = 1.0/10.0`). Recommended: **leave both as-is** (defence in
depth: client politeness + server enforcement).

---

## §6 Expected traffic — 60Hz vs 12Hz × N players

Assumptions: one `player_move` ≈ 80B JSON + ≈40B WS/TCP overhead ≈ **120B**
on the wire. "Moving" = worst case (all N clients holding a key).
Current Godot client sends **only while moving** (0Hz idle); patched client
sends **12Hz moving / 4Hz heartbeat idle**. Server rebroadcasts each move to
N−1 clients: total server egress = **N·(N−1)·rate** msgs/s.

| N players | Topology | 60Hz (now, moving) | 12Hz (new, moving) | 4Hz heartbeat (new, idle) |
|---|---|---|---|---|
| 2 | upstream/client | 60/s · 7.2 KB/s | 12/s · 1.4 KB/s | 4/s · 0.5 KB/s |
| 2 | server egress | 120/s · 14 KB/s | 24/s · 2.9 KB/s | 8/s · 1.0 KB/s |
| 4 | upstream/client | 60/s · 7.2 KB/s | 12/s · 1.4 KB/s | 4/s · 0.5 KB/s |
| 4 | server egress | 720/s · 86 KB/s | 144/s · 17 KB/s | 48/s · 5.8 KB/s |
| 10 | server egress | 5,400/s · 648 KB/s | 1,080/s · 130 KB/s | 360/s · 43 KB/s |
| 32 | server egress | 59,520/s · ~7.1 MB/s | 11,904/s · ~1.4 MB/s | 3,968/s · ~476 KB/s |

> **5× reduction** on every axis while moving (60→12). Idle goes 0→4Hz
> deliberately (liveness + NAT keep-alive ≈ 0.5 KB/s/client — negligible).
> At N=32 the server sheds ~5.7 MB/s of broadcast. Note §5: with the 100ms
> server throttle, sustained-motion effective rate is ~10Hz, i.e. up to a
> further ~17% under the 12Hz column.

---

## §7 Verification

```powershell
& "$env:APPDATA\Python\Python314\Scripts\gdparse.exe" scripts/net_snapshot.gd scripts/network_ext.gd
node --check web/net/Netcode.js
node --check server/server.patch.js  # untouched, regression check
```

Expected: no output (all parsers silent on success), exit 0.
Player/world/network_manager diffs are documentation-only in this file —
re-run `gdparse` on them after applying §1–§3.
