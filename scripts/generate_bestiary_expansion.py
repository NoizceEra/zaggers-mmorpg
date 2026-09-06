"""
generate_bestiary_expansion.py

Phase 3 art pass for the Zaggers bestiary expansion (vault/BESTIARY_EXPANSION.md,
vault/ASSET_MANIFEST.md Task A + Task B).

Follows the exact conventions of the existing generators
(generate_clean_monsters.py, standardize_monsters.py):
  - 256x256 RGBA sheet per monster, 4 rows x 4 cols of 64x64 cells
  - Row 0=Down, 1=Left, 2=Right, 3=Up ; Col 0=Walk0, 1=Idle, 2=Walk1, 3=Attack
  - PIL primitive drawing (ellipse/polygon/line), flat-shaded pixel-art style
  - normalize_and_center_cell() re-used verbatim so every sprite is bounded to
    44-52px and centered at (32,32), matching the legacy sheets exactly.
  - Saved to BOTH assets/sprites_ff/ and web/assets/sprites_ff/

Because this pass covers 48 brand-new monsters, art is produced through a small
library of parametric archetypes (BLOB, BIPED, QUAD, FLYER, PLANT, CONSTRUCT,
BOSS) rather than one bespoke function per monster. Each monster gets its own
config (element palette, silhouette proportions, accessories, weapon) so no two
sheets are identical, but the underlying shape-composition code is shared. This
keeps 48 sheets on-pipeline and internally consistent while staying within the
same PIL/flat-shape aesthetic as the original six.

TASK A (renames) is handled separately by copying pixels byte-for-byte from the
legacy filenames per BESTIARY_EXPANSION.md section 9 - no regeneration.
"""

import os
import math
import shutil
from PIL import Image, ImageDraw

ROOT = r"D:\ai-studio\Zaggers"
TARGET_DIRS = [
    os.path.join(ROOT, "assets", "sprites_ff"),
    os.path.join(ROOT, "web", "assets", "sprites_ff"),
]
SRC_DIR = os.path.join(ROOT, "assets", "sprites_ff")  # source of truth for renames

# -----------------------------------------------------------------------------
# TASK A — renames (BESTIARY_EXPANSION.md section 9 / ASSET_MANIFEST.md Task A)
# -----------------------------------------------------------------------------
RENAMES = {
    "slime_green_ff.png": "gloopling_bellflower_ff.png",
    "goblin_ff.png": "snagtooth_raider_ff.png",
    "skeleton_ff.png": "drowned_marrowguard_ff.png",
    "cactuar_ff.png": "pricklespine_thornmarch_ff.png",
    "bomb_ff.png": "cinderpuff_ff.png",
    "boss_baphomet_ff.png": "verrocaine_sovereign_ff.png",
}


def do_renames():
    print("=== TASK A: Renaming 6 legacy sprites (pixels unchanged) ===")
    for old, new in RENAMES.items():
        src = os.path.join(SRC_DIR, old)
        if not os.path.exists(src):
            print(f"  MISSING SOURCE: {src}")
            continue
        with Image.open(src) as im:
            im = im.convert("RGBA")
            for d in TARGET_DIRS:
                os.makedirs(d, exist_ok=True)
                out = os.path.join(d, new)
                im.save(out, "PNG")
                print(f"  {old} -> {out}")


# -----------------------------------------------------------------------------
# Color helpers
# -----------------------------------------------------------------------------
def hx(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)


def shade(c, f):
    """f<1 darkens toward black, f>1 lightens toward white."""
    r, g, b, a = c
    if f <= 1.0:
        return (int(r * f), int(g * f), int(b * f), a)
    t = f - 1.0
    return (int(r + (255 - r) * t), int(g + (255 - g) * t), int(b + (255 - b) * t), a)


ELEMENT_COLOR = {
    "Neutral": hx("#bdbdbd"),
    "Earth": hx("#8d6e63"),
    "Wind": hx("#aed581"),
    "Water": hx("#4fc3f7"),
    "Fire": hx("#ff7043"),
    "Poison": hx("#9ccc65"),
    "Shadow": hx("#7e57c2"),
    "Holy": hx("#fff59d"),
    "Undead": hx("#90a4ae"),
}

C_EYE_RED = (235, 40, 40, 255)
C_EYE_YELLOW = (255, 220, 30, 255)
C_EYE_WHITE = (245, 250, 255, 255)
C_EYE_HOLY = (255, 250, 200, 255)


# -----------------------------------------------------------------------------
# Shared primitives (matching generate_clean_monsters.py conventions)
# -----------------------------------------------------------------------------
def create_drop_shadow(draw, cx, cy, rx=16, ry=6, alpha=80):
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(10, 15, 25, alpha))


def normalize_and_center_cell(raw_img, target_min=44, target_max=52, center=(32, 32)):
    bbox = raw_img.getbbox()
    if not bbox:
        return Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    cropped = raw_img.crop(bbox)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    if w == 0 or h == 0:
        return Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    ideal_dim = 48
    scale = ideal_dim / float(max(w, h))
    new_w = max(target_min, min(target_max, int(round(w * scale))))
    new_h = max(target_min, min(target_max, int(round(h * scale))))
    resized = cropped.resize((new_w, new_h), resample=Image.NEAREST)
    cell = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    paste_x = center[0] - new_w // 2
    paste_y = center[1] - new_h // 2
    cell.paste(resized, (paste_x, paste_y), resized)
    return cell


