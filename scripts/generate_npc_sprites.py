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

def save_npc_sprite(img, name, dirs):
    for d in dirs:
        path = os.path.join(d, name)
        img.save(path, "PNG")
        print(f"Saved NPC Sprite: {path} ({img.size[0]}x{img.size[1]} {img.mode})")

def create_kafra_sprite():
    """
    Kafra Service Staff: Blue uniform dress, white apron, white headband/ribbon, blonde hair.
    Sheet size: 256x256 RGBA (4 cols x 4 rows of 64x64 frames).
    Rows (dir): 0=Down, 1=Left, 2=Right, 3=Up
    Cols (frame): 0=Idle1, 1=Idle2, 2=Walk, 3=Greet/Wave
    """
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    
    # Palette
    SKIN = (255, 224, 189, 255)
    SKIN_SHADOW = (230, 185, 150, 255)
    HAIR = (255, 215, 0, 255)         # Blonde hair
    HAIR_SHADOW = (218, 165, 32, 255)
    HAIR_LIGHT = (255, 240, 150, 255)
    UNIFORM_BLUE = (30, 90, 180, 255)
    UNIFORM_DARK = (15, 55, 120, 255)
    UNIFORM_LIGHT = (60, 130, 220, 255)
    APRON_WHITE = (245, 248, 255, 255)
    APRON_SHADOW = (200, 210, 225, 255)
    EYE_BLUE = (20, 120, 220, 255)
    RIBBON_RED = (220, 40, 60, 255)
    OUTLINE = (20, 20, 35, 255)
    BOOT_BROWN = (90, 50, 30, 255)

    for row in range(4):
        for col in range(4):
            x_off = col * 64
            y_off = row * 64
            frame_img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame_img)

            # Center base at (32, 54)
            bob = 1 if (col == 1 or col == 3) else 0
            hand_wave = (col == 3)
            leg_step = 1 if col == 2 else 0

            cy = 32 + bob

            if row == 0:  # DOWN (Facing front)
                # Ground shadow
                draw.ellipse([22, 54, 42, 60], fill=(0, 0, 0, 80))

                # Boots
                draw.rectangle([25, 50, 29, 56], fill=BOOT_BROWN, outline=OUTLINE)
                draw.rectangle([35, 50, 39, 56], fill=BOOT_BROWN, outline=OUTLINE)

                # Blue Dress Skirt
                draw.polygon([(22, 40), (42, 40), (46, 51), (18, 51)], fill=UNIFORM_BLUE, outline=OUTLINE)
                draw.line([(24, 51), (40, 51)], fill=UNIFORM_LIGHT, width=1)

                # White Apron Over Skirt
                draw.polygon([(26, 38), (38, 38), (40, 49), (24, 49)], fill=APRON_WHITE, outline=OUTLINE)
                draw.line([(28, 41), (28, 49)], fill=APRON_SHADOW, width=1)
                draw.line([(36, 41), (36, 49)], fill=APRON_SHADOW, width=1)

                # Torso / Blue Uniform Top
                draw.rectangle([25, 28, 39, 38], fill=UNIFORM_BLUE, outline=OUTLINE)

                # White Apron Bib & Collar
                draw.polygon([(27, 28), (37, 28), (35, 36), (29, 36)], fill=APRON_WHITE)
                draw.polygon([(28, 26), (36, 26), (32, 30)], fill=APRON_WHITE, outline=OUTLINE)

                # Red Bow Tie at Chest
                draw.ellipse([30, 28, 34, 32], fill=RIBBON_RED, outline=OUTLINE)
                draw.polygon([(27, 30), (30, 30), (28, 33)], fill=RIBBON_RED)
                draw.polygon([(34, 30), (37, 30), (36, 33)], fill=RIBBON_RED)

                # Arms & Hands
                if hand_wave:
                    # Left arm resting, Right arm waving
                    draw.rectangle([20, 29, 24, 37], fill=UNIFORM_BLUE, outline=OUTLINE)
                    draw.ellipse([19, 36, 24, 40], fill=SKIN)
                    # Waving arm
                    draw.line([(40, 30), (48, 22)], fill=UNIFORM_BLUE, width=4)
                    draw.ellipse([46, 17, 52, 23], fill=SKIN, outline=OUTLINE)
                else:
                    # Both hands clasped gracefully in front of apron
                    draw.line([(21, 30), (27, 36)], fill=UNIFORM_BLUE, width=3)
                    draw.line([(43, 30), (37, 36)], fill=UNIFORM_BLUE, width=3)
                    draw.ellipse([29, 34, 35, 39], fill=SKIN, outline=OUTLINE)

                # Head & Face
                draw.ellipse([23, 13 + bob, 41, 29 + bob], fill=SKIN, outline=OUTLINE)

                # Eyes
                draw.rectangle([27, 21 + bob, 29, 24 + bob], fill=EYE_BLUE)
                draw.rectangle([35, 21 + bob, 37, 24 + bob], fill=EYE_BLUE)
                draw.point((28, 21 + bob), fill=(255, 255, 255, 255))
                draw.point((36, 21 + bob), fill=(255, 255, 255, 255))

                # Smile & Blush
                draw.line([(30, 26 + bob), (34, 26 + bob)], fill=(200, 90, 90, 255), width=1)
                draw.rectangle([25, 23 + bob, 27, 25 + bob], fill=(255, 170, 170, 180))
                draw.rectangle([37, 23 + bob, 39, 25 + bob], fill=(255, 170, 170, 180))

                # Blonde Hair (Bangs & Long Side Locks)
                draw.polygon([(23, 15 + bob), (41, 15 + bob), (38, 9 + bob), (26, 9 + bob)], fill=HAIR, outline=OUTLINE)
                draw.polygon([(24, 15 + bob), (30, 21 + bob), (28, 15 + bob)], fill=HAIR)
                draw.polygon([(34, 15 + bob), (40, 21 + bob), (36, 15 + bob)], fill=HAIR)
                draw.polygon([(30, 15 + bob), (34, 19 + bob), (32, 15 + bob)], fill=HAIR_LIGHT)
                draw.rectangle([20, 17 + bob, 24, 33 + bob], fill=HAIR, outline=OUTLINE)
                draw.rectangle([40, 17 + bob, 44, 33 + bob], fill=HAIR, outline=OUTLINE)

                # White Maid Headband / Cap with Red Ribbon
                draw.rectangle([24, 8 + bob, 40, 13 + bob], fill=APRON_WHITE, outline=OUTLINE)
                draw.ellipse([18, 7 + bob, 24, 13 + bob], fill=APRON_WHITE, outline=OUTLINE)
                draw.ellipse([40, 7 + bob, 46, 13 + bob], fill=APRON_WHITE, outline=OUTLINE)
                draw.ellipse([30, 6 + bob, 34, 10 + bob], fill=RIBBON_RED)

            elif row == 1:  # LEFT (Facing Left)
                draw.ellipse([22, 54, 42, 60], fill=(0, 0, 0, 80))
                bx = 27 - leg_step * 3
                draw.rectangle([bx, 50, bx + 5, 56], fill=BOOT_BROWN, outline=OUTLINE)

                draw.polygon([(24, 40), (38, 40), (42, 51), (20, 51)], fill=UNIFORM_BLUE, outline=OUTLINE)
                draw.polygon([(22, 40), (32, 40), (30, 50), (18, 50)], fill=APRON_WHITE, outline=OUTLINE)
                draw.ellipse([36, 38, 42, 44], fill=APRON_WHITE, outline=OUTLINE)

                draw.rectangle([24, 28, 36, 39], fill=UNIFORM_BLUE, outline=OUTLINE)
                draw.rectangle([22, 28, 28, 38], fill=APRON_WHITE)

                if hand_wave:
                    draw.line([(30, 29), (20, 22)], fill=UNIFORM_BLUE, width=4)
                    draw.ellipse([16, 18, 22, 24], fill=SKIN, outline=OUTLINE)
                else:
                    draw.line([(30, 30), (24, 37)], fill=UNIFORM_BLUE, width=3)
                    draw.ellipse([22, 36, 27, 40], fill=SKIN)

                draw.ellipse([23, 13 + bob, 39, 29 + bob], fill=SKIN, outline=OUTLINE)
                draw.rectangle([25, 21 + bob, 27, 24 + bob], fill=EYE_BLUE)

                draw.rectangle([34, 15 + bob, 42, 34 + bob], fill=HAIR, outline=OUTLINE)
                draw.polygon([(23, 15 + bob), (35, 15 + bob), (28, 22 + bob)], fill=HAIR)
                draw.rectangle([24, 8 + bob, 38, 13 + bob], fill=APRON_WHITE, outline=OUTLINE)
                draw.ellipse([36, 7 + bob, 42, 13 + bob], fill=APRON_WHITE, outline=OUTLINE)

            elif row == 2:  # RIGHT (Facing Right)
                draw.ellipse([22, 54, 42, 60], fill=(0, 0, 0, 80))
                bx = 32 + leg_step * 3
                draw.rectangle([bx, 50, bx + 5, 56], fill=BOOT_BROWN, outline=OUTLINE)

                draw.polygon([(26, 40), (40, 40), (44, 51), (22, 51)], fill=UNIFORM_BLUE, outline=OUTLINE)
                draw.polygon([(32, 40), (42, 40), (46, 50), (34, 50)], fill=APRON_WHITE, outline=OUTLINE)
                draw.ellipse([22, 38, 28, 44], fill=APRON_WHITE, outline=OUTLINE)

                draw.rectangle([28, 28, 40, 39], fill=UNIFORM_BLUE, outline=OUTLINE)
                draw.rectangle([36, 28, 42, 38], fill=APRON_WHITE)

                if hand_wave:
                    draw.line([(34, 29), (44, 22)], fill=UNIFORM_BLUE, width=4)
                    draw.ellipse([42, 18, 48, 24], fill=SKIN, outline=OUTLINE)
                else:
                    draw.line([(34, 30), (40, 37)], fill=UNIFORM_BLUE, width=3)
                    draw.ellipse([37, 36, 42, 40], fill=SKIN)

                draw.ellipse([25, 13 + bob, 41, 29 + bob], fill=SKIN, outline=OUTLINE)
                draw.rectangle([37, 21 + bob, 39, 24 + bob], fill=EYE_BLUE)

                draw.rectangle([22, 15 + bob, 30, 34 + bob], fill=HAIR, outline=OUTLINE)
                draw.polygon([(29, 15 + bob), (41, 15 + bob), (36, 22 + bob)], fill=HAIR)
                draw.rectangle([26, 8 + bob, 40, 13 + bob], fill=APRON_WHITE, outline=OUTLINE)
                draw.ellipse([22, 7 + bob, 28, 13 + bob], fill=APRON_WHITE, outline=OUTLINE)

            elif row == 3:  # UP (Facing Back)
                draw.ellipse([22, 54, 42, 60], fill=(0, 0, 0, 80))
                draw.rectangle([25, 50, 29, 56], fill=BOOT_BROWN, outline=OUTLINE)
                draw.rectangle([35, 50, 39, 56], fill=BOOT_BROWN, outline=OUTLINE)

                draw.polygon([(22, 40), (42, 40), (46, 51), (18, 51)], fill=UNIFORM_BLUE, outline=OUTLINE)
                draw.ellipse([28, 37, 36, 43], fill=APRON_WHITE, outline=OUTLINE)
                draw.polygon([(27, 40), (22, 48), (28, 48)], fill=APRON_WHITE, outline=OUTLINE)
                draw.polygon([(37, 40), (42, 48), (36, 48)], fill=APRON_WHITE, outline=OUTLINE)

                draw.rectangle([25, 28, 39, 38], fill=UNIFORM_BLUE, outline=OUTLINE)
                draw.line([(21, 30), (25, 37)], fill=UNIFORM_BLUE, width=3)
                draw.line([(43, 30), (39, 37)], fill=UNIFORM_BLUE, width=3)

                draw.rectangle([22, 12 + bob, 42, 32 + bob], fill=HAIR, outline=OUTLINE)
                draw.rectangle([26, 10 + bob, 38, 35 + bob], fill=HAIR_SHADOW)
                draw.line([(28, 14 + bob), (28, 32 + bob)], fill=HAIR_LIGHT, width=2)
                draw.line([(36, 14 + bob), (36, 32 + bob)], fill=HAIR_LIGHT, width=2)

                draw.rectangle([22, 7 + bob, 42, 12 + bob], fill=APRON_WHITE, outline=OUTLINE)
                draw.ellipse([29, 5 + bob, 35, 9 + bob], fill=RIBBON_RED)

            sheet.paste(frame_img, (x_off, y_off))
    return sheet

