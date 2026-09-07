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

def create_hero_ranger_sprite():
    """
    Ranger Marksman Sprite Sheet:
    256x256 RGBA (4 cols x 4 rows of 64x64 frames)
    Rows (dir): 0=Down, 1=Left, 2=Right, 3=Up
    Cols (frame): 0=Idle1, 1=Idle2, 2=Walk1, 3=Walk2
    Visual Features:
    - Green hooded cloak
    - Leather armor chestpiece & belt
    - Composite bow
    - Quiver of arrows on back
    """
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))

    # Color Palette
    SKIN = (245, 205, 170, 255)
    SKIN_SHADOW = (215, 165, 130, 255)
    EYE_GREEN = (30, 140, 70, 255)

    HOOD_GREEN = (40, 120, 55, 255)
    HOOD_SHADOW = (25, 80, 35, 255)
    HOOD_HIGHLIGHT = (65, 160, 80, 255)

    CLOAK_DARK = (20, 65, 30, 255)

    LEATHER_BROWN = (135, 80, 40, 255)
    LEATHER_DARK = (90, 50, 25, 255)
    LEATHER_LIGHT = (175, 110, 60, 255)
    BUCKLE_GOLD = (220, 175, 50, 255)

    BOOT_BROWN = (65, 40, 20, 255)
    BOOT_CUFF = (95, 60, 30, 255)

    BOW_WOOD = (160, 95, 45, 255)
    BOW_DARK = (110, 60, 25, 255)
    BOW_TIP = (200, 200, 210, 255)
    STRING_WHITE = (230, 235, 240, 200)

    QUIVER_BROWN = (110, 65, 35, 255)
    ARROW_SHAFT = (180, 140, 95, 255)
    FLETCHING_RED = (210, 45, 45, 255)
    FLETCHING_WHITE = (240, 240, 245, 255)

    OUTLINE = (20, 25, 20, 255)

    for row in range(4):
        for col in range(4):
            x_off = col * 64
            y_off = row * 64
            frame = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame)

            bob = 1 if (col == 1 or col == 3) else 0
            leg_step = 2 if col == 2 else (-2 if col == 3 else 0)
            cy = bob

            # Drop Shadow
            draw.ellipse([20, 53, 44, 59], fill=(0, 0, 0, 90))

            if row == 0:  # DOWN (Facing front)
                # Quiver behind shoulder (right side of back)
                draw.rectangle([40, 22 + cy, 47, 40 + cy], fill=QUIVER_BROWN, outline=OUTLINE)
                # Arrow fletchings in quiver
                draw.polygon([(41, 14 + cy), (44, 14 + cy), (42, 22 + cy)], fill=FLETCHING_RED)
                draw.polygon([(44, 12 + cy), (47, 12 + cy), (45, 22 + cy)], fill=FLETCHING_WHITE)
                draw.polygon([(46, 15 + cy), (49, 15 + cy), (47, 22 + cy)], fill=FLETCHING_RED)

                # Boots & Legs
                draw.rectangle([23 + leg_step, 45 + cy, 29 + leg_step, 56 + cy], fill=BOOT_BROWN, outline=OUTLINE)
                draw.rectangle([35 - leg_step, 45 + cy, 41 - leg_step, 56 + cy], fill=BOOT_BROWN, outline=OUTLINE)
                draw.rectangle([22 + leg_step, 44 + cy, 30 + leg_step, 47 + cy], fill=BOOT_CUFF)
                draw.rectangle([34 - leg_step, 44 + cy, 42 - leg_step, 47 + cy], fill=BOOT_CUFF)

                # Back Cloak Drapes
                draw.polygon([(18, 30 + cy), (23, 30 + cy), (16, 50 + cy), (14, 48 + cy)], fill=CLOAK_DARK)
                draw.polygon([(41, 30 + cy), (46, 30 + cy), (50, 48 + cy), (48, 50 + cy)], fill=CLOAK_DARK)

                # Tunic & Leather Armor Body
                draw.rectangle([23, 30 + cy, 41, 44 + cy], fill=LEATHER_BROWN, outline=OUTLINE)
                draw.rectangle([26, 32 + cy, 38, 42 + cy], fill=LEATHER_LIGHT)
                # Leather Straps & Buckle
                draw.line([(24, 33 + cy), (40, 41 + cy)], fill=LEATHER_DARK, width=2)
                draw.line([(40, 33 + cy), (24, 41 + cy)], fill=LEATHER_DARK, width=2)
                draw.rectangle([30, 35 + cy, 34, 39 + cy], fill=BUCKLE_GOLD, outline=OUTLINE)

                # Arms / Sleeves
                draw.rectangle([18, 31 + cy, 23, 40 + cy], fill=HOOD_GREEN, outline=OUTLINE)
                draw.ellipse([18, 39 + cy, 23, 44 + cy], fill=SKIN)
                draw.rectangle([41, 31 + cy, 46, 40 + cy], fill=HOOD_GREEN, outline=OUTLINE)
                draw.ellipse([41, 39 + cy, 46, 44 + cy], fill=SKIN)

                # Hood & Face
                draw.rectangle([22, 16 + cy, 42, 31 + cy], fill=HOOD_GREEN, outline=OUTLINE)
                # Hood Shadow Opening
                draw.polygon([(23, 20 + cy), (41, 20 + cy), (39, 31 + cy), (25, 31 + cy)], fill=HOOD_SHADOW)
                # Face visible inside hood
                draw.rectangle([25, 22 + cy, 39, 30 + cy], fill=SKIN)
                # Eyes
                draw.rectangle([27, 25 + cy, 29, 28 + cy], fill=EYE_GREEN)
                draw.rectangle([35, 25 + cy, 37, 28 + cy], fill=EYE_GREEN)
                # Hood Cowl / Shoulder drape
                draw.polygon([(18, 29 + cy), (46, 29 + cy), (42, 35 + cy), (22, 35 + cy)], fill=HOOD_GREEN, outline=OUTLINE)

                # Composite Bow in hand (left hand foreground)
                draw.arc([8, 18 + cy, 24, 52 + cy], 260, 100, fill=BOW_WOOD, width=3)
                draw.line([(16, 20 + cy), (16, 50 + cy)], fill=STRING_WHITE, width=1)
                draw.rectangle([14, 18 + cy, 18, 21 + cy], fill=BOW_TIP)
                draw.rectangle([14, 49 + cy, 18, 52 + cy], fill=BOW_TIP)

            elif row == 1:  # LEFT (Facing left)
                # Quiver on back (right side)
                draw.rectangle([41, 22 + cy, 47, 40 + cy], fill=QUIVER_BROWN, outline=OUTLINE)
                draw.polygon([(42, 14 + cy), (45, 14 + cy), (43, 22 + cy)], fill=FLETCHING_RED)
                draw.polygon([(45, 12 + cy), (48, 12 + cy), (46, 22 + cy)], fill=FLETCHING_WHITE)

                # Back Cloak
                draw.polygon([(36, 28 + cy), (44, 28 + cy), (48, 50 + cy), (38, 52 + cy)], fill=CLOAK_DARK)

                # Boots & Legs
                draw.rectangle([26 + leg_step, 45 + cy, 34 + leg_step, 56 + cy], fill=BOOT_BROWN, outline=OUTLINE)
                draw.rectangle([25 + leg_step, 44 + cy, 35 + leg_step, 47 + cy], fill=BOOT_CUFF)

                # Body & Harness
                draw.rectangle([25, 30 + cy, 39, 44 + cy], fill=LEATHER_BROWN, outline=OUTLINE)
                draw.line([(26, 32 + cy), (38, 42 + cy)], fill=LEATHER_DARK, width=2)

                # Arm facing left
                draw.rectangle([24, 32 + cy, 29, 41 + cy], fill=HOOD_GREEN, outline=OUTLINE)
                draw.ellipse([23, 40 + cy, 28, 44 + cy], fill=SKIN)

                # Hood Profile
                draw.polygon([(22, 16 + cy), (40, 16 + cy), (42, 31 + cy), (26, 31 + cy)], fill=HOOD_GREEN, outline=OUTLINE)
                draw.polygon([(21, 20 + cy), (33, 20 + cy), (31, 30 + cy), (23, 30 + cy)], fill=HOOD_SHADOW)
                draw.rectangle([22, 22 + cy, 31, 29 + cy], fill=SKIN)
                draw.rectangle([24, 25 + cy, 26, 28 + cy], fill=EYE_GREEN)

                # Composite Bow in front hand
                draw.arc([6, 18 + cy, 22, 52 + cy], 260, 100, fill=BOW_WOOD, width=3)
                draw.line([(14, 20 + cy), (14, 50 + cy)], fill=STRING_WHITE, width=1)
                draw.rectangle([12, 18 + cy, 16, 21 + cy], fill=BOW_TIP)
                draw.rectangle([12, 49 + cy, 16, 52 + cy], fill=BOW_TIP)

            elif row == 2:  # RIGHT (Facing right)
                # Quiver on back (left side)
                draw.rectangle([17, 22 + cy, 23, 40 + cy], fill=QUIVER_BROWN, outline=OUTLINE)
                draw.polygon([(18, 14 + cy), (21, 14 + cy), (19, 22 + cy)], fill=FLETCHING_RED)
                draw.polygon([(21, 12 + cy), (24, 12 + cy), (22, 22 + cy)], fill=FLETCHING_WHITE)

                # Back Cloak
                draw.polygon([(20, 28 + cy), (28, 28 + cy), (26, 52 + cy), (16, 50 + cy)], fill=CLOAK_DARK)

                # Boots & Legs
                draw.rectangle([30 + leg_step, 45 + cy, 38 + leg_step, 56 + cy], fill=BOOT_BROWN, outline=OUTLINE)
                draw.rectangle([29 + leg_step, 44 + cy, 39 + leg_step, 47 + cy], fill=BOOT_CUFF)

                # Body & Harness
                draw.rectangle([25, 30 + cy, 39, 44 + cy], fill=LEATHER_BROWN, outline=OUTLINE)
                draw.line([(38, 32 + cy), (26, 42 + cy)], fill=LEATHER_DARK, width=2)

                # Arm facing right
                draw.rectangle([35, 32 + cy, 40, 41 + cy], fill=HOOD_GREEN, outline=OUTLINE)
                draw.ellipse([36, 40 + cy, 41, 44 + cy], fill=SKIN)

                # Hood Profile
                draw.polygon([(24, 16 + cy), (42, 16 + cy), (38, 31 + cy), (22, 31 + cy)], fill=HOOD_GREEN, outline=OUTLINE)
                draw.polygon([(31, 20 + cy), (43, 20 + cy), (41, 30 + cy), (33, 30 + cy)], fill=HOOD_SHADOW)
                draw.rectangle([33, 22 + cy, 42, 29 + cy], fill=SKIN)
                draw.rectangle([38, 25 + cy, 40, 28 + cy], fill=EYE_GREEN)

                # Composite Bow in front hand
                draw.arc([42, 18 + cy, 58, 52 + cy], 80, 280, fill=BOW_WOOD, width=3)
                draw.line([(50, 20 + cy), (50, 50 + cy)], fill=STRING_WHITE, width=1)
                draw.rectangle([48, 18 + cy, 52, 21 + cy], fill=BOW_TIP)
                draw.rectangle([48, 49 + cy, 52, 52 + cy], fill=BOW_TIP)

            elif row == 3:  # UP (Facing back)
                # Boots & Legs
                draw.rectangle([23 + leg_step, 45 + cy, 29 + leg_step, 56 + cy], fill=BOOT_BROWN, outline=OUTLINE)
                draw.rectangle([35 - leg_step, 45 + cy, 41 - leg_step, 56 + cy], fill=BOOT_BROWN, outline=OUTLINE)
                draw.rectangle([22 + leg_step, 44 + cy, 30 + leg_step, 47 + cy], fill=BOOT_CUFF)
                draw.rectangle([34 - leg_step, 44 + cy, 42 - leg_step, 47 + cy], fill=BOOT_CUFF)

                # Flowing Cloak on Back
                draw.polygon([(18, 26 + cy), (46, 26 + cy), (50, 51 + cy), (14, 51 + cy)], fill=HOOD_GREEN, outline=OUTLINE)
                draw.polygon([(22, 32 + cy), (42, 32 + cy), (45, 50 + cy), (19, 50 + cy)], fill=HOOD_SHADOW)

                # Diagonal Quiver across back cloak
                draw.polygon([(22, 22 + cy), (28, 20 + cy), (42, 42 + cy), (36, 44 + cy)], fill=QUIVER_BROWN, outline=OUTLINE)
                # Arrow Fletchings sticking out top of quiver
                draw.polygon([(18, 13 + cy), (22, 13 + cy), (23, 21 + cy)], fill=FLETCHING_RED)
                draw.polygon([(22, 10 + cy), (26, 10 + cy), (25, 20 + cy)], fill=FLETCHING_WHITE)
                draw.polygon([(26, 12 + cy), (30, 12 + cy), (27, 21 + cy)], fill=FLETCHING_RED)

                # Back of Hood
                draw.polygon([(20, 14 + cy), (44, 14 + cy), (42, 30 + cy), (22, 30 + cy)], fill=HOOD_GREEN, outline=OUTLINE)
                draw.polygon([(24, 17 + cy), (40, 17 + cy), (38, 28 + cy), (26, 28 + cy)], fill=HOOD_HIGHLIGHT)

                # Composite Bow on side
                draw.arc([6, 18 + cy, 22, 52 + cy], 260, 100, fill=BOW_WOOD, width=3)
                draw.line([(14, 20 + cy), (14, 50 + cy)], fill=STRING_WHITE, width=1)

            sheet.paste(frame, (x_off, y_off))

    return sheet

def main():
    dirs = ensure_dirs()
    ranger_img = create_hero_ranger_sprite()
    for d in dirs:
        out_path = os.path.join(d, "hero_ranger.png")
        ranger_img.save(out_path, "PNG")
        print(f"Saved Hero Ranger Sprite: {out_path} ({ranger_img.size[0]}x{ranger_img.size[1]} {ranger_img.mode})")

if __name__ == "__main__":
    main()
