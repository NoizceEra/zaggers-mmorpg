# monster.gd — Zaggers Monster Entity (HP Bar, Floating Damage Text, AI Sync).
class_name ZaggersMonster
extends CharacterBody2D

signal monster_died(monster: ZaggersMonster)

var monster_id: String = "m_100"
var monster_name: String = "Poring"
var hp: int = 50
var max_hp: int = 50

var _sprite: Sprite2D
var _hp_bar: ProgressBar
var _name_label: Label


func _ready() -> void:
	add_to_group("monsters")
	_build_visuals()


func _build_visuals() -> void:
	_sprite = Sprite2D.new()
	_sprite.name = "Sprite2D"
	if ResourceLoader.exists("res://assets/sprites_ff/slime_green_ff.png"):
		_sprite.texture = load("res://assets/sprites_ff/slime_green_ff.png")
		_sprite.hframes = 4
		_sprite.vframes = 4
	add_child(_sprite)

	_name_label = Label.new()
	_name_label.name = "NameLabel"
	_name_label.text = monster_name
	_name_label.position = Vector2(-30, -32)
	_name_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_name_label.custom_minimum_size = Vector2(60, 14)
	add_child(_name_label)

	_hp_bar = ProgressBar.new()
	_hp_bar.name = "HPBar"
	_hp_bar.min_value = 0
	_hp_bar.max_value = max_hp
	_hp_bar.value = hp
	_hp_bar.show_percentage = false
	_hp_bar.custom_minimum_size = Vector2(40, 4)
	_hp_bar.position = Vector2(-20, -18)
	add_child(_hp_bar)

	var col := CollisionShape2D.new()
	var circle := CircleShape2D.new()
	circle.radius = 14.0
	col.shape = circle
	add_child(col)


func setup_monster(id_str: String, m_name: String, current_hp: int, m_max_hp: int, pos: Vector2) -> void:
	monster_id = id_str
	monster_name = m_name
	hp = current_hp
	max_hp = m_max_hp
	position = pos

	if _name_label:
		_name_label.text = monster_name
	if _hp_bar:
		_hp_bar.max_value = max_hp
		_hp_bar.value = hp

	# Texture customization by monster type
	if _sprite and ResourceLoader.exists("res://assets/sprites_ff/hero_knight.png"):
		if "Poring" in monster_name:
			_sprite.texture = load("res://assets/sprites_ff/slime_green_ff.png")
			_sprite.modulate = Color(1.0, 0.4, 0.6) # Pink Poring tint
		elif "Goblin" in monster_name:
			_sprite.texture = load("res://assets/sprites_ff/goblin_ff.png")
		elif "Skeleton" in monster_name:
			_sprite.texture = load("res://assets/sprites_ff/skeleton_ff.png")
		elif "Baphomet" in monster_name:
			_sprite.texture = load("res://assets/sprites_ff/boss_baphomet_ff.png")
			_sprite.modulate = Color(1.0, 0.2, 0.2)


func take_damage(dmg: int, new_hp: int) -> void:
	hp = new_hp
	if _hp_bar:
		_hp_bar.value = hp
		
	# Floating Damage Number Animation (RO Style)
	var dmg_lbl := Label.new()
	dmg_lbl.text = "-" + str(dmg)
	dmg_lbl.modulate = Color(1.0, 0.2, 0.2) if dmg < 30 else Color(1.0, 0.9, 0.1) # Yellow for high damage
	dmg_lbl.position = position + Vector2(-10, -35)
	get_parent().add_child(dmg_lbl)
	
	var tween := dmg_lbl.create_tween()
	tween.tween_property(dmg_lbl, "position", dmg_lbl.position + Vector2(0, -25), 0.6)
	tween.parallel().tween_property(dmg_lbl, "modulate:a", 0.0, 0.6)
	tween.tween_callback(dmg_lbl.queue_free)

	if hp <= 0:
		visible = false
