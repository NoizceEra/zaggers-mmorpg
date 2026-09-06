import re

with open(r'D:\ai-studio\Zaggers\web\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

creator_js = """
  // ==========================================
  // Character Creation & Class Selection System
  // ==========================================
  const HERO_CLASSES = {
    vanguard: {
      id: 'vanguard',
      name: 'Vanguard Titan',
      sprite: 'hero_knight',
      stats: { str: 14, agi: 10, vit: 16, int: 6, dex: 12, luk: 8 },
      hp: 180, sp: 50,
      weapon: 'Sword & Shield',
      lore: 'Stalwart frontline defender. High VIT & STR allows Vanguard tanks to absorb heavy enemy assaults while protecting allies.'
    },
    spellweaver: {
      id: 'spellweaver',
      name: 'Spellweaver',
      sprite: 'hero_blackmage',
      stats: { str: 5, agi: 8, vit: 8, int: 18, dex: 14, luk: 10 },
      hp: 110, sp: 140,
      weapon: 'Archmage Staff',
      lore: 'Wielder of elemental tempests. High INT enables destructive AoE spells and massive magic damage.'
    },
    shadowblade: {
      id: 'shadowblade',
      name: 'Shadowblade',
      sprite: 'hero_thief',
      stats: { str: 12, agi: 18, vit: 8, int: 6, dex: 14, luk: 12 },
      hp: 130, sp: 60,
      weapon: 'Dual Daggers',
      lore: 'Agile killer in the night. High AGI & LUK delivers blindingly fast attack speeds and critical strikes.'
    },
    cleric: {
      id: 'cleric',
      name: 'Cleric Priest',
      sprite: 'hero_whitemage',
      stats: { str: 8, agi: 6, vit: 12, int: 15, dex: 10, luk: 12 },
      hp: 140, sp: 120,
      weapon: 'Holy Mace',
      lore: 'Divine sanctuary healer. High INT & VIT provides party restoration, protective barriers, and holy holy light.'
    },
    ranger: {
      id: 'ranger',
      name: 'Ranger Marksman',
      sprite: 'hero_redmage',
      stats: { str: 10, agi: 14, vit: 10, int: 8, dex: 18, luk: 10 },
      hp: 140, sp: 70,
      weapon: 'Composite Bow',
      lore: 'Precision long-range sniper. High DEX & AGI ensures pinpoint accuracy and lethal physical shots.'
    }
  };

  let selectedCreatorClassId = 'vanguard';
  let creatorPreviewDir = 0;
  let creatorPreviewFrame = 0;
  let creatorPreviewAnimTimer = 0;
  let currentDistrictName = 'Aethelgard Grand Plaza';

  function renderCreatorClassCards() {
    const container = document.getElementById('creator-class-cards');
    if (!container) return;
    container.innerHTML = '';
    Object.values(HERO_CLASSES).forEach(c => {
      const card = document.createElement('div');
      card.className = 'creator-class-card' + (c.id === selectedCreatorClassId ? ' active' : '');
      card.onclick = () => selectCreatorClass(c.id);
      card.innerHTML = `<div><strong>${c.name}</strong><br><small style="color: #94a3b8;">${c.weapon}</small></div><span style="color: #ffd54f;">★</span>`;
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
    const c = HERO_CLASSES[selectedCreatorClassId];
    if (!c) return;
    const titleEl = document.getElementById('creator-class-title');
    if (titleEl) titleEl.innerText = c.name;

    const statsEl = document.getElementById('creator-stats-list');
    if (statsEl) {
      statsEl.innerHTML = `
        <div style="display:flex; justify-content:space-between;"><span>STR (Attack)</span><strong style="color:#ff8a80;">${c.stats.str}</strong></div>
        <div style="display:flex; justify-content:space-between;"><span>AGI (Speed/Flee)</span><strong style="color:#b9f6ca;">${c.stats.agi}</strong></div>
        <div style="display:flex; justify-content:space-between;"><span>VIT (Max HP)</span><strong style="color:#ffd180;">${c.stats.vit}</strong></div>
        <div style="display:flex; justify-content:space-between;"><span>INT (MATK/SP)</span><strong style="color:#80d8ff;">${c.stats.int}</strong></div>
        <div style="display:flex; justify-content:space-between;"><span>DEX (Hit Speed)</span><strong style="color:#ea80fc;">${c.stats.dex}</strong></div>
        <div style="display:flex; justify-content:space-between;"><span>LUK (Critical)</span><strong style="color:#ffff8d;">${c.stats.luk}</strong></div>
        <div style="border-top:1px solid #2e3d58; margin-top:4px; padding-top:4px; display:flex; justify-space-between;">
          <span>Base HP: <strong style="color:#ff5252;">${c.hp}</strong></span>
          <span>Base SP: <strong style="color:#42a5f5;">${c.sp}</strong></span>
        </div>
      `;
    }

    const loreEl = document.getElementById('creator-lore-text');
    if (loreEl) loreEl.innerText = c.lore;
  }

  function updateCreatorPreviewCanvas() {
    const pCanvas = document.getElementById('creator-preview-canvas');
    if (!pCanvas) return;
    const pCtx = pCanvas.getContext('2d');
    pCtx.imageSmoothingEnabled = false;
    pCtx.clearRect(0, 0, pCanvas.width, pCanvas.height);

    const c = HERO_CLASSES[selectedCreatorClassId];
    if (!c) return;
    const img = sprites[c.sprite];

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
    const c = HERO_CLASSES[selectedCreatorClassId];

    player.sprite = c.sprite;
    player.str = c.stats.str;
    player.agi = c.stats.agi;
    player.vit = c.stats.vit;
    player.int = c.stats.int;
    player.dex = c.stats.dex;
    player.luk = c.stats.luk;
    player.maxHp = c.hp;
    player.hp = c.hp;
    player.maxSp = c.sp;
    player.sp = c.sp;

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

  function showDistrictBanner(name) {
    currentDistrictName = name;
    const b = document.getElementById('district-banner');
    if (b) {
      b.innerText = name;
      b.style.opacity = '1';
      setTimeout(() => { b.style.opacity = '0'; }, 3000);
    }
    const zoneTitle = document.getElementById('minimap-zone-title');
    if (zoneTitle) zoneTitle.innerText = name;
  }

  function checkDistrictTransition() {
    let newDistrict = 'Aethelgard Grand Plaza';
    if (player.wy < -25) {
      newDistrict = 'Whispering Meadows Wilderness';
    } else if (player.wy > 25) {
      newDistrict = 'Sunken Sanctum Catacombs';
    } else if (player.wx < -8 && Math.abs(player.wy) <= 12) {
      newDistrict = 'Smithy Row Forge District';
    } else if (player.wy < -8 && Math.abs(player.wx) <= 12) {
      newDistrict = 'High Temple Sacred Plaza';
    } else if (player.wx > 8 && Math.abs(player.wy) <= 12) {
      newDistrict = 'Market District & Bazaars';
    } else if (player.wy > 8 && Math.abs(player.wx) <= 12) {
      newDistrict = 'Adventurer Guild & Training Grounds';
    }

    if (newDistrict !== currentDistrictName) {
      showDistrictBanner(newDistrict);
    }
  }
"""

# Inject creator_js into script before window.addEventListener('DOMContentLoaded'
content = content.replace("window.addEventListener('DOMContentLoaded', () => {", creator_js + "\n  window.addEventListener('DOMContentLoaded', () => {", 1)

# In DOMContentLoaded, call renderCreatorClassCards()
dom_content = """window.addEventListener('DOMContentLoaded', () => {
    renderCreatorClassCards();
    setInterval(updateCreatorPreviewCanvas, 50);"""

content = content.replace("window.addEventListener('DOMContentLoaded', () => {", dom_content, 1)

# In render loop (update step), call checkDistrictTransition()
content = content.replace("player.wx += (player.targetWx - player.wx) * player.speed;", "player.wx += (player.targetWx - player.wx) * player.speed;\n    checkDistrictTransition();", 1)

with open(r'D:\ai-studio\Zaggers\web\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Injected Character Creator JS & District transition logic successfully.")
