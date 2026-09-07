#!/usr/bin/env python3
"""Zone parallax placeholder pack — Zaggers RESEARCH + PACK.

RESEARCH baseline (vault/WORLD_LORE.md + web/index.html + tools/ + vault docs):
- 7 zones from ZONE_ATMOSPHERE (web/index.html:993-1001):
    aethelgard town neutral (tint null) — citadel + Aetherite Obelisk hub
    gatewatch warm 255,224,178 @0.05 source-over — dawn commons/palisade
    meadows (Whispering Meadows Lv1-15) warm 255,238,170 @0.10 source-over — emerald hills/sunlight
    sanctum (Sunken Sanctum Lv15-30) teal 30,110,120 @0.22 multiply — submerged ruins/turquoise glow
    spire (Obsidian Spire Lv30-50) crimson 160,40,20 @0.20 multiply — volcanic peak/obsidian tower/lava
    chasm (Glacial Chasm Lv50-70) icy 150,195,255 @0.20 multiply — blizzard canyon/frozen statues
    rootways (Realm of Baphomet Lv70+) purple 80,25,105 @0.30 multiply — world-tree roots/shadow domain
- Web parallax needs: 3 layers x 7 zones = 21 PNGs, tileable X (left col == right col),
  horizon-fixed Y (silhouettes bottom-anchored, transparent sky above for mid/near),
  parallax factors far 0.15 / mid 0.35 / near 0.6.
- GIMP norms (tools/gimp_batch_cleanup.py): RGBA, outline OUTLINE_TARGET=(16,16,32),
  drop-shadow convention 40% black (N/A for bg — no ground shadow; outline honored on silhouette top edges).
- Aseprite conventions (vault/PIPELINE_AND_TOOLS.md + ART_PIPELINE_REPORT.md):
    shipped canonical = 128x64 iso diamond tiles + 256x256 sheets of 64x64 cells.
    BG pack uses web-native strip sizes far 640x180 / mid 640x140 / near 640x120
    (wide strips, NOT tiles/sheets — documented deviation, needed for parallax scroll).
- Style: PIL only, no external assets, flat fills + hard edges (pixelated-friendly,
  coords snapped to 2px grid, NEAREST-only), seamless X-wrap via half-width mirror.

Dual-writes assets/bg/ + web/assets/bg/ + manifest.json in both. Verifies tileability + parity.
Usage: python scripts/generate_bg_parallax.py [--root DIR] [--check-only]
"""
import argparse, hashlib, json, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) or ".")

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("ERROR: Pillow required: pip install Pillow", file=sys.stderr); sys.exit(2)

OUTLINE = (16, 16, 32, 255)
FAR_SIZE = (640, 180)
MID_SIZE = (640, 140)
NEAR_SIZE = (640, 120)
FACTORS = {"far": 0.15, "mid": 0.35, "near": 0.6}
ZONES = ["aethelgard", "gatewatch", "meadows", "sanctum", "spire", "chasm", "rootways"]

# palette-matched to ZONE_ATMOSPHERE tints + WORLD_LORE moods
PAL = {
 "aethelgard": dict(sky_top=(110,160,215), sky_bot=(216,232,245),
    far=(107,126,154), mid=(78,94,122), near=(46,52,64),
    glow=(255,240,200)),
 "gatewatch": dict(sky_top=(138,168,208), sky_bot=(245,217,168),
    far=(138,122,106), mid=(107,91,74), near=(58,51,64),
    glow=(255,224,178)),
 "meadows": dict(sky_top=(110,198,232), sky_bot=(255,242,176),
    far=(127,184,106), mid=(78,154,78), near=(30,90,46),
    glow=(255,238,170)),
 "sanctum": dict(sky_top=(14,46,58), sky_bot=(46,138,138),
    far=(42,90,98), mid=(28,62,70), near=(14,34,40),
    glow=(91,232,216)),
 "spire": dict(sky_top=(42,14,14), sky_bot=(192,64,32),
    far=(74,26,26), mid=(42,16,14), near=(20,8,8),
    glow=(255,138,80)),
 "chasm": dict(sky_top=(106,138,181), sky_bot=(216,232,255),
    far=(154,181,216), mid=(94,126,166), near=(42,58,85),
    glow=(255,255,255)),
 "rootways": dict(sky_top=(26,14,42), sky_bot=(90,42,122),
    far=(58,30,85), mid=(42,20,64), near=(18,10,30),
    glow=(193,123,224)),
}

