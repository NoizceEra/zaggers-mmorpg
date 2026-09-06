import os
from PIL import Image

def standardize_monster_sprites():
    project_root = r"D:\ai-studio\Zaggers"
    dirs = [
        os.path.join(project_root, "assets", "sprites_ff"),
        os.path.join(project_root, "web", "assets", "sprites_ff")
    ]
    
    monster_files = [
        "slime_green_ff.png",
        "goblin_ff.png",
        "skeleton_ff.png",
        "boss_baphomet_ff.png",
        "cactuar_ff.png",
        "bomb_ff.png"
    ]
    
    print("=== Standardizing Monster Sprite Sheets ===")
    for folder in dirs:
        print(f"\nProcessing folder: {folder}")
        if not os.path.exists(folder):
            print(f"Directory missing: {folder}")
            continue
            
        for filename in monster_files:
            file_path = os.path.join(folder, filename)
            if not os.path.exists(file_path):
                print(f"File missing: {file_path}")
                continue
                
            im = Image.open(file_path)
            orig_size = im.size
            orig_mode = im.mode
            
            # Ensure RGBA mode
            if im.mode != "RGBA":
                im = im.convert("RGBA")
                
            # Resize to exact 256x256 RGBA if needed
            if im.size != (256, 256):
                # Nearest neighbor resizing preserves pixel art sharpness
                im_rebuilt = im.resize((256, 256), resample=Image.NEAREST)
            else:
                im_rebuilt = im
                
            im_rebuilt.save(file_path, "PNG")
            print(f" -> {filename}: {orig_size} ({orig_mode}) => {im_rebuilt.size} ({im_rebuilt.mode}) [Saved]")

    print("\n=== Verification ===")
    all_valid = True
    for folder in dirs:
        for filename in monster_files:
            file_path = os.path.join(folder, filename)
            im = Image.open(file_path)
            w, h = im.size
            mode = im.mode
            valid = (w == 256 and h == 256 and mode == "RGBA")
            if not valid:
                all_valid = False
            print(f"{filename} in {os.path.basename(os.path.dirname(folder))}/{os.path.basename(folder)}: {w}x{h} {mode} - {'OK' if valid else 'FAIL'}")

    if all_valid:
        print("\nAll monster sprite sheets successfully standardized to 256x256 RGBA PNGs!")
    else:
        print("\nSome sprite sheets failed verification.")

if __name__ == "__main__":
    standardize_monster_sprites()
