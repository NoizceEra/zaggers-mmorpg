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
        print(f"Saved Hero Sprite: {path} ({img.size[0]}x{img.size[1]})")

OUTLINE = (14, 18, 24, 255)
SKIN_BASE = (245, 200, 165, 255)
SKIN_SHADOW = (210, 160, 125, 255)
EYE_DARK = (20, 30, 45, 255)
WHITE = (255, 255, 255, 255)

def draw_shadow(draw, cy):
    draw.ellipse([18, 52 + cy, 46, 59 + cy], fill=(0, 0, 0, 90))

# --- 1. KNIGHT ---
def draw_knight(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    STEEL = (180, 190, 205, 255)
    STEEL_LIGHT = (220, 230, 245, 255)
    STEEL_DARK = (110, 120, 135, 255)
    BLUE_CAPE = (40, 85, 175, 255)
    BLUE_DARK = (25, 55, 120, 255)
    GOLD_TRIM = (235, 190, 50, 255)

    draw_shadow(draw, cy)
    # Cape
    draw.polygon([(16, 24 + cy), (48, 24 + cy), (51, 54 + cy), (13, 54 + cy)], fill=BLUE_CAPE, outline=OUTLINE)
    draw.polygon([(16, 24 + cy), (32, 54 + cy), (13, 54 + cy)], fill=BLUE_DARK)

    # Legs
    lx1, lx2 = 23 + leg, 29 + leg
    rx1, rx2 = 35 - leg, 41 - leg
    draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=STEEL_DARK, outline=OUTLINE)
    draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=STEEL_DARK, outline=OUTLINE)
    draw.rectangle([lx1 + 1, 45 + cy, lx2 - 1, 53 + cy], fill=STEEL)
    draw.rectangle([rx1 + 1, 45 + cy, rx2 - 1, 53 + cy], fill=STEEL)

    # Cuirass
    draw.rectangle([21, 26 + cy, 43, 44 + cy], fill=STEEL, outline=OUTLINE)
    draw.rectangle([25, 28 + cy, 39, 42 + cy], fill=STEEL_LIGHT)
    draw.rectangle([23, 38 + cy, 41, 41 + cy], fill=GOLD_TRIM)

    # Pauldrons
    draw.polygon([(15, 26 + cy), (22, 28 + cy), (20, 36 + cy), (13, 32 + cy)], fill=STEEL_LIGHT, outline=OUTLINE)
    draw.polygon([(49, 26 + cy), (42, 28 + cy), (44, 36 + cy), (51, 32 + cy)], fill=STEEL_LIGHT, outline=OUTLINE)

    # Helm & Visor
    draw.rectangle([21, 12 + cy, 43, 27 + cy], fill=STEEL, outline=OUTLINE)
    draw.rectangle([24, 14 + cy, 40, 25 + cy], fill=STEEL_LIGHT)
    if row != 3:
        draw.rectangle([24, 19 + cy, 40, 23 + cy], fill=OUTLINE)
        draw.line([(26, 21 + cy), (38, 21 + cy)], fill=STEEL_LIGHT, width=1)

    # Sword
    wx = 50 if (row == 0 or row == 2) else 14
    draw.line([(wx, 12 + cy), (wx, 48 + cy)], fill=STEEL_LIGHT, width=3)
    draw.polygon([(wx, 6 + cy), (wx - 4, 14 + cy), (wx + 4, 14 + cy)], fill=WHITE)
    draw.rectangle([wx - 4, 38 + cy, wx + 4, 41 + cy], fill=GOLD_TRIM, outline=OUTLINE)


