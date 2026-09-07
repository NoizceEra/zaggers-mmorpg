# party_data.gd — Zaggers Character & Job Class Data Singleton.
class_name PartyData
extends Node

signal gold_changed(new_gold: int)
signal stats_changed(hero_idx: int, hp: int, max_hp: int, sp: int, max_sp: int, level: int)

# Ragnarok Online Job Classes — mirrors web/zaggers_database.json classes (11).
# First 7 entries preserved byte-for-byte for save compat; db_id added for mapping.
# Order: vanguard, spellweaver, cleric, dragoon, ranger, shadowblade, monk, + paladin/sage/bard/alchemist.
const HERO_DEFS: Array = [
	{
		"db_id": "vanguard",
		"name": "Knight", "title": "Paladin of Light",
		"max_hp": 180, "max_sp": 50, "atk": 24, "matk": 6,
		"defense": 10, "speed": 120.0,
		"icon": "res://assets/sprites_ff/hero_knight.png",
	},
	{
		"db_id": "spellweaver",
		"name": "BlackMage", "title": "Shadow Wizard",
		"max_hp": 90, "max_sp": 140, "atk": 8, "matk": 28,
		"defense": 2, "speed": 95.0,
		"icon": "res://assets/sprites_ff/hero_blackmage.png",
	},
	{
		"db_id": "cleric",
		"name": "WhiteMage", "title": "Holy Priest",
		"max_hp": 110, "max_sp": 120, "atk": 10, "matk": 22,
		"defense": 5, "speed": 100.0,
		"icon": "res://assets/sprites_ff/hero_whitemage.png",
	},
	{
		"db_id": "dragoon",
		"name": "Dragoon", "title": "Sky Lancer",
		"max_hp": 160, "max_sp": 60, "atk": 22, "matk": 8,
		"defense": 7, "speed": 125.0,
		"icon": "res://assets/sprites_ff/hero_dragoon.png",
	},
	{
		"db_id": "ranger",
		"name": "RedMage", "title": "Crimson Fencer",
		"max_hp": 135, "max_sp": 90, "atk": 18, "matk": 18,
		"defense": 6, "speed": 110.0,
		"icon": "res://assets/sprites_ff/hero_redmage.png",
	},
	{
		"db_id": "shadowblade",
		"name": "Thief", "title": "Shadow Assassin",
		"max_hp": 120, "max_sp": 50, "atk": 19, "matk": 6,
		"defense": 4, "speed": 145.0,
		"icon": "res://assets/sprites_ff/hero_thief.png",
	},
	{
		"db_id": "monk",
		"name": "Monk", "title": "Iron Brawler",
		"max_hp": 190, "max_sp": 30, "atk": 26, "matk": 4,
		"defense": 6, "speed": 115.0,
		"icon": "res://assets/sprites_ff/hero_monk.png",
	},
	{
		"db_id": "paladin",
		"name": "Paladin", "title": "Templar of Light",
		"max_hp": 200, "max_sp": 60, "atk": 20, "matk": 12,
		"defense": 12, "speed": 100.0,
		"icon": "res://assets/sprites_ff/hero_paladin.png",
	},
	{
		"db_id": "sage",
		"name": "Sage", "title": "Arcane Scholar",
		"max_hp": 100, "max_sp": 150, "atk": 8, "matk": 26,
		"defense": 3, "speed": 100.0,
		"icon": "res://assets/sprites_ff/hero_sage.png",
	},
	{
		"db_id": "bard",
		"name": "Bard", "title": "Wandering Minstrel",
		"max_hp": 125, "max_sp": 80, "atk": 14, "matk": 12,
		"defense": 5, "speed": 130.0,
		"icon": "res://assets/sprites_ff/hero_bard.png",
	},
	{
		"db_id": "alchemist",
		"name": "Alchemist", "title": "Potion Master",
		"max_hp": 130, "max_sp": 90, "atk": 16, "matk": 16,
		"defense": 6, "speed": 105.0,
		"icon": "res://assets/sprites_ff/hero_alchemist.png",
	},
]

static var instance: PartyData = null
var active_hero_idx: int = 0
var gold: int = 500


static func get_instance() -> PartyData:
	if instance == null:
		instance = PartyData.new()
	return instance


func _init() -> void:
	instance = self


static func hero_def(idx: int) -> Dictionary:
	if idx < 0 or idx >= HERO_DEFS.size():
		return {}
	return HERO_DEFS[idx]


func add_gold(amount: int) -> void:
	gold = maxi(0, gold + amount)
	gold_changed.emit(gold)


func spend_gold(amount: int) -> bool:
	if gold < amount:
		return false
	gold -= amount
	gold_changed.emit(gold)
	return true
