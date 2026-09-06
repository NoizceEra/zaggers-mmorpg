"""
touchup_renamed_sprites.py

Task A2 optional touch-ups for the six renamed legacy sprites
(ASSET_MANIFEST.md Task A2 / ART_PIPELINE_REPORT.md follow-up).

Regenerates ONLY these sheets with bespoke draw functions (higher detail
than the generic archetypes), writing to BOTH asset trees:

  assets/sprites_ff/
  web/assets/sprites_ff/

Targets:
  - pricklespine_thornmarch_ff.png  — redraw head/face off cactuar look
  - cinderpuff_ff.png               — redraw face; keep floating ember sphere
  - verrocaine_sovereign_ff.png     — redraw head off goat/baphomet; keep scale/horns
  - gloopling_bellflower_ff.png     — meadow-blue recolour (+ petal accent)
  - drowned_marrowguard_ff.png      — algae / waterline tint

Sheet layout matches generate_clean_monsters.py:
  256x256 RGBA, 4 rows (Down/Left/Right/Up) x 4 cols (Walk0/Idle/Walk1/Attack),
  cells normalized to 44-52px centered at (32,32) via normalize_and_center_cell.
"""

from __future__ import annotations

import math
import os
from PIL import Image, ImageDraw

ROOT = r"D:\ai-studio\Zaggers"
TARGET_DIRS = [
    os.path.join(ROOT, "assets", "sprites_ff"),
    os.path.join(ROOT, "web", "assets", "sprites_ff"),
]


def create_drop_shadow(draw, cx, cy, rx=16, ry=6, alpha=80):
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(10, 15, 25, alpha))


def normalize_and_center_cell(raw_img, target_min=44, target_max=52, center=(32, 32)):
    bbox = raw_img.getbbox()
    if not bbox:
        return Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    cropped = raw_img.crop(bbox)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    if w == 0 or h == 0:
        return Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    ideal_dim = 48
    scale = ideal_dim / float(max(w, h))
    new_w = max(target_min, min(target_max, int(round(w * scale))))
    new_h = max(target_min, min(target_max, int(round(h * scale))))
    resized = cropped.resize((new_w, new_h), resample=Image.NEAREST)
    cell = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    paste_x = center[0] - new_w // 2
    paste_y = center[1] - new_h // 2
    cell.paste(resized, (paste_x, paste_y), resized)
    return cell


