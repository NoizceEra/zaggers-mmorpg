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
        print(f"Saved HD JRPG Sprite: {path} ({img.size[0]}x{img.size[1]})")

# Master Outline & Base Constants
OUTLINE = (14, 18, 24, 255)
SKIN_LIGHT = (255, 220, 195, 255)
SKIN_BASE  = (245, 200, 165, 255)
SKIN_SHADOW= (210, 160, 125, 255)
EYE_DARK   = (20, 30, 45, 255)
WHITE_SPEC = (255, 255, 255, 255)

def draw_ground_shadow(draw, cy):
    draw.ellipse([18, 52 + cy, 46, 59 + cy], fill=(0, 0, 0, 90))

# --- 1. KNIGHT ---
def draw_hd_knight(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    SPEC = (245, 250, 255, 255)
    LIGHT = (210, 222, 238, 255)
    BASE = (160, 175, 195, 255)
    SHADOW = (105, 118, 140, 255)
    DARK = (65, 75, 95, 255)

    CAPE_LIGHT = (60, 115, 215, 255)
    CAPE_BASE  = (35, 80, 175, 255)
    CAPE_SHADOW= (20, 50, 125, 255)
    GOLD_TRIM  = (235, 190, 50, 255)

    draw_ground_shadow(draw, cy)

    if row == 3: # Back view
        # Flowing Cape
        draw.polygon([(14, 22 + cy), (50, 22 + cy), (54, 55 + cy), (10, 55 + cy)], fill=CAPE_BASE, outline=OUTLINE)
        draw.polygon([(14, 22 + cy), (32, 55 + cy), (10, 55 + cy)], fill=CAPE_SHADOW)
        draw.polygon([(36, 26 + cy), (50, 22 + cy), (52, 53 + cy), (42, 55 + cy)], fill=CAPE_LIGHT)

        # Greaves & Helm Back
        lx1, lx2 = 23 + leg, 29 + leg
        rx1, rx2 = 35 - leg, 41 - leg
        draw.rectangle([lx1, 46 + cy, lx2, 55 + cy], fill=DARK, outline=OUTLINE)
        draw.rectangle([rx1, 46 + cy, rx2, 55 + cy], fill=DARK, outline=OUTLINE)
        draw.rectangle([21, 12 + cy, 43, 27 + cy], fill=BASE, outline=OUTLINE)
        draw.line([(32, 12 + cy), (32, 27 + cy)], fill=GOLD_TRIM, width=2)
    else:
        # Cape side drape
        draw.polygon([(14, 24 + cy), (48, 24 + cy), (52, 53 + cy), (12, 53 + cy)], fill=CAPE_BASE, outline=OUTLINE)
        draw.polygon([(14, 24 + cy), (26, 53 + cy), (12, 53 + cy)], fill=CAPE_SHADOW)

        # Greaves & Legs
        lx1, lx2 = 23 + leg, 29 + leg
        rx1, rx2 = 35 - leg, 41 - leg
        draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=DARK, outline=OUTLINE)
        draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=DARK, outline=OUTLINE)
        draw.rectangle([lx1 + 1, 45 + cy, lx2 - 1, 53 + cy], fill=BASE)
        draw.rectangle([rx1 + 1, 45 + cy, rx2 - 1, 53 + cy], fill=BASE)
        draw.line([(lx1 + 1, 46 + cy), (lx1 + 1, 52 + cy)], fill=SPEC, width=1)

        # Cuirass Plate Chestpiece
        draw.rectangle([21, 26 + cy, 43, 44 + cy], fill=BASE, outline=OUTLINE)
        draw.rectangle([24, 28 + cy, 40, 42 + cy], fill=LIGHT)
        draw.rectangle([26, 29 + cy, 32, 39 + cy], fill=SPEC)
        draw.rectangle([21, 40 + cy, 43, 43 + cy], fill=GOLD_TRIM, outline=OUTLINE)

        # Pauldrons
        draw.polygon([(15, 25 + cy), (22, 27 + cy), (20, 36 + cy), (13, 32 + cy)], fill=LIGHT, outline=OUTLINE)
        draw.line([(16, 26 + cy), (20, 28 + cy)], fill=SPEC, width=1)
        draw.polygon([(49, 25 + cy), (42, 27 + cy), (44, 36 + cy), (51, 32 + cy)], fill=LIGHT, outline=OUTLINE)
        draw.line([(48, 26 + cy), (44, 28 + cy)], fill=SPEC, width=1)

        # Helm & Visor
        draw.rectangle([21, 12 + cy, 43, 27 + cy], fill=BASE, outline=OUTLINE)
        draw.rectangle([24, 14 + cy, 40, 25 + cy], fill=LIGHT)
        draw.line([(25, 14 + cy), (32, 14 + cy)], fill=SPEC, width=2)
        draw.rectangle([24, 19 + cy, 40, 23 + cy], fill=OUTLINE)
        draw.line([(26, 21 + cy), (38, 21 + cy)], fill=SPEC, width=1)

        # Broadsword
        wx = 50 if (row == 0 or row == 2) else 14
        draw.line([(wx, 8 + cy), (wx, 48 + cy)], fill=LIGHT, width=3)
        draw.line([(wx - 1, 10 + cy), (wx - 1, 42 + cy)], fill=SPEC, width=1)
        draw.polygon([(wx, 4 + cy), (wx - 4, 12 + cy), (wx + 4, 12 + cy)], fill=SPEC)
        draw.rectangle([wx - 5, 38 + cy, wx + 5, 41 + cy], fill=GOLD_TRIM, outline=OUTLINE)

