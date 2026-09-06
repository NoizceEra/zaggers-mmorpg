# shop_ui.gd — Zaggers Equipment & Potion Shop UI.
class_name ZaggersShopUI
extends Panel

signal item_purchased(item_name: String, cost: int)

var _item_list: ItemList
var _buy_btn: Button
var _close_btn: Button
var _preview_sprite: Sprite2D
var _info_label: Label

# Shop Items
const SHOP_CATALOG: Array = [
	{ "name": "Red Potion", "cost": 50, "desc": "Restores 100 HP", "icon": "res://assets/sprites_ff/potion_health_ff.png" },
	{ "name": "Mythril Armor", "cost": 300, "desc": "Def +15, Max HP +50", "icon": "res://assets/sprites_ff/hero_knight.png" },
	{ "name": "Archmage Staff", "cost": 450, "desc": "MATK +25, Max SP +40", "icon": "res://assets/sprites_ff/hero_blackmage.png" },
	{ "name": "Dragon Lance", "cost": 600, "desc": "ATK +35, Crit +10%", "icon": "res://assets/sprites_ff/hero_dragoon.png" },
	{ "name": "Flame Rapier", "cost": 550, "desc": "ATK +28, MATK +15", "icon": "res://assets/sprites_ff/hero_redmage.png" },
]


func _ready() -> void:
	name = "ShopUI"
	position = Vector2(180, 40)
	custom_minimum_size = Vector2(280, 260)
	visible = false
	_build_shop_layout()


func _build_shop_layout() -> void:
	var title := Label.new()
	title.text = "Prontera Equipment Shop [S]"
	title.position = Vector2(10, 8)
	add_child(title)

	_item_list = ItemList.new()
	_item_list.position = Vector2(10, 32)
	_item_list.custom_minimum_size = Vector2(160, 180)
	_item_list.item_selected.connect(_on_item_selected)
	add_child(_item_list)

	for item in SHOP_CATALOG:
		var txt: String = item["name"] + " (" + str(item["cost"]) + "z)"
		_item_list.add_item(txt)

	_preview_sprite = Sprite2D.new()
	_preview_sprite.position = Vector2(220, 70)
	_preview_sprite.hframes = 4
	_preview_sprite.vframes = 4
	add_child(_preview_sprite)

	_info_label = Label.new()
	_info_label.text = "Select an item..."
	_info_label.position = Vector2(180, 120)
	_info_label.custom_minimum_size = Vector2(90, 60)
	_info_label.autowrap_mode = TextServer.AUTOWRAP_WORD
	add_child(_info_label)

	_buy_btn = Button.new()
	_buy_btn.text = "Buy Item"
	_buy_btn.position = Vector2(180, 185)
	_buy_btn.custom_minimum_size = Vector2(85, 26)
	_buy_btn.pressed.connect(_on_buy_pressed)
	add_child(_buy_btn)

	_close_btn = Button.new()
	_close_btn.text = "X"
	_close_btn.position = Vector2(250, 6)
	_close_btn.custom_minimum_size = Vector2(24, 20)
	_close_btn.pressed.connect(func(): visible = false)
	add_child(_close_btn)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("toggle_shop"):
		visible = not visible


func _on_item_selected(index: int) -> void:
	if index < 0 or index >= SHOP_CATALOG.size():
		return
	var item: Dictionary = SHOP_CATALOG[index]
	_info_label.text = String(item["desc"])
	var icon_path: String = String(item["icon"])
	if ResourceLoader.exists(icon_path):
		_preview_sprite.texture = load(icon_path)
		_preview_sprite.frame = 0


func _on_buy_pressed() -> void:
	var sel: Array = _item_list.get_selected_items()
	if sel.size() == 0:
		return
	var idx: int = sel[0]
	var item: Dictionary = SHOP_CATALOG[idx]
	var cost: int = int(item["cost"])
	
	if PartyData.instance.spend_gold(cost):
		print("[Shop] Bought ", item["name"], " for ", cost, " zeny!")
		item_purchased.emit(String(item["name"]), cost)
	else:
		print("[Shop] Not enough zeny!")