def create_blacksmith_sprite():
    """
    Muscular Blacksmith: Leather apron, red/brown vest, hammer, spiky hair, broad posture.
    Sheet size: 256x256 RGBA (4 cols x 4 rows of 64x64 frames).
    """
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))

    SKIN = (240, 185, 145, 255)
    HAIR = (180, 60, 30, 255)
    HAIR_LIGHT = (220, 90, 50, 255)
    SHIRT_RED = (160, 35, 35, 255)
    LEATHER_BROWN = (115, 65, 30, 255)
    LEATHER_DARK = (80, 40, 15, 255)
    PANTS_GREY = (55, 60, 70, 255)
    BOOT_DARK = (40, 35, 30, 255)
    HAMMER_STEEL = (170, 180, 195, 255)
    HAMMER_HANDLE = (110, 75, 45, 255)
    OUTLINE = (20, 20, 30, 255)

    for row in range(4):
        for col in range(4):
            x_off = col * 64
            y_off = row * 64
            frame_img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame_img)

            bob = 1 if (col == 1 or col == 3) else 0
            action = (col == 3)
            leg_step = 1 if col == 2 else 0

            if row == 0:  # DOWN
                draw.ellipse([18, 54, 46, 62], fill=(0, 0, 0, 90))
                draw.rectangle([22, 49, 29, 57], fill=BOOT_DARK, outline=OUTLINE)
                draw.rectangle([35, 49, 42, 57], fill=BOOT_DARK, outline=OUTLINE)

                draw.rectangle([23, 42, 41, 51], fill=PANTS_GREY, outline=OUTLINE)
                draw.polygon([(20, 32), (44, 32), (42, 48), (22, 48)], fill=LEATHER_BROWN, outline=OUTLINE)
                draw.rectangle([25, 26, 39, 32], fill=LEATHER_BROWN, outline=OUTLINE)

                draw.rectangle([21, 38, 43, 41], fill=LEATHER_DARK)
                draw.rectangle([29, 37, 35, 42], fill=(220, 180, 50, 255), outline=OUTLINE)

                draw.polygon([(18, 24), (46, 24), (43, 34), (21, 34)], fill=SHIRT_RED, outline=OUTLINE)

                draw.rectangle([14, 25, 20, 37], fill=SKIN, outline=OUTLINE)
                draw.rectangle([13, 35, 20, 42], fill=LEATHER_DARK, outline=OUTLINE)

                if action:
                    draw.line([(44, 26), (52, 14)], fill=SKIN, width=5)
                    draw.ellipse([49, 10, 55, 16], fill=LEATHER_DARK, outline=OUTLINE)
                    draw.line([(44, 18), (56, 6)], fill=HAMMER_HANDLE, width=4)
                    draw.rectangle([48, 3, 62, 13], fill=HAMMER_STEEL, outline=OUTLINE)
                else:
                    draw.rectangle([44, 25, 50, 37], fill=SKIN, outline=OUTLINE)
                    draw.rectangle([44, 35, 51, 42], fill=LEATHER_DARK, outline=OUTLINE)
                    draw.line([(48, 38), (48, 54)], fill=HAMMER_HANDLE, width=3)
                    draw.rectangle([43, 48, 55, 56], fill=HAMMER_STEEL, outline=OUTLINE)

                draw.ellipse([22, 11 + bob, 42, 27 + bob], fill=SKIN, outline=OUTLINE)
                draw.polygon([(24, 21 + bob), (40, 21 + bob), (36, 28 + bob), (28, 28 + bob)], fill=(120, 45, 25, 255))
                draw.line([(26, 17 + bob), (30, 18 + bob)], fill=OUTLINE, width=2)
                draw.line([(38, 17 + bob), (34, 18 + bob)], fill=OUTLINE, width=2)
                draw.point((28, 19 + bob), fill=OUTLINE)
                draw.point((36, 19 + bob), fill=OUTLINE)

                draw.polygon([(20, 13 + bob), (44, 13 + bob), (40, 5 + bob), (24, 5 + bob)], fill=HAIR, outline=OUTLINE)
                draw.polygon([(22, 8 + bob), (28, 2 + bob), (32, 8 + bob)], fill=HAIR_LIGHT)
                draw.polygon([(32, 8 + bob), (38, 2 + bob), (42, 8 + bob)], fill=HAIR)

            elif row == 1:  # LEFT
                draw.ellipse([18, 54, 46, 62], fill=(0, 0, 0, 90))
                bx = 25 - leg_step * 3
                draw.rectangle([bx, 49, bx + 7, 57], fill=BOOT_DARK, outline=OUTLINE)
                draw.rectangle([24, 42, 38, 51], fill=PANTS_GREY, outline=OUTLINE)

                draw.polygon([(20, 32), (36, 32), (34, 48), (22, 48)], fill=LEATHER_BROWN, outline=OUTLINE)
                draw.polygon([(18, 24), (38, 24), (36, 34), (20, 34)], fill=SHIRT_RED, outline=OUTLINE)

                if action:
                    draw.line([(28, 26), (16, 14)], fill=SKIN, width=5)
                    draw.line([(20, 18), (8, 6)], fill=HAMMER_HANDLE, width=4)
                    draw.rectangle([2, 3, 16, 13], fill=HAMMER_STEEL, outline=OUTLINE)
                else:
                    draw.rectangle([20, 26, 28, 38], fill=SKIN, outline=OUTLINE)
                    draw.line([(24, 36), (24, 52)], fill=HAMMER_HANDLE, width=3)
                    draw.rectangle([18, 46, 30, 54], fill=HAMMER_STEEL, outline=OUTLINE)

                draw.ellipse([22, 11 + bob, 38, 27 + bob], fill=SKIN, outline=OUTLINE)
                draw.polygon([(22, 20 + bob), (32, 20 + bob), (28, 28 + bob)], fill=(120, 45, 25, 255))
                draw.polygon([(18, 13 + bob), (38, 13 + bob), (30, 5 + bob)], fill=HAIR, outline=OUTLINE)

            elif row == 2:  # RIGHT
                draw.ellipse([18, 54, 46, 62], fill=(0, 0, 0, 90))
                bx = 32 + leg_step * 3
                draw.rectangle([bx, 49, bx + 7, 57], fill=BOOT_DARK, outline=OUTLINE)
                draw.rectangle([26, 42, 40, 51], fill=PANTS_GREY, outline=OUTLINE)

                draw.polygon([(28, 32), (44, 32), (42, 48), (30, 48)], fill=LEATHER_BROWN, outline=OUTLINE)
                draw.polygon([(26, 24), (46, 24), (44, 34), (28, 34)], fill=SHIRT_RED, outline=OUTLINE)

                if action:
                    draw.line([(36, 26), (48, 14)], fill=SKIN, width=5)
                    draw.line([(44, 18), (56, 6)], fill=HAMMER_HANDLE, width=4)
                    draw.rectangle([48, 3, 62, 13], fill=HAMMER_STEEL, outline=OUTLINE)
                else:
                    draw.rectangle([36, 26, 44, 38], fill=SKIN, outline=OUTLINE)
                    draw.line([(40, 36), (40, 52)], fill=HAMMER_HANDLE, width=3)
                    draw.rectangle([34, 46, 46, 54], fill=HAMMER_STEEL, outline=OUTLINE)

                draw.ellipse([26, 11 + bob, 42, 27 + bob], fill=SKIN, outline=OUTLINE)
                draw.polygon([(32, 20 + bob), (42, 20 + bob), (36, 28 + bob)], fill=(120, 45, 25, 255))
                draw.polygon([(26, 13 + bob), (46, 13 + bob), (34, 5 + bob)], fill=HAIR, outline=OUTLINE)

            elif row == 3:  # UP
                draw.ellipse([18, 54, 46, 62], fill=(0, 0, 0, 90))
                draw.rectangle([22, 49, 29, 57], fill=BOOT_DARK, outline=OUTLINE)
                draw.rectangle([35, 49, 42, 57], fill=BOOT_DARK, outline=OUTLINE)

                draw.rectangle([23, 42, 41, 51], fill=PANTS_GREY, outline=OUTLINE)
                draw.polygon([(20, 24), (44, 24), (42, 46), (22, 46)], fill=SHIRT_RED, outline=OUTLINE)

                draw.line([(24, 24), (40, 42)], fill=LEATHER_BROWN, width=3)
                draw.line([(40, 24), (24, 42)], fill=LEATHER_BROWN, width=3)

                draw.rectangle([14, 25, 20, 37], fill=SKIN, outline=OUTLINE)
                draw.rectangle([44, 25, 50, 37], fill=SKIN, outline=OUTLINE)

                draw.rectangle([20, 7 + bob, 44, 25 + bob], fill=HAIR, outline=OUTLINE)
                draw.polygon([(20, 7 + bob), (28, 2 + bob), (36, 7 + bob)], fill=HAIR_LIGHT)

            sheet.paste(frame_img, (x_off, y_off))
    return sheet

