"""
generate_item_icons.py

Phase 3 Task C — 32x32 item icons (vault/ASSET_MANIFEST.md).
PIL-only procedural JRPG icons matching potion_health_ff.png style:
flat fills, dark outline, highlight speck, soft drop shadow.

Writes to BOTH assets/sprites_ff/ and web/assets/sprites_ff/.
Idempotent — safe to re-run.
"""

import json
import os
from PIL import Image, ImageDraw

ROOT = r"D:\ai-studio\Zaggers"
TARGET_DIRS = [
    os.path.join(ROOT, "assets", "sprites_ff"),
    os.path.join(ROOT, "web", "assets", "sprites_ff"),
]

SIZE = 32
OUTLINE = (16, 16, 32, 255)
SHADOW = (0, 0, 0, 80)
WHITE = (255, 255, 255, 255)


def shade(c, f):
    r, g, b, a = c
    if f <= 1.0:
        return (max(0, int(r * f)), max(0, int(g * f)), max(0, int(b * f)), a)
    t = f - 1.0
    return (
        min(255, int(r + (255 - r) * t)),
        min(255, int(g + (255 - g) * t)),
        min(255, int(b + (255 - b) * t)),
        a,
    )


def new_canvas():
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def save_asset(img, name):
    for d in TARGET_DIRS:
        os.makedirs(d, exist_ok=True)
        img.save(os.path.join(d, name), "PNG")


def oval_shadow(draw, cx, cy, rx, ry):
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=SHADOW)


def poly(draw, pts, fill, outline=OUTLINE):
    draw.polygon(pts, fill=fill, outline=outline)


# =============================================================================
# CONSUMABLES
# =============================================================================

def draw_potion(body, cork=(150, 110, 60, 255), liquid_hl=None):
    """Classic round flask matching potion_health_ff silhouette."""
    img = new_canvas()
    d = ImageDraw.Draw(img)
    oval_shadow(d, 16, 28, 9, 3)

    neck = (shade(body, 0.85))
    # Cork
    d.rectangle([13, 2, 18, 6], fill=cork, outline=OUTLINE)
    d.rectangle([14, 3, 17, 5], fill=shade(cork, 1.25))

    # Neck
    d.rectangle([13, 6, 18, 11], fill=neck, outline=OUTLINE)
    d.line([(14, 7), (14, 10)], fill=shade(body, 1.35), width=1)

    # Round body
    d.ellipse([5, 9, 26, 29], fill=OUTLINE)
    d.ellipse([6, 10, 25, 28], fill=body)
    d.ellipse([8, 12, 16, 20], fill=liquid_hl or shade(body, 1.45))
    d.point((10, 14), fill=WHITE)
    return img


def icon_potion_mana():
    return draw_potion((40, 90, 210, 255), liquid_hl=(120, 180, 255, 255))


def icon_potion_aetherite():
    # Holy gold/white draught
    img = draw_potion((230, 210, 90, 255), cork=(180, 160, 80, 255), liquid_hl=(255, 250, 200, 255))
    d = ImageDraw.Draw(img)
    # Soft aura sparkles
    for x, y in [(4, 8), (27, 12), (7, 22), (24, 24)]:
        d.point((x, y), fill=(255, 255, 220, 200))
    return img


def icon_food_bread():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    oval_shadow(d, 16, 27, 11, 3)
    crust = (180, 120, 55, 255)
    crumb = (230, 190, 120, 255)
    # Loaf
    d.ellipse([4, 10, 28, 26], fill=OUTLINE)
    d.ellipse([5, 11, 27, 25], fill=crust)
    d.ellipse([8, 14, 24, 23], fill=crumb)
    # Score lines
    d.arc([7, 12, 16, 22], 200, 320, fill=shade(crust, 0.7), width=1)
    d.arc([14, 12, 25, 22], 220, 340, fill=shade(crust, 0.7), width=1)
    d.point((11, 15), fill=WHITE)
    return img


