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

def draw_redmage_frame(draw, row, col):
    OUTLINE = (12, 16, 24, 255)
    AO_CREVICE = (6, 8, 14, 255)

    # Crimson Doublet 7-tone ramp
    CRIMSON_7 = (28, 2, 8, 255)      # Core AO Crevice
    CRIMSON_6 = (70, 6, 16, 255)     # Deep Crease
    CRIMSON_5 = (115, 14, 28, 255)   # Shadow
    CRIMSON_4 = (165, 25, 42, 255)   # Midtone Base
    CRIMSON_3 = (215, 45, 65, 255)   # Light Tone
    CRIMSON_2 = (245, 95, 110, 255)  # Highlight
    CRIMSON_1 = (255, 160, 170, 255) # Rim Light Peak

    FEATHER_1 = (255, 255, 255, 255)
    FEATHER_2 = (240, 242, 248, 255)
    FEATHER_3 = (215, 220, 235, 255)
    FEATHER_4 = (175, 182, 205, 255)

    STEEL_1 = (255, 255, 255, 255)
    STEEL_2 = (220, 230, 245, 255)
    STEEL_3 = (175, 188, 208, 255)
    STEEL_4 = (125, 138, 160, 255)

    GOLD_2 = (250, 215, 80, 255)
    GOLD_3 = (235, 190, 50, 255)
    GOLD_4 = (180, 140, 30, 255)

    SKIN = (245, 195, 155, 255)
    HAIR_DARK = (40, 30, 35, 255)

    BOOK_COVER = (140, 20, 30, 255)
    BOOK_PAGES = (245, 240, 220, 255)

    bob = 1 if (col == 1 or col == 3) else 0
    leg_step = 2 if col == 1 else (-2 if col == 3 else 0)
    cy = bob

    # Ground Drop Shadow with Dual-Layer Occlusion
    draw.ellipse([16, 51 + cy, 48, 60 + cy], fill=(0, 0, 0, 70))
    draw.ellipse([20, 53 + cy, 44, 58 + cy], fill=(0, 0, 0, 140))

    # Trousers / Legs & Cuffed Boot Stride
    lx1, lx2 = 22 + leg_step, 29 + leg_step
    rx1, rx2 = 35 - leg_step, 42 - leg_step
    draw.rectangle([lx1, 44 + cy, lx2, 56 + cy], fill=CRIMSON_5, outline=OUTLINE)
    draw.rectangle([rx1, 44 + cy, rx2, 56 + cy], fill=CRIMSON_5, outline=OUTLINE)
    draw.rectangle([lx1, 44 + cy, lx2, 47 + cy], fill=CRIMSON_3) # Boot cuff flap
    draw.rectangle([rx1, 44 + cy, rx2, 47 + cy], fill=CRIMSON_3)
    draw.line([(lx1, 44 + cy), (lx2, 44 + cy)], fill=AO_CREVICE, width=1)
    draw.line([(rx1, 44 + cy), (rx2, 44 + cy)], fill=AO_CREVICE, width=1)

    # Crimson Doublet & Gold Embroidery
    draw.rectangle([23, 26 + cy, 41, 44 + cy], fill=CRIMSON_4, outline=OUTLINE)
    draw.rectangle([25, 28 + cy, 39, 42 + cy], fill=CRIMSON_3)
    draw.line([(32, 26 + cy), (32, 44 + cy)], fill=GOLD_3, width=2)
    draw.line([(32, 26 + cy), (32, 44 + cy)], fill=GOLD_2, width=1)
    draw.line([(24, 27 + cy), (24, 43 + cy)], fill=CRIMSON_1, width=1) # Rim light left

    # TIGHT ARTICULATED SLEEVES & WHITE FENCER GLOVES
    # Left Arm & Grimoire Hand
    draw.polygon([(15, 26 + cy), (22, 27 + cy), (20, 37 + cy), (14, 33 + cy)], fill=CRIMSON_3, outline=OUTLINE)
    draw.rectangle([14, 33 + cy, 21, 43 + cy], fill=CRIMSON_5, outline=OUTLINE) # Sleeve cuff
    draw.rectangle([14, 40 + cy, 20, 46 + cy], fill=FEATHER_1, outline=OUTLINE) # Fencer glove

    # Right Arm & Rapier Hand
    draw.polygon([(49, 26 + cy), (42, 27 + cy), (44, 37 + cy), (50, 33 + cy)], fill=CRIMSON_4, outline=OUTLINE)
    draw.rectangle([43, 33 + cy, 50, 43 + cy], fill=CRIMSON_5, outline=OUTLINE)
    draw.rectangle([44, 40 + cy, 50, 46 + cy], fill=FEATHER_1, outline=OUTLINE)

    # Head & Hair
    draw.rectangle([23, 14 + cy, 41, 28 + cy], fill=SKIN, outline=OUTLINE)
    draw.rectangle([22, 14 + cy, 42, 18 + cy], fill=HAIR_DARK)

    # Feathered Chapeau Cap & AO Line
    draw.polygon([(16, 10 + cy), (48, 10 + cy), (42, 17 + cy), (22, 17 + cy)], fill=CRIMSON_5, outline=OUTLINE)
    draw.polygon([(18, 11 + cy), (34, 11 + cy), (32, 16 + cy)], fill=CRIMSON_4)
    draw.line([(17, 17 + cy), (47, 17 + cy)], fill=AO_CREVICE, width=1) # Cap AO

    # Large White Plume / Feather on Hat
    draw.polygon([(10, 0 + cy), (22, 8 + cy), (16, 16 + cy)], fill=FEATHER_3, outline=OUTLINE)
    draw.polygon([(10, 0 + cy), (16, 8 + cy), (16, 16 + cy)], fill=FEATHER_4)
    draw.polygon([(14, 2 + cy), (20, 8 + cy), (17, 12 + cy)], fill=FEATHER_1)

    # Eyes
    if row == 0:
        draw.rectangle([26, 21 + cy, 28, 24 + cy], fill=OUTLINE)
        draw.rectangle([36, 21 + cy, 38, 24 + cy], fill=OUTLINE)
    elif row == 1:
        draw.rectangle([24, 21 + cy, 26, 24 + cy], fill=OUTLINE)
    elif row == 2:
        draw.rectangle([38, 21 + cy, 40, 24 + cy], fill=OUTLINE)

    # Rapier Blade with Basket Hilt (Right hand)
    draw.line([(48, 12 + cy), (48, 48 + cy)], fill=STEEL_2, width=2)
    draw.line([(49, 14 + cy), (49, 46 + cy)], fill=STEEL_1, width=1)
    draw.ellipse([43, 36 + cy, 53, 43 + cy], fill=GOLD_3, outline=OUTLINE)
    draw.ellipse([45, 38 + cy, 51, 41 + cy], fill=GOLD_2)

    # Spellbook Grimoire (Left hip / hand)
    draw.rectangle([13, 32 + cy, 23, 44 + cy], fill=BOOK_COVER, outline=OUTLINE)
    draw.rectangle([15, 34 + cy, 21, 42 + cy], fill=BOOK_PAGES)
    draw.line([(18, 34 + cy), (18, 42 + cy)], fill=GOLD_3, width=1)

def create_redmage_spritesheet():
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    for row in range(4):
        for col in range(4):
            frame = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame)
            draw_redmage_frame(draw, row, col)
            sheet.paste(frame, (col * 64, row * 64))
    return sheet

def main():
    dirs = ensure_dirs()
    sheet = create_redmage_spritesheet()
    for d in dirs:
        out_path = os.path.join(d, "hero_redmage.png")
        sheet.save(out_path, "PNG")
        print(f"Saved Red Mage sprite sheet: {out_path}")

if __name__ == "__main__":
    main()


    for d in dirs:
        out_path = os.path.join(d, "hero_redmage.png")
        sheet.save(out_path, "PNG")
        print(f"Saved Red Mage sprite sheet: {out_path}")

if __name__ == "__main__":
    main()