# =============================================================================
# 1. Gloopling Bellflower — meadow-blue slime with petal accent
# =============================================================================
def draw_gloopling_frame(row, col):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    c_body = (70, 155, 230, 255)
    c_shade = (35, 95, 170, 255)
    c_dark = (18, 50, 95, 255)
    c_hl = (170, 220, 255, 255)
    c_spec = (235, 250, 255, 255)
    c_eye = (18, 30, 55, 255)
    c_mouth = (225, 70, 110, 255)
    c_petal = (255, 150, 185, 255)
    c_petal_dk = (200, 90, 130, 255)
    c_cheek = (255, 150, 180, 200)

    cx, cy = 32, 34
    create_drop_shadow(draw, cx, cy + 14, rx=18, ry=6)

    if col == 0:
        rx, ry, tilt = 22, 16, -2
        cy += 2
    elif col == 1:
        rx, ry, tilt = 20, 19, 0
    elif col == 2:
        rx, ry, tilt = 17, 22, 2
        cy -= 2
    else:
        rx, ry, tilt = 23, 17, 0
        cy -= 3

    body = [cx - rx + tilt, cy - ry, cx + rx + tilt, cy + ry]
    draw.ellipse([body[0] - 2, body[1] - 2, body[2] + 2, body[3] + 2], fill=c_dark)
    draw.ellipse(body, fill=c_body)
    draw.ellipse([cx - rx + tilt, cy - ry // 3, cx + rx + tilt, cy + ry], fill=c_shade)
    draw.ellipse([cx - rx + 5 + tilt, cy - ry + 4, cx - 2 + tilt, cy - ry // 2], fill=c_hl)
    draw.ellipse([cx - rx + 7 + tilt, cy - ry + 5, cx - 6 + tilt, cy - ry + 9], fill=c_spec)

    # Bellflower petal tuft on crown (identity mark)
    px, py = cx + tilt, cy - ry + 1
    draw.ellipse([px - 5, py - 6, px - 1, py - 1], fill=c_petal)
    draw.ellipse([px + 1, py - 6, px + 5, py - 1], fill=c_petal)
    draw.ellipse([px - 3, py - 9, px + 3, py - 3], fill=c_petal_dk)
    draw.ellipse([px - 2, py - 8, px + 2, py - 4], fill=c_petal)

    if col == 3:
        draw.ellipse([cx - rx - 4, cy - 6, cx - rx - 1, cy - 3], fill=c_body)
        draw.ellipse([cx + rx + 1, cy - 4, cx + rx + 4, cy - 1], fill=c_body)

    if row == 0:
        ex_off, ey = 6, cy - 2
        for s in (-1, 1):
            ex = cx + s * ex_off
            draw.ellipse([ex - 3, ey - 4, ex + 3, ey + 4], fill=c_eye)
            draw.ellipse([ex - 1, ey - 3, ex + 1, ey - 1], fill=(255, 255, 255, 255))
            draw.ellipse([ex + (3 if s > 0 else -5), ey + 3, ex + (5 if s > 0 else -1), ey + 6], fill=c_cheek)
        if col == 3:
            draw.ellipse([cx - 3, ey + 4, cx + 3, ey + 10], fill=c_mouth)
        else:
            draw.line([(cx - 2, ey + 5), (cx, ey + 7), (cx + 2, ey + 5)], fill=c_dark, width=2)
    elif row == 1:
        ex, ey = cx - 10, cy - 2
        draw.ellipse([ex - 3, ey - 4, ex + 3, ey + 4], fill=c_eye)
        draw.ellipse([ex - 2, ey - 3, ex, ey - 1], fill=(255, 255, 255, 255))
        draw.ellipse([ex - 4, ey + 3, ex - 1, ey + 6], fill=c_cheek)
        if col == 3:
            draw.ellipse([ex - 4, ey + 4, ex, ey + 9], fill=c_mouth)
        else:
            draw.line([(ex - 3, ey + 5), (ex, ey + 6)], fill=c_dark, width=2)
    elif row == 2:
        ex, ey = cx + 10, cy - 2
        draw.ellipse([ex - 3, ey - 4, ex + 3, ey + 4], fill=c_eye)
        draw.ellipse([ex, ey - 3, ex + 2, ey - 1], fill=(255, 255, 255, 255))
        draw.ellipse([ex + 1, ey + 3, ex + 4, ey + 6], fill=c_cheek)
        if col == 3:
            draw.ellipse([ex, ey + 4, ex + 4, ey + 9], fill=c_mouth)
        else:
            draw.line([(ex, ey + 6), (ex + 3, ey + 5)], fill=c_dark, width=2)
    else:
        draw.arc([cx - rx + 4 + tilt, cy - ry + 2, cx + rx - 4 + tilt, cy - 2], 200, 340, fill=c_dark, width=2)

    return normalize_and_center_cell(img)


# =============================================================================
# 2. Drowned Marrowguard — skeleton with algae / waterline tint
# =============================================================================
def draw_marrowguard_frame(row, col):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    c_bone = (200, 220, 205, 255)
    c_bone_dark = (110, 140, 125, 255)
    c_outline = (40, 55, 50, 255)
    c_algae = (55, 140, 95, 255)
    c_water = (60, 130, 160, 220)
    c_socket = (15, 25, 30, 255)
    c_eye = (40, 220, 200, 255)
    c_shield_rim = (120, 170, 165, 255)
    c_shield_fill = (55, 85, 95, 255)
    c_boss = (80, 190, 150, 255)
    c_blade = (170, 205, 215, 255)
    c_hilt = (140, 120, 55, 255)

    cx, cy = 32, 32
    create_drop_shadow(draw, cx, cy + 18, rx=13, ry=5)

    l_leg_x, r_leg_x = cx - 5, cx + 5
    if col == 0:
        l_leg_x -= 2
    elif col == 2:
        r_leg_x += 2

    # Legs with waterline wash on lower half
    draw.line([(cx - 5, cy + 8), (l_leg_x, cy + 18)], fill=c_bone, width=3)
    draw.line([(cx + 5, cy + 8), (r_leg_x, cy + 18)], fill=c_bone, width=3)
    draw.line([(cx - 5, cy + 14), (l_leg_x, cy + 18)], fill=c_algae, width=3)
    draw.line([(cx + 5, cy + 14), (r_leg_x, cy + 18)], fill=c_algae, width=3)

    # Spine & ribs
    draw.line([(cx, cy - 4), (cx, cy + 8)], fill=c_bone_dark, width=3)
    for ry in range(cy - 2, cy + 6, 3):
        draw.line([(cx - 6, ry), (cx + 6, ry)], fill=c_bone, width=2)
    # Algae drape across lower ribs
    draw.line([(cx - 7, cy + 4), (cx + 7, cy + 5)], fill=c_algae, width=2)
    draw.ellipse([cx - 3, cy + 5, cx + 3, cy + 9], fill=c_water)

    # Skull
    skull = [cx - 8, cy - 18, cx + 8, cy - 4]
    draw.ellipse(skull, fill=c_bone, outline=c_outline)
    draw.rectangle([cx - 4, cy - 5, cx + 4, cy - 2], fill=c_bone_dark)
    # Verdigris streak on skull crown
    draw.arc([cx - 7, cy - 17, cx + 7, cy - 7], 200, 340, fill=c_algae, width=2)

    if row == 0:
        draw.ellipse([cx - 6, cy - 14, cx - 2, cy - 9], fill=c_socket)
        draw.ellipse([cx + 2, cy - 14, cx + 6, cy - 9], fill=c_socket)
        draw.point((cx - 4, cy - 11), fill=c_eye)
        draw.point((cx + 4, cy - 11), fill=c_eye)
        sx, sy = cx - 13, cy + 2
        draw.ellipse([sx - 8, sy - 8, sx + 8, sy + 8], fill=c_shield_fill, outline=c_shield_rim)
        draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=c_boss)
        # Barnacle dots on shield
        draw.point((sx - 4, sy - 2), fill=c_algae)
        draw.point((sx + 3, sy + 2), fill=c_algae)
        hx, hy = cx + 12, cy + 4
        draw.line([(hx - 3, hy), (hx + 3, hy)], fill=c_hilt, width=2)
        if col == 3:
            draw.polygon([(hx, hy), (hx + 14, hy - 14), (hx + 18, hy - 10)], fill=c_blade)
            draw.arc([hx, hy - 16, hx + 20, hy + 4], 180, 330, fill=(120, 220, 230, 200), width=3)
        else:
            draw.line([(hx, hy), (hx + 8, hy - 12)], fill=c_blade, width=3)
    elif row == 1:
        draw.ellipse([cx - 6, cy - 14, cx - 2, cy - 9], fill=c_socket)
        draw.point((cx - 4, cy - 11), fill=c_eye)
        sx, sy = cx - 12, cy + 2
        draw.ellipse([sx - 6, sy - 8, sx + 6, sy + 8], fill=c_shield_fill, outline=c_shield_rim)
        draw.ellipse([sx - 2, sy - 3, sx + 2, sy + 3], fill=c_boss)
    elif row == 2:
        draw.ellipse([cx + 2, cy - 14, cx + 6, cy - 9], fill=c_socket)
        draw.point((cx + 4, cy - 11), fill=c_eye)
        hx, hy = cx + 10, cy + 4
        if col == 3:
            draw.polygon([(hx, hy), (hx + 16, hy - 2), (hx + 14, hy + 4)], fill=c_blade)
        else:
            draw.line([(hx, hy), (hx + 10, hy - 8)], fill=c_blade, width=3)
    else:
        draw.ellipse([cx - 7, cy - 16, cx + 7, cy - 6], fill=c_bone)
        draw.arc([cx - 6, cy - 15, cx + 6, cy - 7], 200, 340, fill=c_algae, width=2)

    return normalize_and_center_cell(img)


# =============================================================================
# 3. Thornmarch Pricklespine — bristling green biped, non-cactuar head/face
# =============================================================================
def draw_pricklespine_frame(row, col):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    c_body = (55, 155, 70, 255)
    c_shade = (30, 100, 45, 255)
    c_dark = (18, 55, 28, 255)
    c_spine = (200, 230, 90, 255)
    c_spine_dk = (140, 170, 40, 255)
    c_hl = (120, 210, 130, 255)
    c_eye = (255, 210, 60, 255)
    c_pupil = (30, 25, 10, 255)
    c_mouth = (40, 70, 35, 255)

    cx, cy = 32, 32
    create_drop_shadow(draw, cx, cy + 18, rx=12, ry=4)

    # Walk bob / attack lean
    bob = 0
    if col == 0:
        bob = 1
    elif col == 2:
        bob = -1
    elif col == 3:
        bob = -2
    cyb = cy + bob

    # Tapered bristled torso (pillared but slightly pear-shaped — not FF cactus block)
    draw.polygon(
        [
            (cx - 7, cyb - 10),
            (cx + 7, cyb - 10),
            (cx + 9, cyb + 10),
            (cx + 5, cyb + 14),
            (cx - 5, cyb + 14),
            (cx - 9, cyb + 10),
        ],
        fill=c_body,
        outline=c_dark,
    )
    draw.ellipse([cx - 5, cyb - 2, cx + 5, cyb + 10], fill=c_shade)

    # Side thorn bristles along torso (not top-only needles)
    for i, (dx, dy) in enumerate([(-10, -6), (-11, 0), (-10, 6), (10, -6), (11, 0), (10, 6)]):
        tip_x = cx + dx + (1 if dx > 0 else -1)
        tip_y = cyb + dy - 4
        draw.polygon(
            [(cx + dx // 2, cyb + dy), (tip_x, tip_y), (cx + dx // 2, cyb + dy + 3)],
            fill=c_spine if i % 2 == 0 else c_spine_dk,
        )

    # Organic curved branch-limbs (not right-angle cactuar arms)
    if col == 0:
        # left up-curve, right down-curve
        draw.line([(cx - 8, cyb - 2), (cx - 14, cyb - 6), (cx - 16, cyb - 12)], fill=c_body, width=4)
        draw.line([(cx + 8, cyb + 2), (cx + 14, cyb + 4), (cx + 15, cyb + 10)], fill=c_body, width=4)
    elif col == 2:
        draw.line([(cx - 8, cyb + 2), (cx - 14, cyb + 4), (cx - 15, cyb + 10)], fill=c_body, width=4)
        draw.line([(cx + 8, cyb - 2), (cx + 14, cyb - 6), (cx + 16, cyb - 12)], fill=c_body, width=4)
    elif col == 3:
        # arms flung out for needle spray
        draw.line([(cx - 8, cyb - 2), (cx - 18, cyb - 4)], fill=c_body, width=4)
        draw.line([(cx + 8, cyb - 2), (cx + 18, cyb - 4)], fill=c_body, width=4)
        for angle in range(0, 360, 40):
            rad = math.radians(angle)
            nx = cx + int(20 * math.cos(rad))
            ny = cyb + int(18 * math.sin(rad))
            draw.line([(cx, cyb), (nx, ny)], fill=c_spine, width=1)
    else:
        draw.line([(cx - 8, cyb - 2), (cx - 14, cyb - 8), (cx - 13, cyb - 14)], fill=c_body, width=4)
        draw.line([(cx + 8, cyb - 2), (cx + 14, cyb - 8), (cx + 13, cyb - 14)], fill=c_body, width=4)

    # Short root-feet (angled, not square cactuar feet)
    draw.line([(cx - 4, cyb + 14), (cx - 8, cyb + 18)], fill=c_body, width=3)
    draw.line([(cx + 4, cyb + 14), (cx + 8, cyb + 18)], fill=c_body, width=3)
    draw.ellipse([cx - 10, cyb + 16, cx - 5, cyb + 19], fill=c_shade)
    draw.ellipse([cx + 5, cyb + 16, cx + 10, cyb + 19], fill=c_shade)

    # --- NEW HEAD: thistle-bulb crest (not rounded cactus dome + 3 needles) ---
    hx, hy = cx, cyb - 14
    # Bulbous thistle head
    draw.ellipse([hx - 8, hy - 6, hx + 8, hy + 6], fill=c_body, outline=c_dark)
    draw.ellipse([hx - 5, hy - 4, hx + 2, hy + 1], fill=c_hl)
    # Ring of short radial crest spines (thistle look)
    for angle in range(-60, 70, 30):
        rad = math.radians(angle - 90)
        sx = hx + int(5 * math.cos(rad))
        sy = hy + int(3 * math.sin(rad)) - 2
        tx = hx + int(11 * math.cos(rad))
        ty = hy + int(9 * math.sin(rad)) - 4
        draw.line([(sx, sy), (tx, ty)], fill=c_spine, width=2)
    # Central darker crest tuft
    draw.polygon([(hx - 2, hy - 5), (hx, hy - 14), (hx + 2, hy - 5)], fill=c_spine_dk)

    # Face — amber oval eyes + tiny beak notch (not stitch | | + square mouth)
    if row == 0:
        for s in (-1, 1):
            ex = hx + s * 4
            draw.ellipse([ex - 3, hy - 2, ex + 3, hy + 3], fill=c_eye)
            draw.ellipse([ex - 1, hy - 1, ex + 1, hy + 1], fill=c_pupil)
        draw.polygon([(hx - 2, hy + 4), (hx + 2, hy + 4), (hx, hy + 7)], fill=c_mouth)
    elif row == 1:
        draw.ellipse([hx - 7, hy - 2, hx - 1, hy + 3], fill=c_eye)
        draw.ellipse([hx - 5, hy - 1, hx - 3, hy + 1], fill=c_pupil)
        draw.polygon([(hx - 6, hy + 4), (hx - 2, hy + 4), (hx - 4, hy + 7)], fill=c_mouth)
    elif row == 2:
        draw.ellipse([hx + 1, hy - 2, hx + 7, hy + 3], fill=c_eye)
        draw.ellipse([hx + 3, hy - 1, hx + 5, hy + 1], fill=c_pupil)
        draw.polygon([(hx + 2, hy + 4), (hx + 6, hy + 4), (hx + 4, hy + 7)], fill=c_mouth)
    else:
        # Back of thistle crest
        draw.ellipse([hx - 7, hy - 5, hx + 7, hy + 4], fill=c_shade)
        draw.polygon([(hx - 2, hy - 4), (hx, hy - 13), (hx + 2, hy - 4)], fill=c_spine_dk)

    return normalize_and_center_cell(img)


# =============================================================================
# 4. Cinderpuff — floating ember sphere, redrawn face (not FF bomb grin)
# =============================================================================
def draw_cinderpuff_frame(row, col):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    c_shell = (50, 42, 48, 255)
    c_shell_dk = (28, 22, 26, 255)
    c_hl = (95, 80, 85, 255)
    c_ember = (255, 120, 40, 255)
    c_core = (255, 230, 90, 255)
    c_glow = (255, 160, 50, 160)
    c_wisp = (255, 200, 120, 200)
    c_crack = (255, 90, 30, 255)

    cx, cy = 32, 34
    # Float bob
    if col == 0:
        cy += 1
    elif col == 2:
        cy -= 1
    elif col == 3:
        cy -= 2

    create_drop_shadow(draw, cx, cy + 18, rx=14, ry=5, alpha=60)

    if col == 3:
        c_shell = (220, 70, 30, 255)
        draw.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=(255, 100, 20, 70))

    # Soft outer glow (ember sphere, not hard bomb)
    draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=c_glow)
    draw.ellipse([cx - 17, cy - 17, cx + 17, cy + 17], fill=c_shell, outline=c_shell_dk)
    draw.ellipse([cx - 13, cy - 14, cx - 3, cy - 6], fill=c_hl)

    # Ember cracks (subtle veins, not face)
    draw.line([(cx - 10, cy + 2), (cx - 2, cy + 8), (cx + 4, cy + 4)], fill=c_crack, width=1)
    draw.line([(cx + 6, cy - 2), (cx + 12, cy + 4)], fill=c_crack, width=1)

    # Rising ember wisps instead of coiled fuse
    wisp_x = cx + (2 if col % 2 == 0 else -2)
    draw.ellipse([wisp_x - 2, cy - 26, wisp_x + 2, cy - 20], fill=c_wisp)
    draw.ellipse([wisp_x + 3, cy - 30, wisp_x + 7, cy - 25], fill=c_ember)
    draw.ellipse([wisp_x - 1, cy - 33, wisp_x + 3, cy - 29], fill=c_core)
    if col == 3:
        draw.ellipse([cx - 8, cy - 28, cx - 4, cy - 24], fill=c_ember)
        draw.ellipse([cx + 6, cy - 27, cx + 11, cy - 22], fill=c_core)

    # --- NEW FACE: soft circular ember eyes + puff-ring mouth (not triangle glare) ---
    if row in (0, 1, 2):
        if row == 0:
            eyes = [(cx - 7, cy - 3), (cx + 7, cy - 3)]
            mx = cx
        elif row == 1:
            eyes = [(cx - 9, cy - 3)]
            mx = cx - 6
        else:
            eyes = [(cx + 9, cy - 3)]
            mx = cx + 6

        for (ex, ey) in eyes:
            draw.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(255, 140, 40, 120))
            draw.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=c_ember)
            draw.ellipse([ex - 1, ey - 1, ex + 1, ey + 1], fill=c_core)

        # Soft puff mouth (O / smile ring), not triangular fire gape
        if col == 3:
            draw.ellipse([mx - 5, cy + 4, mx + 5, cy + 12], fill=c_ember)
            draw.ellipse([mx - 3, cy + 6, mx + 3, cy + 10], fill=c_core)
        else:
            draw.arc([mx - 5, cy + 4, mx + 5, cy + 11], 20, 160, fill=c_ember, width=2)
            draw.ellipse([mx - 2, cy + 7, mx + 2, cy + 10], fill=(255, 180, 80, 180))
    else:
        # Back: glowing seam
        draw.arc([cx - 10, cy - 8, cx + 10, cy + 8], 200, 340, fill=c_ember, width=2)
        draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=c_core)

    return normalize_and_center_cell(img)


