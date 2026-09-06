import re

with open(r'D:\ai-studio\Zaggers\web\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Inject CSS for Character Creator & District Banner
creator_css = """
    /* District Banner Overlay */
    #district-banner { position: absolute; top: 55px; left: 50%; transform: translateX(-50%); background: rgba(16, 22, 34, 0.94); border: 2px solid #ffd54f; border-radius: 6px; padding: 6px 22px; font-size: 14px; font-weight: bold; color: #ffe082; text-shadow: 0 2px 4px #000; opacity: 0; transition: opacity 0.4s; pointer-events: none; z-index: 90; box-shadow: 0 4px 15px rgba(0,0,0,0.6); }
    
    /* Character Creator Screen Overlay */
    #character-creator-modal { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at center, #1c2638 0%, #090c14 100%); z-index: 500; display: flex; flex-direction: column; padding: 18px; color: #fff; pointer-events: auto; }
    .creator-class-card { background: #131b28; border: 1px solid #33435e; border-radius: 6px; padding: 8px 12px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; transition: all 0.2s; }
    .creator-class-card:hover { background: #1c283c; border-color: #ffd54f; }
    .creator-class-card.active { background: #23324c; border: 2px solid #ffd54f; box-shadow: 0 0 10px rgba(255,213,79,0.3); }
"""

content = content.replace("  </style>", creator_css + "\n  </style>", 1)

# 2. Inject HTML for District Banner and Character Creator Modal right after <div id="game-container">
creator_html = """
  <!-- Floating District Banner Overlay -->
  <div id="district-banner">Entering Aethelgard Grand Plaza</div>

  <!-- Character Creation & Class Selector Modal -->
  <div id="character-creator-modal">
    <div style="text-align: center; margin-bottom: 10px;">
      <h1 style="font-size: 22px; color: #ffd54f; letter-spacing: 2px; text-shadow: 0 2px 8px rgba(255,213,79,0.5);">ZAGGERS MMORPG</h1>
      <p style="font-size: 12px; color: #94a3b8;">Choose your Hero Class & Enter the Realm of Aethelgard</p>
    </div>

    <div style="flex: 1; display: flex; gap: 14px; min-height: 0;">
      <!-- Left Column: Name & Class Cards -->
      <div style="width: 260px; background: rgba(18, 25, 38, 0.95); border: 1px solid #3d4d6c; border-radius: 8px; padding: 12px; display: flex; flex-direction: column; gap: 8px;">
        <div>
          <label style="font-size: 11px; font-weight: bold; color: #ffd54f; text-transform: uppercase;">Hero Name</label>
          <input type="text" id="creator-name-input" value="AethelHero" style="width: 100%; background: #0c111a; border: 1px solid #4a5c82; color: #fff; padding: 6px 10px; border-radius: 4px; font-size: 13px; outline: none; margin-top: 4px;" />
        </div>
        
        <label style="font-size: 11px; font-weight: bold; color: #ffd54f; text-transform: uppercase; margin-top: 2px;">Select Class</label>
        <div id="creator-class-cards" style="flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 6px; padding-right: 4px;"></div>
      </div>

      <!-- Center Column: 2.5D Animated Sprite Preview Canvas -->
      <div style="flex: 1; background: rgba(12, 16, 26, 0.95); border: 2px solid #4a5c84; border-radius: 8px; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; box-shadow: inset 0 0 30px rgba(0,0,0,0.8);">
        <div style="position: absolute; top: 12px; font-size: 15px; font-weight: bold; color: #81d4fa;" id="creator-class-title">Vanguard Titan</div>
        <canvas id="creator-preview-canvas" width="160" height="160" style="image-rendering: pixelated; filter: drop-shadow(0 10px 15px rgba(0,0,0,0.8));"></canvas>
        <div style="position: absolute; bottom: 12px; display: flex; gap: 8px;">
          <button class="btn-icon" onclick="rotateCreatorPreview(-1)">Rotate Left ↺</button>
          <button class="btn-icon" onclick="rotateCreatorPreview(1)">Rotate Right ↻</button>
        </div>
      </div>

      <!-- Right Column: Stats & Lore Breakdown -->
      <div style="width: 280px; background: rgba(18, 25, 38, 0.95); border: 1px solid #3d4d6c; border-radius: 8px; padding: 12px; display: flex; flex-direction: column; justify-content: space-between;">
        <div>
          <div style="font-size: 12px; font-weight: bold; color: #ffe082; margin-bottom: 8px; border-bottom: 1px solid #2e3d58; padding-bottom: 4px;">Class Attributes</div>
          <div id="creator-stats-list" style="display: flex; flex-direction: column; gap: 5px; font-size: 11px;"></div>
        </div>
        <div>
          <div style="font-size: 12px; font-weight: bold; color: #81c784; margin-bottom: 4px;">Class Lore</div>
          <div id="creator-lore-text" style="font-size: 11px; color: #cbd5e1; line-height: 1.35; background: #0e1420; border: 1px solid #28364f; border-radius: 4px; padding: 6px;"></div>
        </div>
      </div>
    </div>

    <div style="margin-top: 10px; text-align: center;">
      <button onclick="confirmCharacterCreation()" style="background: linear-gradient(180deg, #2e7d32 0%, #1b5e20 100%); border: 2px solid #81c784; color: #fff; padding: 8px 28px; font-size: 14px; font-weight: bold; border-radius: 6px; cursor: pointer; box-shadow: 0 4px 15px rgba(46,125,50,0.6); text-transform: uppercase; letter-spacing: 1px;">⚔️ Enter Aethelgard Master Town</button>
    </div>
  </div>
"""

content = content.replace('<div id="game-container">', '<div id="game-container">\n' + creator_html, 1)

with open(r'D:\ai-studio\Zaggers\web\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Injected HTML & CSS successfully.")
