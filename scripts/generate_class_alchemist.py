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
APRON_BROWN   = (155, 95, 45, 255)
APRON_LIGHT   = (185, 125, 70, 255)
BELT_DARK     = (75, 45, 25, 255)
BRASS_GOGGLES = (225, 175, 50, 255)
LENS_CYAN     = (60, 220, 230, 255)
FLASK_RED     = (235, 60, 60, 255)
FLASK_CYAN    = (60, 210, 210, 255)
FLASK_GREEN   = (70, 220, 80, 255)

SKIN_BASE     = (245, 200, 165, 255)
EYE_DARK      = (20, 30, 45, 255)

def draw_alchemist_frame(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    # Drop Shadow
    draw.ellipse([18, 52 + cy, 46, 59 + cy], fill=(0, 0, 0, 90))

    # Trousers & Boots
    lx1, lx2 = 23 + leg, 29 + leg
    rx1, rx2 = 35 - leg, 41 - leg
    draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=BELT_DARK, outline=OUTLINE)
    draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=BELT_DARK, outline=OUTLINE)

    # Leather Apron
    draw.rectangle([21, 27 + cy, 43, 45 + cy], fill=APRON_BROWN, outline=OUTLINE)
    draw.rectangle([25, 29 + cy, 39, 43 + cy], fill=APRON_LIGHT)

    # Potion Belt with Flasks
    draw.rectangle([19, 37 + cy, 45, 40 + cy], fill=BELT_DARK, outline=OUTLINE)
    draw.ellipse([22, 39 + cy, 27, 46 + cy], fill=FLASK_CYAN, outline=OUTLINE)
    draw.ellipse([30, 39 + cy, 35, 46 + cy], fill=FLASK_RED, outline=OUTLINE)
    draw.ellipse([38, 39 + cy, 43, 46 + cy], fill=FLASK_GREEN, outline=OUTLINE)

    # Head & Brass Tinker Goggles
    draw.rectangle([23, 14 + cy, 41, 28 + cy], fill=SKIN_BASE, outline=OUTLINE)
    # Goggles resting on forehead
    draw.rectangle([20, 11 + cy, 44, 17 + cy], fill=BRASS_GOGGLES, outline=OUTLINE)
    draw.ellipse([24, 12 + cy, 30, 16 + cy], fill=LENS_CYAN)
    draw.ellipse([34, 12 + cy, 40, 16 + cy], fill=LENS_CYAN)

    if row == 0:
        draw.rectangle([26, 21 + cy, 28, 24 + cy], fill=EYE_DARK)
        draw.rectangle([36, 21 + cy, 38, 24 + cy], fill=EYE_DARK)

    # Alchemist Flask in hand
    draw.ellipse([44, 30 + cy, 54, 42 + cy], fill=FLASK_CYAN, outline=OUTLINE)
    draw.rectangle([47, 26 + cy, 51, 30 + cy], fill=BRASS_GOGGLES)

def generate_alchemist_spritesheet():
    dirs = ensure_dirs()
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    for row in range(4):
        for col in range(4):
            frame = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame)
            draw_alchemist_frame(draw, row, col)
            sheet.paste(frame, (col * 64, row * 64))
    save_sprite(sheet, "hero_alchemist.png", dirs)

if __name__ == "__main__":
    generate_alchemist_spritesheet()