def eyes_for_row(draw, cx, ey, row, c_eye, glow=False):
    """Simple two/one-eye placement matching row facing (0=down,1=left,2=right,3=up)."""
    if row == 3:
        return  # back of head, no face
    if row == 0:
        pts = [(cx - 6, ey), (cx + 6, ey)]
    elif row == 1:
        pts = [(cx - 8, ey)]
    else:
        pts = [(cx + 8, ey)]
    for (ex, eyy) in pts:
        draw.ellipse([ex - 3, eyy - 3, ex + 3, eyy + 3], fill=c_eye)
        if glow:
            draw.ellipse([ex - 5, eyy - 5, ex + 5, eyy + 5], fill=(c_eye[0], c_eye[1], c_eye[2], 60))


def weapon_hand_point(cx, cy, row, reach=12):
    if row == 0:
        return (cx + reach, cy + 4)
    if row == 1:
        return (cx - reach, cy + 4)
    if row == 2:
        return (cx + reach, cy + 4)
    return (cx, cy + reach - 4)


def draw_weapon(draw, cx, cy, row, col, kind, c_main, c_dark):
    """kind: dagger|sword|spear|staff|whip|claws|bow|drum|scythe|none"""
    if kind == "none" or row == 3:
        return
    attack = col == 3
    hx_, hy_ = weapon_hand_point(cx, cy, row)
    side = -1 if row == 1 else 1
    if kind == "dagger":
        if attack:
            draw.polygon([(hx_, hy_), (hx_ + side * 14, hy_ - 10), (hx_ + side * 16, hy_ - 6)], fill=c_main)
        else:
            draw.polygon([(hx_, hy_), (hx_ + side * 7, hy_ - 6), (hx_ + side * 8, hy_ - 4)], fill=c_main)
    elif kind == "sword":
        if attack:
            draw.polygon([(hx_, hy_), (hx_ + side * 16, hy_ - 12), (hx_ + side * 19, hy_ - 8)], fill=c_main)
            draw.arc([hx_ - 18, hy_ - 20, hx_ + 20, hy_ + 6], 160, 340, fill=shade(c_main, 1.3), width=2)
        else:
            draw.line([(hx_, hy_), (hx_ + side * 9, hy_ - 12)], fill=c_main, width=3)
    elif kind == "spear":
        length = 22 if attack else 16
        draw.line([(hx_, hy_ + 6), (hx_ + side * length, hy_ - length)], fill=c_dark, width=2)
        draw.polygon([(hx_ + side * length, hy_ - length), (hx_ + side * (length + 6), hy_ - length - 4),
                      (hx_ + side * (length + 2), hy_ - length + 4)], fill=c_main)
    elif kind == "staff":
        draw.line([(hx_, hy_ + 10), (hx_ + side * 2, hy_ - 20)], fill=c_dark, width=3)
        orb_c = shade(c_main, 1.4)
        draw.ellipse([hx_ + side * 2 - 5, hy_ - 26, hx_ + side * 2 + 5, hy_ - 16], fill=orb_c)
        if attack:
            draw.ellipse([hx_ + side * 2 - 9, hy_ - 30, hx_ + side * 2 + 9, hy_ - 12], fill=(orb_c[0], orb_c[1], orb_c[2], 90))
    elif kind == "whip":
        n = 5 if attack else 3
        px, py = hx_, hy_
        for i in range(n):
            nx = px + side * (7 if i % 2 == 0 else -3)
            ny = py - 5
            draw.line([(px, py), (nx, ny)], fill=c_main, width=2)
            px, py = nx, ny
    elif kind == "claws":
        for i in range(3):
            draw.line([(hx_, hy_ - 4 + i * 4), (hx_ + side * (10 if attack else 6), hy_ - 8 + i * 4)],
                      fill=c_main, width=2)
    elif kind == "bow":
        draw.arc([hx_ - 3, hy_ - 14, hx_ + 3, hy_ + 10], 260, 100, fill=c_dark, width=2)
        if attack:
            draw.line([(hx_ - 2, hy_ - 12), (hx_ + side * 16, hy_ - 2)], fill=(230, 230, 220, 255), width=1)
    elif kind == "drum":
        dx, dy = cx - side * 0, cy + 6
        draw.ellipse([hx_ - 8, hy_ - 6, hx_ + 8, hy_ + 10], fill=c_dark, outline=shade(c_dark, 0.6))
        draw.ellipse([hx_ - 6, hy_ - 4, hx_ + 6, hy_ + 4], fill=c_main)
    elif kind == "scythe":
        draw.line([(hx_, hy_ + 14), (hx_, hy_ - 20)], fill=c_dark, width=3)
        draw.polygon([(hx_, hy_ - 18), (hx_ + side * 18, hy_ - 26), (hx_ + side * 10, hy_ - 10)], fill=c_main)
        if attack:
            draw.arc([cx - 22, cy - 22, cx + 24, cy + 20], 150, 350, fill=(c_main[0], c_main[1], c_main[2], 200), width=3)


