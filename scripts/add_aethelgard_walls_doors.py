"""
add_aethelgard_walls_doors.py

Adds a walled perimeter around Aethelgard's central Obelisk Plaza district
(subRegions "obelisk_plaza", bounds -9..9 both axes) using the new
env_wall_curtain / env_wall_corner / env_gatehouse props, with gatehouse
gaps aligned toward each neighboring district/exit so the plaza stays fully
navigable. Also drops a handful of env_door instances at existing building
entrances (shop, guild-hall-equivalent, temple, tavern) per
COLLISION_WALLS_DOORS_REPORT.md task 3.

Idempotent: running twice will not duplicate entries (guarded by a marker
field on each added structure).
"""
import json

PATH = r"D:\ai-studio\Zaggers\.claude\worktrees\agent-a3b12d2ecaed5d7b9\web\maps\aethelgard.json"
MARKER = "collisionPass"


def wall_seg(wx, wy):
    return {"type": "env_wall_curtain", "wx": wx, "wy": wy, "width": 96, "height": 128,
            "anchorX": 48, "anchorY": 116, MARKER: True}


def corner_seg(wx, wy):
    return {"type": "env_wall_corner", "wx": wx, "wy": wy, "width": 96, "height": 128,
            "anchorX": 48, "anchorY": 116, MARKER: True}


def gatehouse(wx, wy, name):
    return {"type": "env_gatehouse", "wx": wx, "wy": wy, "width": 160, "height": 192,
            "anchorX": 80, "anchorY": 178, "name": name, MARKER: True}


def door(wx, wy, name):
    return {"type": "env_door", "wx": wx, "wy": wy, "width": 64, "height": 96,
            "anchorX": 32, "anchorY": 88, "animated": True, "name": name, MARKER: True}


def main():
    with open(PATH, encoding="utf-8") as f:
        data = json.load(f)

    envs = data["envStructures"]
    # Wipe any prior run of this script (idempotent re-run)
    envs[:] = [e for e in envs if not e.get(MARKER)]

    PLAZA_MIN, PLAZA_MAX = -9, 9
    GATE_HALF = 1  # gate gap spans [-1, 1] on the edge's running axis

    new_structs = []

    # --- Plaza perimeter walls, one edge at a time, in steps of 2 tiles,
    # skipping the gate gap in the middle of each edge (Obelisk Plaza's four
    # district connections: north -> Rampart Gate/Gatewatch, south ->
    # Wetstone Docks, west -> Kestrel Market/Lantern Rows, east -> Ashen
    # Ward/High Temple).
    for x in range(PLAZA_MIN + 2, PLAZA_MAX - 1, 2):
        if abs(x) <= GATE_HALF:
            continue
        new_structs.append(wall_seg(x, PLAZA_MIN))  # north wall (wy = -9)
        new_structs.append(wall_seg(x, PLAZA_MAX))  # south wall (wy = 9)
    for y in range(PLAZA_MIN + 2, PLAZA_MAX - 1, 2):
        if abs(y) <= GATE_HALF:
            continue
        new_structs.append(wall_seg(PLAZA_MIN, y))  # west wall (wx = -9)
        new_structs.append(wall_seg(PLAZA_MAX, y))  # east wall (wx = 9)

    # Corners
    new_structs.append(corner_seg(PLAZA_MIN, PLAZA_MIN))
    new_structs.append(corner_seg(PLAZA_MAX, PLAZA_MIN))
    new_structs.append(corner_seg(PLAZA_MIN, PLAZA_MAX))
    new_structs.append(corner_seg(PLAZA_MAX, PLAZA_MAX))

    # Gatehouses marking the four plaza entrances (visual only at the gap -
    # the gap itself stays clear so the plaza is never sealed off)
    new_structs.append(gatehouse(0, PLAZA_MIN, "Obelisk Plaza North Gate"))
    new_structs.append(gatehouse(0, PLAZA_MAX, "Obelisk Plaza South Gate"))
    new_structs.append(gatehouse(PLAZA_MIN, 0, "Obelisk Plaza West Gate"))
    new_structs.append(gatehouse(PLAZA_MAX, 0, "Obelisk Plaza East Gate"))

    # --- Building-entrance doors (task 3) ---
    # Kestrel Consignment House (shop) at (-18, 0), steward NPC at (-17, -1)
    new_structs.append(door(-18, 2, "Kestrel Consignment House Door"))
    # Elder's House (guild-hall-equivalent / town elder) at (-18, -18)
    new_structs.append(door(-18, -16, "Elder's House Door"))
    # High Temple Nave (env_stained_arch) at (18, 0)
    new_structs.append(door(18, 3, "High Temple Door"))
    # The Barnacle Tavern (shop) at (-8, 18)
    new_structs.append(door(-8, 20, "Barnacle Tavern Door"))

    envs.extend(new_structs)

    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Added {len(new_structs)} wall/gatehouse/door structures to {PATH}")


if __name__ == "__main__":
    main()
