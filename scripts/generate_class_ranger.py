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
FOREST_HI     = (90, 185, 95, 255)
FOREST_LIGHT  = (60, 150, 68, 255)
FOREST_BASE   = (38, 112, 46, 255)
FOREST_SHADOW = (22, 76, 30, 255)
FOREST_DARK   = (12, 48, 18, 255)

LEATHER_HI    = (185, 128, 75, 255)
LEATHER_LIGHT = (150, 98, 52, 255)
LEATHER_BASE  = (118, 70, 32, 255)
LEATHER_SHADOW= (80, 44, 18, 255)
LEATHER_DARK  = (48, 24, 8, 255)

BOW_HI        = (205, 145, 82, 255)
BOW_LIGHT     = (170, 112, 55, 255)
BOW_BASE      = (132, 80, 34, 255)
BOW_SHADOW    = (90, 50, 18, 255)
BOW_DARK      = (55, 28, 8, 255)

STRING_COLOR  = (230, 235, 240, 220)
FLETCH_RED    = (210, 45, 45, 255)
FLETCH_WHITE  = (240, 240, 245, 255)
GOLD_BUCKLE   = (220, 175, 50, 255)
SKIN_BASE     = (245, 205, 170, 255)
EYE_GREEN     = (30, 140, 70, 255)

def draw_ranger_frame(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    # Drop Shadow
    draw.ellipse([18, 52 + cy, 46, 59 + cy], fill=(0, 0, 0, 90))

    if row == 3: # UP (Back view)
        # Flowing Hood Cloak Back
        draw.polygon([(18, 12 + cy), (46, 12 + cy), (50, 52 + cy), (14, 52 + cy)], fill=FOREST_BASE, outline=OUTLINE)
        draw.polygon([(22, 16 + cy), (42, 16 + cy), (46, 50 + cy), (18, 50 + cy)], fill=FOREST_SHADOW)

        # Quiver on Back
        draw.rectangle([38, 22 + cy, 46, 42 + cy], fill=LEATHER_BASE, outline=OUTLINE)
        draw.polygon([(39, 14 + cy), (42, 14 + cy), (40, 22 + cy)], fill=FLETCH_RED)
        draw.polygon([(42, 12 + cy), (45, 12 + cy), (43, 22 + cy)], fill=FLETCH_WHITE)

        # Boots
        lx1, lx2 = 23 + leg, 29 + leg
        rx1, rx2 = 35 - leg, 41 - leg
        draw.rectangle([lx1, 45 + cy, lx2, 56 + cy], fill=LEATHER_DARK, outline=OUTLINE)
        draw.rectangle([rx1, 45 + cy, rx2, 56 + cy], fill=LEATHER_DARK, outline=OUTLINE)
    else:
        # Quiver behind shoulder
        draw.rectangle([40, 22 + cy, 47, 40 + cy], fill=LEATHER_BASE, outline=OUTLINE)
        draw.polygon([(41, 14 + cy), (44, 14 + cy), (42, 22 + cy)], fill=FLETCH_RED)
        draw.polygon([(44, 12 + cy), (47, 12 + cy), (45, 22 + cy)], fill=FLETCH_WHITE)

        # Boots & Legs
        lx1, lx2 = 23 + leg, 29 + leg
        rx1, rx2 = 35 - leg, 41 - leg
        draw.rectangle([lx1, 45 + cy, lx2, 56 + cy], fill=LEATHER_DARK, outline=OUTLINE)
        draw.rectangle([rx1, 45 + cy, rx2, 56 + cy], fill=LEATHER_DARK, outline=OUTLINE)

        # Leather Archer Armor & Harness
        draw.rectangle([23, 30 + cy, 41, 44 + cy], fill=LEATHER_BASE, outline=OUTLINE)
        draw.rectangle([26, 32 + cy, 38, 42 + cy], fill=LEATHER_LIGHT)
        draw.line([(24, 33 + cy), (40, 41 + cy)], fill=LEATHER_DARK, width=2)
        draw.line([(40, 33 + cy), (24, 41 + cy)], fill=LEATHER_DARK, width=2)
        draw.rectangle([30, 35 + cy, 34, 39 + cy], fill=GOLD_BUCKLE, outline=OUTLINE)

        # Green Hooded Cloak & Face
        draw.rectangle([22, 16 + cy, 42, 31 + cy], fill=FOREST_BASE, outline=OUTLINE)
        draw.polygon([(23, 20 + cy), (41, 20 + cy), (39, 31 + cy), (25, 31 + cy)], fill=FOREST_SHADOW)
        draw.rectangle([25, 22 + cy, 39, 30 + cy], fill=SKIN_BASE)

        if row == 0:
            draw.rectangle([27, 25 + cy, 29, 28 + cy], fill=EYE_GREEN)
            draw.rectangle([35, 25 + cy, 37, 28 + cy], fill=EYE_GREEN)
        elif row == 1:
            draw.rectangle([25, 25 + cy, 27, 28 + cy], fill=EYE_GREEN)
        elif row == 2:
            draw.rectangle([37, 25 + cy, 39, 28 + cy], fill=EYE_GREEN)

        # Longbow with Drawn String
        wx = 10 if (row == 0 or row == 1) else 50
        draw.arc([wx - 6, 16 + cy, wx + 10, 52 + cy], 260, 100, fill=BOW_BASE, width=3)
        draw.line([(wx + 2, 18 + cy), (wx + 2, 50 + cy)], fill=STRING_COLOR, width=1)
        # Drawn string notch
        draw.line([(wx + 2, 18 + cy), (wx + 8, 34 + cy)], fill=STRING_COLOR, width=1)
        draw.line([(wx + 8, 34 + cy), (wx + 2, 50 + cy)], fill=STRING_COLOR, width=1)

def generate_ranger_spritesheet():
    dirs = ensure_dirs()
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    for row in range(4):
        for col in range(4):
            frame = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame)
            draw_ranger_frame(draw, row, col)
            sheet.paste(frame, (col * 64, row * 64))
    save_sprite(sheet, "hero_ranger.png", dirs)

if __name__ == "__main__":
    generate_ranger_spritesheet()
