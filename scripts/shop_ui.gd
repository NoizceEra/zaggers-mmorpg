# shop_ui.gd — Zaggers Equipment & Potion Shop UI.
class_name ZaggersShopUI
extends Panel

signal item_purchased(item_name: String, cost: int)

var _item_list: ItemList
var _buy_btn: Button
var _close_btn: Button
var _preview_sprite: Sprite2D
var _info_label: Label

# Shop Items — mirrors web/zaggers_database.json shop filter (source=='shop' or tier<=2).
# Sorted by req_level like web populateShopFromDB(). Late-tier gear (emberglass, slagworks,
# hoarfrost, umbral, rootfang, sovereign) is drop-only by design, not sold here.
# Thawstone (price 0, quest) excluded like web.
const SHOP_CATALOG: Array = [
	{ "db_id": "meadow_bread", "name": "Meadow Bread", "cost": 25, "req_level": 1, "slot": "consumable", "desc": "Restores 45 HP", "icon": "res://assets/sprites_ff/food_bread_ff.png" },
	{ "db_id": "red_potion", "name": "Red Potion", "cost": 50, "req_level": 1, "slot": "consumable", "desc": "Restores 100 HP", "icon": "res://assets/sprites_ff/potion_health_ff.png" },
	{ "db_id": "travellers_jerkin", "name": "Traveller's Jerkin", "cost": 70, "req_level": 1, "slot": "armor", "desc": "DEF +5, MDEF +1", "icon": "res://assets/sprites_ff/arm_jerkin_ff.png" },
	{ "db_id": "blue_potion", "name": "Blue Potion", "cost": 80, "req_level": 1, "slot": "consumable", "desc": "Restores 60 SP", "icon": "res://assets/sprites_ff/potion_mana_ff.png" },
	{ "db_id": "bellflower_shortsword", "name": "Bellflower Shortsword", "cost": 90, "req_level": 1, "slot": "weapon", "desc": "ATK +14", "icon": "res://assets/sprites_ff/wpn_shortsword_ff.png" },
	{ "db_id": "militia_kettle_helm", "name": "Militia Kettle Helm", "cost": 60, "req_level": 3, "slot": "headgear", "desc": "DEF +4, MDEF +1, VIT +1", "icon": "res://assets/sprites_ff/hat_kettle_ff.png" },
	{ "db_id": "oaken_targe", "name": "Oaken Targe", "cost": 120, "req_level": 5, "slot": "shield", "desc": "DEF +6, MDEF +2, Earth", "icon": "res://assets/sprites_ff/shd_targe_ff.png" },
	{ "db_id": "hedgerow_charm", "name": "Hedgerow Charm", "cost": 150, "req_level": 6, "slot": "accessory", "desc": "LUK +2, FLEE +5, Earth", "icon": "res://assets/sprites_ff/acc_charm_ff.png" },
	{ "db_id": "snagtooth_cleaver", "name": "Snagtooth Cleaver", "cost": 260, "req_level": 12, "slot": "weapon", "desc": "ATK +22, STR +2", "icon": "res://assets/sprites_ff/wpn_cleaver_ff.png" },
	{ "db_id": "mythril_armor", "name": "Mythril Armor", "cost": 300, "req_level": 20, "slot": "armor", "desc": "DEF +15, MDEF +5", "icon": "res://assets/sprites_ff/arm_mythril_ff.png" },
	{ "db_id": "tidebreak_trident", "name": "Tidebreak Trident", "cost": 700, "req_level": 22, "slot": "weapon", "desc": "ATK +38, DEX +3, Water, 2H", "icon": "res://assets/sprites_ff/wpn_trident_ff.png" },
	{ "db_id": "glasslight_pendant", "name": "Glasslight Pendant", "cost": 1400, "req_level": 24, "slot": "accessory", "desc": "MDEF +8, INT +4, Holy", "icon": "res://assets/sprites_ff/acc_pendant_ff.png" },
	{ "db_id": "nave_aegis", "name": "Nave Aegis", "cost": 850, "req_level": 26, "slot": "shield", "desc": "DEF +18, MDEF +10, VIT +3", "icon": "res://assets/sprites_ff/shd_aegis_ff.png" },
	{ "db_id": "coral_circlet", "name": "Coral Circlet", "cost": 1100, "req_level": 27, "slot": "headgear", "desc": "DEF +9, MDEF +6, INT +3, Water", "icon": "res://assets/sprites_ff/hat_circlet_ff.png" },
	{ "db_id": "dragon_lance", "name": "Dragon Lance", "cost": 600, "req_level": 34, "slot": "weapon", "desc": "ATK +35, CRIT +10%, 2H", "icon": "res://assets/sprites_ff/wpn_lance_dragon_ff.png" },
	{ "db_id": "aetherite_draught", "name": "Aetherite Draught", "cost": 900, "req_level": 50, "slot": "consumable", "desc": "Restores 800 HP, 300 SP, Holy", "icon": "res://assets/sprites_ff/potion_aetherite_ff.png" },
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
	var req: int = int(item.get("req_level", 1))
	_info_label.text = String(item["desc"]) + "\nLv %d · %s" % [req, String(item.get("slot", ""))]
	var icon_path: String = String(item["icon"])
	if ResourceLoader.exists(icon_path):
		var tex := load(icon_path) as Texture2D
		_preview_sprite.texture = tex
		# Item icons are 32x32 single-frame; hero sheets are 256x256 4x4.
		if tex and tex.get_width() <= 32 and tex.get_height() <= 32:
			_preview_sprite.hframes = 1
			_preview_sprite.vframes = 1
		else:
			_preview_sprite.hframes = 4
			_preview_sprite.vframes = 4
		_preview_sprite.frame = 0


func _on_buy_pressed() -> void:
	var sel: Array = _item_list.get_selected_items()
	if sel.size() == 0:
		return
	var idx: int = sel[0]
	var item: Dictionary = SHOP_CATALOG[idx]
	var cost: int = int(item["cost"])
	var req: int = int(item.get("req_level", 1))

	# Level gate (web parity: buyItemById checks reqLevel vs player.level).
	var player := get_tree().get_first_node_in_group("player")
	if player and int(player.get("level")) < req:
		print("[Shop] Requires Lv. %d for %s." % [req, String(item["name"])])
		return

	if PartyData.instance.spend_gold(cost):
		print("[Shop] Bought ", item["name"], " (", String(item.get("db_id", "")), ") for ", cost, " zeny!")
		item_purchased.emit(String(item["name"]), cost)
	else:
		print("[Shop] Not enough zeny!")
