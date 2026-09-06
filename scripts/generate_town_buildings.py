"""
generate_town_buildings.py

Higher-quality isometric kingdom-town buildings & curtain walls for Aethelgard.
Follows the Pillow conventions of generate_env_assets.py (iso left/right wall
diamonds, terracotta/slate roofs, timber beams, soft oval ground shadow) and
saves to BOTH assets/tiles_ff/ and web/assets/tiles_ff/.
"""

import os
from PIL import Image, ImageDraw

ROOT = r"D:\ai-studio\Zaggers"
TARGET_DIRS = [
    os.path.join(ROOT, "assets", "tiles_ff"),
    os.path.join(ROOT, "web", "assets", "tiles_ff"),
]


def save_asset(img, name):
    for d in TARGET_DIRS:
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, name)
        img.save(path, "PNG")
        print(f"  Saved: {path} ({img.size[0]}x{img.size[1]})")


def draw_shadow(draw, center, rx, ry, alpha=110):
    cx, cy = center
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(10, 15, 25, alpha))


def shade(c, f):
    r, g, b, a = c if len(c) == 4 else (*c, 255)
    if f <= 1.0:
        return (int(r * f), int(g * f), int(b * f), a)
    t = f - 1.0
    return (int(r + (255 - r) * t), int(g + (255 - g) * t), int(b + (255 - b) * t), a)


# Warm cobble-town palette
STONE_L = (110, 95, 80, 255)
STONE_R = (155, 138, 118, 255)
STONE_DK = (60, 50, 40, 255)
STONE_PALE_L = (150, 145, 135, 255)
STONE_PALE_R = (195, 188, 175, 255)
STONE_PALE_DK = (90, 85, 75, 255)
TIMBER = (70, 55, 42, 255)
TIMBER_R = (85, 68, 52, 255)
ROOF_L = (160, 55, 45, 255)
ROOF_R = (210, 80, 65, 255)
ROOF_DK = (90, 25, 20, 255)
SLATE_L = (70, 78, 92, 255)
SLATE_R = (100, 110, 128, 255)
SLATE_DK = (40, 45, 55, 255)
ASH_L = (70, 62, 55, 255)
ASH_R = (105, 95, 85, 255)
ASH_DK = (40, 35, 30, 255)
DOOR = (75, 45, 25, 255)
DOOR_DK = (40, 20, 10, 255)
GOLD = (220, 180, 50, 255)
WIN_GLOW = (255, 220, 110, 255)
WIN_BLUE = (140, 190, 230, 255)
WIN_STAIN = (180, 120, 220, 255)


