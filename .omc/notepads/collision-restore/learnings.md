# Collision restore learnings
- checkCollision lives after checkZoneExits (~823); uses dynamic currentMapBounds, customTileMap tile_town_border + 2.5 exit gaps, type-based envStructures radii.
- WASD and click-to-move both axis-slide via checkCollision; do not reuse scripts/update_collision_and_class_fix.py hardcoded -28..45 bounds.