# =============================================================================
# 5. Verrocaine the Horned Sovereign — antlered mask head (not goat/baphomet)
# =============================================================================
def draw_verrocaine_frame(row, col):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    c_fur = (42, 30, 58, 255)
    c_fur_dk = (22, 14, 32, 255)
    c_armor = (70, 50, 90, 255)
    c_horn = (210, 185, 120, 255)
    c_horn_dk = (130, 100, 50, 255)
    c_mask = (200, 190, 205, 255)
    c_mask_dk = (120, 110, 130, 255)
    c_eye = (180, 70, 255, 255)
    c_eye_core = (255, 220, 255, 255)
    c_cloth = (140, 25, 55, 255)
    c_cloth_dk = (90, 15, 35, 255)
    c_handle = (90, 60, 35, 255)
    c_blade = (160, 60, 140, 255)
    c_crown = (180, 140, 60, 255)

    cx, cy = 32, 32
    create_drop_shadow(draw, cx, cy + 20, rx=18, ry=6)

    # Broad seated/throne torso (kept scale & posture)
    draw.polygon(
        [(cx - 13, cy - 4), (cx + 13, cy - 4), (cx + 11, cy + 14), (cx - 11, cy + 14)],
        fill=c_fur,
        outline=c_fur_dk,
    )
    # Shoulder pauldrons
    draw.ellipse([cx - 16, cy - 6, cx - 6, cy + 4], fill=c_armor)
    draw.ellipse([cx + 6, cy - 6, cx + 16, cy + 4], fill=c_armor)
    # Crimson drape / loincloth
    draw.polygon(
        [(cx - 8, cy + 8), (cx + 8, cy + 8), (cx + 6, cy + 20), (cx, cy + 17), (cx - 6, cy + 20)],
        fill=c_cloth,
        outline=c_cloth_dk,
    )

    # Legs (seated-forward posture)
    draw.polygon([(cx - 10, cy + 12), (cx - 4, cy + 12), (cx - 6, cy + 20), (cx - 12, cy + 20)], fill=c_fur_dk)
    draw.polygon([(cx + 4, cy + 12), (cx + 10, cy + 12), (cx + 12, cy + 20), (cx + 6, cy + 20)], fill=c_fur_dk)

    # --- NEW HEAD: elongated pale mask + swept root-antlers (not goat snout) ---
    hx, hy = cx, cy - 10
    # Neck
    draw.rectangle([cx - 3, hy + 2, cx + 3, hy + 8], fill=c_fur_dk)
    # Elongated oval mask-face (humanoid demonic, no muzzle)
    draw.ellipse([hx - 8, hy - 10, hx + 8, hy + 4], fill=c_mask, outline=c_mask_dk)
    draw.ellipse([hx - 6, hy - 8, hx + 2, hy - 2], fill=(230, 225, 235, 255))

    # Swept-back branching antlers (root-crown, not classic Baphomet curls)
    # Left antler
    draw.line([(hx - 5, hy - 8), (hx - 14, hy - 18)], fill=c_horn, width=3)
    draw.line([(hx - 10, hy - 14), (hx - 18, hy - 16)], fill=c_horn, width=2)
    draw.line([(hx - 10, hy - 14), (hx - 16, hy - 22)], fill=c_horn_dk, width=2)
    # Right antler
    draw.line([(hx + 5, hy - 8), (hx + 14, hy - 18)], fill=c_horn, width=3)
    draw.line([(hx + 10, hy - 14), (hx + 18, hy - 16)], fill=c_horn, width=2)
    draw.line([(hx + 10, hy - 14), (hx + 16, hy - 22)], fill=c_horn_dk, width=2)
    # Small brow crown spike
    draw.polygon([(hx - 2, hy - 10), (hx, hy - 16), (hx + 2, hy - 10)], fill=c_crown)

    if row == 0:
        # Violet almond eyes + thin mouth slit
        for s in (-1, 1):
            ex = hx + s * 4
            draw.ellipse([ex - 3, hy - 5, ex + 3, hy - 1], fill=c_eye)
            draw.point((ex, hy - 3), fill=c_eye_core)
        draw.line([(hx - 3, hy + 1), (hx + 3, hy + 1)], fill=c_mask_dk, width=2)
        # Scythe
        handle_x = cx + 15
        draw.line([(handle_x, cy - 22), (handle_x, cy + 18)], fill=c_handle, width=3)
        draw.polygon(
            [(handle_x, cy - 20), (handle_x + 16, cy - 26), (handle_x + 10, cy - 12)],
            fill=c_blade,
        )
        if col == 3:
            draw.arc([cx - 22, cy - 22, cx + 24, cy + 18], 150, 340, fill=(200, 80, 255, 200), width=4)
    elif row == 1:
        draw.ellipse([hx - 7, hy - 5, hx - 1, hy - 1], fill=c_eye)
        draw.point((hx - 4, hy - 3), fill=c_eye_core)
        draw.line([(hx - 6, hy + 1), (hx - 1, hy + 1)], fill=c_mask_dk, width=2)
        draw.line([(cx - 12, cy - 18), (cx - 12, cy + 16)], fill=c_handle, width=3)
        draw.polygon([(cx - 12, cy - 16), (cx - 26, cy - 22), (cx - 18, cy - 10)], fill=c_blade)
    elif row == 2:
        draw.ellipse([hx + 1, hy - 5, hx + 7, hy - 1], fill=c_eye)
        draw.point((hx + 4, hy - 3), fill=c_eye_core)
        draw.line([(hx + 1, hy + 1), (hx + 6, hy + 1)], fill=c_mask_dk, width=2)
        draw.line([(cx + 12, cy - 18), (cx + 12, cy + 16)], fill=c_handle, width=3)
        draw.polygon([(cx + 12, cy - 16), (cx + 26, cy - 22), (cx + 18, cy - 10)], fill=c_blade)
    else:
        # Back of mask + antler roots
        draw.ellipse([hx - 7, hy - 9, hx + 7, hy + 2], fill=c_fur_dk)
        draw.line([(hx - 4, hy - 8), (hx - 12, hy - 16)], fill=c_horn_dk, width=3)
        draw.line([(hx + 4, hy - 8), (hx + 12, hy - 16)], fill=c_horn_dk, width=3)
        draw.polygon([(hx - 2, hy - 9), (hx, hy - 15), (hx + 2, hy - 9)], fill=c_crown)

    return normalize_and_center_cell(img)


