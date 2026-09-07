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
APRON_1 = (225, 175, 125, 255) # Rim Light
APRON_2 = (185, 132, 82, 255)  # Highlight
APRON_3 = (145, 95, 50, 255)   # Light
APRON_4 = (110, 68, 32, 255)   # Midtone Base
APRON_5 = (75, 42, 18, 255)    # Form Shadow
APRON_6 = (46, 22, 8, 255)     # Deep Crease

BELT_DARK     = (30, 30, 38, 255)
BRASS_1       = (255, 235, 120, 255)
BRASS_GOGGLES = (225, 175, 50, 255)
LENS_CYAN     = (60, 220, 230, 255)
LENS_SPEC     = (220, 255, 255, 255)
FLASK_RED     = (245, 60, 60, 255)
FLASK_CYAN    = (60, 220, 220, 255)
FLASK_GREEN   = (70, 230, 80, 255)

SKIN_BASE     = (245, 195, 155, 255)
EYE_PUPIL     = (20, 28, 42, 255)

def draw_alchemist_frame(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 2 if col == 1 else (-2 if col == 3 else 0)
    cy = bob

    # Ground Drop Shadow with Dual-Layer Occlusion
    draw.ellipse([16, 51 + cy, 48, 60 + cy], fill=(0, 0, 0, 70))
    draw.ellipse([20, 53 + cy, 44, 58 + cy], fill=(0, 0, 0, 140))

    # Trousers & Boots Stride
    lx1, lx2 = 22 + leg, 29 + leg
    rx1, rx2 = 35 - leg, 42 - leg
    draw.rectangle([lx1, 44 + cy, lx2, 56 + cy], fill=BELT_DARK, outline=OUTLINE)
    draw.rectangle([rx1, 44 + cy, rx2, 56 + cy], fill=BELT_DARK, outline=OUTLINE)
    draw.rectangle([lx1 + 1, 45 + cy, lx2 - 1, 53 + cy], fill=APRON_5)
    draw.rectangle([rx1 + 1, 45 + cy, rx2 - 1, 53 + cy], fill=APRON_5)
    draw.line([(lx1, 44 + cy), (lx2, 44 + cy)], fill=AO_CREVICE, width=1)
    draw.line([(rx1, 44 + cy), (rx2, 44 + cy)], fill=AO_CREVICE, width=1)

    # Leather Apron & Pocket Stitching
    draw.rectangle([23, 27 + cy, 41, 45 + cy], fill=APRON_4, outline=OUTLINE)
    draw.rectangle([25, 29 + cy, 39, 43 + cy], fill=APRON_3)
    draw.line([(24, 28 + cy), (24, 44 + cy)], fill=APRON_1, width=1) # Rim light

    # TIGHT ARTICULATED ROLLED SLEEVES & POTION-HOLDING HANDS
    # Left Arm & Flask Holding Hand
    draw.polygon([(16, 27 + cy), (23, 28 + cy), (20, 37 + cy), (14, 33 + cy)], fill=APRON_3, outline=OUTLINE) # Rolled sleeve
    draw.rectangle([14, 33 + cy, 21, 43 + cy], fill=APRON_5, outline=OUTLINE)
    draw.rectangle([14, 40 + cy, 20, 46 + cy], fill=SKIN_BASE, outline=OUTLINE) # Bare hand holding potion flask
    draw.ellipse([12, 44 + cy, 18, 51 + cy], fill=FLASK_CYAN, outline=OUTLINE)
    draw.line([(14, 33 + cy), (21, 33 + cy)], fill=AO_CREVICE, width=1)

    # Right Arm & Hand
    draw.polygon([(48, 27 + cy), (41, 28 + cy), (44, 37 + cy), (50, 33 + cy)], fill=APRON_4, outline=OUTLINE)
    draw.rectangle([43, 33 + cy, 50, 43 + cy], fill=APRON_5, outline=OUTLINE)
    draw.rectangle([44, 40 + cy, 50, 46 + cy], fill=SKIN_BASE, outline=OUTLINE)
    draw.ellipse([46, 44 + cy, 52, 51 + cy], fill=FLASK_RED, outline=OUTLINE)
    draw.line([(43, 33 + cy), (50, 33 + cy)], fill=AO_CREVICE, width=1)

    # Potion Belt with Flasks
    draw.rectangle([21, 37 + cy, 43, 40 + cy], fill=BELT_DARK, outline=OUTLINE)
    draw.ellipse([23, 39 + cy, 28, 46 + cy], fill=FLASK_CYAN, outline=OUTLINE)
    draw.point((24, 40 + cy), fill=LENS_SPEC)

    draw.ellipse([29, 39 + cy, 34, 46 + cy], fill=FLASK_RED, outline=OUTLINE)
    draw.point((30, 40 + cy), fill=LENS_SPEC)

    draw.ellipse([35, 39 + cy, 40, 46 + cy], fill=FLASK_GREEN, outline=OUTLINE)
    draw.point((36, 40 + cy), fill=LENS_SPEC)
    draw.line([(21, 37 + cy), (43, 37 + cy)], fill=AO_CREVICE, width=1)

    # Head & Brass Tinker Goggles
    draw.rectangle([23, 14 + cy, 41, 28 + cy], fill=SKIN_BASE, outline=OUTLINE)

    # Brass Goggles (Front & Side)
    draw.rectangle([21, 15 + cy, 43, 21 + cy], fill=BRASS_GOGGLES, outline=OUTLINE)
    draw.line([(22, 16 + cy), (42, 16 + cy)], fill=BRASS_1, width=1)
    if row == 0 or row == 1:
        draw.ellipse([24, 16 + cy, 30, 21 + cy], fill=LENS_CYAN, outline=OUTLINE)
        draw.point((25, 17 + cy), fill=LENS_SPEC)
    if row == 0 or row == 2:
        draw.ellipse([34, 16 + cy, 40, 21 + cy], fill=LENS_CYAN, outline=OUTLINE)
        draw.point((35, 17 + cy), fill=LENS_SPEC)

    # Eyes & Glint
    if row == 0:
        draw.rectangle([26, 22 + cy, 28, 25 + cy], fill=EYE_PUPIL)
        draw.rectangle([36, 22 + cy, 38, 25 + cy], fill=EYE_PUPIL)
        draw.point((27, 22 + cy), fill=LENS_SPEC)
        draw.point((37, 22 + cy), fill=LENS_SPEC)

def create_alchemist_spritesheet():
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    for row in range(4):
        for col in range(4):
            frame = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame)
            draw_alchemist_frame(draw, row, col)
            sheet.paste(frame, (col * 64, row * 64))
    return sheet

def main():
    dirs = ensure_dirs()
    sheet = create_alchemist_spritesheet()
    save_sprite(sheet, "hero_alchemist.png", dirs)

if __name__ == "__main__":
    main()
