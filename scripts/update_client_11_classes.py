import re

with open(r'D:\ai-studio\Zaggers\web\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update spriteNames array to include all 11 hero sprites
old_sprite_names = "'hero_knight', 'hero_blackmage', 'hero_whitemage', 'hero_dragoon', \n    'hero_redmage', 'hero_thief', 'hero_monk',"
new_sprite_names = "'hero_knight', 'hero_blackmage', 'hero_whitemage', 'hero_dragoon', \n    'hero_redmage', 'hero_thief', 'hero_monk', 'hero_paladin', 'hero_sage', 'hero_bard', 'hero_alchemist',"

content = content.replace(old_sprite_names, new_sprite_names, 1)

# 2. Add Class Advancement UI inside #stat-window in index.html
stat_advancement_ui = """
      <div style="border-top: 1px solid #3d4a68; margin-top: 10px; padding-top: 8px;">
        <div style="font-size: 11px; font-weight: bold; color: #ffd54f; margin-bottom: 4px;">Class Advancement & Branching</div>
        <div id="job-branch-list" style="display: flex; flex-direction: column; gap: 4px; font-size: 11px;"></div>
      </div>
"""

content = content.replace('</div>\n    </div>\n  </div>\n\n  <!-- Shop Window Modal -->', stat_advancement_ui + '</div>\n    </div>\n  </div>\n\n  <!-- Shop Window Modal -->', 1)

# 3. Add JS function to check and render class advancement options
advancement_js = """
  function updateJobAdvancementUI() {
    const container = document.getElementById('job-branch-list');
    if (!container) return;
    container.innerHTML = '';

    const classesMap = getDbClasses();
    const currentClassId = selectedCreatorClassId;

    Object.values(classesMap).forEach(c => {
      if (c.id === currentClassId) return;
      const req = c.advancementRequirements;
      if (!req) return;

      let meetsAll = true;
      let reqText = [];
      for (const [statKey, reqVal] of Object.entries(req)) {
        const curVal = player[statKey] || 10;
        reqText.push(`${statKey.toUpperCase()}: ${curVal}/${reqVal}`);
        if (curVal < reqVal) meetsAll = false;
      }

      const div = document.createElement('div');
      div.style.cssText = 'background: #111824; border: 1px solid #2e3d58; border-radius: 4px; padding: 6px; display: flex; justify-content: space-between; align-items: center;';
      div.innerHTML = `
        <div>
          <strong style="color: ${meetsAll ? '#81c784' : '#b0bec5'};">${c.name}</strong><br>
          <small style="color: #94a3b8;">${reqText.join(' | ')}</small>
        </div>
        <button class="btn-icon" style="background: ${meetsAll ? '#2e7d32' : '#33415c'}; opacity: ${meetsAll ? '1' : '0.5'};" ${meetsAll ? '' : 'disabled'} onclick="promoteJobClass('${c.id}')">Promote</button>
      `;
      container.appendChild(div);
    });
  }

  function promoteJobClass(targetClassId) {
    const classesMap = getDbClasses();
    const c = classesMap[targetClassId];
    if (!c) return;

    player.class = c.sprite || 'hero_knight';
    player.sprite = c.sprite || 'hero_knight';
    selectedCreatorClassId = c.id;

    const pNameEl = document.getElementById('player-name');
    if (pNameEl) {
      const heroName = pNameEl.innerText.split(' [')[0] || 'Hero';
      pNameEl.innerText = `${heroName} [${c.name}]`;
    }

    updateHUD();
    updateJobAdvancementUI();

    const chatBox = document.getElementById('chat-messages');
    if (chatBox) {
      chatBox.innerHTML += `<div><span style="color: #ffd54f;">[System]:</span> 🌟 <strong>JOB ADVANCEMENT!</strong> You have promoted to <strong>${c.name}</strong>!</div>`;
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  }
"""

content = content.replace("function updateHUD() {", advancement_js + "\n  function updateHUD() {", 1)
content = content.replace("const hpPercent = (player.hp / player.maxHp) * 100;", "updateJobAdvancementUI();\n    const hpPercent = (player.hp / player.maxHp) * 100;", 1)

with open(r'D:\ai-studio\Zaggers\web\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated web/index.html with 11 class preloader and Stat Advancement UI successfully.")
