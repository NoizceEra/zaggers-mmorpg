# parallax_background.gd — Zaggers Godot parallax background.
# class_name ZaggersParallax, extends ParallaxBackground.
#
# RESEARCH (codebase facts, verified 2026-09-07):
# - scripts/world.gd `_build_isometric_terrain()` brute-forces ~600 sprites:
#     for y in range(0, 700, 32):          # 22 rows
#       for x in range(0, 900, 32):        # ~29 cols  -> 22*29 = 638 Sprite2D
#     each Sprite2D optionally regions res://assets/tiles_ff/tileset_town_ff.png
#     (32x32 region) under a `TerrainGrid` Node2D. No culling, no chunking.
# - `_setup_camera()` creates Camera2D as a CHILD of the player:
#     _camera.zoom = Vector2(1.75, 1.75)
#     _camera.position_smoothing_enabled = true
#   => camera moves via player + smoothing; parallax must NEVER touch the camera.
# - scenes/world.tscn is 6 lines, root Node2D + ext_resource world.gd only.
#   All nodes (Entities, TerrainGrid, Camera2D, HUD, Shop) are built via `.new()`.
#   Parallax integration therefore stays code-first (see snippet below).
# - project.godot: 640x360 viewport, window stretch mode `canvas_items`, aspect
#   `keep`, window overrides 1280x720. Parallax art must survive 640x360 with
#   zoom 1.75 (visible area ~366x206 px) — wide mirrored sprites are required.
# - web/index.html `ZONE_ATMOSPHERE` (lines ~994-1000) is the tint authority:
#     aethelgard: tint null
#     gatewatch:  rgb(255,224,178) a=0.05 source-over
#     meadows:    rgb(255,238,170) a=0.10 source-over + pollen
#     sanctum:    rgb(30,110,120)  a=0.22 multiply   + motes
#     spire:      rgb(160,40,20)   a=0.20 multiply   + ash
#     chasm:      rgb(150,195,255) a=0.20 multiply   + snow
#     rootways:   rgb(80,25,105)   a=0.30 multiply   + rootmotes
#   ZONE_TINTS below mirrors these values 1:1 for parity (modulate hook).
#
# DESIGN:
# - Extends ParallaxBackground so camera-follow is NATIVE (engine reads the
#   Camera2D scroll each frame). This script never touches Camera2D position,
#   offset, smoothing, or zoom -> no fight with position_smoothing_enabled.
# - 3 ParallaxLayer children, motion_scale 0.15 (far) / 0.35 (mid) / 0.6 (near).
# - Infinite X: each layer holds 3 mirrored Sprite2Ds at x = -W, 0, +W AND sets
#   ParallaxLayer.motion_mirroring.x = W, so scrolling past one tile wraps.
# - No dedicated parallax PNGs ship in assets/ yet, so set_zone() reuses the
#   existing tilesets (town/meadow/dungeon + per-zone accent tiles). Missing
#   files fall back gracefully (layer keeps previous texture, never crashes).
class_name ZaggersParallax
extends ParallaxBackground

## Parallax factors per layer: far / mid / near.
const MOTION_SCALES: Array[float] = [0.15, 0.35, 0.6]
## How many mirrored copies per layer (covers 640px viewport at zoom 1.75
## plus smoothing overshoot; engine mirroring extends beyond these).
const MIRROR_COPIES: int = 3
## Vertical offsets give a fake horizon: far sits higher on screen.
const LAYER_Y_OFFSETS: Array[float] = [-80.0, -20.0, 60.0]

# Reused art — these files exist in assets/tiles_ff/ (verified).
const TEX_TOWN: String = "res://assets/tiles_ff/tileset_town_ff.png"
const TEX_MEADOW: String = "res://assets/tiles_ff/tileset_meadow_ff.png"
const TEX_DUNGEON: String = "res://assets/tiles_ff/tileset_dungeon_ff.png"
const TEX_SANCTUM: String = "res://assets/tiles_ff/tile_sanctum_marble.png"
const TEX_SPIRE: String = "res://assets/tiles_ff/tile_spire_basalt.png"
const TEX_CHASM: String = "res://assets/tiles_ff/tile_ice_mirror.png"
const TEX_ROOT: String = "res://assets/tiles_ff/tile_root_bark.png"

## Per-zone [far, mid, near] texture paths. Ids match
## web/zaggers_database.json zones[].id exactly.
const ZONE_TEXTURES: Dictionary = {
	"aethelgard": [TEX_TOWN, TEX_TOWN, TEX_MEADOW],
	"gatewatch": [TEX_TOWN, TEX_MEADOW, TEX_TOWN],
	"meadows": [TEX_MEADOW, TEX_MEADOW, TEX_TOWN],
	"sanctum": [TEX_SANCTUM, TEX_DUNGEON, TEX_DUNGEON],
	"spire": [TEX_SPIRE, TEX_DUNGEON, TEX_DUNGEON],
	"chasm": [TEX_CHASM, TEX_DUNGEON, TEX_SPIRE],
	"rootways": [TEX_ROOT, TEX_DUNGEON, TEX_ROOT],
}

