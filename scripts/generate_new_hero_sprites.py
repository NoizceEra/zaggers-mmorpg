import os
import math
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

def save_sprite(img, name, dirs):
    for d in dirs:
        path = os.path.join(d, name)
        img.save(path, "PNG")
        print(f"Saved Hero Sprite: {path} ({img.size[0]}x{img.size[1]})")

def draw_base_hero(draw, row, col, skin_color, hair_color, armor_color, accent_color, is_female=False):
    """
    Renders 64x64 frame for a hero sprite.
    row: 0=Down, 1=Left, 2=Right, 3=Up
    col: 0=Idle1, 1=Idle2, 2=Walk1, 3=Walk2
    """
    cx = 32
    cy = 32
    bob = 1 if (col == 1 or col == 3) else 0
    cy += bob
    step = 2 if col == 2 else (-2 if col == 3 else 0)

    # Shadow
    draw.ellipse([cx - 12, cy + 20, cx + 12, cy + 26], fill=(0, 0, 0, 80))

    # Legs / Boots
    boot_color = (40, 40, 50, 255)
    if row == 0 or row == 3: # Down or Up
        draw.rectangle([cx - 8 + step, cy + 12, cx - 2 + step, cy + 22], fill=boot_color)
        draw.rectangle([cx + 2 - step, cy + 12, cx + 8 - step, cy + 22], fill=boot_color)
    else: # Left or Right
        draw.rectangle([cx - 5 + step, cy + 12, cx + 5 + step, cy + 22], fill=boot_color)

    # Torso / Armor
    draw.rectangle([cx - 10, cy - 2, cx + 10, cy + 12], fill=armor_color)
    draw.rectangle([cx - 8, cy, cx + 8, cy + 10], fill=accent_color)

    # Head / Face
    draw.rectangle([cx - 9, cy - 20, cx + 9, cy - 2], fill=skin_color)

    # Eyes (Front & Side)
    if row == 0: # Down
        draw.rectangle([cx - 6, cy - 12, cx - 3, cy - 8], fill=(20, 20, 20, 255))
        draw.rectangle([cx + 3, cy - 12, cx + 6, cy - 8], fill=(20, 20, 20, 255))
    elif row == 1: # Left
        draw.rectangle([cx - 7, cy - 12, cx - 4, cy - 8], fill=(20, 20, 20, 255))
    elif row == 2: # Right
        draw.rectangle([cx + 4, cy - 12, cx + 7, cy - 8], fill=(20, 20, 20, 255))

    # Hair / Helmet
    draw.rectangle([cx - 10, cy - 23, cx + 10, cy - 14], fill=hair_color)
    if row != 3: # Front fringe
        draw.polygon([(cx - 9, cy - 15), (cx - 4, cy - 10), (cx, cy - 15), (cx + 4, cy - 10), (cx + 9, cy - 15)], fill=hair_color)

def generate_hero_sheet(skin, hair, armor, accent):
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    for row in range(4):
        for col in range(4):
            frame_img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame_img)
            draw_base_hero(draw, row, col, skin, hair, armor, accent)
            sheet.paste(frame_img, (col * 64, row * 64))
    return sheet

def main():
    dirs = ensure_dirs()

    # 1. Dragoon (Dark purple dragon armor, silver trim, golden hair)
    dragoon = generate_hero_sheet(
        skin=(255, 224, 189, 255), hair=(255, 215, 0, 255),
        armor=(60, 40, 90, 255), accent=(190, 190, 210, 255)
    )
    save_sprite(dragoon, "hero_dragoon.png", dirs)

    # 2. Monk (Martial arts white gi, red belt, dark hair)
    monk = generate_hero_sheet(
        skin=(240, 200, 160, 255), hair=(40, 40, 40, 255),
        armor=(245, 245, 245, 255), accent=(200, 30, 40, 255)
    )
    save_sprite(monk, "hero_monk.png", dirs)

    # 3. Paladin (Golden holy armor, blue cape, blonde hair)
    paladin = generate_hero_sheet(
        skin=(255, 224, 189, 255), hair=(255, 230, 120, 255),
        armor=(230, 180, 40, 255), accent=(30, 100, 200, 255)
    )
    save_sprite(paladin, "hero_paladin.png", dirs)

    # 4. Sage (Scholastic emerald green robes, silver trim, brown hair)
    sage = generate_hero_sheet(
        skin=(255, 224, 189, 255), hair=(100, 60, 30, 255),
        armor=(30, 120, 80, 255), accent=(220, 220, 220, 255)
    )
    save_sprite(sage, "hero_sage.png", dirs)

    # 5. Bard (Crimson minstrel doublet, gold trim, auburn hair)
    bard = generate_hero_sheet(
        skin=(255, 224, 189, 255), hair=(180, 80, 40, 255),
        armor=(180, 40, 60, 255), accent=(240, 200, 80, 255)
    )
    save_sprite(bard, "hero_bard.png", dirs)

    # 6. Alchemist (Copper smith aprons, turquoise flask belt, dark hair)
    alchemist = generate_hero_sheet(
        skin=(255, 224, 189, 255), hair=(50, 40, 35, 255),
        armor=(160, 90, 40, 255), accent=(40, 180, 160, 255)
    )
    save_sprite(alchemist, "hero_alchemist.png", dirs)

if __name__ == "__main__":
    main()