def icon_key_thawstone():
    """Ice key visibly melting — pale cyan with drip."""
    img = new_canvas()
    d = ImageDraw.Draw(img)
    oval_shadow(d, 16, 28, 8, 3)
    ice = (160, 220, 245, 255)
    # Bow (circular head) with punched hole
    d.ellipse([8, 3, 22, 17], fill=OUTLINE)
    d.ellipse([9, 4, 21, 16], fill=ice)
    # Shaft
    d.rectangle([13, 15, 18, 26], fill=OUTLINE)
    d.rectangle([14, 16, 17, 25], fill=ice)
    # Bits
    d.rectangle([18, 18, 22, 20], fill=ice, outline=OUTLINE)
    d.rectangle([18, 22, 21, 24], fill=ice, outline=OUTLINE)
    # Melt drip
    d.ellipse([15, 25, 18, 30], fill=(140, 210, 240, 220))
    d.point((11, 6), fill=WHITE)
    d.point((19, 9), fill=(220, 250, 255, 255))
    # Punch transparent hole in bow
    px = img.load()
    cx, cy, r2 = 15, 10, 2.6 * 2.6
    for y in range(7, 14):
        for x in range(12, 19):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r2:
                px[x, y] = (0, 0, 0, 0)
    return img


# =============================================================================
# WEAPONS
# =============================================================================

def icon_wpn_shortsword():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    oval_shadow(d, 16, 28, 8, 3)
    steel = (190, 200, 215, 255)
    # Blade diagonal
    poly(d, [(18, 3), (22, 5), (12, 20), (8, 18)], steel)
    d.line([(19, 5), (11, 18)], fill=WHITE, width=1)
    # Guard
    poly(d, [(6, 17), (16, 22), (14, 24), (4, 19)], (180, 150, 60, 255))
    # Grip
    poly(d, [(8, 21), (12, 23), (8, 29), (4, 27)], (110, 70, 40, 255))
    # Pommel
    d.ellipse([3, 26, 8, 31], fill=(200, 170, 70, 255), outline=OUTLINE)
    return img


def icon_wpn_cleaver():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    oval_shadow(d, 16, 28, 9, 3)
    iron = (140, 145, 155, 255)
    # Heavy rectangular blade
    poly(d, [(6, 4), (24, 6), (22, 18), (5, 16)], iron)
    d.line([(8, 6), (20, 8)], fill=shade(iron, 1.35), width=1)
    # Cutting edge darker
    d.line([(22, 7), (21, 17)], fill=OUTLINE, width=1)
    # Handle
    d.rectangle([8, 16, 13, 28], fill=(90, 55, 30, 255), outline=OUTLINE)
    d.rectangle([9, 17, 12, 20], fill=(160, 140, 50, 255))
    return img


def icon_wpn_trident():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    oval_shadow(d, 16, 28, 7, 3)
    teal = (70, 160, 190, 255)
    shaft = (120, 90, 50, 255)
    # Shaft
    d.line([(16, 10), (16, 29)], fill=OUTLINE, width=3)
    d.line([(16, 10), (16, 29)], fill=shaft, width=1)
    # Three prongs
    for tip in [(8, 2), (16, 1), (24, 2)]:
        poly(d, [(16, 12), tip, (tip[0], tip[1] + 6)], teal)
    d.point((16, 3), fill=WHITE)
    # Crossbar
    d.line([(8, 12), (24, 12)], fill=teal, width=2)
    return img


def icon_wpn_emberglass():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    oval_shadow(d, 16, 28, 8, 3)
    glass = (220, 80, 40, 255)
    glow = (255, 180, 60, 255)
    # Jagged volcanic blade
    poly(d, [(17, 2), (22, 6), (14, 20), (9, 17)], glass)
    poly(d, [(17, 2), (19, 5), (13, 18), (11, 16)], glow)
    d.point((16, 5), fill=WHITE)
    # Ember cracks
    d.line([(15, 8), (17, 14)], fill=(255, 220, 100, 255), width=1)
    # Guard / grip
    poly(d, [(7, 18), (16, 22), (14, 24), (5, 20)], (60, 40, 35, 255))
    poly(d, [(8, 22), (12, 24), (8, 30), (4, 28)], (40, 30, 28, 255))
    return img


def icon_wpn_longbow():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    oval_shadow(d, 18, 28, 8, 3)
    wood = (100, 150, 190, 255)  # hoarfrost blue-wood
    # Bow arc
    d.arc([4, 2, 28, 30], 200, 340, fill=OUTLINE, width=3)
    d.arc([4, 2, 28, 30], 200, 340, fill=wood, width=2)
    # String
    d.line([(10, 6), (10, 26)], fill=(220, 235, 245, 255), width=1)
    # Frost tips
    d.ellipse([8, 3, 13, 8], fill=(200, 240, 255, 255), outline=OUTLINE)
    d.ellipse([8, 24, 13, 29], fill=(200, 240, 255, 255), outline=OUTLINE)
    # Grip wrap
    d.line([(22, 14), (26, 16)], fill=(180, 140, 70, 255), width=2)
    return img


