import os
from PIL import Image, ImageDraw

def ensure_dirs():
    project_root = r"D:\ai-studio\Zaggers"
    dirs = [
        os.path.join(project_root, "assets", "sprites_ff"),
        os.path.join(project_root, "web", "assets", "sprites_ff")
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    return dirs

def save_sprite(img, name, dirs):
    for d in dirs:
        path = os.path.join(d, name)
        img.save(path, "PNG")
        print(f"Saved 16-bit JRPG Sprite: {path} ({img.size[0]}x{img.size[1]})")

OUTLINE = (18, 24, 36, 255)
SKIN_LIGHT = (255, 225, 195, 255)
SKIN_BASE  = (245, 200, 165, 255)
SKIN_SHADOW= (210, 160, 125, 255)
EYE_DARK   = (20, 30, 45, 255)
WHITE_SPEC = (255, 255, 255, 255)

def draw_shadow(draw, cy):
    draw.ellipse([18, 52 + cy, 46, 59 + cy], fill=(0, 0, 0, 90))

# --- 1. KNIGHT ---
def draw_knight(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    STEEL_SPEC  = (245, 250, 255, 255)
    STEEL_LIGHT = (210, 222, 238, 255)
    STEEL_BASE  = (160, 175, 195, 255)
    STEEL_SHADOW= (105, 118, 140, 255)
    CAPE_BLUE   = (35, 80, 175, 255)
    CAPE_LIGHT  = (65, 115, 215, 255)
    GOLD_TRIM   = (235, 190, 50, 255)

    draw_shadow(draw, cy)

    if row == 3: # Back view
        draw.polygon([(14, 22 + cy), (50, 22 + cy), (54, 55 + cy), (10, 55 + cy)], fill=CAPE_BLUE, outline=OUTLINE)
        draw.polygon([(36, 26 + cy), (50, 22 + cy), (52, 53 + cy), (42, 55 + cy)], fill=CAPE_LIGHT)
        lx1, lx2 = 23 + leg, 29 + leg
        rx1, rx2 = 35 - leg, 41 - leg
        draw.rectangle([lx1, 46 + cy, lx2, 55 + cy], fill=STEEL_SHADOW, outline=OUTLINE)
        draw.rectangle([rx1, 46 + cy, rx2, 55 + cy], fill=STEEL_SHADOW, outline=OUTLINE)
        draw.rectangle([21, 12 + cy, 43, 27 + cy], fill=STEEL_BASE, outline=OUTLINE)
        draw.line([(32, 12 + cy), (32, 27 + cy)], fill=GOLD_TRIM, width=2)
    else:
        draw.polygon([(14, 24 + cy), (48, 24 + cy), (52, 53 + cy), (12, 53 + cy)], fill=CAPE_BLUE, outline=OUTLINE)
        lx1, lx2 = 23 + leg, 29 + leg
        rx1, rx2 = 35 - leg, 41 - leg
        draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=STEEL_SHADOW, outline=OUTLINE)
        draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=STEEL_SHADOW, outline=OUTLINE)
        draw.rectangle([lx1 + 1, 45 + cy, lx2 - 1, 53 + cy], fill=STEEL_BASE)
        draw.rectangle([rx1 + 1, 45 + cy, rx2 - 1, 53 + cy], fill=STEEL_BASE)

        draw.rectangle([21, 26 + cy, 43, 44 + cy], fill=STEEL_BASE, outline=OUTLINE)
        draw.rectangle([24, 28 + cy, 40, 42 + cy], fill=STEEL_LIGHT)
        draw.rectangle([26, 29 + cy, 32, 39 + cy], fill=STEEL_SPEC)
        draw.rectangle([21, 40 + cy, 43, 43 + cy], fill=GOLD_TRIM, outline=OUTLINE)

        draw.polygon([(15, 25 + cy), (22, 27 + cy), (20, 36 + cy), (13, 32 + cy)], fill=STEEL_LIGHT, outline=OUTLINE)
        draw.polygon([(49, 25 + cy), (42, 27 + cy), (44, 36 + cy), (51, 32 + cy)], fill=STEEL_LIGHT, outline=OUTLINE)

        draw.rectangle([21, 12 + cy, 43, 27 + cy], fill=STEEL_BASE, outline=OUTLINE)
        draw.rectangle([24, 14 + cy, 40, 25 + cy], fill=STEEL_LIGHT)
        draw.rectangle([24, 19 + cy, 40, 23 + cy], fill=OUTLINE)
        draw.line([(26, 21 + cy), (38, 21 + cy)], fill=STEEL_SPEC, width=1)

        wx = 50 if (row == 0 or row == 2) else 14
        draw.line([(wx, 8 + cy), (wx, 48 + cy)], fill=STEEL_LIGHT, width=3)
        draw.polygon([(wx, 4 + cy), (wx - 4, 12 + cy), (wx + 4, 12 + cy)], fill=STEEL_SPEC)
        draw.rectangle([wx - 5, 38 + cy, wx + 5, 41 + cy], fill=GOLD_TRIM, outline=OUTLINE)

