# player.gd — Zaggers Player Character (Point-and-Click, WASD, Paperdoll System).
class_name ZaggersPlayer
extends CharacterBody2D

signal stats_changed(hp, max_hp, sp, max_sp, hero_idx, gold, level, xp)

const SPEED: float = 120.0
const INTERACT_RANGE: float = 28.0

var player_id: String = ""
var is_local_player: bool = true
var target_move_pos: Vector2 = Vector2.ZERO
var is_moving_to_target: bool = false
var facing_dir_name: String = "down"

# Paperdoll Sprite Layers
var base_sprite: Sprite2D = null
var armor_sprite: Sprite2D = null
var helm_sprite: Sprite2D = null
var weapon_sprite: Sprite2D = null

# Class & Stats
var class_idx: int = 0
var hp: int = 180
var max_hp: int = 180
var sp: int = 50
var max_sp: int = 50
var level: int = 1
var str_stat: int = 10
var agi_stat: int = 10
var vit_stat: int = 10
var int_stat: int = 10
var dex_stat: int = 10
var luk_stat: int = 10

var is_attacking: bool = false
var attack_timer: float = 0.0


func _ready() -> void:
	add_to_group("player")
	target_move_pos = position
	_build_paperdoll_layers()
	_ensure_collision()
	set_hero_class(0)


func _build_paperdoll_layers() -> void:
	base_sprite = Sprite2D.new()
	base_sprite.name = "BaseSprite"
	base_sprite.hframes = 4
	base_sprite.vframes = 4
	add_child(base_sprite)

	armor_sprite = Sprite2D.new()
	armor_sprite.name = "ArmorSprite"
	armor_sprite.hframes = 4
	armor_sprite.vframes = 4
	add_child(armor_sprite)

	helm_sprite = Sprite2D.new()
	helm_sprite.name = "HelmSprite"
	helm_sprite.hframes = 4
	helm_sprite.vframes = 4
	add_child(helm_sprite)

	weapon_sprite = Sprite2D.new()
	weapon_sprite.name = "WeaponSprite"
	weapon_sprite.hframes = 4
	weapon_sprite.vframes = 4
	add_child(weapon_sprite)


func _ensure_collision() -> void:
	if get_node_or_null("CollisionShape2D") == null:
		var col := CollisionShape2D.new()
		col.name = "CollisionShape2D"
		var cap := CapsuleShape2D.new()
		cap.radius = 10.0
		cap.height = 24.0
		col.shape = cap
		col.position = Vector2(0, 6)
		add_child(col)


func set_hero_class(idx: int) -> void:
	class_idx = idx % PartyData.HERO_DEFS.size()
	var def: Dictionary = PartyData.hero_def(class_idx)
	if def.is_empty():
		return

	var path: String = String(def.get("icon", "res://assets/sprites_ff/hero_knight.png"))
	if ResourceLoader.exists(path):
		var tex := load(path) as Texture2D
		base_sprite.texture = tex
		
	max_hp = int(def.get("max_hp", 180))
	max_sp = int(def.get("max_sp", 50))
	hp = max_hp
	sp = max_sp
	_update_animation_frame(0)


func _unhandled_input(event: InputEvent) -> void:
	if not is_local_player:
		return
		
	# Ragnarok Online Point-and-Click Movement
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		var global_click: Vector2 = get_global_mouse_position()
		target_move_pos = global_click
		is_moving_to_target = true


func _physics_process(delta: float) -> void:
	if is_attacking:
		attack_timer -= delta
		if attack_timer <= 0.0:
			is_attacking = false
			_update_animation_frame(1) # Back to idle
		return

	if not is_local_player:
		return

	# Movement calculation (Keyboard WASD or Mouse Click-to-move)
	var move_dir := Vector2.ZERO
	if Input.is_key_pressed(KEY_A) or Input.is_action_pressed("ui_left"):
		move_dir.x -= 1.0
	if Input.is_key_pressed(KEY_D) or Input.is_action_pressed("ui_right"):
		move_dir.x += 1.0
	if Input.is_key_pressed(KEY_W) or Input.is_action_pressed("ui_up"):
		move_dir.y -= 1.0
	if Input.is_key_pressed(KEY_S) or Input.is_action_pressed("ui_down"):
		move_dir.y += 1.0

	if move_dir != Vector2.ZERO:
		is_moving_to_target = false
		velocity = move_dir.normalized() * SPEED
		_set_facing_from_vector(move_dir)
		_update_animation_frame(int(Time.get_ticks_msec() / 150) % 2 * 2) # Alternate walk0/walk1
		move_and_slide()
		if NetworkManager.instance:
			NetworkManager.instance.send_move(position.x, position.y, facing_dir_name)
	elif is_moving_to_target:
		var dist := position.distance_to(target_move_pos)
		if dist > 4.0:
			var dir_vec := (target_move_pos - position).normalized()
			velocity = dir_vec * SPEED
			_set_facing_from_vector(dir_vec)
			_update_animation_frame(int(Time.get_ticks_msec() / 150) % 2 * 2)
			move_and_slide()
			if NetworkManager.instance:
				NetworkManager.instance.send_move(position.x, position.y, facing_dir_name)
		else:
			is_moving_to_target = false
			velocity = Vector2.ZERO
			_update_animation_frame(1) # Idle
	else:
		velocity = Vector2.ZERO
		_update_animation_frame(1) # Idle

	# Attack trigger
	if Input.is_action_just_pressed("ui_attack"):
		perform_attack()


func perform_attack() -> void:
	if is_attacking:
		return
	is_attacking = true
	attack_timer = 0.35
	_update_animation_frame(3) # Attack frame
	if is_local_player and NetworkManager.instance:
		NetworkManager.instance.send_attack("", facing_dir_name)


func _set_facing_from_vector(v: Vector2) -> void:
	if abs(v.x) > abs(v.y):
		facing_dir_name = "left" if v.x < 0 else "right"
	else:
		facing_dir_name = "up" if v.y < 0 else "down"


func _update_animation_frame(col: int) -> void:
	var row := 0
	match facing_dir_name:
		"down": row = 0
		"left": row = 1
		"right": row = 2
		"up": row = 3
	
	var frame_num := row * 4 + col
	base_sprite.frame = frame_num
	armor_sprite.frame = frame_num
	helm_sprite.frame = frame_num
	weapon_sprite.frame = frame_num
