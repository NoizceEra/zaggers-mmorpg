import os
from PIL import Image, ImageOps

def process_sprite_grid(src_path, dest_filename):
    project_root = r"D:\ai-studio\Zaggers"
    dest_dirs = [
        os.path.join(project_root, "assets", "sprites_ff"),
        os.path.join(project_root, "web", "assets", "sprites_ff")
    ]
    for d in dest_dirs:
        os.makedirs(d, exist_ok=True)

    img = Image.open(src_path).convert("RGBA")
    # Resize to exact 256x256 if needed
    img = img.resize((256, 256), Image.Resampling.NEAREST)

    # Convert white background to transparent
    datas = img.getdata()
    new_data = []
    for item in datas:
        r, g, b, a = item
        # Check if color is close to white (background)
        if r > 240 and g > 240 and b > 240:
            new_data.append((0, 0, 0, 0)) # Fully transparent
        else:
            new_data.append(item)
    img.putdata(new_data)

    for d in dest_dirs:
        out_path = os.path.join(d, dest_filename)
        img.save(out_path, "PNG")
        print(f"Processed & Saved Sprite Sheet: {out_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        process_sprite_grid(sys.argv[1], sys.argv[2])
