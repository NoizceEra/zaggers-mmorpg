# net_snapshot.gd — P0 netcode: 12Hz throttled sender + interpolated remote receiver.
#
# PROBLEM (see scripts/net_snapshot.patch.md §0):
#   scripts/player.gd calls NetworkManager.send_move() every _physics_process
#   (~60Hz) while moving, and scripts/world.gd snaps remote positions directly
#   onto each player_move packet (jitter / teleport on lossy links).
#
# WHAT THIS DOES:
#   * Local  -> server: 12Hz accumulator. A packet is emitted at most every
#     1/12s AND only if the player moved > 2px, changed facing, or the 250ms
#     heartbeat expired (keeps NAT open + proves liveness while idle).
#   * Server -> local : stores per-remote target positions; world.gd polls each
#     frame and exponential-lerps (10/s, framerate-independent) toward them,
#     snapping only on teleports (> 200px, e.g. welcome / respawn).
#
# USAGE: attach one instance to the local player (sender side) and one to the
# world (receiver side), or share a single instance. Never sends directly when
# NetworkManager is absent — tick_local_sender() then just returns false.
class_name NetSnapshot
extends Node

## Max send rate (Hz) for local movement snapshots.
const SEND_INTERVAL: float = 1.0 / 12.0
## Force a snapshot at least this often even when idle (seconds).
const HEARTBEAT_INTERVAL: float = 0.25
## Minimum displacement (px) since the last sent snapshot that counts as "moved".
const MOVE_EPSILON_PX: float = 2.0
## Exponential lerp rate (per second) for remote interpolation.
const REMOTE_LERP_RATE: float = 10.0
## Above this distance (px) a remote is teleported instead of interpolated.
const REMOTE_SNAP_DIST_PX: float = 200.0

var _accum: float = 0.0
var _since_send: float = 99.0
var _last_sent_pos: Vector2 = Vector2.ZERO
var _has_sent_once: bool = false
var _last_sent_dir: String = ""

# id (String) -> Vector2 target / String facing.
var _targets: Dictionary = {}
var _target_dirs: Dictionary = {}


## Re-arm the sender (e.g. after welcome / teleport) so the next snapshot
## goes out immediately instead of waiting on the accumulator.
func reset_sender(pos: Vector2, dir: String = "") -> void:
	_accum = SEND_INTERVAL
	_since_send = HEARTBEAT_INTERVAL
	_last_sent_pos = pos
	_last_sent_dir = dir
	_has_sent_once = true


## Pure gate: true when a snapshot should be emitted this tick.
## Call every physics frame with the local player's position/facing.
func should_send(delta: float, cur_pos: Vector2, dir: String) -> bool:
	_accum += delta
	_since_send += delta
	if _accum < SEND_INTERVAL:
		return false
	if not _has_sent_once:
		return true
	if dir != _last_sent_dir:
		return true
	if _since_send >= HEARTBEAT_INTERVAL:
		return true
	return cur_pos.distance_to(_last_sent_pos) > MOVE_EPSILON_PX


## Throttled sender. Emits via NetworkManager when should_send() passes,
## resets the accumulator/heartbeat, and returns true when a packet went out.
func tick_local_sender(delta: float, cur_pos: Vector2, dir: String) -> bool:
	if not should_send(delta, cur_pos, dir):
		return false
	if NetworkManager.instance == null:
		return false
	NetworkManager.instance.send_move(cur_pos.x, cur_pos.y, dir)
	_accum = 0.0
	_since_send = 0.0
	_last_sent_pos = cur_pos
	_last_sent_dir = dir
	_has_sent_once = true
	return true


## Record the latest authoritative position for a remote player.
## Called from world.gd's player_moved handler (replaces direct snapping).
func set_remote_target(id: String, pos: Vector2, dir: String = "") -> void:
	_targets[id] = pos
	if not dir.is_empty():
		_target_dirs[id] = dir


func has_target(id: String) -> bool:
	return _targets.has(id)


func target_dir(id: String, fallback: String = "down") -> String:
	return String(_target_dirs.get(id, fallback))


func clear_remote(id: String) -> void:
	_targets.erase(id)
	_target_dirs.erase(id)


func clear_all() -> void:
	_targets.clear()
	_target_dirs.clear()


## One interpolation step toward the stored target. Teleports on large
## gaps (spawn / respawn / heavy loss), otherwise exponential lerp at
## REMOTE_LERP_RATE — framerate-independent via exp().
static func interp_step(cur: Vector2, target: Vector2, delta: float) -> Vector2:
	if cur.distance_to(target) > REMOTE_SNAP_DIST_PX:
		return target
	var t: float = 1.0 - exp(-REMOTE_LERP_RATE * delta)
	return cur.lerp(target, clampf(t, 0.0, 1.0))


## Poll helper for world.gd _process: returns the position the remote's
## node should be assigned this frame. Returns cur when no target is known.
func poll_remote(id: String, cur: Vector2, delta: float) -> Vector2:
	if not _targets.has(id):
		return cur
	return interp_step(cur, _targets[id] as Vector2, delta)
