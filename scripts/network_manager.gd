# network_manager.gd — Zaggers WebSocket Multiplayer Connector.
class_name NetworkManager
extends Node

signal connected_to_server
signal disconnected_from_server
signal welcome_received(self_data: Dictionary, players: Array, monsters: Array)
signal player_joined(player_data: Dictionary)
signal player_moved(id: String, x: float, y: float, dir: String)
signal player_attacked(id: String, target_id: String, dir: String)
signal player_left(id: String)
signal monster_hit(id: String, hp: int, max_hp: int, dmg: int)
signal chat_received(sender_name: String, text: String)
signal zeny_updated(new_zeny: int)

const SERVER_URL: String = "ws://localhost:8080"

static var instance: NetworkManager = null
var _ws: WebSocketPeer = WebSocketPeer.new()
var is_connected_to_server: bool = false
var self_id: String = ""


static func get_instance() -> NetworkManager:
	return instance


func _init() -> void:
	instance = self


func _ready() -> void:
	connect_to_server()


func connect_to_server() -> void:
	var err := _ws.connect_to_url(SERVER_URL)
	if err == OK:
		print("[Network] Connecting to Zaggers server at ", SERVER_URL)
	else:
		print("[Network] Connection error: ", err)


func _process(_delta: float) -> void:
	_ws.poll()
	var state := _ws.get_ready_state()
	
	if state == WebSocketPeer.STATE_OPEN:
		if not is_connected_to_server:
			is_connected_to_server = true
			print("[Network] Connected to server!")
			connected_to_server.emit()
		
		while _ws.get_available_packet_count() > 0:
			var pkt := _ws.get_packet()
			var txt := pkt.get_string_from_utf8()
			_parse_packet(txt)
			
	elif state == WebSocketPeer.STATE_CLOSED:
		if is_connected_to_server:
			is_connected_to_server = false
			print("[Network] Disconnected from server.")
			disconnected_from_server.emit()


func _parse_packet(json_txt: String) -> void:
	var json := JSON.new()
	if json.parse(json_txt) != OK:
		return
	var data: Dictionary = json.data as Dictionary
	var pkt_type: String = String(data.get("type", ""))
	
	match pkt_type:
		"welcome":
			var self_d: Dictionary = data.get("self", {})
			self_id = String(self_d.get("id", ""))
			var p_arr: Array = data.get("players", [])
			var m_arr: Array = data.get("monsters", [])
			welcome_received.emit(self_d, p_arr, m_arr)
			
		"player_join":
			player_joined.emit(data.get("player", {}))
			
		"player_move":
			player_moved.emit(String(data.get("id", "")), float(data.get("x", 0)), float(data.get("y", 0)), String(data.get("dir", "down")))
			
		"player_attack":
			player_attacked.emit(String(data.get("id", "")), String(data.get("target_id", "")), String(data.get("dir", "down")))
			
		"player_leave":
			player_left.emit(String(data.get("id", "")))
			
		"monster_hit":
			monster_hit.emit(String(data.get("id", "")), int(data.get("hp", 0)), int(data.get("max_hp", 100)), int(data.get("dmg", 0)))
			
		"chat":
			chat_received.emit(String(data.get("name", "Player")), String(data.get("text", "")))
			
		"zeny_update":
			zeny_updated.emit(int(data.get("zeny", 0)))


func send_move(pos_x: float, pos_y: float, dir: String) -> void:
	if is_connected_to_server:
		_send_json({"type": "move", "x": pos_x, "y": pos_y, "dir": dir})


func send_attack(target_id: String, dir: String) -> void:
	if is_connected_to_server:
		_send_json({"type": "attack", "target_id": target_id, "dir": dir})


func send_chat(text: String) -> void:
	if is_connected_to_server:
		_send_json({"type": "chat", "text": text})


func send_stat_add(stat_name: String) -> void:
	if is_connected_to_server:
		_send_json({"type": "stat_add", "stat": stat_name})


func _send_json(dict: Dictionary) -> void:
	var txt := JSON.stringify(dict)
	_ws.send_text(txt)
