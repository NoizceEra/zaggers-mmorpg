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
EMERALD_1 = (160, 245, 185, 255) # Rim Light Peak
EMERALD_2 = (85, 210, 125, 255)  # Highlight
EMERALD_3 = (45, 165, 88, 255)   # Light
EMERALD_4 = (26, 122, 58, 255)   # Midtone Base
EMERALD_5 = (14, 82, 36, 255)    # Form Shadow
EMERALD_6 = (8, 52, 22, 255)     # Deep Crease
EMERALD_7 = (2, 24, 8, 255)      # Core AO

LEATHER_1 = (225, 175, 125, 255)
LEATHER_2 = (185, 132, 82, 255)
LEATHER_3 = (145, 95, 50, 255)
LEATHER_4 = (110, 68, 32, 255)
LEATHER_5 = (75, 42, 18, 255)
LEATHER_6 = (46, 22, 8, 255)
LEATHER_7 = (20, 8, 2, 255)

STEEL_1 = (255, 255, 255, 255)
STEEL_2 = (230, 242, 252, 255)
STEEL_3 = (185, 202, 220, 255)
STEEL_4 = (130, 148, 168, 255)
STEEL_5 = (80, 95, 115, 255)

BELT_DARK = (30, 30, 38, 255)
GOLD_BUCKLE = (240, 195, 45, 255)
SKIN_BASE = (245, 195, 155, 255)
EYE_PUPIL = (20, 28, 42, 255)

