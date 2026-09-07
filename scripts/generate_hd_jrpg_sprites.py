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

def save_sprite(img, name, dirs):
    for d in dirs:
        path = os.path.join(d, name)
        img.save(path, "PNG")
        print(f"Saved 16-bit JRPG Sprite: {path} ({img.size[0]}x{img.size[1]})")

# Import 5-tone high detail drawing functions for all 12 hero classes
from generate_class_knight import draw_knight_frame
from generate_class_blackmage import draw_blackmage_frame
from generate_class_thief import draw_thief_frame
from generate_class_whitemage import draw_whitemage_frame
from generate_class_redmage import draw_redmage_frame
from generate_class_ranger import draw_ranger_frame
from generate_class_dragoon import draw_dragoon_frame
from generate_class_monk import draw_monk_frame
from generate_class_paladin import draw_paladin_frame
from generate_class_sage import draw_sage_frame
from generate_class_bard import draw_bard_frame
from generate_class_alchemist import draw_alchemist_frame

def generate_all_hd_sprites():
    dirs = ensure_dirs()
    classes_map = [
        ("hero_knight.png", draw_knight_frame),
        ("hero_blackmage.png", draw_blackmage_frame),
        ("hero_thief.png", draw_thief_frame),
        ("hero_whitemage.png", draw_whitemage_frame),
        ("hero_redmage.png", draw_redmage_frame),
        ("hero_ranger.png", draw_ranger_frame),
        ("hero_dragoon.png", draw_dragoon_frame),
        ("hero_monk.png", draw_monk_frame),
        ("hero_paladin.png", draw_paladin_frame),
        ("hero_sage.png", draw_sage_frame),
        ("hero_bard.png", draw_bard_frame),
        ("hero_alchemist.png", draw_alchemist_frame),
    ]

    for filename, func in classes_map:
        sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
        for row in range(4):
            for col in range(4):
                frame = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
                draw = ImageDraw.Draw(frame)
                func(draw, row, col)
                sheet.paste(frame, (col * 64, row * 64))
        save_sprite(sheet, filename, dirs)

if __name__ == "__main__":
    generate_all_hd_sprites()