def snap(v, g=2): return int(round(v / g) * g)

def vgrad(w, h, top, bot):
    img = Image.new("RGBA", (w, h), (0,0,0,0))
    px = img.load()
    for y in range(h):
        t = y / max(1, h-1)
        c = tuple(int(top[i]+(bot[i]-top[i])*t) for i in range(3)) + (255,)
        for x in range(w): px[x,y] = c
    return img

def outline_top(draw, pts, w, h):
    # 1px outline along silhouette top edge Sequential segments
    for i in range(len(pts)-1):
        draw.line([pts[i], pts[i+1]], fill=OUTLINE, width=1)

def half_canvas(w2, h): return Image.new("RGBA", (w2, h), (0,0,0,0))

def mirror_to_full(half):
    w2, h = half.size
    full = Image.new("RGBA", (w2*2, h), (0,0,0,0))
    full.paste(half, (0,0))
    full.paste(half.transpose(Image.FLIP_LEFT_RIGHT), (w2,0))
    return full

def rng_for(zone, layer):
    import hashlib as _hl
    seed = int.from_bytes(_hl.md5(f"{zone}/{layer}".encode()).digest()[:4], "little")
    return random.Random(seed)

# ---- silhouette painters (operate on HALF width 320 canvas) ----
def paint_far(zone, d, w2, h, P, R):
    base = h - snap(h*0.34)
    if zone in ("aethelgard",):
        # town towers + obelisk skyline
        pts=[(0,h),(0,base)]
        x=0
        while x < w2:
            tw = snap(R.randint(18,40)); th = snap(R.randint(10,44))
            pts += [(x,base),(x,base-th),(x+tw,base-th),(x+tw,base-th+snap(6)),(x+tw,base)]
            x += tw + snap(R.randint(4,14))
        pts += [(w2,h)]
        d.polygon(pts, fill=P["far"]+(255,))
        outline_top(d, pts[1:-1], w2, h)
        # obelisk spike center-left + windows
        ox = snap(w2*0.32)
        d.polygon([(ox-8,h),(ox-8,base-64),(ox,h//4),(ox+8,base-64),(ox+8,h)], fill=P["mid"]+(255,))
        d.rectangle([ox-2, base-56, ox+2, base-10], fill=P["glow"]+(255,))
    elif zone == "gatewatch":
        pts=[(0,h),(0,base)]
        x=0
        while x < w2:
            tw=snap(R.randint(30,60)); th=snap(R.randint(8,26))
            pts += [(x,base-th),(x+tw//2,base-th-snap(R.randint(2,8))),(x+tw,base-th)]
            x+=tw
        pts += [(w2,base),(w2,h)]
        d.polygon(pts, fill=P["far"]+(255,)); outline_top(d, pts[1:-1], w2, h)
        # distant palisade posts
        for x in range(0, w2, snap(16)):
            d.rectangle([x, base-snap(12), x+snap(4), base], fill=P["mid"]+(255,))
    elif zone == "meadows":
        for k, (col, off, amp) in enumerate([(P["far"],0,26),(P["mid"],10,18)]):
            b = base + snap(k*10)
            pts=[(0,h),(0,b)]
            for x in range(0, w2+8, snap(16)):
                y = b - snap(abs(((x*37+k*101)%40)/40.0)*amp)
                pts.append((x,y))
            pts += [(w2,h)]
            d.polygon(pts, fill=col+(255,))
            outline_top(d, pts[1:-1], w2, h)
    elif zone == "sanctum":
        pts=[(0,h),(0,base)]
        x=0
        while x < w2:
            tw=snap(R.randint(24,48)); th=snap(R.randint(14,40))
            # broken ruin blocks
            pts += [(x,base),(x,base-th),(x+tw,base-th),(x+tw,base)]
            x+=tw+snap(R.randint(2,10))
        pts += [(w2,h)]
        d.polygon(pts, fill=P["far"]+(255,)); outline_top(d, pts[1:-1], w2, h)
        for i in range(6):
            cx=snap(R.randint(8,w2-8)); d.polygon([(cx,base-snap(R.randint(18,40))),(cx-4,base),(cx+4,base)], fill=P["glow"]+(255,))
    elif zone == "spire":
        pts=[(0,h),(0,base)]
        x=0
        while x < w2:
            tw=snap(R.randint(28,56)); th=snap(R.randint(24,64))
            pts += [(x,base),(x+tw//2,base-th),(x+tw,base)]
            x+=tw
        pts += [(w2,h)]
        d.polygon(pts, fill=P["far"]+(255,)); outline_top(d, pts[1:-1], w2, h)
        # ember dots in sky
        for i in range(14):
            ex=R.randint(0,w2-1); ey=R.randint(4,base-10)
            d.rectangle([ex,ey,ex+1,ey+1], fill=P["glow"]+(255,))
    elif zone == "chasm":
        pts=[(0,h),(0,base)]
        x=0
        while x < w2:
            tw=snap(R.randint(30,60)); th=snap(R.randint(26,66))
            pts += [(x,base),(x+tw//2,base-th),(x+tw,base)]
            x+=tw
        pts += [(w2,h)]
        d.polygon(pts, fill=P["far"]+(255,)); outline_top(d, pts[1:-1], w2, h)
        # snow caps
        for x in range(0,w2,snap(32)):
            d.polygon([(x,base-snap(20)),(x+snap(8),base-snap(28)),(x+snap(16),base-snap(20))], fill=(255,255,255,255))
    else: # rootways
        pts=[(0,h),(0,base)]
        x=0
        while x < w2:
            tw=snap(R.randint(20,44)); th=snap(R.randint(16,48))
            pts += [(x,base),(x+tw//2,base-th),(x+tw,base)]
            x+=tw+snap(4)
        pts += [(w2,h)]
        d.polygon(pts, fill=P["far"]+(255,)); outline_top(d, pts[1:-1], w2, h)
        for i in range(8):
            ex=R.randint(0,w2-1); ey=R.randint(4,base-6)
            d.rectangle([ex,ey,ex+1,ey+1], fill=P["glow"]+(255,))

def paint_mid(zone, d, w2, h, P, R):
    base = h
    top = snap(h*0.34)
    if zone == "aethelgard":
        y0=top+snap(10)
        d.rectangle([0,y0,w2,h], fill=P["mid"]+(255,))
        d.line([(0,y0),(w2,y0)], fill=OUTLINE, width=1)
        for x in range(snap(6), w2, snap(36)): # houses w/ roofs
            hw=snap(24); hh=snap(R.randint(26,44))
            d.rectangle([x,h-hh,x+hw,h], fill=P["mid"]+(255,))
            d.polygon([(x-2,h-hh),(x+hw//2,h-hh-snap(12)),(x+hw+2,h-hh)], fill=P["near"]+(255,))
            d.rectangle([x+snap(8),h-hh+snap(8),x+snap(12),h-hh+snap(14)], fill=P["glow"]+(255,))
        d.line([(0,y0),(w2,y0)], fill=OUTLINE, width=1)
    elif zone == "gatewatch":
        y0=top+snap(14)
        pts=[(0,h),(0,y0)]
        for x in range(0,w2+8,snap(24)): pts.append((x, y0-snap(R.randint(0,10))))
        pts += [(w2,h)]
        d.polygon(pts, fill=P["mid"]+(255,)); outline_top(d, pts[1:-1], w2, h)
        for x in range(0,w2,snap(20)): # palisade wall
            d.rectangle([x,y0-snap(22),x+snap(8),h-snap(6)], fill=P["near"]+(255,))
            d.polygon([(x,y0-snap(22)),(x+snap(4),y0-snap(28)),(x+snap(8),y0-snap(22))], fill=P["near"]+(255,))
    elif zone == "meadows":
        y0=top+snap(12)
        pts=[(0,h),(0,y0)]
        for x in range(0,w2+8,snap(20)): pts.append((x, y0-snap(R.randint(0,14))))
        pts += [(w2,h)]
        d.polygon(pts, fill=P["mid"]+(255,)); outline_top(d, pts[1:-1], w2, h)
        for i in range(7): # peaks/haystacks
            cx=snap(R.randint(10,w2-10)); d.polygon([(cx-snap(14),h),(cx,h-snap(R.randint(26,40))),(cx+snap(14),h)], fill=P["near"]+(255,))
    elif zone == "sanctum":
        y0=top+snap(10)
        d.rectangle([0,y0,w2,h], fill=(0,0,0,0))
        pts=[(0,h),(0,y0+snap(8))]
        for x in range(0,w2+8,snap(28)): pts.append((x, y0+snap(R.randint(0,12))))
        pts += [(w2,h)]
        d.polygon(pts, fill=P["mid"]+(255,)); outline_top(d, pts[1:-1], w2, h)
        for i in range(6): # crystal spires
            cx=snap(R.randint(8,w2-8)); ch=snap(R.randint(30,58))
            d.polygon([(cx-6,h),(cx-6,h-ch),(cx,h-ch-snap(10)),(cx+6,h-ch),(cx+6,h)], fill=P["mid"]+(255,))
            d.polygon([(cx-2,h-ch),(cx,h-ch-snap(10)),(cx+2,h-ch)], fill=P["glow"]+(255,))
            d.line([(cx-6,h-ch),(cx,h-ch-snap(10)),(cx+6,h-ch)], fill=OUTLINE, width=1)
    elif zone == "spire":
        y0=top+snap(8)
        pts=[(0,h),(0,y0+snap(20))]
        x=0
        while x < w2:
            tw=snap(R.randint(26,52)); th=snap(R.randint(34,66))
            pts += [(x,y0+snap(20)),(x+tw//2,y0+snap(20)-th),(x+tw,y0+snap(20))]
            x+=tw
        pts += [(w2,h)]
        d.polygon(pts, fill=P["mid"]+(255,)); outline_top(d, pts[1:-1], w2, h)
        # lava cracks
        for i in range(5):
            cx=snap(R.randint(10,w2-10))
            d.rectangle([cx,h-snap(24),cx+snap(3),h-snap(4)], fill=P["glow"]+(255,))
    elif zone == "chasm":
        y0=top+snap(12)
        pts=[(0,h),(0,y0)]
        for x in range(0,w2+8,snap(26)): pts.append((x, y0-snap(R.randint(0,16))))
        pts += [(w2,h)]
        d.polygon(pts, fill=P["mid"]+(255,)); outline_top(d, pts[1:-1], w2, h)
        for i in range(4): # frozen statues
            cx=snap(R.randint(12,w2-12))
            d.rectangle([cx-4,h-snap(44),cx+4,h-snap(10)], fill=(220,235,255,255))
            d.ellipse([cx-7,h-snap(52),cx+7,h-snap(40)], fill=(220,235,255,255))
    else:
        y0=top+snap(10)
        pts=[(0,h),(0,y0+snap(14))]
        for x in range(0,w2+8,snap(22)): pts.append((x, y0+snap(R.randint(0,14))))
        pts += [(w2,h)]
        d.polygon(pts, fill=P["mid"]+(255,)); outline_top(d, pts[1:-1], w2, h)
        for i in range(6): # twisted spires/roots
            cx=snap(R.randint(8,w2-8)); ch=snap(R.randint(30,56))
            d.rectangle([cx-3,h-ch,cx+3,h], fill=P["near"]+(255,))
            d.ellipse([cx-6,h-ch-8,cx+6,h-ch+4], fill=P["glow"]+(255,))

def paint_near(zone, d, w2, h, P, R):
    top = snap(h*0.44)
    if zone in ("meadows",):
        d.rectangle([0,h-snap(30),w2,h], fill=P["near"]+(255,))
        d.line([(0,h-snap(30)),(w2,h-snap(30))], fill=OUTLINE, width=1)
        for x in range(0,w2,snap(28)): # treeline blobs
            th=snap(R.randint(30,58))
            d.ellipse([x-2,h-th-14,x+snap(24),h-snap(18)], fill=P["near"]+(255,))
            d.rectangle([x+snap(8),h-snap(26),x+snap(12),h-snap(14)], fill=(40,26,18,255))
        d.line([(0,h-snap(30)),(w2,h-snap(30))], fill=OUTLINE, width=1)
    elif zone in ("aethelgard","gatewatch"):
        wall_h = snap(44); y0=h-wall_h
        d.rectangle([0,y0,w2,h], fill=P["near"]+(255,))
        d.line([(0,y0),(w2,y0)], fill=OUTLINE, width=1)
        for x in range(0,w2,snap(32)): # crenellations
            d.rectangle([x,y0-snap(8),x+snap(12),y0], fill=P["near"]+(255,))
        for x in range(snap(10),w2,snap(48)):
            d.rectangle([x,y0+snap(12),x+snap(8),y0+snap(22)], fill=P["glow"]+(255,))
    elif zone == "sanctum":
        y0=top
        d.rectangle([0,y0+snap(20),w2,h], fill=P["near"]+(255,))
        d.line([(0,y0+snap(20)),(w2,y0+snap(20))], fill=OUTLINE, width=1)
        for x in range(snap(4),w2,snap(40)): # pillars
            d.rectangle([x,y0,x+snap(14),h-snap(8)], fill=P["near"]+(255,))
            d.rectangle([x-2,y0,x+snap(16),y0+snap(6)], fill=P["mid"]+(255,))
            d.rectangle([x+snap(4),y0+snap(10),x+snap(10),y0+snap(30)], fill=P["glow"]+(255,))
    elif zone == "spire":
        y0=top+snap(6)
        pts=[(0,h),(0,y0+snap(16))]
        for x in range(0,w2+8,snap(24)): pts.append((x,y0+snap(R.randint(0,12))))
        pts += [(w2,h)]
        d.polygon(pts, fill=P["near"]+(255,)); outline_top(d, pts[1:-1], w2, h)
        for x in range(0,w2,snap(44)): # basalt columns + lava pool
            d.rectangle([x,y0+snap(20),x+snap(16),h], fill=(30,14,14,255))
            d.rectangle([x+snap(2),y0+snap(22),x+snap(5),h-snap(4)], fill=P["glow"]+(255,))
    elif zone == "chasm":
        y0=top+snap(4)
        pts=[(0,h),(0,y0+snap(18))]
        for x in range(0,w2+8,snap(26)): pts.append((x,y0+snap(R.randint(0,12))))
        pts += [(w2,h)]
        d.polygon(pts, fill=P["near"]+(255,)); outline_top(d, pts[1:-1], w2, h)
        for x in range(snap(6),w2,snap(52)): # icicles hanging? use shards up
            d.polygon([(x,h),(x+snap(8),y0-snap(2)),(x+snap(16),h)], fill=(200,225,255,255))
    else:
        y0=top
        d.rectangle([0,y0+snap(24),w2,h], fill=P["near"]+(255,))
        d.line([(0,y0+snap(24)),(w2,y0+snap(24))], fill=OUTLINE, width=1)
        for i in range(7): # hanging + rising roots
            cx=snap(R.randint(6,w2-6))
            d.rectangle([cx-3,y0,cx+3,h-snap(10)], fill=P["mid"]+(255,))
            if i%2==0:
                ex=cx+snap(R.randint(-8,8))
                d.ellipse([ex-3,y0+snap(R.randint(2,16)),ex+3,y0+snap(R.randint(18,28))], fill=P["glow"]+(255,))

def make_layer(zone, layer):
    P = PAL[zone]; R = rng_for(zone, layer)
    if layer=="far":
        W,H = FAR_SIZE; w2=W//2
        base = vgrad(w2, H, P["sky_top"], P["sky_bot"])
        d = ImageDraw.Draw(base)
        paint_far(zone, d, w2, H, P, R)
        # subtle tint wash line at horizon for grade feel
        return mirror_to_full(base)
    elif layer=="mid":
        W,H = MID_SIZE; w2=W//2
        half = half_canvas(w2,H)
        d = ImageDraw.Draw(half)
        paint_mid(zone, d, w2, H, P, R)
        return mirror_to_full(half)
    else:
        W,H = NEAR_SIZE; w2=W//2
        half = half_canvas(w2,H)
        d = ImageDraw.Draw(half)
        paint_near(zone, d, w2, H, P, R)
        return mirror_to_full(half)

def md5(p):
    import hashlib
    return hashlib.md5(open(p,'rb').read()).hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root",default="."); ap.add_argument("--check-only",action="store_true")
    a=ap.parse_args(); root=a.root
    d1=os.path.join(root,"assets","bg"); d2=os.path.join(root,"web","assets","bg")
    manifest={"zones":{}}
    for z in ZONES:
        manifest["zones"][z]={"layers":[
            {"file":f"bg_{z}_far.png","parallax_factor":FACTORS["far"],"size":list(FAR_SIZE)},
            {"file":f"bg_{z}_mid.png","parallax_factor":FACTORS["mid"],"size":list(MID_SIZE)},
            {"file":f"bg_{z}_near.png","parallax_factor":FACTORS["near"],"size":list(NEAR_SIZE)}]}
    if not a.check_only:
        os.makedirs(d1,exist_ok=True); os.makedirs(d2,exist_ok=True)
        for z in ZONES:
            for layer in ("far","mid","near"):
                img=make_layer(z,layer)
                assert img.mode=="RGBA"
                for dp in (d1,d2):
                    img.save(os.path.join(dp,f"bg_{z}_{layer}.png"))
        man=json.dumps(manifest,indent=2)
        open(os.path.join(d1,"manifest.json"),"w").write(man)
        open(os.path.join(d2,"manifest.json"),"w").write(man)
    # ---- verification ----
    ok=True; lines=[]
    for z in ZONES:
        for layer,sz in (("far",FAR_SIZE),("mid",MID_SIZE),("near",NEAR_SIZE)):
            f1=os.path.join(d1,f"bg_{z}_{layer}.png"); f2=os.path.join(d2,f"bg_{z}_{layer}.png")
            for f in (f1,f2):
                if not os.path.exists(f): lines.append(f"FAIL missing {f}"); ok=False; continue
                im=Image.open(f)
                if im.size!=sz: lines.append(f"FAIL size {f} {im.size}!={sz}"); ok=False
                if im.mode!="RGBA": lines.append(f"FAIL mode {f} {im.mode}"); ok=False
                px=im.load(); W,H=im.size
                bad=sum(1 for y in range(H) if px[0,y]!=px[W-1,y])
                if bad: lines.append(f"FAIL wrap {f} {bad}/{H} rows mismatch"); ok=False
                else: lines.append(f"OK wrap {z}/{layer} {os.path.basename(f)} {W}x{H} left==right all {H} rows")
            if os.path.exists(f1) and os.path.exists(f2):
                h1,h2=md5(f1),md5(f2)
                if h1!=h2: lines.append(f"FAIL parity bg_{z}_{layer}.png {h1}!={h2}"); ok=False
                else: lines.append(f"OK parity bg_{z}_{layer}.png md5={h1[:12]}")
    for dp in (d1,d2):
        mf=os.path.join(dp,"manifest.json")
        if not os.path.exists(mf): lines.append(f"FAIL missing {mf}"); ok=False
        else:
            m=json.load(open(mf))
            nz=len(m.get("zones",{})); nl=sum(len(v.get("layers",[])) for v in m.get("zones",{}).values())
            fl=m["zones"][ZONES[0]]["layers"]
            fac=[l["parallax_factor"] for l in fl]
            status="OK" if (nz==7 and nl==21 and fac==[0.15,0.35,0.6]) else "FAIL"
            if status=="FAIL": ok=False
            lines.append(f"{status} manifest {mf} zones={nz} layers={nl} factors={fac}")
    # alpha expectations: far opaque, mid/near have transparency
    for z in ZONES:
        for layer in ("mid","near"):
            f=os.path.join(d2,f"bg_{z}_{layer}.png")
            if os.path.exists(f):
                im=Image.open(f); al=im.getchannel("A"); hist=al.histogram()
                if hist[0]==0: lines.append(f"WARN {z}/{layer} fully opaque (expected alpha sky)"); 
                else: lines.append(f"OK alpha {z}/{layer} transparent_px={hist[0]}")
    print("\n".join(lines))
    print("VERIFY:", "PASS" if ok else "FAIL")
    # file list
    files=[]
    for z in ZONES:
        for layer in ("far","mid","near"): files.append(f"web/assets/bg/bg_{z}_{layer}.png")
    files.append("web/assets/bg/manifest.json")
    print("FILES:", len(files))
    return 0 if ok else 1

if __name__=="__main__": sys.exit(main())
