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
PURPLE_1 = (220, 180, 255, 255) # Rim Light Peak
PURPLE_2 = (175, 120, 235, 255) # Specular
PURPLE_3 = (130, 70, 190, 255)  # Light Tone
PURPLE_4 = (92, 42, 145, 255)   # Midtone Base
PURPLE_5 = (60, 24, 98, 255)    # Form Shadow
PURPLE_6 = (36, 12, 62, 255)    # Deep Crease
PURPLE_7 = (16, 4, 30, 255)     # Core AO

GOLD_1 = (255, 255, 210, 255)
GOLD_2 = (245, 200, 60, 255)
GOLD_3 = (215, 160, 25, 255)
GOLD_4 = (160, 112, 12, 255)

CYAN_1 = (220, 255, 255, 255)
CYAN_2 = (110, 245, 255, 255)
CYAN_3 = (30, 210, 230, 255)

SILVER_1 = (245, 250, 255, 255)
SILVER_2 = (215, 225, 238, 255)
SILVER_3 = (135, 145, 160, 255)
LANCE_WOOD = (120, 75, 40, 255)
RIBBON_RED = (235, 45, 55, 255)

def draw_dragoon_frame(draw, row, col):
    bob = 1 if (col == 1 or col == 3) else 0
    leg = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    # Ground Drop Shadow with Dual-Layer Occlusion
    draw.ellipse([14, 51 + cy, 50, 60 + cy], fill=(0, 0, 0, 70))
    draw.ellipse([18, 53 + cy, 46, 58 + cy], fill=(0, 0, 0, 140))

    if row == 3: # UP (Back view)
        # Legs & Greaves
        lx1, lx2 = 23 + leg, 29 + leg
        rx1, rx2 = 35 - leg, 41 - leg
        draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=PURPLE_6, outline=OUTLINE)
        draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=PURPLE_6, outline=OUTLINE)
        draw.line([(lx1, 44 + cy), (lx2, 44 + cy)], fill=AO_CREVICE, width=1)
        draw.line([(rx1, 44 + cy), (rx2, 44 + cy)], fill=AO_CREVICE, width=1)

        # Spiked Dragoon Back Armor
        draw.rectangle([20, 25 + cy, 44, 44 + cy], fill=PURPLE_5, outline=OUTLINE)
        draw.polygon([(26, 25 + cy), (38, 25 + cy), (32, 40 + cy)], fill=PURPLE_4)

        # Dragon Helmet Back & Gold Horns
        draw.rectangle([21, 10 + cy, 43, 26 + cy], fill=PURPLE_4, outline=OUTLINE)
        draw.polygon([(10, 2 + cy), (22, 10 + cy), (18, 18 + cy)], fill=GOLD_3, outline=OUTLINE)
        draw.polygon([(54, 2 + cy), (42, 10 + cy), (46, 18 + cy)], fill=GOLD_4, outline=OUTLINE)
    else:
        # Greaves & Boots
        lx1, lx2 = 23 + leg, 29 + leg
        rx1, rx2 = 35 - leg, 41 - leg
        draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=PURPLE_5, outline=OUTLINE)
        draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=PURPLE_5, outline=OUTLINE)
        draw.rectangle([lx1 + 1, 45 + cy, lx2 - 1, 52 + cy], fill=PURPLE_4)
        draw.rectangle([rx1 + 1, 45 + cy, rx2 - 1, 52 + cy], fill=PURPLE_4)
        draw.line([(lx1 + 1, 45 + cy), (lx1 + 1, 51 + cy)], fill=PURPLE_1, width=1) # Rim light
        draw.line([(rx1 + 1, 45 + cy), (rx1 + 1, 51 + cy)], fill=PURPLE_1, width=1)
        draw.line([(lx1, 44 + cy), (lx2, 44 + cy)], fill=AO_CREVICE, width=1)
        draw.line([(rx1, 44 + cy), (rx2, 44 + cy)], fill=AO_CREVICE, width=1)

        # Spiked Dragon Scale Cuirass
        # Cyan Visor Glow
        if row == 0: # Down
            draw.rectangle([24, 21 + cy, 40, 24 + cy], fill=OUTLINE)
            draw.line([(26, 22 + cy), (38, 22 + cy)], fill=CYAN_3, width=2)
            draw.line([(28, 22 + cy), (36, 22 + cy)], fill=CYAN_1, width=1)
        elif row == 1: # Left
            draw.rectangle([22, 21 + cy, 34, 24 + cy], fill=OUTLINE)
            draw.line([(24, 22 + cy), (32, 22 + cy)], fill=CYAN_3, width=2)
            draw.line([(25, 22 + cy), (30, 22 + cy)], fill=CYAN_1, width=1)
        elif row == 2: # Right
            draw.rectangle([30, 21 + cy, 42, 24 + cy], fill=OUTLINE)
            draw.line([(32, 22 + cy), (40, 22 + cy)], fill=CYAN_3, width=2)
            draw.line([(34, 22 + cy), (39, 22 + cy)], fill=CYAN_1, width=1)

    # Dragon Lance Weapon
    wx = 50 if (row == 0 or row == 2) else 14
    draw.line([(wx, 4 + cy), (wx, 56 + cy)], fill=LANCE_WOOD, width=3)
    draw.polygon([(wx, -2 + cy), (wx - 5, 12 + cy), (wx + 5, 12 + cy)], fill=SILVER_2, outline=OUTLINE)
    draw.polygon([(wx - 2, 0 + cy), (wx, -4 + cy), (wx + 2, 0 + cy)], fill=(255, 255, 255, 255))
    draw.polygon([(wx, 12 + cy), (wx - 8, 18 + cy), (wx + 2, 16 + cy)], fill=RIBBON_RED)

def generate_dragoon_spritesheet():
    dirs = ensure_dirs()
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    for row in range(4):
        for col in range(4):
            frame = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame)
            draw_dragoon_frame(draw, row, col)
            sheet.paste(frame, (col * 64, row * 64))
    save_sprite(sheet, "hero_dragoon.png", dirs)

if __name__ == "__main__":
    generate_dragoon_spritesheet()