def icon_wpn_staff_root():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    oval_shadow(d, 16, 28, 8, 3)
    bark = (70, 45, 55, 255)
    shadow_glow = (140, 60, 160, 255)
    # Twisted staff shaft
    poly(d, [(14, 8), (18, 8), (17, 29), (13, 29)], bark)
    d.line([(15, 10), (16, 28)], fill=shade(bark, 1.3), width=1)
    # Root crown / thorns
    poly(d, [(16, 2), (22, 8), (16, 10), (10, 8)], shadow_glow)
    d.ellipse([13, 4, 19, 10], fill=(40, 20, 50, 255), outline=OUTLINE)
    d.point((16, 6), fill=(220, 120, 255, 255))
    # Side roots
    d.line([(14, 12), (8, 8)], fill=bark, width=2)
    d.line([(18, 14), (24, 10)], fill=bark, width=2)
    return img


def icon_wpn_lance_dragon():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    oval_shadow(d, 16, 28, 8, 3)
    gold = (220, 180, 60, 255)
    red = (180, 40, 40, 255)
    # Long shaft
    poly(d, [(14, 8), (18, 8), (17, 29), (13, 29)], (120, 80, 40, 255))
    # Spearhead
    poly(d, [(16, 1), (22, 10), (16, 12), (10, 10)], gold)
    d.line([(16, 3), (16, 10)], fill=WHITE, width=1)
    # Dragon wing crossguard
    poly(d, [(8, 10), (16, 14), (8, 16)], red)
    poly(d, [(24, 10), (16, 14), (24, 16)], red)
    d.point((12, 12), fill=(255, 100, 80, 255))
    return img


# =============================================================================
# SHIELDS
# =============================================================================

def icon_shd_targe():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    oval_shadow(d, 16, 27, 10, 3)
    oak = (140, 95, 45, 255)
    d.ellipse([4, 4, 28, 28], fill=OUTLINE)
    d.ellipse([5, 5, 27, 27], fill=oak)
    d.ellipse([10, 10, 22, 22], fill=shade(oak, 0.75))
    # Boss rivet
    d.ellipse([13, 13, 19, 19], fill=(180, 160, 70, 255), outline=OUTLINE)
    d.point((15, 15), fill=WHITE)
    # Wood grain hint
    d.arc([7, 7, 25, 25], 30, 120, fill=shade(oak, 0.6), width=1)
    return img


def icon_shd_aegis():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    oval_shadow(d, 16, 28, 10, 3)
    sea = (60, 130, 180, 255)
    # Heater shield
    poly(d, [(16, 2), (28, 8), (26, 20), (16, 30), (6, 20), (4, 8)], OUTLINE)
    poly(d, [(16, 3), (27, 9), (25, 19), (16, 28), (7, 19), (5, 9)], sea)
    poly(d, [(16, 5), (20, 10), (16, 24), (12, 10)], shade(sea, 1.35))
    # Wave emblem
    d.arc([10, 12, 22, 22], 200, 340, fill=(180, 230, 255, 255), width=1)
    d.point((14, 8), fill=WHITE)
    return img


def icon_shd_bulwark():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    oval_shadow(d, 16, 28, 11, 3)
    slag = (90, 70, 65, 255)
    ember = (220, 100, 40, 255)
    # Tower shield
    poly(d, [(6, 3), (26, 3), (28, 24), (16, 30), (4, 24)], OUTLINE)
    poly(d, [(7, 4), (25, 4), (27, 23), (16, 28), (5, 23)], slag)
    # Ember rivets / forge glow
    for xy in [(10, 8), (22, 8), (10, 16), (22, 16), (16, 12)]:
        d.ellipse([xy[0] - 1, xy[1] - 1, xy[0] + 1, xy[1] + 1], fill=ember)
    d.rectangle([14, 6, 18, 20], fill=shade(slag, 1.25))
    d.point((15, 7), fill=(255, 200, 120, 255))
    return img


# =============================================================================
# ARMOR
# =============================================================================

