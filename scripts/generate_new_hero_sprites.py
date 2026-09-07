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

# Master Color Palettes
OUTLINE = (14, 18, 24, 255)
SKIN_BASE = (245, 200, 165, 255)
SKIN_SHADOW = (210, 160, 125, 255)
EYE_DARK = (20, 30, 45, 255)

# --- 1. DRAGOON (Lancer / Dragon Knight) ---
def draw_dragoon_frame(draw, row, col):
    # row: 0=Down, 1=Left, 2=Right, 3=Up
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    P_BASE = (75, 45, 120, 255)
    P_LIGHT = (115, 80, 165, 255)
    P_SHADOW = (45, 25, 75, 255)
    SILVER = (200, 205, 220, 255)
    SILVER_SHADOW = (140, 145, 160, 255)
    GOLD = (235, 190, 50, 255)
    VISOR_CYAN = (60, 230, 240, 255)
    LANCE_SHAFT = (120, 75, 40, 255)
    LANCE_TIP = (220, 230, 245, 255)
    RIBBON_RED = (220, 45, 55, 255)

    # Shadow
    draw.ellipse([18, 52, 46, 59], fill=(0, 0, 0, 90))

    # Legs & Greaves
    lx1, lx2 = 23 + leg, 29 + leg
    rx1, rx2 = 35 - leg, 41 - leg
    draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=P_SHADOW, outline=OUTLINE)
    draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=P_SHADOW, outline=OUTLINE)
    draw.rectangle([lx1 + 1, 46 + cy, lx2 - 1, 54 + cy], fill=SILVER_SHADOW)
    draw.rectangle([rx1 + 1, 46 + cy, rx2 - 1, 54 + cy], fill=SILVER_SHADOW)

    # Body Cuirass
    draw.rectangle([21, 28 + cy, 43, 44 + cy], fill=P_BASE, outline=OUTLINE)
    draw.rectangle([25, 30 + cy, 39, 42 + cy], fill=P_LIGHT)
    draw.line([(32, 29 + cy), (32, 43 + cy)], fill=SILVER, width=2)
    draw.rectangle([23, 40 + cy, 41, 43 + cy], fill=GOLD)

    # Shoulder Pauldrons (Spiked Dragon Scales)
    draw.polygon([(15, 26 + cy), (22, 28 + cy), (20, 36 + cy), (13, 32 + cy)], fill=P_LIGHT, outline=OUTLINE)
    draw.polygon([(49, 26 + cy), (42, 28 + cy), (44, 36 + cy), (51, 32 + cy)], fill=P_LIGHT, outline=OUTLINE)

    # Dragon Helm & Horn Crest
    draw.rectangle([21, 14 + cy, 43, 29 + cy], fill=P_BASE, outline=OUTLINE)
    draw.rectangle([23, 16 + cy, 41, 27 + cy], fill=P_LIGHT)
    # Dragon Horns
    draw.polygon([(32, 4 + cy), (25, 14 + cy), (39, 14 + cy)], fill=GOLD, outline=OUTLINE)
    draw.polygon([(17, 10 + cy), (22, 16 + cy), (20, 20 + cy)], fill=GOLD, outline=OUTLINE)
    draw.polygon([(47, 10 + cy), (42, 16 + cy), (44, 20 + cy)], fill=GOLD, outline=OUTLINE)

    # Visor Slit
    if row == 0: # Down
        draw.rectangle([24, 21 + cy, 40, 24 + cy], fill=OUTLINE)
        draw.line([(26, 22 + cy), (38, 22 + cy)], fill=VISOR_CYAN, width=2)
    elif row == 1: # Left
        draw.rectangle([22, 21 + cy, 34, 24 + cy], fill=OUTLINE)
        draw.line([(24, 22 + cy), (32, 22 + cy)], fill=VISOR_CYAN, width=2)
    elif row == 2: # Right
        draw.rectangle([30, 21 + cy, 42, 24 + cy], fill=OUTLINE)
        draw.line([(32, 22 + cy), (40, 22 + cy)], fill=VISOR_CYAN, width=2)
    elif row == 3: # Up (Back view dragon crest)
        draw.rectangle([23, 16 + cy, 41, 27 + cy], fill=P_SHADOW)
        draw.line([(32, 16 + cy), (32, 27 + cy)], fill=SILVER, width=2)

    # Dragon Lance Weapon
    wx = 50 if (row == 0 or row == 2) else 14
    draw.line([(wx, 4 + cy), (wx, 56 + cy)], fill=LANCE_SHAFT, width=3)
    draw.polygon([(wx, -2 + cy), (wx - 5, 12 + cy), (wx + 5, 12 + cy)], fill=LANCE_TIP, outline=OUTLINE)
    draw.polygon([(wx - 2, 0 + cy), (wx, -4 + cy), (wx + 2, 0 + cy)], fill=(255, 255, 255, 255))
    draw.polygon([(wx, 12 + cy), (wx - 8, 18 + cy), (wx + 2, 16 + cy)], fill=RIBBON_RED)


