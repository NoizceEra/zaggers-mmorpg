"""
generate_wall_door_assets.py

Collision/Walls/Doors pass (vault/COLLISION_WALLS_DOORS_REPORT.md).

Follows the exact conventions of generate_env_expansion.py's "wall" prop
archetype (flat isometric box + shadow, saved to both asset dirs) so the new
props sit visually alongside env_palisade_wall / env_briar_wall / env_vault_door.

New assets:
  - env_wall_curtain.png  (96x128, anchor 48,116)  - stone town-wall segment
  - env_wall_corner.png   (96x128, anchor 48,116)  - stone wall corner piece
  - env_gatehouse.png     (160x192, anchor 80,178) - town gatehouse w/ arch
  - env_door.png          (128x96, anchor per-frame 32,80) - 2-frame sheet:
        frame 0 (0..64px)   = closed door
        frame 1 (64..128px) = open door (swung frame, passable)
"""

import os
from PIL import Image, ImageDraw

ROOT = r"D:\ai-studio\Zaggers\.claude\worktrees\agent-a3b12d2ecaed5d7b9"
TARGET_DIRS = [
    os.path.join(ROOT, "assets", "tiles_ff"),
    os.path.join(ROOT, "web", "assets", "tiles_ff"),
]


def save_asset(img, name):
    for d in TARGET_DIRS:
        os.makedirs(d, exist_ok=True)
        img.save(os.path.join(d, name), "PNG")
        print(f"Saved: {os.path.join(d, name)} ({img.size[0]}x{img.size[1]})")


def hx(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)


def new_canvas(w, h):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)


def draw_shadow(draw, center, rx, ry, alpha=100):
    cx, cy = center
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(10, 15, 25, alpha))


def create_wall_curtain():
    """Stone curtain-wall segment - matches env_palisade_wall/env_briar_wall
    sizing (96x128, anchor 48,116) so it drops into the same map-authoring
    convention (chain several side-by-side to form a long perimeter)."""
    w, h, anchor = 96, 128, (48, 116)
    c_main, c_dark, c_accent = hx("#8a8a90"), hx("#45454c"), hx("#c9c2a0")
    img, draw = new_canvas(w, h)
    ax, ay = anchor
    draw_shadow(draw, (ax, ay), int(w * 0.44), int(h * 0.07), 110)

    # Main stone wall body (flat isometric box, like prop_wall)
    draw.polygon([(ax - w * 0.46, ay), (ax + w * 0.46, ay), (ax + w * 0.46, ay - h * 0.72),
                  (ax - w * 0.46, ay - h * 0.72)], fill=c_main, outline=c_dark)

    # Coursed stone-block lines (horizontal courses + staggered verticals)
    course_h = (h * 0.72) / 5
    for row in range(5):
        y = ay - row * course_h
        draw.line([(ax - w * 0.46, y), (ax + w * 0.46, y)], fill=c_dark, width=1)
        offset = (w * 0.15) if row % 2 == 0 else 0
        for bx in range(-2, 3):
            x = ax + bx * (w * 0.23) + offset
            draw.line([(x, y), (x, y - course_h)], fill=c_dark, width=1)

    # Crenellated battlement top
    merlon_w = w * 0.16
    x = ax - w * 0.46
    while x < ax + w * 0.46:
        draw.polygon([(x, ay - h * 0.72), (x + merlon_w * 0.7, ay - h * 0.72),
                      (x + merlon_w * 0.7, ay - h * 0.86), (x, ay - h * 0.86)],
                     fill=c_accent, outline=c_dark)
        x += merlon_w * 1.4

    save_asset(img, "env_wall_curtain.png")


def create_wall_corner():
    """Stone wall corner piece - two faces meeting at a vertical edge, same
    footprint size as env_wall_curtain so it can be dropped at perimeter
    turns without a visible seam mismatch."""
    w, h, anchor = 96, 128, (48, 116)
    c_left, c_right, c_dark, c_accent = hx("#767680"), hx("#9a9aa4"), hx("#3c3c44"), hx("#c9c2a0")
    img, draw = new_canvas(w, h)
    ax, ay = anchor
    draw_shadow(draw, (ax, ay), int(w * 0.44), int(h * 0.07), 110)

    top = ay - h * 0.72
    # Left face (darker) and right face (lighter) meeting at the corner edge
    draw.polygon([(ax - w * 0.46, ay), (ax, ay + h * 0.05), (ax, top + h * 0.05), (ax - w * 0.46, top)],
                 fill=c_left, outline=c_dark)
    draw.polygon([(ax, ay + h * 0.05), (ax + w * 0.46, ay), (ax + w * 0.46, top), (ax, top + h * 0.05)],
                 fill=c_right, outline=c_dark)

    # Coursed block lines on both faces
    course_h = (h * 0.72) / 5
    for row in range(5):
        yL = ay - row * course_h
        yR = ay - row * course_h
        draw.line([(ax - w * 0.46, yL - row * 0.002), (ax, yL + h * 0.05 - row * 0.002)], fill=c_dark, width=1)
        draw.line([(ax, yR + h * 0.05), (ax + w * 0.46, yR)], fill=c_dark, width=1)

    # Corner cap merlon
    draw.polygon([(ax - w * 0.14, top), (ax + w * 0.14, top),
                  (ax + w * 0.14, top - h * 0.14), (ax - w * 0.14, top - h * 0.14)],
                 fill=c_accent, outline=c_dark)

    save_asset(img, "env_wall_corner.png")