def icon_arm_jerkin():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    oval_shadow(d, 16, 28, 10, 3)
    leather = (130, 90, 50, 255)
    # Torso silhouette
    poly(d, [(10, 6), (14, 4), (18, 4), (22, 6), (26, 12), (24, 28), (8, 28), (6, 12)], leather)
    # Neck hole
    d.ellipse([12, 5, 20, 12], fill=(0, 0, 0, 0))
    d.ellipse([12, 5, 20, 12], fill=OUTLINE)
    d.ellipse([13, 6, 19, 11], fill=(40, 30, 20, 255))
    # Belt
    d.rectangle([8, 20, 24, 23], fill=(90, 60, 30, 255), outline=OUTLINE)
    d.rectangle([14, 19, 18, 24], fill=(180, 150, 60, 255), outline=OUTLINE)
    # Highlight shoulder
    d.line([(9, 10), (12, 8)], fill=shade(leather, 1.4), width=1)
    return img


def icon_arm_mythril():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    oval_shadow(d, 16, 28, 10, 3)
    myth = (160, 190, 210, 255)
    poly(d, [(10, 6), (14, 3), (18, 3), (22, 6), (27, 12), (25, 28), (7, 28), (5, 12)], myth)
    # Collar
    d.ellipse([12, 4, 20, 11], fill=OUTLINE)
    d.ellipse([13, 5, 19, 10], fill=shade(myth, 0.7))
    # Plate lines
    d.line([(16, 12), (16, 26)], fill=shade(myth, 0.7), width=1)
    d.line([(8, 14), (24, 14)], fill=shade(myth, 1.25), width=1)
    d.line([(8, 20), (24, 20)], fill=shade(myth, 1.25), width=1)
    d.point((11, 9), fill=WHITE)
    return img


def icon_arm_slagplate():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    oval_shadow(d, 16, 28, 10, 3)
    plate = (70, 55, 50, 255)
    glow = (230, 90, 30, 255)
    poly(d, [(9, 6), (14, 3), (18, 3), (23, 6), (28, 12), (26, 28), (6, 28), (4, 12)], plate)
    d.ellipse([12, 4, 20, 11], fill=OUTLINE)
    d.ellipse([13, 5, 19, 10], fill=(40, 30, 28, 255))
    # Molten seams
    d.line([(10, 14), (22, 14)], fill=glow, width=1)
    d.line([(10, 20), (22, 20)], fill=glow, width=1)
    d.line([(16, 11), (16, 26)], fill=shade(glow, 0.8), width=1)
    d.point((12, 15), fill=(255, 200, 80, 255))
    return img


def icon_arm_shroud():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    oval_shadow(d, 16, 28, 10, 3)
    shroud = (50, 30, 70, 255)
    # Flowing cloak / robe torso
    poly(d, [(10, 5), (16, 2), (22, 5), (28, 14), (24, 30), (8, 30), (4, 14)], shroud)
    poly(d, [(12, 6), (16, 4), (20, 6), (22, 14), (16, 28), (10, 14)], shade(shroud, 1.35))
    # Hood void
    d.ellipse([11, 4, 21, 14], fill=(20, 10, 30, 255), outline=OUTLINE)
    d.point((14, 8), fill=(160, 80, 200, 180))
    # Trailing wisps
    d.line([(6, 18), (3, 24)], fill=shade(shroud, 1.2), width=1)
    d.line([(26, 18), (29, 24)], fill=shade(shroud, 1.2), width=1)
    return img


# =============================================================================
# HEADGEAR
# =============================================================================

def icon_hat_kettle():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    oval_shadow(d, 16, 26, 10, 3)
    iron = (120, 125, 135, 255)
    # Dome
    d.ellipse([6, 6, 26, 24], fill=OUTLINE)
    d.ellipse([7, 7, 25, 23], fill=iron)
    d.ellipse([10, 9, 18, 15], fill=shade(iron, 1.4))
    # Brim
    d.ellipse([3, 16, 29, 26], fill=OUTLINE)
    d.ellipse([4, 17, 28, 25], fill=shade(iron, 0.85))
    # Rivet
    d.point((16, 12), fill=WHITE)
    return img


def icon_hat_circlet():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    oval_shadow(d, 16, 24, 9, 3)
    coral = (230, 120, 140, 255)
    # Band
    d.ellipse([4, 10, 28, 24], fill=OUTLINE)
    d.ellipse([5, 11, 27, 23], fill=(70, 160, 180, 255))
    # Coral gems on top (drawn before hole punch so band stays under)
    for x in (10, 16, 22):
        d.ellipse([x - 3, 6, x + 3, 14], fill=coral, outline=OUTLINE)
        d.point((x - 1, 8), fill=(255, 200, 210, 255))
    # Punch ring opening
    px = img.load()
    for y in range(14, 23):
        for x in range(8, 25):
            # ellipse 8,14,24,22
            nx = (x - 16) / 8.0
            ny = (y - 18) / 4.0
            if nx * nx + ny * ny <= 1.0:
                px[x, y] = (0, 0, 0, 0)
    return img


