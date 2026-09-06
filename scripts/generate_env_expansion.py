"""
generate_env_expansion.py

Phase 3 environment art pass (vault/ASSET_MANIFEST.md Task D + Task E,
flavour cross-checked against vault/WORLD_MAP_EXPANSION.md).

Follows the conventions of the existing environment generators:
  - generate_terrain_tilesets.py: 128x64 isometric diamond floor tiles,
    alpha-masked to the diamond, noise-shaded fill + border blend.
  - generate_env_assets.py: variable-size RGBA prop sprites built from
    flat polygons/ellipses with an oval drop shadow at the ground-contact
    anchor point, saved to BOTH assets/tiles_ff/ and web/assets/tiles_ff/.

TASK D — 19 new iso floor tiles (4 new categories: meadow extras, sanctum,
spire, plus two brand-new categories `ice` and `root`).

TASK E — 38 new environmental props across Aethelgard districts (16) and
Wilderness/Chasm/Rootways (22), each sized and anchored exactly per the
ASSET_MANIFEST.md table. As with the monster pass, art is produced through a
small library of parametric prop archetypes (BOX/PILLAR, BANNER, ORGANIC,
FIGURE/STATUE, HAZARD-GLOW, OVERHEAD, CONTAINER) rather than one fully bespoke
painting per prop, so all 38 stay on-pipeline and visually consistent while
matching each entry's exact filename / size / anchor from the manifest.
"""

import os
import random
from PIL import Image, ImageDraw, ImageFilter

ROOT = r"D:\ai-studio\Zaggers"
TARGET_DIRS = [
    os.path.join(ROOT, "assets", "tiles_ff"),
    os.path.join(ROOT, "web", "assets", "tiles_ff"),
]


def save_asset(img, name):
    for d in TARGET_DIRS:
        os.makedirs(d, exist_ok=True)
        img.save(os.path.join(d, name), "PNG")


def hx(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)


def shade(c, f):
    r, g, b, a = c
    if f <= 1.0:
        return (int(r * f), int(g * f), int(b * f), a)
    t = f - 1.0
    return (int(r + (255 - r) * t), int(g + (255 - g) * t), int(b + (255 - b) * t), a)


def draw_shadow(draw, center, rx, ry, alpha=100):
    cx, cy = center
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(10, 15, 25, alpha))


# =============================================================================
# TASK D — Iso floor tiles (128x64 diamond, matches generate_terrain_tilesets.py)
# =============================================================================
TILE_W, TILE_H = 128, 64


def is_inside_diamond(x, y, tw=TILE_W, th=TILE_H):
    cx, cy = tw / 2.0 - 0.5, th / 2.0 - 0.5
    return (abs(x - cx) / (tw / 2.0) + abs(y - cy) / (th / 2.0)) <= 1.0


def diamond_dist(x, y, tw=TILE_W, th=TILE_H):
    cx, cy = tw / 2.0 - 0.5, th / 2.0 - 0.5
    return abs(x - cx) / (tw / 2.0) + abs(y - cy) / (th / 2.0)


def apply_diamond_mask(img, border_color):
    w, h = img.size
    px = img.load()
    for y in range(h):
        for x in range(w):
            d = diamond_dist(x, y, w, h)
            if d > 1.0:
                px[x, y] = (0, 0, 0, 0)
            elif d >= 0.94:
                r, g, b, a = px[x, y]
                br, bg, bb, ba = border_color
                px[x, y] = (int(r * 0.4 + br * 0.6), int(g * 0.4 + bg * 0.6), int(b * 0.4 + bb * 0.6), 255)


