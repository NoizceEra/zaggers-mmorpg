import os
import math
from PIL import Image, ImageDraw

# Target directories to save generated monster sprite sheets
TARGET_DIRS = [
    r"D:\ai-studio\Zaggers\assets\sprites_ff",
    r"D:\ai-studio\Zaggers\web\assets\sprites_ff"
]

def normalize_and_center_cell(raw_img, target_min=44, target_max=52, center=(32, 32)):
    """
    Takes a raw 64x64 (or larger) RGBA image of a sprite, finds its bounding box,
    scales/pads it so both width and height are strictly within target_min..target_max (44..52),
    and centers it perfectly at (32, 32) inside a 64x64 cell.
    """
    bbox = raw_img.getbbox()
    if not bbox:
        return Image.new("RGBA", (64, 64), (0, 0, 0, 0))

    cropped = raw_img.crop(bbox)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    if w == 0 or h == 0:
        return Image.new("RGBA", (64, 64), (0, 0, 0, 0))

    # Scale so the larger dimension is ~48px (ideal center of 44..52)
    ideal_dim = 48
    scale = ideal_dim / float(max(w, h))

    new_w = int(round(w * scale))
    new_h = int(round(h * scale))

    # Strictly clamp both dimensions to target_min..target_max (44..52)
    new_w = max(target_min, min(target_max, new_w))
    new_h = max(target_min, min(target_max, new_h))

    # Resize cleanly preserving pixel art details
    resized = cropped.resize((new_w, new_h), resample=Image.NEAREST)

    cell = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    paste_x = center[0] - new_w // 2
    paste_y = center[1] - new_h // 2
    cell.paste(resized, (paste_x, paste_y), resized)

    return cell


def create_drop_shadow(draw, cx, cy, rx=20, ry=8, alpha=80):
    """Draws an oval drop shadow at base."""
    bbox = [cx - rx, cy - ry, cx + rx, cy + ry]
    draw.ellipse(bbox, fill=(10, 15, 25, alpha))