def icon_hat_diadem():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    oval_shadow(d, 16, 24, 9, 3)
    gold = (220, 190, 70, 255)
    aurora = (140, 220, 255, 255)
    # Band
    d.arc([4, 12, 28, 28], 200, 340, fill=OUTLINE, width=4)
    d.arc([4, 12, 28, 28], 200, 340, fill=gold, width=2)
    # Central jewel
    poly(d, [(16, 2), (20, 10), (16, 14), (12, 10)], aurora)
    d.point((16, 7), fill=WHITE)
    # Side spikes
    poly(d, [(8, 8), (10, 14), (6, 14)], gold)
    poly(d, [(24, 8), (26, 14), (22, 14)], gold)
    # Aurora shimmer
    d.point((14, 5), fill=(255, 180, 255, 255))
    d.point((18, 5), fill=(180, 255, 220, 255))
    return img


# =============================================================================
# ACCESSORIES
# =============================================================================

def icon_acc_charm():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    oval_shadow(d, 16, 27, 8, 3)
    leaf = (70, 150, 60, 255)
    twig = (120, 85, 40, 255)
    # Cord
    d.arc([8, 2, 24, 16], 200, 340, fill=twig, width=2)
    # Leaf charm
    poly(d, [(16, 10), (24, 18), (16, 28), (8, 18)], leaf)
    d.line([(16, 12), (16, 26)], fill=shade(leaf, 0.6), width=1)
    d.point((13, 16), fill=shade(leaf, 1.45))
    # Berry
    d.ellipse([14, 17, 18, 21], fill=(200, 50, 60, 255), outline=OUTLINE)
    return img


def icon_acc_pendant():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    oval_shadow(d, 16, 28, 7, 3)
    glass = (200, 230, 255, 255)
    # Chain
    d.arc([8, 2, 24, 14], 200, 340, fill=(180, 170, 90, 255), width=1)
    # Pendant crystal
    poly(d, [(16, 10), (24, 18), (16, 30), (8, 18)], OUTLINE)
    poly(d, [(16, 11), (23, 18), (16, 28), (9, 18)], glass)
    poly(d, [(16, 12), (19, 18), (16, 24)], shade(glass, 1.2))
    d.point((14, 16), fill=WHITE)
    # Holy glow
    d.point((6, 14), fill=(255, 255, 200, 180))
    d.point((26, 14), fill=(255, 255, 200, 180))
    return img


def icon_acc_signet():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    oval_shadow(d, 16, 26, 9, 3)
    gold = (200, 160, 50, 255)
    void = (40, 20, 60, 255)
    # Ring band
    d.ellipse([6, 10, 26, 28], fill=OUTLINE)
    d.ellipse([7, 11, 25, 27], fill=gold)
    d.ellipse([11, 15, 21, 25], fill=void)
    # Signet face
    d.ellipse([10, 4, 22, 16], fill=OUTLINE)
    d.ellipse([11, 5, 21, 15], fill=gold)
    # Sovereign mark (crescent / eye)
    d.ellipse([13, 7, 19, 13], fill=void)
    d.ellipse([14, 8, 17, 11], fill=(180, 80, 220, 255))
    d.point((15, 9), fill=WHITE)
    return img


# =============================================================================
# REGISTRY
# =============================================================================

ICONS = {
    # Consumables (4)
    "potion_mana_ff.png": icon_potion_mana,
    "food_bread_ff.png": icon_food_bread,
    "potion_aetherite_ff.png": icon_potion_aetherite,
    "key_thawstone_ff.png": icon_key_thawstone,
    # Weapons (6 + optional lance)
    "wpn_shortsword_ff.png": icon_wpn_shortsword,
    "wpn_cleaver_ff.png": icon_wpn_cleaver,
    "wpn_trident_ff.png": icon_wpn_trident,
    "wpn_emberglass_ff.png": icon_wpn_emberglass,
    "wpn_longbow_ff.png": icon_wpn_longbow,
    "wpn_staff_root_ff.png": icon_wpn_staff_root,
    "wpn_lance_dragon_ff.png": icon_wpn_lance_dragon,
    # Shields (3)
    "shd_targe_ff.png": icon_shd_targe,
    "shd_aegis_ff.png": icon_shd_aegis,
    "shd_bulwark_ff.png": icon_shd_bulwark,
    # Armor (4)
    "arm_jerkin_ff.png": icon_arm_jerkin,
    "arm_mythril_ff.png": icon_arm_mythril,
    "arm_slagplate_ff.png": icon_arm_slagplate,
    "arm_shroud_ff.png": icon_arm_shroud,
    # Headgear (3)
    "hat_kettle_ff.png": icon_hat_kettle,
    "hat_circlet_ff.png": icon_hat_circlet,
    "hat_diadem_ff.png": icon_hat_diadem,
    # Accessories (3)
    "acc_charm_ff.png": icon_acc_charm,
    "acc_pendant_ff.png": icon_acc_pendant,
    "acc_signet_ff.png": icon_acc_signet,
}