# =============================================================================
# Sheet generation + verification
# =============================================================================
GENERATORS = {
    "gloopling_bellflower_ff.png": draw_gloopling_frame,
    "drowned_marrowguard_ff.png": draw_marrowguard_frame,
    "pricklespine_thornmarch_ff.png": draw_pricklespine_frame,
    "cinderpuff_ff.png": draw_cinderpuff_frame,
    "verrocaine_sovereign_ff.png": draw_verrocaine_frame,
}


def generate_sheet(drawer):
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    for row in range(4):
        for col in range(4):
            cell = drawer(row, col)
            sheet.paste(cell, (col * 64, row * 64), cell)
    return sheet


def verify_sheet(path, filename):
    assert os.path.exists(path), f"Missing: {path}"
    sheet = Image.open(path)
    assert sheet.size == (256, 256), f"{filename}: size {sheet.size}"
    assert sheet.mode == "RGBA", f"{filename}: mode {sheet.mode}"
    warnings = []
    for r in range(4):
        for c in range(4):
            cell = sheet.crop((c * 64, r * 64, (c + 1) * 64, (r + 1) * 64))
            bbox = cell.getbbox()
            assert bbox is not None, f"{filename}: empty cell ({c},{r})"
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            cx = (bbox[0] + bbox[2]) / 2.0
            cy = (bbox[1] + bbox[3]) / 2.0
            if not (44 <= w <= 52 and 44 <= h <= 52 and 31.0 <= cx <= 33.0 and 31.0 <= cy <= 33.0):
                warnings.append(f"  cell ({c},{r}): {w}x{h} center=({cx:.1f},{cy:.1f})")
    return warnings


def main():
    print("=== Task A2: Touch-up renamed sprites (bespoke redraws) ===")
    all_warnings = []
    for filename, drawer in GENERATORS.items():
        sheet = generate_sheet(drawer)
        for d in TARGET_DIRS:
            os.makedirs(d, exist_ok=True)
            out = os.path.join(d, filename)
            sheet.save(out, "PNG")
            print(f"  Saved {out}")
            warns = verify_sheet(out, filename)
            if warns:
                print(f"  WARNINGS in {out}:")
                for w in warns:
                    print(w)
                all_warnings.extend(warns)
            else:
                print(f"  OK 256x256 RGBA, all 16 cells 44-52px @ (32,32)")

    print()
    if all_warnings:
        print(f"Done with {len(all_warnings)} cell-bound warnings (see above).")
    else:
        print("All 5 sheets verified in both asset trees.")
    print(f"Targets: {', '.join(GENERATORS)}")


if __name__ == "__main__":
    main()