def iso_box(draw, cx, bottom_y, half_w, wall_h, c_l, c_r, c_dk, timber=True):
    """Draw a classic iso building body. Returns roof attachment y (top of walls)."""
    top_y = bottom_y - wall_h
    mid_y = bottom_y - wall_h // 2
    left = [(cx, bottom_y), (cx - half_w, bottom_y - half_w // 2),
            (cx - half_w, top_y - half_w // 2), (cx, top_y)]
    right = [(cx, bottom_y), (cx + half_w, bottom_y - half_w // 2),
             (cx + half_w, top_y - half_w // 2), (cx, top_y)]
    draw.polygon(left, fill=c_l, outline=c_dk)
    draw.polygon(right, fill=c_r, outline=c_dk)
    if timber:
        # Vertical beams
        lx = cx - half_w // 2
        rx = cx + half_w // 2
        draw.line([(lx, bottom_y - half_w // 4), (lx, top_y - half_w // 4)], fill=shade(c_l, 0.55), width=3)
        draw.line([(rx, bottom_y - half_w // 4), (rx, top_y - half_w // 4)], fill=shade(c_r, 0.55), width=3)
        # Horizontal crossbeams
        draw.line([(cx - half_w, mid_y - half_w // 2), (cx, mid_y)], fill=shade(c_l, 0.55), width=2)
        draw.line([(cx, mid_y), (cx + half_w, mid_y - half_w // 2)], fill=shade(c_r, 0.55), width=2)
    return top_y


def iso_roof(draw, cx, ridge_attach_y, half_w, roof_rise, c_l, c_r, c_dk, shingles=True):
    """Gabled iso roof sitting on wall tops. ridge_attach_y is the wall peak (cx,top_y)."""
    # Roof diamond: peak above, eaves out past walls
    peak_y = ridge_attach_y - roof_rise
    eaves_drop = half_w // 5
    left = [
        (cx, ridge_attach_y + eaves_drop),
        (cx - half_w - 8, ridge_attach_y - half_w // 2 + eaves_drop + 4),
        (cx - half_w - 8, peak_y + 8),
        (cx, peak_y),
    ]
    right = [
        (cx, ridge_attach_y + eaves_drop),
        (cx + half_w + 8, ridge_attach_y - half_w // 2 + eaves_drop + 4),
        (cx + half_w + 8, peak_y + 8),
        (cx, peak_y),
    ]
    draw.polygon(left, fill=c_l, outline=c_dk)
    draw.polygon(right, fill=c_r, outline=c_dk)
    if shingles:
        for i in range(3, roof_rise, 5):
            y = peak_y + i
            t = i / max(roof_rise, 1)
            span = int((half_w + 8) * t)
            draw.line([(cx, y), (cx - span, y + span // 2)], fill=shade(c_l, 0.7), width=1)
            draw.line([(cx, y), (cx + span, y + span // 2)], fill=shade(c_r, 1.15), width=1)
    return peak_y


def iso_door(draw, cx, bottom_y, half_w, side="right", tall=18, wide=12):
    """Door on left or right iso face."""
    if side == "right":
        ox = cx + half_w // 3
        base = bottom_y - half_w // 6
        door = [
            (ox - wide // 3, base),
            (ox + wide // 2, base - wide // 3),
            (ox + wide // 2, base - tall - wide // 3),
            (ox - wide // 3, base - tall),
        ]
        draw.polygon(door, fill=DOOR, outline=DOOR_DK)
        draw.ellipse([ox + 2, base - tall // 2 - 2, ox + 5, base - tall // 2 + 1], fill=GOLD)
    else:
        ox = cx - half_w // 3
        base = bottom_y - half_w // 6
        door = [
            (ox + wide // 3, base),
            (ox - wide // 2, base - wide // 3),
            (ox - wide // 2, base - tall - wide // 3),
            (ox + wide // 3, base - tall),
        ]
        draw.polygon(door, fill=DOOR, outline=DOOR_DK)
        draw.ellipse([ox - 5, base - tall // 2 - 2, ox - 2, base - tall // 2 + 1], fill=GOLD)


def iso_window(draw, cx, bottom_y, half_w, side="left", glow=WIN_GLOW, y_off=0):
    """Small glowing window on iso face."""
    if side == "left":
        ox = cx - half_w // 2
        by = bottom_y - half_w // 3 - 8 + y_off
        win = [(ox - 6, by), (ox + 6, by + 6), (ox + 6, by - 8), (ox - 6, by - 14)]
        draw.polygon(win, fill=glow, outline=STONE_DK)
        draw.line([(ox, by + 3), (ox, by - 11)], fill=shade(glow, 0.45), width=1)
        draw.line([(ox - 6, by - 4), (ox + 6, by + 2)], fill=shade(glow, 0.45), width=1)
    else:
        ox = cx + half_w // 2
        by = bottom_y - half_w // 3 - 8 + y_off
        win = [(ox + 6, by), (ox - 6, by + 6), (ox - 6, by - 8), (ox + 6, by - 14)]
        draw.polygon(win, fill=glow, outline=STONE_DK)
        draw.line([(ox, by + 3), (ox, by - 11)], fill=shade(glow, 0.45), width=1)
        draw.line([(ox + 6, by - 4), (ox - 6, by + 2)], fill=shade(glow, 0.45), width=1)


def chimney(draw, cx, peak_y, offset_x=-18, soot=False):
    base_y = peak_y + 16
    cl = ASH_L if soot else (80, 85, 95, 255)
    cr = ASH_R if soot else (110, 115, 125, 255)
    cdk = ASH_DK if soot else (40, 45, 55, 255)
    x = cx + offset_x
    left = [(x, base_y), (x + 8, base_y - 4), (x + 8, peak_y - 6), (x, peak_y - 2)]
    right = [(x + 8, base_y - 4), (x + 14, base_y - 1), (x + 14, peak_y - 3), (x + 8, peak_y - 6)]
    draw.polygon(left, fill=cl, outline=cdk)
    draw.polygon(right, fill=cr, outline=cdk)
    # Smoke
    draw.ellipse([x + 4, peak_y - 14, x + 12, peak_y - 6], fill=(220, 225, 235, 160))
    draw.ellipse([x + 8, peak_y - 20, x + 18, peak_y - 12], fill=(240, 245, 250, 180))
    if soot:
        draw.ellipse([x + 2, peak_y - 10, x + 10, peak_y - 4], fill=(40, 40, 45, 120))


# =============================================================================
# 1. Curtain wall segment
# =============================================================================
def create_wall_curtain():
    w, h = 96, 128
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    ax, ay = 48, 116
    draw_shadow(draw, (ax, ay), 42, 14, 120)

    # Iso curtain wall: long diamond faces, crenellations on top
    wall_h = 70
    half = 40
    top = ay - wall_h
    left = [(ax, ay), (ax - half, ay - 20), (ax - half, top - 20), (ax, top)]
    right = [(ax, ay), (ax + half, ay - 20), (ax + half, top - 20), (ax, top)]
    draw.polygon(left, fill=(95, 90, 82, 255), outline=(50, 48, 42, 255))
    draw.polygon(right, fill=(135, 128, 115, 255), outline=(60, 55, 48, 255))

    # Stone course lines
    for i in range(1, 5):
        y = ay - i * 14
        draw.line([(ax - half + 2, y - 20), (ax - 2, y)], fill=(70, 66, 58, 255), width=1)
        draw.line([(ax + 2, y), (ax + half - 2, y - 20)], fill=(100, 95, 85, 255), width=1)

    # Vertical mortar seams
    for sx in (-20, 0, 20):
        if sx < 0:
            draw.line([(ax + sx, ay - 8), (ax + sx, top - 12)], fill=(65, 60, 52, 180), width=1)
        elif sx > 0:
            draw.line([(ax + sx, ay - 8), (ax + sx, top - 12)], fill=(110, 104, 92, 180), width=1)

    # Crenellations / battlements
    for i, ox in enumerate([-28, -10, 10, 28]):
        ctop = top - 18
        if ox <= 0:
            merlon = [
                (ax + ox - 6, top - 8),
                (ax + ox + 6, top - 2),
                (ax + ox + 6, ctop - 2),
                (ax + ox - 6, ctop - 8),
            ]
            draw.polygon(merlon, fill=(105, 100, 90, 255), outline=(50, 48, 42, 255))
        else:
            merlon = [
                (ax + ox + 6, top - 8),
                (ax + ox - 6, top - 2),
                (ax + ox - 6, ctop - 2),
                (ax + ox + 6, ctop - 8),
            ]
            draw.polygon(merlon, fill=(145, 138, 125, 255), outline=(60, 55, 48, 255))

    # Arrow slit
    slit = [(ax - 14, ay - 40), (ax - 10, ay - 38), (ax - 10, ay - 52), (ax - 14, ay - 54)]
    draw.polygon(slit, fill=(25, 22, 20, 255))
    slit2 = [(ax + 14, ay - 40), (ax + 10, ay - 38), (ax + 10, ay - 52), (ax + 14, ay - 54)]
    draw.polygon(slit2, fill=(25, 22, 20, 255))

    return img


# =============================================================================
# 2. Corner bastion / tower stub
# =============================================================================
def create_wall_corner():
    w, h = 96, 144
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    ax, ay = 48, 132
    draw_shadow(draw, (ax, ay), 36, 14, 120)

    # Squatter roundish bastion built as iso box with thicker walls
    half = 32
    wall_h = 78
    top = iso_box(draw, ax, ay, half, wall_h,
                  (100, 95, 86, 255), (140, 132, 118, 255), (50, 48, 42, 255), timber=False)

    # Extra stone banding
    for i in (0.25, 0.5, 0.75):
        y = ay - int(wall_h * i)
        draw.line([(ax - half, y - half // 2), (ax, y)], fill=(70, 66, 58, 255), width=2)
        draw.line([(ax, y), (ax + half, y - half // 2)], fill=(110, 104, 92, 255), width=2)

    # Narrow arrow slits
    for side in ("left", "right"):
        iso_window(draw, ax, ay, half, side=side, glow=(20, 18, 16, 255), y_off=-10)

    # Conical / flat battlement cap
    peak = top - 22
    left_cap = [(ax, top + 4), (ax - half - 4, top - half // 2 + 4), (ax, peak)]
    right_cap = [(ax, top + 4), (ax + half + 4, top - half // 2 + 4), (ax, peak)]
    draw.polygon(left_cap, fill=(90, 86, 78, 255), outline=(45, 42, 38, 255))
    draw.polygon(right_cap, fill=(130, 122, 110, 255), outline=(55, 50, 45, 255))

    # Merlon ring
    for ox in (-16, 0, 16):
        draw.rectangle([ax + ox - 4, peak - 2, ax + ox + 4, peak + 8],
                       fill=(120, 114, 102, 255), outline=(50, 48, 42, 255))

    # Flagpole
    draw.line([(ax, peak - 2), (ax, peak - 28)], fill=(60, 50, 40, 255), width=2)
    draw.polygon([(ax, peak - 28), (ax + 16, peak - 22), (ax, peak - 16)],
                 fill=(180, 40, 40, 255), outline=(100, 20, 20, 255))

    return img


# =============================================================================
# 3. Gatehouse with arch
# =============================================================================
def create_gatehouse():
    w, h = 128, 160
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    ax, ay = 64, 148
    draw_shadow(draw, (ax, ay), 52, 16, 120)

    half = 48
    wall_h = 78
    top = iso_box(draw, ax, ay, half, wall_h,
                  (100, 94, 84, 255), (142, 134, 120, 255), (48, 44, 38, 255), timber=False)

    # Course lines
    for i in range(1, 5):
        y = ay - i * 15
        draw.line([(ax - half + 2, y - half // 2), (ax - 2, y)], fill=(68, 64, 56, 200), width=1)
        draw.line([(ax + 2, y), (ax + half - 2, y - half // 2)], fill=(105, 98, 88, 200), width=1)

    # Arch opening through the front (carved into both faces near center)
    # Dark tunnel void
    arch_l = [
        (ax - 10, ay - 4), (ax - 22, ay - 14), (ax - 22, ay - 48),
        (ax - 10, ay - 58), (ax, ay - 52), (ax, ay - 8),
    ]
    arch_r = [
        (ax + 10, ay - 4), (ax + 22, ay - 14), (ax + 22, ay - 48),
        (ax + 10, ay - 58), (ax, ay - 52), (ax, ay - 8),
    ]
    draw.polygon(arch_l, fill=(22, 20, 18, 255))
    draw.polygon(arch_r, fill=(30, 28, 24, 255))
    # Arch stone rim
    draw.arc([ax - 24, ay - 62, ax + 24, ay - 20], 200, 340, fill=(160, 150, 135, 255), width=3)

    # Portcullis hints
    for gx in range(-8, 10, 5):
        draw.line([(ax + gx, ay - 12), (ax + gx, ay - 50)], fill=(55, 58, 65, 220), width=1)

    # Upper walkway / machicolation band
    draw.polygon(
        [(ax - half - 2, top - half // 2 + 2), (ax, top + 6), (ax + half + 2, top - half // 2 + 2),
         (ax + half + 2, top - half // 2 - 8), (ax, top - 4), (ax - half - 2, top - half // 2 - 8)],
        fill=(120, 112, 100, 255), outline=(50, 46, 40, 255)
    )

    # Twin small towers on sides
    for sx, c_l, c_r in [(-34, (95, 90, 80, 255), (125, 118, 105, 255)),
                         (34, (95, 90, 80, 255), (125, 118, 105, 255))]:
        tw = 12
        th = 28
        base = top + 4
        draw.polygon(
            [(ax + sx, base), (ax + sx - tw, base - 6), (ax + sx - tw, base - th - 6), (ax + sx, base - th)],
            fill=c_l, outline=(45, 42, 38, 255)
        )
        draw.polygon(
            [(ax + sx, base), (ax + sx + tw, base - 6), (ax + sx + tw, base - th - 6), (ax + sx, base - th)],
            fill=c_r, outline=(45, 42, 38, 255)
        )
        # Merlon
        draw.rectangle([ax + sx - 5, base - th - 10, ax + sx + 5, base - th],
                       fill=(130, 122, 110, 255), outline=(45, 42, 38, 255))

    # Flat roof between towers
    peak = top - 18
    draw.polygon(
        [(ax, top + 2), (ax - 28, top - 12), (ax, peak), (ax + 28, top - 12)],
        fill=SLATE_R, outline=SLATE_DK
    )
    draw.polygon([(ax, top + 2), (ax - 28, top - 12), (ax, peak)], fill=SLATE_L, outline=SLATE_DK)

    # Banner over gate
    draw.line([(ax, top - 8), (ax, top - 36)], fill=TIMBER, width=2)
    draw.polygon([(ax, top - 36), (ax + 14, top - 30), (ax, top - 24)],
                 fill=(40, 90, 160, 255), outline=(20, 50, 90, 255))

    return img


# =============================================================================
# 4. Smithy — ash/soot, chimney, forge glow
# =============================================================================
def create_house_smithy():
    w, h = 128, 144
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    ax, ay = 64, 114
    draw_shadow(draw, (ax, ay + 8), 50, 18, 115)

    half = 42
    wall_h = 48
    top = iso_box(draw, ax, ay, half, wall_h, ASH_L, ASH_R, ASH_DK, timber=True)

    # Soot stains on walls
    draw.ellipse([ax - 30, ay - 40, ax - 10, ay - 20], fill=(30, 28, 26, 90))
    draw.ellipse([ax + 8, ay - 36, ax + 28, ay - 16], fill=(30, 28, 26, 70))

    # Wide workshop door (right)
    door = [
        (ax + 10, ay - 4), (ax + 28, ay - 14), (ax + 28, ay - 42),
        (ax + 10, ay - 32),
    ]
    draw.polygon(door, fill=(35, 32, 28, 255), outline=DOOR_DK)
    # Forge glow from doorway
    draw.polygon(
        [(ax + 14, ay - 10), (ax + 24, ay - 16), (ax + 24, ay - 28), (ax + 14, ay - 22)],
        fill=(255, 120, 30, 200)
    )
    draw.polygon(
        [(ax + 16, ay - 14), (ax + 22, ay - 18), (ax + 22, ay - 24), (ax + 16, ay - 20)],
        fill=(255, 200, 60, 230)
    )

    # Window with orange forge light (left)
    iso_window(draw, ax, ay, half, side="left", glow=(255, 160, 50, 255), y_off=-4)

    # Dark slate roof
    peak = iso_roof(draw, ax, top, half, 28, SLATE_L, SLATE_R, SLATE_DK)

    # Tall sooty chimney
    chimney(draw, ax, peak, offset_x=-20, soot=True)
    # Second stub chimney
    chimney(draw, ax, peak + 6, offset_x=14, soot=True)

    # Anvil silhouette out front (tiny prop cue)
    draw.polygon([(ax - 6, ay + 2), (ax + 8, ay - 4), (ax + 8, ay - 10), (ax - 6, ay - 4)],
                 fill=(45, 48, 55, 255), outline=(20, 22, 28, 255))

    return img


# =============================================================================
# 5. Temple / chapel — pale stone, stained glass, steeple
# =============================================================================
def create_house_temple():
    w, h = 128, 160
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    ax, ay = 64, 148
    draw_shadow(draw, (ax, ay), 50, 16, 110)

    half = 44
    wall_h = 58
    top = iso_box(draw, ax, ay, half, wall_h,
                  STONE_PALE_L, STONE_PALE_R, STONE_PALE_DK, timber=False)

    for i in range(1, 4):
        y = ay - i * 14
        draw.line([(ax - half + 2, y - half // 2), (ax - 2, y)], fill=(120, 115, 105, 180), width=1)
        draw.line([(ax + 2, y), (ax + half - 2, y - half // 2)], fill=(170, 164, 150, 180), width=1)

    # Tall arched door (right)
    door = [
        (ax + 8, ay - 4), (ax + 22, ay - 12), (ax + 22, ay - 48),
        (ax + 15, ay - 56), (ax + 8, ay - 48),
    ]
    draw.polygon(door, fill=(55, 45, 70, 255), outline=(35, 30, 45, 255))
    draw.ellipse([ax + 16, ay - 30, ax + 19, ay - 27], fill=GOLD)

    # Stained glass window (left)
    win = [(ax - 28, ay - 28), (ax - 14, ay - 20), (ax - 14, ay - 48), (ax - 28, ay - 56)]
    draw.polygon(win, fill=WIN_STAIN, outline=STONE_PALE_DK)
    draw.line([(ax - 21, ay - 24), (ax - 21, ay - 52)], fill=(90, 50, 130, 255), width=1)
    draw.line([(ax - 28, ay - 36), (ax - 14, ay - 28)], fill=(90, 50, 130, 255), width=1)
    draw.polygon([(ax - 27, ay - 40), (ax - 21, ay - 36), (ax - 21, ay - 48), (ax - 27, ay - 52)],
                 fill=(80, 160, 220, 220))
    draw.polygon([(ax - 21, ay - 34), (ax - 15, ay - 30), (ax - 15, ay - 44), (ax - 21, ay - 48)],
                 fill=(220, 180, 60, 220))

    # Rose window on upper wall face
    draw.ellipse([ax - 8, top + 4, ax + 8, top + 20], fill=(200, 160, 240, 230), outline=STONE_PALE_DK)
    draw.ellipse([ax - 3, top + 9, ax + 3, top + 15], fill=(255, 240, 180, 255))

    # Steep slate roof (drawn before steeple so spire sits cleanly on top)
    peak = iso_roof(draw, ax, top, half, 32, SLATE_L, SLATE_R, SLATE_DK)

    # Steeple cube sitting on the ridge, then conical spire above
    sb = peak + 6
    draw.polygon([(ax - 7, sb), (ax, sb + 4), (ax, peak - 2), (ax - 7, peak - 6)],
                 fill=STONE_PALE_L, outline=STONE_PALE_DK)
    draw.polygon([(ax + 7, sb), (ax, sb + 4), (ax, peak - 2), (ax + 7, peak - 6)],
                 fill=STONE_PALE_R, outline=STONE_PALE_DK)
    # Spire cone
    tip = peak - 36
    draw.polygon([(ax - 7, peak - 6), (ax + 7, peak - 6), (ax, tip)],
                 fill=SLATE_R, outline=SLATE_DK)
    draw.polygon([(ax - 7, peak - 6), (ax, tip), (ax - 1, peak - 6)],
                 fill=SLATE_L)
    draw.line([(ax, tip), (ax, tip - 10)], fill=GOLD, width=2)
    draw.line([(ax - 4, tip - 6), (ax + 4, tip - 6)], fill=GOLD, width=2)

    return img


# =============================================================================
# 6. Guild hall — tall narrow tower building
# =============================================================================
def create_house_guild():
    w, h = 128, 176
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    ax, ay = 64, 164
    draw_shadow(draw, (ax, ay), 42, 14, 115)

    half = 34
    wall_h = 88
    top = iso_box(draw, ax, ay, half, wall_h,
                  (105, 88, 72, 255), (150, 128, 105, 255), (55, 45, 35, 255), timber=True)

    # Extra horizontal floor bands (multi-storey)
    for i in (0.33, 0.66):
        y = ay - int(wall_h * i)
        draw.line([(ax - half, y - half // 2), (ax, y)], fill=TIMBER, width=2)
        draw.line([(ax, y), (ax + half, y - half // 2)], fill=TIMBER_R, width=2)

    # Door
    iso_door(draw, ax, ay, half, side="right", tall=22, wide=11)

    # Windows on each floor
    iso_window(draw, ax, ay, half, side="left", glow=WIN_GLOW, y_off=0)
    iso_window(draw, ax, ay, half, side="left", glow=WIN_BLUE, y_off=-28)
    iso_window(draw, ax, ay, half, side="right", glow=WIN_GLOW, y_off=-30)
    iso_window(draw, ax, ay, half, side="left", glow=WIN_GLOW, y_off=-55)

    # Clock face near top (right)
    draw.ellipse([ax + 8, top + 8, ax + 24, top + 24], fill=(240, 230, 200, 255), outline=TIMBER)
    draw.ellipse([ax + 14, top + 14, ax + 18, top + 18], fill=(40, 30, 20, 255))
    draw.line([(ax + 16, top + 16), (ax + 16, top + 10)], fill=(40, 30, 20, 255), width=1)
    draw.line([(ax + 16, top + 16), (ax + 21, top + 18)], fill=(40, 30, 20, 255), width=1)

    # Tall peaked roof
    peak = iso_roof(draw, ax, top, half, 34, ROOF_L, ROOF_R, ROOF_DK)

    # Guild banner hanging from right eave (inset so it stays in-frame)
    draw.line([(ax + 18, top + 6), (ax + 28, top + 18)], fill=TIMBER, width=2)
    ban = [(ax + 20, top + 14), (ax + 32, top + 8),
           (ax + 32, top + 28), (ax + 20, top + 34)]
    draw.polygon(ban, fill=(140, 30, 30, 255), outline=(70, 15, 15, 255))
    draw.ellipse([ax + 23, top + 16, ax + 29, top + 22], fill=GOLD)

    # Weather vane
    draw.line([(ax, peak), (ax, peak - 14)], fill=(80, 85, 95, 255), width=2)
    draw.polygon([(ax, peak - 14), (ax + 10, peak - 12), (ax, peak - 10)], fill=(200, 180, 60, 255))

    return img


# =============================================================================
# 7. Inn / tavern
# =============================================================================
def create_house_inn():
    w, h = 128, 144
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    ax, ay = 64, 114
    draw_shadow(draw, (ax, ay + 8), 50, 18, 115)

    half = 44
    wall_h = 50
    # Warm timber / plaster
    top = iso_box(draw, ax, ay, half, wall_h,
                  (125, 105, 85, 255), (170, 148, 120, 255), (60, 48, 36, 255), timber=True)

    # Plaster panels between timber (lighter patches)
    draw.polygon(
        [(ax - 30, ay - 18), (ax - 14, ay - 10), (ax - 14, ay - 28), (ax - 30, ay - 36)],
        fill=(210, 200, 175, 200)
    )

    # Wide tavern door
    iso_door(draw, ax, ay, half, side="right", tall=24, wide=14)

    # Warm glowing windows
    iso_window(draw, ax, ay, half, side="left", glow=WIN_GLOW, y_off=-2)
    iso_window(draw, ax, ay, half, side="right", glow=(255, 200, 90, 255), y_off=-18)

    # Upper dormer window suggestion on left
    iso_window(draw, ax, ay, half, side="left", glow=WIN_GLOW, y_off=-22)

    # Terracotta roof
    peak = iso_roof(draw, ax, top, half, 30, ROOF_L, ROOF_R, ROOF_DK)

    # Hanging inn sign
    draw.line([(ax + 30, top + 8), (ax + 42, top + 2)], fill=TIMBER, width=3)
    sign = [(ax + 34, top + 4), (ax + 50, top - 4), (ax + 50, top + 12), (ax + 34, top + 20)]
    draw.polygon(sign, fill=(60, 100, 70, 255), outline=(30, 55, 35, 255))
    # Mug glyph
    draw.rectangle([ax + 38, top + 4, ax + 46, top + 12], fill=(220, 190, 100, 255))
    draw.arc([ax + 44, top + 5, ax + 50, top + 11], 270, 90, fill=(220, 190, 100, 255), width=2)

    chimney(draw, ax, peak, offset_x=-16, soot=False)

    # Barrel by door
    draw.ellipse([ax + 2, ay - 2, ax + 14, ay + 8], fill=(95, 62, 32, 255), outline=(50, 30, 15, 255))
    draw.rectangle([ax + 2, ay - 8, ax + 14, ay + 2], fill=(130, 85, 45, 255))
    draw.ellipse([ax + 2, ay - 12, ax + 14, ay - 4], fill=(175, 120, 68, 255), outline=(85, 55, 28, 255))

    return img


# =============================================================================
# 8. Terraced residential row
# =============================================================================
def create_house_row():
    w, h = 128, 128
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    ax, ay = 64, 98
    draw_shadow(draw, (ax, ay + 6), 52, 16, 110)

    half = 48
    wall_h = 42
    top = iso_box(draw, ax, ay, half, wall_h,
                  (118, 100, 82, 255), (162, 142, 118, 255), (58, 48, 38, 255), timber=True)

    # Party-wall dividers suggesting 2–3 joined houses
    for sx in (-16, 16):
        if sx < 0:
            draw.line([(ax + sx, ay - 4), (ax + sx, top - 4)], fill=TIMBER, width=2)
        else:
            draw.line([(ax + sx, ay - 4), (ax + sx, top - 4)], fill=TIMBER_R, width=2)

    # Three doors / entries
    for ox, side in [(-18, "left"), (0, "right"), (20, "right")]:
        if side == "left":
            base = ay - 4
            door = [(ax + ox + 4, base), (ax + ox - 6, base - 5),
                    (ax + ox - 6, base - 20), (ax + ox + 4, base - 15)]
            draw.polygon(door, fill=DOOR, outline=DOOR_DK)
        else:
            base = ay - 4
            door = [(ax + ox - 4, base), (ax + ox + 6, base - 5),
                    (ax + ox + 6, base - 20), (ax + ox - 4, base - 15)]
            draw.polygon(door, fill=DOOR, outline=DOOR_DK)

    # Windows along the row
    iso_window(draw, ax, ay, half, side="left", glow=WIN_GLOW, y_off=-6)
    iso_window(draw, ax - 8, ay, half - 8, side="right", glow=WIN_BLUE, y_off=-8)
    # Extra small window
    ox, by = ax + 28, ay - 30
    win = [(ox + 5, by), (ox - 5, by + 4), (ox - 5, by - 8), (ox + 5, by - 12)]
    draw.polygon(win, fill=WIN_GLOW, outline=STONE_DK)

    # Continuous roof with slight steps
    peak = iso_roof(draw, ax, top, half, 26, ROOF_L, ROOF_R, ROOF_DK)

    # Shared chimneys
    chimney(draw, ax, peak, offset_x=-22, soot=False)
    chimney(draw, ax, peak + 4, offset_x=12, soot=False)

    return img


# =============================================================================
# Optional quality upgrades for existing shop / terrace
# =============================================================================
def create_house_shop_improved():
    """Shop rebuilt in the original generate_env_assets layout (kept regenerable)."""
    w, h = 128, 128
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw_shadow(draw, (64, 108), 50, 20, 110)

    left_wall = [(64, 98), (24, 78), (24, 48), (64, 68)]
    draw.polygon(left_wall, fill=(110, 95, 80, 255), outline=(60, 50, 40, 255))
    right_wall = [(64, 98), (104, 78), (104, 48), (64, 68)]
    draw.polygon(right_wall, fill=(155, 138, 118, 255), outline=(75, 62, 50, 255))

    draw.line([(44, 88), (44, 58)], fill=(70, 55, 42, 255), width=3)
    draw.line([(24, 63), (64, 83)], fill=(70, 55, 42, 255), width=2)
    draw.line([(84, 88), (84, 58)], fill=(85, 68, 52, 255), width=3)
    draw.line([(64, 83), (104, 63)], fill=(85, 68, 52, 255), width=2)

    door = [(74, 90), (86, 84), (86, 64), (74, 70)]
    draw.polygon(door, fill=(75, 45, 25, 255), outline=(40, 20, 10, 255))
    draw.ellipse([82, 77, 85, 80], fill=(220, 180, 50, 255))

    win = [(36, 76), (48, 82), (48, 68), (36, 62)]
    draw.polygon(win, fill=(255, 220, 110, 255), outline=(50, 40, 30, 255))
    draw.line([(42, 79), (42, 65)], fill=(120, 90, 40, 255), width=1)
    draw.line([(36, 69), (48, 75)], fill=(120, 90, 40, 255), width=1)

    left_roof = [(64, 42), (16, 46), (16, 26), (64, 18)]
    draw.polygon(left_roof, fill=(160, 55, 45, 255), outline=(90, 25, 20, 255))
    right_roof = [(64, 42), (112, 46), (112, 26), (64, 18)]
    draw.polygon(right_roof, fill=(210, 80, 65, 255), outline=(110, 35, 25, 255))

    front_gable = [(64, 42), (20, 46), (64, 68)]
    draw.polygon(front_gable, fill=(130, 110, 90, 255), outline=(70, 55, 40, 255))
    front_gable_r = [(64, 42), (108, 46), (64, 68)]
    draw.polygon(front_gable_r, fill=(160, 138, 115, 255), outline=(80, 65, 50, 255))

    for sy in range(24, 44, 4):
        draw.line([(64, sy), (16, sy + 8)], fill=(120, 40, 30, 255), width=1)
        draw.line([(64, sy), (112, sy + 8)], fill=(230, 100, 80, 255), width=1)

    draw.line([(88, 62), (106, 53)], fill=(60, 40, 20, 255), width=3)
    sign_board = [(92, 60), (104, 54), (104, 66), (92, 72)]
    draw.polygon(sign_board, fill=(220, 175, 100, 255), outline=(90, 60, 20, 255))
    draw.text((94, 61), "SHOP", fill=(100, 40, 10, 255))

    chimney_left = [(30, 34), (38, 30), (38, 14), (30, 18)]
    chimney_right = [(38, 30), (44, 33), (44, 17), (38, 14)]
    draw.polygon(chimney_left, fill=(80, 85, 95, 255), outline=(40, 45, 55, 255))
    draw.polygon(chimney_right, fill=(110, 115, 125, 255), outline=(50, 55, 65, 255))
    draw.ellipse([34, 6, 40, 12], fill=(220, 225, 235, 160))
    draw.ellipse([38, 1, 46, 7], fill=(240, 245, 250, 200))

    return img


def create_house_terrace_improved():
    """Upgrade parametric terrace into a proper iso townhouse."""
    w, h = 128, 128
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    ax, ay = 64, 98
    draw_shadow(draw, (ax, ay + 6), 48, 16, 110)

    half = 42
    wall_h = 46
    top = iso_box(draw, ax, ay, half, wall_h,
                  (125, 100, 72, 255), (168, 140, 100, 255), (55, 42, 28, 255), timber=True)

    iso_door(draw, ax, ay, half, side="right", tall=22, wide=11)
    iso_window(draw, ax, ay, half, side="left", glow=WIN_GLOW)
    iso_window(draw, ax, ay, half, side="right", glow=WIN_BLUE, y_off=-16)

    peak = iso_roof(draw, ax, top, half, 28, ROOF_L, ROOF_R, ROOF_DK)
    chimney(draw, ax, peak, offset_x=-18, soot=False)

    # Flower box under left window
    draw.polygon([(ax - 28, ay - 22), (ax - 14, ay - 16), (ax - 14, ay - 20), (ax - 28, ay - 26)],
                 fill=(60, 100, 50, 255))
    for bx, by in [(ax - 24, ay - 24), (ax - 20, ay - 22), (ax - 16, ay - 20)]:
        draw.ellipse([bx - 2, by - 2, bx + 2, by + 2], fill=(220, 60, 80, 255))

    return img


ASSETS = [
    ("env_wall_curtain.png", create_wall_curtain),
    ("env_wall_corner.png", create_wall_corner),
    ("env_gatehouse.png", create_gatehouse),
    ("env_house_smithy.png", create_house_smithy),
    ("env_house_temple.png", create_house_temple),
    ("env_house_guild.png", create_house_guild),
    ("env_house_inn.png", create_house_inn),
    ("env_house_row.png", create_house_row),
    # Optional in-place upgrades
    ("env_house_shop.png", create_house_shop_improved),
    ("env_house_terrace.png", create_house_terrace_improved),
]

# Manifest for registration / docs
PROP_META = [
    ("env_wall_curtain", "Curtain Wall", 96, 128, 48, 116),
    ("env_wall_corner", "Wall Corner Bastion", 96, 144, 48, 132),
    ("env_gatehouse", "Gatehouse", 128, 160, 64, 148),
    ("env_house_smithy", "Smithy", 128, 144, 64, 114),
    ("env_house_temple", "Temple Chapel", 128, 160, 64, 148),
    ("env_house_guild", "Guild Hall", 128, 176, 64, 164),
    ("env_house_inn", "Inn / Tavern", 128, 144, 64, 114),
    ("env_house_row", "Terraced Row House", 128, 128, 64, 98),
]


def main():
    print(f"=== Generating {len(ASSETS)} town building / wall sprites ===")
    for name, fn in ASSETS:
        img = fn()
        save_asset(img, name)
    print("\n=== Prop meta (type, name, w, h, ax, ay) ===")
    for row in PROP_META:
        print(f"  {row}")
    print("DONE")


if __name__ == "__main__":
    main()