# --- 2. MONK (Brawler / Martial Artist) ---
def draw_monk_frame(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    GI_WHITE = (245, 248, 252, 255)
    GI_SHADOW = (185, 195, 210, 255)
    BELT_RED = (215, 35, 45, 255)
    BELT_DARK = (150, 20, 30, 255)
    WRAP_GREY = (160, 170, 185, 255)
    HAIR_DARK = (35, 35, 40, 255)
    GOLD_STUD = (240, 195, 50, 255)

    draw.ellipse([18, 52, 46, 59], fill=(0, 0, 0, 90))

    # Trousers & Boots
    lx1, lx2 = 23 + leg, 29 + leg
    rx1, rx2 = 35 - leg, 41 - leg
    draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=GI_SHADOW, outline=OUTLINE)
    draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=GI_SHADOW, outline=OUTLINE)

    # Martial Gi Body & Folded Lapels
    draw.rectangle([21, 27 + cy, 43, 44 + cy], fill=GI_WHITE, outline=OUTLINE)
    draw.polygon([(21, 27 + cy), (32, 38 + cy), (21, 38 + cy)], fill=GI_SHADOW)
    draw.polygon([(43, 27 + cy), (32, 38 + cy), (43, 38 + cy)], fill=GI_SHADOW)
    # V-Neck Skin exposure
    if row != 3:
        draw.polygon([(27, 27 + cy), (32, 35 + cy), (37, 27 + cy)], fill=SKIN_BASE)

    # Red Martial Sash Belt & Fluttering Knot
    draw.rectangle([20, 38 + cy, 44, 43 + cy], fill=BELT_RED, outline=OUTLINE)
    draw.polygon([(36, 43 + cy), (41, 43 + cy), (39, 53 + cy)], fill=BELT_RED, outline=OUTLINE)
    draw.polygon([(32, 43 + cy), (37, 43 + cy), (34, 50 + cy)], fill=BELT_DARK)

    # Arms & Spiked Iron Fist Wraps
    draw.rectangle([16, 29 + cy, 21, 38 + cy], fill=GI_WHITE, outline=OUTLINE)
    draw.ellipse([14, 37 + cy, 22, 45 + cy], fill=WRAP_GREY, outline=OUTLINE)
    draw.rectangle([16, 40 + cy, 20, 42 + cy], fill=GOLD_STUD)

    draw.rectangle([43, 29 + cy, 48, 38 + cy], fill=GI_WHITE, outline=OUTLINE)
    draw.ellipse([42, 37 + cy, 50, 45 + cy], fill=WRAP_GREY, outline=OUTLINE)
    draw.rectangle([44, 40 + cy, 48, 42 + cy], fill=GOLD_STUD)

    # Head, Hair & Red Bandana
    draw.rectangle([23, 14 + cy, 41, 28 + cy], fill=SKIN_BASE, outline=OUTLINE)
    draw.rectangle([22, 10 + cy, 42, 17 + cy], fill=HAIR_DARK) # Hair
    draw.rectangle([21, 15 + cy, 43, 19 + cy], fill=BELT_RED, outline=OUTLINE) # Bandana
    draw.polygon([(43, 16 + cy), (49, 14 + cy), (47, 22 + cy)], fill=BELT_RED) # Bandana tail

    if row == 0: # Down
        draw.rectangle([26, 22 + cy, 28, 25 + cy], fill=EYE_DARK)
        draw.rectangle([36, 22 + cy, 38, 25 + cy], fill=EYE_DARK)
        draw.line([(28, 26 + cy), (36, 26 + cy)], fill=SKIN_SHADOW, width=1)
    elif row == 1: # Left
        draw.rectangle([24, 22 + cy, 26, 25 + cy], fill=EYE_DARK)
    elif row == 2: # Right
        draw.rectangle([38, 22 + cy, 40, 25 + cy], fill=EYE_DARK)


