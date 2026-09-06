import re

with open(r'D:\ai-studio\Zaggers\web\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Inject Player Death Modal HTML right after <div id="game-container">
death_modal_html = """
  <!-- Player Death & Respawn Modal Overlay -->
  <div id="player-death-modal" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(10, 5, 5, 0.92); backdrop-filter: blur(6px); z-index: 600; display: none; flex-direction: column; align-items: center; justify-content: center; color: #fff; pointer-events: auto;">
    <div style="background: #181015; border: 2px solid #ff5252; border-radius: 8px; padding: 24px; max-width: 440px; text-align: center; box-shadow: 0 10px 30px rgba(255,82,82,0.3);">
      <h2 style="font-size: 22px; color: #ff5252; letter-spacing: 2px; text-shadow: 0 2px 8px #ff5252; margin-bottom: 8px;">YOU HAVE FALLEN IN BATTLE</h2>
      <p style="font-size: 13px; color: #cbd5e1; margin-bottom: 18px; line-height: 1.4;">Your physical form was overcome by the wild forces of Midgard. Select your resurrection path to continue your adventure.</p>
      
      <div style="display: flex; flex-direction: column; gap: 10px;">
        <button onclick="respawnAtKafra()" style="background: linear-gradient(180deg, #1e88e5 0%, #1565c0 100%); border: 1px solid #90caf9; color: #fff; padding: 10px 18px; font-weight: bold; border-radius: 4px; cursor: pointer; font-size: 13px; box-shadow: 0 4px 10px rgba(30,136,229,0.4);">💾 Respawn at Aethelgard Kafra Save Crystal (Free)</button>
        <button onclick="reviveOnSpot()" style="background: linear-gradient(180deg, #d97706 0%, #b45309 100%); border: 1px solid #ffe082; color: #fff; padding: 10px 18px; font-weight: bold; border-radius: 4px; cursor: pointer; font-size: 13px; box-shadow: 0 4px 10px rgba(217,119,6,0.4);">✨ Revive On The Spot (100 z)</button>
      </div>
    </div>
  </div>
"""

content = content.replace('<div id="game-container">', '<div id="game-container">\n' + death_modal_html, 1)

# 2. Refactor HERO_CLASSES to source dynamically from db.classes (Single Source of Truth)
db_class_js = """
  // ==========================================
  // Single Source of Truth DB Class Integration
  // ==========================================
  function getDbClasses() {
    let dbData = null;
    try {
      const stored = localStorage.getItem('zaggers_db');
      if (stored) dbData = JSON.parse(stored);
    } catch(e) {}
    if (!dbData || !dbData.classes) {
      return {
        vanguard: { id: 'vanguard', name: 'Vanguard Titan', sprite: 'hero_knight', baseStats: { str: 14, agi: 10, vit: 16, int: 6, dex: 12, luk: 8 }, hpGrowth: 18, spGrowth: 4, primaryWeapon: 'Sword & Shield', description: 'Stalwart frontline defender with heavy armor.' },
        spellweaver: { id: 'spellweaver', name: 'Spellweaver', sprite: 'hero_blackmage', baseStats: { str: 5, agi: 8, vit: 8, int: 18, dex: 14, luk: 10 }, hpGrowth: 10, spGrowth: 12, primaryWeapon: 'Archmage Staff', description: 'Master of arcane storm and flame.' },
        shadowblade: { id: 'shadowblade', name: 'Shadowblade', sprite: 'hero_thief', baseStats: { str: 12, agi: 18, vit: 8, int: 6, dex: 14, luk: 12 }, hpGrowth: 12, spGrowth: 5, primaryWeapon: 'Dual Daggers', description: 'Lethal rogue specializing in rapid critical hits.' },
        cleric: { id: 'cleric', name: 'Cleric Priest', sprite: 'hero_whitemage', baseStats: { str: 8, agi: 6, vit: 12, int: 15, dex: 10, luk: 12 }, hpGrowth: 13, spGrowth: 10, primaryWeapon: 'Holy Mace', description: 'Devout guardian granting holy protection and healing.' },
        ranger: { id: 'ranger', name: 'Ranger Marksman', sprite: 'hero_redmage', baseStats: { str: 10, agi: 14, vit: 10, int: 8, dex: 18, luk: 10 }, hpGrowth: 14, spGrowth: 6, primaryWeapon: 'Composite Bow', description: 'Precision sniper firing deadly arrows.' }
      };
    }
    return dbData.classes;
  }

  let selectedCreatorClassId = 'vanguard';
  let creatorPreviewDir = 0;
  let creatorPreviewFrame = 0;
  let creatorPreviewAnimTimer = 0;
  let currentDistrictName = 'Aethelgard Grand Plaza';
  let isPlayerDead = false;

  function renderCreatorClassCards() {
    const container = document.getElementById('creator-class-cards');
    if (!container) return;
    container.innerHTML = '';
    const classesMap = getDbClasses();
    Object.values(classesMap).forEach(c => {
      const card = document.createElement('div');
      card.className = 'creator-class-card' + (c.id === selectedCreatorClassId ? ' active' : '');
      card.onclick = () => selectCreatorClass(c.id);
      card.innerHTML = `<div><strong>${c.name}</strong><br><small style="color: #94a3b8;">${c.primaryWeapon || c.weapon || 'Weapon'}</small></div><span style="color: #ffd54f;">★</span>`;
      container.appendChild(card);
    });
    updateCreatorClassDetails();
  }

  function selectCreatorClass(classId) {
    selectedCreatorClassId = classId;
    renderCreatorClassCards();
  }

  function rotateCreatorPreview(dir) {
    creatorPreviewDir = (creatorPreviewDir + dir + 4) % 4;
  }

  function updateCreatorClassDetails() {
    const classesMap = getDbClasses();
    const c = classesMap[selectedCreatorClassId] || Object.values(classesMap)[0];
    if (!c) return;
    const titleEl = document.getElementById('creator-class-title');
    if (titleEl) titleEl.innerText = c.name;

    const stats = c.baseStats || c.stats || { str: 10, agi: 10, vit: 10, int: 10, dex: 10, luk: 10 };
    const statsEl = document.getElementById('creator-stats-list');
    if (statsEl) {
      statsEl.innerHTML = `
        <div style="display:flex; justify-content:space-between;"><span>STR (Attack)</span><strong style="color:#ff8a80;">${stats.str}</strong></div>
        <div style="display:flex; justify-content:space-between;"><span>AGI (Speed/Flee)</span><strong style="color:#b9f6ca;">${stats.agi}</strong></div>
        <div style="display:flex; justify-content:space-between;"><span>VIT (Max HP)</span><strong style="color:#ffd180;">${stats.vit}</strong></div>
        <div style="display:flex; justify-content:space-between;"><span>INT (MATK/SP)</span><strong style="color:#80d8ff;">${stats.int}</strong></div>
        <div style="display:flex; justify-content:space-between;"><span>DEX (Hit Speed)</span><strong style="color:#ea80fc;">${stats.dex}</strong></div>
        <div style="display:flex; justify-content:space-between;"><span>LUK (Critical)</span><strong style="color:#ffff8d;">${stats.luk}</strong></div>
        <div style="border-top:1px solid #2e3d58; margin-top:4px; padding-top:4px; display:flex; justify-space-between;">
          <span>HP Growth: <strong style="color:#ff5252;">${c.hpGrowth || 14}</strong></span>
          <span>SP Growth: <strong style="color:#42a5f5;">${c.spGrowth || 6}</strong></span>
        </div>
      `;
    }

    const loreEl = document.getElementById('creator-lore-text');
    if (loreEl) loreEl.innerText = c.description || c.lore || 'Hero class in Midgard.';
  }

  function updateCreatorPreviewCanvas() {
    const pCanvas = document.getElementById('creator-preview-canvas');
    if (!pCanvas) return;
    const pCtx = pCanvas.getContext('2d');
    pCtx.imageSmoothingEnabled = false;
    pCtx.clearRect(0, 0, pCanvas.width, pCanvas.height);

    const classesMap = getDbClasses();
    const c = classesMap[selectedCreatorClassId] || Object.values(classesMap)[0];
    if (!c) return;
    const spriteKey = c.sprite || 'hero_knight';
    const img = sprites[spriteKey];

    creatorPreviewAnimTimer++;
    if (creatorPreviewAnimTimer >= 10) {
      creatorPreviewAnimTimer = 0;
      creatorPreviewFrame = (creatorPreviewFrame + 1) % 4;
    }

    if (img && img.complete && img.naturalWidth > 0) {
      pCtx.drawImage(img, creatorPreviewFrame * 64, creatorPreviewDir * 64, 64, 64, 16, 16, 128, 128);
    }
  }

  function confirmCharacterCreation() {
    const input = document.getElementById('creator-name-input');
    const heroName = input ? (input.value.trim() || 'Hero') : 'Hero';
    const classesMap = getDbClasses();
    const c = classesMap[selectedCreatorClassId] || Object.values(classesMap)[0];

    const stats = c.baseStats || c.stats || { str: 10, agi: 10, vit: 10, int: 10, dex: 10, luk: 10 };
    const baseHp = 100 + stats.vit * 15;
    const baseSp = 30 + stats.int * 8;

    player.class = c.sprite || 'hero_knight';
    player.sprite = c.sprite || 'hero_knight';
    player.str = stats.str;
    player.agi = stats.agi;
    player.vit = stats.vit;
    player.int = stats.int;
    player.dex = stats.dex;
    player.luk = stats.luk;
    player.maxHp = baseHp;
    player.hp = baseHp;
    player.maxSp = baseSp;
    player.sp = baseSp;

    const pNameEl = document.getElementById('player-name');
    if (pNameEl) pNameEl.innerText = `${heroName} [${c.name}]`;

    updateHUD();

    const modal = document.getElementById('character-creator-modal');
    if (modal) modal.style.display = 'none';

    const chatBox = document.getElementById('chat-messages');
    if (chatBox) {
      chatBox.innerHTML += `<div><span style="color: #ffd54f;">[System]:</span> Welcome to Aethelgard Master Town, ${heroName}! Class set to <strong>${c.name}</strong>.</div>`;
      chatBox.scrollTop = chatBox.scrollHeight;
    }
    showDistrictBanner("Entering Aethelgard Grand Plaza");
  }

  // Death & Respawn System
  function triggerPlayerDeath() {
    if (isPlayerDead) return;
    isPlayerDead = true;
    player.hp = 0;
    updateHUD();

    const modal = document.getElementById('player-death-modal');
    if (modal) modal.style.display = 'flex';

    const chatBox = document.getElementById('chat-messages');
    if (chatBox) {
      chatBox.innerHTML += `<div><span style="color: #ff5252;">[System]:</span> You have fallen in battle! Choose a resurrection option.</div>`;
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  }

  function respawnAtKafra() {
    isPlayerDead = false;
    player.hp = player.maxHp;
    player.sp = player.maxSp;
    updateHUD();

    const modal = document.getElementById('player-death-modal');
    if (modal) modal.style.display = 'none';

    // Teleport back to Aethelgard Town Center (0, 0)
    loadZoneMap('aethelgard', { wx: 0, wy: 0 });
  }

  function reviveOnSpot() {
    if (player.zeny >= 100) {
      player.zeny -= 100;
      isPlayerDead = false;
      player.hp = player.maxHp;
      player.sp = player.maxSp;
      updateHUD();

      const modal = document.getElementById('player-death-modal');
      if (modal) modal.style.display = 'none';

      const chatBox = document.getElementById('chat-messages');
      if (chatBox) {
        chatBox.innerHTML += `<div><span style="color: #ffd54f;">[System]:</span> Revived on the spot for 100 zeny!</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
      }
    } else {
      alert("Insufficient Zeny! Respawning at Kafra Save Crystal.");
      respawnAtKafra();
    }
  }
"""

content = re.sub(r'  // ==========================================\n  // Character Creation & Class Selection System.*?\n  function showDistrictBanner', db_class_js + "\n  function showDistrictBanner", content, flags=re.DOTALL)

with open(r'D:\ai-studio\Zaggers\web\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated Single Source of Truth DB Class and Player Death/Respawn System successfully.")
