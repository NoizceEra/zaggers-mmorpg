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

# Color Palettes & Outlines
OUTLINE = (18, 22, 28, 255)
SKIN = (245, 205, 170, 255)

def draw_dragoon_frame(draw, row, col):
    """ Dragoon Lancer: Dragon helm, spiked plate, dragon polearm """
    bob = 1 if (col == 1 or col == 3) else 0
    leg_step = 2 if col == 2 else (-2 if col == 3 else 0)
    cy = bob

    # Colors
    ARMOR_PURPLE = (75, 45, 110, 255)
    ARMOR_DARK = (45, 25, 75, 255)
    TRIM_SILVER = (190, 195, 210, 255)
    HORN_GOLD = (230, 185, 55, 255)
    LANCE_WOOD = (130, 80, 45, 255)
    LANCE_TIP = (220, 225, 235, 255)

    # Shadow
    draw.ellipse([20, 53, 44, 59], fill=(0, 0, 0, 90))

    # Boots & Legs
    draw.rectangle([23 + leg_step, 45 + cy, 29 + leg_step, 56 + cy], fill=ARMOR_DARK, outline=OUTLINE)
    draw.rectangle([35 - leg_step, 45 + cy, 41 - leg_step, 56 + cy], fill=ARMOR_DARK, outline=OUTLINE)

    # Torso & Plate
    draw.rectangle([22, 30 + cy, 42, 44 + cy], fill=ARMOR_PURPLE, outline=OUTLINE)
    draw.rectangle([26, 32 + cy, 38, 42 + cy], fill=TRIM_SILVER)

    # Arms
    draw.rectangle([17, 31 + cy, 22, 42 + cy], fill=ARMOR_PURPLE, outline=OUTLINE)
    draw.rectangle([42, 31 + cy, 47, 42 + cy], fill=ARMOR_PURPLE, outline=OUTLINE)

    # Dragon Helm & Horn Crest
    draw.rectangle([21, 15 + cy, 43, 31 + cy], fill=ARMOR_PURPLE, outline=OUTLINE)
    # Visor slit
    if row != 3:
        draw.rectangle([25, 23 + cy, 39, 26 + cy], fill=HORN_GOLD)
    # Dragon Horn Crest
    draw.polygon([(32, 8 + cy), (27, 16 + cy), (37, 16 + cy)], fill=HORN_GOLD, outline=OUTLINE)

    # Dragon Lance Weapon
    if row == 0 or row == 2: # Right hand
        draw.line([(48, 10 + cy), (48, 54 + cy)], fill=LANCE_WOOD, width=3)
        draw.polygon([(48, 2 + cy), (44, 12 + cy), (52, 12 + cy)], fill=LANCE_TIP, outline=OUTLINE)
    elif row == 1: # Left hand
        draw.line([(16, 10 + cy), (16, 54 + cy)], fill=LANCE_WOOD, width=3)
        draw.polygon([(16, 2 + cy), (12, 12 + cy), (20, 12 + cy)], fill=LANCE_TIP, outline=OUTLINE)

def draw_monk_frame(draw, row, col):
    """ Brawler Monk: Martial arts white gi, red belt, wrapped fists """
    bob = 1 if (col == 1 or col == 3) else 0
    leg_step = 2 if col == 2 else (-2 if col == 3 else 0)
    cy = bob

    GI_WHITE = (240, 242, 245, 255)
    GI_SHADOW = (190, 195, 205, 255)
    BELT_RED = (210, 40, 45, 255)
    WRAP_GREY = (170, 175, 185, 255)
    HAIR_DARK = (40, 40, 45, 255)

    draw.ellipse([20, 53, 44, 59], fill=(0, 0, 0, 90))

    # Pants & Boots
    draw.rectangle([23 + leg_step, 44 + cy, 29 + leg_step, 56 + cy], fill=GI_SHADOW, outline=OUTLINE)
    draw.rectangle([35 - leg_step, 44 + cy, 41 - leg_step, 56 + cy], fill=GI_SHADOW, outline=OUTLINE)

    # Martial Gi Body
    draw.rectangle([23, 28 + cy, 41, 44 + cy], fill=GI_WHITE, outline=OUTLINE)
    # Red Martial Belt / Sash
    draw.rectangle([22, 38 + cy, 42, 42 + cy], fill=BELT_RED, outline=OUTLINE)
    draw.polygon([(36, 42 + cy), (40, 42 + cy), (38, 50 + cy)], fill=BELT_RED)

    # Arms with Wrapped Fists
    draw.rectangle([17, 30 + cy, 22, 39 + cy], fill=GI_WHITE, outline=OUTLINE)
    draw.ellipse([16, 38 + cy, 23, 45 + cy], fill=WRAP_GREY, outline=OUTLINE)
    draw.rectangle([42, 30 + cy, 47, 39 + cy], fill=GI_WHITE, outline=OUTLINE)
    draw.ellipse([41, 38 + cy, 48, 45 + cy], fill=WRAP_GREY, outline=OUTLINE)

    # Head & Headband
    draw.rectangle([23, 16 + cy, 41, 29 + cy], fill=SKIN, outline=OUTLINE)
    draw.rectangle([22, 16 + cy, 42, 20 + cy], fill=BELT_RED) # Red Headband
    draw.rectangle([22, 12 + cy, 42, 17 + cy], fill=HAIR_DARK) # Hair
    if row == 0:
        draw.rectangle([26, 23 + cy, 28, 26 + cy], fill=OUTLINE)
        draw.rectangle([36, 23 + cy, 38, 26 + cy], fill=OUTLINE)