# --- 2. BLACK MAGE ---
def draw_blackmage(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    cy = bob

    ROBE_BLUE  = (35, 75, 175, 255)
    ROBE_LIGHT = (65, 115, 215, 255)
    HAT_YELLOW = (235, 185, 30, 255)
    HAT_SHADOW = (185, 135, 15, 255)
    GLOW_EYE   = (255, 220, 30, 255)
    STAFF_WOOD = (115, 70, 30, 255)

    draw_shadow(draw, cy)
    draw.polygon([(18, 30 + cy), (46, 30 + cy), (50, 55 + cy), (14, 55 + cy)], fill=ROBE_BLUE, outline=OUTLINE)
    draw.polygon([(36, 32 + cy), (46, 30 + cy), (44, 48 + cy)], fill=ROBE_LIGHT)

    draw.rectangle([23, 16 + cy, 41, 28 + cy], fill=OUTLINE)
    sway = 1 if (col == 1 or col == 3) else 0
    draw.polygon([(14, 16 + cy), (50, 16 + cy), (32 + sway, -4 + cy)], fill=HAT_YELLOW, outline=OUTLINE)
    draw.polygon([(14, 16 + cy), (32 + sway, 16 + cy), (32 + sway, -4 + cy)], fill=HAT_SHADOW)
    draw.rectangle([12, 14 + cy, 52, 18 + cy], fill=HAT_YELLOW, outline=OUTLINE)

    if row == 0:
        draw.rectangle([25, 20 + cy, 29, 24 + cy], fill=GLOW_EYE)
        draw.rectangle([35, 20 + cy, 39, 24 + cy], fill=GLOW_EYE)

    wx = 52 if (row == 0 or row == 2) else 12
    draw.line([(wx, 10 + cy), (wx, 54 + cy)], fill=STAFF_WOOD, width=4)
    draw.ellipse([wx - 6, 4 + cy, wx + 6, 16 + cy], fill=GLOW_EYE, outline=OUTLINE)

# --- 3. THIEF ---
def draw_thief(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    EMERALD_BASE = (30, 130, 65, 255)
    EMERALD_LIGHT= (55, 175, 95, 255)
    LEATHER_BASE = (125, 75, 38, 255)
    LEATHER_LIGHT= (160, 105, 58, 255)
    STEEL_LIGHT  = (225, 238, 245, 255)

    draw_shadow(draw, cy)

    if row == 3:
        draw.polygon([(18, 12 + cy), (46, 12 + cy), (50, 52 + cy), (14, 52 + cy)], fill=EMERALD_BASE, outline=OUTLINE)
        lx1, lx2 = 23 + leg, 29 + leg
        rx1, rx2 = 35 - leg, 41 - leg
        draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=LEATHER_BASE, outline=OUTLINE)
        draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=LEATHER_BASE, outline=OUTLINE)
    else:
        lx1, lx2 = 23 + leg, 29 + leg
        rx1, rx2 = 35 - leg, 41 - leg
        draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=LEATHER_BASE, outline=OUTLINE)
        draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=LEATHER_BASE, outline=OUTLINE)

        draw.rectangle([21, 26 + cy, 43, 44 + cy], fill=LEATHER_BASE, outline=OUTLINE)
        draw.rectangle([25, 28 + cy, 39, 41 + cy], fill=LEATHER_LIGHT)

        draw.polygon([(18, 12 + cy), (46, 12 + cy), (44, 28 + cy), (20, 28 + cy)], fill=EMERALD_BASE, outline=OUTLINE)
        draw.polygon([(20, 14 + cy), (44, 14 + cy), (42, 26 + cy)], fill=EMERALD_LIGHT)
        draw.rectangle([24, 17 + cy, 40, 26 + cy], fill=SKIN_BASE)

        if row == 0:
            draw.rectangle([26, 20 + cy, 28, 23 + cy], fill=EYE_DARK)
            draw.rectangle([36, 20 + cy, 38, 23 + cy], fill=EYE_DARK)

        draw.line([(12, 26 + cy), (12, 44 + cy)], fill=STEEL_LIGHT, width=2)
        draw.line([(52, 26 + cy), (52, 44 + cy)], fill=STEEL_LIGHT, width=2)

