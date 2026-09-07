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
    OUTLINE = (14, 18, 24, 255)

    CRIMSON_5 = (95, 5, 18, 255)
    CRIMSON_4 = (145, 15, 30, 255)
    CRIMSON_3 = (195, 30, 50, 255)
    CRIMSON_2 = (225, 55, 75, 255)
    CRIMSON_1 = (245, 90, 105, 255)

    FEATHER_5 = (130, 138, 165, 255)
    FEATHER_4 = (175, 182, 205, 255)
    FEATHER_3 = (215, 220, 235, 255)
    FEATHER_2 = (240, 242, 248, 255)
    FEATHER_1 = (255, 255, 255, 255)

    STEEL_5 = (80, 90, 110, 255)
    STEEL_4 = (125, 138, 160, 255)
    STEEL_3 = (175, 188, 208, 255)
    STEEL_2 = (220, 230, 245, 255)
    STEEL_1 = (255, 255, 255, 255)

    GOLD_3 = (235, 190, 50, 255)
    GOLD_2 = (250, 215, 80, 255)

    SKIN = (245, 200, 165, 255)
    HAIR_DARK = (45, 35, 40, 255)

    BOOK_COVER = (140, 20, 30, 255)
    BOOK_PAGES = (245, 240, 220, 255)

    bob = 1 if (col == 1 or col == 3) else 0
    leg_step = 3 if col == 1 else (-3 if col == 3 else 0)
    cy = bob

    # Drop Shadow
    draw.ellipse([18, 52 + cy, 46, 59 + cy], fill=(0, 0, 0, 90))

    # Trousers / Legs
    lx1, lx2 = 23 + leg_step, 29 + leg_step
    rx1, rx2 = 35 - leg_step, 41 - leg_step
    draw.rectangle([lx1, 44 + cy, lx2, 55 + cy], fill=CRIMSON_4, outline=OUTLINE)
    draw.rectangle([rx1, 44 + cy, rx2, 55 + cy], fill=CRIMSON_4, outline=OUTLINE)

    # Crimson Doublet
    draw.rectangle([21, 26 + cy, 43, 44 + cy], fill=CRIMSON_3, outline=OUTLINE)
    draw.rectangle([25, 28 + cy, 39, 42 + cy], fill=CRIMSON_2)
    draw.line([(32, 26 + cy), (32, 44 + cy)], fill=GOLD_3, width=2)

    # Head & Hair
    draw.rectangle([23, 14 + cy, 41, 28 + cy], fill=SKIN, outline=OUTLINE)
    draw.rectangle([22, 14 + cy, 42, 18 + cy], fill=HAIR_DARK)

    # Feathered Chapeau Cap
    draw.polygon([(16, 10 + cy), (48, 10 + cy), (42, 17 + cy), (22, 17 + cy)], fill=CRIMSON_4, outline=OUTLINE)
    draw.polygon([(18, 11 + cy), (34, 11 + cy), (32, 16 + cy)], fill=CRIMSON_3)

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
    draw.line([(50, 12 + cy), (50, 48 + cy)], fill=STEEL_2, width=2)
    draw.line([(51, 14 + cy), (51, 46 + cy)], fill=STEEL_1, width=1)
    draw.ellipse([45, 36 + cy, 55, 43 + cy], fill=GOLD_3, outline=OUTLINE)
    draw.ellipse([47, 38 + cy, 53, 41 + cy], fill=GOLD_2)

    # Spellbook Grimoire (Left hip / hand)
    draw.rectangle([10, 32 + cy, 20, 44 + cy], fill=BOOK_COVER, outline=OUTLINE)
    draw.rectangle([12, 34 + cy, 18, 42 + cy], fill=BOOK_PAGES)
    draw.line([(15, 34 + cy), (15, 42 + cy)], fill=GOLD_3, width=1)

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