# -----------------------------------------------------------------------------
# ARCHETYPE 1: BLOB — floating orb/wisp (dustmote, glasslight mote, rimewind
# sprite, snowveil shade, the unquenched)
# -----------------------------------------------------------------------------
def make_blob(cfg):
    c_body = cfg["body"]
    c_dark = shade(c_body, 0.55)
    c_hl = shade(c_body, 1.45)
    c_core = cfg.get("core", shade(c_body, 1.6))

    def _draw(row, col):
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        cx, cy = 32, 30
        create_drop_shadow(draw, cx, cy + 16, rx=14, ry=5, alpha=60)

        bob = {0: 2, 1: 0, 2: -2, 3: 0}[col]
        rx, ry = 16, 18
        cy2 = cy - bob
        # wispy trailing tendrils
        for i, ang in enumerate(range(0, 360, 60)):
            rad = math.radians(ang + col * 15)
            tx = cx + int((rx + 6) * math.cos(rad))
            ty = cy2 + int((ry + 6) * math.sin(rad) * 0.6)
            draw.line([(cx, cy2), (tx, ty)], fill=(c_dark[0], c_dark[1], c_dark[2], 110), width=2)

        draw.ellipse([cx - rx - 2, cy2 - ry - 2, cx + rx + 2, cy2 + ry + 2], fill=c_dark)
        draw.ellipse([cx - rx, cy2 - ry, cx + rx, cy2 + ry], fill=c_body)
        draw.ellipse([cx - rx + 5, cy2 - ry + 4, cx - 2, cy2 - 2], fill=c_hl)
        draw.ellipse([cx - 8, cy2 - 8, cx + 8, cy2 + 8], fill=c_core)

        if row != 3:
            eyes_for_row(draw, cx, cy2 - 1, row, (20, 20, 25, 255))
        if col == 3:
            draw.ellipse([cx - rx - 6, cy2 - ry - 6, cx + rx + 6, cy2 + ry + 6],
                         fill=(c_core[0], c_core[1], c_core[2], 70))
        return normalize_and_center_cell(img)

    return _draw


# -----------------------------------------------------------------------------
# ARCHETYPE 2: BIPED — flexible humanoid (small/armored/robed/undead/boss)
# -----------------------------------------------------------------------------
def make_biped(cfg):
    c_body = cfg["body"]
    c_body_dark = shade(c_body, 0.55)
    c_outline = shade(c_body, 0.32)
    c_accent = cfg.get("accent", shade(c_body, 1.3))
    c_accent_dark = shade(c_accent, 0.55)
    c_eye = cfg.get("eye", C_EYE_YELLOW)
    scale = cfg.get("scale", 1.0)
    weapon = cfg.get("weapon", "none")
    c_weapon = cfg.get("weapon_color", (200, 210, 225, 255))
    c_weapon_dark = shade(c_weapon, 0.6)
    robe = cfg.get("robe", False)
    hood = cfg.get("hood", False)
    horns = cfg.get("horns", False)
    ears = cfg.get("ears", False)
    skull = cfg.get("skull", False)
    crown = cfg.get("crown", False)
    cape = cfg.get("cape", False)
    glow_eye = cfg.get("glow_eye", False)
    head_color = cfg.get("head_color", c_body)

    def S(v):
        return v * scale

    def _draw(row, col):
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        cx, cy = 32, int(32 - (scale - 1) * 4)
        create_drop_shadow(draw, cx, cy + S(18), rx=S(14), ry=S(5))

        l_off, r_off = 0, 0
        if col == 0:
            l_off, r_off = -2, 2
        elif col == 2:
            l_off, r_off = 2, -2

        # legs
        draw.rectangle([cx - S(8), cy + S(10) + l_off, cx - S(3), cy + S(18)], fill=c_body_dark, outline=c_outline)
        draw.rectangle([cx + S(3), cy + S(10) + r_off, cx + S(8), cy + S(18)], fill=c_body_dark, outline=c_outline)

        # torso / robe
        torso = [(cx - S(9), cy - S(2)), (cx + S(9), cy - S(2)), (cx + S(7), cy + S(12)), (cx - S(7), cy + S(12))]
        draw.polygon(torso, fill=c_body, outline=c_outline)
        if robe:
            draw.polygon([(cx - S(9), cy + S(6)), (cx + S(9), cy + S(6)),
                          (cx + S(12), cy + S(20)), (cx - S(12), cy + S(20))], fill=c_accent, outline=c_accent_dark)
        if cape and row != 0:
            draw.polygon([(cx - S(8), cy - S(2)), (cx + S(8), cy - S(2)),
                          (cx + S(10), cy + S(18)), (cx - S(10), cy + S(18))],
                         fill=(c_accent_dark[0], c_accent_dark[1], c_accent_dark[2], 220))

        # head
        head_bbox = [cx - S(9), cy - S(18), cx + S(9), cy - S(1)]
        if hood:
            draw.polygon([(cx - S(11), cy - S(2)), (cx, cy - S(25)), (cx + S(11), cy - S(2))],
                         fill=c_accent, outline=c_accent_dark)
        draw.ellipse(head_bbox, fill=head_color, outline=c_outline)

        if ears:
            draw.polygon([(cx - S(8), cy - S(10)), (cx - S(19), cy - S(15)), (cx - S(8), cy - S(4))],
                         fill=head_color, outline=c_outline)
            draw.polygon([(cx + S(8), cy - S(10)), (cx + S(19), cy - S(15)), (cx + S(8), cy - S(4))],
                         fill=head_color, outline=c_outline)
        if horns:
            hc = cfg.get("horn_color", (222, 190, 120, 255))
            draw.polygon([(cx - S(5), cy - S(14)), (cx - S(15), cy - S(25)), (cx - S(9), cy - S(8))], fill=hc)
            draw.polygon([(cx + S(5), cy - S(14)), (cx + S(15), cy - S(25)), (cx + S(9), cy - S(8))], fill=hc)
        if crown:
            cc = cfg.get("crown_color", (230, 195, 60, 255))
            draw.polygon([(cx - S(8), cy - S(17)), (cx - S(4), cy - S(24)), (cx, cy - S(17)),
                          (cx + S(4), cy - S(24)), (cx + S(8), cy - S(17))], fill=cc, outline=shade(cc, 0.6))

        if not hood and not skull:
            pass

        if row != 3:
            ey = cy - S(11)
            if skull:
                if row == 0:
                    draw.ellipse([cx - S(6), ey - S(2), cx - S(2), ey + S(3)], fill=(20, 18, 18, 255))
                    draw.ellipse([cx + S(2), ey - S(2), cx + S(6), ey + S(3)], fill=(20, 18, 18, 255))
                elif row == 1:
                    draw.ellipse([cx - S(7), ey - S(2), cx - S(3), ey + S(3)], fill=(20, 18, 18, 255))
                else:
                    draw.ellipse([cx + S(3), ey - S(2), cx + S(7), ey + S(3)], fill=(20, 18, 18, 255))
            eyes_for_row(draw, cx, ey, row, c_eye, glow=glow_eye)

        draw_weapon(draw, cx, cy, row, col, weapon, c_weapon, c_weapon_dark)
        return normalize_and_center_cell(img)

    return _draw