def create_gatehouse():
    """Town gatehouse - a wide stone structure with a dark walkable archway
    cut through the middle (the archway itself is the passable gap the map
    author places between two wall runs; the gatehouse sprite's own footprint
    is still solid on the sides)."""
    w, h, anchor = 160, 192, (80, 178)
    c_main, c_dark, c_accent, c_roof = hx("#8a8a90"), hx("#45454c"), hx("#d8a840"), hx("#5a3c28")
    img, draw = new_canvas(w, h)
    ax, ay = anchor
    draw_shadow(draw, (ax, ay), int(w * 0.42), int(h * 0.05), 120)

    body_top = ay - h * 0.62
    # Main stone block spanning the full width
    draw.polygon([(ax - w * 0.46, ay), (ax + w * 0.46, ay),
                  (ax + w * 0.46, body_top), (ax - w * 0.46, body_top)],
                 fill=c_main, outline=c_dark)

    # Dark archway cut-out in the center (visually implies the passage)
    arch_w = w * 0.24
    arch_h = h * 0.42
    draw.polygon([(ax - arch_w / 2, ay), (ax + arch_w / 2, ay),
                  (ax + arch_w / 2, ay - arch_h), (ax, ay - arch_h * 1.18), (ax - arch_w / 2, ay - arch_h)],
                 fill=(10, 8, 14, 255), outline=c_dark)

    # Coursed stone block lines either side of the arch
    course_h = (h * 0.62) / 5
    for row in range(5):
        y = ay - row * course_h
        draw.line([(ax - w * 0.46, y), (ax - arch_w / 2 - 4, y)], fill=c_dark, width=1)
        draw.line([(ax + arch_w / 2 + 4, y), (ax + w * 0.46, y)], fill=c_dark, width=1)

    # Twin flanking towers
    for side in (-1, 1):
        tx = ax + side * w * 0.34
        draw.polygon([(tx - w * 0.09, body_top), (tx + w * 0.09, body_top),
                      (tx + w * 0.09, body_top - h * 0.24), (tx - w * 0.09, body_top - h * 0.24)],
                     fill=c_main, outline=c_dark)
        # conical tower roof
        draw.polygon([(tx - w * 0.11, body_top - h * 0.24), (tx + w * 0.11, body_top - h * 0.24),
                      (tx, body_top - h * 0.4)], fill=c_roof, outline=(30, 20, 14, 255))

    # Banner over the arch
    draw.polygon([(ax - 10, body_top), (ax + 10, body_top), (ax + 8, body_top + 26), (ax - 8, body_top + 26)],
                 fill=c_accent, outline=(90, 60, 20, 255))

    save_asset(img, "env_gatehouse.png")


def create_door():
    """Interactive door - 2-frame sheet (64x96 per frame, matching the
    torch-brazier convention of laying animation frames side by side in one
    sheet). Frame 0 = closed (solid), frame 1 = open (passable doorway)."""
    frame_w, frame_h = 64, 96
    sheet = Image.new("RGBA", (frame_w * 2, frame_h), (0, 0, 0, 0))

    c_frame = hx("#5a4028")
    c_frame_dark = hx("#2c2014")
    c_wood = hx("#8a6a45")
    c_wood_dark = hx("#4a3620")
    c_handle = hx("#d8a840")

    # --- Frame 0: closed door ---
    closed, cd = new_canvas(frame_w, frame_h)
    ax, ay = 32, 88
    draw_shadow(cd, (ax, ay), 22, 6, 110)
    # Stone door-frame arch
    cd.polygon([(ax - 20, ay), (ax + 20, ay), (ax + 20, ay - 62), (ax - 20, ay - 62)],
               fill=c_frame, outline=c_frame_dark)
    # Wooden door leaf (inset within the frame)
    cd.polygon([(ax - 15, ay - 4), (ax + 15, ay - 4), (ax + 15, ay - 56), (ax - 15, ay - 56)],
               fill=c_wood, outline=c_wood_dark)
    for lx in (ax - 7, ax, ax + 7):
        cd.line([(lx, ay - 8), (lx, ay - 52)], fill=c_wood_dark, width=1)
    cd.ellipse([ax + 8, ay - 32, ax + 12, ay - 28], fill=c_handle)
    sheet.paste(closed, (0, 0))

    # --- Frame 1: open door (leaf swung aside, dark passable doorway shown) ---
    opened, od = new_canvas(frame_w, frame_h)
    draw_shadow(od, (ax, ay), 22, 6, 110)
    od.polygon([(ax - 20, ay), (ax + 20, ay), (ax + 20, ay - 62), (ax - 20, ay - 62)],
               fill=c_frame, outline=c_frame_dark)
    # Dark open passage
    od.polygon([(ax - 15, ay - 4), (ax + 15, ay - 4), (ax + 15, ay - 56), (ax - 15, ay - 56)],
               fill=(12, 10, 16, 255))
    # Door leaf swung flat against the left frame post (thin sliver)
    od.polygon([(ax - 20, ay - 2), (ax - 15, ay - 4), (ax - 15, ay - 56), (ax - 20, ay - 60)],
               fill=c_wood, outline=c_wood_dark)
    sheet.paste(opened, (frame_w, 0))

    save_asset(sheet, "env_door.png")


def main():
    create_wall_curtain()
    create_wall_corner()
    create_gatehouse()
    create_door()


if __name__ == "__main__":
    main()
