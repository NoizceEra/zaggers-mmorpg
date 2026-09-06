# ASSET PIPELINE & GRAPHICS TOOLS GUIDE

This guide details the asset production workflow for Zaggers MMORPG using **Aseprite**, **GIMP**, and **Krita**, along with rendering conventions in the 2.5D engine.

---

## 1. Sprite Sheet Conventions (Aseprite / Krita)
- **Cell Dimensions**: All character, NPC, and monster sprite sheets use fixed uniform frames ($64\times 64$ pixels).
- **Directional Ordering**:
  - Row 0 (Top): Down Facing (South)
  - Row 1: Left Facing (West)
  - Row 2: Right Facing (East)
  - Row 3 (Bottom): Up Facing (North)
- **Palettes**: 16-color or 32-color indexed color palettes matching classic 16-bit JRPG aesthetics.

---

## 2. Isometric Tile Tiling (GIMP / Photoshop)
- **Diamond Grid Ratio**: Standard isometric $2:1$ projection ratio ($64\times 32$ pixels per tile floor diamond).
- **Sub-Pixel Seam Prevention**:
  When rendering isometric tiles on HTML5 Canvas:
  ```javascript
  const tw = TILE_W * cameraZoom + 0.5;
  const th = TILE_H * cameraZoom + 0.5;
  ctx.drawImage(tileImg, isoX - tw/2, isoY, tw, th);
  ```
  Adding `+ 0.5` prevents anti-aliasing seam gaps when zooming or panning.

---

## 3. Depth Sorting Algorithm
Entities and environmental props are sorted every frame before rendering:
```javascript
drawList.sort((a, b) => (a.isoY - b.isoY) || (a.isoX - b.isoX));
```
Sorting primarily on `isoY` (screen Y coordinate) guarantees correct visual overlap across all camera rotation angles ($0^\circ, 90^\circ, 180^\circ, 270^\circ$).

---

## 4. Vercel Production Build Setup
- Static files served directly from repository root or `web/` directory.
- `vercel.json` rewrite routing:
  ```json
  {
    "rewrites": [
      { "source": "/assets/(.*)", "destination": "/web/assets/$1" },
      { "source": "/editor", "destination": "/web/editor.html" },
      { "source": "/db_editor", "destination": "/web/db_editor.html" }
    ]
  }
  ```
