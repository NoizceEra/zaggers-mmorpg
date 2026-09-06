import os
import math
import random
from PIL import Image, ImageDraw

# Create output directories
DIR_ASSETS = r"D:\ai-studio\Zaggers\assets\tiles_ff"
DIR_WEB_ASSETS = r"D:\ai-studio\Zaggers\web\assets\tiles_ff"

os.makedirs(DIR_ASSETS, exist_ok=True)
os.makedirs(DIR_WEB_ASSETS, exist_ok=True)

TILE_W = 128
TILE_H = 64
SHEET_W = 256
SHEET_H = 256

def is_inside_diamond(x, y, tw=128, th=64):
    cx = tw / 2.0 - 0.5
    cy = th / 2.0 - 0.5
    return (abs(x - cx) / (tw / 2.0) + abs(y - cy) / (th / 2.0)) <= 1.0

def get_diamond_dist(x, y, tw=128, th=64):
    cx = tw / 2.0 - 0.5
    cy = th / 2.0 - 0.5
    return abs(x - cx) / (tw / 2.0) + abs(y - cy) / (th / 2.0)

# Helper to draw diamond tile outline/border onto image
def apply_diamond_mask(img, border_color=(40, 50, 70, 255)):
    w, h = img.size
    pixels = img.load()
    for y in range(h):
        for x in range(w):
            d = get_diamond_dist(x, y, w, h)
            if d > 1.0:
                pixels[x, y] = (0, 0, 0, 0)
            elif d >= 0.94:
                # Border outline
                r, g, b, a = pixels[x, y]
                br, bg, bb, ba = border_color
                # blend
                pixels[x, y] = (int(r*0.4 + br*0.6), int(g*0.4 + bg*0.6), int(b*0.4 + bb*0.6), 255)

# --- TILE GENERATORS ---

def create_town_cobble_1():
    img = Image.new("RGBA", (128, 64), (0, 0, 0, 0))
    pixels = img.load()
    random.seed(42)
    
    # Cobblestone pattern grid
    for y in range(64):
        for x in range(128):
            if not is_inside_diamond(x, y): continue
            
            # Base slate color with noise
            noise = random.randint(-12, 12)
            base_r, base_g, base_b = 60 + noise, 70 + noise, 90 + noise
            
            # Cobblestone mortar lines
            gx = (x + y * 2) % 24
            gy = (y * 2 - x) % 18
            
            if gx <= 2 or gy <= 2:
                # Mortar line
                pixels[x, y] = (25, 30, 42, 255)
            elif gx <= 5 or gy <= 5:
                # Stone highlight edge (top-left bevel)
                pixels[x, y] = (min(255, base_r + 35), min(255, base_g + 35), min(255, base_b + 40), 255)
            elif gx >= 21 or gy >= 15:
                # Stone shadow edge (bottom-right bevel)
                pixels[x, y] = (max(0, base_r - 25), max(0, base_g - 25), max(0, base_b - 20), 255)
            else:
                pixels[x, y] = (base_r, base_g, base_b, 255)
                
    apply_diamond_mask(img, (35, 45, 65, 255))
    return img

def create_town_cobble_2():
    # Accent cobblestone with central diamond star inlay
    img = Image.new("RGBA", (128, 64), (0, 0, 0, 0))
    pixels = img.load()
    random.seed(101)
    
    for y in range(64):
        for x in range(128):
            if not is_inside_diamond(x, y): continue
            
            d = get_diamond_dist(x, y, 128, 64)
            noise = random.randint(-10, 10)
            
            if d < 0.4:
                # Central decorative star / golden inlay
                base_r, base_g, base_b = 180 + noise, 140 + noise, 60 + noise
                if (x + y) % 6 == 0:
                    pixels[x, y] = (220, 180, 80, 255)
                else:
                    pixels[x, y] = (base_r, base_g, base_b, 255)
            elif d < 0.5:
                # Dark border ring
                pixels[x, y] = (30, 35, 50, 255)
            else:
                # Outer cobblestones
                gx = (x - y * 2) % 20
                gy = (x * 2 + y) % 16
                base_r, base_g, base_b = 70 + noise, 80 + noise, 100 + noise
                if gx <= 2 or gy <= 2:
                    pixels[x, y] = (28, 32, 45, 255)
                else:
                    pixels[x, y] = (base_r, base_g, base_b, 255)
                    
    apply_diamond_mask(img, (40, 50, 75, 255))
    return img

