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

def create_whitemage_spritesheet():
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))

    OUTLINE = (14, 18, 24, 255)

    # White Cleric Robe 5-tone ramp
    WHITE_5 = (145, 150, 170, 255)    # Deep shadow fold
    WHITE_4 = (185, 190, 210, 255)    # Shadow
    WHITE_3 = (220, 225, 238, 255)    # Base
    WHITE_2 = (242, 244, 250, 255)    # Light
    WHITE_1 = (255, 255, 255, 255)    # Pure highlight

    # Red Triangle Pattern 5-tone ramp
    RED_5 = (85, 5, 15, 255)
    RED_4 = (130, 15, 25, 255)
    RED_3 = (180, 25, 35, 255)
    RED_2 = (230, 45, 55, 255)
    RED_1 = (255, 100, 110, 255)

    # Skin 5-tone ramp
    SKIN_5 = (140, 90, 65, 255)
    SKIN_4 = (185, 130, 95, 255)
    SKIN_3 = (220, 165, 130, 255)
    SKIN_2 = (245, 200, 165, 255)
    SKIN_1 = (255, 220, 195, 255)

    # Golden Hair 5-tone ramp
    HAIR_5 = (135, 95, 10, 255)
    HAIR_4 = (175, 130, 20, 255)
    HAIR_3 = (215, 170, 35, 255)
    HAIR_2 = (245, 205, 65, 255)
    HAIR_1 = (255, 235, 135, 255)

    # Golden Wand 5-tone ramp
    GOLD_5 = (105, 70, 5, 255)
    GOLD_4 = (155, 110, 15, 255)
    GOLD_3 = (195, 150, 30, 255)
    GOLD_2 = (235, 190, 50, 255)
    GOLD_1 = (255, 225, 120, 255)

    # Holy Pearl Tip 5-tone ramp
    PEARL_5 = (120, 140, 180, 255)
    PEARL_4 = (170, 190, 220, 255)
    PEARL_3 = (210, 225, 245, 255)
    PEARL_2 = (240, 245, 255, 255)
    PEARL_1 = (255, 255, 255, 255)

    EYE_BLUE = (35, 105, 195, 255)

    for row in range(4):
        for col in range(4):
            frame = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame)

            bob = 1 if (col == 1 or col == 3) else 0
            cy = bob

            # Drop Shadow
            draw.ellipse([18, 52 + cy, 46, 59 + cy], fill=(0, 0, 0, 90))

            # White Cleric Robe
            draw.polygon([(18, 28 + cy), (46, 28 + cy), (50, 55 + cy), (14, 55 + cy)], fill=WHITE_3, outline=OUTLINE)
            draw.polygon([(18, 28 + cy), (32, 55 + cy), (14, 55 + cy)], fill=WHITE_4)
            draw.polygon([(14, 48 + cy), (22, 55 + cy), (14, 55 + cy)], fill=WHITE_5)
            draw.polygon([(36, 30 + cy), (46, 28 + cy), (44, 48 + cy)], fill=WHITE_2)
            draw.line([(25, 28 + cy), (27, 52 + cy)], fill=WHITE_1, width=1)

            # Red Triangle Pattern Hem
            for tx in range(16, 48, 8):
                draw.polygon([(tx, 54 + cy), (tx + 4, 45 + cy), (tx + 8, 54 + cy)], fill=RED_3, outline=OUTLINE)
                draw.polygon([(tx, 54 + cy), (tx + 4, 45 + cy), (tx + 4, 54 + cy)], fill=RED_4)
                draw.polygon([(tx + 4, 45 + cy), (tx + 6, 50 + cy), (tx + 4, 54 + cy)], fill=RED_2)

            # Cowl Hood & Head
            draw.polygon([(18, 12 + cy), (46, 12 + cy), (44, 27 + cy), (20, 27 + cy)], fill=WHITE_3, outline=OUTLINE)
            draw.polygon([(18, 12 + cy), (32, 27 + cy), (20, 27 + cy)], fill=WHITE_4)

            # Face & Hair Bangs
            draw.rectangle([24, 16 + cy, 40, 26 + cy], fill=SKIN_2)
            draw.rectangle([24, 24 + cy, 40, 26 + cy], fill=SKIN_3)

            if row != 3: # Front/Side Face Hair
                draw.polygon([(22, 12 + cy), (42, 12 + cy), (40, 18 + cy), (24, 18 + cy)], fill=HAIR_3)
                draw.polygon([(24, 12 + cy), (32, 12 + cy), (30, 17 + cy)], fill=HAIR_4)
                draw.polygon([(34, 12 + cy), (42, 12 + cy), (40, 16 + cy)], fill=HAIR_2)

            # Eyes
            if row == 0:
                draw.rectangle([26, 20 + cy, 28, 23 + cy], fill=EYE_BLUE)
                draw.rectangle([36, 20 + cy, 38, 23 + cy], fill=EYE_BLUE)
                draw.point((27, 20 + cy), fill=WHITE_1)
                draw.point((37, 20 + cy), fill=WHITE_1)
            elif row == 1:
                draw.rectangle([24, 20 + cy, 26, 23 + cy], fill=EYE_BLUE)
                draw.point((25, 20 + cy), fill=WHITE_1)
            elif row == 2:
                draw.rectangle([38, 20 + cy, 40, 23 + cy], fill=EYE_BLUE)
                draw.point((39, 20 + cy), fill=WHITE_1)

            # Golden Priest Wand with Holy Pearl Tip
            wx = 52 if (row == 0 or row == 2) else 12
            draw.line([(wx, 12 + cy), (wx, 54 + cy)], fill=GOLD_3, width=3)
            draw.line([(wx - 1, 14 + cy), (wx - 1, 52 + cy)], fill=GOLD_4, width=1)
            draw.line([(wx + 1, 14 + cy), (wx + 1, 52 + cy)], fill=GOLD_2, width=1)

            # Holy Pearl Tip
            draw.ellipse([wx - 5, 5 + cy, wx + 5, 15 + cy], fill=PEARL_3, outline=OUTLINE)
            draw.ellipse([wx - 3, 7 + cy, wx + 3, 13 + cy], fill=PEARL_2)
            draw.ellipse([wx - 1, 8 + cy, wx + 1, 10 + cy], fill=PEARL_1)

            sheet.paste(frame, (col * 64, row * 64))

    return sheet

def main():
    dirs = ensure_dirs()
    sheet = create_whitemage_spritesheet()
    for d in dirs:
        out_path = os.path.join(d, "hero_whitemage.png")
        sheet.save(out_path, "PNG")
        print(f"Saved White Mage sprite sheet: {out_path}")

if __name__ == "__main__":
    main()