# -----------------------------------------------------------------------------
# ARCHETYPE 3: QUAD — four-legged / shelled / serpentine creatures
# -----------------------------------------------------------------------------
def make_quad(cfg):
    c_body = cfg["body"]
    c_dark = shade(c_body, 0.55)
    c_outline = shade(c_body, 0.3)
    c_belly = cfg.get("belly", shade(c_body, 1.3))
    c_eye = cfg.get("eye", (20, 20, 25, 255))
    scale = cfg.get("scale", 1.0)
    shell = cfg.get("shell", False)
    serpent = cfg.get("serpent", False)
    low = cfg.get("low", False)  # near-ground creeper

    def S(v):
        return v * scale

    def _draw(row, col):
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        cx, cy = 32, 36 if low else 34
        create_drop_shadow(draw, cx, cy + S(12), rx=S(18), ry=S(6))

        bob = {0: 1, 1: -1, 2: 1, 3: -1}[col]

        if serpent:
            # long sinuous body
            wob = {0: 0, 1: -4, 2: 4, 3: 0}[col]
            pts = [(cx - S(20), cy + S(4)), (cx - S(8) + wob, cy - S(4)), (cx + S(6) - wob, cy + S(2)),
                   (cx + S(18), cy - S(2))]
            draw.line(pts, fill=c_dark, width=int(S(14)), joint="curve")
            draw.line(pts, fill=c_body, width=int(S(10)), joint="curve")
            hx_, hy_ = pts[-1]
            draw.ellipse([hx_ - S(2), hy_ - S(6), hx_ + S(10), hy_ + S(6)], fill=c_body, outline=c_outline)
            eyes_for_row(draw, hx_ + S(3), hy_ - S(1), 0 if row in (0, 3) else row, c_eye)
        else:
            body_bbox = [cx - S(16), cy - S(8) + bob, cx + S(16), cy + S(10) + bob]
            draw.ellipse([body_bbox[0] - 2, body_bbox[1] - 2, body_bbox[2] + 2, body_bbox[3] + 2], fill=c_dark)
            draw.ellipse(body_bbox, fill=c_body)
            if shell:
                draw.ellipse([cx - S(14), cy - S(14) + bob, cx + S(14), cy + S(4) + bob], fill=c_dark, outline=c_outline)
                for lx in range(-10, 11, 8):
                    draw.line([(cx + S(lx), cy - S(12) + bob), (cx + S(lx), cy + S(2) + bob)],
                              fill=shade(c_dark, 1.3), width=1)
            else:
                draw.ellipse([cx - S(12), cy - S(4) + bob, cx + S(12), cy + S(9) + bob], fill=c_belly)

            # legs
            leg_positions = [(-12, 6), (-4, 9), (4, 9), (12, 6)]
            for i, (lx, ly) in enumerate(leg_positions):
                leg_bob = bob if i % 2 == 0 else -bob
                draw.rectangle([cx + S(lx) - S(2), cy + S(ly) + bob, cx + S(lx) + S(2), cy + S(ly) + S(8) + leg_bob],
                               fill=c_dark)

            # head
            if row == 0:
                hcx, hcy = cx, cy - S(6) + bob
            elif row == 1:
                hcx, hcy = cx - S(14), cy - S(4) + bob
            elif row == 2:
                hcx, hcy = cx + S(14), cy - S(4) + bob
            else:
                hcx, hcy = cx, cy - S(10) + bob
            draw.ellipse([hcx - S(6), hcy - S(6), hcx + S(6), hcy + S(6)], fill=c_body, outline=c_outline)
            if row != 3:
                eyes_for_row(draw, hcx, hcy - S(1), 0 if row == 0 else row, c_eye)

            if cfg.get("wings") and row != 3:
                wc = cfg.get("wing_color", shade(c_body, 1.4))
                flap = 6 if col in (0, 2) else 2
                draw.polygon([(cx - S(10), cy - S(6) + bob), (cx - S(24), cy - S(14) - flap + bob),
                              (cx - S(8), cy - S(2) + bob)], fill=wc)
                draw.polygon([(cx + S(10), cy - S(6) + bob), (cx + S(24), cy - S(14) - flap + bob),
                              (cx + S(8), cy - S(2) + bob)], fill=wc)

        if col == 3:
            draw.ellipse([cx - S(24), cy - S(18), cx + S(24), cy + S(14)], fill=(c_dark[0], c_dark[1], c_dark[2], 40))

        return normalize_and_center_cell(img)

    return _draw


