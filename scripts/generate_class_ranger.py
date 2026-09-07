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

OUTLINE = (12, 16, 24, 255)
AO_CREVICE = (6, 8, 14, 255)

# 7-Tone Color Ramps
FOREST_1 = (160, 245, 185, 255) # Rim Light Peak
FOREST_2 = (90, 185, 95, 255)   # Highlight
FOREST_3 = (60, 150, 68, 255)   # Light
FOREST_4 = (38, 112, 46, 255)   # Midtone Base
FOREST_5 = (22, 76, 30, 255)    # Form Shadow
FOREST_6 = (12, 48, 18, 255)    # Deep Crease
FOREST_7 = (4, 24, 8, 255)      # Core AO

LEATHER_3 = (145, 95, 50, 255)
LEATHER_4 = (110, 68, 32, 255)
LEATHER_5 = (75, 42, 18, 255)
LEATHER_6 = (46, 22, 8, 255)

BOW_BASE  = (145, 90, 42, 255)
BOW_LIGHT = (185, 125, 65, 255)
STRING_COLOR = (245, 250, 255, 240)
FLETCH_RED = (225, 45, 55, 255)
FLETCH_WHITE = (250, 250, 255, 255)
GOLD_BUCKLE = (240, 195, 45, 255)
SKIN_BASE = (245, 195, 155, 255)
EYE_GREEN = (30, 150, 75, 255)