# Core 23 required by ASSET_MANIFEST Task C (lance is optional bonus)
REQUIRED_23 = [n for n in ICONS if n != "wpn_lance_dragon_ff.png"]


def update_dragon_lance_icon():
    """Point dragon_lance at the new lance icon if still on excalibur placeholder."""
    db_path = os.path.join(ROOT, "web", "zaggers_database.json")
    with open(db_path, "r", encoding="utf-8") as f:
        raw = f.read()
    db = json.loads(raw)
    lance = db.get("items", {}).get("dragon_lance")
    if not lance:
        print("  dragon_lance: not found in DB (skipped)")
        return
    old = lance.get("icon")
    if old == "wpn_lance_dragon_ff.png":
        print("  dragon_lance: already points at wpn_lance_dragon_ff.png")
        return
    # Surgical replace inside the dragon_lance block only
    marker = '"id": "dragon_lance"'
    idx = raw.find(marker)
    if idx < 0:
        print("  dragon_lance: block not found (skipped)")
        return
    # Limit search to this item object (~400 chars)
    chunk_end = raw.find('\n    },\n    "', idx)
    if chunk_end < 0:
        chunk_end = idx + 500
    chunk = raw[idx:chunk_end]
    old_lit = f'"icon": "{old}"'
    new_lit = '"icon": "wpn_lance_dragon_ff.png"'
    if old_lit not in chunk:
        print(f"  dragon_lance: could not locate icon field {old!r}")
        return
    new_chunk = chunk.replace(old_lit, new_lit, 1)
    raw = raw[:idx] + new_chunk + raw[chunk_end:]
    with open(db_path, "w", encoding="utf-8") as f:
        f.write(raw)
    print(f"  dragon_lance: icon {old!r} -> 'wpn_lance_dragon_ff.png'")


def verify():
    ok = True
    for name in ICONS:
        for d in TARGET_DIRS:
            path = os.path.join(d, name)
            if not os.path.isfile(path):
                print(f"  MISSING: {path}")
                ok = False
                continue
            im = Image.open(path)
            if im.size != (SIZE, SIZE) or im.mode != "RGBA":
                print(f"  BAD FORMAT: {path} {im.size} {im.mode}")
                ok = False
    return ok


def cross_check_db():
    db_path = os.path.join(ROOT, "web", "zaggers_database.json")
    with open(db_path, "r", encoding="utf-8") as f:
        db = json.load(f)
    missing = []
    checked = 0
    search_dirs = list(TARGET_DIRS)
    for d in TARGET_DIRS:
        search_dirs.append(os.path.join(os.path.dirname(d), "tiles_ff"))
    for item_id, item in db.get("items", {}).items():
        icon = item.get("icon")
        if not icon:
            continue
        checked += 1
        if not any(os.path.isfile(os.path.join(d, icon)) for d in search_dirs):
            missing.append((item_id, icon))
    return checked, missing


def main():
    print("Generating item icons...")
    for name, fn in ICONS.items():
        img = fn()
        assert img.size == (SIZE, SIZE) and img.mode == "RGBA"
        save_asset(img, name)
        print(f"  wrote {name}")

    print("\nUpdating dragon_lance icon field...")
    update_dragon_lance_icon()

    print("\nVerifying on-disk icons...")
    if not verify():
        raise SystemExit(1)
    print(f"  OK: {len(ICONS)} icons x {len(TARGET_DIRS)} dirs, all {SIZE}x{SIZE} RGBA")

    print("\nCross-checking items[].icon in zaggers_database.json...")
    checked, missing = cross_check_db()
    if missing:
        for item_id, icon in missing:
            print(f"  MISSING FILE for {item_id}: {icon}")
        raise SystemExit(1)
    print(f"  OK: {checked} item icons resolve on disk")
    print("Done.")


if __name__ == "__main__":
    main()
