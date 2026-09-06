# world.gd — Zaggers 2.5D Isometric World Manager.
class_name ZaggersWorld
extends Node2D

const TILE_SIZE: int = 32

var _player: ZaggersPlayer
var _hud: ZaggersHUD
var _shop_ui: ZaggersShopUI
var _remote_players: Dictionary = {} # id -> ZaggersPlayer
var _monsters: Dictionary = {}       # id -> ZaggersMonster

var _entities_node: Node2D
var _camera: Camera2D


func _ready() -> void:
	_entities_node = Node2D.new()
	_entities_node.name = "Entities"
	add_child(_entities_node)

	_build_isometric_terrain()
	_spawn_local_player()
	_setup_camera()
	_setup_ui()

	_connect_network_handlers()


func _build_isometric_terrain() -> void:
	# Build 2.5D grid background tiles
	var bg_node := Node2D.new()
	bg_node.name = "TerrainGrid"
	add_child(bg_node)
	
	# Simple grid representation for world boundaries (800x600 px)
	var tile_tex: Texture2D = null
	if ResourceLoader.exists("res://assets/tiles_ff/tileset_town_ff.png"):
		tile_tex = load("res://assets/tiles_ff/tileset_town_ff.png") as Texture2D

	for y in range(0, 700, 32):
		for x in range(0, 900, 32):
			var sprite := Sprite2D.new()
			if tile_tex:
				sprite.texture = tile_tex
				sprite.region_enabled = true
				sprite.region_rect = Rect2(0, 0, 32, 32)
			sprite.position = Vector2(x + 16, y + 16)
			bg_node.add_child(sprite)


func _spawn_local_player() -> void:
	_player = ZaggersPlayer.new()
	_player.name = "LocalPlayer"
	_player.position = Vector2(320, 240)
	_player.is_local_player = true
	_entities_node.add_child(_player)


func _setup_camera() -> void:
	_camera = Camera2D.new()
	_camera.name = "Camera2D"
	_camera.zoom = Vector2(1.75, 1.75)
	_camera.position_smoothing_enabled = true
	_player.add_child(_camera)


func _setup_ui() -> void:
	_hud = ZaggersHUD.new()
	add_child(_hud)

	_shop_ui = ZaggersShopUI.new()
	add_child(_shop_ui)


func _connect_network_handlers() -> void:
	if NetworkManager.instance:
		NetworkManager.instance.welcome_received.connect(_on_welcome_received)
		NetworkManager.instance.player_joined.connect(_on_remote_player_joined)
		NetworkManager.instance.player_moved.connect(_on_remote_player_moved)
		NetworkManager.instance.player_attacked.connect(_on_remote_player_attacked)
		NetworkManager.instance.player_left.connect(_on_remote_player_left)
		NetworkManager.instance.monster_hit.connect(_on_monster_hit)


func _on_welcome_received(self_data: Dictionary, players: Array, monsters: Array) -> void:
	if _player:
		_player.player_id = String(self_data.get("id", ""))
		_player.position = Vector2(float(self_data.get("x", 320)), float(self_data.get("y", 240)))
	
	for p_data in players:
		_on_remote_player_joined(p_data)
		
	for m_data in monsters:
		_spawn_monster(m_data)


func _on_remote_player_joined(p_data: Dictionary) -> void:
	var id_str: String = String(p_data.get("id", ""))
	if id_str.is_empty() or id_str == _player.player_id or _remote_players.has(id_str):
		return
		
	var r_player := ZaggersPlayer.new()
	r_player.name = "Player_" + id_str
	r_player.player_id = id_str
	r_player.is_local_player = false
	r_player.position = Vector2(float(p_data.get("x", 320)), float(p_data.get("y", 240)))
	r_player.facing_dir_name = String(p_data.get("dir", "down"))
	_entities_node.add_child(r_player)
	_remote_players[id_str] = r_player


func _on_remote_player_moved(id_str: String, x: float, y: float, dir_str: String) -> void:
	if _remote_players.has(id_str):
		var r_player: ZaggersPlayer = _remote_players[id_str]
		r_player.position = Vector2(x, y)
		r_player.facing_dir_name = dir_str


func _on_remote_player_attacked(id_str: String, _target_id: String, dir_str: String) -> void:
	if _remote_players.has(id_str):
		var r_player: ZaggersPlayer = _remote_players[id_str]
		r_player.facing_dir_name = dir_str
		r_player.perform_attack()


func _on_remote_player_left(id_str: String) -> void:
	if _remote_players.has(id_str):
		var r_player: ZaggersPlayer = _remote_players[id_str]
		r_player.queue_free()
		_remote_players.erase(id_str)


func _spawn_monster(m_data: Dictionary) -> void:
	var m_id: String = String(m_data.get("id", ""))
	if m_id.is_empty() or _monsters.has(m_id):
		return
		
	var monster := ZaggersMonster.new()
	monster.name = "Monster_" + m_id
	monster.setup_monster(
		m_id,
		String(m_data.get("name", "Poring")),
		int(m_data.get("hp", 50)),
		int(m_data.get("max_hp", 50)),
		Vector2(float(m_data.get("x", 400)), float(m_data.get("y", 300)))
	)
	_entities_node.add_child(monster)
	_monsters[m_id] = monster


func _on_monster_hit(m_id: String, new_hp: int, _max_hp: int, dmg: int) -> void:
	if _monsters.has(m_id):
		var monster: ZaggersMonster = _monsters[m_id]
		monster.take_damage(dmg, new_hp)