def draw_paladin_frame(draw, row, col):
    """ Holy Paladin: Golden holy armor, blue cape, tower shield """
    bob = 1 if (col == 1 or col == 3) else 0
    leg_step = 2 if col == 2 else (-2 if col == 3 else 0)
    cy = bob

    GOLD_ARMOR = (235, 185, 45, 255)
    GOLD_HIGHLIGHT = (255, 225, 90, 255)
    CAPE_BLUE = (35, 95, 185, 255)
    SHIELD_BLUE = (25, 75, 155, 255)

    draw.ellipse([20, 53, 44, 59], fill=(0, 0, 0, 90))

    # Blue Cape Back
    draw.polygon([(16, 26 + cy), (48, 26 + cy), (50, 52 + cy), (14, 52 + cy)], fill=CAPE_BLUE)

    # Boots & Legs
    draw.rectangle([23 + leg_step, 45 + cy, 29 + leg_step, 56 + cy], fill=GOLD_ARMOR, outline=OUTLINE)
    draw.rectangle([35 - leg_step, 45 + cy, 41 - leg_step, 56 + cy], fill=GOLD_ARMOR, outline=OUTLINE)

    # Golden Breastplate
    draw.rectangle([22, 28 + cy, 42, 44 + cy], fill=GOLD_ARMOR, outline=OUTLINE)
    draw.rectangle([26, 30 + cy, 38, 42 + cy], fill=GOLD_HIGHLIGHT)

    # Golden Winged Helmet
    draw.rectangle([22, 14 + cy, 42, 29 + cy], fill=GOLD_ARMOR, outline=OUTLINE)
    draw.polygon([(18, 12 + cy), (23, 14 + cy), (20, 24 + cy)], fill=GOLD_HIGHLIGHT) # Left wing
    draw.polygon([(46, 12 + cy), (41, 14 + cy), (44, 24 + cy)], fill=GOLD_HIGHLIGHT) # Right wing
    if row != 3:
        draw.rectangle([26, 21 + cy, 38, 25 + cy], fill=OUTLINE)

    # Holy Tower Shield (Left hand foreground)
    draw.rectangle([8, 24 + cy, 20, 48 + cy], fill=SHIELD_BLUE, outline=OUTLINE)
    draw.polygon([(14, 26 + cy), (14, 46 + cy), (8, 36 + cy), (20, 36 + cy)], fill=GOLD_ARMOR)

def draw_sage_frame(draw, row, col):
    """ Scholar Sage: Scholastic emerald robes, spellbook """
    bob = 1 if (col == 1 or col == 3) else 0
    leg_step = 2 if col == 2 else (-2 if col == 3 else 0)
    cy = bob

    ROBE_EMERALD = (35, 125, 80, 255)
    ROBE_DARK = (20, 80, 50, 255)
    GOLD_TRIM = (230, 185, 55, 255)
    BOOK_BROWN = (140, 75, 35, 255)
    BOOK_PAGE = (240, 235, 210, 255)

    draw.ellipse([20, 53, 44, 59], fill=(0, 0, 0, 90))

    # Flowing Robe Skirt
    draw.polygon([(20, 34 + cy), (44, 34 + cy), (48, 54 + cy), (16, 54 + cy)], fill=ROBE_EMERALD, outline=OUTLINE)

    # Robe Torso & Gold Trim Collar
    draw.rectangle([23, 26 + cy, 41, 38 + cy], fill=ROBE_EMERALD, outline=OUTLINE)
    draw.line([(32, 26 + cy), (32, 38 + cy)], fill=GOLD_TRIM, width=2)

    # Head & Hood Cowl
    draw.polygon([(20, 14 + cy), (44, 14 + cy), (42, 28 + cy), (22, 28 + cy)], fill=ROBE_DARK, outline=OUTLINE)
    draw.rectangle([25, 18 + cy, 39, 27 + cy], fill=SKIN)
    if row == 0:
        draw.rectangle([27, 21 + cy, 29, 24 + cy], fill=OUTLINE)
        draw.rectangle([35, 21 + cy, 37, 24 + cy], fill=OUTLINE)

    # Elemental Spellbook in hand
    draw.rectangle([42, 32 + cy, 54, 46 + cy], fill=BOOK_BROWN, outline=OUTLINE)
    draw.rectangle([44, 34 + cy, 52, 44 + cy], fill=BOOK_PAGE)