# --- 2. BLACK MAGE ---
def draw_blackmage(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    ROBE_BLUE = (35, 75, 175, 255)
    ROBE_LIGHT = (65, 115, 215, 255)
    HAT_YELLOW = (235, 195, 45, 255)
    HAT_SHADOW = (185, 145, 25, 255)
    EYE_GLOW = (255, 235, 60, 255)
    STAFF_WOOD = (120, 70, 35, 255)

    draw_shadow(draw, cy)
    # Robe
    draw.polygon([(18, 30 + cy), (46, 30 + cy), (50, 55 + cy), (14, 55 + cy)], fill=ROBE_BLUE, outline=OUTLINE)
    draw.polygon([(18, 30 + cy), (32, 55 + cy), (14, 55 + cy)], fill=ROBE_LIGHT)

    # Shadow Face & Yellow Wizard Hat
    draw.rectangle([23, 16 + cy, 41, 28 + cy], fill=OUTLINE) # Pitch-black shadow face
    draw.polygon([(16, 16 + cy), (48, 16 + cy), (32, -4 + cy)], fill=HAT_YELLOW, outline=OUTLINE)
    draw.polygon([(16, 16 + cy), (32, 16 + cy), (32, -4 + cy)], fill=HAT_SHADOW)
    draw.rectangle([14, 14 + cy, 50, 18 + cy], fill=HAT_YELLOW, outline=OUTLINE) # Hat brim

    if row == 0: # Glowing eyes
        draw.rectangle([25, 20 + cy, 28, 24 + cy], fill=EYE_GLOW)
        draw.rectangle([36, 20 + cy, 39, 24 + cy], fill=EYE_GLOW)
    elif row == 1:
        draw.rectangle([24, 20 + cy, 27, 24 + cy], fill=EYE_GLOW)
    elif row == 2:
        draw.rectangle([37, 20 + cy, 40, 24 + cy], fill=EYE_GLOW)

    # Wizard Staff
    wx = 52 if (row == 0 or row == 2) else 12
    draw.line([(wx, 10 + cy), (wx, 54 + cy)], fill=STAFF_WOOD, width=3)
    draw.ellipse([wx - 5, 5 + cy, wx + 5, 15 + cy], fill=EYE_GLOW, outline=OUTLINE)


# --- 3. THIEF ---
def draw_thief(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    GREEN_CLOAK = (45, 135, 75, 255)
    GREEN_LIGHT = (75, 175, 105, 255)
    LEATHER_BROWN = (145, 85, 45, 255)
    DAGGER_STEEL = (220, 230, 240, 255)

    draw_shadow(draw, cy)
    # Trousers
    lx1, lx2 = 23 + leg, 29 + leg
    rx1, rx2 = 35 - leg, 41 - leg
    draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=LEATHER_BROWN, outline=OUTLINE)
    draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=LEATHER_BROWN, outline=OUTLINE)

    # Leather Vest & Green Hood
    draw.rectangle([21, 26 + cy, 43, 44 + cy], fill=LEATHER_BROWN, outline=OUTLINE)
    draw.polygon([(18, 12 + cy), (46, 12 + cy), (44, 27 + cy), (20, 27 + cy)], fill=GREEN_CLOAK, outline=OUTLINE)
    draw.rectangle([24, 16 + cy, 40, 26 + cy], fill=SKIN_BASE)

    if row == 0:
        draw.rectangle([26, 20 + cy, 28, 23 + cy], fill=EYE_DARK)
        draw.rectangle([36, 20 + cy, 38, 23 + cy], fill=EYE_DARK)

    # Dual Curved Daggers
    draw.line([(12, 28 + cy), (12, 44 + cy)], fill=DAGGER_STEEL, width=2)
    draw.line([(52, 28 + cy), (52, 44 + cy)], fill=DAGGER_STEEL, width=2)