# --- 4. WHITE MAGE ---
def draw_whitemage(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    cy = bob

    ROBE_WHITE = (245, 245, 250, 255)
    ROBE_SHADOW= (195, 200, 215, 255)
    RED_HEM    = (220, 45, 55, 255)
    HAIR_GOLD  = (240, 200, 60, 255)
    STAFF_GOLD = (235, 190, 50, 255)

    draw_shadow(draw, cy)
    draw.polygon([(18, 30 + cy), (46, 30 + cy), (50, 55 + cy), (14, 55 + cy)], fill=ROBE_WHITE, outline=OUTLINE)
    draw.polygon([(18, 30 + cy), (32, 55 + cy), (14, 55 + cy)], fill=ROBE_SHADOW)

    for tx in range(16, 48, 8):
        draw.polygon([(tx, 54 + cy), (tx + 4, 46 + cy), (tx + 8, 54 + cy)], fill=RED_HEM)

    draw.polygon([(18, 12 + cy), (46, 12 + cy), (44, 27 + cy), (20, 27 + cy)], fill=ROBE_WHITE, outline=OUTLINE)
    draw.rectangle([24, 16 + cy, 40, 26 + cy], fill=SKIN_BASE)
    draw.rectangle([22, 12 + cy, 42, 17 + cy], fill=HAIR_GOLD)

    if row == 0:
        draw.rectangle([26, 20 + cy, 28, 23 + cy], fill=EYE_DARK)
        draw.rectangle([36, 20 + cy, 38, 23 + cy], fill=EYE_DARK)

    wx = 52 if (row == 0 or row == 2) else 12
    draw.line([(wx, 12 + cy), (wx, 54 + cy)], fill=STAFF_GOLD, width=3)
    draw.ellipse([wx - 4, 6 + cy, wx + 4, 14 + cy], fill=WHITE_SPEC, outline=OUTLINE)

# --- 5. RED MAGE ---
def draw_redmage(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    RED_DOUBLET = (205, 45, 65, 255)
    RED_SHADOW  = (145, 20, 35, 255)
    CAP_RED     = (185, 30, 45, 255)
    FEATHER_W   = (250, 250, 255, 255)
    STEEL_RAPIER= (220, 230, 245, 255)

    draw_shadow(draw, cy)
    lx1, lx2 = 23 + leg, 29 + leg
    rx1, rx2 = 35 - leg, 41 - leg
    draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=RED_SHADOW, outline=OUTLINE)
    draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=RED_SHADOW, outline=OUTLINE)

    draw.rectangle([21, 26 + cy, 43, 44 + cy], fill=RED_DOUBLET, outline=OUTLINE)
    draw.line([(32, 26 + cy), (32, 44 + cy)], fill=(240, 200, 50, 255), width=2)

    draw.rectangle([23, 14 + cy, 41, 28 + cy], fill=SKIN_BASE, outline=OUTLINE)
    draw.polygon([(16, 10 + cy), (48, 10 + cy), (42, 17 + cy), (22, 17 + cy)], fill=CAP_RED, outline=OUTLINE)
    draw.polygon([(10, 2 + cy), (20, 8 + cy), (16, 16 + cy)], fill=FEATHER_W, outline=OUTLINE)

    if row == 0:
        draw.rectangle([26, 21 + cy, 28, 24 + cy], fill=EYE_DARK)
        draw.rectangle([36, 21 + cy, 38, 24 + cy], fill=EYE_DARK)

    draw.line([(50, 14 + cy), (50, 48 + cy)], fill=STEEL_RAPIER, width=2)
    draw.ellipse([46, 38 + cy, 54, 44 + cy], fill=(240, 200, 50, 255), outline=OUTLINE)

