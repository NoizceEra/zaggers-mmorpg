import json, os, glob

project_root = r"D:\ai-studio\Zaggers"
maps_dir = os.path.join(project_root, "web", "maps")

def update_aethelgard():
    path = os.path.join(maps_dir, "aethelgard.json")
    if not os.path.exists(path): return
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    existing_types = {e.get("name"): e for e in data.get("envStructures", [])}
    
    new_buildings = [
        {"type": "env_house_smithy", "wx": -18, "wy": 12, "width": 64, "height": 64, "anchorX": 32, "anchorY": 48, "name": "Blacksmith Forge"},
        {"type": "env_house_inn", "wx": 18, "wy": -12, "width": 64, "height": 64, "anchorX": 32, "anchorY": 48, "name": "Travelers Inn"},
        {"type": "env_house_guild", "wx": 18, "wy": 0, "width": 64, "height": 64, "anchorX": 32, "anchorY": 48, "name": "Adventurer Guild Hall"},
        {"type": "env_house_temple", "wx": 18, "wy": 12, "width": 64, "height": 64, "anchorX": 32, "anchorY": 48, "name": "Sanctuary Temple"}
    ]

    for b in new_buildings:
        if b["name"] not in existing_types:
            data["envStructures"].append(b)
            print(f"Added 3D Building to Aethelgard: {b['name']}")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def update_other_maps():
    for path in glob.glob(os.path.join(maps_dir, "*.json")):
        if "aethelgard.json" in path: continue
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        env = data.get("envStructures", [])
        updated = False
        for e in env:
            # Upgrade generic walls near center into 3D shelter buildings
            if e.get("type") == "env_wall_curtain" and abs(e.get("wx", 0)) > 10 and abs(e.get("wy", 0)) > 10:
                e["type"] = "env_house_row"
                e["name"] = "Outpost Shelter"
                updated = True

        if updated:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print(f"Updated 3D building blocks in {os.path.basename(path)}")

if __name__ == "__main__":
    update_aethelgard()
    update_other_maps()
