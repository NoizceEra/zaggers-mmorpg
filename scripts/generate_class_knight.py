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
STEEL_1 = (255, 255, 255, 255) # Super Specular Glint
STEEL_2 = (230, 240, 252, 255) # Specular Highlight
STEEL_3 = (185, 200, 222, 255) # Light Tone
STEEL_4 = (140, 155, 178, 255) # Midtone Base
STEEL_5 = (90, 105, 128, 255)  # Form Shadow
STEEL_6 = (50, 62, 82, 255)    # Deep Shadow
STEEL_7 = (24, 30, 44, 255)    # Core AO

CAPE_1  = (165, 210, 255, 255) # Rim Light Peak
CAPE_2  = (95, 155, 250, 255)  # Light Fold
CAPE_3  = (50, 110, 215, 255)  # Base Light
CAPE_4  = (28, 72, 170, 255)   # Midtone Base
CAPE_5  = (16, 44, 120, 255)   # Form Shadow
CAPE_6  = (8, 24, 75, 255)     # Deep Crease
CAPE_7  = (4, 10, 42, 255)     # Core Shadow

GOLD_1  = (255, 255, 210, 255)
GOLD_2  = (255, 235, 130, 255)
GOLD_3  = (245, 195, 45, 255)
GOLD_4  = (200, 150, 20, 255)
GOLD_5  = (150, 105, 10, 255)
GOLD_6  = (95, 62, 5, 255)
GOLD_7  = (24, 16, 4, 255)