def draw_thief_frame(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    # Ground Drop Shadow with Dual-Layer Occlusion
    draw.ellipse([14, 51 + cy, 50, 60 + cy], fill=(0, 0, 0, 70))
    draw.ellipse([18, 53 + cy, 46, 58 + cy], fill=(0, 0, 0, 140))

    if row == 3: # UP (Back view)
        # Emerald Hood & Back Cloak
        draw.polygon([(18, 12 + cy), (46, 12 + cy), (50, 52 + cy), (14, 52 + cy)], fill=EMERALD_4, outline=OUTLINE)
        draw.polygon([(22, 16 + cy), (42, 16 + cy), (46, 50 + cy), (18, 50 + cy)], fill=EMERALD_5)
        draw.polygon([(18, 44 + cy), (28, 52 + cy), (14, 52 + cy)], fill=EMERALD_6)
        draw.line([(49, 13 + cy), (49, 51 + cy)], fill=EMERALD_1, width=1) # Rim light right

        # Legs
        lx1, lx2 = 23 + leg, 29 + leg
        rx1, rx2 = 35 - leg, 41 - leg
        draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=LEATHER_5, outline=OUTLINE)
        draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=LEATHER_5, outline=OUTLINE)
        draw.line([(lx1, 44 + cy), (lx2, 44 + cy)], fill=AO_CREVICE, width=1)
        draw.line([(rx1, 44 + cy), (rx2, 44 + cy)], fill=AO_CREVICE, width=1)
    else:
        # Legs / Trousers & Boot Stride
        lx1, lx2 = 20 + leg, 28 + leg
        rx1, rx2 = 36 - leg, 44 - leg
        draw.rectangle([lx1, 44 + cy, lx2, 56 + cy], fill=LEATHER_5, outline=OUTLINE)
        draw.rectangle([rx1, 44 + cy, rx2, 56 + cy], fill=LEATHER_5, outline=OUTLINE)
        draw.rectangle([lx1 + 1, 45 + cy, lx2 - 1, 53 + cy], fill=LEATHER_4)
        draw.rectangle([rx1 + 1, 45 + cy, rx2 - 1, 53 + cy], fill=LEATHER_4)
        draw.line([(lx1 + 1, 45 + cy), (lx1 + 1, 51 + cy)], fill=LEATHER_2, width=1)
        draw.line([(rx1 + 1, 45 + cy), (rx1 + 1, 51 + cy)], fill=LEATHER_2, width=1)
        draw.rectangle([lx1, 48 + cy, lx2, 50 + cy], fill=LEATHER_3) # Knee wrap plate
        draw.rectangle([rx1, 48 + cy, rx2, 50 + cy], fill=LEATHER_3)
        draw.line([(lx1, 44 + cy), (lx2, 44 + cy)], fill=AO_CREVICE, width=1)
        draw.line([(rx1, 44 + cy), (rx2, 44 + cy)], fill=AO_CREVICE, width=1)

        # Leather Doublet & Chest Straps
        draw.rectangle([21, 26 + cy, 43, 44 + cy], fill=LEATHER_4, outline=OUTLINE)
        draw.rectangle([25, 28 + cy, 39, 41 + cy], fill=LEATHER_3)
        draw.line([(32, 28 + cy), (32, 41 + cy)], fill=LEATHER_6, width=2)
        draw.line([(24, 29 + cy), (40, 37 + cy)], fill=BELT_DARK, width=2) # Chest strap

        # Shadow Belt & Pouches
        draw.rectangle([20, 40 + cy, 44, 43 + cy], fill=BELT_DARK, outline=OUTLINE)
        draw.rectangle([30, 39 + cy, 34, 44 + cy], fill=GOLD_BUCKLE, outline=OUTLINE)
        draw.rectangle([21, 41 + cy, 25, 45 + cy], fill=LEATHER_6)
        draw.rectangle([39, 41 + cy, 43, 45 + cy], fill=LEATHER_6)
        draw.line([(20, 40 + cy), (44, 40 + cy)], fill=AO_CREVICE, width=1)

        # ARTICULATED ARMS, LEATHER BRACERS & GLOVED HANDS
        # Left Arm & Bracer
        draw.polygon([(13, 26 + cy), (21, 27 + cy), (18, 37 + cy), (10, 33 + cy)], fill=LEATHER_3, outline=OUTLINE)
        draw.rectangle([10, 33 + cy, 18, 43 + cy], fill=LEATHER_5, outline=OUTLINE) # Bracer
        draw.rectangle([11, 40 + cy, 17, 46 + cy], fill=LEATHER_2, outline=OUTLINE) # Assassin glove hand
        draw.line([(10, 33 + cy), (18, 33 + cy)], fill=AO_CREVICE, width=1)

        # Right Arm & Bracer
        draw.polygon([(51, 26 + cy), (43, 27 + cy), (46, 37 + cy), (54, 33 + cy)], fill=LEATHER_4, outline=OUTLINE)
        draw.rectangle([46, 33 + cy, 54, 43 + cy], fill=LEATHER_5, outline=OUTLINE)
        draw.rectangle([47, 40 + cy, 53, 46 + cy], fill=LEATHER_2, outline=OUTLINE)
        draw.line([(46, 33 + cy), (54, 33 + cy)], fill=AO_CREVICE, width=1)

        # Emerald Assassin Hood & Cloak
        draw.polygon([(18, 12 + cy), (46, 12 + cy), (44, 28 + cy), (20, 28 + cy)], fill=EMERALD_4, outline=OUTLINE)
        draw.polygon([(20, 14 + cy), (44, 14 + cy), (42, 26 + cy)], fill=EMERALD_3)
        draw.line([(19, 13 + cy), (19, 27 + cy)], fill=EMERALD_1, width=1) # Rim light
        draw.rectangle([24, 17 + cy, 40, 26 + cy], fill=SKIN_BASE)

        # Eyes & Pupil Catchlights
        if row == 0:
            draw.rectangle([26, 20 + cy, 28, 23 + cy], fill=EYE_PUPIL)
            draw.rectangle([36, 20 + cy, 38, 23 + cy], fill=EYE_PUPIL)
            draw.point((27, 20 + cy), fill=STEEL_1)
            draw.point((37, 20 + cy), fill=STEEL_1)
        elif row == 1:
            draw.rectangle([24, 20 + cy, 27, 23 + cy], fill=EYE_PUPIL)
            draw.point((25, 20 + cy), fill=STEEL_1)
        elif row == 2:
            draw.rectangle([37, 20 + cy, 40, 23 + cy], fill=EYE_PUPIL)
            draw.point((38, 20 + cy), fill=STEEL_1)

        # Dual Curved Daggers with Dual Bevels
        # Left Hand Dagger
        draw.line([(12, 24 + cy), (12, 44 + cy)], fill=STEEL_2, width=2)
        draw.line([(11, 24 + cy), (11, 42 + cy)], fill=STEEL_1, width=1)
        draw.line([(13, 26 + cy), (13, 42 + cy)], fill=STEEL_4, width=1)
        draw.rectangle([9, 41 + cy, 15, 43 + cy], fill=GOLD_BUCKLE)
        # Right Hand Dagger
        draw.line([(52, 24 + cy), (52, 44 + cy)], fill=STEEL_2, width=2)
        draw.line([(53, 24 + cy), (53, 42 + cy)], fill=STEEL_1, width=1)
        draw.line([(51, 26 + cy), (51, 42 + cy)], fill=STEEL_4, width=1)
        draw.rectangle([49, 41 + cy, 55, 43 + cy], fill=GOLD_BUCKLE)

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

