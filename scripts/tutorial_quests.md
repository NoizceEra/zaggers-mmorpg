# Tutorial Quests — Godot Mirror (Starter Arc)

Parity mirror of `web/tutorial/StarterQuests.js` for the Godot client.
Same 3-quest arc, same IDs/thresholds, same rewards. Web is authoritative;
this doc is the implementation contract for the Godot HUD pass.

## Quest arc (identical to web)

| # | Quest | Objective | Complete when | Reward |
|---|-------|-----------|---------------|--------|
| 1 | First Papers | Talk to the Kestrel Consignment Steward (Kafra) in Aethelgard Grand Plaza | NPC dialog opened with `id == "kafra_kestrel"` or `sprite == "npc_kafra"` (see `web/maps/aethelgard.json` wx −17, wy −1) | Quest brief for Q2 |
| 2 | Downs Patrol | Defeat **3 Bellflower Glooplings** (Whispering Meadows / Gatewatch fields) | Kill credit where `sprite == "gloopling_bellflower_ff"`, `id == "gloopling_bellflower"`, or name `Bellflower Gloopling` (map ids `meadow_gloopling_*` in `web/maps/meadows.json`) | **1× `bellflower_shortsword`** (DB item, `slot: weapon`, `reqLevel: 1`) granted to inventory |
| 3 | Oath of the Bell | Equip the Bellflower Shortsword **and** reach **Base Lv 5** | `player.equipment.weapon == "bellflower_shortsword"` **and** `player.level >= 5` | Lv5 induction ceremony + **3× `red_potion`** |

Elder/Ordwin hunt (`hasQuest`/`questCompleted` in `web/index.html`) is a
separate optional veteran quest — untouched by this arc.

## Godot HUD mapping (scripts/hud.gd — ZaggersHUD)

All quest text goes through the existing HUD labels; no new scenes required.

- **Briefs / completion banners:** append BBCode to the ChatBox
  `RichTextLabel` (`_chat_box`), same strings as `StarterQuests.js`
  `briefQ1/briefQ2/briefQ3` and completion messages. Use the web color
  equivalents (`#ffe082` briefs, `#81c784` completions, `#ffd54f` ceremony).
- **Kill counter (Q2):** update a HUD label `QuestTracker` (create under
  `StatusPanel` if absent) with `🌸 Gloopling pacified (n/3).`
- **Q3 ceremony:** show a center-screen `Label` (`OathBanner`) with
  `🎔 OATH SWORN — LV 5!` for ~4s, then append the ceremony text to `_chat_box`.
- **Level display:** read Base Lv from the existing level label backing
  (`player.level`); Q3 checks `>= 5`.
- **Persistence:** mirror the web `localStorage` flag
  `zaggers_starter_quests_v1` with a `ConfigFile` (`user://starter_quests.cfg`,
  section `quests`: `started,q1,kills,q2,q3,done`) so progress survives scene
  reloads on both clients.

## Hook points (Godot equivalents of the web wrappers)

1. `openNpcDialog(npc)` → Godot NPC interact signal: if quest data matches
   Kafra (step 1), mark Q1 and push the Q2 brief to `_chat_box`.
2. `grantKillRewards(m)` → Godot combat kill callback: if Q1 done, Q2 open,
   and the victim matches the Gloopling triple (sprite/id/name), increment
   `kills`; at 3, grant `bellflower_shortsword` to inventory and brief Q3.
3. `equipItem(id)` + level-up callback → after any equip or level change,
   evaluate Q3 (`weapon == bellflower_shortsword && level >= 5`); on success
   grant `3× red_potion`, show `OathBanner`, append ceremony text.

## web/index.html integration (DO NOT overwrite index.html)

Apply by hand — two insertions only:

1. Script tag (before the main inline `<script>`, e.g. next to other
   `<script src=...>` includes, or just before `</body>` — must load before
   the player can finish character creation):
   ```html
   <script src="tutorial/StarterQuests.js"></script>
   ```
2. One call at the end of `confirmCharacterCreation()`, after the existing
   `showOnboardingHint();` line:
   ```js
   if (typeof StarterQuests !== 'undefined' && StarterQuests.start) StarterQuests.start();
   ```

`StarterQuests.js` self-installs its `openNpcDialog` / `grantKillRewards` /
`equipItem` / `grantXp` wrappers on `DOMContentLoaded` (with retries), so no
other index.html edits are needed. Existing `onboarding-hint`,
`npc-dialog-window`, `hasQuest`/`questCompleted` flows are untouched.

## Verification

- `python tools/check_db_drift.py` → `7/7 sections PASS` (covers
  `npc_militia.png` / `npc_smuggler.png` in `sprite-files-exist`).
- `node --check web/tutorial/StarterQuests.js` → syntax OK.
- In-browser: fresh profile → create character → Starter brief 1/3 in chat →
  talk to Kafra → Q2 brief → kill 3 Bellflower Glooplings → sword issued →
  equip + Lv5 → ceremony + 3× Red Potion; reload mid-arc → re-brief resumes.