# --- 3. PALADIN (Holy Templar) ---
def draw_paladin_frame(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    GOLD = (240, 190, 45, 255)
    GOLD_LIGHT = (255, 230, 110, 255)
    GOLD_SHADOW = (180, 135, 25, 255)
    CAPE_BLUE = (35, 95, 195, 255)
    CAPE_DARK = (20, 60, 135, 255)
    SHIELD_BLUE = (30, 80, 170, 255)
    STEEL_SWORD = (230, 235, 245, 255)

    draw.ellipse([18, 52, 46, 59], fill=(0, 0, 0, 90))

    # Royal Blue Cape (Renders behind body)
    draw.polygon([(16, 24 + cy), (48, 24 + cy), (51, 54 + cy), (13, 54 + cy)], fill=CAPE_BLUE, outline=OUTLINE)
    draw.polygon([(16, 24 + cy), (32, 54 + cy), (13, 54 + cy)], fill=CAPE_DARK)

    # Golden Boots & Leg Plate
    lx1, lx2 = 23 + leg, 29 + leg
    rx1, rx2 = 35 - leg, 41 - leg
    draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=GOLD, outline=OUTLINE)
    draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=GOLD, outline=OUTLINE)
    draw.rectangle([lx1 + 1, 45 + cy, lx2 - 1, 53 + cy], fill=GOLD_LIGHT)
    draw.rectangle([rx1 + 1, 45 + cy, rx2 - 1, 53 + cy], fill=GOLD_LIGHT)

    # Holy Golden Cuirass
    draw.rectangle([21, 26 + cy, 43, 44 + cy], fill=GOLD, outline=OUTLINE)
    draw.rectangle([25, 28 + cy, 39, 42 + cy], fill=GOLD_LIGHT)
    draw.polygon([(32, 28 + cy), (28, 36 + cy), (36, 36 + cy)], fill=GOLD_SHADOW) # Cross emblem

    # Winged Templar Helmet
    draw.rectangle([21, 12 + cy, 43, 27 + cy], fill=GOLD, outline=OUTLINE)
    draw.rectangle([24, 14 + cy, 40, 25 + cy], fill=GOLD_LIGHT)
    # Golden Wings on Helm
    draw.polygon([(14, 8 + cy), (21, 12 + cy), (18, 22 + cy)], fill=GOLD_LIGHT, outline=OUTLINE)
    draw.polygon([(50, 8 + cy), (43, 12 + cy), (46, 22 + cy)], fill=GOLD_LIGHT, outline=OUTLINE)

    if row != 3: # Visor
        draw.rectangle([24, 19 + cy, 40, 23 + cy], fill=OUTLINE)
        draw.line([(26, 21 + cy), (38, 21 + cy)], fill=GOLD_LIGHT, width=1)

    # Holy Winged Tower Shield (Left hand)
    draw.polygon([(6, 22 + cy), (20, 22 + cy), (18, 48 + cy), (8, 48 + cy)], fill=SHIELD_BLUE, outline=OUTLINE)
    draw.polygon([(13, 24 + cy), (13, 46 + cy), (8, 35 + cy), (18, 35 + cy)], fill=GOLD, outline=OUTLINE)

    # Holy Longsword (Right hand)
    if row == 0 or row == 2:
        draw.line([(48, 14 + cy), (48, 48 + cy)], fill=STEEL_SWORD, width=3)
        draw.polygon([(48, 8 + cy), (45, 16 + cy), (51, 16 + cy)], fill=(255, 255, 255, 255))
        draw.rectangle([44, 38 + cy, 52, 41 + cy], fill=GOLD, outline=OUTLINE)


