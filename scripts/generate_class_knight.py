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

# 7-Tone Steel & Armor Ramps
STEEL_1 = (255, 255, 255, 255) # Super Specular Glint
STEEL_2 = (230, 240, 252, 255) # Specular Highlight
STEEL_3 = (185, 200, 222, 255) # Light Tone
STEEL_4 = (140, 155, 178, 255) # Midtone Base
STEEL_5 = (90, 105, 128, 255)  # Form Shadow
STEEL_6 = (50, 62, 82, 255)    # Deep Shadow
STEEL_7 = (24, 30, 44, 255)    # Core AO

CAPE_1  = (165, 210, 255, 255)
CAPE_2  = (95, 155, 250, 255)
CAPE_3  = (50, 110, 215, 255)
CAPE_4  = (28, 72, 170, 255)
CAPE_5  = (16, 44, 120, 255)

GOLD_1  = (255, 255, 210, 255)
GOLD_2  = (255, 235, 130, 255)
GOLD_3  = (245, 195, 45, 255)
GOLD_4  = (200, 150, 20, 255)

SKIN_BASE = (245, 195, 155, 255)

def draw_knight_frame(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 4 if col == 1 else (-4 if col == 3 else 0)
    cy = bob

    # Ground Drop Shadow
    draw.ellipse([12, 51 + cy, 52, 60 + cy], fill=(0, 0, 0, 70))
    draw.ellipse([16, 53 + cy, 48, 58 + cy], fill=(0, 0, 0, 140))

    if row == 3: # UP (Back view)
        # Flowing Cape Back
        draw.polygon([(14, 22 + cy), (50, 22 + cy), (55, 55 + cy), (9, 55 + cy)], fill=CAPE_4, outline=OUTLINE)
        draw.polygon([(14, 22 + cy), (32, 55 + cy), (9, 55 + cy)], fill=CAPE_5)

        # Articulated Legs & Steel Greaves (Back)
        lx1, lx2 = 21 + leg, 29 + leg
        rx1, rx2 = 35 - leg, 43 - leg
        draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=STEEL_5, outline=OUTLINE)
        draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=STEEL_5, outline=OUTLINE)
        draw.line([(lx1, 44 + cy), (lx2, 44 + cy)], fill=AO_CREVICE, width=1)
        draw.line([(rx1, 44 + cy), (rx2, 44 + cy)], fill=AO_CREVICE, width=1)

        # Back Armor & Helm
        draw.rectangle([20, 11 + cy, 44, 27 + cy], fill=STEEL_4, outline=OUTLINE)
        draw.line([(32, 11 + cy), (32, 27 + cy)], fill=GOLD_3, width=2)
    else:
        # Cape Wings behind shoulders
        draw.polygon([(14, 23 + cy), (48, 23 + cy), (53, 53 + cy), (11, 53 + cy)], fill=CAPE_4, outline=OUTLINE)
        draw.polygon([(14, 23 + cy), (26, 53 + cy), (11, 53 + cy)], fill=CAPE_5)

        # Articulated Legs, Thighs & Steel Greaves
        lx1, lx2 = 20 + leg, 28 + leg
        rx1, rx2 = 36 - leg, 44 - leg

        # Left Leg
        draw.rectangle([lx1, 44 + cy, lx2, 56 + cy], fill=STEEL_5, outline=OUTLINE)
        draw.rectangle([lx1 + 1, 45 + cy, lx2 - 1, 53 + cy], fill=STEEL_4)
        draw.line([(lx1 + 1, 45 + cy), (lx1 + 1, 52 + cy)], fill=STEEL_1, width=1) # Kneecap ridge
        draw.rectangle([lx1, 48 + cy, lx2, 50 + cy], fill=STEEL_2) # Knee joint plate

        # Right Leg
        draw.rectangle([rx1, 44 + cy, rx2, 56 + cy], fill=STEEL_5, outline=OUTLINE)
        draw.rectangle([rx1 + 1, 45 + cy, rx2 - 1, 53 + cy], fill=STEEL_4)
        draw.line([(rx1 + 1, 45 + cy), (rx1 + 1, 52 + cy)], fill=STEEL_1, width=1)
        draw.rectangle([rx1, 48 + cy, rx2, 50 + cy], fill=STEEL_2)

        draw.line([(lx1, 44 + cy), (lx2, 44 + cy)], fill=AO_CREVICE, width=1)
        draw.line([(rx1, 44 + cy), (rx2, 44 + cy)], fill=AO_CREVICE, width=1)

        # Torso & Chestplate
        draw.rectangle([22, 25 + cy, 42, 44 + cy], fill=STEEL_4, outline=OUTLINE)
        draw.rectangle([24, 26 + cy, 40, 42 + cy], fill=STEEL_3)
        draw.line([(22, 25 + cy), (42, 25 + cy)], fill=AO_CREVICE, width=1)

        # Gold Belt & Buckle
        draw.rectangle([21, 40 + cy, 43, 43 + cy], fill=GOLD_4, outline=OUTLINE)
        draw.rectangle([29, 39 + cy, 35, 44 + cy], fill=GOLD_3, outline=OUTLINE)
        draw.rectangle([30, 40 + cy, 34, 43 + cy], fill=GOLD_1)

        # ARTICULATED ARMS, GAUNTLETS & HANDS
        # Left Arm & Steel Gauntlet
        draw.polygon([(13, 25 + cy), (21, 26 + cy), (18, 36 + cy), (10, 32 + cy)], fill=STEEL_3, outline=OUTLINE) # Pauldron
        draw.rectangle([10, 33 + cy, 18, 43 + cy], fill=STEEL_4, outline=OUTLINE) # Forearm gauntlet
        draw.rectangle([11, 40 + cy, 17, 46 + cy], fill=STEEL_2, outline=OUTLINE) # Steel glove hand
        draw.line([(10, 33 + cy), (18, 33 + cy)], fill=AO_CREVICE, width=1)

        # Right Arm & Steel Gauntlet
        draw.polygon([(51, 25 + cy), (43, 26 + cy), (46, 36 + cy), (54, 32 + cy)], fill=STEEL_4, outline=OUTLINE) # Pauldron
        draw.rectangle([46, 33 + cy, 54, 43 + cy], fill=STEEL_5, outline=OUTLINE) # Forearm gauntlet
        draw.rectangle([47, 40 + cy, 53, 46 + cy], fill=STEEL_3, outline=OUTLINE) # Steel glove hand
        draw.line([(46, 33 + cy), (54, 33 + cy)], fill=AO_CREVICE, width=1)

        # Helmet with Visor & Super Specular Glint
        draw.rectangle([20, 11 + cy, 44, 27 + cy], fill=STEEL_4, outline=OUTLINE)
        draw.rectangle([22, 13 + cy, 42, 25 + cy], fill=STEEL_3)
        draw.rectangle([22, 19 + cy, 42, 23 + cy], fill=OUTLINE)
        draw.line([(24, 21 + cy), (40, 21 + cy)], fill=STEEL_2, width=1)
        draw.line([(32, 11 + cy), (32, 18 + cy)], fill=GOLD_3, width=2)
        draw.line([(32, 11 + cy), (32, 15 + cy)], fill=GOLD_1, width=1)

        # Greatsword with Dual Bevels
        wx = 51 if (row == 0 or row == 2) else 13
        draw.line([(wx, 6 + cy), (wx, 48 + cy)], fill=STEEL_3, width=3)
        draw.line([(wx, 6 + cy), (wx, 46 + cy)], fill=STEEL_1, width=1)
        draw.polygon([(wx, 2 + cy), (wx - 4, 10 + cy), (wx + 4, 10 + cy)], fill=STEEL_1)
        draw.rectangle([wx - 5, 38 + cy, wx + 5, 41 + cy], fill=GOLD_3, outline=OUTLINE)
        draw.ellipse([wx - 2, 47 + cy, wx + 2, 51 + cy], fill=GOLD_2, outline=OUTLINE)

def create_knight_spritesheet():
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    for row in range(4):
        for col in range(4):
            frame = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame)
            draw_knight_frame(draw, row, col)
            sheet.paste(frame, (col * 64, row * 64))
    return sheet

def main():
    dirs = ensure_dirs()
    sheet = create_knight_spritesheet()
    save_sprite(sheet, "hero_knight.png", dirs)

if __name__ == "__main__":
    main()


