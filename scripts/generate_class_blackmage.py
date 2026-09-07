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

def create_blackmage_spritesheet():
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))

    # Master Color Palette (5-tone color ramps)
    OUTLINE = (14, 18, 24, 255)
    
    # Robe: Deep Blue 5-tone ramp
    ROBE_5 = (10, 25, 75, 255)      # Deep Shadow
    ROBE_4 = (20, 45, 120, 255)     # Shadow
    ROBE_3 = (35, 75, 175, 255)     # Base
    ROBE_2 = (65, 115, 215, 255)    # Light
    ROBE_1 = (110, 160, 245, 255)   # Highlight

    # Hat: Yellow 5-tone ramp
    HAT_5 = (125, 85, 5, 255)       # Deep Shadow
    HAT_4 = (185, 135, 15, 255)     # Shadow
    HAT_3 = (235, 185, 30, 255)     # Base
    HAT_2 = (250, 215, 60, 255)     # Light
    HAT_1 = (255, 240, 120, 255)    # Highlight

    # Oak Staff 5-tone ramp
    OAK_5 = (50, 25, 10, 255)
    OAK_4 = (80, 45, 18, 255)
    OAK_3 = (115, 70, 30, 255)
    OAK_2 = (145, 95, 50, 255)
    OAK_1 = (180, 125, 75, 255)

    # Orb & Eye Glowing Yellow/Arcane Cyan 5-tone ramp
    GLOW_5 = (180, 140, 0, 255)
    GLOW_4 = (215, 175, 10, 255)
    GLOW_3 = (255, 220, 30, 255)
    GLOW_2 = (255, 245, 100, 255)
    GLOW_1 = (255, 255, 220, 255)

    FACE_VOID = (12, 14, 20, 255)
    BELT_GOLD = (235, 190, 50, 255)

    for row in range(4): # 0=Down, 1=Left, 2=Right, 3=Up
        for col in range(4): # 4 animation frames
            frame = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame)

            bob = 1 if (col == 1 or col == 3) else 0
            cy = bob

            # Drop Shadow
            draw.ellipse([18, 52 + cy, 46, 59 + cy], fill=(0, 0, 0, 90))

            # Robe Skirt & Shading
            draw.polygon([(18, 30 + cy), (46, 30 + cy), (50, 55 + cy), (14, 55 + cy)], fill=ROBE_3, outline=OUTLINE)
            draw.polygon([(18, 30 + cy), (32, 55 + cy), (14, 55 + cy)], fill=ROBE_4)
            draw.polygon([(14, 50 + cy), (22, 55 + cy), (14, 55 + cy)], fill=ROBE_5)
            draw.polygon([(36, 32 + cy), (46, 30 + cy), (44, 48 + cy)], fill=ROBE_2)
            draw.line([(24, 30 + cy), (26, 52 + cy)], fill=ROBE_1, width=1)

            # Belt & Gold Buckle
            draw.rectangle([21, 38 + cy, 43, 41 + cy], fill=ROBE_5, outline=OUTLINE)
            draw.rectangle([29, 37 + cy, 35, 42 + cy], fill=BELT_GOLD, outline=OUTLINE)

            # Pitch-black shadow face & yellow pointed hat
            draw.rectangle([23, 16 + cy, 41, 28 + cy], fill=FACE_VOID)

            # Pointed Hat Base & Cone (Sways slightly on walk frames)
            sway = 1 if (col == 1 or col == 3) else 0
            draw.polygon([(14, 16 + cy), (50, 16 + cy), (32 + sway, -4 + cy)], fill=HAT_3, outline=OUTLINE)
            draw.polygon([(14, 16 + cy), (32 + sway, 16 + cy), (32 + sway, -4 + cy)], fill=HAT_4)
            draw.polygon([(14, 16 + cy), (22 + sway, 16 + cy), (32 + sway, -4 + cy)], fill=HAT_5)
            draw.polygon([(36 + sway, 10 + cy), (46, 16 + cy), (32 + sway, -4 + cy)], fill=HAT_2)
            draw.polygon([(30 + sway, 2 + cy), (32 + sway, -4 + cy), (34 + sway, 4 + cy)], fill=HAT_1)

            # Hat Brim
            draw.rectangle([12, 14 + cy, 52, 18 + cy], fill=HAT_3, outline=OUTLINE)
            draw.rectangle([13, 15 + cy, 32, 17 + cy], fill=HAT_4)
            draw.rectangle([33, 15 + cy, 51, 17 + cy], fill=HAT_2)

            # Eyes (Glowing yellow) based on direction
            if row == 0:  # DOWN
                draw.rectangle([25, 20 + cy, 29, 24 + cy], fill=GLOW_3)
                draw.rectangle([26, 21 + cy, 28, 23 + cy], fill=GLOW_1)
                draw.rectangle([35, 20 + cy, 39, 24 + cy], fill=GLOW_3)
                draw.rectangle([36, 21 + cy, 38, 23 + cy], fill=GLOW_1)
            elif row == 1:  # LEFT
                draw.rectangle([23, 20 + cy, 27, 24 + cy], fill=GLOW_3)
                draw.rectangle([24, 21 + cy, 26, 23 + cy], fill=GLOW_1)
            elif row == 2:  # RIGHT
                draw.rectangle([37, 20 + cy, 41, 24 + cy], fill=GLOW_3)
                draw.rectangle([38, 21 + cy, 40, 23 + cy], fill=GLOW_1)

            # Oak Staff with Glowing Orb
            wx = 52 if (row == 0 or row == 2) else 12
            draw.line([(wx, 10 + cy), (wx, 54 + cy)], fill=OAK_3, width=4)
            draw.line([(wx - 1, 12 + cy), (wx - 1, 52 + cy)], fill=OAK_4, width=1)
            draw.line([(wx + 1, 12 + cy), (wx + 1, 52 + cy)], fill=OAK_2, width=1)

            # Orb on top of staff
            draw.ellipse([wx - 6, 4 + cy, wx + 6, 16 + cy], fill=GLOW_4, outline=OUTLINE)
            draw.ellipse([wx - 4, 6 + cy, wx + 4, 14 + cy], fill=GLOW_3)
            draw.ellipse([wx - 2, 7 + cy, wx + 2, 11 + cy], fill=GLOW_1)

            sheet.paste(frame, (col * 64, row * 64))

    return sheet

def main():
    dirs = ensure_dirs()
    sheet = create_blackmage_spritesheet()
    for d in dirs:
        out_path = os.path.join(d, "hero_blackmage.png")
        sheet.save(out_path, "PNG")
        print(f"Saved Black Mage sprite sheet: {out_path}")

if __name__ == "__main__":
    main()