# --- 4. SAGE (Scholar / High Arcanist) ---
def draw_sage_frame(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    ROBE_EMERALD = (35, 135, 85, 255)
    ROBE_LIGHT = (65, 175, 115, 255)
    ROBE_DARK = (20, 85, 50, 255)
    GOLD_TRIM = (240, 195, 55, 255)
    BOOK_BROWN = (145, 75, 35, 255)
    PAGE_CREAM = (245, 240, 220, 255)
    ARCANE_CYAN = (80, 235, 245, 255)

    draw.ellipse([18, 52, 46, 59], fill=(0, 0, 0, 90))

    # Flowing Robe Skirt
    draw.polygon([(18, 32 + cy), (46, 32 + cy), (50, 55 + cy), (14, 55 + cy)], fill=ROBE_EMERALD, outline=OUTLINE)
    draw.polygon([(18, 32 + cy), (32, 55 + cy), (14, 55 + cy)], fill=ROBE_DARK)
    draw.line([(16, 53 + cy), (48, 53 + cy)], fill=GOLD_TRIM, width=2)

    # Robe Torso & Vestment Trim
    draw.rectangle([22, 24 + cy, 42, 36 + cy], fill=ROBE_EMERALD, outline=OUTLINE)
    draw.line([(32, 24 + cy), (32, 36 + cy)], fill=GOLD_TRIM, width=2)

    # Head, Cowl Hood & Golden Halo
    draw.ellipse([24, 4 + cy, 40, 18 + cy], fill=(0, 0, 0, 0), outline=GOLD_TRIM) # Halo
    draw.polygon([(18, 12 + cy), (46, 12 + cy), (44, 27 + cy), (20, 27 + cy)], fill=ROBE_DARK, outline=OUTLINE)
    draw.rectangle([24, 16 + cy, 40, 26 + cy], fill=SKIN_BASE)

    if row == 0:
        draw.rectangle([26, 20 + cy, 28, 23 + cy], fill=EYE_DARK)
        draw.rectangle([36, 20 + cy, 38, 23 + cy], fill=EYE_DARK)

    # Spellbook Grimoire (Held open)
    draw.rectangle([42, 30 + cy, 56, 46 + cy], fill=BOOK_BROWN, outline=OUTLINE)
    draw.rectangle([44, 32 + cy, 54, 44 + cy], fill=PAGE_CREAM)
    draw.line([(49, 32 + cy), (49, 44 + cy)], fill=OUTLINE, width=1)
    draw.rectangle([46, 36 + cy, 48, 38 + cy], fill=ARCANE_CYAN) # Glowing rune


# --- 5. BARD (Minstrel / Troubadour) ---
def draw_bard_frame(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    DOUBLET_CRIMSON = (205, 45, 65, 255)
    DOUBLET_LIGHT = (235, 80, 100, 255)
    TROUSERS_GREEN = (45, 135, 75, 255)
    CAP_GREEN = (35, 115, 60, 255)
    FEATHER_WHITE = (250, 250, 255, 255)
    LUTE_WOOD = (180, 110, 45, 255)
    LUTE_LIGHT = (215, 145, 75, 255)
    LUTE_DARK = (110, 60, 25, 255)

    draw.ellipse([18, 52, 46, 59], fill=(0, 0, 0, 90))

    # Trousers & Boots
    lx1, lx2 = 23 + leg, 29 + leg
    rx1, rx2 = 35 - leg, 41 - leg
    draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=TROUSERS_GREEN, outline=OUTLINE)
    draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=TROUSERS_GREEN, outline=OUTLINE)

    # Crimson Doublet & Gold Buttons
    draw.rectangle([21, 27 + cy, 43, 44 + cy], fill=DOUBLET_CRIMSON, outline=OUTLINE)
    draw.rectangle([25, 29 + cy, 39, 42 + cy], fill=DOUBLET_LIGHT)
    for button_y in range(30, 42, 4):
        draw.rectangle([31, button_y + cy, 33, button_y + 2 + cy], fill=(240, 200, 50, 255))

    # Head & Feathered Minstrel Cap
    draw.rectangle([23, 14 + cy, 41, 28 + cy], fill=SKIN_BASE, outline=OUTLINE)
    draw.polygon([(18, 10 + cy), (46, 10 + cy), (42, 17 + cy), (22, 17 + cy)], fill=CAP_GREEN, outline=OUTLINE)
    # White Plume Feather
    draw.polygon([(12, 2 + cy), (20, 8 + cy), (16, 16 + cy)], fill=FEATHER_WHITE, outline=OUTLINE)

    if row == 0:
        draw.rectangle([26, 21 + cy, 28, 24 + cy], fill=EYE_DARK)
        draw.rectangle([36, 21 + cy, 38, 24 + cy], fill=EYE_DARK)

    # Acoustic Lute / Harp
    draw.ellipse([36, 28 + cy, 54, 46 + cy], fill=LUTE_WOOD, outline=OUTLINE)
    draw.ellipse([38, 30 + cy, 52, 44 + cy], fill=LUTE_LIGHT)
    draw.ellipse([43, 35 + cy, 47, 39 + cy], fill=LUTE_DARK)
    draw.line([(30, 20 + cy), (43, 33 + cy)], fill=LUTE_DARK, width=3)


