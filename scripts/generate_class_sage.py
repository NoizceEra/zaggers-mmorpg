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
    OUTLINE = (12, 16, 24, 255)
    AO_CREVICE = (6, 8, 14, 255)

    EMERALD_1 = (160, 245, 185, 255) # Rim Light Peak
    EMERALD_2 = (85, 210, 125, 255)  # Highlight
    EMERALD_3 = (45, 165, 88, 255)   # Light
    EMERALD_4 = (26, 122, 58, 255)   # Midtone Base
    EMERALD_5 = (14, 82, 36, 255)    # Form Shadow
    EMERALD_6 = (8, 52, 22, 255)     # Deep Crease
    EMERALD_7 = (2, 24, 8, 255)      # Core AO

    WHITE_3 = (242, 244, 250, 255)
    WHITE_4 = (220, 225, 238, 255)
    WHITE_5 = (185, 190, 210, 255)

    HALO_1 = (255, 250, 180, 255)
    HALO_2 = (255, 225, 90, 255)
    HALO_3 = (240, 195, 45, 255)

    CRYSTAL_1 = (210, 250, 255, 255)
    CRYSTAL_2 = (110, 225, 250, 255)
    CRYSTAL_3 = (45, 185, 230, 255)

    STAFF_WOOD = (90, 55, 30, 255)
    SKIN = (245, 195, 155, 255)
    BOOK_BROWN = (145, 75, 35, 255)
    PAGE_CREAM = (245, 240, 220, 255)

    bob = 1 if (col == 1 or col == 3) else 0
    cy = bob

    # Ground Drop Shadow with Dual-Layer Occlusion
    draw.ellipse([14, 51 + cy, 50, 60 + cy], fill=(0, 0, 0, 70))
    draw.ellipse([18, 53 + cy, 46, 58 + cy], fill=(0, 0, 0, 140))

    # Golden Halo Aura & Ring floating above head
    draw.ellipse([21, 0 + cy, 43, 16 + cy], fill=(255, 225, 90, 45)) # Soft halo aura
    draw.ellipse([23, 2 + cy, 41, 14 + cy], fill=(0, 0, 0, 0), outline=HALO_3, width=2)
    draw.ellipse([25, 4 + cy, 39, 12 + cy], fill=(0, 0, 0, 0), outline=HALO_1, width=1)

    # Emerald Robe Skirt & 7-Tone Fold Shading with Front Slit
    leg = 2 if col == 1 else (-2 if col == 3 else 0)
    lx1, lx2 = 22 + leg, 29 + leg
    rx1, rx2 = 35 - leg, 42 - leg
    draw.rectangle([lx1, 44 + cy, lx2, 56 + cy], fill=(20, 30, 25, 255), outline=OUTLINE)
    draw.rectangle([rx1, 44 + cy, rx2, 56 + cy], fill=(20, 30, 25, 255), outline=OUTLINE)
    draw.line([(lx1, 44 + cy), (lx2, 44 + cy)], fill=AO_CREVICE, width=1)
    draw.line([(rx1, 44 + cy), (rx2, 44 + cy)], fill=AO_CREVICE, width=1)

    draw.polygon([(18, 30 + cy), (46, 30 + cy), (48, 54 + cy), (16, 54 + cy)], fill=EMERALD_4, outline=OUTLINE)
    draw.polygon([(18, 30 + cy), (32, 54 + cy), (16, 54 + cy)], fill=EMERALD_5)
    draw.polygon([(16, 50 + cy), (22, 54 + cy), (16, 54 + cy)], fill=EMERALD_6)
    draw.polygon([(36, 32 + cy), (46, 30 + cy), (44, 48 + cy)], fill=EMERALD_3)
    # Front Robe Slit
    draw.polygon([(29, 42 + cy), (35, 42 + cy), (37, 55 + cy), (27, 55 + cy)], fill=(8, 20, 15, 255))
    draw.line([(17, 31 + cy), (17, 54 + cy)], fill=EMERALD_1, width=1) # Rim light
    draw.line([(18, 53 + cy), (46, 53 + cy)], fill=HALO_3, width=2)

    # TIGHT ARTICULATED SCHOLASTIC SLEEVES & WHITE GLOVED HANDS
    draw.polygon([(15, 26 + cy), (22, 27 + cy), (20, 37 + cy), (14, 34 + cy)], fill=EMERALD_3, outline=OUTLINE)
    draw.rectangle([14, 35 + cy, 21, 44 + cy], fill=EMERALD_5, outline=OUTLINE) # Scholastic sleeve
    draw.rectangle([14, 42 + cy, 20, 47 + cy], fill=WHITE_3, outline=OUTLINE) # Gloved hand

    draw.polygon([(49, 26 + cy), (42, 27 + cy), (44, 37 + cy), (50, 34 + cy)], fill=EMERALD_4, outline=OUTLINE)
    draw.rectangle([43, 35 + cy, 50, 44 + cy], fill=EMERALD_6, outline=OUTLINE) # Scholastic sleeve
    draw.rectangle([44, 42 + cy, 50, 47 + cy], fill=WHITE_3, outline=OUTLINE) # Gloved hand

    # White Hood Cowl & Head
    draw.polygon([(18, 12 + cy), (46, 12 + cy), (44, 27 + cy), (20, 27 + cy)], fill=WHITE_4, outline=OUTLINE)
    draw.polygon([(18, 12 + cy), (32, 27 + cy), (20, 27 + cy)], fill=WHITE_5)
    draw.rectangle([24, 16 + cy, 40, 26 + cy], fill=SKIN)
    draw.line([(18, 27 + cy), (46, 27 + cy)], fill=AO_CREVICE, width=1) # Neck AO

    if row == 0:
        draw.rectangle([26, 20 + cy, 28, 23 + cy], fill=OUTLINE)
        draw.rectangle([36, 20 + cy, 38, 23 + cy], fill=OUTLINE)
        draw.point((27, 20 + cy), fill=CRYSTAL_1)
        draw.point((37, 20 + cy), fill=CRYSTAL_1)

    # Spellbook Grimoire (Held in left hand)
    draw.rectangle([12, 30 + cy, 22, 46 + cy], fill=BOOK_BROWN, outline=OUTLINE)
    draw.rectangle([14, 32 + cy, 20, 44 + cy], fill=PAGE_CREAM)
    draw.line([(17, 32 + cy), (17, 44 + cy)], fill=OUTLINE, width=1)
    draw.rectangle([15, 36 + cy, 17, 38 + cy], fill=CRYSTAL_3)

    # Crystal Staff (Right hand)
    wx = 48 if (row == 0 or row == 2) else 16
    draw.line([(wx, 12 + cy), (wx, 54 + cy)], fill=STAFF_WOOD, width=3)
    draw.polygon([(wx, 2 + cy), (wx - 5, 10 + cy), (wx, 18 + cy), (wx + 5, 10 + cy)], fill=CRYSTAL_3, outline=OUTLINE)
    draw.polygon([(wx, 2 + cy), (wx - 5, 10 + cy), (wx, 10 + cy)], fill=CRYSTAL_2)
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