def draw_bard_frame(draw, row, col):
    """ Minstrel Bard: Feathered cap, crimson doublet, acoustic lute """
    bob = 1 if (col == 1 or col == 3) else 0
    leg_step = 2 if col == 2 else (-2 if col == 3 else 0)
    cy = bob

    DOUBLET_CRIMSON = (195, 45, 60, 255)
    CAP_GREEN = (45, 135, 75, 255)
    FEATHER_WHITE = (245, 245, 250, 255)
    LUTE_WOOD = (175, 110, 50, 255)
    LUTE_DARK = (120, 70, 30, 255)

    draw.ellipse([20, 53, 44, 59], fill=(0, 0, 0, 90))

    # Tights & Boots
    draw.rectangle([23 + leg_step, 45 + cy, 29 + leg_step, 56 + cy], fill=CAP_GREEN, outline=OUTLINE)
    draw.rectangle([35 - leg_step, 45 + cy, 41 - leg_step, 56 + cy], fill=CAP_GREEN, outline=OUTLINE)

    # Crimson Doublet
    draw.rectangle([22, 28 + cy, 42, 44 + cy], fill=DOUBLET_CRIMSON, outline=OUTLINE)

    # Head & Feathered Cap
    draw.rectangle([23, 16 + cy, 41, 29 + cy], fill=SKIN, outline=OUTLINE)
    draw.polygon([(20, 12 + cy), (44, 12 + cy), (40, 18 + cy), (24, 18 + cy)], fill=CAP_GREEN, outline=OUTLINE)
    # White Feather Plume
    draw.polygon([(16, 4 + cy), (22, 10 + cy), (18, 16 + cy)], fill=FEATHER_WHITE, outline=OUTLINE)

    # Acoustic Lute (held diagonally)
    draw.ellipse([38, 30 + cy, 54, 46 + cy], fill=LUTE_WOOD, outline=OUTLINE)
    draw.ellipse([43, 35 + cy, 49, 41 + cy], fill=LUTE_DARK)
    draw.line([(32, 22 + cy), (44, 34 + cy)], fill=LUTE_DARK, width=3)

def draw_alchemist_frame(draw, row, col):
    """ Alchemist Smith: Brass goggles, leather apron, potion belt """
    bob = 1 if (col == 1 or col == 3) else 0
    leg_step = 2 if col == 2 else (-2 if col == 3 else 0)
    cy = bob

    APRON_BROWN = (150, 90, 45, 255)
    BELT_DARK = (80, 45, 25, 255)
    GOGGLE_BRASS = (220, 170, 50, 255)
    FLASK_CYAN = (60, 210, 200, 255)
    FLASK_RED = (230, 60, 60, 255)

    draw.ellipse([20, 53, 44, 59], fill=(0, 0, 0, 90))

    # Pants & Boots
    draw.rectangle([23 + leg_step, 45 + cy, 29 + leg_step, 56 + cy], fill=BELT_DARK, outline=OUTLINE)
    draw.rectangle([35 - leg_step, 45 + cy, 41 - leg_step, 56 + cy], fill=BELT_DARK, outline=OUTLINE)

    # Leather Apron
    draw.rectangle([22, 28 + cy, 42, 45 + cy], fill=APRON_BROWN, outline=OUTLINE)

    # Potion Belt with Flasks
    draw.rectangle([21, 38 + cy, 43, 41 + cy], fill=BELT_DARK, outline=OUTLINE)
    draw.ellipse([24, 40 + cy, 28, 46 + cy], fill=FLASK_CYAN, outline=OUTLINE)
    draw.ellipse([36, 40 + cy, 40, 46 + cy], fill=FLASK_RED, outline=OUTLINE)

    # Head & Brass Goggles
    draw.rectangle([23, 16 + cy, 41, 29 + cy], fill=SKIN, outline=OUTLINE)
    # Goggles on forehead
    draw.rectangle([22, 13 + cy, 42, 18 + cy], fill=GOGGLE_BRASS, outline=OUTLINE)
    draw.ellipse([25, 14 + cy, 31, 18 + cy], fill=FLASK_CYAN)
    draw.ellipse([33, 14 + cy, 39, 18 + cy], fill=FLASK_CYAN)

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

    # 1. Dragoon
    dragoon = generate_custom_hero_sheet(draw_dragoon_frame)
    save_sprite(dragoon, "hero_dragoon.png", dirs)

    # 2. Monk
    monk = generate_custom_hero_sheet(draw_monk_frame)
    save_sprite(monk, "hero_monk.png", dirs)

    # 3. Paladin
    paladin = generate_custom_hero_sheet(draw_paladin_frame)
    save_sprite(paladin, "hero_paladin.png", dirs)

    # 4. Sage
    sage = generate_custom_hero_sheet(draw_sage_frame)
    save_sprite(sage, "hero_sage.png", dirs)

    # 5. Bard
    bard = generate_custom_hero_sheet(draw_bard_frame)
    save_sprite(bard, "hero_bard.png", dirs)

    # 6. Alchemist
    alchemist = generate_custom_hero_sheet(draw_alchemist_frame)
    save_sprite(alchemist, "hero_alchemist.png", dirs)

if __name__ == "__main__":
    main()
