# zaggers_audio.gd — procedural audio, zero asset files. Autoload-ready.
# Mirrors web/audio/ZaggersAudio.js recipes (swing/hit/crit/coin/levelup/ui
# + per-zone ambient pad) using AudioServer buses + generated AudioStreamWAV.
#
# Setup (do NOT overwrite project.godot — merge this snippet under [autoload]):
#   ZaggersAudio="*res://scripts/zaggers_audio.gd"
# Full project.godot bus snippet is returned alongside this file (see below).
class_name ZaggersAudio
extends Node

const SAMPLE_RATE: int = 22050
const BUS_MASTER: StringName = &"Master"
const BUS_SFX: StringName = &"SFX"
const BUS_BGM: StringName = &"BGM"

# Zone pad recipes — keys match MAP_REGISTRY ids (aethelgard, gatewatch,
# meadows, sanctum, spire, chasm, rootways) and web ZONE_PAD.
const ZONE_PAD_FREQ: Dictionary = {
	"aethelgard": 220.0,
	"gatewatch": 246.9,
	"meadows": 329.6,
	"sanctum": 196.0,
	"spire": 146.8,
	"chasm": 440.0,
	"rootways": 164.8,
}

var _sfx_streams: Dictionary = {} # name -> AudioStreamWAV
var _sfx_players: Array[AudioStreamPlayer] = []
var _bgm_player: AudioStreamPlayer
var _current_zone: String = ""
var _low_graphics: bool = false
const MAX_VOICES: int = 12
const MAX_VOICES_LOW: int = 6


func _ready() -> void:
	_ensure_buses()
	_bg_m_player_setup()
	_prewarm_sfx()


func _ensure_buses() -> void:
	_ensure_bus(BUS_SFX)
	_ensure_bus(BUS_BGM)


func _ensure_bus(bus_name: StringName) -> void:
	if AudioServer.bus_count <= 0:
		return
	var idx: int = AudioServer.get_bus_index(bus_name)
	if idx == -1:
		AudioServer.add_bus(AudioServer.bus_count)
		AudioServer.set_bus_name(AudioServer.bus_count - 1, bus_name)


func _bg_m_player_setup() -> void:
	_bgm_player = AudioStreamPlayer.new()
	_bgm_player.name = "BGMPadPlayer"
	_bgm_player.bus = BUS_BGM
	add_child(_bgm_player)


func set_low_graphics(on: bool) -> void:
	_low_graphics = on


func voice_cap() -> int:
	return MAX_VOICES_LOW if _low_graphics else MAX_VOICES


# --- procedural tone builder (matches web oscillator recipes) -------------
func _make_tone(freq_start: float, freq_end: float, duration: float, wave: String, volume: float) -> AudioStreamWAV:
	var frames: int = int(SAMPLE_RATE * duration)
	var data := PackedByteArray()
	data.resize(frames * 2) # 16-bit mono
	var phase: float = 0.0
	for i in range(frames):
		var t: float = float(i) / float(frames)
		var freq: float = lerpf(freq_start, freq_end, t)
		phase += TAU * freq / float(SAMPLE_RATE)
		var s: float
		match wave:
			"square":
				s = 1.0 if sin(phase) >= 0.0 else -1.0
			"saw":
				s = fmod(phase, TAU) / PI - 1.0
			"triangle":
				s = 2.0 * abs(2.0 * fmod(phase / TAU, 1.0) - 1.0) - 1.0
			_:
				s = sin(phase)
		# Simple attack/decay envelope so beeps don't click.
		var env: float = minf(float(i) / (0.008 * SAMPLE_RATE), 1.0) * (1.0 - t)
		var v: int = int(clampf(s * volume * env, -1.0, 1.0) * 32767.0)
		data.encode_s16(i * 2, v)
	var stream := AudioStreamWAV.new()
	stream.format = AudioStreamWAV.FORMAT_16_BITS
	stream.mix_rate = SAMPLE_RATE
	stream.stereo = false
	stream.data = data
	return stream


