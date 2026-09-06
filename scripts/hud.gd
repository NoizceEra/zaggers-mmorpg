# hud.gd — Zaggers Ragnarok Online Style HUD.
class_name ZaggersHUD
extends CanvasLayer

signal stat_add_requested(stat_name: String)
signal chat_sent(text: String)

var _hp_bar: ProgressBar
var _sp_bar: ProgressBar
var _exp_bar: ProgressBar
var _hp_lbl: Label
var _sp_lbl: Label
var _zeny_lbl: Label

var _chat_box: RichTextLabel
var _chat_input: LineEdit

var _stat_panel: Panel
var _stat_labels: Dictionary = {}


func _ready() -> void:
	_build_ro_hud()
	_connect_network_signals()


func _build_ro_hud() -> void:
	# Top-Left Character Status Window
	var status_panel := Panel.new()
	status_panel.name = "StatusPanel"
	status_panel.position = Vector2(10, 10)
	status_panel.custom_minimum_size = Vector2(210, 80)
	add_child(status_panel)

	var name_lbl := Label.new()
	name_lbl.text = "Hero [Novice]"
	name_lbl.position = Vector2(8, 4)
	status_panel.add_child(name_lbl)

	# HP Bar
	_hp_bar = ProgressBar.new()
	_hp_bar.position = Vector2(8, 24)
	_hp_bar.custom_minimum_size = Vector2(194, 14)
	_hp_bar.show_percentage = false
	status_panel.add_child(_hp_bar)

	_hp_lbl = Label.new()
	_hp_lbl.text = "HP: 180 / 180"
	_hp_lbl.position = Vector2(12, 24)
	status_panel.add_child(_hp_lbl)

	# SP Bar
	_sp_bar = ProgressBar.new()
	_sp_bar.position = Vector2(8, 42)
	_sp_bar.custom_minimum_size = Vector2(194, 12)
	_sp_bar.show_percentage = false
	status_panel.add_child(_sp_bar)

	_sp_lbl = Label.new()
	_sp_lbl.text = "SP: 50 / 50"
	_sp_lbl.position = Vector2(12, 42)
	status_panel.add_child(_sp_lbl)

	# Zeny Display
	_zeny_lbl = Label.new()
	_zeny_lbl.text = "Zeny: 500 z"
	_zeny_lbl.position = Vector2(8, 58)
	status_panel.add_child(_zeny_lbl)

	# Bottom Chat Box
	var chat_container := VBoxContainer.new()
	chat_container.position = Vector2(10, 240)
	chat_container.custom_minimum_size = Vector2(280, 110)
	add_child(chat_container)

	_chat_box = RichTextLabel.new()
	_chat_box.custom_minimum_size = Vector2(280, 80)
	_chat_box.scroll_following = true
	_chat_box.bbcode_enabled = true
	_chat_box.text = "[color=yellow]Welcome to Zaggers MMORPG![/color]\n"
	chat_container.add_child(_chat_box)

	_chat_input = LineEdit.new()
	_chat_input.placeholder_text = "Press Enter to chat..."
	_chat_input.custom_minimum_size = Vector2(280, 24)
	_chat_input.text_submitted.connect(_on_chat_submitted)
	chat_container.add_child(_chat_input)

	# Stat Window (Toggle via C key)
	_build_stat_window()


func _build_stat_window() -> void:
	_stat_panel = Panel.new()
	_stat_panel.name = "StatPanel"
	_stat_panel.position = Vector2(420, 10)
	_stat_panel.custom_minimum_size = Vector2(210, 200)
	_stat_panel.visible = false
	add_child(_stat_panel)

	var title := Label.new()
	title.text = "Character Stats [C]"
	title.position = Vector2(8, 6)
	_stat_panel.add_child(title)

	var stats := ["str", "agi", "vit", "int", "dex", "luk"]
	var y_pos := 30
	for s in stats:
		var lbl := Label.new()
		lbl.text = s.to_upper() + ": 10"
		lbl.position = Vector2(12, y_pos)
		_stat_panel.add_child(lbl)
		_stat_labels[s] = lbl

		var btn := Button.new()
		btn.text = "+"
		btn.position = Vector2(160, y_pos - 2)
		btn.custom_minimum_size = Vector2(24, 20)
		btn.pressed.connect(func(): NetworkManager.instance.send_stat_add(s))
		_stat_panel.add_child(btn)

		y_pos += 26


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("toggle_stats"):
		_stat_panel.visible = not _stat_panel.visible


func _on_chat_submitted(text: String) -> void:
	if text.strip_edges().is_empty():
		return
	if NetworkManager.instance:
		NetworkManager.instance.send_chat(text)
	_chat_input.text = ""


func _connect_network_signals() -> void:
	if NetworkManager.instance:
		NetworkManager.instance.chat_received.connect(func(name_str, text):
			_chat_box.append_text("[color=cyan]" + name_str + ":[/color] " + text + "\n")
		)
		NetworkManager.instance.zeny_updated.connect(func(zeny):
			_zeny_lbl.text = "Zeny: " + str(zeny) + " z"
		)


func update_player_status(hp: int, max_hp: int, sp: int, max_sp: int, zeny: int) -> void:
	if _hp_bar:
		_hp_bar.max_value = max_hp
		_hp_bar.value = hp
		_hp_lbl.text = "HP: " + str(hp) + " / " + str(max_hp)
	if _sp_bar:
		_sp_bar.max_value = max_sp
		_sp_bar.value = sp
		_sp_lbl.text = "SP: " + str(sp) + " / " + str(max_sp)
	if _zeny_lbl:
		_zeny_lbl.text = "Zeny: " + str(zeny) + " z"
