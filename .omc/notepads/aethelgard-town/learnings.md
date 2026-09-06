# Aethelgard town densify learnings

- Prefer regenerating `envStructures` via `scripts/build_aethelgard_town.py` while preserving tiles/NPCs/exits/subRegions from the existing JSON.
- Do not pre-seed `occupied` with landmark cells (e.g. obelisk `0,0`) before placing those landmarks — radius-0 self-collision drops them.
- Inner-ring clearance should only cover the plaza ring (`|x| or |y| in {9,10}` within ±10), not the full cardinal axes; otherwise temple/market landmarks on district avenues are rejected.
- New building/wall PNGs (`env_house_*`, `env_wall_*`, `env_gatehouse`) may land mid-task — always `asset_exists()` before emitting types; use real PNG sizes for width/height/anchors.
- Wall curtains densify fast: 4-tile spacing blew past the ~150 prop budget; 4 per edge (16 total) + 4 corners + 4 gatehouses is enough.

