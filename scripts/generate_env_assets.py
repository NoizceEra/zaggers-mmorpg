import math
import os
from PIL import Image, ImageDraw, ImageFilter

def ensure_dirs():
    dirs = [
        r"D:\ai-studio\Zaggers\assets\tiles_ff",
        r"D:\ai-studio\Zaggers\web\assets\tiles_ff"
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    return dirs

def save_asset(img, name, dirs):
    for d in dirs:
        path = os.path.join(d, name)
        img.save(path, "PNG")
        print(f"Saved: {path} ({img.size[0]}x{img.size[1]})")

def draw_shadow(draw, center, rx, ry, alpha=90):
    cx, cy = center
    bbox = [cx - rx, cy - ry, cx + rx, cy + ry]
    draw.ellipse(bbox, fill=(10, 15, 25, alpha))

def create_house_shop():
    w, h = 128, 128
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Ground shadow
    draw_shadow(draw, (64, 108), 50, 20, 110)
    
    # Base Wall Isometric Box
    left_wall = [(64, 98), (24, 78), (24, 48), (64, 68)]
    draw.polygon(left_wall, fill=(110, 95, 80, 255), outline=(60, 50, 40, 255))
    
    right_wall = [(64, 98), (104, 78), (104, 48), (64, 68)]
    draw.polygon(right_wall, fill=(155, 138, 118, 255), outline=(75, 62, 50, 255))
    
    # Timber Beams detail on left wall
    draw.line([(44, 88), (44, 58)], fill=(70, 55, 42, 255), width=3)
    draw.line([(24, 63), (64, 83)], fill=(70, 55, 42, 255), width=2)
    
    # Timber Beams detail on right wall
    draw.line([(84, 88), (84, 58)], fill=(85, 68, 52, 255), width=3)
    draw.line([(64, 83), (104, 63)], fill=(85, 68, 52, 255), width=2)

    # Wooden Shop Door on Right Wall
    door = [(74, 90), (86, 84), (86, 64), (74, 70)]
    draw.polygon(door, fill=(75, 45, 25, 255), outline=(40, 20, 10, 255))
    draw.ellipse([82, 77, 85, 80], fill=(220, 180, 50, 255))

    # Glass Window with Glow on Left Wall
    win = [(36, 76), (48, 82), (48, 68), (36, 62)]
    draw.polygon(win, fill=(255, 220, 110, 255), outline=(50, 40, 30, 255))
    draw.line([(42, 79), (42, 65)], fill=(120, 90, 40, 255), width=1)
    draw.line([(36, 69), (48, 75)], fill=(120, 90, 40, 255), width=1)
    
    # Roof (Isometric Terracotta Roof)
    left_roof = [(64, 42), (16, 46), (16, 26), (64, 18)]
    draw.polygon(left_roof, fill=(160, 55, 45, 255), outline=(90, 25, 20, 255))
    
    right_roof = [(64, 42), (112, 46), (112, 26), (64, 18)]
    draw.polygon(right_roof, fill=(210, 80, 65, 255), outline=(110, 35, 25, 255))
    
    front_gable = [(64, 42), (20, 46), (64, 68)]
    draw.polygon(front_gable, fill=(130, 110, 90, 255), outline=(70, 55, 40, 255))
    front_gable_r = [(64, 42), (108, 46), (64, 68)]
    draw.polygon(front_gable_r, fill=(160, 138, 115, 255), outline=(80, 65, 50, 255))

    # Roof Shingle Lines
    for sy in range(24, 44, 4):
        draw.line([(64, sy), (16, sy + 8)], fill=(120, 40, 30, 255), width=1)
        draw.line([(64, sy), (112, sy + 8)], fill=(230, 100, 80, 255), width=1)

    # Wooden Shop Sign
    sign_post = [(88, 62), (106, 53)]
    draw.line(sign_post, fill=(60, 40, 20, 255), width=3)
    sign_board = [(92, 60), (104, 54), (104, 66), (92, 72)]
    draw.polygon(sign_board, fill=(220, 175, 100, 255), outline=(90, 60, 20, 255))
    draw.text((94, 61), "SHOP", fill=(100, 40, 10, 255))

    # Stone Chimney
    chimney_left = [(30, 34), (38, 30), (38, 14), (30, 18)]
    chimney_right = [(38, 30), (44, 33), (44, 17), (38, 14)]
    draw.polygon(chimney_left, fill=(80, 85, 95, 255), outline=(40, 45, 55, 255))
    draw.polygon(chimney_right, fill=(110, 115, 125, 255), outline=(50, 55, 65, 255))
    
    # Smoke puffs
    draw.ellipse([34, 6, 40, 12], fill=(220, 225, 235, 160))
    draw.ellipse([38, 1, 46, 7], fill=(240, 245, 250, 200))

    return img

def create_fountain():
    w, h = 96, 96
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    draw_shadow(draw, (48, 76), 40, 16, 120)
    
    # Outer Stone Fountain Rim
    draw.ellipse([8, 48, 88, 84], fill=(80, 88, 98, 255), outline=(45, 50, 60, 255))
    draw.ellipse([8, 42, 88, 78], fill=(130, 140, 155, 255), outline=(70, 78, 90, 255))
    
    # Inner Water Pool
    draw.ellipse([14, 46, 82, 74], fill=(20, 40, 60, 255))
    draw.ellipse([16, 48, 80, 72], fill=(30, 140, 210, 220))
    
    # Water ripples
    draw.ellipse([24, 54, 72, 66], fill=None, outline=(120, 210, 255, 180), width=1)
    draw.ellipse([32, 57, 64, 63], fill=None, outline=(200, 245, 255, 220), width=1)
    
    # Center Stone Column Pedestal
    draw.rectangle([42, 38, 54, 60], fill=(100, 110, 125, 255), outline=(50, 55, 65, 255))
    draw.rectangle([44, 38, 54, 60], fill=(140, 150, 165, 255))
    
    # Upper Water Basin Bowl
    draw.ellipse([28, 30, 68, 46], fill=(90, 100, 115, 255), outline=(50, 55, 65, 255))
    draw.ellipse([28, 26, 68, 42], fill=(150, 160, 175, 255), outline=(80, 90, 105, 255))
    draw.ellipse([32, 28, 64, 40], fill=(40, 160, 230, 240))
    
    # Top Spout Pillar
    draw.rectangle([45, 18, 51, 30], fill=(160, 170, 185, 255), outline=(70, 75, 85, 255))
    draw.ellipse([43, 14, 53, 20], fill=(180, 190, 205, 255))
    
    # Water Fountain Spray
    draw.line([(48, 14), (48, 4)], fill=(220, 245, 255, 255), width=3)
    draw.line([(48, 4), (44, 18)], fill=(150, 220, 255, 200), width=2)
    draw.line([(48, 4), (52, 18)], fill=(150, 220, 255, 200), width=2)
    
    # Waterfalls
    draw.line([(34, 36), (30, 56)], fill=(180, 235, 255, 190), width=2)
    draw.line([(62, 36), (66, 56)], fill=(180, 235, 255, 190), width=2)
    draw.line([(48, 40), (48, 58)], fill=(200, 240, 255, 210), width=2)
    
    # Water Splash Droplets
    draw.ellipse([46, 2, 50, 6], fill=(240, 255, 255, 255))
    draw.ellipse([28, 54, 32, 58], fill=(220, 250, 255, 220))
    draw.ellipse([64, 54, 68, 58], fill=(220, 250, 255, 220))

    return img

def create_market_stall():
    w, h = 96, 96
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    draw_shadow(draw, (48, 76), 36, 14, 110)
    
    # Wooden Table Legs
    draw.line([(24, 55), (24, 72)], fill=(60, 42, 25, 255), width=3)
    draw.line([(72, 43), (72, 60)], fill=(75, 52, 32, 255), width=3)
    draw.line([(18, 62), (18, 78)], fill=(60, 42, 25, 255), width=3)
    draw.line([(78, 48), (78, 66)], fill=(75, 52, 32, 255), width=3)
    
    # Wooden Table Top Box
    draw.polygon([(18, 62), (48, 76), (48, 70), (18, 56)], fill=(100, 70, 40, 255), outline=(50, 32, 18, 255))
    draw.polygon([(48, 76), (78, 62), (78, 56), (48, 70)], fill=(135, 95, 55, 255), outline=(65, 42, 22, 255))
    draw.polygon([(18, 56), (48, 42), (78, 56), (48, 70)], fill=(160, 115, 68, 255), outline=(85, 58, 30, 255))

    # Goods on display
    draw.ellipse([26, 50, 40, 60], fill=(110, 75, 40, 255), outline=(60, 35, 15, 255))
    for ax, ay in [(29, 52), (34, 51), (31, 55), (36, 54)]:
        draw.ellipse([ax, ay, ax+4, ay+4], fill=(225, 45, 45, 255))
    
    draw.ellipse([42, 54, 56, 64], fill=(110, 75, 40, 255), outline=(60, 35, 15, 255))
    for ox, oy in [(44, 56), (49, 55), (46, 58), (51, 58)]:
        draw.ellipse([ox, oy, ox+4, oy+4], fill=(245, 140, 30, 255))
        
    draw.rectangle([60, 52, 64, 60], fill=(240, 60, 80, 240))
    draw.ellipse([59, 50, 65, 54], fill=(200, 200, 220, 255))
    draw.rectangle([68, 48, 72, 56], fill=(50, 140, 240, 240))
    draw.ellipse([67, 46, 73, 50], fill=(200, 200, 220, 255))

    # Awning Canopy Posts
    draw.line([(18, 56), (18, 24)], fill=(80, 55, 30, 255), width=2)
    draw.line([(78, 56), (78, 24)], fill=(100, 70, 40, 255), width=2)
    draw.line([(48, 42), (48, 12)], fill=(90, 62, 35, 255), width=2)
    draw.line([(48, 70), (48, 38)], fill=(100, 70, 40, 255), width=2)

    # Red & White Striped Canopy Roof
    draw.polygon([(48, 6), (12, 22), (48, 36)], fill=(180, 40, 40, 255), outline=(90, 20, 20, 255))
    draw.polygon([(48, 6), (84, 22), (48, 36)], fill=(235, 60, 60, 255), outline=(120, 30, 30, 255))

    draw.polygon([(48, 6), (30, 14), (48, 36)], fill=(230, 230, 235, 255))
    draw.polygon([(48, 6), (66, 14), (48, 36)], fill=(245, 245, 250, 255))

    # Scalloped Awning Fringe Trims
    for fx in range(14, 48, 8):
        fy = 22 + (fx - 14) * (14 / 34)
        draw.ellipse([fx-3, fy, fx+3, fy+5], fill=(230, 50, 50, 255))
    for fx in range(48, 84, 8):
        fy = 36 - (fx - 48) * (14 / 36)
        draw.ellipse([fx-3, fy, fx+3, fy+5], fill=(230, 230, 235, 255))

    return img

def create_barrel_crate():
    w, h = 64, 64
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    draw_shadow(draw, (32, 50), 26, 10, 110)

    # 1. Wooden Crate
    draw.polygon([(10, 36), (28, 45), (28, 25), (10, 16)], fill=(120, 85, 50, 255), outline=(65, 45, 25, 255))
    draw.polygon([(28, 45), (46, 36), (46, 16), (28, 25)], fill=(165, 120, 75, 255), outline=(85, 60, 35, 255))
    draw.polygon([(10, 16), (28, 7), (46, 16), (28, 25)], fill=(195, 145, 95, 255), outline=(100, 72, 42, 255))
    
    draw.line([(10, 16), (28, 45)], fill=(75, 52, 30, 255), width=2)
    draw.line([(10, 36), (28, 25)], fill=(75, 52, 30, 255), width=2)
    draw.line([(28, 25), (46, 36)], fill=(100, 70, 40, 255), width=2)
    draw.line([(28, 45), (46, 16)], fill=(100, 70, 40, 255), width=2)
    for cx, cy in [(10, 16), (28, 25), (46, 16), (28, 45)]:
        draw.rectangle([cx-2, cy-2, cx+2, cy+2], fill=(70, 75, 85, 255))

    # 2. Wooden Barrel #1
    draw.ellipse([20, 34, 44, 56], fill=(95, 62, 32, 255), outline=(50, 30, 15, 255))
    draw.rectangle([20, 26, 44, 45], fill=(130, 85, 45, 255))
    draw.ellipse([20, 18, 44, 30], fill=(175, 120, 68, 255), outline=(85, 55, 28, 255))
    
    draw.ellipse([20, 23, 44, 31], fill=None, outline=(70, 75, 85, 255), width=2)
    draw.ellipse([20, 38, 44, 46], fill=None, outline=(70, 75, 85, 255), width=2)
    draw.line([(26, 22), (26, 48)], fill=(85, 52, 25, 255), width=1)
    draw.line([(32, 24), (32, 50)], fill=(95, 58, 28, 255), width=1)
    draw.line([(38, 22), (38, 48)], fill=(145, 95, 52, 255), width=1)

    # 3. Smaller Barrel #2
    draw.ellipse([38, 40, 58, 58], fill=(85, 55, 28, 255), outline=(45, 28, 12, 255))
    draw.rectangle([38, 33, 58, 49], fill=(120, 78, 40, 255))
    draw.ellipse([38, 26, 58, 36], fill=(160, 110, 60, 255), outline=(75, 48, 24, 255))
    draw.ellipse([38, 30, 58, 37], fill=None, outline=(65, 70, 80, 255), width=2)
    draw.ellipse([38, 43, 58, 50], fill=None, outline=(65, 70, 80, 255), width=2)

    return img

def create_tree_meadow():
    w, h = 96, 128
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    draw_shadow(draw, (48, 112), 40, 14, 110)
    
    # Trunk
    trunk = [(44, 112), (52, 112), (54, 70), (42, 70)]
    draw.polygon(trunk, fill=(90, 60, 35, 255), outline=(50, 32, 18, 255))
    draw.line([(49, 112), (51, 70)], fill=(130, 90, 55, 255), width=3)
    draw.line([(44, 110), (36, 116)], fill=(75, 48, 25, 255), width=4)
    draw.line([(52, 110), (60, 116)], fill=(95, 65, 38, 255), width=4)

    # Foliage Canopy
    draw.ellipse([12, 45, 84, 95], fill=(30, 85, 45, 255))
    draw.ellipse([8, 25, 70, 75], fill=(42, 120, 60, 255))
    draw.ellipse([26, 30, 88, 80], fill=(48, 135, 68, 255))
    draw.ellipse([18, 8, 78, 60], fill=(65, 175, 85, 255))
    
    draw.ellipse([40, 12, 74, 45], fill=(95, 215, 115, 255))
    draw.ellipse([50, 35, 84, 65], fill=(85, 200, 105, 255))
    draw.ellipse([24, 20, 52, 48], fill=(80, 190, 98, 255))

    draw.ellipse([54, 16, 70, 32], fill=(140, 240, 155, 255))
    draw.ellipse([62, 38, 76, 52], fill=(130, 235, 145, 255))

    return img

def create_bush():
    w, h = 64, 64
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    draw_shadow(draw, (32, 52), 26, 10, 100)
    
    draw.ellipse([6, 22, 42, 52], fill=(32, 90, 48, 255))
    draw.ellipse([22, 24, 58, 54], fill=(28, 82, 42, 255))
    draw.ellipse([14, 12, 50, 44], fill=(42, 115, 58, 255))

    draw.ellipse([10, 16, 44, 38], fill=(62, 165, 82, 255))
    draw.ellipse([26, 18, 54, 46], fill=(55, 152, 75, 255))
    draw.ellipse([18, 10, 46, 30], fill=(82, 198, 102, 255))

    draw.ellipse([22, 12, 38, 24], fill=(125, 230, 142, 255))
    draw.ellipse([34, 20, 48, 32], fill=(110, 215, 128, 255))

    berries = [(16, 28), (24, 36), (32, 22), (40, 32), (44, 24), (28, 16)]
    for bx, by in berries:
        draw.ellipse([bx-2, by-2, bx+2, by+2], fill=(235, 45, 55, 255))
        draw.ellipse([bx-1, by-1, bx, by], fill=(255, 180, 185, 255))

    return img

def create_rock():
    w, h = 64, 64
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    draw_shadow(draw, (32, 48), 26, 10, 110)

    draw.polygon([(6, 44), (16, 48), (22, 40), (14, 34)], fill=(80, 88, 98, 255), outline=(45, 50, 60, 255))
    draw.polygon([(14, 34), (22, 40), (18, 32)], fill=(130, 140, 155, 255))

    draw.polygon([(14, 46), (36, 56), (56, 44), (58, 26), (38, 14), (18, 22)], fill=(70, 78, 88, 255), outline=(40, 45, 52, 255))
    draw.polygon([(14, 46), (36, 56), (34, 34), (18, 22)], fill=(90, 100, 112, 255))
    draw.polygon([(36, 56), (56, 44), (46, 32), (34, 34)], fill=(110, 120, 135, 255))
    draw.polygon([(18, 22), (34, 34), (46, 32), (58, 26), (38, 14)], fill=(170, 182, 198, 255))
    draw.polygon([(26, 20), (36, 26), (46, 22), (38, 14)], fill=(210, 222, 238, 255))

    draw.line([(34, 34), (38, 14)], fill=(45, 50, 60, 255), width=2)
    draw.line([(34, 34), (36, 56)], fill=(45, 50, 60, 255), width=2)
    draw.line([(34, 34), (46, 32)], fill=(45, 50, 60, 255), width=1)
    
    draw.ellipse([22, 18, 32, 24], fill=(75, 145, 75, 220))
    draw.ellipse([40, 22, 48, 28], fill=(65, 135, 65, 200))

    return img

def create_crystal():
    w, h = 64, 96
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    draw_shadow(draw, (32, 82), 22, 8, 110)
    
    draw.ellipse([14, 72, 50, 86], fill=(130, 95, 25, 255), outline=(70, 48, 10, 255))
    draw.ellipse([16, 70, 48, 82], fill=(210, 165, 45, 255), outline=(110, 80, 20, 255))
    draw.ellipse([22, 72, 42, 80], fill=(245, 205, 75, 255))
    
    draw.polygon([(18, 72), (22, 60), (26, 74)], fill=(210, 165, 45, 255), outline=(100, 70, 15, 255))
    draw.polygon([(46, 72), (42, 60), (38, 74)], fill=(210, 165, 45, 255), outline=(100, 70, 15, 255))
    draw.polygon([(30, 74), (32, 58), (34, 74)], fill=(245, 205, 75, 255))

    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse([8, 12, 56, 64], fill=(40, 220, 255, 140))
    glow = glow.filter(ImageFilter.GaussianBlur(8))
    img.alpha_composite(glow)
    
    draw.polygon([(32, 8), (12, 36), (32, 28)], fill=(20, 140, 180, 255))
    draw.polygon([(32, 8), (52, 36), (32, 28)], fill=(40, 170, 210, 255))
    draw.polygon([(32, 8), (12, 36), (32, 44)], fill=(30, 185, 225, 255), outline=(15, 110, 140, 255))
    draw.polygon([(32, 8), (52, 36), (32, 44)], fill=(120, 235, 255, 255), outline=(30, 160, 190, 255))
    draw.polygon([(32, 64), (12, 36), (32, 44)], fill=(20, 150, 190, 255), outline=(10, 90, 120, 255))
    draw.polygon([(32, 64), (52, 36), (32, 44)], fill=(70, 210, 245, 255), outline=(20, 130, 160, 255))

    draw.line([(32, 12), (32, 60)], fill=(230, 255, 255, 255), width=2)
    draw.line([(16, 36), (48, 36)], fill=(200, 250, 255, 220), width=1)
    
    draw.ellipse([30, 22, 34, 26], fill=(255, 255, 255, 255))
    draw.line([(32, 18), (32, 30)], fill=(255, 255, 255, 255), width=1)
    draw.line([(26, 24), (38, 24)], fill=(255, 255, 255, 255), width=1)

    return img

def create_dungeon_pillar():
    w, h = 64, 128
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    draw_shadow(draw, (32, 116), 26, 9, 120)
    
    draw.polygon([(10, 116), (32, 124), (54, 116), (54, 108), (32, 100), (10, 108)], fill=(45, 48, 58, 255), outline=(25, 28, 35, 255))
    draw.polygon([(10, 116), (32, 124), (32, 116), (10, 108)], fill=(55, 60, 72, 255))
    draw.polygon([(32, 124), (54, 116), (54, 108), (32, 116)], fill=(75, 82, 98, 255))
    
    draw.polygon([(14, 106), (32, 112), (50, 106), (50, 98), (32, 92), (14, 98)], fill=(55, 60, 72, 255), outline=(30, 34, 42, 255))

    shaft = [(18, 98), (32, 103), (46, 98), (46, 28), (32, 23), (18, 28)]
    draw.polygon(shaft, fill=(50, 54, 65, 255), outline=(25, 28, 35, 255))
    draw.polygon([(18, 98), (32, 103), (32, 23), (18, 28)], fill=(60, 65, 78, 255))
    draw.polygon([(32, 103), (46, 98), (46, 28), (32, 23)], fill=(90, 98, 116, 255))

    draw.line([(24, 96), (24, 26)], fill=(40, 44, 54, 255), width=2)
    draw.line([(32, 101), (32, 24)], fill=(35, 38, 48, 255), width=2)
    draw.line([(40, 96), (40, 26)], fill=(115, 125, 145, 255), width=2)

    runes = [(32, 85), (32, 70), (32, 55), (32, 40)]
    for rx, ry in runes:
        draw.ellipse([rx-4, ry-4, rx+4, ry+4], fill=(160, 60, 240, 180))
        draw.line([(rx-3, ry), (rx+3, ry)], fill=(220, 180, 255, 255), width=2)
        draw.line([(rx, ry-3), (rx, ry+3)], fill=(220, 180, 255, 255), width=2)

    draw.polygon([(12, 28), (32, 34), (52, 28), (52, 18), (32, 12), (12, 18)], fill=(70, 76, 92, 255), outline=(35, 38, 48, 255))
    draw.polygon([(10, 18), (32, 24), (54, 18), (54, 8), (32, 2), (10, 8)], fill=(95, 104, 124, 255), outline=(45, 50, 62, 255))

    return img

def create_torch_brazier():
    w, h = 256, 64
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    
    flame_variations = [
        (0, 24, [(-2, -26), (3, -28)]),
        (-4, 26, [(-6, -28), (-1, -30), (2, -24)]),
        (2, 28, [(1, -32), (5, -30), (-3, -27)]),
        (4, 25, [(4, -28), (7, -26), (-2, -29)]),
    ]
    
    for i in range(4):
        f_img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(f_img)
        
        draw_shadow(draw, (32, 54), 18, 7, 110)
        
        draw.line([(32, 40), (18, 56)], fill=(35, 38, 45, 255), width=3)
        draw.line([(32, 40), (46, 56)], fill=(55, 60, 70, 255), width=3)
        draw.line([(32, 40), (32, 58)], fill=(45, 48, 56, 255), width=3)
        
        draw.ellipse([22, 46, 42, 52], fill=None, outline=(60, 65, 75, 255), width=2)
        
        draw.ellipse([18, 30, 46, 44], fill=(50, 54, 64, 255), outline=(25, 28, 35, 255))
        draw.ellipse([18, 26, 46, 40], fill=(85, 92, 108, 255), outline=(45, 50, 60, 255))
        
        draw.ellipse([22, 28, 42, 38], fill=(220, 70, 20, 255))
        draw.ellipse([25, 30, 39, 36], fill=(255, 170, 30, 255))

        glow = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(glow)
        gdraw.ellipse([10, 4, 54, 48], fill=(255, 140, 20, 90))
        glow = glow.filter(ImageFilter.GaussianBlur(6))
        f_img.alpha_composite(glow)
        
        lean, f_height, sparks = flame_variations[i]
        
        flame_poly = [
            (32, 32),
            (20, 26),
            (24 + lean//2, 18),
            (32 + lean, 32 - f_height),
            (40 + lean//2, 18),
            (44, 26)
        ]
        draw.polygon(flame_poly, fill=(245, 100, 20, 240))
        
        core_poly = [
            (32, 31),
            (24, 27),
            (32 + lean, 32 - int(f_height * 0.7)),
            (40, 27)
        ]
        draw.polygon(core_poly, fill=(255, 220, 50, 255))

        draw.ellipse([30 + lean//2, 24, 34 + lean//2, 30], fill=(255, 255, 220, 255))

        for sx, sy in sparks:
            draw.ellipse([32 + sx - 1, 32 + sy - 1, 32 + sx + 1, 32 + sy + 1], fill=(255, 200, 50, 240))
            
        img.paste(f_img, (i * 64, 0))
        
    return img

def main():
    dirs = ensure_dirs()
    
    assets = {
        "env_house_shop.png": create_house_shop(),
        "env_fountain.png": create_fountain(),
        "env_market_stall.png": create_market_stall(),
        "env_barrel_crate.png": create_barrel_crate(),
        "env_tree_meadow.png": create_tree_meadow(),
        "env_bush.png": create_bush(),
        "env_rock.png": create_rock(),
        "env_crystal.png": create_crystal(),
        "env_dungeon_pillar.png": create_dungeon_pillar(),
        "env_torch_brazier.png": create_torch_brazier()
    }
    
    for filename, img in assets.items():
        save_asset(img, filename, dirs)

if __name__ == "__main__":
    main()