## Zone tint parity with web/index.html ZONE_ATMOSPHERE.
## Stored as [Color(r,g,b 0-1), alpha, blend_mode_string].
## `blend` is informational (web canvas compositing); Godot Sprite2D.modulate
## is always a multiply, so we lerp White -> tint color by alpha.
const ZONE_TINTS: Dictionary = {
	"aethelgard": [Color(1, 1, 1), 0.0, "none"],
	"gatewatch": [Color(1.0, 0.878, 0.698), 0.05, "source-over"],
	"meadows": [Color(1.0, 0.933, 0.667), 0.10, "source-over"],
	"sanctum": [Color(0.118, 0.431, 0.471), 0.22, "multiply"],
	"spire": [Color(0.627, 0.157, 0.078), 0.20, "multiply"],
	"chasm": [Color(0.588, 0.765, 1.0), 0.20, "multiply"],
	"rootways": [Color(0.314, 0.098, 0.412), 0.30, "multiply"],
}

var _layers: Array[ParallaxLayer] = []
var _layer_sprites: Array[Array] = [] # per-layer Array[Sprite2D]
var _current_zone: String = ""


func _ready() -> void:
	# Render behind the world (TerrainGrid sprites are at default CanvasItem
	# z; ParallaxBackground is a CanvasLayer so `layer` orders it globally).
	layer = -100
	_build_layers()
	if not _current_zone.is_empty():
		set_zone(_current_zone)


func _build_layers() -> void:
	for child in get_children():
		if child is ParallaxLayer:
			child.queue_free()
	_layers.clear()
	_layer_sprites.clear()
	for i in range(MOTION_SCALES.size()):
		var pl := ParallaxLayer.new()
		pl.name = "ParallaxLayer_%d" % i
		var s: float = MOTION_SCALES[i]
		pl.motion_scale = Vector2(s, s)
		pl.motion_offset = Vector2(0, LAYER_Y_OFFSETS[i])
		add_child(pl)
		_layers.append(pl)
		_layer_sprites.append([])
	# Default zone so the scene never renders empty.
	_apply_zone_textures("aethelgard")
	_apply_zone_tint("aethelgard")


## Swap far/mid/near textures for a zone id. Unknown ids fall back to the
## current zone (or aethelgard) and push a warning instead of crashing.
## Safe to call before _ready() (applies on _ready via _current_zone).
func set_zone(zone_id: String) -> void:
	var zid: String = zone_id.to_lower()
	if not ZONE_TEXTURES.has(zid):
		push_warning("[ZaggersParallax] unknown zone '%s', keeping '%s'." % [zone_id, _current_zone])
		return
	_current_zone = zid
	# _layers may not exist yet if called before _ready/_build_layers.
	if _layers.is_empty():
		return
	_apply_zone_textures(zid)
	_apply_zone_tint(zid)


func get_zone() -> String:
	return _current_zone


## Direct modulate override hook (e.g. day/night tween, damage flash).
## Multiplies onto the current zone tint for the given layer (-1 = all).
func set_layer_tint(layer_idx: int, color: Color) -> void:
	if layer_idx < 0:
		for sprites in _layer_sprites:
			for sp in sprites:
				(sp as Sprite2D).modulate = color
	elif layer_idx >= 0 and layer_idx < _layer_sprites.size():
		for sp in _layer_sprites[layer_idx]:
			(sp as Sprite2D).modulate = color


func _apply_zone_textures(zid: String) -> void:
	var paths: Array = ZONE_TEXTURES.get(zid, ZONE_TEXTURES["aethelgard"])
	for i in range(_layers.size()):
		var tex_path: String = String(paths[mini(i, paths.size() - 1)])
		var tex: Texture2D = null
		if ResourceLoader.exists(tex_path):
			tex = load(tex_path) as Texture2D
		if tex == null:
			push_warning("[ZaggersParallax] missing texture '%s', layer %d unchanged." % [tex_path, i])
			continue
		_set_layer_texture(i, tex)


func _set_layer_texture(layer_idx: int, tex: Texture2D) -> void:
	var pl: ParallaxLayer = _layers[layer_idx]
	# Clear old mirrors.
	for sp in _layer_sprites[layer_idx]:
		(sp as Sprite2D).queue_free()
	_layer_sprites[layer_idx].clear()
	# Tile width: full texture width keeps seams minimal for tilesets;
	# scale far layers up slightly so 640px @ zoom 1.75 is always covered.
	var tile_w: float = float(tex.get_width())
	var y_scale: float = 1.0 + float(layer_idx) * 0.35
	pl.motion_mirroring = Vector2(tile_w, 0)
	for c in range(MIRROR_COPIES):
		var sp := Sprite2D.new()
		sp.texture = tex
		sp.centered = true
		sp.scale = Vector2(1.0, y_scale)
		# x = -W, 0, +W -> seamless strip; engine mirroring repeats it.
		sp.position = Vector2((float(c) - 1.0) * tile_w, 0)
		pl.add_child(sp)
		_layer_sprites[layer_idx].append(sp)
	# Re-apply tint so a texture swap never drops the zone color-grade.
	if not _current_zone.is_empty():
		_apply_zone_tint(_current_zone)


## Web parity: modulate = White.lerp(tint_color, alpha).
## aethelgard (alpha 0) stays pure white = no tint, exactly like web.
func _apply_zone_tint(zid: String) -> void:
	var entry: Array = ZONE_TINTS.get(zid, ZONE_TINTS["aethelgard"])
	var tint_color: Color = entry[0]
	var alpha: float = float(entry[1])
	var final_mod := Color(1, 1, 1).lerp(tint_color, clampf(alpha, 0.0, 1.0))
	for sprites in _layer_sprites:
		for sp in sprites:
			(sp as Sprite2D).modulate = final_mod
