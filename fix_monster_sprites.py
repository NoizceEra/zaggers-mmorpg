import os
from PIL import Image

# Target directories to overwrite monster sprite sheets
TARGET_DIRS = [
    r'D:\ai-studio\Zaggers\assets\sprites_ff',
    r'D:\ai-studio\Zaggers\web\assets\sprites_ff'
]

MONSTER_FILES = [
    'slime_green_ff.png',
    'goblin_ff.png',
    'skeleton_ff.png',
    'boss_baphomet_ff.png',
    'cactuar_ff.png',
    'bomb_ff.png'
]

def process_monster_sheet(src_img_path):
    """
    Reads a source monster PNG sheet and outputs a clean 256x256 RGBA image
    where each of the 4 rows (Down=0, Left=1, Right=2, Up=3) x 4 cols (Walk0=0, Idle=1, Walk1=2, Attack=3)
    contains strictly ONE isolated 64x64 cell.
    """
    src = Image.open(src_img_path).convert('RGBA')
    filename = os.path.basename(src_img_path)
    
    # Create empty 256x256 RGBA canvas
    dst = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    
    if filename == 'boss_baphomet_ff.png':
        # Baphomet source has 4 64x64 sprites in top-left 128x128 grid:
        # (0,0) -> Down, (1,0) -> Left, (0,1) -> Right, (1,1) -> Up
        down_src = src.crop((0, 0, 64, 64))
        left_src = src.crop((64, 0, 128, 64))
        right_src = src.crop((0, 64, 64, 128))
        up_src = src.crop((64, 64, 128, 128))
        
        for c in range(4):
            dst.paste(down_src, (c * 64, 0 * 64))   # Row 0: Down
            dst.paste(left_src, (c * 64, 1 * 64))   # Row 1: Left
            dst.paste(right_src, (c * 64, 2 * 64))  # Row 2: Right
            dst.paste(up_src, (c * 64, 3 * 64))     # Row 3: Up
    else:
        # Standard 32x32 monster tiles in top-left 128x128 grid:
        # Row 0 (y=0..32): Down (cols 0..3: Walk0, Idle, Walk1, Attack)
        # Row 1 (y=32..64): Left
        # Row 2 (y=64..96): Right
        # Row 3 (y=96..128): Up
        for r in range(4):     # 0=Down, 1=Left, 2=Right, 3=Up
            for c in range(4): # 0=Walk0, 1=Idle, 2=Walk1, 3=Attack
                tile = src.crop((c * 32, r * 32, (c + 1) * 32, (r + 1) * 32))
                # Center 32x32 tile inside the 64x64 cell
                dst.paste(tile, (c * 64 + 16, r * 64 + 16))
                
    return dst

def main():
    print("Starting Monster Sprite Sheet Repair & Slicing...")
    
    # Process each monster file for all target directories
    for monster_file in MONSTER_FILES:
        primary_src_path = os.path.join(TARGET_DIRS[0], monster_file)
        if not os.path.exists(primary_src_path):
            print(f"Error: {primary_src_path} not found.")
            continue
            
        fixed_img = process_monster_sheet(primary_src_path)
        
        # Save fixed image to both directories
        for target_dir in TARGET_DIRS:
            out_path = os.path.join(target_dir, monster_file)
            os.makedirs(target_dir, exist_ok=True)
            fixed_img.save(out_path, 'PNG')
            print(f"Successfully wrote fixed sprite sheet: {out_path}")
            
    print("\nVerification on Disk:")
    for target_dir in TARGET_DIRS:
        print(f"\n--- Directory: {target_dir} ---")
        for monster_file in MONSTER_FILES:
            out_path = os.path.join(target_dir, monster_file)
            if os.path.exists(out_path):
                img = Image.open(out_path)
                print(f"{monster_file}: size={img.size}, mode={img.mode}")
                for r in range(4):
                    for c in range(4):
                        cell = img.crop((c * 64, r * 64, (c + 1) * 64, (r + 1) * 64))
                        bbox = cell.getbbox()
                        assert bbox is not None, f"Empty cell at (c={c}, r={r}) in {monster_file}"
            else:
                print(f"FAILED: {out_path} missing!")

if __name__ == '__main__':
    main()