# --- 6. RANGER ---
def draw_ranger(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    CLOAK_GREEN  = (40, 125, 65, 255)
    LEATHER_BROWN= (135, 75, 35, 255)
    BOW_WOOD     = (165, 100, 45, 255)

    draw_shadow(draw, cy)
    lx1, lx2 = 23 + leg, 29 + leg
    rx1, rx2 = 35 - leg, 41 - leg
    draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=CLOAK_GREEN, outline=OUTLINE)
    draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=CLOAK_GREEN, outline=OUTLINE)

    draw.rectangle([21, 26 + cy, 43, 44 + cy], fill=LEATHER_BROWN, outline=OUTLINE)
    draw.polygon([(18, 12 + cy), (46, 12 + cy), (44, 27 + cy), (20, 27 + cy)], fill=CLOAK_GREEN, outline=OUTLINE)
    draw.rectangle([24, 16 + cy, 40, 26 + cy], fill=SKIN_BASE)

    if row == 0:
        draw.rectangle([26, 20 + cy, 28, 23 + cy], fill=EYE_DARK)
        draw.rectangle([36, 20 + cy, 38, 23 + cy], fill=EYE_DARK)

    draw.arc([42, 14 + cy, 56, 46 + cy], 270, 90, fill=BOW_WOOD, width=3)
    draw.line([(49, 14 + cy), (49, 46 + cy)], fill=WHITE_SPEC, width=1)

# Import individual drawing functions for Dragoon, Monk, Paladin, Sage, Bard, Alchemist
from generate_class_dragoon import draw_dragoon_frame
from generate_class_monk import draw_monk_frame
from generate_class_paladin import draw_paladin_frame
from generate_class_sage import draw_sage_frame
from generate_class_bard import draw_bard_frame
from generate_class_alchemist import draw_alchemist_frame

def generate_all_hd_sprites():
    dirs = ensure_dirs()
    classes_map = [
        ("hero_knight.png", draw_knight),
        ("hero_blackmage.png", draw_blackmage),
        ("hero_thief.png", draw_thief),
        ("hero_whitemage.png", draw_whitemage),
        ("hero_redmage.png", draw_redmage),
        ("hero_ranger.png", draw_ranger),
        ("hero_dragoon.png", draw_dragoon_frame),
        ("hero_monk.png", draw_monk_frame),
        ("hero_paladin.png", draw_paladin_frame),
        ("hero_sage.png", draw_sage_frame),
        ("hero_bard.png", draw_bard_frame),
        ("hero_alchemist.png", draw_alchemist_frame),
    ]

    for filename, func in classes_map:
        sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
        for row in range(4):
            for col in range(4):
                frame = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
                draw = ImageDraw.Draw(frame)
                func(draw, row, col)
                sheet.paste(frame, (col * 64, row * 64))
        save_sprite(sheet, filename, dirs)

if __name__ == "__main__":
    generate_all_hd_sprites()
