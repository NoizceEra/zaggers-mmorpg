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
GOLD_SPEC     = (255, 250, 180, 255)
GOLD_HI       = (255, 230, 110, 255)
GOLD_LIGHT    = (245, 205, 60, 255)
GOLD_BASE     = (215, 165, 30, 255)
GOLD_SHADOW   = (165, 120, 15, 255)

CAPE_BLUE     = (35, 95, 195, 255)
CAPE_DARK     = (20, 60, 135, 255)
SHIELD_BLUE   = (30, 80, 170, 255)
STEEL_SWORD   = (230, 235, 245, 255)

def draw_paladin_frame(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    # Drop Shadow
    draw.ellipse([18, 52 + cy, 46, 59 + cy], fill=(0, 0, 0, 90))

    # Royal Blue Cape
    draw.polygon([(16, 24 + cy), (48, 24 + cy), (51, 54 + cy), (13, 54 + cy)], fill=CAPE_BLUE, outline=OUTLINE)
    draw.polygon([(16, 24 + cy), (32, 54 + cy), (13, 54 + cy)], fill=CAPE_DARK)

    # Golden Boots & Leg Plate
    lx1, lx2 = 23 + leg, 29 + leg
    rx1, rx2 = 35 - leg, 41 - leg
    draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=GOLD_BASE, outline=OUTLINE)
    draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=GOLD_BASE, outline=OUTLINE)
    draw.rectangle([lx1 + 1, 45 + cy, lx2 - 1, 53 + cy], fill=GOLD_LIGHT)
    draw.rectangle([rx1 + 1, 45 + cy, rx2 - 1, 53 + cy], fill=GOLD_LIGHT)

    # Holy Golden Cuirass
    draw.rectangle([21, 26 + cy, 43, 44 + cy], fill=GOLD_BASE, outline=OUTLINE)
    draw.rectangle([25, 28 + cy, 39, 42 + cy], fill=GOLD_LIGHT)
    draw.polygon([(32, 28 + cy), (28, 36 + cy), (36, 36 + cy)], fill=GOLD_SHADOW) # Cross emblem

    # Winged Templar Helmet
    draw.rectangle([21, 12 + cy, 43, 27 + cy], fill=GOLD_BASE, outline=OUTLINE)
    draw.rectangle([24, 14 + cy, 40, 25 + cy], fill=GOLD_LIGHT)
    # Golden Wings on Helm
    draw.polygon([(14, 8 + cy), (21, 12 + cy), (18, 22 + cy)], fill=GOLD_SPEC, outline=OUTLINE)
    draw.polygon([(50, 8 + cy), (43, 12 + cy), (46, 22 + cy)], fill=GOLD_SPEC, outline=OUTLINE)

    if row != 3: # Visor
        draw.rectangle([24, 19 + cy, 40, 23 + cy], fill=OUTLINE)
        draw.line([(26, 21 + cy), (38, 21 + cy)], fill=GOLD_SPEC, width=1)

    # Holy Winged Tower Shield (Left hand)
    draw.polygon([(6, 22 + cy), (20, 22 + cy), (18, 48 + cy), (8, 48 + cy)], fill=SHIELD_BLUE, outline=OUTLINE)
    draw.polygon([(13, 24 + cy), (13, 46 + cy), (8, 35 + cy), (18, 35 + cy)], fill=GOLD_BASE, outline=OUTLINE)

    # Holy Longsword (Right hand)
    if row == 0 or row == 2:
        draw.line([(48, 14 + cy), (48, 48 + cy)], fill=STEEL_SWORD, width=3)
        draw.polygon([(48, 8 + cy), (45, 16 + cy), (51, 16 + cy)], fill=(255, 255, 255, 255))
        draw.rectangle([44, 38 + cy, 52, 41 + cy], fill=GOLD_BASE, outline=OUTLINE)

def generate_paladin_spritesheet():
    dirs = ensure_dirs()
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    for row in range(4):
        for col in range(4):
            frame = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame)
            draw_paladin_frame(draw, row, col)
            sheet.paste(frame, (col * 64, row * 64))
    save_sprite(sheet, "hero_paladin.png", dirs)

if __name__ == "__main__":
    generate_paladin_spritesheet()
