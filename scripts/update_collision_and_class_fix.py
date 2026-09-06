import re

with open(r'D:\ai-studio\Zaggers\web\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix confirmCharacterCreation() to set player.class and player.sprite properly
old_creation = """    player.sprite = c.sprite;
    player.str = c.stats.str;"""

new_creation = """    player.class = c.sprite;
    player.sprite = c.sprite;
    player.str = c.stats.str;"""

content = content.replace(old_creation, new_creation, 1)

# Fix player rendering to use player.sprite || player.class
content = content.replace("const playerImg = sprites[player.class];", "const playerImg = sprites[player.sprite || player.class || 'hero_knight'];", 1)

# 2. Add 2.5D Collision Engine function checkCollision(wx, wy)
collision_engine_js = """
  // 2.5D Isometric Structure & Boundary Collision Engine
  function checkCollision(wx, wy) {
    // 1. World Map Perimeter Bounds (Aethelgard 60x60 Grid: wx: -28..28, wy: -45..45)
    if (wx < -28 || wx > 28 || wy < -45 || wy > 45) return true;

    // 2. Environment Structures Collision Bounding Boxes
    for (let i = 0; i < envStructures.length; i++) {
      const s = envStructures[i];
      let radius = 0.8; // Default collision radius
      if (s.type === 'env_house_shop') radius = 2.2;
      else if (s.type === 'env_fountain') radius = 1.8;
      else if (s.type === 'env_market_stall') radius = 1.4;
      else if (s.type === 'env_crystal' || s.type === 'env_dungeon_pillar') radius = 1.0;
      else if (s.type === 'env_tree_meadow') radius = 0.9;
      else if (s.type === 'env_torch_brazier' || s.type === 'env_barrel_crate') radius = 0.7;

      const dist = Math.hypot(wx - s.wx, wy - s.wy);
      if (dist < radius) return true;
    }
    return false;
  }
"""

content = content.replace("  let selectedCreatorClassId = 'vanguard';", collision_engine_js + "\n  let selectedCreatorClassId = 'vanguard';", 1)

# 3. Update movement logic with collision checks and expand bounds to -28..28
old_move_logic = """    if (len > 0) {
      player.wx += (dwx / len) * player.speed;
      player.wy += (dwy / len) * player.speed;
      player.targetWx = player.wx;
      player.targetWy = player.wy;
      
      if (screenDir !== -1) player.dir = screenDir;
      player.frame = Math.floor(frameCount / 8) % 2 * 2;
    } else {
      const dwx_t = player.targetWx - player.wx;
      const dwy_t = player.targetWy - player.wy;
      const dist = Math.hypot(dwx_t, dwy_t);
      if (dist > 0.1) {
        const angle = Math.atan2(dwy_t, dwx_t);
        player.wx += Math.cos(angle) * player.speed;
        player.wy += Math.sin(angle) * player.speed;"""

new_move_logic = """    if (len > 0) {
      const stepX = (dwx / len) * player.speed;
      const stepY = (dwy / len) * player.speed;
      if (!checkCollision(player.wx + stepX, player.wy + stepY)) {
        player.wx += stepX;
        player.wy += stepY;
      } else if (!checkCollision(player.wx + stepX, player.wy)) {
        player.wx += stepX;
      } else if (!checkCollision(player.wx, player.wy + stepY)) {
        player.wy += stepY;
      }
      player.targetWx = player.wx;
      player.targetWy = player.wy;
      
      if (screenDir !== -1) player.dir = screenDir;
      player.frame = Math.floor(frameCount / 8) % 2 * 2;
    } else {
      const dwx_t = player.targetWx - player.wx;
      const dwy_t = player.targetWy - player.wy;
      const dist = Math.hypot(dwx_t, dwy_t);
      if (dist > 0.1) {
        const angle = Math.atan2(dwy_t, dwx_t);
        const stepX = Math.cos(angle) * player.speed;
        const stepY = Math.sin(angle) * player.speed;
        if (!checkCollision(player.wx + stepX, player.wy + stepY)) {
          player.wx += stepX;
          player.wy += stepY;
        } else if (!checkCollision(player.wx + stepX, player.wy)) {
          player.wx += stepX;
        } else if (!checkCollision(player.wx, player.wy + stepY)) {
          player.wy += stepY;
        } else {
          player.targetWx = player.wx;
          player.targetWy = player.wy;
        }"""

content = content.replace(old_move_logic, new_move_logic, 1)

# Update bounds from -15..15 to -28..28
content = content.replace("player.wx = Math.max(-15, Math.min(15, player.wx));", "player.wx = Math.max(-28, Math.min(28, player.wx));", 1)

with open(r'D:\ai-studio\Zaggers\web\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated Class Sprite rendering fix and 2.5D Collision engine successfully.")
