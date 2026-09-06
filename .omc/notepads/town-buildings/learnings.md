# Town buildings / walls art pass

- Regenerable via `scripts/generate_town_buildings.py` (Pillow iso helpers mirroring `generate_env_assets.py`).
- Writes both `assets/tiles_ff/` and `web/assets/tiles_ff/`.
- Shop upgrade kept as faithful recreation of original shop polygons (front-gable overlay on parametric roof looked wrong).
- Collision radii for the 8 new types already present in `web/index.html` (another agent); only preload list was extended here.
- Do not edit `web/maps/aethelgard.json` from this pass.