def create_merchant_sprite():
    """
    Item Shop Merchant: Large merchant backpack/frame on rear, green/teal vest, yellow tunic, merchant cap.
    Sheet size: 256x256 RGBA (4 cols x 4 rows of 64x64 frames).
    """
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))

    SKIN = (255, 218, 180, 255)
    VEST_TEAL = (30, 140, 120, 255)
    VEST_DARK = (15, 85, 75, 255)
    TUNIC_YELLOW = (240, 195, 60, 255)
    PANTS_BROWN = (85, 60, 40, 255)
    BOOT_LEATHER = (120, 75, 40, 255)
    PACK_WOOD = (160, 105, 55, 255)
    PACK_CANVAS = (210, 185, 140, 255)
    PACK_ROPE = (240, 220, 170, 255)
    POTION_RED = (235, 45, 50, 255)
    CAP_TEAL = (25, 125, 110, 255)
    OUTLINE = (20, 20, 30, 255)

    for row in range(4):
        for col in range(4):
            x_off = col * 64
            y_off = row * 64
            frame_img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame_img)

            bob = 1 if (col == 1 or col == 3) else 0
            action = (col == 3)
            leg_step = 1 if col == 2 else 0

            if row == 0:  # DOWN
                draw.ellipse([16, 54, 48, 62], fill=(0, 0, 0, 90))

                draw.rectangle([13, 20, 21, 44], fill=PACK_CANVAS, outline=OUTLINE)
                draw.rectangle([43, 20, 51, 44], fill=PACK_CANVAS, outline=OUTLINE)
                draw.line([(11, 18), (53, 18)], fill=PACK_WOOD, width=3)

                draw.rectangle([23, 49, 29, 56], fill=BOOT_LEATHER, outline=OUTLINE)
                draw.rectangle([35, 49, 41, 56], fill=BOOT_LEATHER, outline=OUTLINE)

                draw.rectangle([23, 41, 41, 50], fill=PANTS_BROWN, outline=OUTLINE)
                draw.polygon([(21, 30), (43, 30), (45, 43), (19, 43)], fill=TUNIC_YELLOW, outline=OUTLINE)

                draw.rectangle([20, 28, 27, 41], fill=VEST_TEAL, outline=OUTLINE)
                draw.rectangle([37, 28, 44, 41], fill=VEST_TEAL, outline=OUTLINE)

                draw.rectangle([28, 39, 36, 44], fill=PACK_WOOD, outline=OUTLINE)
                draw.ellipse([20, 39, 25, 44], fill=POTION_RED, outline=OUTLINE)

                if action:
                    draw.line([(19, 30), (14, 38)], fill=TUNIC_YELLOW, width=4)
                    draw.line([(44, 30), (50, 22)], fill=TUNIC_YELLOW, width=4)
                    draw.ellipse([48, 16, 55, 23], fill=SKIN, outline=OUTLINE)
                    draw.polygon([(49, 12), (54, 12), (56, 17), (47, 17)], fill=POTION_RED, outline=OUTLINE)
                else:
                    draw.rectangle([15, 30, 21, 40], fill=TUNIC_YELLOW, outline=OUTLINE)
                    draw.rectangle([43, 30, 49, 40], fill=TUNIC_YELLOW, outline=OUTLINE)

                draw.ellipse([23, 12 + bob, 41, 28 + bob], fill=SKIN, outline=OUTLINE)
                draw.point((27, 20 + bob), fill=OUTLINE)
                draw.point((37, 20 + bob), fill=OUTLINE)
                draw.line([(30, 24 + bob), (34, 24 + bob)], fill=(180, 80, 60, 255), width=1)

                draw.polygon([(21, 14 + bob), (43, 14 + bob), (40, 7 + bob), (24, 7 + bob)], fill=CAP_TEAL, outline=OUTLINE)
                draw.ellipse([20, 13 + bob, 44, 17 + bob], fill=VEST_DARK)
                draw.polygon([(38, 5 + bob), (43, 10 + bob), (40, 13 + bob)], fill=TUNIC_YELLOW)

            elif row == 1:  # LEFT
                draw.ellipse([16, 54, 48, 62], fill=(0, 0, 0, 90))
                bx = 27 - leg_step * 3
                draw.rectangle([bx, 49, bx + 6, 56], fill=BOOT_LEATHER, outline=OUTLINE)
                draw.rectangle([24, 41, 38, 50], fill=PANTS_BROWN, outline=OUTLINE)

                draw.rectangle([34, 16, 54, 46], fill=PACK_CANVAS, outline=OUTLINE)
                draw.line([(32, 14), (56, 14)], fill=PACK_WOOD, width=3)
                draw.line([(32, 46), (56, 46)], fill=PACK_WOOD, width=3)
                draw.line([(34, 28), (54, 28)], fill=PACK_ROPE, width=2)
                draw.ellipse([34, 8, 52, 15], fill=TUNIC_YELLOW, outline=OUTLINE)

                draw.polygon([(20, 30), (36, 30), (34, 43), (18, 43)], fill=TUNIC_YELLOW, outline=OUTLINE)
                draw.rectangle([20, 28, 28, 41], fill=VEST_TEAL, outline=OUTLINE)

                if action:
                    draw.line([(22, 30), (14, 22)], fill=TUNIC_YELLOW, width=4)
                    draw.polygon([(11, 16), (16, 16), (18, 21), (9, 21)], fill=POTION_RED, outline=OUTLINE)
                else:
                    draw.rectangle([18, 30, 24, 40], fill=TUNIC_YELLOW, outline=OUTLINE)

                draw.ellipse([21, 12 + bob, 37, 28 + bob], fill=SKIN, outline=OUTLINE)
                draw.polygon([(19, 14 + bob), (37, 14 + bob), (34, 7 + bob)], fill=CAP_TEAL, outline=OUTLINE)
                draw.ellipse([17, 13 + bob, 38, 17 + bob], fill=VEST_DARK)

            elif row == 2:  # RIGHT
                draw.ellipse([16, 54, 48, 62], fill=(0, 0, 0, 90))
                bx = 31 + leg_step * 3
                draw.rectangle([bx, 49, bx + 6, 56], fill=BOOT_LEATHER, outline=OUTLINE)
                draw.rectangle([26, 41, 40, 50], fill=PANTS_BROWN, outline=OUTLINE)

                draw.rectangle([10, 16, 30, 46], fill=PACK_CANVAS, outline=OUTLINE)
                draw.line([(8, 14), (32, 14)], fill=PACK_WOOD, width=3)
                draw.line([(8, 46), (32, 46)], fill=PACK_WOOD, width=3)
                draw.line([(10, 28), (30, 28)], fill=PACK_ROPE, width=2)
                draw.ellipse([12, 8, 30, 15], fill=TUNIC_YELLOW, outline=OUTLINE)

                draw.polygon([(28, 30), (44, 30), (46, 43), (30, 43)], fill=TUNIC_YELLOW, outline=OUTLINE)
                draw.rectangle([36, 28, 44, 41], fill=VEST_TEAL, outline=OUTLINE)

                if action:
                    draw.line([(42, 30), (50, 22)], fill=TUNIC_YELLOW, width=4)
                    draw.polygon([(48, 16), (53, 16), (55, 21), (46, 21)], fill=POTION_RED, outline=OUTLINE)
                else:
                    draw.rectangle([40, 30, 46, 40], fill=TUNIC_YELLOW, outline=OUTLINE)

                draw.ellipse([27, 12 + bob, 43, 28 + bob], fill=SKIN, outline=OUTLINE)
                draw.polygon([(27, 14 + bob), (45, 14 + bob), (42, 7 + bob)], fill=CAP_TEAL, outline=OUTLINE)
                draw.ellipse([25, 13 + bob, 47, 17 + bob], fill=VEST_DARK)

            elif row == 3:  # UP
                draw.ellipse([16, 54, 48, 62], fill=(0, 0, 0, 90))
                draw.rectangle([23, 49, 29, 56], fill=BOOT_LEATHER, outline=OUTLINE)
                draw.rectangle([35, 49, 41, 56], fill=BOOT_LEATHER, outline=OUTLINE)

                draw.rectangle([14, 16, 50, 48], fill=PACK_CANVAS, outline=OUTLINE)
                draw.line([(12, 14), (52, 14)], fill=PACK_WOOD, width=4)
                draw.line([(12, 48), (52, 48)], fill=PACK_WOOD, width=4)
                draw.line([(14, 14), (14, 48)], fill=PACK_WOOD, width=3)
                draw.line([(50, 14), (50, 48)], fill=PACK_WOOD, width=3)
                draw.line([(14, 30), (50, 30)], fill=PACK_ROPE, width=3)
                draw.rectangle([16, 7, 48, 14], fill=TUNIC_YELLOW, outline=OUTLINE)

                draw.polygon([(21, 10 + bob), (43, 10 + bob), (40, 3 + bob), (24, 3 + bob)], fill=CAP_TEAL, outline=OUTLINE)

            sheet.paste(frame_img, (x_off, y_off))
    return sheet

