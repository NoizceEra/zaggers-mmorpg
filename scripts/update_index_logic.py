import re

with open(r'D:\ai-studio\Zaggers\web\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update NPC locations for expanded districts
new_npcs = """  // Town NPCs distributed across Aethelgard Master Town Districts
  const npcs = [
    {
      id: 'kafra',
      name: '[NPC] Kafra Staff',
      title: 'Kafra Service Staff',
      wx: 0, wy: -2,
      dir: 0, frame: 1,
      sprite: 'npc_kafra',
      dialogHeader: 'Kafra Service Staff',
      dialogText: 'Welcome to the Aethelgard Kafra Depot! We provide save point recording and teleportation services across the 5 realms. How may I serve you today, adventurer?',
      options: [
        { text: '💾 Save Position & Heal (Aethelgard)', action: 'kafra_save' },
        { text: '🌀 Teleport to Wilderness Fields', action: 'kafra_teleport' },
        { text: '❌ Cancel', action: 'close' }
      ]
    },
    {
      id: 'merchant',
      name: '[NPC] Market Merchant',
      title: 'Market Bazaar Trader',
      wx: 18, wy: 0,
      dir: 0, frame: 1,
      sprite: 'npc_merchant',
      dialogHeader: 'Market Merchant',
      dialogText: 'Welcome to the Market Bazaar! I have fresh potions brewed from royal herbs and sturdy adventure equipment. What would you like to buy?',
      options: [
        { text: '🧪 Open Item Shop (Potions & Gear)', action: 'open_shop' },
        { text: '🍷 Buy Red Potion (50 z)', action: 'buy_red_potion' },
        { text: '❌ Cancel', action: 'close' }
      ]
    },
    {
      id: 'blacksmith',
      name: '[NPC] Master Smith',
      title: 'Smithy Row Blacksmith',
      wx: -18, wy: 0,
      dir: 0, frame: 1,
      sprite: 'npc_blacksmith',
      dialogHeader: 'Master Smith Ironhide',
      dialogText: 'Clang! Clang! Welcome to Smithy Row! Need your weapon sharpened or your armor reinforced? I can upgrade your gear for a modest fee!',
      options: [
        { text: '⚔️ Refine Weapon (+2 STR) [100 z]', action: 'upgrade_weapon' },
        { text: '🛡️ Reinforce Armor (+20 Max HP, +10 Max SP) [150 z]', action: 'upgrade_armor' },
        { text: '❌ Cancel', action: 'close' }
      ]
    },
    {
      id: 'elder',
      name: '[NPC] Guildmaster',
      title: 'Training Grounds Elder',
      wx: 0, wy: 18,
      dir: 0, frame: 1,
      sprite: 'npc_elder',
      dialogHeader: 'Guildmaster Elder',
      dialogText: 'Greetings, brave hero. Shadows grow long in the surrounding wilderness and monsters threaten Aethelgard. Are you ready to take on a hero’s quest?',
      options: [
        { text: '📜 Accept Quest: Defeat Lord Baphomet', action: 'quest_accept' },
        { text: '🎁 Claim Quest Reward (500 z)', action: 'quest_claim' },
        { text: '💡 Seek Wisdom & Training Advice', action: 'elder_advice' },
        { text: '❌ Cancel', action: 'close' }
      ]
    }
  ];"""

content = re.sub(r'  // Town NPCs \(Placed in Town Center.*?\n  \];', new_npcs, content, flags=re.DOTALL)

# 2. Update envStructures for 6 expansive districts
new_env_structures = """  // 2.5D Isometric Environment Structures Library (Expanded Multi-District Aethelgard & Wilderness)
  const envStructures = [
    // District 1: Grand Fountain Plaza (Center: wx: -8..8, wy: -8..8)
    { type: 'env_fountain', wx: 0, wy: 0, width: 96, height: 96, anchorX: 48, anchorY: 64, name: 'Aethelgard Central Fountain' },
    { type: 'env_crystal', wx: 0, wy: 3, width: 64, height: 96, anchorX: 32, anchorY: 82, name: 'Aetherite Save Crystal' },
    { type: 'env_market_stall', wx: -4, wy: -3, width: 96, height: 96, anchorX: 48, anchorY: 64, name: 'Kafra Info Booth' },
    { type: 'env_barrel_crate', wx: -5.2, wy: -3.2, width: 64, height: 64, anchorX: 32, anchorY: 48 },
    { type: 'env_barrel_crate', wx: 4.2, wy: -1.2, width: 64, height: 64, anchorX: 32, anchorY: 48 },

    // District 2: Smithy Row (West: wx: -25..-9, wy: -10..10)
    { type: 'env_house_shop', wx: -18, wy: -4, width: 128, height: 128, anchorX: 64, anchorY: 98, name: 'Ironhide Blacksmith Forge' },
    { type: 'env_barrel_crate', wx: -20, wy: 2, width: 64, height: 64, anchorX: 32, anchorY: 48 },
    { type: 'env_barrel_crate', wx: -16, wy: 3, width: 64, height: 64, anchorX: 32, anchorY: 48 },
    { type: 'env_torch_brazier', wx: -15, wy: -2, width: 64, height: 64, anchorX: 32, anchorY: 54, animated: true },
    { type: 'env_torch_brazier', wx: -15, wy: 2, width: 64, height: 64, anchorX: 32, anchorY: 54, animated: true },

    // District 3: High Temple Plaza (North: wx: -10..10, wy: -25..-9)
    { type: 'env_dungeon_pillar', wx: -6, wy: -18, width: 64, height: 128, anchorX: 32, anchorY: 116 },
    { type: 'env_dungeon_pillar', wx: 6, wy: -18, width: 64, height: 128, anchorX: 32, anchorY: 116 },
    { type: 'env_crystal', wx: 0, wy: -20, width: 64, height: 96, anchorX: 32, anchorY: 82, name: 'High Temple Sanctuary Shrine' },
    { type: 'env_torch_brazier', wx: -3, wy: -16, width: 64, height: 64, anchorX: 32, anchorY: 54, animated: true },
    { type: 'env_torch_brazier', wx: 3, wy: -16, width: 64, height: 64, anchorX: 32, anchorY: 54, animated: true },

    // District 4: Market District & Bazaars (East: wx: 9..25, wy: -10..10)
    { type: 'env_market_stall', wx: 18, wy: -3, width: 96, height: 96, anchorX: 48, anchorY: 64, name: 'Potion & Elixir Stall' },
    { type: 'env_market_stall', wx: 18, wy: 3, width: 96, height: 96, anchorX: 48, anchorY: 64, name: 'Exotic Goods Merchant' },
    { type: 'env_barrel_crate', wx: 16, wy: 0, width: 64, height: 64, anchorX: 32, anchorY: 48 },
    { type: 'env_barrel_crate', wx: 21, wy: -2, width: 64, height: 64, anchorX: 32, anchorY: 48 },

    // District 5: Adventurer Guild & Training Grounds (South: wx: -10..10, wy: 9..25)
    { type: 'env_house_shop', wx: 0, wy: 22, width: 128, height: 128, anchorX: 64, anchorY: 98, name: 'Adventurer Guild Hall' },
    { type: 'env_barrel_crate', wx: -4, wy: 16, width: 64, height: 64, anchorX: 32, anchorY: 48, name: 'Training Target Dummy A' },
    { type: 'env_barrel_crate', wx: 4, wy: 16, width: 64, height: 64, anchorX: 32, anchorY: 48, name: 'Training Target Dummy B' },

    // District 6: Northern Wilderness Gate (North-East: wy: -45..-26)
    { type: 'env_tree_meadow', wx: -8, wy: -30, width: 96, height: 128, anchorX: 48, anchorY: 112 },
    { type: 'env_tree_meadow', wx: 7, wy: -34, width: 96, height: 128, anchorX: 48, anchorY: 112 },
    { type: 'env_tree_meadow', wx: -6, wy: -40, width: 96, height: 128, anchorX: 48, anchorY: 112 },
    { type: 'env_tree_meadow', wx: 8, wy: -44, width: 96, height: 128, anchorX: 48, anchorY: 112 },
    { type: 'env_bush', wx: -4, wy: -28, width: 64, height: 64, anchorX: 32, anchorY: 48 },
    { type: 'env_bush', wx: 5, wy: -37, width: 64, height: 64, anchorX: 32, anchorY: 48 },
    { type: 'env_rock', wx: 3, wy: -32, width: 64, height: 64, anchorX: 32, anchorY: 48 },

    // Underground Sanctum Catacombs (South Deep: wy: 26..45)
    { type: 'env_dungeon_pillar', wx: -6, wy: 30, width: 64, height: 128, anchorX: 32, anchorY: 116 },
    { type: 'env_dungeon_pillar', wx: 6, wy: 30, width: 64, height: 128, anchorX: 32, anchorY: 116 },
    { type: 'env_torch_brazier', wx: -4, wy: 28, width: 64, height: 64, anchorX: 32, anchorY: 54, animated: true },
    { type: 'env_torch_brazier', wx: 4, wy: 28, width: 64, height: 64, anchorX: 32, anchorY: 54, animated: true },
    { type: 'env_crystal', wx: 0, wy: 42, width: 64, height: 96, anchorX: 32, anchorY: 82, name: 'Sanctum Core' }
  ];"""

content = re.sub(r'  // 2\.5D Isometric Environment Structures Library.*?\n  \];', new_env_structures, content, flags=re.DOTALL)

with open(r'D:\ai-studio\Zaggers\web\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated NPCs and envStructures successfully.")
