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
STEEL_1 = (248, 252, 255, 255) # Specular Gleam
STEEL_2 = (215, 228, 242, 255) # Light Tone
STEEL_3 = (165, 180, 202, 255) # Midtone Base
STEEL_4 = (110, 125, 148, 255) # Shadow Tone
STEEL_5 = (68, 80, 102, 255)   # Deep Crevice

CAPE_1  = (110, 170, 255, 255) # Specular Peak
CAPE_2  = (70, 130, 230, 255)  # Light Fold
CAPE_3  = (38, 88, 185, 255)   # Midtone Base
CAPE_4  = (22, 56, 135, 255)   # Shadow Crease
CAPE_5  = (12, 34, 90, 255)    # Core Shadow

GOLD_1  = (255, 242, 160, 255)
GOLD_2  = (250, 215, 75, 255)
GOLD_3  = (218, 168, 30, 255)
GOLD_4  = (165, 120, 15, 255)
GOLD_5  = (102, 70, 6, 255)

SKIN_1  = (255, 235, 212, 255)
SKIN_2  = (252, 212, 178, 255)
SKIN_3  = (242, 188, 148, 255)
SKIN_4  = (198, 142, 108, 255)
SKIN_5  = (150, 98, 72, 255)

EYE_PUPIL = (20, 28, 42, 255)
WHITE_SPEC= (255, 255, 255, 255)

def draw_knight_frame(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    # Ground Drop Shadow
    draw.ellipse([16, 52 + cy, 48, 59 + cy], fill=(0, 0, 0, 90))

    if row == 3: # UP (Back view)
        # Flowing Cape Back
        draw.polygon([(14, 22 + cy), (50, 22 + cy), (54, 55 + cy), (10, 55 + cy)], fill=CAPE_3, outline=OUTLINE)
        draw.polygon([(14, 22 + cy), (32, 55 + cy), (10, 55 + cy)], fill=CAPE_4)
        draw.polygon([(10, 48 + cy), (20, 55 + cy), (10, 55 + cy)], fill=CAPE_5)
        draw.polygon([(36, 26 + cy), (50, 22 + cy), (52, 53 + cy), (42, 55 + cy)], fill=CAPE_2)

        # Greaves & Boots (Back view)
        lx1, lx2 = 22 + leg, 29 + leg
        rx1, rx2 = 35 - leg, 42 - leg
        draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=STEEL_4, outline=OUTLINE)
        draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=STEEL_4, outline=OUTLINE)
        draw.rectangle([lx1 + 1, 45 + cy, lx2 - 1, 53 + cy], fill=STEEL_5)
        draw.rectangle([rx1 + 1, 45 + cy, rx2 - 1, 53 + cy], fill=STEEL_5)

        # Helm (Back view)
        draw.rectangle([20, 11 + cy, 44, 27 + cy], fill=STEEL_3, outline=OUTLINE)
        draw.rectangle([22, 13 + cy, 42, 25 + cy], fill=STEEL_4)
        draw.line([(32, 11 + cy), (32, 27 + cy)], fill=GOLD_3, width=2)
        draw.line([(32, 11 + cy), (32, 20 + cy)], fill=GOLD_1, width=1)
    else:
        # Cape Wings
        draw.polygon([(14, 23 + cy), (48, 23 + cy), (52, 53 + cy), (12, 53 + cy)], fill=CAPE_3, outline=OUTLINE)
        draw.polygon([(14, 23 + cy), (26, 53 + cy), (12, 53 + cy)], fill=CAPE_4)
        draw.polygon([(38, 25 + cy), (48, 23 + cy), (50, 50 + cy), (42, 53 + cy)], fill=CAPE_2)

        # Greaves & Boots
        lx1, lx2 = 22 + leg, 29 + leg
        rx1, rx2 = 35 - leg, 42 - leg
        draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=STEEL_4, outline=OUTLINE)
        draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=STEEL_4, outline=OUTLINE)
        draw.rectangle([lx1 + 1, 45 + cy, lx2 - 1, 52 + cy], fill=STEEL_3)
        draw.rectangle([rx1 + 1, 45 + cy, rx2 - 1, 52 + cy], fill=STEEL_3)
        draw.line([(lx1 + 1, 45 + cy), (lx1 + 1, 51 + cy)], fill=STEEL_1, width=1)
        draw.line([(rx1 + 1, 45 + cy), (rx1 + 1, 51 + cy)], fill=STEEL_1, width=1)

        # Torso & Chestplate
        draw.rectangle([20, 25 + cy, 44, 44 + cy], fill=STEEL_3, outline=OUTLINE)
        draw.rectangle([23, 27 + cy, 41, 42 + cy], fill=STEEL_2)
        draw.rectangle([25, 28 + cy, 33, 38 + cy], fill=STEEL_1)
        draw.rectangle([20, 40 + cy, 44, 43 + cy], fill=GOLD_3, outline=OUTLINE)
        draw.line([(22, 41 + cy), (42, 41 + cy)], fill=GOLD_1, width=1)

        # Shoulder Pauldrons with Gold Trim
        draw.polygon([(14, 24 + cy), (22, 26 + cy), (20, 36 + cy), (12, 32 + cy)], fill=STEEL_2, outline=OUTLINE)
        draw.polygon([(15, 25 + cy), (21, 26 + cy), (19, 30 + cy)], fill=STEEL_1)
        draw.line([(12, 32 + cy), (20, 36 + cy)], fill=GOLD_2, width=2)

        draw.polygon([(50, 24 + cy), (42, 26 + cy), (44, 36 + cy), (52, 32 + cy)], fill=STEEL_3, outline=OUTLINE)
        draw.polygon([(49, 25 + cy), (43, 26 + cy), (45, 30 + cy)], fill=STEEL_2)
        draw.line([(52, 32 + cy), (44, 36 + cy)], fill=GOLD_3, width=2)

        # Helmet with Visor & Specular Gleam
        draw.rectangle([20, 11 + cy, 44, 27 + cy], fill=STEEL_3, outline=OUTLINE)
        draw.rectangle([23, 13 + cy, 41, 25 + cy], fill=STEEL_2)
        draw.rectangle([25, 14 + cy, 33, 20 + cy], fill=STEEL_1)
        draw.rectangle([23, 19 + cy, 41, 23 + cy], fill=OUTLINE)
        draw.line([(25, 21 + cy), (39, 21 + cy)], fill=STEEL_1, width=1)
        draw.line([(32, 11 + cy), (32, 18 + cy)], fill=GOLD_2, width=2)

        # Greatsword with Fuller & Guard
        wx = 51 if (row == 0 or row == 2) else 13
        draw.line([(wx, 6 + cy), (wx, 48 + cy)], fill=STEEL_2, width=3)
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