func _sfx_recipe(sfx_name: String) -> AudioStreamWAV:
	match sfx_name:
		"swing":
			return _make_tone(900.0, 300.0, 0.18, "sine", 0.5)
		"hit":
			return _make_tone(220.0, 80.0, 0.14, "square", 0.45)
		"crit":
			return _make_tone(440.0, 110.0, 0.22, "saw", 0.5)
		"coin":
			return _make_tone(988.0, 1319.0, 0.22, "sine", 0.45)
		"levelup":
			return _make_tone(523.0, 1047.0, 0.5, "triangle", 0.45)
		"ui":
			return _make_tone(660.0, 660.0, 0.06, "sine", 0.35)
	return _make_tone(440.0, 440.0, 0.1, "sine", 0.3)


func _prewarm_sfx() -> void:
	for sfx_name in ["swing", "hit", "crit", "coin", "levelup", "ui"]:
		_sfx_streams[sfx_name] = _sfx_recipe(sfx_name)


func play_sfx(sfx_name: String, volume_db: float = 0.0) -> void:
	if not _sfx_streams.has(sfx_name):
		_sfx_streams[sfx_name] = _sfx_recipe(sfx_name)
	# Voice cap (lowGraphics halves) — reuse finished players first.
	_prune_players()
	var cap: int = voice_cap()
	if _active_sfx_count() >= cap:
		return
	var p := AudioStreamPlayer.new()
	p.stream = _sfx_streams[sfx_name]
	p.bus = BUS_SFX
	p.volume_db = volume_db
	add_child(p)
	_sfx_players.append(p)
	p.finished.connect(_on_sfx_finished.bind(p))
	p.play()


func _active_sfx_count() -> int:
	var n: int = 0
	for p in _sfx_players:
		if is_instance_valid(p) and p.playing:
			n += 1
	return n


func _prune_players() -> void:
	_sfx_players = _sfx_players.filter(
		func(p: AudioStreamPlayer) -> bool: return is_instance_valid(p) and p.playing
	)


func _on_sfx_finished(p: AudioStreamPlayer) -> void:
	if is_instance_valid(p):
		p.queue_free()


# --- per-zone ambient pad: 2s looped sine pad at the zone root + fifth -----
func play_bgm(zone: String) -> void:
	if zone == _current_zone and _bgm_player.playing:
		return
	_current_zone = zone
	if not ZONE_PAD_FREQ.has(zone):
		_bgm_player.stop()
		return
	var root: float = float(ZONE_PAD_FREQ[zone])
	var stream: AudioStreamWAV = _make_pad_loop(root, root * 1.5)
	stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
	stream.loop_begin = 0
	stream.loop_end = stream.get_data().size() / 2
	_bgm_player.stream = stream
	_bgm_player.volume_db = -14.0
	_bgm_player.play()


func _make_pad_loop(f1: float, f2: float) -> AudioStreamWAV:
	var seconds: float = 2.0
	var frames: int = int(SAMPLE_RATE * seconds)
	var data := PackedByteArray()
	data.resize(frames * 2)
	for i in range(frames):
		var ph: float = float(i) / float(SAMPLE_RATE)
		var s: float = 0.6 * sin(TAU * f1 * ph) + 0.4 * sin(TAU * f2 * ph)
		s *= 0.3
		# Crossfade loop seam so LOOP_FORWARD doesn't click.
		var edge: int = int(0.05 * SAMPLE_RATE)
		if i < edge:
			s *= float(i) / float(edge)
		elif i >= frames - edge:
			s *= float(frames - i) / float(edge)
		data.encode_s16(i * 2, int(clampf(s, -1.0, 1.0) * 32767.0))
	var stream := AudioStreamWAV.new()
	stream.format = AudioStreamWAV.FORMAT_16_BITS
	stream.mix_rate = SAMPLE_RATE
	stream.stereo = false
	stream.data = data
	return stream


func stop_bgm() -> void:
	_current_zone = ""
	if is_instance_valid(_bgm_player):
		_bgm_player.stop()