# -----------------------------------------------------------------------------
# ARCHETYPE 4: FLYER — winged insect/bird hovering above ground
# -----------------------------------------------------------------------------
def make_flyer(cfg):
    c_body = cfg["body"]
    c_dark = shade(c_body, 0.5)
    c_wing = cfg.get("wing", (255, 255, 255, 160))
    c_eye = cfg.get("eye", (20, 20, 25, 255))
    wing_pairs = cfg.get("wing_pairs", 1)

    def _draw(row, col):
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        cx, cy = 32, 30
        create_drop_shadow(draw, cx, cy + 16, rx=12, ry=4, alpha=55)

        flap = {0: 10, 1: 4, 2: 14, 3: 6}[col]
        for pair in range(wing_pairs):
            dy = pair * 5
            draw.polygon([(cx - 4, cy - dy), (cx - 22, cy - flap - dy), (cx - 6, cy + 6 - dy)], fill=c_wing)
            draw.polygon([(cx + 4, cy - dy), (cx + 22, cy - flap - dy), (cx + 6, cy + 6 - dy)], fill=c_wing)

        draw.ellipse([cx - 10, cy - 6, cx + 10, cy + 10], fill=c_dark)
        draw.ellipse([cx - 9, cy - 7, cx + 9, cy + 8], fill=c_body)
        # head
        if row == 0:
            hcx, hcy = cx, cy - 8
        elif row == 1:
            hcx, hcy = cx - 8, cy - 6
        elif row == 2:
            hcx, hcy = cx + 8, cy - 6
        else:
            hcx, hcy = cx, cy - 8
        draw.ellipse([hcx - 5, hcy - 5, hcx + 5, hcy + 5], fill=c_body, outline=c_dark)
        if row != 3:
            eyes_for_row(draw, hcx, hcy - 1, 0 if row == 0 else row, c_eye)

        if row == 0 and col == 3:  # dive/sting pose
            draw.line([(cx, cy + 8), (cx, cy + 18)], fill=c_dark, width=2)

        return normalize_and_center_cell(img)

    return _draw


# -----------------------------------------------------------------------------
# ARCHETYPE 5: PLANT — rooted humanoid/mushroom/branch creature
# -----------------------------------------------------------------------------
def make_plant(cfg):
    c_body = cfg["body"]
    c_dark = shade(c_body, 0.55)
    c_outline = shade(c_body, 0.3)
    c_accent = cfg.get("accent", shade(c_body, 1.4))
    c_eye = cfg.get("eye", (255, 210, 90, 255))
    cap = cfg.get("cap", False)  # mushroom cap silhouette
    overhead = cfg.get("overhead", False)  # hangs from above (weeping bough)
    teeth = cfg.get("teeth", False)

    def _draw(row, col):
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        cx, cy = 32, 22 if overhead else 32
        create_drop_shadow(draw, cx, 52, rx=14, ry=5, alpha=70)

        sway = {0: -2, 1: 0, 2: 2, 3: 0}[col]

        if overhead:
            draw.line([(cx, 0), (cx, cy - 6)], fill=c_dark, width=4)
            draw.ellipse([cx - 12, cy - 10, cx + 12, cy + 10], fill=c_body, outline=c_outline)
            draw.ellipse([cx - 6 + sway, cy - 4, cx + 6 + sway, cy + 6], fill=c_accent)
            if row != 3:
                eyes_for_row(draw, cx, cy + 1, row, c_eye)
        else:
            # stalk / trunk
            draw.polygon([(cx - 6 + sway, cy + 16), (cx + 6 + sway, cy + 16), (cx + 4, cy - 4), (cx - 4, cy - 4)],
                         fill=c_dark, outline=c_outline)
            if cap:
                draw.ellipse([cx - 16, cy - 22, cx + 16, cy - 2], fill=c_body, outline=c_outline)
                draw.ellipse([cx - 12, cy - 19, cx + 12, cy - 9], fill=c_accent)
            else:
                draw.ellipse([cx - 11 + sway, cy - 22, cx + 11 + sway, cy - 2], fill=c_body, outline=c_outline)
                for ang in (-40, 0, 40):
                    rad = math.radians(ang)
                    tx = cx + sway + int(14 * math.sin(rad))
                    ty = (cy - 12) - int(10 * math.cos(rad))
                    draw.line([(cx + sway, cy - 12), (tx, ty)], fill=c_accent, width=2)

            # arms/branches
            arm_reach = 14 if col == 3 else 9
            draw.line([(cx - 8 + sway, cy - 6), (cx - arm_reach - 8 + sway, cy - 10)], fill=c_dark, width=3)
            draw.line([(cx + 8 + sway, cy - 6), (cx + arm_reach + 8 + sway, cy - 10)], fill=c_dark, width=3)

            if row != 3:
                ey = cy - 14
                if teeth and (col == 3 or row == 0):
                    draw.polygon([(cx - 5, ey + 6), (cx + 5, ey + 6), (cx, ey + 13)], fill=(30, 15, 15, 255))
                    for tx_ in range(-4, 5, 2):
                        draw.line([(cx + tx_, ey + 6), (cx + tx_, ey + 9)], fill=(240, 235, 220, 255), width=1)
                eyes_for_row(draw, cx + sway, ey, row, c_eye)

        return normalize_and_center_cell(img)

    return _draw


