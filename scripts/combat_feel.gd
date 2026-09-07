# combat_feel.gd — Zaggers Combat Feel (additive juice layer).
# Autoload-friendly: works as an Autoload singleton ("CombatFeel") OR as a
# plain child Node. Never touches damage math or kill flow - only freeze /
# shake / push / input-buffer juice around the existing calls.
#
# Pairs with:
#   scripts/player.gd  perform_attack()  (instant frame swap, 0.35s lock)
#   scripts/monster.gd take_damage()     (tween float text, visible=false)
#
# Usage (autoload):  CombatFeel.hit_stop(60.0) / CombatFeel.add_trauma(0.3)
# Usage (child node): $CombatFeel.hit_stop(60.0)  (assign `camera` in editor)

class_name ZaggersCombatFeel
extends Node

## Peak camera offset (px) at trauma == 1.0.
const SHAKE_MAX_PX: float = 8.0
## Trauma units drained per second (linear decay).
const SHAKE_DECAY_PER_SEC: float = 1.6
## Default hitstop length (matches web 60ms freeze).
const HITSTOP_DEFAULT_MS: float = 60.0
## Hitstop time_scale while frozen (near-stop, keeps tweens alive).
const HITSTOP_SCALE: float = 0.05
## How long a pressed attack is buffered while already swinging.
const BUFFER_WINDOW: float = 0.25
## Default knockback push speed (px/sec velocity kick).
const KNOCKBACK_POWER: float = 140.0

var trauma: float = 0.0
var camera: Camera2D = null

var _hitstop_token: int = 0
var _queued_attack: bool = false
var _buffer_time: float = 0.0


func _process(delta: float) -> void:
	if trauma > 0.0:
		trauma = clampf(trauma - SHAKE_DECAY_PER_SEC * delta, 0.0, 1.0)
	if _queued_attack:
		_buffer_time -= delta
		if _buffer_time <= 0.0:
			_queued_attack = false
	_apply_shake()


## Hitstop pulse: briefly drops Engine.time_scale, then restores it.
## Safe for re-entry (token guard) and for nodes outside the tree.
func hit_stop(duration_ms: float = HITSTOP_DEFAULT_MS, frozen_scale: float = HITSTOP_SCALE) -> void:
	if not is_inside_tree():
		return
	_hitstop_token += 1
	var my_token: int = _hitstop_token
	Engine.time_scale = frozen_scale
	await get_tree().create_timer(duration_ms / 1000.0, true, false, true).timeout
	if my_token == _hitstop_token:
		Engine.time_scale = 1.0


## Adds screen-shake energy (0..1 clamped). Crits should pass ~0.55.
func add_trauma(amount: float = 0.3) -> float:
	trauma = clampf(trauma + amount, 0.0, 1.0)
	return trauma


## Applies the current trauma to the assigned camera (call every frame
## or rely on _process doing it automatically when `camera` is set).
func apply_to_camera(cam: Camera2D) -> void:
	if cam == null:
		return
	var mag: float = SHAKE_MAX_PX * trauma * trauma
	if mag <= 0.01:
		cam.offset = Vector2.ZERO
		return
	var t: float = float(Time.get_ticks_msec()) / 1000.0
	cam.offset = Vector2(
		(sin(t * 53.0) * 0.6 + sin(t * 19.0 + 1.7) * 0.4) * mag,
		(cos(t * 49.0 + 0.6) * 0.6 + cos(t * 17.0 + 3.1) * 0.4) * mag
	)


## Knockback kick on any CharacterBody2D (player or monster). Adds to the
## body's existing velocity so the caller's move_and_slide() carries it.
func apply_knockback(body: CharacterBody2D, from_pos: Vector2, power: float = KNOCKBACK_POWER) -> Vector2:
	if body == null:
		return Vector2.ZERO
	var dir: Vector2 = body.global_position - from_pos
	if dir.length() < 0.01:
		dir = Vector2.RIGHT
	dir = dir.normalized()
	body.velocity += dir * power
	return dir * power


## Buffer an attack pressed mid-swing so it fires on release instead of
## being swallowed (mirrors the web 1-deep skill queue).
func buffer_attack() -> void:
	_queued_attack = true
	_buffer_time = BUFFER_WINDOW


## Returns true once when a buffered attack should fire: fighter is free
## and the buffer window has not expired. Clears the buffer either way
## once it is consumed or expires (expiry handled in _process).
func consume_buffered_attack(is_attacking: bool) -> bool:
	if _queued_attack and not is_attacking:
		_queued_attack = false
		_buffer_time = 0.0
		return true
	return false


func has_queued_attack() -> bool:
	return _queued_attack


func _apply_shake() -> void:
	if camera != null:
		apply_to_camera(camera)