# --- 2. BLACK MAGE ---
def draw_hd_blackmage(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    cy = bob

    ROBE_5 = (10, 25, 75, 255)
    ROBE_4 = (20, 45, 120, 255)
    ROBE_3 = (35, 75, 175, 255)
    ROBE_2 = (65, 115, 215, 255)
    HAT_3 = (235, 185, 30, 255)
    HAT_2 = (250, 215, 60, 255)
    HAT_4 = (185, 135, 15, 255)
    GLOW_3 = (255, 220, 30, 255)
    GLOW_1 = (255, 255, 220, 255)
    OAK_3 = (115, 70, 30, 255)

    draw_ground_shadow(draw, cy)

    # Robe Skirt
    draw.polygon([(18, 30 + cy), (46, 30 + cy), (50, 55 + cy), (14, 55 + cy)], fill=ROBE_3, outline=OUTLINE)
    draw.polygon([(18, 30 + cy), (32, 55 + cy), (14, 55 + cy)], fill=ROBE_4)
    draw.polygon([(36, 32 + cy), (46, 30 + cy), (44, 48 + cy)], fill=ROBE_2)

    # Shadow Face & Hat
    draw.rectangle([23, 16 + cy, 41, 28 + cy], fill=OUTLINE)
    sway = 1 if (col == 1 or col == 3) else 0
    draw.polygon([(14, 16 + cy), (50, 16 + cy), (32 + sway, -4 + cy)], fill=HAT_3, outline=OUTLINE)
    draw.polygon([(14, 16 + cy), (32 + sway, 16 + cy), (32 + sway, -4 + cy)], fill=HAT_4)
    draw.rectangle([12, 14 + cy, 52, 18 + cy], fill=HAT_3, outline=OUTLINE)

    if row == 0: # Glowing eyes
        draw.rectangle([25, 20 + cy, 29, 24 + cy], fill=GLOW_3)
        draw.rectangle([26, 21 + cy, 28, 23 + cy], fill=GLOW_1)
        draw.rectangle([35, 20 + cy, 39, 24 + cy], fill=GLOW_3)
        draw.rectangle([36, 21 + cy, 38, 23 + cy], fill=GLOW_1)
    elif row == 1:
        draw.rectangle([23, 20 + cy, 27, 24 + cy], fill=GLOW_3)
    elif row == 2:
        draw.rectangle([37, 20 + cy, 41, 24 + cy], fill=GLOW_3)

    # Oak Staff with Glowing Orb
    wx = 52 if (row == 0 or row == 2) else 12
    draw.line([(wx, 10 + cy), (wx, 54 + cy)], fill=OAK_3, width=4)
    draw.ellipse([wx - 6, 4 + cy, wx + 6, 16 + cy], fill=GLOW_3, outline=OUTLINE)
    draw.ellipse([wx - 2, 7 + cy, wx + 2, 11 + cy], fill=GLOW_1)

# --- 3. THIEF ---
def draw_hd_thief(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    EMERALD_BASE = (30, 130, 65, 255)
    EMERALD_LIGHT= (55, 175, 95, 255)
    EMERALD_SHADOW=(18, 88, 42, 255)
    LEATHER_BASE = (125, 75, 38, 255)
    LEATHER_LIGHT= (160, 105, 58, 255)
    STEEL_SPEC   = (250, 255, 255, 255)
    STEEL_LIGHT  = (225, 238, 245, 255)
    GOLD_BASE    = (220, 175, 45, 255)

    draw_ground_shadow(draw, cy)

    if row == 3: # Back view
        draw.polygon([(18, 12 + cy), (46, 12 + cy), (50, 52 + cy), (14, 52 + cy)], fill=EMERALD_BASE, outline=OUTLINE)
        draw.polygon([(22, 16 + cy), (42, 16 + cy), (46, 50 + cy), (18, 50 + cy)], fill=EMERALD_SHADOW)
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

        # Dual Daggers
        draw.line([(12, 26 + cy), (12, 44 + cy)], fill=STEEL_LIGHT, width=2)
        draw.line([(11, 26 + cy), (11, 42 + cy)], fill=STEEL_SPEC, width=1)
        draw.line([(52, 26 + cy), (52, 44 + cy)], fill=STEEL_LIGHT, width=2)
        draw.line([(53, 26 + cy), (53, 42 + cy)], fill=STEEL_SPEC, width=1)

def generate_all_hd_sprites():
    dirs = ensure_dirs()
    # We apply this HD rendering across all 12 classes
    classes_map = [
        ("hero_knight.png", draw_hd_knight),
        ("hero_blackmage.png", draw_hd_blackmage),
        ("hero_thief.png", draw_hd_thief),
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