# -----------------------------------------------------------------------------
# ARCHETYPE 6: CONSTRUCT — golem/automaton/crystalline boxy body
# -----------------------------------------------------------------------------
def make_construct(cfg):
    c_body = cfg["body"]
    c_dark = shade(c_body, 0.5)
    c_outline = shade(c_body, 0.28)
    c_core = cfg.get("core", (255, 210, 90, 255))
    scale = cfg.get("scale", 1.0)
    crystal = cfg.get("crystal", False)

    def S(v):
        return v * scale

    def _draw(row, col):
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        cx, cy = 32, int(32 - (scale - 1) * 3)
        create_drop_shadow(draw, cx, cy + S(18), rx=S(16), ry=S(6))

        thud = {0: 0, 1: -1, 2: 1, 3: 0}[col]

        if crystal:
            pts = [(cx, cy - S(20)), (cx - S(12), cy - S(4) + thud), (cx - S(6), cy + S(16)),
                   (cx + S(6), cy + S(16)), (cx + S(12), cy - S(4) + thud)]
            draw.polygon(pts, fill=c_dark, outline=c_outline)
            draw.polygon([(cx, cy - S(20)), (cx - S(6), cy - S(2) + thud), (cx, cy + S(6)), (cx + S(6), cy - S(2) + thud)],
                         fill=c_body)
            draw.ellipse([cx - S(4), cy - S(4), cx + S(4), cy + S(4)], fill=c_core)
            if col == 3:
                draw.ellipse([cx - S(10), cy - S(10), cx + S(10), cy + S(10)], fill=(c_core[0], c_core[1], c_core[2], 70))
        else:
            # legs
            draw.rectangle([cx - S(9), cy + S(9) + thud, cx - S(3), cy + S(19)], fill=c_dark, outline=c_outline)
            draw.rectangle([cx + S(3), cy + S(9) - thud, cx + S(9), cy + S(19)], fill=c_dark, outline=c_outline)
            # torso block
            draw.rectangle([cx - S(11), cy - S(8), cx + S(11), cy + S(11)], fill=c_body, outline=c_outline)
            draw.rectangle([cx - S(7), cy - S(4), cx + S(7), cy + S(4)], fill=c_dark)
            draw.ellipse([cx - S(4), cy - S(2), cx + S(4), cy + S(6)], fill=c_core)
            # head
            draw.rectangle([cx - S(7), cy - S(18), cx + S(7), cy - S(7)], fill=c_body, outline=c_outline)
            if row != 3:
                if row == 0:
                    draw.rectangle([cx - S(5), cy - S(14), cx - S(1), cy - S(11)], fill=c_core)
                    draw.rectangle([cx + S(1), cy - S(14), cx + S(5), cy - S(11)], fill=c_core)
                elif row == 1:
                    draw.rectangle([cx - S(6), cy - S(14), cx - S(2), cy - S(11)], fill=c_core)
                else:
                    draw.rectangle([cx + S(2), cy - S(14), cx + S(6), cy - S(11)], fill=c_core)
            # arms
            arm_y = cy - S(2)
            reach = S(16) if col == 3 else S(11)
            draw.rectangle([cx - reach, arm_y - S(3), cx - S(11), arm_y + S(3)], fill=c_dark)
            draw.rectangle([cx + S(11), arm_y - S(3), cx + reach, arm_y + S(3)], fill=c_dark)

        return normalize_and_center_cell(img)

    return _draw


# -----------------------------------------------------------------------------
# BOSS = BIPED with bigger scale + crown/cape defaults (kept as a thin wrapper
# so bosses are visually distinct — larger silhouette, crown, cape, glow eyes)
# -----------------------------------------------------------------------------
def make_boss(cfg):
    boss_cfg = dict(cfg)
    boss_cfg.setdefault("scale", 1.35)
    boss_cfg.setdefault("crown", True)
    boss_cfg.setdefault("cape", True)
    boss_cfg.setdefault("glow_eye", True)
    return make_biped(boss_cfg)


# -----------------------------------------------------------------------------
# 48 MONSTER CONFIGS — grouped by zone / manifest order
# -----------------------------------------------------------------------------
def E(name):
    return ELEMENT_COLOR[name]


MONSTERS = {}

# --- Gatewatch Commons ---
MONSTERS["dustmote_wisp_ff.png"] = make_blob({"body": E("Wind")})
MONSTERS["gutter_ratkin_ff.png"] = make_biped({
    "body": E("Neutral"), "scale": 0.85, "ears": True, "weapon": "dagger",
    "weapon_color": (190, 195, 205, 255), "eye": C_EYE_RED,
})
MONSTERS["thatch_beetle_ff.png"] = make_quad({"body": E("Earth"), "scale": 0.85, "shell": True})
MONSTERS["straw_effigy_ff.png"] = make_plant({
    "body": hx("#c9a24a"), "accent": E("Fire"), "eye": (255, 90, 40, 255),
})

