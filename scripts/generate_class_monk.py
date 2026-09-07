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
GI_1 = (255, 255, 255, 255) # Pure Glint
GI_2 = (242, 245, 250, 255) # Highlight
GI_3 = (215, 222, 235, 255) # Light Tone
GI_4 = (175, 185, 205, 255) # Midtone Base
GI_5 = (135, 145, 168, 255) # Form Shadow
GI_6 = (95, 105, 128, 255)  # Deep Crease
GI_7 = (45, 52, 70, 255)    # Core AO

RED_1 = (255, 140, 150, 255)
RED_2 = (230, 45, 55, 255)
RED_3 = (180, 25, 35, 255)
RED_4 = (130, 15, 25, 255)
RED_5 = (85, 5, 15, 255)

WRAP_BASE = (170, 180, 195, 255)
WRAP_DARK = (110, 120, 135, 255)
GOLD_STUD = (245, 205, 50, 255)

SKIN_BASE = (245, 195, 155, 255)
HAIR_DARK = (30, 30, 35, 255)
EYE_PUPIL = (20, 28, 42, 255)

def draw_monk_frame(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    # Ground Drop Shadow with Dual-Layer Occlusion
    draw.ellipse([14, 51 + cy, 50, 60 + cy], fill=(0, 0, 0, 70))
    draw.ellipse([18, 53 + cy, 46, 58 + cy], fill=(0, 0, 0, 140))

    # Trousers & Boots
    lx1, lx2 = 23 + leg, 29 + leg
    rx1, rx2 = 35 - leg, 41 - leg
    draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=GI_5, outline=OUTLINE)
    draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=GI_5, outline=OUTLINE)
    draw.line([(lx1, 44 + cy), (lx2, 44 + cy)], fill=AO_CREVICE, width=1)
    draw.line([(rx1, 44 + cy), (rx2, 44 + cy)], fill=AO_CREVICE, width=1)

    # Martial Gi Body & Folded Lapels
    draw.rectangle([21, 27 + cy, 43, 44 + cy], fill=GI_3, outline=OUTLINE)
    draw.polygon([(21, 27 + cy), (32, 38 + cy), (21, 38 + cy)], fill=GI_5)
    draw.polygon([(43, 27 + cy), (32, 38 + cy), (43, 38 + cy)], fill=GI_4)
    draw.line([(22, 28 + cy), (22, 43 + cy)], fill=GI_1, width=1) # Rim light

    # Red Sash Belt & Knot
    draw.rectangle([20, 39 + cy, 44, 43 + cy], fill=RED_3, outline=OUTLINE)
    draw.line([(21, 40 + cy), (43, 40 + cy)], fill=RED_1, width=1)
    draw.polygon([(28, 41 + cy), (26, 51 + cy), (32, 51 + cy), (30, 41 + cy)], fill=RED_3, outline=OUTLINE)
    draw.polygon([(30, 41 + cy), (32, 49 + cy), (36, 49 + cy), (34, 41 + cy)], fill=RED_4, outline=OUTLINE)
    draw.line([(20, 39 + cy), (44, 39 + cy)], fill=AO_CREVICE, width=1)

    # Head, Hair & Red Headband
    draw.rectangle([23, 14 + cy, 41, 27 + cy], fill=SKIN_BASE, outline=OUTLINE)
    draw.rectangle([22, 14 + cy, 42, 18 + cy], fill=HAIR_DARK)
    draw.rectangle([21, 17 + cy, 43, 21 + cy], fill=RED_3, outline=OUTLINE)
    draw.line([(22, 18 + cy), (42, 18 + cy)], fill=RED_1, width=1)

    # Eyes
    if row == 0:
        draw.rectangle([26, 22 + cy, 28, 25 + cy], fill=EYE_PUPIL)
        draw.rectangle([36, 22 + cy, 38, 25 + cy], fill=EYE_PUPIL)
        draw.point((27, 22 + cy), fill=GI_1)
        draw.point((37, 22 + cy), fill=GI_1)
    elif row == 1:
        draw.rectangle([24, 22 + cy, 27, 25 + cy], fill=EYE_PUPIL)
        draw.point((25, 22 + cy), fill=GI_1)
    elif row == 2:
        draw.rectangle([37, 22 + cy, 40, 25 + cy], fill=EYE_PUPIL)
        draw.point((38, 22 + cy), fill=GI_1)

    # Spiked Iron Wrapped Fists
    draw.rectangle([11, 31 + cy, 19, 41 + cy], fill=WRAP_BASE, outline=OUTLINE)
    draw.point((13, 33 + cy), fill=GOLD_STUD)
    draw.point((17, 37 + cy), fill=GOLD_STUD)

    draw.rectangle([45, 31 + cy, 53, 41 + cy], fill=WRAP_BASE, outline=OUTLINE)
    draw.point((47, 33 + cy), fill=GOLD_STUD)
    draw.point((51, 37 + cy), fill=GOLD_STUD)

def create_monk_spritesheet():
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    for row in range(4):
        for col in range(4):
            frame = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame)
            draw_monk_frame(draw, row, col)
            sheet.paste(frame, (col * 64, row * 64))
    return sheet

def main():
    dirs = ensure_dirs()
    sheet = create_monk_spritesheet()
    save_sprite(sheet, "hero_monk.png", dirs)

if __name__ == "__main__":
    main()