def make_noise_tile(name, base, seed, mortar=None, variant=0.12, pattern="grain", border=None, glow=None):
    img = Image.new("RGBA", (TILE_W, TILE_H), (0, 0, 0, 0))
    px = img.load()
    rnd = random.Random(seed)
    br, bg, bb, _ = base
    mortar = mortar or shade(base, 0.4)
    for y in range(TILE_H):
        for x in range(TILE_W):
            if not is_inside_diamond(x, y):
                continue
            n = rnd.uniform(-variant, variant)
            r = max(0, min(255, int(br * (1 + n))))
            g = max(0, min(255, int(bg * (1 + n))))
            b = max(0, min(255, int(bb * (1 + n))))

            if pattern == "grain":
                px[x, y] = (r, g, b, 255)
            elif pattern == "planks":
                if (y // 6) % 2 == 0 and (x % 22) < 2:
                    px[x, y] = mortar
                else:
                    px[x, y] = (r, g, b, 255)
            elif pattern == "cracked":
                gx = (x + y) % 26
                gy = (x - y) % 22
                if gx < 2 or gy < 2:
                    px[x, y] = mortar
                else:
                    px[x, y] = (r, g, b, 255)
            elif pattern == "hex":
                gx = (x + (y // 8) * 7) % 20
                if gx < 2:
                    px[x, y] = mortar
                else:
                    px[x, y] = (r, g, b, 255)
            elif pattern == "veined":
                d = diamond_dist(x, y)
                vein = abs((x * 2 + y * 3) % 40 - 20)
                if vein < 2 and d < 0.85:
                    px[x, y] = glow or shade(base, 1.6)
                else:
                    px[x, y] = (r, g, b, 255)
            else:
                px[x, y] = (r, g, b, 255)

    apply_diamond_mask(img, border or shade(base, 0.35))
    save_asset(img, name)
    print(f"  Saved tile: {name}")


TILES = [
    # Meadow set — Fen and Grove
    ("tile_meadow_reed.png", hx("#5c7a3e"), 501, "planks", shade(hx("#5c7a3e"), 0.4), None),
    ("tile_meadow_mud.png", hx("#4a3a2a"), 502, "grain", shade(hx("#4a3a2a"), 0.4), None),
    ("tile_meadow_path.png", hx("#8a7050"), 503, "cracked", shade(hx("#8a7050"), 0.35), None),
    ("tile_grove_moss.png", hx("#2f5a34"), 504, "grain", shade(hx("#2f5a34"), 0.4), None),
    # Sanctum / water set
    ("tile_sanctum_flooded.png", hx("#2c5a78"), 505, "grain", shade(hx("#2c5a78"), 0.4), None),
    ("tile_sanctum_marble.png", hx("#c9c4b8"), 506, "cracked", shade(hx("#c9c4b8"), 0.5), None),
    ("tile_sanctum_algae.png", hx("#3a5a3e"), 507, "grain", shade(hx("#3a5a3e"), 0.4), None),
    ("tile_sanctum_glass.png", hx("#7fd8e8"), 508, "veined", shade(hx("#7fd8e8"), 0.5), (255, 250, 220, 255)),
    # Spire set
    ("tile_spire_ash.png", hx("#4a4038"), 509, "grain", shade(hx("#4a4038"), 0.4), None),
    ("tile_spire_emberglass.png", hx("#241414"), 510, "veined", shade(hx("#241414"), 0.4), (255, 120, 40, 255)),
    ("tile_spire_basalt.png", hx("#3a3a40"), 511, "hex", shade(hx("#3a3a40"), 0.4), None),
    # Chasm / ice set — new category `ice`
    ("tile_ice_packed.png", hx("#c8e0ea"), 512, "grain", shade(hx("#c8e0ea"), 0.5), None),
    ("tile_ice_blue.png", hx("#5aa8d8"), 513, "veined", shade(hx("#5aa8d8"), 0.4), (220, 245, 255, 255)),
    ("tile_ice_crevasse.png", hx("#1a3a4a"), 514, "cracked", shade(hx("#1a3a4a"), 0.35), None),
    ("tile_ice_mirror.png", hx("#e8f4fb"), 515, "veined", shade(hx("#e8f4fb"), 0.55), (255, 255, 255, 255)),
    # Rootways set — new category `root`
    ("tile_root_bark.png", hx("#4a3626"), 516, "planks", shade(hx("#4a3626"), 0.4), None),
    ("tile_root_bonemeal.png", hx("#cfc8b0"), 517, "grain", shade(hx("#cfc8b0"), 0.4), None),
    ("tile_root_sap.png", hx("#7a5a1a"), 518, "veined", shade(hx("#7a5a1a"), 0.4), (230, 190, 60, 255)),
    ("tile_root_terrace.png", hx("#5a1e22"), 519, "hex", shade(hx("#5a1e22"), 0.4), None),
]


def generate_tiles():
    print(f"=== TASK D: Generating {len(TILES)} new iso floor tiles ===")
    for name, base, seed, pattern, border, glow in TILES:
        make_noise_tile(name, base, seed, pattern=pattern, border=border, glow=glow)


# =============================================================================
# TASK E — Environmental props (38), exact W x H per ASSET_MANIFEST.md
# =============================================================================
def new_canvas(w, h):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)


def prop_pillar(name, w, h, anchor, c_main, c_dark, c_accent, glow=None, taper=0.35):
    img, draw = new_canvas(w, h)
    ax, ay = anchor
    draw_shadow(draw, (ax, ay + 4), int(w * 0.32), int(h * 0.05), 100)
    base_w = w * 0.5
    top_w = base_w * (1 - taper)
    bx0, bx1 = ax - base_w / 2, ax + base_w / 2
    tx0, tx1 = ax - top_w / 2, ax + top_w / 2
    top_y = h * 0.05
    draw.polygon([(bx0, ay), (bx1, ay), (tx1, top_y), (tx0, top_y)], fill=c_main, outline=c_dark)
    draw.line([(ax, ay), (ax, top_y)], fill=c_dark, width=2)
    for f in (0.25, 0.5, 0.75):
        yy = top_y + (ay - top_y) * f
        ww = (tx1 - tx0) + (bx1 - bx0 - (tx1 - tx0)) * f
        draw.line([(ax - ww / 2, yy), (ax + ww / 2, yy)], fill=c_accent, width=1)
    if glow:
        draw.ellipse([ax - w * 0.12, top_y - w * 0.06, ax + w * 0.12, top_y + w * 0.12], fill=glow)
    save_asset(img, name)


def prop_banner(name, w, h, anchor, c_main, c_dark, c_accent):
    img, draw = new_canvas(w, h)
    ax, ay = anchor
    draw_shadow(draw, (ax, ay + 3), int(w * 0.2), int(h * 0.04), 90)
    draw.line([(ax, ay), (ax, h * 0.05)], fill=c_dark, width=3)
    cloth_top = h * 0.08
    cloth = [(ax - w * 0.28, cloth_top), (ax + w * 0.28, cloth_top),
             (ax + w * 0.22, ay - h * 0.05), (ax, ay), (ax - w * 0.22, ay - h * 0.05)]
    draw.polygon(cloth, fill=c_main, outline=c_dark)
    for i in range(3):
        yy = cloth_top + (ay - cloth_top) * (0.25 + i * 0.25)
        draw.line([(ax - w * 0.18, yy), (ax + w * 0.18, yy)], fill=c_accent, width=2)
    save_asset(img, name)


def prop_organic_tree(name, w, h, anchor, c_trunk, c_trunk_dark, c_leaf, c_leaf_hl, canopy_scale=1.0):
    img, draw = new_canvas(w, h)
    ax, ay = anchor
    draw_shadow(draw, (ax, ay), int(w * 0.32), int(h * 0.06), 100)
    trunk_w = w * 0.1
    draw.polygon([(ax - trunk_w, ay), (ax + trunk_w, ay), (ax + trunk_w * 0.6, ay - h * 0.45),
                  (ax - trunk_w * 0.6, ay - h * 0.45)], fill=c_trunk, outline=c_trunk_dark)
    cy = ay - h * 0.55
    cr = w * 0.42 * canopy_scale
    draw.ellipse([ax - cr, cy - cr * 0.85, ax + cr, cy + cr * 0.55], fill=shade(c_leaf, 0.75))
    draw.ellipse([ax - cr * 0.8, cy - cr, ax + cr * 0.55, cy + cr * 0.15], fill=c_leaf)
    draw.ellipse([ax - cr * 0.35, cy - cr * 1.1, ax + cr * 0.75, cy - cr * 0.15], fill=c_leaf_hl)
    save_asset(img, name)


def prop_figure(name, w, h, anchor, c_body, c_dark, c_accent, horns=False, large=False):
    img, draw = new_canvas(w, h)
    ax, ay = anchor
    draw_shadow(draw, (ax, ay), int(w * 0.3), int(h * 0.06), 105)
    body_w = w * 0.34
    draw.polygon([(ax - body_w, ay), (ax + body_w, ay), (ax + body_w * 0.8, ay - h * 0.55),
                  (ax - body_w * 0.8, ay - h * 0.55)], fill=c_body, outline=c_dark)
    head_r = w * 0.18
    hy = ay - h * 0.62
    draw.ellipse([ax - head_r, hy - head_r, ax + head_r, hy + head_r], fill=c_body, outline=c_dark)
    if horns:
        draw.polygon([(ax - head_r * 0.6, hy - head_r), (ax - head_r * 1.6, hy - head_r * 2.2),
                      (ax - head_r * 0.3, hy - head_r * 0.3)], fill=c_accent)
        draw.polygon([(ax + head_r * 0.6, hy - head_r), (ax + head_r * 1.6, hy - head_r * 2.2),
                      (ax + head_r * 0.3, hy - head_r * 0.3)], fill=c_accent)
    draw.rectangle([ax - body_w * 0.9, ay - h * 0.18, ax + body_w * 0.9, ay - h * 0.02], fill=c_accent)
    if large:
        draw.ellipse([ax - w * 0.4, ay - h * 0.7, ax + w * 0.4, ay + h * 0.05], outline=shade(c_body, 1.5), width=2)
    save_asset(img, name)


def prop_hazard_glow(name, w, h, anchor, c_base, c_glow):
    img, draw = new_canvas(w, h)
    ax, ay = anchor
    draw.ellipse([ax - w * 0.42, ay - h * 0.16, ax + w * 0.42, ay + h * 0.16], fill=shade(c_base, 0.5))
    inner = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    idraw = ImageDraw.Draw(inner)
    idraw.ellipse([ax - w * 0.32, ay - h * 0.12, ax + w * 0.32, ay + h * 0.12], fill=c_glow)
    inner = inner.filter(ImageFilter.GaussianBlur(2))
    img.alpha_composite(inner)
    draw.ellipse([ax - w * 0.16, ay - h * 0.06, ax + w * 0.16, ay + h * 0.06], fill=shade(c_glow, 1.3))
    save_asset(img, name)


def prop_overhead(name, w, h, anchor, c_main, c_dark, c_accent):
    img, draw = new_canvas(w, h)
    ax, ay = anchor
    draw.line([(ax - w * 0.4, ay), (ax + w * 0.4, ay)], fill=c_dark, width=2)
    n = 4
    for i in range(n):
        x = ax - w * 0.35 + i * (w * 0.7 / (n - 1))
        draw.line([(x, ay), (x, ay + h * 0.35)], fill=c_dark, width=2)
        draw.ellipse([x - w * 0.06, ay + h * 0.3, x + w * 0.06, ay + h * 0.45], fill=c_main, outline=c_accent)
    save_asset(img, name)


def prop_container(name, w, h, anchor, c_main, c_dark, c_accent):
    img, draw = new_canvas(w, h)
    ax, ay = anchor
    draw_shadow(draw, (ax, ay), int(w * 0.32), int(h * 0.06), 105)
    bw, bh = w * 0.5, h * 0.55
    top = ay - bh
    draw.polygon([(ax - bw / 2, ay), (ax + bw / 2, ay), (ax + bw / 2, top), (ax - bw / 2, top)],
                 fill=c_main, outline=c_dark)
    draw.polygon([(ax - bw / 2, top), (ax + bw / 2, top), (ax + bw / 2 - bw * 0.1, top - h * 0.1),
                  (ax - bw / 2 + bw * 0.1, top - h * 0.1)], fill=c_accent, outline=c_dark)
    for f in (0.3, 0.6, 0.9):
        draw.line([(ax - bw / 2, ay - bh * f), (ax + bw / 2, ay - bh * f)], fill=shade(c_main, 0.7), width=1)
    save_asset(img, name)


def prop_wall(name, w, h, anchor, c_main, c_dark, c_accent):
    img, draw = new_canvas(w, h)
    ax, ay = anchor
    draw_shadow(draw, (ax, ay), int(w * 0.4), int(h * 0.06), 100)
    draw.polygon([(ax - w * 0.46, ay), (ax + w * 0.46, ay), (ax + w * 0.46, ay - h * 0.7),
                  (ax - w * 0.46, ay - h * 0.7)], fill=c_main, outline=c_dark)
    for i in range(4):
        x = ax - w * 0.46 + i * (w * 0.92 / 3)
        draw.line([(x, ay), (x, ay - h * 0.7)], fill=c_dark, width=2)
    draw.polygon([(ax - w * 0.5, ay - h * 0.7), (ax + w * 0.5, ay - h * 0.7),
                  (ax + w * 0.4, ay - h * 0.82), (ax - w * 0.4, ay - h * 0.82)], fill=c_accent, outline=c_dark)
    save_asset(img, name)


PROPS = [
    # --- Aethelgard districts (16) ---
    ("env_obelisk_aetherite.png", 96, 192, (48, 176), "pillar",
     dict(c_main=hx("#c9c2a0"), c_dark=hx("#7a755a"), c_accent=hx("#e8e0b0"), glow=(255, 250, 200, 140), taper=0.5)),
    ("env_notice_board.png", 64, 64, (32, 52), "container",
     dict(c_main=hx("#8a6a45"), c_dark=hx("#4a3620"), c_accent=hx("#d8c8a0"))),
    ("env_awning_stall.png", 96, 96, (48, 64), "overhead",
     dict(c_main=hx("#b03a3a"), c_dark=hx("#5a1a1a"), c_accent=hx("#e8e0d0"))),
    ("env_crate_stack_tall.png", 64, 96, (32, 82), "container",
     dict(c_main=hx("#a07840"), c_dark=hx("#5a3c1c"), c_accent=hx("#c89858"))),
    ("env_forge_anvil.png", 64, 64, (32, 50), "container",
     dict(c_main=hx("#3a3a40"), c_dark=hx("#18181c"), c_accent=hx("#c04020"))),
    ("env_guild_banner.png", 64, 128, (32, 116), "banner",
     dict(c_main=hx("#8a2020"), c_dark=hx("#3a0c0c"), c_accent=hx("#d8b040"))),
    ("env_chimney_stack.png", 64, 160, (32, 148), "pillar",
     dict(c_main=hx("#6a5548"), c_dark=hx("#332822"), c_accent=hx("#8a7060"), taper=0.15)),
    ("env_temple_pillar.png", 64, 160, (32, 148), "pillar",
     dict(c_main=hx("#e8e2d0"), c_dark=hx("#a09878"), c_accent=hx("#fff6c8"), taper=0.1)),
    ("env_stained_arch.png", 128, 160, (64, 146), "wall",
     dict(c_main=hx("#c9c4b0"), c_dark=hx("#847e68"), c_accent=hx("#7fd8e8"))),
    ("env_prayer_candles.png", 64, 64, (32, 54), "hazard",
     dict(c_base=hx("#8a7040"), c_glow=hx("#ffe082"))),
    ("env_lantern_string.png", 128, 64, (64, 20), "overhead",
     dict(c_main=hx("#ffcc66"), c_dark=hx("#7a5a20"), c_accent=hx("#ffe8a8"))),
    ("env_house_terrace.png", 128, 128, (64, 98), "wall",
     dict(c_main=hx("#b08858"), c_dark=hx("#5a4028"), c_accent=hx("#7a4a2a"))),
    ("env_washing_line.png", 96, 64, (48, 24), "overhead",
     dict(c_main=hx("#eae4d4"), c_dark=hx("#8a8470"), c_accent=hx("#c9c2a0"))),
    ("env_well_stone.png", 64, 64, (32, 50), "container",
     dict(c_main=hx("#8a8a90"), c_dark=hx("#45454c"), c_accent=hx("#3a6a90"))),
    ("env_dock_piling.png", 64, 96, (32, 84), "pillar",
     dict(c_main=hx("#5a4530"), c_dark=hx("#2c2016"), c_accent=hx("#7a6040"), taper=0.05)),
    ("env_cargo_crane.png", 128, 192, (64, 178), "wall",
     dict(c_main=hx("#6a5a3a"), c_dark=hx("#332c1c"), c_accent=hx("#c9a840"))),
    # --- Wilderness (14) ---
    ("env_fishing_net.png", 64, 64, (32, 48), "overhead",
     dict(c_main=hx("#c9bfa0"), c_dark=hx("#6a6248"), c_accent=hx("#e8e0c0"))),
    ("env_rowboat.png", 96, 64, (48, 52), "container",
     dict(c_main=hx("#7a5a38"), c_dark=hx("#3a2a18"), c_accent=hx("#a07848"))),
    ("env_windmill.png", 160, 224, (80, 206), "pillar",
     dict(c_main=hx("#d8cfa8"), c_dark=hx("#8a8058"), c_accent=hx("#eae0c0"), taper=0.45)),
    ("env_fence_rail.png", 64, 64, (32, 50), "wall",
     dict(c_main=hx("#8a6a45"), c_dark=hx("#4a3620"), c_accent=hx("#c89858"))),
    ("env_scarecrow.png", 64, 96, (32, 86), "figure",
     dict(c_body=hx("#c9a24a"), c_dark=hx("#6a5020"), c_accent=hx("#8a4a20"))),
    ("env_palisade_wall.png", 96, 128, (48, 116), "wall",
     dict(c_main=hx("#7a5a38"), c_dark=hx("#3a2a18"), c_accent=hx("#a07848"))),
    ("env_campfire.png", 64, 64, (32, 52), "hazard",
     dict(c_base=hx("#3a2a1a"), c_glow=hx("#ff8c30"))),
    ("env_reed_clump.png", 64, 64, (32, 50), "organic",
     dict(c_trunk=hx("#5c7a3e"), c_trunk_dark=hx("#345020"), c_leaf=hx("#6c8f48"), c_leaf_hl=hx("#a8c878"), canopy_scale=0.55)),
    ("env_hollow_tree.png", 128, 192, (64, 178), "organic",
     dict(c_trunk=hx("#4a3626"), c_trunk_dark=hx("#241a10"), c_leaf=hx("#2f5a34"), c_leaf_hl=hx("#5a8a55"), canopy_scale=1.3)),
    ("env_waterfall_curtain.png", 96, 160, (48, 150), "hazard",
     dict(c_base=hx("#1a3a4a"), c_glow=hx("#bfe8ff"))),
    ("env_pew_floating.png", 96, 64, (48, 50), "container",
     dict(c_main=hx("#5a4a3a"), c_dark=hx("#2a2018"), c_accent=hx("#8a7458"))),
    ("env_reliquary_casket.png", 64, 64, (32, 52), "container",
     dict(c_main=hx("#c9c2a0"), c_dark=hx("#7a755a"), c_accent=hx("#fff59d"))),
    ("env_lava_channel.png", 64, 64, (32, 40), "hazard",
     dict(c_base=hx("#3a1a10"), c_glow=hx("#ff7043"))),
    ("env_bellows_great.png", 128, 128, (64, 116), "wall",
     dict(c_main=hx("#6a4a3a"), c_dark=hx("#332418"), c_accent=hx("#c04020"))),
    # --- Chasm & Rootways (8) ---
    ("env_ice_statue.png", 64, 128, (32, 116), "figure",
     dict(c_body=hx("#c8e0ea"), c_dark=hx("#7a95a2"), c_accent=hx("#eaf6fb"))),
    ("env_ice_colossus_shell.png", 128, 192, (64, 178), "figure",
     dict(c_body=hx("#9fb8c4"), c_dark=hx("#556a72"), c_accent=hx("#d8ecf4"), large=True)),
    ("env_cairn_waypoint.png", 64, 96, (32, 84), "pillar",
     dict(c_main=hx("#8a8a90"), c_dark=hx("#45454c"), c_accent=hx("#c8e0ea"), taper=0.55)),
    ("env_guide_rope.png", 96, 64, (48, 30), "overhead",
     dict(c_main=hx("#a08858"), c_dark=hx("#5a4a2c"), c_accent=hx("#c9b078"))),
    ("env_vault_door.png", 128, 160, (64, 148), "wall",
     dict(c_main=hx("#5a6a72"), c_dark=hx("#2c3438"), c_accent=hx("#d8a840"))),
    ("env_root_hair.png", 64, 128, (32, 24), "overhead",
     dict(c_main=hx("#3a2c4a"), c_dark=hx("#1a1428"), c_accent=hx("#7e57c2"))),
    ("env_weeping_branch.png", 128, 160, (64, 40), "overhead",
     dict(c_main=hx("#5a3c28"), c_dark=hx("#2c1c12"), c_accent=hx("#9ccc65"))),
    ("env_briar_wall.png", 96, 128, (48, 116), "wall",
     dict(c_main=hx("#403050"), c_dark=hx("#201828"), c_accent=hx("#7e57c2"))),
]

PROP_FN = {
    "pillar": prop_pillar,
    "banner": prop_banner,
    "organic": prop_organic_tree,
    "figure": prop_figure,
    "hazard": prop_hazard_glow,
    "overhead": prop_overhead,
    "container": prop_container,
    "wall": prop_wall,
}


def generate_props():
    print(f"=== TASK E: Generating {len(PROPS)} new environmental props ===")
    for name, w, h, anchor, kind, kwargs in PROPS:
        PROP_FN[kind](name, w, h, anchor, **kwargs)
        print(f"  Saved prop: {name} ({w}x{h})")


def verify():
    print("\n=== Verification ===")
    expected = [t[0] for t in TILES] + [p[0] for p in PROPS]
    ok = True
    for d in TARGET_DIRS:
        for name in expected:
            path = os.path.join(d, name)
            if not os.path.exists(path):
                print(f"  MISSING: {path}")
                ok = False
    print(f"Total expected files per dir: {len(expected)} (19 tiles + 38 props = 57)")
    print("ALL OK" if ok else "SOME FILES FAILED VERIFICATION")
    return ok


if __name__ == "__main__":
    generate_tiles()
    generate_props()
    verify()
