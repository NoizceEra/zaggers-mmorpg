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
STEEL_SPEC    = (245, 250, 255, 255)
STEEL_LIGHT   = (210, 222, 238, 255)
STEEL_BASE    = (160, 175, 195, 255)
STEEL_SHADOW  = (105, 118, 140, 255)
STEEL_DARK    = (65, 75, 95, 255)

CAPE_HI       = (90, 150, 245, 255)
CAPE_LIGHT    = (60, 115, 215, 255)
CAPE_BASE     = (35, 80, 175, 255)
CAPE_SHADOW   = (20, 50, 125, 255)
CAPE_DARK     = (12, 30, 80, 255)

GOLD_HI       = (255, 230, 110, 255)
GOLD_LIGHT    = (245, 205, 60, 255)
GOLD_BASE     = (215, 165, 30, 255)
GOLD_SHADOW   = (165, 120, 15, 255)
GOLD_DARK     = (100, 70, 5, 255)

SKIN_HI       = (255, 225, 195, 255)
SKIN_BASE     = (245, 200, 165, 255)
SKIN_SHADOW   = (210, 160, 125, 255)
SKIN_DARK     = (175, 125, 95, 255)

EYE_COLOR     = (20, 30, 45, 255)

def draw_knight_frame(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    # Drop Shadow
    draw.ellipse([18, 52 + cy, 46, 59 + cy], fill=(0, 0, 0, 90))

    if row == 3:  # UP (Back view)
        # Flowing Cape Back
        draw.polygon([(16, 24 + cy), (48, 24 + cy), (52, 54 + cy), (12, 54 + cy)], fill=CAPE_BASE, outline=OUTLINE)
        draw.polygon([(16, 24 + cy), (32, 54 + cy), (12, 54 + cy)], fill=CAPE_SHADOW)
        draw.polygon([(36, 28 + cy), (48, 24 + cy), (50, 52 + cy), (42, 54 + cy)], fill=CAPE_LIGHT)

        # Legs (Back of boots)
        lx1, lx2 = 23 + leg, 29 + leg
        rx1, rx2 = 35 - leg, 41 - leg
        draw.rectangle([lx1, 46 + cy, lx2, 55 + cy], fill=STEEL_DARK, outline=OUTLINE)
        draw.rectangle([rx1, 46 + cy, rx2, 55 + cy], fill=STEEL_DARK, outline=OUTLINE)

        # Helm (Back view)
        draw.rectangle([21, 12 + cy, 43, 27 + cy], fill=STEEL_BASE, outline=OUTLINE)
        draw.rectangle([23, 14 + cy, 41, 25 + cy], fill=STEEL_SHADOW)
        draw.line([(32, 12 + cy), (32, 27 + cy)], fill=GOLD_BASE, width=2)
    else:
        # Cape Wings
        draw.polygon([(14, 24 + cy), (48, 24 + cy), (52, 53 + cy), (12, 53 + cy)], fill=CAPE_BASE, outline=OUTLINE)
        draw.polygon([(14, 24 + cy), (26, 53 + cy), (12, 53 + cy)], fill=CAPE_SHADOW)

        # Greaves & Legs
        lx1, lx2 = 23 + leg, 29 + leg
        rx1, rx2 = 35 - leg, 41 - leg
        draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=STEEL_DARK, outline=OUTLINE)
        draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=STEEL_DARK, outline=OUTLINE)
        draw.rectangle([lx1 + 1, 45 + cy, lx2 - 1, 53 + cy], fill=STEEL_BASE)
        draw.rectangle([rx1 + 1, 45 + cy, rx2 - 1, 53 + cy], fill=STEEL_BASE)
        draw.line([(lx1 + 1, 46 + cy), (lx1 + 1, 52 + cy)], fill=STEEL_SPEC, width=1)

        # Cuirass (Plate Chestpiece)
        draw.rectangle([21, 26 + cy, 43, 44 + cy], fill=STEEL_BASE, outline=OUTLINE)
        draw.rectangle([24, 28 + cy, 40, 42 + cy], fill=STEEL_LIGHT)
        draw.rectangle([26, 29 + cy, 32, 39 + cy], fill=STEEL_SPEC)
        draw.rectangle([21, 40 + cy, 43, 43 + cy], fill=GOLD_BASE, outline=OUTLINE)

        # Pauldrons (Shoulders with Specular Highlights)
        draw.polygon([(15, 25 + cy), (22, 27 + cy), (20, 36 + cy), (13, 32 + cy)], fill=STEEL_LIGHT, outline=OUTLINE)
        draw.line([(16, 26 + cy), (20, 28 + cy)], fill=STEEL_SPEC, width=1)
        draw.polygon([(49, 25 + cy), (42, 27 + cy), (44, 36 + cy), (51, 32 + cy)], fill=STEEL_LIGHT, outline=OUTLINE)
        draw.line([(48, 26 + cy), (44, 28 + cy)], fill=STEEL_SPEC, width=1)

        # Helm & Visor
        draw.rectangle([21, 12 + cy, 43, 27 + cy], fill=STEEL_BASE, outline=OUTLINE)
        draw.rectangle([24, 14 + cy, 40, 25 + cy], fill=STEEL_LIGHT)
        draw.line([(25, 14 + cy), (32, 14 + cy)], fill=STEEL_SPEC, width=2)
        # Dark Visor Slit with metallic trim
        draw.rectangle([24, 19 + cy, 40, 23 + cy], fill=OUTLINE)
        draw.line([(26, 21 + cy), (38, 21 + cy)], fill=STEEL_SPEC, width=1)

        # Claymore Broadsword
        wx = 50 if (row == 0 or row == 2) else 14
        draw.line([(wx, 8 + cy), (wx, 48 + cy)], fill=STEEL_LIGHT, width=3)
        draw.line([(wx - 1, 10 + cy), (wx - 1, 42 + cy)], fill=STEEL_SPEC, width=1)
        draw.polygon([(wx, 4 + cy), (wx - 4, 12 + cy), (wx + 4, 12 + cy)], fill=STEEL_SPEC)
        draw.rectangle([wx - 5, 38 + cy, wx + 5, 41 + cy], fill=GOLD_LIGHT, outline=OUTLINE)
        draw.ellipse([wx - 2, 48 + cy, wx + 2, 52 + cy], fill=GOLD_BASE)

def generate_knight_spritesheet():
    dirs = ensure_dirs()
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    for row in range(4):
        for col in range(4):
            frame = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame)
            draw_knight_frame(draw, row, col)
            sheet.paste(frame, (col * 64, row * 64))
    save_sprite(sheet, "hero_knight.png", dirs)

if __name__ == "__main__":
    generate_knight_spritesheet()
