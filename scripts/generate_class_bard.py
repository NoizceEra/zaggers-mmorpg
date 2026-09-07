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
DOUBLET_1 = (255, 160, 170, 255) # Rim Light
DOUBLET_2 = (245, 95, 110, 255)  # Highlight
DOUBLET_3 = (215, 45, 65, 255)   # Light
DOUBLET_4 = (165, 25, 42, 255)   # Midtone Base
DOUBLET_5 = (115, 14, 28, 255)   # Shadow
DOUBLET_6 = (70, 6, 16, 255)     # Deep Crease

TROUSERS_BASE = (45, 135, 75, 255)
TROUSERS_DARK = (24, 82, 42, 255)

CAP_GREEN = (35, 115, 60, 255)
FEATHER_WHITE = (255, 255, 255, 255)

LUTE_1 = (235, 165, 95, 255)
LUTE_2 = (180, 110, 45, 255)
LUTE_3 = (110, 60, 25, 255)
STRING_SILVER = (230, 240, 255, 255)

SKIN_BASE = (245, 195, 155, 255)
EYE_PUPIL = (20, 28, 42, 255)

def draw_bard_frame(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 2 if col == 1 else (-2 if col == 3 else 0)
    cy = bob

    # Ground Drop Shadow with Dual-Layer Occlusion
    draw.ellipse([16, 51 + cy, 48, 60 + cy], fill=(0, 0, 0, 70))
    draw.ellipse([20, 53 + cy, 44, 58 + cy], fill=(0, 0, 0, 140))

    # Trousers & Boots Stride
    lx1, lx2 = 22 + leg, 29 + leg
    rx1, rx2 = 35 - leg, 42 - leg
    draw.rectangle([lx1, 44 + cy, lx2, 56 + cy], fill=TROUSERS_DARK, outline=OUTLINE)
    draw.rectangle([rx1, 44 + cy, rx2, 56 + cy], fill=TROUSERS_DARK, outline=OUTLINE)
    draw.rectangle([lx1 + 1, 45 + cy, lx2 - 1, 53 + cy], fill=TROUSERS_BASE)
    draw.rectangle([rx1 + 1, 45 + cy, rx2 - 1, 53 + cy], fill=TROUSERS_BASE)
    draw.line([(lx1, 44 + cy), (lx2, 44 + cy)], fill=AO_CREVICE, width=1)
    draw.line([(rx1, 44 + cy), (rx2, 44 + cy)], fill=AO_CREVICE, width=1)

    # Crimson Doublet & Gold Buttons
    draw.rectangle([23, 27 + cy, 41, 44 + cy], fill=DOUBLET_4, outline=OUTLINE)
    draw.rectangle([25, 29 + cy, 39, 42 + cy], fill=DOUBLET_3)
    draw.line([(24, 28 + cy), (24, 43 + cy)], fill=DOUBLET_1, width=1) # Rim light
    for button_y in range(30, 42, 4):
        draw.rectangle([31, button_y + cy, 33, button_y + 2 + cy], fill=(255, 220, 60, 255))

    # TIGHT ARTICULATED PUFFED SLEEVES & EXPOSED MINSTREL HANDS
    # Left Arm & Hand holding Lute Neck
    draw.polygon([(16, 27 + cy), (23, 28 + cy), (20, 37 + cy), (14, 33 + cy)], fill=DOUBLET_3, outline=OUTLINE) # Puffed sleeve
    draw.rectangle([14, 33 + cy, 21, 43 + cy], fill=DOUBLET_5, outline=OUTLINE)
    draw.rectangle([14, 40 + cy, 20, 46 + cy], fill=SKIN_BASE, outline=OUTLINE) # Skin hand
    draw.line([(14, 33 + cy), (21, 33 + cy)], fill=AO_CREVICE, width=1)

    # Right Arm & Hand plucking Lute Strings
    draw.polygon([(48, 27 + cy), (41, 28 + cy), (44, 37 + cy), (50, 33 + cy)], fill=DOUBLET_4, outline=OUTLINE)
    draw.rectangle([43, 33 + cy, 50, 43 + cy], fill=DOUBLET_5, outline=OUTLINE)
    draw.rectangle([44, 40 + cy, 50, 46 + cy], fill=SKIN_BASE, outline=OUTLINE)
    draw.line([(43, 33 + cy), (50, 33 + cy)], fill=AO_CREVICE, width=1)

    # Head & Feathered Minstrel Cap
    draw.rectangle([23, 14 + cy, 41, 28 + cy], fill=SKIN_BASE, outline=OUTLINE)
    draw.polygon([(18, 10 + cy), (46, 10 + cy), (42, 17 + cy), (22, 17 + cy)], fill=CAP_GREEN, outline=OUTLINE)
    draw.line([(18, 17 + cy), (46, 17 + cy)], fill=AO_CREVICE, width=1)
    # White Plume Feather
    draw.polygon([(12, 2 + cy), (20, 8 + cy), (16, 16 + cy)], fill=FEATHER_WHITE, outline=OUTLINE)

    # Eyes & Glint
    if row == 0:
        draw.rectangle([26, 21 + cy, 28, 24 + cy], fill=EYE_PUPIL)
        draw.rectangle([36, 21 + cy, 38, 24 + cy], fill=EYE_PUPIL)
        draw.point((27, 21 + cy), fill=FEATHER_WHITE)
        draw.point((37, 21 + cy), fill=FEATHER_WHITE)
    elif row == 1:
        draw.rectangle([24, 21 + cy, 26, 24 + cy], fill=EYE_PUPIL)
        draw.point((25, 21 + cy), fill=FEATHER_WHITE)
    elif row == 2:
        draw.rectangle([38, 21 + cy, 40, 24 + cy], fill=EYE_PUPIL)
        draw.point((39, 21 + cy), fill=FEATHER_WHITE)

    # Acoustic Carved Lute with Silver Strings
    draw.ellipse([11, 28 + cy, 23, 46 + cy], fill=LUTE_2, outline=OUTLINE)
    draw.ellipse([13, 31 + cy, 21, 43 + cy], fill=LUTE_1)
    draw.ellipse([15, 35 + cy, 19, 39 + cy], fill=LUTE_3) # Soundhole
    draw.line([(17, 18 + cy), (17, 35 + cy)], fill=LUTE_3, width=3) # Neck
    draw.line([(16, 18 + cy), (16, 45 + cy)], fill=STRING_SILVER, width=1) # Strings
    draw.line([(18, 18 + cy), (18, 45 + cy)], fill=STRING_SILVER, width=1)

def create_bard_spritesheet():
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    for row in range(4):
        for col in range(4):
            frame = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame)
            draw_bard_frame(draw, row, col)
            sheet.paste(frame, (col * 64, row * 64))
    return sheet

def main():
    dirs = ensure_dirs()
    sheet = create_bard_spritesheet()
    save_sprite(sheet, "hero_bard.png", dirs)

if __name__ == "__main__":
    main()