# -----------------------------------------------------------------------------
# MONSTER 1: Slime Green (Poring)
# -----------------------------------------------------------------------------
def draw_slime_frame(row, col):
    """
    row: 0=Down, 1=Left, 2=Right, 3=Up
    col: 0=Walk0, 1=Idle, 2=Walk1, 3=Attack
    """
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Base colors
    c_green = (50, 215, 75, 255)
    c_shade = (25, 140, 50, 255)
    c_dark = (12, 70, 28, 255)
    c_hl = (175, 255, 185, 255)
    c_spec = (240, 255, 245, 255)
    c_eye = (20, 35, 25, 255)
    c_mouth = (225, 60, 90, 255)

    cx, cy = 32, 34
    create_drop_shadow(draw, cx, cy + 14, rx=18, ry=6)

    # Shape variations based on column (Walk0, Idle, Walk1, Attack)
    if col == 0:  # Walk0: Squashed blob, left tilt
        rx, ry = 22, 16
        cy += 2
        tilt = -2
    elif col == 1:  # Idle: Standard teardrop dome
        rx, ry = 20, 19
        tilt = 0
    elif col == 2:  # Walk1: Stretched tall, right tilt
        rx, ry = 17, 22
        cy -= 2
        tilt = 2
    else:  # Attack: Lunge forward, wide bounce
        rx, ry = 23, 17
        cy -= 3
        tilt = 0

    # Draw body outline & main fill
    body_bbox = [cx - rx + tilt, cy - ry, cx + rx + tilt, cy + ry]
    draw.ellipse([body_bbox[0]-2, body_bbox[1]-2, body_bbox[2]+2, body_bbox[3]+2], fill=c_dark)
    draw.ellipse(body_bbox, fill=c_green)

    # Bottom shading arc
    shade_bbox = [cx - rx + tilt, cy - ry // 3, cx + rx + tilt, cy + ry]
    draw.ellipse(shade_bbox, fill=c_shade)

    # Top-left glossy highlight
    hl_bbox = [cx - rx + 5 + tilt, cy - ry + 4, cx - 2 + tilt, cy - ry // 2]
    draw.ellipse(hl_bbox, fill=c_hl)
    draw.ellipse([cx - rx + 7 + tilt, cy - ry + 5, cx - 6 + tilt, cy - ry + 9], fill=c_spec)

    # Splash droplets for attack pose
    if col == 3:
        draw.ellipse([cx - rx - 4, cy - 6, cx - rx - 1, cy - 3], fill=c_green)
        draw.ellipse([cx + rx + 1, cy - 4, cx + rx + 4, cy - 1], fill=c_green)

    # Eyes & Mouth based on direction (row: 0=Down, 1=Left, 2=Right, 3=Up)
    if row == 0:  # Down facing
        ex_off = 6
        ey = cy - 2
        # Left eye
        draw.ellipse([cx - ex_off - 3, ey - 4, cx - ex_off + 3, ey + 4], fill=c_eye)
        draw.ellipse([cx - ex_off - 1, ey - 3, cx - ex_off + 1, ey - 1], fill=(255, 255, 255, 255))
        # Right eye
        draw.ellipse([cx + ex_off - 3, ey - 4, cx + ex_off + 3, ey + 4], fill=c_eye)
        draw.ellipse([cx + ex_off - 1, ey - 3, cx + ex_off + 1, ey - 1], fill=(255, 255, 255, 255))

        # Mouth
        if col == 3:  # Open mouth attack
            draw.ellipse([cx - 3, ey + 4, cx + 3, ey + 10], fill=c_mouth)
        else:
            draw.line([(cx - 2, ey + 5), (cx, ey + 7), (cx + 2, ey + 5)], fill=c_dark, width=2)

        # Pink cheeks
        draw.ellipse([cx - ex_off - 5, ey + 3, cx - ex_off - 1, ey + 6], fill=(255, 140, 160, 200))
        draw.ellipse([cx + ex_off + 1, ey + 3, cx + ex_off + 5, ey + 6], fill=(255, 140, 160, 200))

    elif row == 1:  # Left facing
        ex = cx - 10
        ey = cy - 2
        draw.ellipse([ex - 3, ey - 4, ex + 3, ey + 4], fill=c_eye)
        draw.ellipse([ex - 2, ey - 3, ex, ey - 1], fill=(255, 255, 255, 255))
        if col == 3:
            draw.ellipse([ex - 4, ey + 4, ex, ey + 9], fill=c_mouth)
        else:
            draw.line([(ex - 3, ey + 5), (ex, ey + 6)], fill=c_dark, width=2)
        draw.ellipse([ex - 4, ey + 3, ex - 1, ey + 6], fill=(255, 140, 160, 200))

    elif row == 2:  # Right facing
        ex = cx + 10
        ey = cy - 2
        draw.ellipse([ex - 3, ey - 4, ex + 3, ey + 4], fill=c_eye)
        draw.ellipse([ex, ey - 3, ex + 2, ey - 1], fill=(255, 255, 255, 255))
        if col == 3:
            draw.ellipse([ex, ey + 4, ex + 4, ey + 9], fill=c_mouth)
        else:
            draw.line([(ex, ey + 6), (ex + 3, ey + 5)], fill=c_dark, width=2)
        draw.ellipse([ex + 1, ey + 3, ex + 4, ey + 6], fill=(255, 140, 160, 200))

    elif row == 3:  # Up facing
        # Back of slime - gel contour ridges
        draw.arc([cx - 12, cy - 10, cx + 12, cy + 5], start=200, end=340, fill=c_hl, width=2)

    return normalize_and_center_cell(img)


# -----------------------------------------------------------------------------
# MONSTER 2: Goblin Warrior
# -----------------------------------------------------------------------------
def draw_goblin_frame(row, col):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    c_skin = (90, 175, 45, 255)
    c_skin_dark = (50, 110, 25, 255)
    c_outline = (25, 60, 15, 255)
    c_vest = (135, 80, 40, 255)
    c_vest_dark = (75, 40, 20, 255)
    c_belt = (50, 30, 15, 255)
    c_buckle = (235, 195, 30, 255)
    c_blade = (195, 210, 225, 255)
    c_eye = (255, 220, 30, 255)

    cx, cy = 32, 32
    create_drop_shadow(draw, cx, cy + 18, rx=14, ry=5)

    # Poses offset
    l_leg_y, r_leg_y = 0, 0
    arm_angle = 0
    if col == 0:  # Walk0
        l_leg_y = -2
        r_leg_y = 2
    elif col == 2:  # Walk1
        l_leg_y = 2
        r_leg_y = -2
    elif col == 3:  # Attack
        arm_angle = 45

    # Feet / Legs
    draw.rectangle([cx - 8, cy + 12 + l_leg_y, cx - 3, cy + 18], fill=c_skin_dark, outline=c_outline)
    draw.rectangle([cx + 3, cy + 12 + r_leg_y, cx + 8, cy + 18], fill=c_skin_dark, outline=c_outline)

    # Body / Vest
    body_poly = [(cx - 9, cy - 2), (cx + 9, cy - 2), (cx + 7, cy + 13), (cx - 7, cy + 13)]
    draw.polygon(body_poly, fill=c_vest, outline=c_vest_dark)

    # Belt & Buckle
    draw.rectangle([cx - 7, cy + 8, cx + 7, cy + 11], fill=c_belt)
    draw.rectangle([cx - 2, cy + 7, cx + 2, cy + 12], fill=c_buckle)

    # Head (Green Goblin head with pointy ears)
    head_bbox = [cx - 10, cy - 18, cx + 10, cy - 1]
    draw.ellipse(head_bbox, fill=c_skin, outline=c_outline)

    # Pointy Ears
    # Left ear
    draw.polygon([(cx - 8, cy - 10), (cx - 21, cy - 16), (cx - 8, cy - 4)], fill=c_skin, outline=c_outline)
    # Right ear
    draw.polygon([(cx + 8, cy - 10), (cx + 21, cy - 16), (cx + 8, cy - 4)], fill=c_skin, outline=c_outline)

    # Direction-specific features & Dagger weapon
    if row == 0:  # Down
        # Glowing Yellow Eyes
        draw.ellipse([cx - 6, cy - 12, cx - 2, cy - 8], fill=c_eye)
        draw.ellipse([cx + 2, cy - 12, cx + 6, cy - 8], fill=c_eye)
        draw.point((cx - 4, cy - 10), fill=(0, 0, 0, 255))
        draw.point((cx + 4, cy - 10), fill=(0, 0, 0, 255))
        # Snout / Mouth
        draw.polygon([(cx - 2, cy - 7), (cx + 2, cy - 7), (cx, cy - 4)], fill=c_skin_dark)
        # Dagger in right hand
        hand_x, hand_y = cx + 12, cy + 4
        draw.ellipse([hand_x - 3, hand_y - 3, hand_x + 3, hand_y + 3], fill=c_skin)
        if col == 3:  # Attack slash
            draw.polygon([(hand_x, hand_y), (hand_x + 14, hand_y - 12), (hand_x + 16, hand_y - 8)], fill=c_blade)
            draw.arc([hand_x, hand_y - 14, hand_x + 18, hand_y + 4], 200, 340, fill=(255, 240, 160, 200), width=3)
        else:
            draw.polygon([(hand_x, hand_y), (hand_x + 6, hand_y - 10), (hand_x + 8, hand_y - 8)], fill=c_blade)

    elif row == 1:  # Left
        # Profile Eyes
        draw.ellipse([cx - 8, cy - 12, cx - 4, cy - 8], fill=c_eye)
        # Dagger thrust left
        hand_x, hand_y = cx - 10, cy + 4
        if col == 3:
            draw.polygon([(hand_x, hand_y), (hand_x - 16, hand_y - 2), (hand_x - 14, hand_y + 3)], fill=c_blade)
            draw.line([(hand_x, hand_y), (hand_x - 18, hand_y - 2)], fill=(255, 255, 200, 220), width=2)
        else:
            draw.polygon([(hand_x, hand_y), (hand_x - 10, hand_y - 2), (hand_x - 8, hand_y + 2)], fill=c_blade)

    elif row == 2:  # Right
        # Profile Eyes
        draw.ellipse([cx + 4, cy - 12, cx + 8, cy - 8], fill=c_eye)
        # Dagger thrust right
        hand_x, hand_y = cx + 10, cy + 4
        if col == 3:
            draw.polygon([(hand_x, hand_y), (hand_x + 16, hand_y - 2), (hand_x + 14, hand_y + 3)], fill=c_blade)
            draw.line([(hand_x, hand_y), (hand_x + 18, hand_y - 2)], fill=(255, 255, 200, 220), width=2)
        else:
            draw.polygon([(hand_x, hand_y), (hand_x + 10, hand_y - 2), (hand_x + 8, hand_y + 2)], fill=c_blade)

    elif row == 3:  # Up
        # Back of head & vest
        draw.line([(cx - 6, cy - 6), (cx + 6, cy - 6)], fill=c_vest_dark, width=2)

    return normalize_and_center_cell(img)


# -----------------------------------------------------------------------------
# MONSTER 3: Skeleton Warrior
# -----------------------------------------------------------------------------
def draw_skeleton_frame(row, col):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    c_bone = (235, 230, 210, 255)
    c_bone_dark = (150, 145, 130, 255)
    c_outline = (60, 55, 45, 255)
    c_socket = (20, 18, 18, 255)
    c_red_eye = (235, 40, 40, 255)

    # Shield colors
    c_shield_rim = (175, 190, 205, 255)
    c_shield_fill = (90, 105, 120, 255)
    c_boss = (220, 175, 40, 255)

    # Sword colors
    c_blade = (200, 215, 235, 255)
    c_hilt = (180, 135, 35, 255)

    cx, cy = 32, 32
    create_drop_shadow(draw, cx, cy + 18, rx=13, ry=5)

    # Walk legs
    l_leg_x, r_leg_x = cx - 5, cx + 5
    if col == 0:
        l_leg_x -= 2
    elif col == 2:
        r_leg_x += 2

    # Leg bones
    draw.line([(cx - 5, cy + 8), (l_leg_x, cy + 18)], fill=c_bone, width=3)
    draw.line([(cx + 5, cy + 8), (r_leg_x, cy + 18)], fill=c_bone, width=3)

    # Spine & Ribcage
    draw.line([(cx, cy - 4), (cx, cy + 8)], fill=c_bone_dark, width=3)
    for ry in range(cy - 2, cy + 6, 3):
        draw.line([(cx - 6, ry), (cx + 6, ry)], fill=c_bone, width=2)

    # Skull
    skull_bbox = [cx - 8, cy - 18, cx + 8, cy - 4]
    draw.ellipse(skull_bbox, fill=c_bone, outline=c_outline)
    # Teeth jaw
    draw.rectangle([cx - 4, cy - 5, cx + 4, cy - 2], fill=c_bone_dark)

    # Directional facial & weapon features
    if row == 0:  # Down
        # Eye sockets
        draw.ellipse([cx - 6, cy - 14, cx - 2, cy - 9], fill=c_socket)
        draw.ellipse([cx + 2, cy - 14, cx + 6, cy - 9], fill=c_socket)
        # Red pupil glow
        draw.point((cx - 4, cy - 11), fill=c_red_eye)
        draw.point((cx + 4, cy - 11), fill=c_red_eye)

        # Shield on left arm
        sx, sy = cx - 13, cy + 2
        draw.ellipse([sx - 8, sy - 8, sx + 8, sy + 8], fill=c_shield_fill, outline=c_shield_rim)
        draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=c_boss)

        # Sword in right arm
        hx, hy = cx + 12, cy + 4
        draw.line([(hx - 3, hy), (hx + 3, hy)], fill=c_hilt, width=2)
        if col == 3:  # Attack swing
            draw.polygon([(hx, hy), (hx + 14, hy - 14), (hx + 18, hy - 10)], fill=c_blade)
            draw.arc([hx, hy - 16, hx + 20, hy + 4], 180, 330, fill=(200, 230, 255, 220), width=3)
        else:
            draw.line([(hx, hy), (hx + 8, hy - 12)], fill=c_blade, width=3)

    elif row == 1:  # Left
        # Eye socket side
        draw.ellipse([cx - 6, cy - 14, cx - 2, cy - 9], fill=c_socket)
        draw.point((cx - 4, cy - 11), fill=c_red_eye)
        # Shield forward
        sx, sy = cx - 12, cy + 2
        draw.ellipse([sx - 6, sy - 8, sx + 6, sy + 8], fill=c_shield_fill, outline=c_shield_rim)
        draw.ellipse([sx - 2, sy - 3, sx + 2, sy + 3], fill=c_boss)

    elif row == 2:  # Right
        # Eye socket side
        draw.ellipse([cx + 2, cy - 14, cx + 6, cy - 9], fill=c_socket)
        draw.point((cx + 4, cy - 11), fill=c_red_eye)
        # Sword forward
        hx, hy = cx + 10, cy + 4
        if col == 3:
            draw.polygon([(hx, hy), (hx + 16, hy - 2), (hx + 14, hy + 4)], fill=c_blade)
        else:
            draw.line([(hx, hy), (hx + 10, hy - 8)], fill=c_blade, width=3)

    elif row == 3:  # Up
        # Back of skull
        draw.ellipse([cx - 7, cy - 16, cx + 7, cy - 6], fill=c_bone)

    return normalize_and_center_cell(img)


# -----------------------------------------------------------------------------
# MONSTER 4: Boss Baphomet
# -----------------------------------------------------------------------------
def draw_boss_baphomet_frame(row, col):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    c_fur = (45, 35, 55, 255)
    c_fur_dark = (25, 20, 35, 255)
    c_horn = (225, 175, 45, 255)
    c_horn_dark = (130, 95, 25, 255)
    c_eye_glow = (255, 30, 30, 255)
    c_cloth = (180, 30, 40, 255)
    c_scythe_handle = (110, 70, 35, 255)
    c_scythe_blade = (190, 50, 120, 255)

    cx, cy = 32, 32
    create_drop_shadow(draw, cx, cy + 20, rx=18, ry=6)

    # Large demonic torso & head
    draw.polygon([(cx - 12, cy - 6), (cx + 12, cy - 6), (cx + 9, cy + 12), (cx - 9, cy + 12)], fill=c_fur, outline=c_fur_dark)
    # Loincloth
    draw.polygon([(cx - 7, cy + 8), (cx + 7, cy + 8), (cx + 5, cy + 18), (cx - 5, cy + 18)], fill=c_cloth)

    # Goat Head
    draw.ellipse([cx - 9, cy - 18, cx + 9, cy - 2], fill=c_fur, outline=c_fur_dark)
    # Goat Snout
    draw.polygon([(cx - 4, cy - 6), (cx + 4, cy - 6), (cx, cy + 1)], fill=c_fur_dark)

    # Huge Golden Curved Horns
    # Left Horn
    draw.polygon([(cx - 6, cy - 14), (cx - 20, cy - 24), (cx - 16, cy - 8)], fill=c_horn, outline=c_horn_dark)
    # Right Horn
    draw.polygon([(cx + 6, cy - 14), (cx + 20, cy - 24), (cx + 16, cy - 8)], fill=c_horn, outline=c_horn_dark)

    # Directional features & Scythe
    if row == 0:  # Down
        # Crimson Eyes
        draw.ellipse([cx - 6, cy - 12, cx - 2, cy - 8], fill=c_eye_glow)
        draw.ellipse([cx + 2, cy - 12, cx + 6, cy - 8], fill=c_eye_glow)

        # Scythe weapon
        handle_x = cx + 14
        draw.line([(handle_x, cy - 20), (handle_x, cy + 18)], fill=c_scythe_handle, width=3)
        # Scythe Blade
        draw.polygon([(handle_x, cy - 18), (handle_x + 16, cy - 24), (handle_x + 10, cy - 12)], fill=c_scythe_blade)

        if col == 3:  # Attack slash arc
            draw.arc([cx - 20, cy - 20, cx + 22, cy + 18], 160, 340, fill=(255, 60, 120, 220), width=4)

    elif row == 1:  # Left
        draw.ellipse([cx - 7, cy - 12, cx - 3, cy - 8], fill=c_eye_glow)
        # Scythe held left
        draw.line([(cx - 10, cy - 18), (cx - 10, cy + 16)], fill=c_scythe_handle, width=3)
        draw.polygon([(cx - 10, cy - 16), (cx - 24, cy - 22), (cx - 18, cy - 10)], fill=c_scythe_blade)

    elif row == 2:  # Right
        draw.ellipse([cx + 3, cy - 12, cx + 7, cy - 8], fill=c_eye_glow)
        # Scythe held right
        draw.line([(cx + 10, cy - 18), (cx + 10, cy + 16)], fill=c_scythe_handle, width=3)
        draw.polygon([(cx + 10, cy - 16), (cx + 24, cy - 22), (cx + 18, cy - 10)], fill=c_scythe_blade)

    elif row == 3:  # Up
        # Back of head & furry back
        draw.polygon([(cx - 8, cy - 16), (cx + 8, cy - 16), (cx, cy - 4)], fill=c_fur_dark)

    return normalize_and_center_cell(img)


# -----------------------------------------------------------------------------
# MONSTER 5: Cactuar
# -----------------------------------------------------------------------------
def draw_cactuar_frame(row, col):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    c_cactus = (40, 180, 70, 255)
    c_cactus_dark = (20, 115, 45, 255)
    c_needle = (225, 245, 65, 255)
    c_stitch = (15, 20, 15, 255)

    cx, cy = 32, 32
    create_drop_shadow(draw, cx, cy + 18, rx=12, ry=4)

    # Main Cactus Pillar Body
    draw.rectangle([cx - 8, cy - 14, cx + 8, cy + 12], fill=c_cactus, outline=c_cactus_dark)
    # Rounded top head
    draw.ellipse([cx - 8, cy - 18, cx + 8, cy - 10], fill=c_cactus, outline=c_cactus_dark)

    # 3 Needle Spines on top head
    draw.polygon([(cx - 4, cy - 16), (cx - 7, cy - 24), (cx - 2, cy - 17)], fill=c_needle)
    draw.polygon([(cx - 1, cy - 17), (cx, cy - 26), (cx + 1, cy - 17)], fill=c_needle)
    draw.polygon([(cx + 2, cy - 17), (cx + 7, cy - 24), (cx + 4, cy - 16)], fill=c_needle)

    # Arm & Leg Right-Angle Poses (Signature Cactuar!)
    if col == 0:  # Walk0
        # Right angle arms
        draw.line([(cx - 8, cy - 4), (cx - 16, cy - 4), (cx - 16, cy - 12)], fill=c_cactus, width=4)
        draw.line([(cx + 8, cy + 2), (cx + 16, cy + 2), (cx + 16, cy + 10)], fill=c_cactus, width=4)
    elif col == 1 or col == 3:  # Idle / Attack
        draw.line([(cx - 8, cy - 4), (cx - 15, cy - 4), (cx - 15, cy - 12)], fill=c_cactus, width=4)
        draw.line([(cx + 8, cy - 4), (cx + 15, cy - 4), (cx + 15, cy + 4)], fill=c_cactus, width=4)
    elif col == 2:  # Walk1
        draw.line([(cx - 8, cy + 2), (cx - 16, cy + 2), (cx - 16, cy + 10)], fill=c_cactus, width=4)
        draw.line([(cx + 8, cy - 4), (cx + 16, cy - 4), (cx + 16, cy - 12)], fill=c_cactus, width=4)

    # Right-Angle Legs
    draw.line([(cx - 4, cy + 12), (cx - 4, cy + 18), (cx - 10, cy + 18)], fill=c_cactus, width=4)
    draw.line([(cx + 4, cy + 12), (cx + 4, cy + 18), (cx + 10, cy + 18)], fill=c_cactus, width=4)

    # Face Stitches
    if row == 0 or row == 1 or row == 2:  # Down/Left/Right
        # Eye stitches: |  |
        draw.line([(cx - 5, cy - 11), (cx - 5, cy - 5)], fill=c_stitch, width=2)
        draw.line([(cx + 5, cy - 11), (cx + 5, cy - 5)], fill=c_stitch, width=2)
        # Rectangular mouth stitch: [ O ]
        draw.rectangle([cx - 3, cy - 3, cx + 3, cy + 3], fill=c_stitch)

    # Attack pose: 1000 Needles discharge burst!
    if col == 3:
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            nx = cx + int(22 * math.cos(rad))
            ny = cy + int(22 * math.sin(rad))
            draw.line([(cx, cy), (nx, ny)], fill=c_needle, width=2)

    return normalize_and_center_cell(img)


# -----------------------------------------------------------------------------
# MONSTER 6: Bomb
# -----------------------------------------------------------------------------
def draw_bomb_frame(row, col):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    c_shell = (45, 48, 55, 255)
    c_shell_dark = (22, 24, 30, 255)
    c_hl = (90, 95, 110, 255)
    c_magma = (255, 110, 20, 255)
    c_core = (255, 230, 60, 255)
    c_fuse = (160, 115, 65, 255)
    c_spark = (255, 255, 200, 255)

    cx, cy = 32, 34
    create_drop_shadow(draw, cx, cy + 16, rx=15, ry=5)

    # Attack pose: Body turns glowing hot red-orange!
    if col == 3:
        c_shell = (240, 80, 25, 255)
        c_magma = (255, 220, 40, 255)
        # Flame aura around bomb
        draw.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=(255, 100, 0, 100))

    # Bomb Spherical Body
    body_bbox = [cx - 18, cy - 18, cx + 18, cy + 18]
    draw.ellipse(body_bbox, fill=c_shell, outline=c_shell_dark)
    # Metallic top highlight
    draw.ellipse([cx - 14, cy - 15, cx - 4, cy - 8], fill=c_hl)

    # Coiled Fuse on top
    draw.arc([cx - 4, cy - 26, cx + 8, cy - 16], 180, 360, fill=c_fuse, width=3)
    # Lit Spark
    draw.ellipse([cx + 5, cy - 27, cx + 11, cy - 21], fill=c_spark)
    draw.ellipse([cx + 3, cy - 29, cx + 13, cy - 19], fill=(255, 160, 30, 180))

    # Fiery Glowing Face & Magma Cracks
    if row == 0 or row == 1 or row == 2:  # Down / Side
        # Angry glowing eyes
        draw.polygon([(cx - 12, cy - 6), (cx - 4, cy - 2), (cx - 10, cy + 2)], fill=c_magma)
        draw.polygon([(cx + 12, cy - 6), (cx + 4, cy - 2), (cx + 10, cy + 2)], fill=c_magma)
        draw.point((cx - 8, cy - 3), fill=c_core)
        draw.point((cx + 8, cy - 3), fill=c_core)

        # Fiery mouth gap
        draw.polygon([(cx - 6, cy + 5), (cx + 6, cy + 5), (cx, cy + 11)], fill=c_magma)

    elif row == 3:  # Up
        # Back of bomb: Magma vein cracks across shell
        draw.line([(cx - 8, cy - 4), (cx, cy + 4), (cx + 8, cy - 2)], fill=c_magma, width=2)

    return normalize_and_center_cell(img)


