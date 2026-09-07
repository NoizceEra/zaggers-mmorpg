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

def draw_blackmage_frame(draw, row, col):
    OUTLINE = (12, 16, 24, 255)
    AO_CREVICE = (6, 8, 14, 255)

    # Robe: Deep Blue 7-tone ramp
    ROBE_7 = (4, 10, 42, 255)       # Core AO
    ROBE_6 = (8, 24, 75, 255)       # Deep Crease
    ROBE_5 = (16, 44, 120, 255)     # Shadow
    ROBE_4 = (28, 72, 170, 255)     # Midtone Base
    ROBE_3 = (50, 110, 215, 255)    # Light Tone
    ROBE_2 = (95, 155, 250, 255)    # Highlight
    ROBE_1 = (165, 210, 255, 255)   # Rim Light

    # Hat: Yellow 7-tone ramp
    HAT_7 = (60, 38, 2, 255)        # Deep Crevice
    HAT_6 = (95, 62, 5, 255)        # Deep Shadow
    HAT_5 = (145, 100, 10, 255)     # Shadow
    HAT_4 = (195, 145, 18, 255)     # Midtone Base
    HAT_3 = (240, 190, 30, 255)     # Light Tone
    HAT_2 = (255, 220, 75, 255)     # Specular
    HAT_1 = (255, 245, 150, 255)    # Peak Glint

    OAK_BASE = (115, 70, 30, 255)
    OAK_DARK = (65, 36, 14, 255)

    GLOW_1 = (255, 255, 220, 255)
    GLOW_2 = (255, 245, 100, 255)
    GLOW_3 = (255, 220, 30, 255)
    GLOW_4 = (215, 160, 10, 255)
    GLOW_5 = (150, 100, 0, 255)

    FACE_VOID = (8, 10, 16, 255)
    BELT_GOLD = (240, 190, 40, 255)

    bob = 1 if (col == 1 or col == 3) else 0
    cy = bob

    # Ground Drop Shadow with Dual-Layer Occlusion
    draw.ellipse([14, 51 + cy, 50, 60 + cy], fill=(0, 0, 0, 70))
    draw.ellipse([18, 53 + cy, 46, 58 + cy], fill=(0, 0, 0, 140))

    # Robe Skirt & 7-Tone Fold Shading
    draw.polygon([(18, 30 + cy), (46, 30 + cy), (50, 55 + cy), (14, 55 + cy)], fill=ROBE_4, outline=OUTLINE)
    draw.polygon([(18, 30 + cy), (32, 55 + cy), (14, 55 + cy)], fill=ROBE_5)
    draw.polygon([(14, 50 + cy), (22, 55 + cy), (14, 55 + cy)], fill=ROBE_6)
    draw.polygon([(36, 32 + cy), (46, 30 + cy), (44, 48 + cy)], fill=ROBE_3)
    draw.line([(24, 30 + cy), (26, 52 + cy)], fill=ROBE_2, width=1)
    draw.line([(15, 31 + cy), (15, 54 + cy)], fill=ROBE_1, width=1) # Rim light left

    # Belt & Gold Buckle
    draw.rectangle([21, 38 + cy, 43, 41 + cy], fill=ROBE_6, outline=OUTLINE)
    draw.rectangle([29, 37 + cy, 35, 42 + cy], fill=BELT_GOLD, outline=OUTLINE)
    draw.line([(21, 38 + cy), (43, 38 + cy)], fill=AO_CREVICE, width=1)

    # Pitch-black shadow face & yellow pointed hat
    draw.rectangle([23, 16 + cy, 41, 28 + cy], fill=FACE_VOID)

    # Pointed Hat Base & Cone
    sway = 1 if (col == 1 or col == 3) else 0
    draw.polygon([(14, 16 + cy), (50, 16 + cy), (32 + sway, -4 + cy)], fill=HAT_4, outline=OUTLINE)
    draw.polygon([(14, 16 + cy), (32 + sway, 16 + cy), (32 + sway, -4 + cy)], fill=HAT_5)
    draw.polygon([(14, 16 + cy), (22 + sway, 16 + cy), (32 + sway, -4 + cy)], fill=HAT_6)
    draw.polygon([(36 + sway, 10 + cy), (46, 16 + cy), (32 + sway, -4 + cy)], fill=HAT_3)
    draw.polygon([(30 + sway, 2 + cy), (32 + sway, -4 + cy), (34 + sway, 4 + cy)], fill=HAT_1)

    # Hat Brim & AO Crevice Line
    draw.rectangle([12, 14 + cy, 52, 18 + cy], fill=HAT_4, outline=OUTLINE)
    draw.rectangle([13, 15 + cy, 32, 17 + cy], fill=HAT_5)
    draw.rectangle([33, 15 + cy, 51, 17 + cy], fill=HAT_3)
    draw.line([(13, 18 + cy), (51, 18 + cy)], fill=AO_CREVICE, width=1) # Hat brim AO

    # Eyes (Glowing yellow)
    if row == 0:
        draw.rectangle([25, 20 + cy, 29, 24 + cy], fill=GLOW_3)
        draw.rectangle([26, 21 + cy, 28, 23 + cy], fill=GLOW_1)
        draw.rectangle([35, 20 + cy, 39, 24 + cy], fill=GLOW_3)
        draw.rectangle([36, 21 + cy, 38, 23 + cy], fill=GLOW_1)
    elif row == 1:
        draw.rectangle([23, 20 + cy, 27, 24 + cy], fill=GLOW_3)
        draw.rectangle([24, 21 + cy, 26, 23 + cy], fill=GLOW_1)
    elif row == 2:
        draw.rectangle([37, 20 + cy, 41, 24 + cy], fill=GLOW_3)
        draw.rectangle([38, 21 + cy, 40, 23 + cy], fill=GLOW_1)

    # Oak Staff with Glowing Arcane Orb & Outer Aura
    wx = 52 if (row == 0 or row == 2) else 12
    draw.line([(wx, 10 + cy), (wx, 54 + cy)], fill=OAK_BASE, width=4)
    draw.line([(wx - 1, 12 + cy), (wx - 1, 52 + cy)], fill=OAK_DARK, width=1)

    # Orb Aura Rings
    draw.ellipse([wx - 7, 3 + cy, wx + 7, 17 + cy], fill=(255, 220, 30, 40)) # Soft aura
    draw.ellipse([wx - 6, 4 + cy, wx + 6, 16 + cy], fill=GLOW_4, outline=OUTLINE)
    draw.ellipse([wx - 4, 6 + cy, wx + 4, 14 + cy], fill=GLOW_3)
    draw.ellipse([wx - 2, 7 + cy, wx + 2, 11 + cy], fill=GLOW_1)

def create_blackmage_spritesheet():
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    for row in range(4):
        for col in range(4):
            frame = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame)
            draw_blackmage_frame(draw, row, col)
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


