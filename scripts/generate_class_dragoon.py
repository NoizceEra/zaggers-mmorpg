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

def save_sprite(img, filename, dirs):
    for d in dirs:
        path = os.path.join(d, filename)
        img.save(path, "PNG")
        print(f"Saved: {path} ({img.size[0]}x{img.size[1]})")

OUTLINE = (14, 18, 24, 255)

# 5-Tone Color Ramps
PURPLE_HI     = (160, 110, 220, 255)
PURPLE_LIGHT  = (125, 75, 180, 255)
PURPLE_BASE   = (90, 48, 138, 255)
PURPLE_SHADOW = (58, 28, 92, 255)
PURPLE_DARK   = (34, 14, 56, 255)

GOLD_HI       = (255, 235, 120, 255)
GOLD_LIGHT    = (245, 200, 60, 255)
GOLD_BASE     = (215, 160, 25, 255)
GOLD_SHADOW   = (160, 112, 12, 255)
GOLD_DARK     = (98, 65, 4, 255)

CYAN_HI       = (220, 255, 255, 255)
CYAN_LIGHT    = (110, 245, 255, 255)
CYAN_BASE     = (30, 210, 230, 255)
CYAN_SHADOW   = (10, 150, 175, 255)
CYAN_DARK     = (4, 90, 110, 255)

SILVER_LIGHT  = (215, 225, 238, 255)
SILVER_SHADOW = (135, 145, 160, 255)
LANCE_WOOD    = (120, 75, 40, 255)
RIBBON_RED    = (220, 45, 55, 255)

def draw_dragoon_frame(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    # Drop Shadow
    draw.ellipse([18, 52 + cy, 46, 59 + cy], fill=(0, 0, 0, 90))

    if row == 3: # UP (Back view)
        # Legs & Greaves
        lx1, lx2 = 23 + leg, 29 + leg
        rx1, rx2 = 35 - leg, 41 - leg
        draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=PURPLE_DARK, outline=OUTLINE)
        draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=PURPLE_DARK, outline=OUTLINE)

        # Spiked Dragon Scale Body
        draw.rectangle([21, 28 + cy, 43, 44 + cy], fill=PURPLE_SHADOW, outline=OUTLINE)
        draw.line([(32, 28 + cy), (32, 43 + cy)], fill=SILVER_SHADOW, width=2)

        # Dragon Helm (Back View)
        draw.rectangle([21, 14 + cy, 43, 29 + cy], fill=PURPLE_SHADOW, outline=OUTLINE)
        draw.polygon([(32, 4 + cy), (25, 14 + cy), (39, 14 + cy)], fill=GOLD_BASE, outline=OUTLINE)
    else:
        # Legs & Greaves
        lx1, lx2 = 23 + leg, 29 + leg
        rx1, rx2 = 35 - leg, 41 - leg
        draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=PURPLE_SHADOW, outline=OUTLINE)
        draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=PURPLE_SHADOW, outline=OUTLINE)
        draw.rectangle([lx1 + 1, 46 + cy, lx2 - 1, 54 + cy], fill=PURPLE_LIGHT)
        draw.rectangle([rx1 + 1, 46 + cy, rx2 - 1, 54 + cy], fill=PURPLE_LIGHT)

        # Spiked Dragon Scale Cuirass
        draw.rectangle([21, 28 + cy, 43, 44 + cy], fill=PURPLE_BASE, outline=OUTLINE)
        draw.rectangle([25, 30 + cy, 39, 42 + cy], fill=PURPLE_LIGHT)
        draw.line([(32, 29 + cy), (32, 43 + cy)], fill=SILVER_LIGHT, width=2)
        draw.rectangle([23, 40 + cy, 41, 43 + cy], fill=GOLD_BASE)

        # Shoulder Pauldrons (Spiked Dragon Scales)
        draw.polygon([(15, 26 + cy), (22, 28 + cy), (20, 36 + cy), (13, 32 + cy)], fill=PURPLE_HI, outline=OUTLINE)
        draw.polygon([(49, 26 + cy), (42, 28 + cy), (44, 36 + cy), (51, 32 + cy)], fill=PURPLE_HI, outline=OUTLINE)

        # Dragon Helm & Gold Horns
        draw.rectangle([21, 14 + cy, 43, 29 + cy], fill=PURPLE_BASE, outline=OUTLINE)
        draw.rectangle([23, 16 + cy, 41, 27 + cy], fill=PURPLE_LIGHT)
        # Gold Dragon Horn Crest
        draw.polygon([(32, 4 + cy), (25, 14 + cy), (39, 14 + cy)], fill=GOLD_LIGHT, outline=OUTLINE)
        draw.polygon([(32, 4 + cy), (32, 14 + cy), (39, 14 + cy)], fill=GOLD_HI)
        draw.polygon([(17, 10 + cy), (22, 16 + cy), (20, 20 + cy)], fill=GOLD_BASE, outline=OUTLINE)
        draw.polygon([(47, 10 + cy), (42, 16 + cy), (44, 20 + cy)], fill=GOLD_BASE, outline=OUTLINE)

        # Cyan Visor Glow
        if row == 0: # Down
            draw.rectangle([24, 21 + cy, 40, 24 + cy], fill=OUTLINE)
            draw.line([(26, 22 + cy), (38, 22 + cy)], fill=CYAN_BASE, width=2)
            draw.line([(28, 22 + cy), (36, 22 + cy)], fill=CYAN_HI, width=1)
        elif row == 1: # Left
            draw.rectangle([22, 21 + cy, 34, 24 + cy], fill=OUTLINE)
            draw.line([(24, 22 + cy), (32, 22 + cy)], fill=CYAN_BASE, width=2)
            draw.line([(25, 22 + cy), (30, 22 + cy)], fill=CYAN_HI, width=1)
        elif row == 2: # Right
            draw.rectangle([30, 21 + cy, 42, 24 + cy], fill=OUTLINE)
            draw.line([(32, 22 + cy), (40, 22 + cy)], fill=CYAN_BASE, width=2)
            draw.line([(34, 22 + cy), (39, 22 + cy)], fill=CYAN_HI, width=1)

    # Dragon Lance Weapon
    wx = 50 if (row == 0 or row == 2) else 14
    draw.line([(wx, 4 + cy), (wx, 56 + cy)], fill=LANCE_WOOD, width=3)
    draw.polygon([(wx, -2 + cy), (wx - 5, 12 + cy), (wx + 5, 12 + cy)], fill=SILVER_LIGHT, outline=OUTLINE)
    draw.polygon([(wx - 2, 0 + cy), (wx, -4 + cy), (wx + 2, 0 + cy)], fill=(255, 255, 255, 255))
    draw.polygon([(wx, 12 + cy), (wx - 8, 18 + cy), (wx + 2, 16 + cy)], fill=RIBBON_RED)

def generate_dragoon_spritesheet():
    dirs = ensure_dirs()
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    for row in range(4):
        for col in range(4):
            frame = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame)
            draw_dragoon_frame(draw, row, col)
            sheet.paste(frame, (col * 64, row * 64))
    save_sprite(sheet, "hero_dragoon.png", dirs)

if __name__ == "__main__":
    generate_dragoon_spritesheet()
