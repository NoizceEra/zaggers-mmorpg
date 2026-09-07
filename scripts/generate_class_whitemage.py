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

def draw_whitemage_frame(draw, row, col):
    OUTLINE = (12, 16, 24, 255)
    AO_CREVICE = (6, 8, 14, 255)

    # White Cleric Robe 7-tone ramp
    WHITE_7 = (115, 120, 140, 255)   # Core AO Crevice
    WHITE_6 = (145, 150, 170, 255)   # Deep Shadow
    WHITE_5 = (185, 190, 210, 255)   # Shadow
    WHITE_4 = (220, 225, 238, 255)   # Midtone Base
    WHITE_3 = (242, 244, 250, 255)   # Light Tone
    WHITE_2 = (250, 252, 255, 255)   # Highlight
    WHITE_1 = (255, 255, 255, 255)   # Pure Glint / Rim Light

    RED_3 = (195, 25, 40, 255)
    RED_4 = (145, 15, 28, 255)
    RED_2 = (235, 55, 70, 255)

    SKIN_2 = (245, 200, 165, 255)
    SKIN_3 = (215, 165, 130, 255)

    HAIR_BASE = (235, 185, 45, 255)
    HAIR_LIGHT = (255, 215, 80, 255)
    HAIR_DARK = (175, 130, 20, 255)

    GOLD_3 = (215, 168, 30, 255)
    GOLD_2 = (250, 215, 75, 255)

    PEARL_1 = (255, 255, 255, 255)
    PEARL_2 = (240, 245, 255, 255)
    PEARL_3 = (210, 225, 245, 255)
    PEARL_4 = (170, 190, 220, 255)

    EYE_BLUE = (35, 105, 195, 255)

    bob = 1 if (col == 1 or col == 3) else 0
    cy = bob

    # Ground Drop Shadow with Dual-Layer Occlusion
    draw.ellipse([14, 51 + cy, 50, 60 + cy], fill=(0, 0, 0, 70))
    draw.ellipse([18, 53 + cy, 46, 58 + cy], fill=(0, 0, 0, 140))

    # White Cleric Robe & 7-Tone Fold Shading
    draw.polygon([(18, 28 + cy), (46, 28 + cy), (50, 55 + cy), (14, 55 + cy)], fill=WHITE_4, outline=OUTLINE)
    draw.polygon([(18, 28 + cy), (32, 55 + cy), (14, 55 + cy)], fill=WHITE_5)
    draw.polygon([(14, 48 + cy), (22, 55 + cy), (14, 55 + cy)], fill=WHITE_6)
    draw.polygon([(36, 30 + cy), (46, 28 + cy), (44, 48 + cy)], fill=WHITE_3)
    draw.line([(25, 28 + cy), (27, 52 + cy)], fill=WHITE_1, width=1)
    draw.line([(15, 29 + cy), (15, 54 + cy)], fill=WHITE_1, width=1) # Rim light

    # Red Triangle Pattern Hem
    for tx in range(16, 48, 8):
        draw.polygon([(tx, 54 + cy), (tx + 4, 45 + cy), (tx + 8, 54 + cy)], fill=RED_3, outline=OUTLINE)
        draw.polygon([(tx, 54 + cy), (tx + 4, 45 + cy), (tx + 4, 54 + cy)], fill=RED_4)
        draw.polygon([(tx + 4, 45 + cy), (tx + 6, 50 + cy), (tx + 4, 54 + cy)], fill=RED_2)

    # Cowl Hood & Head
    draw.polygon([(18, 12 + cy), (46, 12 + cy), (44, 27 + cy), (20, 27 + cy)], fill=WHITE_4, outline=OUTLINE)
    draw.polygon([(18, 12 + cy), (32, 27 + cy), (20, 27 + cy)], fill=WHITE_5)
    draw.line([(18, 27 + cy), (46, 27 + cy)], fill=AO_CREVICE, width=1) # Neck AO

    # Face & Hair Bangs
    draw.rectangle([24, 16 + cy, 40, 26 + cy], fill=SKIN_2)
    draw.rectangle([24, 24 + cy, 40, 26 + cy], fill=SKIN_3)

    if row != 3:
        draw.polygon([(22, 12 + cy), (42, 12 + cy), (40, 18 + cy), (24, 18 + cy)], fill=HAIR_BASE)
        draw.polygon([(24, 12 + cy), (32, 12 + cy), (30, 17 + cy)], fill=HAIR_DARK)
        draw.polygon([(34, 12 + cy), (42, 12 + cy), (40, 16 + cy)], fill=HAIR_LIGHT)

    # Eyes & Specular Glint
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

    # Golden Priest Wand with Holy Pearl Tip & Radiant Aura
    wx = 52 if (row == 0 or row == 2) else 12
    draw.line([(wx, 12 + cy), (wx, 54 + cy)], fill=GOLD_3, width=3)
    draw.line([(wx - 1, 14 + cy), (wx - 1, 52 + cy)], fill=GOLD_2, width=1)

    # Holy Pearl Tip Aura Rings
    draw.ellipse([wx - 7, 3 + cy, wx + 7, 17 + cy], fill=(255, 255, 255, 50)) # Soft holy aura
    draw.ellipse([wx - 5, 5 + cy, wx + 5, 15 + cy], fill=PEARL_3, outline=OUTLINE)
    draw.ellipse([wx - 3, 7 + cy, wx + 3, 13 + cy], fill=PEARL_2)
    draw.ellipse([wx - 1, 8 + cy, wx + 1, 10 + cy], fill=PEARL_1)

def create_whitemage_spritesheet():
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    for row in range(4):
        for col in range(4):
            frame = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame)
            draw_whitemage_frame(draw, row, col)
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


    for d in dirs:
        out_path = os.path.join(d, "hero_whitemage.png")
        sheet.save(out_path, "PNG")
        print(f"Saved White Mage sprite sheet: {out_path}")

if __name__ == "__main__":
    main()
