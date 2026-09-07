# network_ext.gd — P0 netcode: the two packet arms missing from network_manager.gd.
#
# SERVER ALREADY SENDS (see server/server.js):
#   * {"type": "monster_respawn", "id", "hp", "x", "y"}  (server.js:166, respawn timer)
#   * {"type": "stats_update", "player": {...}}          (server.js:181, stat_add reply)
# CLIENT DROPS BOTH: NetworkManager._parse_packet() has no "monster_respawn"
# or "stats_update" arm, so respawns never render and stat-point allocation
# never reflects server-authoritative values.
#
# DESIGN: signals live here (not in NetworkManager) so this file is the only
# new dependency. network_manager.gd needs a 6-line patch that forwards the
# two packet types (see scripts/net_snapshot.patch.md §3). world.gd connects
# to these signals exactly like the existing NetworkManager ones.
class_name NetworkExt
extends Node

## Emitted when the server respawns a monster (full HP, usually same x/y).
signal monster_respawned(id: String, hp: int, x: float, y: float)
## Emitted with the full server-authoritative player dict after stat_add.
signal stats_updated(player: Dictionary)

static var instance: NetworkExt = null


func _init() -> void:
	instance = self


func _exit_tree() -> void:
	if instance == self:
		instance = null


## Route one packet. Returns true when pkt_type was handled.
## Called by the patched NetworkManager._parse_packet(); harmless to call
## directly in unit tests with hand-built dictionaries.
func handle_packet(pkt_type: String, data: Dictionary) -> bool:
	match pkt_type:
		"monster_respawn":
			monster_respawned.emit(
				String(data.get("id", "")),
				int(data.get("hp", 0)),
				float(data.get("x", 0.0)),
				float(data.get("y", 0.0))
			)
			return true
		"stats_update":
			stats_updated.emit(data.get("player", {}) as Dictionary)
			return true
	return false