# --- Whispering Meadows ---
MONSTERS["bramblehop_ff.png"] = make_quad({"body": E("Earth"), "scale": 0.9, "belly": hx("#c8b28a")})
MONSTERS["hornhaste_wasp_ff.png"] = make_flyer({"body": hx("#d8c93a"), "wing": (240, 250, 255, 150)})
MONSTERS["mossback_tortin_ff.png"] = make_quad({"body": E("Earth"), "scale": 1.15, "shell": True})
MONSTERS["fen_lurker_ff.png"] = make_biped({
    "body": hx("#3f6b57"), "scale": 1.0, "weapon": "claws", "weapon_color": hx("#2c4a3c"), "eye": C_EYE_WHITE,
})
MONSTERS["rot_capling_ff.png"] = make_plant({"body": hx("#c46a3a"), "accent": E("Poison"), "cap": True})
MONSTERS["snagtooth_warchanter_ff.png"] = make_biped({
    "body": hx("#7a9450"), "scale": 1.1, "weapon": "drum", "weapon_color": hx("#8a5a30"),
    "accent": hx("#5a4028"), "ears": True, "eye": C_EYE_YELLOW,
})
MONSTERS["grovewarden_thistle_ff.png"] = make_plant({
    "body": E("Earth"), "accent": hx("#4a6a3a"), "horns": False, "eye": (150, 255, 170, 255),
})
MONSTERS["ordwin_palisade_tyrant_ff.png"] = make_boss({
    "body": hx("#8a7a5a"), "accent": hx("#4a4038"), "weapon": "sword",
    "weapon_color": (210, 220, 235, 255), "eye": C_EYE_RED, "crown_color": (180, 150, 60, 255),
})

# --- Sunken Sanctum ---
MONSTERS["brinemaw_eel_ff.png"] = make_quad({"body": E("Water"), "serpent": True, "eye": C_EYE_YELLOW})
MONSTERS["silt_creeper_ff.png"] = make_quad({"body": hx("#6b7a4a"), "low": True, "belly": E("Poison"), "scale": 0.85})
MONSTERS["glasslight_mote_ff.png"] = make_blob({"body": E("Holy"), "core": (255, 255, 240, 255)})
MONSTERS["reliquary_husk_ff.png"] = make_biped({
    "body": hx("#8a8878"), "scale": 1.0, "robe": True, "accent": hx("#5a5848"),
    "skull": False, "eye": (150, 200, 210, 255),
})
MONSTERS["coralbound_acolyte_ff.png"] = make_biped({
    "body": hx("#e79ec7"), "robe": True, "hood": True, "accent": E("Water"), "weapon": "staff",
    "weapon_color": hx("#3a8bb0"), "eye": C_EYE_WHITE,
})
MONSTERS["warden_of_the_nave_ff.png"] = make_biped({
    "body": hx("#4a5560"), "scale": 1.25, "cape": True, "accent": hx("#20303a"),
    "weapon": "spear", "weapon_color": (200, 210, 225, 255), "eye": (60, 120, 200, 255), "glow_eye": True,
})
MONSTERS["pale_choirmaster_ff.png"] = make_biped({
    "body": hx("#f5efe0"), "robe": True, "hood": True, "accent": E("Holy"), "weapon": "none",
    "eye": (255, 250, 210, 255), "glow_eye": True,
})
MONSTERS["hallowdeep_warden_ff.png"] = make_boss({
    "body": hx("#2e5f78"), "accent": hx("#123244"), "weapon": "spear",
    "weapon_color": (170, 210, 230, 255), "eye": (120, 220, 255, 255), "crown_color": (120, 190, 210, 255),
})

# --- Obsidian Spire ---
MONSTERS["emberglass_shard_ff.png"] = make_construct({"body": hx("#2a1810"), "core": E("Fire"), "crystal": True})
MONSTERS["ashfall_harrier_ff.png"] = make_flyer({"body": hx("#5a4a48"), "wing": (120, 90, 80, 200), "eye": C_EYE_RED})
MONSTERS["magma_hulk_ff.png"] = make_construct({"body": hx("#3a2a24"), "core": E("Fire"), "scale": 1.3})
MONSTERS["soot_revenant_ff.png"] = make_biped({
    "body": hx("#3a3632"), "scale": 1.0, "skull": True, "eye": (255, 130, 40, 255), "glow_eye": True,
})
MONSTERS["forgewrought_sentinel_ff.png"] = make_construct({"body": E("Earth"), "core": hx("#d8a840"), "scale": 1.1})
MONSTERS["pyrelash_imp_ff.png"] = make_biped({
    "body": E("Fire"), "scale": 0.85, "horns": True, "weapon": "whip",
    "weapon_color": (255, 160, 40, 255), "eye": C_EYE_RED,
})
MONSTERS["bellowmaster_grukk_ff.png"] = make_biped({
    "body": hx("#6a4a3a"), "scale": 1.25, "weapon": "sword", "weapon_color": hx("#c04020"),
    "accent": hx("#3a2418"), "eye": C_EYE_RED, "horns": True,
})
MONSTERS["the_unquenched_ff.png"] = make_blob({"body": E("Fire"), "core": (255, 250, 200, 255)})
MONSTERS["vashkar_spire_crown_ff.png"] = make_boss({
    "body": hx("#241414"), "accent": hx("#120a0a"), "weapon": "scythe",
    "weapon_color": (255, 140, 40, 255), "eye": (255, 60, 20, 255), "crown_color": E("Fire"), "horns": True,
})