# -----------------------------------------------------------------------------
# SHEET GENERATOR & VERIFICATION
# -----------------------------------------------------------------------------
MONSTER_GENERATORS = {
    "slime_green_ff.png": draw_slime_frame,
    "goblin_ff.png": draw_goblin_frame,
    "skeleton_ff.png": draw_skeleton_frame,
    "boss_baphomet_ff.png": draw_boss_baphomet_frame,
    "cactuar_ff.png": draw_cactuar_frame,
    "bomb_ff.png": draw_bomb_frame,
}

def generate_all_monsters():
    print("=== Generating Clean Monster Sprite Sheets ===")
    
    for filename, drawer in MONSTER_GENERATORS.items():
        sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
        
        # 4 rows (0=Down, 1=Left, 2=Right, 3=Up) x 4 cols (0=Walk0, 1=Idle, 2=Walk1, 3=Attack)
        for row in range(4):
            for col in range(4):
                cell_img = drawer(row, col)
                sheet.paste(cell_img, (col * 64, row * 64))

        # Save to target directories
        for d in TARGET_DIRS:
            os.makedirs(d, exist_ok=True)
            out_path = os.path.join(d, filename)
            sheet.save(out_path, "PNG")
            print(f"Saved: {out_path} (256x256 RGBA)")

    print("\n=== Running Slicing & Centering Verification ===")
    all_passed = True
    
    for filename in MONSTER_GENERATORS.keys():
        for d in TARGET_DIRS:
            out_path = os.path.join(d, filename)
            assert os.path.exists(out_path), f"File missing: {out_path}"
            
            sheet = Image.open(out_path)
            assert sheet.size == (256, 256) and sheet.mode == "RGBA", f"Invalid sheet specs: {sheet.size} {sheet.mode}"

            # Check cell (0,0) specifically as requested by prompt
            cell_0_0 = sheet.crop((0, 0, 64, 64))
            bbox_0_0 = cell_0_0.getbbox()
            assert bbox_0_0 is not None, f"Cell (0,0) is empty in {filename}!"
            
            w0 = bbox_0_0[2] - bbox_0_0[0]
            h0 = bbox_0_0[3] - bbox_0_0[1]
            cx0 = (bbox_0_0[0] + bbox_0_0[2]) / 2.0
            cy0 = (bbox_0_0[1] + bbox_0_0[3]) / 2.0

            # Verify ALL 16 cells in the sheet
            for r in range(4):
                for c in range(4):
                    cell = sheet.crop((c * 64, r * 64, (c + 1) * 64, (r + 1) * 64))
                    bbox = cell.getbbox()
                    assert bbox is not None, f"Empty cell at ({c},{r}) in {filename}"
                    w = bbox[2] - bbox[0]
                    h = bbox[3] - bbox[1]
                    cx = (bbox[0] + bbox[2]) / 2.0
                    cy = (bbox[1] + bbox[3]) / 2.0

                    if not (44 <= w <= 52 and 44 <= h <= 52 and 31.0 <= cx <= 33.0 and 31.0 <= cy <= 33.0):
                        print(f"WARNING: Cell ({c},{r}) specs: w={w}, h={h}, center=({cx},{cy})")
                        all_passed = False

            print(f"CONFIRMED: {filename} in {os.path.basename(os.path.dirname(d))}/{os.path.basename(d)} - Cell (0,0) contains EXACTLY 1 centered monster sprite ({w0}x{h0} bounds at ({cx0},{cy0}) with alpha background)!")

    if all_passed:
        print("\nALL MONSTER SPRITE SHEETS SUCCESSFULLY GENERATED AND VERIFIED 100%!")
    else:
        print("\nGeneration complete with warnings.")


if __name__ == "__main__":
    generate_all_monsters()