def create_elder_sprite():
    """
    Wise Quest Guide Elder: Deep purple/blue robe with gold trim, long white beard & hair, wooden staff with crystal.
    Sheet size: 256x256 RGBA (4 cols x 4 rows of 64x64 frames).
    """
    sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))

    SKIN = (245, 205, 175, 255)
    HAIR_WHITE = (245, 245, 250, 255)
    HAIR_SHADOW = (200, 205, 220, 255)
    ROBE_PURPLE = (75, 40, 120, 255)
    ROBE_LIGHT = (110, 65, 170, 255)
    TRIM_GOLD = (235, 190, 40, 255)
    STAFF_WOOD = (100, 60, 30, 255)
    GEM_BLUE = (80, 220, 255, 255)
    OUTLINE = (20, 20, 30, 255)

    for row in range(4):
        for col in range(4):
            x_off = col * 64
            y_off = row * 64
            frame_img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame_img)

            bob = 1 if (col == 1 or col == 3) else 0
            action = (col == 3)

            if row == 0:  # DOWN
                draw.ellipse([18, 54, 46, 62], fill=(0, 0, 0, 90))

                draw.polygon([(20, 32), (44, 32), (48, 56), (16, 56)], fill=ROBE_PURPLE, outline=OUTLINE)
                draw.line([(32, 32), (32, 56)], fill=TRIM_GOLD, width=2)
                draw.line([(18, 54), (46, 54)], fill=TRIM_GOLD, width=2)

                draw.rectangle([21, 24, 43, 33], fill=ROBE_PURPLE, outline=OUTLINE)
                draw.polygon([(21, 24), (32, 32), (43, 24)], fill=ROBE_LIGHT)

                draw.line([(20, 26), (15, 38)], fill=ROBE_PURPLE, width=4)
                draw.ellipse([13, 37, 18, 41], fill=SKIN)

                draw.line([(44, 26), (48, 36)], fill=ROBE_PURPLE, width=4)
                draw.ellipse([46, 35, 51, 39], fill=SKIN)

                staff_y_offset = -4 if action else 0
                draw.line([(50, 10 + staff_y_offset), (50, 58)], fill=STAFF_WOOD, width=3)
                draw.polygon([(50, 4 + staff_y_offset), (55, 9 + staff_y_offset), (50, 14 + staff_y_offset), (45, 9 + staff_y_offset)], fill=GEM_BLUE, outline=OUTLINE)
                if action:
                    draw.ellipse([42, 2, 58, 18], fill=(120, 230, 255, 100))
                    draw.point((43, 4), fill=(255, 255, 255, 255))
                    draw.point((57, 5), fill=(255, 255, 255, 255))
                    draw.point((44, 16), fill=(255, 255, 255, 255))

                draw.ellipse([24, 11 + bob, 40, 26 + bob], fill=SKIN, outline=OUTLINE)
                draw.point((28, 18 + bob), fill=OUTLINE)
                draw.point((36, 18 + bob), fill=OUTLINE)

                draw.polygon([(23, 20 + bob), (41, 20 + bob), (38, 40 + bob), (26, 40 + bob)], fill=HAIR_WHITE, outline=OUTLINE)
                draw.line([(28, 22 + bob), (28, 38 + bob)], fill=HAIR_SHADOW, width=1)
                draw.line([(36, 22 + bob), (36, 38 + bob)], fill=HAIR_SHADOW, width=1)
                draw.ellipse([26, 19 + bob, 38, 24 + bob], fill=HAIR_WHITE)

                draw.polygon([(20, 12 + bob), (44, 12 + bob), (38, 4 + bob), (26, 4 + bob)], fill=ROBE_PURPLE, outline=OUTLINE)
                draw.line([(22, 12 + bob), (42, 12 + bob)], fill=TRIM_GOLD, width=2)
                draw.rectangle([19, 14 + bob, 23, 34 + bob], fill=HAIR_WHITE)
                draw.rectangle([41, 14 + bob, 45, 34 + bob], fill=HAIR_WHITE)

            elif row == 1:  # LEFT
                draw.ellipse([18, 54, 46, 62], fill=(0, 0, 0, 90))
                draw.polygon([(22, 32), (38, 32), (42, 56), (18, 56)], fill=ROBE_PURPLE, outline=OUTLINE)
                draw.line([(20, 54), (40, 54)], fill=TRIM_GOLD, width=2)

                draw.rectangle([22, 24, 36, 33], fill=ROBE_PURPLE, outline=OUTLINE)

                staff_y_offset = -4 if action else 0
                draw.line([(16, 10 + staff_y_offset), (16, 58)], fill=STAFF_WOOD, width=3)
                draw.polygon([(16, 4 + staff_y_offset), (21, 9 + staff_y_offset), (16, 14 + staff_y_offset), (11, 9 + staff_y_offset)], fill=GEM_BLUE, outline=OUTLINE)
                draw.ellipse([14, 30, 20, 36], fill=SKIN)

                draw.ellipse([23, 11 + bob, 37, 26 + bob], fill=SKIN, outline=OUTLINE)
                draw.polygon([(21, 20 + bob), (33, 20 + bob), (28, 40 + bob)], fill=HAIR_WHITE, outline=OUTLINE)

                draw.polygon([(20, 12 + bob), (38, 12 + bob), (30, 4 + bob)], fill=ROBE_PURPLE, outline=OUTLINE)
                draw.line([(21, 12 + bob), (37, 12 + bob)], fill=TRIM_GOLD, width=2)
                draw.rectangle([34, 14 + bob, 40, 34 + bob], fill=HAIR_WHITE)

            elif row == 2:  # RIGHT
                draw.ellipse([18, 54, 46, 62], fill=(0, 0, 0, 90))
                draw.polygon([(26, 32), (42, 32), (46, 56), (22, 56)], fill=ROBE_PURPLE, outline=OUTLINE)
                draw.line([(24, 54), (44, 54)], fill=TRIM_GOLD, width=2)

                draw.rectangle([28, 24, 42, 33], fill=ROBE_PURPLE, outline=OUTLINE)

                staff_y_offset = -4 if action else 0
                draw.line([(48, 10 + staff_y_offset), (48, 58)], fill=STAFF_WOOD, width=3)
                draw.polygon([(48, 4 + staff_y_offset), (53, 9 + staff_y_offset), (48, 14 + staff_y_offset), (43, 9 + staff_y_offset)], fill=GEM_BLUE, outline=OUTLINE)
                draw.ellipse([44, 30, 50, 36], fill=SKIN)

                draw.ellipse([27, 11 + bob, 41, 26 + bob], fill=SKIN, outline=OUTLINE)
                draw.polygon([(31, 20 + bob), (43, 20 + bob), (36, 40 + bob)], fill=HAIR_WHITE, outline=OUTLINE)

                draw.polygon([(26, 12 + bob), (44, 12 + bob), (34, 4 + bob)], fill=ROBE_PURPLE, outline=OUTLINE)
                draw.line([(27, 12 + bob), (43, 12 + bob)], fill=TRIM_GOLD, width=2)
                draw.rectangle([24, 14 + bob, 30, 34 + bob], fill=HAIR_WHITE)

            elif row == 3:  # UP
                draw.ellipse([18, 54, 46, 62], fill=(0, 0, 0, 90))
                draw.polygon([(20, 32), (44, 32), (48, 56), (16, 56)], fill=ROBE_PURPLE, outline=OUTLINE)
                draw.line([(18, 54), (46, 54)], fill=TRIM_GOLD, width=2)

                draw.rectangle([21, 24, 43, 33], fill=ROBE_PURPLE, outline=OUTLINE)
                draw.line([(50, 10), (50, 58)], fill=STAFF_WOOD, width=3)
                draw.polygon([(50, 4), (55, 9), (50, 14), (45, 9)], fill=GEM_BLUE, outline=OUTLINE)

                draw.rectangle([22, 14 + bob, 42, 38 + bob], fill=HAIR_WHITE, outline=OUTLINE)
                draw.line([(28, 16 + bob), (28, 36 + bob)], fill=HAIR_SHADOW, width=1)
                draw.line([(36, 16 + bob), (36, 36 + bob)], fill=HAIR_SHADOW, width=1)

                draw.polygon([(20, 12 + bob), (44, 12 + bob), (38, 4 + bob), (26, 4 + bob)], fill=ROBE_PURPLE, outline=OUTLINE)
                draw.line([(22, 12 + bob), (42, 12 + bob)], fill=TRIM_GOLD, width=2)

            sheet.paste(frame_img, (x_off, y_off))
    return sheet

def main():
    dirs = ensure_dirs()

    print("Generating NPC sprite sheets...")
    kafra = create_kafra_sprite()
    save_npc_sprite(kafra, "npc_kafra.png", dirs)

    blacksmith = create_blacksmith_sprite()
    save_npc_sprite(blacksmith, "npc_blacksmith.png", dirs)

    merchant = create_merchant_sprite()
    save_npc_sprite(merchant, "npc_merchant.png", dirs)

    elder = create_elder_sprite()
    save_npc_sprite(elder, "npc_elder.png", dirs)

    print("All 4 NPC sprite sheets generated successfully!")

if __name__ == "__main__":
    main()