def draw_ranger_frame(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 2 if col == 1 else (-2 if col == 3 else 0)
    cy = bob

    # Ground Drop Shadow with Dual-Layer Occlusion
    draw.ellipse([16, 51 + cy, 48, 60 + cy], fill=(0, 0, 0, 70))
    draw.ellipse([20, 53 + cy, 44, 58 + cy], fill=(0, 0, 0, 140))

    if row == 3: # UP (Back view)
        # Flowing Hood Cloak Back
        draw.polygon([(18, 12 + cy), (46, 12 + cy), (48, 52 + cy), (16, 52 + cy)], fill=FOREST_4, outline=OUTLINE)
        draw.polygon([(22, 16 + cy), (42, 16 + cy), (44, 50 + cy), (20, 50 + cy)], fill=FOREST_5)
        draw.polygon([(18, 44 + cy), (28, 52 + cy), (16, 52 + cy)], fill=FOREST_6)
        draw.line([(47, 13 + cy), (47, 51 + cy)], fill=FOREST_1, width=1) # Rim light

        # Quiver on Back
        draw.rectangle([37, 22 + cy, 44, 42 + cy], fill=LEATHER_4, outline=OUTLINE)
        draw.polygon([(38, 14 + cy), (41, 14 + cy), (39, 22 + cy)], fill=FLETCH_RED)
        draw.polygon([(41, 12 + cy), (44, 12 + cy), (42, 22 + cy)], fill=FLETCH_WHITE)

        # Boots
        lx1, lx2 = 22 + leg, 29 + leg
        rx1, rx2 = 35 - leg, 42 - leg
        draw.rectangle([lx1, 45 + cy, lx2, 56 + cy], fill=LEATHER_6, outline=OUTLINE)
        draw.rectangle([rx1, 45 + cy, rx2, 56 + cy], fill=LEATHER_6, outline=OUTLINE)
        draw.line([(lx1, 45 + cy), (lx2, 45 + cy)], fill=AO_CREVICE, width=1)
        draw.line([(rx1, 45 + cy), (rx2, 45 + cy)], fill=AO_CREVICE, width=1)
    else:
        # Quiver behind shoulder
        draw.rectangle([39, 22 + cy, 45, 40 + cy], fill=LEATHER_4, outline=OUTLINE)
        draw.polygon([(40, 14 + cy), (43, 14 + cy), (41, 22 + cy)], fill=FLETCH_RED)
        draw.polygon([(43, 12 + cy), (46, 12 + cy), (44, 22 + cy)], fill=FLETCH_WHITE)

        # Boots & Legs Stride
        lx1, lx2 = 22 + leg, 29 + leg
        rx1, rx2 = 35 - leg, 42 - leg
        draw.rectangle([lx1, 44 + cy, lx2, 56 + cy], fill=LEATHER_6, outline=OUTLINE)
        draw.rectangle([rx1, 44 + cy, rx2, 56 + cy], fill=LEATHER_6, outline=OUTLINE)
        draw.rectangle([lx1 + 1, 45 + cy, lx2 - 1, 53 + cy], fill=LEATHER_5)
        draw.rectangle([rx1 + 1, 45 + cy, rx2 - 1, 53 + cy], fill=LEATHER_5)
        draw.line([(lx1, 44 + cy), (lx2, 44 + cy)], fill=AO_CREVICE, width=1)
        draw.line([(rx1, 44 + cy), (rx2, 44 + cy)], fill=AO_CREVICE, width=1)

        # Leather Archer Armor & Harness
        draw.rectangle([23, 30 + cy, 41, 44 + cy], fill=LEATHER_4, outline=OUTLINE)
        draw.rectangle([25, 32 + cy, 39, 42 + cy], fill=LEATHER_3)
        draw.line([(24, 33 + cy), (40, 41 + cy)], fill=LEATHER_6, width=2)
        draw.line([(40, 33 + cy), (24, 41 + cy)], fill=LEATHER_6, width=2)
        draw.rectangle([30, 35 + cy, 34, 39 + cy], fill=GOLD_BUCKLE, outline=OUTLINE)

        # TIGHT ARTICULATED ARCHER ARMS, BRACERS & HANDS
        # Left Arm & Bow Holding Hand
        draw.polygon([(16, 27 + cy), (23, 28 + cy), (20, 37 + cy), (14, 33 + cy)], fill=FOREST_4, outline=OUTLINE)
        draw.rectangle([14, 33 + cy, 21, 43 + cy], fill=LEATHER_5, outline=OUTLINE) # Archer bracer
        draw.rectangle([14, 40 + cy, 20, 46 + cy], fill=LEATHER_3, outline=OUTLINE) # Archer glove hand
        draw.line([(14, 33 + cy), (21, 33 + cy)], fill=AO_CREVICE, width=1)

        # Right Arm & Arrow Drawing Hand
        draw.polygon([(48, 27 + cy), (41, 28 + cy), (44, 37 + cy), (50, 33 + cy)], fill=FOREST_4, outline=OUTLINE)
        draw.rectangle([43, 33 + cy, 50, 43 + cy], fill=LEATHER_5, outline=OUTLINE)
        draw.rectangle([44, 40 + cy, 50, 46 + cy], fill=LEATHER_3, outline=OUTLINE)
        draw.line([(43, 33 + cy), (50, 33 + cy)], fill=AO_CREVICE, width=1)

        # Green Hooded Cloak & Face
        draw.rectangle([22, 16 + cy, 42, 31 + cy], fill=FOREST_4, outline=OUTLINE)
        draw.polygon([(23, 20 + cy), (41, 20 + cy), (39, 31 + cy), (25, 31 + cy)], fill=FOREST_5)
        draw.line([(23, 17 + cy), (23, 30 + cy)], fill=FOREST_1, width=1) # Rim light
        draw.rectangle([25, 22 + cy, 39, 30 + cy], fill=SKIN_BASE)

        if row == 0:
            draw.rectangle([27, 25 + cy, 29, 28 + cy], fill=EYE_GREEN)
            draw.rectangle([35, 25 + cy, 37, 28 + cy], fill=EYE_GREEN)
            draw.point((28, 25 + cy), fill=FLETCH_WHITE)
            draw.point((36, 25 + cy), fill=FLETCH_WHITE)
        elif row == 1:
            draw.rectangle([25, 25 + cy, 27, 28 + cy], fill=EYE_GREEN)
            draw.point((26, 25 + cy), fill=FLETCH_WHITE)
        elif row == 2:
            draw.rectangle([37, 25 + cy, 39, 28 + cy], fill=EYE_GREEN)
            draw.point((38, 25 + cy), fill=FLETCH_WHITE)

        # Longbow with Drawn String
        wx = 15 if (row == 0 or row == 1) else 48
        draw.arc([wx - 6, 16 + cy, wx + 10, 52 + cy], 260, 100, fill=BOW_BASE, width=3)
        draw.arc([wx - 6, 16 + cy, wx + 10, 52 + cy], 260, 100, fill=BOW_LIGHT, width=1)
        draw.line([(wx + 2, 18 + cy), (wx + 2, 50 + cy)], fill=STRING_COLOR, width=1)
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

