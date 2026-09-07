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
GI_HI        = (255, 255, 255, 255)
GI_LIGHT     = (242, 245, 250, 255)
GI_BASE      = (215, 222, 235, 255)
GI_SHADOW    = (165, 175, 195, 255)
GI_DARK      = (110, 120, 140, 255)

RED_HI       = (255, 100, 110, 255)
RED_LIGHT    = (230, 45, 55, 255)
RED_BASE     = (180, 25, 35, 255)
RED_SHADOW   = (130, 15, 25, 255)
RED_DARK     = (85, 5, 15, 255)

WRAP_HI      = (210, 215, 225, 255)
WRAP_BASE    = (160, 170, 185, 255)
WRAP_SHADOW  = (110, 120, 135, 255)
GOLD_STUD    = (245, 205, 50, 255)

SKIN_BASE    = (245, 200, 165, 255)
HAIR_DARK    = (35, 35, 40, 255)
EYE_DARK     = (20, 30, 45, 255)

def draw_monk_frame(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    # Drop Shadow
    draw.ellipse([18, 52 + cy, 46, 59 + cy], fill=(0, 0, 0, 90))

    # Trousers & Boots
    lx1, lx2 = 23 + leg, 29 + leg
    rx1, rx2 = 35 - leg, 41 - leg
    draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=GI_SHADOW, outline=OUTLINE)
    draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=GI_SHADOW, outline=OUTLINE)

    # Martial Gi Body & Folded Lapels
    draw.rectangle([21, 27 + cy, 43, 44 + cy], fill=GI_BASE, outline=OUTLINE)
    draw.polygon([(21, 27 + cy), (32, 38 + cy), (21, 38 + cy)], fill=GI_SHADOW)
    draw.polygon([(43, 27 + cy), (32, 38 + cy), (43, 38 + cy)], fill=GI_SHADOW)
    if row != 3:
        draw.polygon([(27, 27 + cy), (32, 35 + cy), (37, 27 + cy)], fill=SKIN_BASE)

    # Red Martial Sash Belt & Fluttering Knot
    draw.rectangle([20, 38 + cy, 44, 43 + cy], fill=RED_BASE, outline=OUTLINE)
    draw.polygon([(36, 43 + cy), (41, 43 + cy), (39, 53 + cy)], fill=RED_BASE, outline=OUTLINE)
    draw.polygon([(32, 43 + cy), (37, 43 + cy), (34, 50 + cy)], fill=RED_SHADOW)

    # Arms & Spiked Iron Fist Wraps
    draw.rectangle([16, 29 + cy, 21, 38 + cy], fill=GI_BASE, outline=OUTLINE)
    draw.ellipse([14, 37 + cy, 22, 45 + cy], fill=WRAP_BASE, outline=OUTLINE)
    draw.rectangle([16, 40 + cy, 20, 42 + cy], fill=GOLD_STUD)

    draw.rectangle([43, 29 + cy, 48, 38 + cy], fill=GI_BASE, outline=OUTLINE)
    draw.ellipse([42, 37 + cy, 50, 45 + cy], fill=WRAP_BASE, outline=OUTLINE)
    draw.rectangle([44, 40 + cy, 48, 42 + cy], fill=GOLD_STUD)

    # Head, Hair & Red Bandana
    draw.rectangle([23, 14 + cy, 41, 28 + cy], fill=SKIN_BASE, outline=OUTLINE)
    draw.rectangle([22, 10 + cy, 42, 17 + cy], fill=HAIR_DARK) # Hair
    draw.rectangle([21, 15 + cy, 43, 19 + cy], fill=RED_BASE, outline=OUTLINE) # Bandana
    draw.polygon([(43, 16 + cy), (49, 14 + cy), (47, 22 + cy)], fill=RED_BASE) # Bandana tail

    if row == 0:
        draw.rectangle([26, 22 + cy, 28, 25 + cy], fill=EYE_DARK)
        draw.rectangle([36, 22 + cy, 38, 25 + cy], fill=EYE_DARK)
    elif row == 1:
        draw.rectangle([24, 22 + cy, 26, 25 + cy], fill=EYE_DARK)
    elif row == 2:
        draw.rectangle([38, 22 + cy, 40, 25 + cy], fill=EYE_DARK)

def generate_monk_spritesheet():
    dirs = ensure_dirs()
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    for row in range(4):
        for col in range(4):
            frame = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame)
            draw_monk_frame(draw, row, col)
            sheet.paste(frame, (col * 64, row * 64))
    save_sprite(sheet, "hero_monk.png", dirs)

if __name__ == "__main__":
    generate_monk_spritesheet()