# --- Glacial Chasm ---
MONSTERS["rimewind_sprite_ff.png"] = make_blob({"body": (220, 240, 255, 255), "core": (255, 255, 255, 255)})
MONSTERS["hoarfrost_stalker_ff.png"] = make_biped({
    "body": (225, 240, 250, 255), "scale": 1.05, "weapon": "claws", "weapon_color": (200, 225, 240, 255),
    "eye": (150, 220, 255, 255), "glow_eye": True,
})
MONSTERS["frozen_penitent_ff.png"] = make_biped({
    "body": hx("#b7d0dc"), "scale": 1.0, "robe": True, "accent": hx("#7a95a2"), "eye": (200, 235, 255, 255),
})
MONSTERS["glacier_drake_whelp_ff.png"] = make_quad({
    "body": hx("#2f6fae"), "scale": 0.85, "wings": True, "wing_color": (150, 210, 250, 200), "eye": C_EYE_YELLOW,
})
MONSTERS["snowveil_shade_ff.png"] = make_blob({"body": E("Shadow"), "core": (40, 20, 60, 255)})
MONSTERS["aurora_seraphon_ff.png"] = make_flyer({"body": E("Holy"), "wing": (200, 240, 255, 170), "wing_pairs": 3})
MONSTERS["permafrost_lich_ff.png"] = make_biped({
    "body": hx("#8ea8b0"), "robe": True, "hood": True, "accent": hx("#3a5560"), "weapon": "staff",
    "weapon_color": (120, 210, 240, 255), "eye": (140, 230, 255, 255), "glow_eye": True,
})
MONSTERS["statuary_colossus_ff.png"] = make_construct({"body": hx("#9fb8c4"), "core": (140, 220, 255, 255), "scale": 1.35})
MONSTERS["the_vault_keeper_ff.png"] = make_biped({
    "body": hx("#5a6a72"), "scale": 1.15, "cape": True, "weapon": "sword",
    "weapon_color": (200, 220, 235, 255), "eye": (170, 230, 255, 255), "glow_eye": True,
})
MONSTERS["sylveth_silent_thaw_ff.png"] = make_boss({
    "body": (235, 248, 255, 255), "accent": hx("#4a7a95"), "weapon": "staff",
    "weapon_color": (150, 225, 255, 255), "eye": (100, 200, 255, 255), "crown_color": (210, 240, 255, 255),
})

# --- Umbral Rootways ---
MONSTERS["nethergate_creeper_ff.png"] = make_quad({"body": hx("#3a2c4a"), "low": True, "belly": E("Shadow"), "scale": 0.9})
MONSTERS["weeping_bough_ff.png"] = make_plant({"body": hx("#5a3c28"), "accent": E("Poison"), "overhead": True})
MONSTERS["umbral_houndkin_ff.png"] = make_quad({"body": hx("#241c30"), "belly": E("Shadow"), "eye": (200, 40, 220, 255)})
MONSTERS["sanguine_thorncaller_ff.png"] = make_biped({
    "body": hx("#7a1f2a"), "robe": True, "accent": hx("#2a1418"), "weapon": "none", "eye": E("Shadow"),
})
MONSTERS["hollow_penitent_choir_ff.png"] = make_biped({
    "body": hx("#c8c2b0"), "robe": True, "hood": True, "accent": hx("#8a8270"), "eye": (30, 25, 25, 255),
})
MONSTERS["rootfang_devourer_ff.png"] = make_plant({"body": hx("#3a2818"), "accent": E("Poison"), "teeth": True})
MONSTERS["abyssal_heraldon_ff.png"] = make_biped({
    "body": hx("#2c2438"), "scale": 1.15, "horns": True, "cape": True, "weapon": "spear",
    "weapon_color": (150, 120, 200, 255), "eye": (220, 60, 220, 255), "glow_eye": True,
})
MONSTERS["thorncradle_warden_ff.png"] = make_biped({
    "body": hx("#403050"), "scale": 1.2, "weapon": "sword", "weapon_color": (170, 140, 210, 255),
    "accent": hx("#20182c"), "eye": E("Shadow"), "glow_eye": True,
})
MONSTERS["the_pale_apostate_ff.png"] = make_biped({
    "body": hx("#f0ece0"), "robe": True, "hood": True, "accent": hx("#c9c0a0"), "weapon": "staff",
    "weapon_color": E("Holy"), "eye": (255, 250, 210, 255), "glow_eye": True,
})


# -----------------------------------------------------------------------------
# SHEET GENERATION + VERIFICATION
# -----------------------------------------------------------------------------
def generate_all_new_monsters():
    print(f"=== TASK B: Generating {len(MONSTERS)} new monster sprite sheets ===")
    for filename, drawer in MONSTERS.items():
        sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
        for row in range(4):
            for col in range(4):
                cell_img = drawer(row, col)
                sheet.paste(cell_img, (col * 64, row * 64))
        for d in TARGET_DIRS:
            os.makedirs(d, exist_ok=True)
            out_path = os.path.join(d, filename)
            sheet.save(out_path, "PNG")
        print(f"  Saved: {filename}")


def verify():
    print("\n=== Verification ===")
    expected = set(RENAMES.values()) | set(MONSTERS.keys())
    ok = True
    for d in TARGET_DIRS:
        for filename in sorted(expected):
            path = os.path.join(d, filename)
            if not os.path.exists(path):
                print(f"  MISSING: {path}")
                ok = False
                continue
            im = Image.open(path)
            if im.size != (256, 256) or im.mode != "RGBA":
                print(f"  BAD SPEC: {path} -> {im.size} {im.mode}")
                ok = False
    print(f"Total expected sheets per dir: {len(expected)} (6 renamed + {len(MONSTERS)} new = 54)")
    print("ALL OK" if ok else "SOME FILES FAILED VERIFICATION")
    return ok


if __name__ == "__main__":
    do_renames()
    generate_all_new_monsters()
    verify()
