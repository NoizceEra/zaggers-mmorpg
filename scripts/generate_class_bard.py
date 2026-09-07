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
DOUBLET_CRIMSON = (205, 45, 65, 255)
DOUBLET_LIGHT   = (235, 80, 100, 255)
TROUSERS_GREEN  = (45, 135, 75, 255)
CAP_GREEN       = (35, 115, 60, 255)
FEATHER_WHITE   = (250, 250, 255, 255)
LUTE_WOOD       = (180, 110, 45, 255)
LUTE_LIGHT      = (215, 145, 75, 255)
LUTE_DARK       = (110, 60, 25, 255)

SKIN_BASE       = (245, 200, 165, 255)
EYE_DARK        = (20, 30, 45, 255)

def draw_bard_frame(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    # Drop Shadow
    draw.ellipse([18, 52 + cy, 46, 59 + cy], fill=(0, 0, 0, 90))

    # Trousers & Boots
    lx1, lx2 = 23 + leg, 29 + leg
    rx1, rx2 = 35 - leg, 41 - leg
    draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=TROUSERS_GREEN, outline=OUTLINE)
    draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=TROUSERS_GREEN, outline=OUTLINE)

    # Crimson Doublet & Gold Buttons
    draw.rectangle([21, 27 + cy, 43, 44 + cy], fill=DOUBLET_CRIMSON, outline=OUTLINE)
    draw.rectangle([25, 29 + cy, 39, 42 + cy], fill=DOUBLET_LIGHT)
    for button_y in range(30, 42, 4):
        draw.rectangle([31, button_y + cy, 33, button_y + 2 + cy], fill=(240, 200, 50, 255))

    # Head & Feathered Minstrel Cap
    draw.rectangle([23, 14 + cy, 41, 28 + cy], fill=SKIN_BASE, outline=OUTLINE)
    draw.polygon([(18, 10 + cy), (46, 10 + cy), (42, 17 + cy), (22, 17 + cy)], fill=CAP_GREEN, outline=OUTLINE)
    # White Plume Feather
    draw.polygon([(12, 2 + cy), (20, 8 + cy), (16, 16 + cy)], fill=FEATHER_WHITE, outline=OUTLINE)

    if row == 0:
        draw.rectangle([26, 21 + cy, 28, 24 + cy], fill=EYE_DARK)
        draw.rectangle([36, 21 + cy, 38, 24 + cy], fill=EYE_DARK)

    # Acoustic Lute / Harp
    draw.ellipse([36, 28 + cy, 54, 46 + cy], fill=LUTE_WOOD, outline=OUTLINE)
    draw.ellipse([38, 30 + cy, 52, 44 + cy], fill=LUTE_LIGHT)
    draw.ellipse([43, 35 + cy, 47, 39 + cy], fill=LUTE_DARK)
    draw.line([(30, 20 + cy), (43, 33 + cy)], fill=LUTE_DARK, width=3)

def generate_bard_spritesheet():
    dirs = ensure_dirs()
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    for row in range(4):
        for col in range(4):
            frame = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame)
            draw_bard_frame(draw, row, col)
            sheet.paste(frame, (col * 64, row * 64))
    save_sprite(sheet, "hero_bard.png", dirs)

if __name__ == "__main__":
    generate_bard_spritesheet()