def create_town_stone_border():
    # Stone slab border with smooth chiselled center
    img = Image.new("RGBA", (128, 64), (0, 0, 0, 0))
    pixels = img.load()
    random.seed(88)
    
    for y in range(64):
        for x in range(128):
            if not is_inside_diamond(x, y): continue
            d = get_diamond_dist(x, y, 128, 64)
            noise = random.randint(-8, 8)
            
            if d >= 0.75:
                # Outer stone trim border
                pixels[x, y] = (100 + noise, 110 + noise, 130 + noise, 255)
            elif abs(d - 0.74) < 0.03:
                # Chiselled border groove
                pixels[x, y] = (25, 30, 42, 255)
            else:
                # Smooth stone slab interior
                pixels[x, y] = (75 + noise, 85 + noise, 108 + noise, 255)
                
    apply_diamond_mask(img, (50, 60, 85, 255))
    return img

def create_town_brick():
    # Decorative terracotta brick tile
    img = Image.new("RGBA", (128, 64), (0, 0, 0, 0))
    pixels = img.load()
    random.seed(202)
    
    for y in range(64):
        for x in range(128):
            if not is_inside_diamond(x, y): continue
            
            noise = random.randint(-12, 12)
            base_r, base_g, base_b = 140 + noise, 75 + noise, 55 + noise
            
            # Brick grid
            bx = (x + y * 2) % 16
            by = (y - x // 2) % 10
            
            if bx == 0 or by == 0:
                pixels[x, y] = (50, 25, 18, 255)
            elif bx == 1 or by == 1:
                pixels[x, y] = (180 + noise, 100 + noise, 75 + noise, 255)
            else:
                pixels[x, y] = (base_r, base_g, base_b, 255)
                
    apply_diamond_mask(img, (60, 30, 20, 255))
    return img


# --- MEADOW GENERATORS ---

def create_meadow_grass():
    img = Image.new("RGBA", (128, 64), (0, 0, 0, 0))
    pixels = img.load()
    random.seed(777)
    
    for y in range(64):
        for x in range(128):
            if not is_inside_diamond(x, y): continue
            
            noise = random.randint(-15, 15)
            # Rich green grass base
            r = max(0, min(255, 45 + noise))
            g = max(0, min(255, 140 + noise * 2))
            b = max(0, min(255, 50 + noise))
            
            pixels[x, y] = (r, g, b, 255)
            
    # Add grass blade highlights
    draw = ImageDraw.Draw(img)
    for _ in range(80):
        gx = random.randint(10, 118)
        gy = random.randint(10, 54)
        if is_inside_diamond(gx, gy):
            draw.line([(gx, gy), (gx + random.choice([-1, 1]), gy - random.randint(2, 4))],
                      fill=(110, 210, 90, 255), width=1)
                      
    apply_diamond_mask(img, (30, 90, 35, 255))
    return img

def create_meadow_dirt():
    img = Image.new("RGBA", (128, 64), (0, 0, 0, 0))
    pixels = img.load()
    random.seed(333)
    
    for y in range(64):
        for x in range(128):
            if not is_inside_diamond(x, y): continue
            
            d = get_diamond_dist(x, y, 128, 64)
            noise = random.randint(-15, 15)
            
            if d > 0.75:
                # Grassy edge
                pixels[x, y] = (45 + noise, 130 + noise, 45 + noise, 255)
            else:
                # Dirt path core
                r = max(0, min(255, 115 + noise))
                g = max(0, min(255, 80 + noise))
                b = max(0, min(255, 55 + noise))
                pixels[x, y] = (r, g, b, 255)
                
    # Add pebbles
    draw = ImageDraw.Draw(img)
    for _ in range(25):
        px = random.randint(20, 108)
        py = random.randint(15, 48)
        if is_inside_diamond(px, py) and get_diamond_dist(px, py) < 0.7:
            draw.ellipse([px, py, px+2, py+1], fill=(160, 140, 120, 255))
            
    apply_diamond_mask(img, (80, 60, 40, 255))
    return img

def create_meadow_flowers():
    img = create_meadow_grass()
    draw = ImageDraw.Draw(img)
    random.seed(555)
    
    flower_colors = [
        (240, 70, 70, 255),   # Red
        (255, 220, 50, 255),  # Yellow
        (80, 160, 240, 255),  # Blue
        (240, 240, 255, 255)  # White
    ]
    
    for _ in range(16):
        fx = random.randint(15, 112)
        fy = random.randint(12, 52)
        if is_inside_diamond(fx, fy, 128, 64) and get_diamond_dist(fx, fy) < 0.8:
            color = random.choice(flower_colors)
            # 3x3 flower cross
            draw.point([(fx, fy-1), (fx-1, fy), (fx, fy), (fx+1, fy), (fx, fy+1)], fill=color)
            draw.point([(fx, fy)], fill=(255, 235, 100, 255)) # yellow stem center
            
    apply_diamond_mask(img, (30, 90, 35, 255))
    return img

def create_meadow_water():
    img = Image.new("RGBA", (128, 64), (0, 0, 0, 0))
    pixels = img.load()
    random.seed(999)
    
    for y in range(64):
        for x in range(128):
            if not is_inside_diamond(x, y): continue
            
            wave = int(math.sin((x + y*2) * 0.15) * 12)
            noise = random.randint(-8, 8)
            
            # Crystal blue water gradient with ripples
            r = max(0, min(255, 15 + wave + noise))
            g = max(0, min(255, 130 + wave*2 + noise))
            b = max(0, min(255, 210 + wave + noise))
            
            pixels[x, y] = (r, g, b, 235)
            
    # Add foam highlights
    draw = ImageDraw.Draw(img)
    for _ in range(12):
        wx = random.randint(20, 100)
        wy = random.randint(15, 48)
        if is_inside_diamond(wx, wy) and get_diamond_dist(wx, wy) < 0.75:
            draw.arc([wx, wy, wx+12, wy+4], start=0, end=180, fill=(220, 245, 255, 220), width=1)
            
    apply_diamond_mask(img, (20, 100, 160, 255))
    return img


# --- DUNGEON GENERATORS ---

def create_dungeon_slate():
    img = Image.new("RGBA", (128, 64), (0, 0, 0, 0))
    pixels = img.load()
    random.seed(666)
    
    for y in range(64):
        for x in range(128):
            if not is_inside_diamond(x, y): continue
            
            noise = random.randint(-10, 10)
            base_r, base_g, base_b = 32 + noise, 38 + noise, 52 + noise
            
            # Large stone slab grid
            sx = (x + y * 2) % 32
            sy = (y * 2 - x) % 24
            
            if sx <= 2 or sy <= 2:
                pixels[x, y] = (12, 15, 22, 255) # dark mortar
            elif sx <= 4 or sy <= 4:
                pixels[x, y] = (60 + noise, 70 + noise, 90 + noise, 255) # slab highlight
            else:
                pixels[x, y] = (base_r, base_g, base_b, 255)
                
    apply_diamond_mask(img, (20, 25, 38, 255))
    return img

def create_dungeon_obsidian():
    img = Image.new("RGBA", (128, 64), (0, 0, 0, 0))
    pixels = img.load()
    random.seed(444)
    
    for y in range(64):
        for x in range(128):
            if not is_inside_diamond(x, y): continue
            
            noise = random.randint(-6, 6)
            # Pitch black obsidian base
            pixels[x, y] = (18 + noise, 16 + noise, 24 + noise, 255)
            
    # Glowing magma cracks
    draw = ImageDraw.Draw(img)
    cracks = [
        [(25, 30), (45, 25), (65, 35), (90, 20)],
        [(45, 25), (55, 45), (75, 48)],
        [(65, 35), (85, 42), (105, 38)]
    ]
    for pts in cracks:
        draw.line(pts, fill=(255, 60, 0, 255), width=2)
        draw.line(pts, fill=(255, 200, 0, 255), width=1)
        
    apply_diamond_mask(img, (15, 12, 20, 255))
    return img

def create_dungeon_lava():
    img = Image.new("RGBA", (128, 64), (0, 0, 0, 0))
    pixels = img.load()
    random.seed(888)
    
    for y in range(64):
        for x in range(128):
            if not is_inside_diamond(x, y): continue
            
            heat = int(math.sin((x * 0.1) + (y * 0.2)) * 30 + math.cos(x * 0.15 - y * 0.1) * 20)
            noise = random.randint(-15, 15)
            
            # Molten lava color gradient
            val = heat + noise
            if val > 20:
                # Bright yellow molten core
                r, g, b = 255, 230, 60 + noise
            elif val > -10:
                # Vibrant fiery orange
                r, g, b = 255, 110 + noise, 10
            else:
                # Deep crimson red lava / crust
                r, g, b = 180 + noise, 20, 10
                
            pixels[x, y] = (r, g, b, 255)
            
    # Floating black basalt crust flakes
    draw = ImageDraw.Draw(img)
    for _ in range(10):
        bx = random.randint(25, 95)
        by = random.randint(18, 44)
        if is_inside_diamond(bx, by) and get_diamond_dist(bx, by) < 0.7:
            draw.polygon([(bx, by), (bx+6, by-2), (bx+10, by+3), (bx+4, by+5)], fill=(30, 20, 20, 255))
            
    apply_diamond_mask(img, (180, 40, 10, 255))
    return img

def create_dungeon_rune():
    img = create_dungeon_slate()
    draw = ImageDraw.Draw(img)
    
    # Glowing magical cyan runic circle in center
    cx, cy = 64, 32
    draw.ellipse([cx-20, cy-10, cx+20, cy+10], outline=(0, 229, 255, 255), width=2)
    draw.ellipse([cx-12, cy-6, cx+12, cy+6], outline=(179, 136, 255, 255), width=1)
    
    # Runic accents
    draw.line([(cx-20, cy), (cx+20, cy)], fill=(0, 229, 255, 200), width=1)
    draw.line([(cx, cy-10), (cx, cy+10)], fill=(0, 229, 255, 200), width=1)
    
    apply_diamond_mask(img, (20, 25, 38, 255))
    return img

# --- BUILD TILESETS AND SAVE ---

def build_tileset(tile_tl, tile_tr, tile_bl, tile_br):
    sheet = Image.new("RGBA", (SHEET_W, SHEET_H), (0, 0, 0, 0))
    sheet.paste(tile_tl, (0, 0))
    sheet.paste(tile_tr, (128, 0))
    sheet.paste(tile_bl, (0, 128))
    sheet.paste(tile_br, (128, 128))
    return sheet

def main():
    print("Generating 2.5D Isometric Ground Tilesets...")
    
    # Town
    t_cobble1 = create_town_cobble_1()
    t_cobble2 = create_town_cobble_2()
    t_border = create_town_stone_border()
    t_brick = create_town_brick()
    tileset_town = build_tileset(t_cobble1, t_cobble2, t_border, t_brick)
    
    # Meadow
    m_grass = create_meadow_grass()
    m_dirt = create_meadow_dirt()
    m_flowers = create_meadow_flowers()
    m_water = create_meadow_water()
    tileset_meadow = build_tileset(m_grass, m_dirt, m_flowers, m_water)
    
    # Dungeon
    d_slate = create_dungeon_slate()
    d_obsidian = create_dungeon_obsidian()
    d_lava = create_dungeon_lava()
    d_rune = create_dungeon_rune()
    tileset_dungeon = build_tileset(d_slate, d_obsidian, d_lava, d_rune)
    
    # Save Tilesets
    tilesets = {
        "tileset_town_ff.png": tileset_town,
        "tileset_meadow_ff.png": tileset_meadow,
        "tileset_dungeon_ff.png": tileset_dungeon,
    }
    
    # Also individual tiles for convenience
    individual_tiles = {
        "tile_town_cobble.png": t_cobble1,
        "tile_town_cobble2.png": t_cobble2,
        "tile_town_border.png": t_border,
        "tile_town_brick.png": t_brick,
        "tile_meadow_grass.png": m_grass,
        "tile_meadow_dirt.png": m_dirt,
        "tile_meadow_flowers.png": m_flowers,
        "tile_meadow_water.png": m_water,
        "tile_dungeon_slate.png": d_slate,
        "tile_dungeon_obsidian.png": d_obsidian,
        "tile_dungeon_lava.png": d_lava,
        "tile_dungeon_rune.png": d_rune,
    }
    
    all_files = {**tilesets, **individual_tiles}
    
    for filename, img in all_files.items():
        path_assets = os.path.join(DIR_ASSETS, filename)
        path_web = os.path.join(DIR_WEB_ASSETS, filename)
        img.save(path_assets, "PNG")
        img.save(path_web, "PNG")
        print(f"Saved: {filename} to both asset locations.")

if __name__ == "__main__":
    main()
