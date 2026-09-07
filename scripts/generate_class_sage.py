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

def draw_sage_frame(draw, row, col):
    OUTLINE = (14, 18, 24, 255)

    EMERALD_5 = (10, 60, 32, 255)
    EMERALD_4 = (20, 95, 55, 255)
    EMERALD_3 = (35, 140, 85, 255)
    EMERALD_2 = (65, 185, 115, 255)
    EMERALD_1 = (110, 225, 155, 255)

    WHITE_5 = (140, 145, 160, 255)
    WHITE_4 = (180, 185, 200, 255)
    WHITE_3 = (220, 225, 240, 255)
    WHITE_2 = (240, 245, 255, 255)
    WHITE_1 = (255, 255, 255, 255)

    HALO_5 = (140, 100, 10, 255)
    HALO_4 = (195, 150, 25, 255)
    HALO_3 = (240, 195, 45, 255)
    HALO_2 = (255, 225, 90, 255)
    HALO_1 = (255, 250, 180, 255)

    CRYSTAL_5 = (15, 80, 120, 255)
    CRYSTAL_4 = (25, 130, 180, 255)
    CRYSTAL_3 = (45, 185, 230, 255)
    CRYSTAL_2 = (110, 225, 250, 255)
    CRYSTAL_1 = (210, 250, 255, 255)

    STAFF_WOOD = (90, 55, 30, 255)
    SKIN = (245, 200, 165, 255)
    BOOK_BROWN = (145, 75, 35, 255)
    PAGE_CREAM = (245, 240, 220, 255)

    bob = 1 if (col == 1 or col == 3) else 0
    cy = bob

    # Drop Shadow
    draw.ellipse([18, 52 + cy, 46, 59 + cy], fill=(0, 0, 0, 90))

    # Golden Halo floating above head
    draw.ellipse([23, 2 + cy, 41, 14 + cy], fill=(0, 0, 0, 0), outline=HALO_3, width=2)
    draw.ellipse([25, 4 + cy, 39, 12 + cy], fill=(0, 0, 0, 0), outline=HALO_1, width=1)

    # Emerald Robe Skirt
    draw.polygon([(18, 30 + cy), (46, 30 + cy), (50, 55 + cy), (14, 55 + cy)], fill=EMERALD_3, outline=OUTLINE)
    draw.polygon([(18, 30 + cy), (32, 55 + cy), (14, 55 + cy)], fill=EMERALD_4)
    draw.polygon([(14, 50 + cy), (22, 55 + cy), (14, 55 + cy)], fill=EMERALD_5)
    draw.polygon([(36, 32 + cy), (46, 30 + cy), (44, 48 + cy)], fill=EMERALD_2)
    draw.line([(16, 53 + cy), (48, 53 + cy)], fill=HALO_3, width=2)

    # White Hood Cowl & Head
    draw.polygon([(18, 12 + cy), (46, 12 + cy), (44, 27 + cy), (20, 27 + cy)], fill=WHITE_3, outline=OUTLINE)
    draw.polygon([(18, 12 + cy), (32, 27 + cy), (20, 27 + cy)], fill=WHITE_4)
    draw.rectangle([24, 16 + cy, 40, 26 + cy], fill=SKIN)

    if row == 0:
        draw.rectangle([26, 20 + cy, 28, 23 + cy], fill=OUTLINE)
        draw.rectangle([36, 20 + cy, 38, 23 + cy], fill=OUTLINE)

    # Spellbook Grimoire (Held in left hand)
    draw.rectangle([10, 30 + cy, 22, 46 + cy], fill=BOOK_BROWN, outline=OUTLINE)
    draw.rectangle([12, 32 + cy, 20, 44 + cy], fill=PAGE_CREAM)
    draw.line([(16, 32 + cy), (16, 44 + cy)], fill=OUTLINE, width=1)
    draw.rectangle([13, 36 + cy, 15, 38 + cy], fill=CRYSTAL_3)

    # Crystal Staff (Right hand)
    wx = 52 if (row == 0 or row == 2) else 12
    draw.line([(wx, 12 + cy), (wx, 54 + cy)], fill=STAFF_WOOD, width=3)

    # Crystal Gem at top
    draw.polygon([(wx, 2 + cy), (wx - 5, 10 + cy), (wx, 18 + cy), (wx + 5, 10 + cy)], fill=CRYSTAL_3, outline=OUTLINE)
    draw.polygon([(wx, 2 + cy), (wx - 5, 10 + cy), (wx, 10 + cy)], fill=CRYSTAL_4)
    draw.polygon([(wx, 2 + cy), (wx + 5, 10 + cy), (wx, 10 + cy)], fill=CRYSTAL_2)
    draw.polygon([(wx - 1, 4 + cy), (wx + 1, 4 + cy), (wx, 8 + cy)], fill=CRYSTAL_1)

def create_sage_spritesheet():
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    for row in range(4):
        for col in range(4):
            frame = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame)
            draw_sage_frame(draw, row, col)
            sheet.paste(frame, (col * 64, row * 64))
    return sheet

def main():
    dirs = ensure_dirs()
    sheet = create_sage_spritesheet()
    for d in dirs:
        out_path = os.path.join(d, "hero_sage.png")
        sheet.save(out_path, "PNG")
        print(f"Saved Sage sprite sheet: {out_path}")

if __name__ == "__main__":
    main()

