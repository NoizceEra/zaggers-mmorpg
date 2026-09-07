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
GOLD_1 = (255, 255, 210, 255) # Super Glint
GOLD_2 = (255, 235, 130, 255) # Specular
GOLD_3 = (245, 195, 45, 255)  # Light Tone
GOLD_4 = (215, 165, 30, 255)  # Midtone Base
GOLD_5 = (165, 120, 15, 255)  # Form Shadow
GOLD_6 = (105, 70, 5, 255)    # Deep Shadow
GOLD_7 = (32, 20, 4, 255)     # Core AO

CAPE_1 = (165, 210, 255, 255)
CAPE_2 = (95, 155, 250, 255)
CAPE_3 = (50, 110, 215, 255)
CAPE_4 = (28, 72, 170, 255)
CAPE_5 = (16, 44, 120, 255)

SHIELD_BLUE = (30, 80, 170, 255)
STEEL_SWORD = (245, 250, 255, 255)

def draw_paladin_frame(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 2 if col == 1 else (-2 if col == 3 else 0)
    cy = bob

    # Ground Drop Shadow with Dual-Layer Occlusion
    draw.ellipse([16, 51 + cy, 48, 60 + cy], fill=(0, 0, 0, 70))
    draw.ellipse([20, 53 + cy, 44, 58 + cy], fill=(0, 0, 0, 140))

    # Royal Blue Cape
    draw.polygon([(16, 24 + cy), (48, 24 + cy), (50, 54 + cy), (14, 54 + cy)], fill=CAPE_3, outline=OUTLINE)
    draw.polygon([(16, 24 + cy), (32, 54 + cy), (14, 54 + cy)], fill=CAPE_4)
    draw.line([(49, 25 + cy), (50, 53 + cy)], fill=CAPE_1, width=1) # Rim light

    # Golden Boots & Leg Plate Stride
    lx1, lx2 = 22 + leg, 29 + leg
    rx1, rx2 = 35 - leg, 42 - leg
    draw.rectangle([lx1, 44 + cy, lx2, 56 + cy], fill=GOLD_5, outline=OUTLINE)
    draw.rectangle([rx1, 44 + cy, rx2, 56 + cy], fill=GOLD_5, outline=OUTLINE)
    draw.rectangle([lx1 + 1, 45 + cy, lx2 - 1, 53 + cy], fill=GOLD_3)
    draw.rectangle([rx1 + 1, 45 + cy, rx2 - 1, 53 + cy], fill=GOLD_3)
    draw.rectangle([lx1, 48 + cy, lx2, 50 + cy], fill=GOLD_1) # Knee joint plate
    draw.rectangle([rx1, 48 + cy, rx2, 50 + cy], fill=GOLD_1)
    draw.line([(lx1, 44 + cy), (lx2, 44 + cy)], fill=AO_CREVICE, width=1)
    draw.line([(rx1, 44 + cy), (rx2, 44 + cy)], fill=AO_CREVICE, width=1)

    # Holy Golden Cuirass
    draw.rectangle([23, 26 + cy, 41, 44 + cy], fill=GOLD_4, outline=OUTLINE)
    draw.rectangle([25, 28 + cy, 39, 42 + cy], fill=GOLD_3)
    draw.polygon([(32, 28 + cy), (28, 36 + cy), (36, 36 + cy)], fill=GOLD_6) # Cross emblem
    draw.line([(24, 27 + cy), (24, 43 + cy)], fill=GOLD_1, width=1) # Rim light

    # TIGHT ARTICULATED ARMS & GOLDEN GAUNTLETS
    # Left Arm & Golden Gauntlet
    draw.polygon([(16, 25 + cy), (23, 26 + cy), (20, 36 + cy), (14, 32 + cy)], fill=GOLD_3, outline=OUTLINE)
    draw.rectangle([14, 33 + cy, 21, 43 + cy], fill=GOLD_4, outline=OUTLINE)
    draw.rectangle([14, 40 + cy, 20, 46 + cy], fill=GOLD_2, outline=OUTLINE)
    draw.line([(14, 33 + cy), (21, 33 + cy)], fill=AO_CREVICE, width=1)

    # Right Arm & Golden Gauntlet
    draw.polygon([(48, 25 + cy), (41, 26 + cy), (44, 36 + cy), (50, 32 + cy)], fill=GOLD_4, outline=OUTLINE)
    draw.rectangle([43, 33 + cy, 50, 43 + cy], fill=GOLD_5, outline=OUTLINE)
    draw.rectangle([44, 40 + cy, 50, 46 + cy], fill=GOLD_3, outline=OUTLINE)
    draw.line([(43, 33 + cy), (50, 33 + cy)], fill=AO_CREVICE, width=1)

    # Winged Templar Helmet
    draw.rectangle([21, 12 + cy, 43, 27 + cy], fill=GOLD_4, outline=OUTLINE)
    draw.rectangle([23, 14 + cy, 41, 25 + cy], fill=GOLD_3)
    draw.polygon([(12, 4 + cy), (22, 12 + cy), (18, 20 + cy)], fill=GOLD_1, outline=OUTLINE) # Left wing
    draw.polygon([(52, 4 + cy), (42, 12 + cy), (46, 20 + cy)], fill=GOLD_2, outline=OUTLINE) # Right wing
    draw.rectangle([24, 19 + cy, 40, 23 + cy], fill=OUTLINE) # Visor slot
    draw.line([(26, 21 + cy), (38, 21 + cy)], fill=GOLD_1, width=1)

    # Tower Shield with Golden Cross (Left hand)
    if row == 0 or row == 1:
        draw.rectangle([11, 24 + cy, 21, 48 + cy], fill=SHIELD_BLUE, outline=OUTLINE)
        draw.line([(16, 24 + cy), (16, 48 + cy)], fill=GOLD_3, width=2)
        draw.line([(11, 36 + cy), (21, 36 + cy)], fill=GOLD_3, width=2)

    # Holy Longsword (Right hand)
    wx = 48 if (row == 0 or row == 2) else 16
    draw.line([(wx, 8 + cy), (wx, 48 + cy)], fill=STEEL_SWORD, width=3)
    draw.line([(wx, 8 + cy), (wx, 46 + cy)], fill=GOLD_1, width=1)
    draw.rectangle([wx - 5, 38 + cy, wx + 5, 41 + cy], fill=GOLD_3, outline=OUTLINE)

def create_paladin_spritesheet():
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    for row in range(4):
        for col in range(4):
            frame = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame)
            draw_paladin_frame(draw, row, col)
            sheet.paste(frame, (col * 64, row * 64))
    return sheet

def main():
    dirs = ensure_dirs()
    sheet = create_paladin_spritesheet()
    save_sprite(sheet, "hero_paladin.png", dirs)

if __name__ == "__main__":
    main()