def draw_knight_frame(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    # Ground Drop Shadow with Dual-Layer Occlusion
    draw.ellipse([14, 51 + cy, 50, 60 + cy], fill=(0, 0, 0, 70))
    draw.ellipse([18, 53 + cy, 46, 58 + cy], fill=(0, 0, 0, 140))

    if row == 3: # UP (Back view)
        # Flowing Cape Back with 7-Tone Fold Depth & Rim Highlights
        draw.polygon([(14, 22 + cy), (50, 22 + cy), (55, 55 + cy), (9, 55 + cy)], fill=CAPE_4, outline=OUTLINE)
        draw.polygon([(14, 22 + cy), (32, 55 + cy), (9, 55 + cy)], fill=CAPE_5)
        draw.polygon([(9, 46 + cy), (20, 55 + cy), (9, 55 + cy)], fill=CAPE_6)
        draw.polygon([(9, 50 + cy), (15, 55 + cy), (9, 55 + cy)], fill=CAPE_7)
        draw.polygon([(36, 26 + cy), (50, 22 + cy), (53, 53 + cy), (42, 55 + cy)], fill=CAPE_3)
        draw.line([(51, 23 + cy), (54, 54 + cy)], fill=CAPE_1, width=1) # Rim light edge

        # Greaves & Boots (Back view)
        lx1, lx2 = 22 + leg, 29 + leg
        rx1, rx2 = 35 - leg, 42 - leg
        draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=STEEL_5, outline=OUTLINE)
        draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=STEEL_5, outline=OUTLINE)
        draw.rectangle([lx1 + 1, 45 + cy, lx2 - 1, 54 + cy], fill=STEEL_6)
        draw.rectangle([rx1 + 1, 45 + cy, rx2 - 1, 54 + cy], fill=STEEL_6)
        draw.line([(lx1, 44 + cy), (lx2, 44 + cy)], fill=AO_CREVICE, width=1)
        draw.line([(rx1, 44 + cy), (rx2, 44 + cy)], fill=AO_CREVICE, width=1)

        # Helm (Back view)
        draw.rectangle([20, 11 + cy, 44, 27 + cy], fill=STEEL_4, outline=OUTLINE)
        draw.rectangle([22, 13 + cy, 42, 25 + cy], fill=STEEL_5)
        draw.line([(21, 12 + cy), (21, 26 + cy)], fill=STEEL_2, width=1) # Rim light
        draw.line([(32, 11 + cy), (32, 27 + cy)], fill=GOLD_3, width=2)
        draw.line([(32, 11 + cy), (32, 19 + cy)], fill=GOLD_1, width=1)
    else:
        # Cape Wings
        draw.polygon([(14, 23 + cy), (48, 23 + cy), (53, 53 + cy), (11, 53 + cy)], fill=CAPE_4, outline=OUTLINE)
        draw.polygon([(14, 23 + cy), (26, 53 + cy), (11, 53 + cy)], fill=CAPE_5)
        draw.polygon([(38, 25 + cy), (48, 23 + cy), (51, 50 + cy), (42, 53 + cy)], fill=CAPE_3)
        draw.line([(12, 24 + cy), (12, 52 + cy)], fill=CAPE_1, width=1) # Rim light left
        draw.line([(52, 24 + cy), (52, 52 + cy)], fill=CAPE_1, width=1) # Rim light right

        # Greaves & Boots
        lx1, lx2 = 22 + leg, 29 + leg
        rx1, rx2 = 35 - leg, 42 - leg
        draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=STEEL_5, outline=OUTLINE)
        draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=STEEL_5, outline=OUTLINE)
        draw.rectangle([lx1 + 1, 45 + cy, lx2 - 1, 53 + cy], fill=STEEL_4)
        draw.rectangle([rx1 + 1, 45 + cy, rx2 - 1, 53 + cy], fill=STEEL_4)
        draw.line([(lx1 + 1, 45 + cy), (lx1 + 1, 52 + cy)], fill=STEEL_1, width=1)
        draw.line([(rx1 + 1, 45 + cy), (rx1 + 1, 52 + cy)], fill=STEEL_1, width=1)
        draw.line([(lx1, 44 + cy), (lx2, 44 + cy)], fill=AO_CREVICE, width=1)
        draw.line([(rx1, 44 + cy), (rx2, 44 + cy)], fill=AO_CREVICE, width=1)

        # Torso & Chestplate
        draw.rectangle([20, 25 + cy, 44, 44 + cy], fill=STEEL_4, outline=OUTLINE)
        draw.rectangle([22, 26 + cy, 42, 42 + cy], fill=STEEL_3)
        draw.polygon([(25, 27 + cy), (33, 27 + cy), (31, 38 + cy), (25, 38 + cy)], fill=STEEL_2)
        draw.line([(26, 28 + cy), (26, 36 + cy)], fill=STEEL_1, width=1) # Glint
        draw.line([(20, 25 + cy), (44, 25 + cy)], fill=AO_CREVICE, width=1) # Neck AO

        # Gold Belt & Buckle
        draw.rectangle([20, 40 + cy, 44, 43 + cy], fill=GOLD_4, outline=OUTLINE)
        draw.line([(21, 41 + cy), (43, 41 + cy)], fill=GOLD_2, width=1)
        draw.rectangle([29, 39 + cy, 35, 44 + cy], fill=GOLD_3, outline=OUTLINE)
        draw.rectangle([30, 40 + cy, 34, 43 + cy], fill=GOLD_1)

        # Shoulder Pauldrons with Gold Crest
        draw.polygon([(13, 24 + cy), (22, 26 + cy), (20, 36 + cy), (11, 32 + cy)], fill=STEEL_3, outline=OUTLINE)
        draw.polygon([(14, 25 + cy), (21, 26 + cy), (19, 30 + cy)], fill=STEEL_1)
        draw.line([(11, 32 + cy), (20, 36 + cy)], fill=GOLD_3, width=2)
        draw.line([(11, 32 + cy), (20, 36 + cy)], fill=GOLD_1, width=1)

        draw.polygon([(51, 24 + cy), (42, 26 + cy), (44, 36 + cy), (53, 32 + cy)], fill=STEEL_4, outline=OUTLINE)
        draw.polygon([(50, 25 + cy), (43, 26 + cy), (45, 30 + cy)], fill=STEEL_2)
        draw.line([(53, 32 + cy), (44, 36 + cy)], fill=GOLD_4, width=2)

        # Helmet with Visor & Super Specular Glint
        draw.rectangle([20, 11 + cy, 44, 27 + cy], fill=STEEL_4, outline=OUTLINE)
        draw.rectangle([22, 13 + cy, 42, 25 + cy], fill=STEEL_3)
        draw.polygon([(24, 13 + cy), (32, 13 + cy), (30, 19 + cy), (24, 19 + cy)], fill=STEEL_1)
        draw.rectangle([22, 19 + cy, 42, 23 + cy], fill=OUTLINE)
        draw.line([(24, 21 + cy), (40, 21 + cy)], fill=STEEL_2, width=1)
        draw.point((26, 21 + cy), fill=STEEL_1)
        draw.line([(32, 11 + cy), (32, 18 + cy)], fill=GOLD_3, width=2)
        draw.line([(32, 11 + cy), (32, 15 + cy)], fill=GOLD_1, width=1)

        # Greatsword with Dual Bevels & Pommel
        wx = 51 if (row == 0 or row == 2) else 13
        draw.line([(wx, 6 + cy), (wx, 48 + cy)], fill=STEEL_3, width=3)
        draw.line([(wx, 6 + cy), (wx, 46 + cy)], fill=STEEL_1, width=1)
        draw.line([(wx + 1, 8 + cy), (wx + 1, 46 + cy)], fill=STEEL_5, width=1)
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

