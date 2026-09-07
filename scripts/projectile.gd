# projectile.gd — Zaggers pooled ranged projectile (Godot mirror of web/fx/Projectiles.js).
# class_name ZaggersProjectile, extends Node2D.
#
# DESIGN (mirrors web rules):
# - Ranged single-target skills travel; melee physical stays instant.
#   Ranged = damageType magic OR classId in ranger/bard/alchemist.
# - Pool of 24, oldest fizzle. Slight arc, glow color by element.
# - On arrival: monster.take_damage(dmg, new_hp) + optional server
#   send_attack(real_id) — fixes the legacy send_attack("", ...) no-hit bug.
# - Web parity: arrow 11 u/s, bolt 8, orb 7 (in tiles/sec here, SPEED x32px).
# - Not auto-wired: see _INTEGRATION below. Zero cost when pool empty.
class_name ZaggersProjectile
extends Node2D

const POOL_MAX: int = 24
const SPEEDS: Dictionary = { "arrow": 352.0, "bolt": 256.0, "orb": 224.0 }
const RANGED_CLASSES: Array[String] = ["ranger", "bard", "alchemist"]

var target: ZaggersMonster = null
var target_pos: Vector2 = Vector2.ZERO
var from_pos: Vector2 = Vector2.ZERO
var travel_t: float = 0.0
var travel_dur: float = 0.3
var kind: String = "bolt"
var hit_color: Color = Color.WHITE
var damage: int = 10
var active: bool = false
var skill_ref: Dictionary = {}

var _draw_node: Node2D = null


static func kind_for(skill: Dictionary) -> String:
	if skill.is_empty():
		return ""
	if String(skill.get("damageType", "")) == "magic":
		return "bolt"
	if String(skill.get("classId", "")) in RANGED_CLASSES:
		return "arrow" if String(skill.get("classId", "")) == "ranger" else "orb"
	return ""


static func is_ranged(skill: Dictionary) -> bool:
	return kind_for(skill) != ""


func _ready() -> void:
	visible = false
	_draw_node = Node2D.new()
	add_child(_draw_node)


func launch(from: Vector2, tgt: ZaggersMonster, dmg: int, color: Color, skill: Dictionary) -> void:
	from_pos = from
	target = tgt
	target_pos = tgt.global_position if is_instance_valid(tgt) else from
	damage = dmg
	hit_color = color
	skill_ref = skill
	kind = kind_for(skill)
	if kind.is_empty():
		kind = "bolt"
	var dist: float = from.distance_to(target_pos)
	var speed: float = float(SPEEDS.get(kind, 256.0))
	travel_dur = maxf(0.12, dist / speed)
	travel_t = 0.0
	active = true
	visible = true
	global_position = from


func _physics_process(delta: float) -> void:
	if not active:
		return
	travel_t += delta
	var f: float = clampf(travel_t / travel_dur, 0.0, 1.0)
	if is_instance_valid(target) and target.hp > 0:
		target_pos = target.global_position
	global_position = from_pos.lerp(target_pos, f) + Vector2(0, -sin(f * PI) * 11.0)
	queue_redraw()
	if f >= 1.0:
		_impact()


func _impact() -> void:
	active = false
	visible = false
	if is_instance_valid(target) and target.hp > 0:
		target.take_damage(damage, maxi(0, target.hp - damage))
		if NetworkManager.instance:
			NetworkManager.instance.send_attack(target.monster_id, "down")


func _draw() -> void:
	if not active:
		return
	var r: float = 3.2 if kind == "arrow" else 4.2
	draw_circle(Vector2.ZERO, r, hit_color)
	draw_circle(Vector2.ZERO, r * 0.5, Color.WHITE)


# _INTEGRATION (paste into world.gd + player.gd, not applied):
#
# # world.gd — pool (add var _projectiles: Array[ZaggersProjectile] = []):
# func _spawn_projectile(from: Vector2, tgt: ZaggersMonster, dmg: int, color: Color, skill: Dictionary) -> void:
# 	for p in _projectiles:
# 		if not p.active:
# 			_entities_node.add_child(p) if p.get_parent() == null else null
# 			p.launch(from, tgt, dmg, color, skill)
# 			return
# 	if _projectiles.size() < ZaggersProjectile.POOL_MAX:
# 		var p := ZaggersProjectile.new()
# 		_entities_node.add_child(p)
# 		_projectiles.append(p)
# 		p.launch(from, tgt, dmg, color, skill)
#
# # player.gd perform_attack() ranged branch (nearest monster in 176px ≈ 5.5 tiles):
# # var skill := PartyData.hero_def(class_idx)  # + skill lookup
# # if ZaggersProjectile.is_ranged(skill):
# #   var best: ZaggersMonster = null; var best_d := 176.0
# #   for m in get_tree().get_nodes_in_group("monsters"):
# #     var d := global_position.distance_to((m as Node2D).global_position)
# #     if d < best_d: best_d = d; best = m
# #   if best: get_parent().get_parent()._spawn_projectile(global_position, best, 20, Color.WHITE, skill)