# --- 4. WHITE MAGE ---
def draw_whitemage(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    cy = bob

    ROBE_WHITE = (245, 245, 250, 255)
    ROBE_SHADOW = (195, 200, 215, 255)
    RED_TRIANGLE = (220, 45, 55, 255)
    HAIR_GOLD = (240, 200, 60, 255)
    STAFF_GOLD = (235, 190, 50, 255)

    draw_shadow(draw, cy)
    # Cleric Robe
    draw.polygon([(18, 30 + cy), (46, 30 + cy), (50, 55 + cy), (14, 55 + cy)], fill=ROBE_WHITE, outline=OUTLINE)
    draw.polygon([(18, 30 + cy), (32, 55 + cy), (14, 55 + cy)], fill=ROBE_SHADOW)
    # Red Triangle Pattern Hem
    for tx in range(16, 48, 8):
        draw.polygon([(tx, 54 + cy), (tx + 4, 46 + cy), (tx + 8, 54 + cy)], fill=RED_TRIANGLE)

    # Cowl & Hair
    draw.polygon([(18, 12 + cy), (46, 12 + cy), (44, 27 + cy), (20, 27 + cy)], fill=ROBE_WHITE, outline=OUTLINE)
    draw.rectangle([24, 16 + cy, 40, 26 + cy], fill=SKIN_BASE)
    draw.rectangle([22, 12 + cy, 42, 17 + cy], fill=HAIR_GOLD)

    if row == 0:
        draw.rectangle([26, 20 + cy, 28, 23 + cy], fill=EYE_DARK)
        draw.rectangle([36, 20 + cy, 38, 23 + cy], fill=EYE_DARK)

    # Priest Wand
    wx = 52 if (row == 0 or row == 2) else 12
    draw.line([(wx, 12 + cy), (wx, 54 + cy)], fill=STAFF_GOLD, width=3)
    draw.ellipse([wx - 4, 6 + cy, wx + 4, 14 + cy], fill=WHITE, outline=OUTLINE)


# --- 5. RED MAGE ---
def draw_redmage(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    RED_DOUBLET = (205, 40, 55, 255)
    RED_SHADOW = (145, 20, 35, 255)
    CAP_RED = (185, 30, 45, 255)
    FEATHER_WHITE = (250, 250, 255, 255)
    STEEL_RAPIER = (220, 230, 245, 255)

    draw_shadow(draw, cy)
    # Trousers
    lx1, lx2 = 23 + leg, 29 + leg
    rx1, rx2 = 35 - leg, 41 - leg
    draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=RED_SHADOW, outline=OUTLINE)
    draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=RED_SHADOW, outline=OUTLINE)

    # Crimson Doublet
    draw.rectangle([21, 26 + cy, 43, 44 + cy], fill=RED_DOUBLET, outline=OUTLINE)
    draw.line([(32, 26 + cy), (32, 44 + cy)], fill=(240, 195, 50, 255), width=2)

    # Head & Feathered Chapeau Cap
    draw.rectangle([23, 14 + cy, 41, 28 + cy], fill=SKIN_BASE, outline=OUTLINE)
    draw.polygon([(16, 10 + cy), (48, 10 + cy), (42, 17 + cy), (22, 17 + cy)], fill=CAP_RED, outline=OUTLINE)
    draw.polygon([(10, 2 + cy), (20, 8 + cy), (16, 16 + cy)], fill=FEATHER_WHITE, outline=OUTLINE)

    if row == 0:
        draw.rectangle([26, 21 + cy, 28, 24 + cy], fill=EYE_DARK)
        draw.rectangle([36, 21 + cy, 38, 24 + cy], fill=EYE_DARK)

    # Rapier Weapon
    draw.line([(50, 14 + cy), (50, 48 + cy)], fill=STEEL_RAPIER, width=2)
    draw.ellipse([46, 38 + cy, 54, 44 + cy], fill=(240, 195, 50, 255), outline=OUTLINE)


# --- 6. RANGER ---
def draw_ranger(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    CLOAK_GREEN = (40, 125, 65, 255)
    LEATHER_BROWN = (135, 75, 35, 255)
    BOW_WOOD = (165, 100, 45, 255)

    draw_shadow(draw, cy)
    # Trousers
    lx1, lx2 = 23 + leg, 29 + leg
    rx1, rx2 = 35 - leg, 41 - leg
    draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=CLOAK_GREEN, outline=OUTLINE)
    draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=CLOAK_GREEN, outline=OUTLINE)

    # Leather Armor & Green Cloak
    draw.rectangle([21, 26 + cy, 43, 44 + cy], fill=LEATHER_BROWN, outline=OUTLINE)
    draw.polygon([(18, 12 + cy), (46, 12 + cy), (44, 27 + cy), (20, 27 + cy)], fill=CLOAK_GREEN, outline=OUTLINE)
    draw.rectangle([24, 16 + cy, 40, 26 + cy], fill=SKIN_BASE)

    if row == 0:
        draw.rectangle([26, 20 + cy, 28, 23 + cy], fill=EYE_DARK)
        draw.rectangle([36, 20 + cy, 38, 23 + cy], fill=EYE_DARK)

    # Longbow
    draw.arc([42, 14 + cy, 56, 46 + cy], 270, 90, fill=BOW_WOOD, width=3)
    draw.line([(49, 14 + cy), (49, 46 + cy)], fill=WHITE, width=1)


# Include the 6 upgraded specialist classes from generate_new_hero_sprites.py
from generate_new_hero_sprites import (
    draw_dragoon_frame, draw_monk_frame, draw_paladin_frame,
    draw_sage_frame, draw_bard_frame, draw_alchemist_frame
)

def generate_custom_hero_sheet(draw_func):
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    for row in range(4):
        for col in range(4):
            frame_img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame_img)
            draw_func(draw, row, col)
            sheet.paste(frame_img, (col * 64, row * 64))
    return sheet

def main():
    dirs = ensure_dirs()
    
    classes = [
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

    for name, func in classes:
        sheet = generate_custom_hero_sheet(func)
        save_sprite(sheet, name, dirs)

if __name__ == "__main__":
    main()
