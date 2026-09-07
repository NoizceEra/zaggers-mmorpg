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
EMERALD_HI    = (95, 215, 135, 255)
EMERALD_LIGHT = (55, 175, 95, 255)
EMERALD_BASE  = (30, 130, 65, 255)
EMERALD_SHADOW= (18, 88, 42, 255)
EMERALD_DARK  = (10, 52, 24, 255)

LEATHER_HI    = (195, 135, 85, 255)
LEATHER_LIGHT = (160, 105, 58, 255)
LEATHER_BASE  = (125, 75, 38, 255)
LEATHER_SHADOW= (85, 48, 22, 255)
LEATHER_DARK  = (52, 28, 12, 255)

STEEL_SPEC    = (250, 255, 255, 255)
STEEL_LIGHT   = (225, 238, 245, 255)
STEEL_BASE    = (180, 195, 208, 255)
STEEL_SHADOW  = (120, 135, 150, 255)
STEEL_DARK    = (70, 82, 95, 255)

BELT_HI       = (75, 75, 85, 255)
BELT_LIGHT    = (52, 52, 60, 255)
BELT_BASE     = (35, 35, 42, 255)
BELT_SHADOW   = (22, 22, 28, 255)

GOLD_BASE     = (220, 175, 45, 255)
SKIN_BASE     = (245, 200, 165, 255)
EYE_DARK      = (20, 30, 45, 255)

def draw_thief_frame(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    # Drop Shadow
    draw.ellipse([18, 52 + cy, 46, 59 + cy], fill=(0, 0, 0, 90))

    if row == 3: # UP (Back view)
        # Emerald Hood & Back Cloak
        draw.polygon([(18, 12 + cy), (46, 12 + cy), (50, 52 + cy), (14, 52 + cy)], fill=EMERALD_BASE, outline=OUTLINE)
        draw.polygon([(22, 16 + cy), (42, 16 + cy), (46, 50 + cy), (18, 50 + cy)], fill=EMERALD_SHADOW)

        # Legs
        lx1, lx2 = 23 + leg, 29 + leg
        rx1, rx2 = 35 - leg, 41 - leg
        draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=LEATHER_DARK, outline=OUTLINE)
        draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=LEATHER_DARK, outline=OUTLINE)
    else:
        # Legs / Trousers
        lx1, lx2 = 23 + leg, 29 + leg
        rx1, rx2 = 35 - leg, 41 - leg
        draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=LEATHER_SHADOW, outline=OUTLINE)
        draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=LEATHER_SHADOW, outline=OUTLINE)
        draw.rectangle([lx1 + 1, 45 + cy, lx2 - 1, 53 + cy], fill=LEATHER_BASE)
        draw.rectangle([rx1 + 1, 45 + cy, rx2 - 1, 53 + cy], fill=LEATHER_BASE)

        # Leather Doublet
        draw.rectangle([21, 26 + cy, 43, 44 + cy], fill=LEATHER_BASE, outline=OUTLINE)
        draw.rectangle([25, 28 + cy, 39, 41 + cy], fill=LEATHER_LIGHT)
        draw.line([(32, 28 + cy), (32, 41 + cy)], fill=LEATHER_DARK, width=2)

        # Shadow Belt & Pouches
        draw.rectangle([20, 40 + cy, 44, 43 + cy], fill=BELT_BASE, outline=OUTLINE)
        draw.rectangle([30, 39 + cy, 34, 44 + cy], fill=GOLD_BASE, outline=OUTLINE)
        draw.rectangle([21, 41 + cy, 25, 45 + cy], fill=BELT_SHADOW)
        draw.rectangle([39, 41 + cy, 43, 45 + cy], fill=BELT_SHADOW)

        # Emerald Assassin Hood & Cloak
        draw.polygon([(18, 12 + cy), (46, 12 + cy), (44, 28 + cy), (20, 28 + cy)], fill=EMERALD_BASE, outline=OUTLINE)
        draw.polygon([(20, 14 + cy), (44, 14 + cy), (42, 26 + cy)], fill=EMERALD_LIGHT)
        draw.rectangle([24, 17 + cy, 40, 26 + cy], fill=SKIN_BASE)

        if row == 0:
            draw.rectangle([26, 20 + cy, 28, 23 + cy], fill=EYE_DARK)
            draw.rectangle([36, 20 + cy, 38, 23 + cy], fill=EYE_DARK)
        elif row == 1:
            draw.rectangle([24, 20 + cy, 27, 23 + cy], fill=EYE_DARK)
        elif row == 2:
            draw.rectangle([37, 20 + cy, 40, 23 + cy], fill=EYE_DARK)

        # Dual Curved Daggers
        # Left Hand Dagger
        draw.line([(12, 26 + cy), (12, 44 + cy)], fill=STEEL_LIGHT, width=2)
        draw.line([(11, 26 + cy), (11, 42 + cy)], fill=STEEL_SPEC, width=1)
        draw.rectangle([9, 41 + cy, 15, 43 + cy], fill=GOLD_BASE)
        # Right Hand Dagger
        draw.line([(52, 26 + cy), (52, 44 + cy)], fill=STEEL_LIGHT, width=2)
        draw.line([(53, 26 + cy), (53, 42 + cy)], fill=STEEL_SPEC, width=1)
        draw.rectangle([49, 41 + cy, 55, 43 + cy], fill=GOLD_BASE)

def generate_thief_spritesheet():
    dirs = ensure_dirs()
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    for row in range(4):
        for col in range(4):
            frame = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame)
            draw_thief_frame(draw, row, col)
            sheet.paste(frame, (col * 64, row * 64))
    save_sprite(sheet, "hero_thief.png", dirs)

if __name__ == "__main__":
    generate_thief_spritesheet()