# --- 6. ALCHEMIST (Smith / Master Tinker) ---
def draw_alchemist_frame(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    APRON_BROWN = (155, 95, 45, 255)
    APRON_LIGHT = (185, 125, 70, 255)
    BELT_DARK = (75, 45, 25, 255)
    BRASS_GOGGLES = (225, 175, 50, 255)
    LENS_CYAN = (60, 220, 230, 255)
    FLASK_RED = (235, 60, 60, 255)
    FLASK_CYAN = (60, 210, 210, 255)
    FLASK_GREEN = (70, 220, 80, 255)

    draw.ellipse([18, 52, 46, 59], fill=(0, 0, 0, 90))

    # Trousers & Boots
    lx1, lx2 = 23 + leg, 29 + leg
    rx1, rx2 = 35 - leg, 41 - leg
    draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=BELT_DARK, outline=OUTLINE)
    draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=BELT_DARK, outline=OUTLINE)

    # Leather Apron
    draw.rectangle([21, 27 + cy, 43, 45 + cy], fill=APRON_BROWN, outline=OUTLINE)
    draw.rectangle([25, 29 + cy, 39, 43 + cy], fill=APRON_LIGHT)

    # Potion Belt with Flasks
    draw.rectangle([19, 37 + cy, 45, 40 + cy], fill=BELT_DARK, outline=OUTLINE)
    draw.ellipse([22, 39 + cy, 27, 46 + cy], fill=FLASK_CYAN, outline=OUTLINE)
    draw.ellipse([30, 39 + cy, 35, 46 + cy], fill=FLASK_RED, outline=OUTLINE)
    draw.ellipse([38, 39 + cy, 43, 46 + cy], fill=FLASK_GREEN, outline=OUTLINE)

    # Head & Brass Tinker Goggles
    draw.rectangle([23, 14 + cy, 41, 28 + cy], fill=SKIN_BASE, outline=OUTLINE)
    # Goggles resting on forehead
    draw.rectangle([20, 11 + cy, 44, 17 + cy], fill=BRASS_GOGGLES, outline=OUTLINE)
    draw.ellipse([24, 12 + cy, 30, 16 + cy], fill=LENS_CYAN)
    draw.ellipse([34, 12 + cy, 40, 16 + cy], fill=LENS_CYAN)

    if row == 0:
        draw.rectangle([26, 21 + cy, 28, 24 + cy], fill=EYE_DARK)
        draw.rectangle([36, 21 + cy, 38, 24 + cy], fill=EYE_DARK)

    # Alchemist Flask in hand
    draw.ellipse([44, 30 + cy, 54, 42 + cy], fill=FLASK_CYAN, outline=OUTLINE)
    draw.rectangle([47, 26 + cy, 51, 30 + cy], fill=BRASS_GOGGLES)


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

    dragoon = generate_custom_hero_sheet(draw_dragoon_frame)
    save_sprite(dragoon, "hero_dragoon.png", dirs)

    monk = generate_custom_hero_sheet(draw_monk_frame)
    save_sprite(monk, "hero_monk.png", dirs)

    paladin = generate_custom_hero_sheet(draw_paladin_frame)
    save_sprite(paladin, "hero_paladin.png", dirs)

    sage = generate_custom_hero_sheet(draw_sage_frame)
    save_sprite(sage, "hero_sage.png", dirs)

    bard = generate_custom_hero_sheet(draw_bard_frame)
    save_sprite(bard, "hero_bard.png", dirs)

    alchemist = generate_custom_hero_sheet(draw_alchemist_frame)
    save_sprite(alchemist, "hero_alchemist.png", dirs)

if __name__ == "__main__":
    main()
