"""
Blender isometric render kit for Zaggers — 2:1 dimetric ("iso") props.

RESEARCH BASIS (measured 2026-09-06, see assets/renders/README.md):
  - assets/models_3d/*.obj (+ .mtl): prontera_fountain (h=4.5),
    shop_building (h=6.81), dungeon_brazier (h=5.7),
    guild_clocktower (h=22.0). Z-up, ground at z=0, units ~Blender units.
  - assets/tiles_ff: floor tiles 128x64 diamond RGBA (tile_meadow_grass,
    tile_town_cobble); props: env_fountain 96x96, env_tree_meadow 96x128,
    env_house_* 128 wide x 128..176 tall (smithy/inn 128x144,
    temple 128x160, guild 128x176, shop/row/terrace 128x128).
  - web/index.html: TILE_W=48 TILE_H=24 runtime footprint (2:1), worldToIso /
    isoToWorld project (rx-ry, rx+ry); 128x64 source art is drawn scaled down
    to the 48x24 footprint (image-rendering: pixelated).
  - vault/ART_PIPELINE_REPORT.md: canonical tile spec is the 128x64 diamond
    (doc's old 64x32 spec superseded); props are variable-size RGBA with oval
    ground-contact shadow anchored at base centre.

WHAT THIS SCRIPT DOES (safe to run headless):
  - Clears the scene, imports each assets/models_3d/*.obj with materials,
    centres XY on origin and drops base to z=0.
  - Sets an ORTHOGRAPHIC 2:1 iso camera: rotation X=54.73561deg,
    Y=0, Z=45deg; ortho_scale auto-fit per model height (+ margin).
  - Enables transparent film (PNG RGBA), Sun key + Hemisphere fill, soft
    shadows, optional Cycles AO bake (--bake-ao), and a consistent fake
    ground-contact ellipse (circle scaled 1.0 x 0.5, black alpha ~0.35)
    so every render shares the same grounding language as the PIL props.
  - Renders each model at the framing in RENDER_JOBS (tile 128x64 reference
    + 96-128px prop canvases matching env_* conventions) to
    assets/renders/<name>_iso.png, then copies to web/assets/tiles_ff/
    for web parity (same bytes, keeps index.html sprite paths working).

USAGE (inside Blender — bpy only exists there):
  blender --background --python tools/blender_iso_render.py -- \
    --models assets/models_3d --out assets/renders --web-out web/assets/tiles_ff

  Flags: --engine BLENDER_EEVEE|CYCLES  --bake-ao  --margin 1.25
         --only prontera_fountain,shop_building  --list-jobs

IF bpy IS MISSING (plain `python tools/blender_iso_render.py`):
  The script prints the manual camera/lighting/export steps below and exits 2
  instead of crashing. Those same steps are in assets/renders/README.md.
"""

from __future__ import annotations

import argparse
import math
import os
import shutil
import sys

# --------------------------------------------------------------------------
# Canonical iso values — single source of truth (mirrored in README.md).
# --------------------------------------------------------------------------
ISO_ROT_X_DEG = 54.73561  # arcsin(tan(30deg)); true 2:1 dimetric tilt
ISO_ROT_Y_DEG = 0.0
ISO_ROT_Z_DEG = 45.0
TILE_SRC_W, TILE_SRC_H = 128, 64          # source-art diamond (ART_PIPELINE)
TILE_WEB_W, TILE_WEB_H = 48, 24           # runtime footprint (web/index.html)
GROUND_ELLIPSE_ALPHA = 0.35
GROUND_ELLIPSE_SQUASH_Y = 0.5             # ellipse reads as circle in 2:1 iso

# Per-model framing: output canvas + ortho_scale baseline + web sprite name.
# Canvas sizes deliberately match existing assets/tiles_ff conventions so
# Blender output is a drop-in (houses 128w x 128-176h, fountain 96x96, ...).
RENDER_JOBS = {
    "prontera_fountain": {
        "canvas": (96, 96), "ortho_scale": 8.0, "web_name": "env_fountain.png",
    },
    "dungeon_brazier": {
        "canvas": (96, 128), "ortho_scale": 7.5, "web_name": "env_torch_brazier.png",
    },
    "shop_building": {
        "canvas": (128, 128), "ortho_scale": 9.5, "web_name": "env_house_shop.png",
    },
    "guild_clocktower": {
        "canvas": (128, 256), "ortho_scale": 24.0, "web_name": "env_guild_clocktower.png",
    },
}

MANUAL_STEPS = """
MANUAL ISO RENDER STEPS (no Blender Python available).
-------------------------------------------------------
1. Blender 3.6+ > New > General. Delete default Cube/Light/Camera.
2. File > Import > Wavefront (.obj): assets/models_3d/<name>.obj
   (enable 'Import Materials' so the .mtl Kd colours come along).
3. Select mesh: Object > Set Origin > Origin to Geometry, then move so the
   base sits at Z=0 and XY centre is at world origin (Alt+G, then G+Z).
4. Camera: Add > Camera. Set Type=Orthographic. Rotation X=54.73561deg,
   Y=0deg, Z=45deg. Aim at model centre (add Track-To constraint to an
   Empty at (0,0,height/2), or position manually along the iso diagonal).
   Ortho Scale: brazier ~7.5 / fountain ~8 / shop ~9.5 / clocktower ~24,
   then nudge so the model fills the frame with ~8px padding.
5. Ground ellipse: Add > Mesh > Circle (radius ~ model footprint), scale
   Y by 0.5, place at Z=0.01. Material: black, alpha 0.35, blend=Alpha
   Blend, shadow catcher off — this is the shared contact-shadow language.
6. Lighting: Add > Light > Sun, rotation to azimuth 45deg / elevation ~50deg,
   Strength 3.0, shadow soft (EEVEE: enable Ambient Occlusion + Bloom off;
   Cycles: 32 samples is plenty for flat low-poly). Add Hemisphere/Ambient
   fill ~0.4 so shadow sides never go pure black. Optional: bake AO
   (Cycles > Render > Bake > Ambient Occlusion) before final render.
7. Render: Engine EEVEE or Cycles, Film > Transparent ON, Output PNG RGBA
   8-bit, resolution per model (fountain 96x96, brazier 96x128,
   shop 128x128, clocktower 128x256, tile reference 128x64). Render (F12),
   Image > Save As assets/renders/<name>_iso.png, copy to web/assets/tiles_ff/.
""".strip()


def parse_args(argv):
    p = argparse.ArgumentParser(description="Zaggers Blender iso batch renderer")
    p.add_argument("--models", default="assets/models_3d")
    p.add_argument("--out", default="assets/renders")
    p.add_argument("--web-out", default="web/assets/tiles_ff",
                   help="web parity copy dir ('' to skip)")
    p.add_argument("--engine", default="BLENDER_EEVEE",
                   choices=["BLENDER_EEVEE", "CYCLES"])
    p.add_argument("--bake-ao", action="store_true",
                   help="Cycles AO bake pass before render (slow, optional)")
    p.add_argument("--margin", type=float, default=1.25)
    p.add_argument("--only", default="",
                   help="comma-separated model basenames to render only")
    p.add_argument("--list-jobs", action="store_true")
    return p.parse_args(argv)


def job_list(only: str):
    if only:
        wanted = [s.strip() for s in only.split(",") if s.strip()]
        return {k: v for k, v in RENDER_JOBS.items() if k in wanted}
    return dict(RENDER_JOBS)


# -- bpy-dependent implementation (imported lazily so --help works w/o bpy) --
def run_in_blender(args):
    import bpy  # noqa: F401  (only importable inside Blender)

    jobs = job_list(args.only)
    os.makedirs(args.out, exist_ok=True)
    if args.web_out:
        os.makedirs(args.web_out, exist_ok=True)

    for name, job in jobs.items():
        src = os.path.join(args.models, name + ".obj")
        if not os.path.isfile(src):
            print(f"[iso-render] SKIP {name}: missing {src}")
            continue
        _render_one(args, name, job, src)

    print(f"[iso-render] done: {len(jobs)} job(s) -> {args.out}")


def _clear_scene():
    import bpy
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    # purge orphan data so batch imports don't accumulate materials
    for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.images):
        for x in list(coll):
            try:
                coll.remove(x)
            except Exception:
                pass


def _setup_scene(args, canvas):
    import bpy
    scene = bpy.context.scene
    scene.render.engine = args.engine
    scene.render.film_transparent = True
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.image_settings.color_depth = "8"
    scene.render.resolution_x, scene.render.resolution_y = canvas
    scene.render.resolution_percentage = 100
    scene.render.pixel_aspect_x = 1.0
    scene.render.pixel_aspect_y = 1.0
    if args.engine == "BLENDER_EEVEE":
        eevee = scene.eevee
        eevee.taa_render_samples = 32
        try:
            eevee.use_gtao = True  # baked-AO look without a bake pass
        except AttributeError:
            pass
    else:
        scene.cycles.samples = 32
        scene.cycles.use_denoising = True
    # World: flat neutral so transparent PNGs composite over any tile.
    world = scene.world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.05, 0.05, 0.07, 1.0)
        bg.inputs["Strength"].default_value = 0.4


def _import_obj_centered(src):
    import bpy
    bpy.ops.wm.obj_import(filepath=src, forward_axis="NEGATIVE_Z", up_axis="Z")
    imported = [o for o in bpy.context.selected_objects if o.type == "MESH"]
    if not imported:
        raise RuntimeError(f"OBJ import produced no meshes: {src}")
    # Join multi-part imports so bounds/origin math is trivial.
    bpy.ops.object.select_all(action="DESELECT")
    for o in imported:
        o.select_set(True)
    bpy.context.view_layer.objects.active = imported[0]
    if len(imported) > 1:
        bpy.ops.object.join()
    root = bpy.context.view_layer.objects.active
    # Centre XY via origin-to-bounds, drop base to z=0.
    import mathutils
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
    root.location = (0.0, 0.0, 0.0)
    bpy.context.view_layer.update()
    bound = [root.matrix_world @ mathutils.Vector(c) for c in root.bound_box]
    root.location.z -= min(c.z for c in bound)
    bpy.context.view_layer.update()
    return root


def _model_height(root):
    import mathutils
    bound = [root.matrix_world @ mathutils.Vector(c) for c in root.bound_box]
    zs = [c.z for c in bound]
    xs = [c.x for c in bound]
    ys = [c.y for c in bound]
    return max(zs) - min(zs), max(xs) - min(xs), max(ys) - min(ys)


def _add_iso_camera(height, ortho_baseline, margin):
    import bpy
    from mathutils import Vector
    cam_data = bpy.data.cameras.new("IsoCam_2to1")
    cam_data.type = "ORTHO"
    # Auto-fit: keep authoring baseline, grow if the model is taller than the
    # baseline framing expects (clocktower h=22 needs ~24).
    cam_data.ortho_scale = max(ortho_baseline, (height + 2.0) * margin)
    cam = bpy.data.objects.new("IsoCam_2to1", cam_data)
    bpy.context.scene.collection.objects.link(cam)
    # Position back along the iso view diagonal, look at mid-height target.
    dist = max(30.0, height * 3.0 + 20.0)
    direction = Vector((math.cos(math.radians(ISO_ROT_Z_DEG)),
                        math.sin(math.radians(ISO_ROT_Z_DEG)),
                        math.tan(math.radians(30.0)))).normalized()
    target = Vector((0.0, 0.0, height / 2.0))
    cam.location = target + direction * dist
    cam.rotation_euler = (math.radians(ISO_ROT_X_DEG),
                          math.radians(ISO_ROT_Y_DEG),
                          math.radians(ISO_ROT_Z_DEG))
    bpy.context.scene.camera = cam
    return cam


def _add_lights_and_ground(root_w, root_d):
    import bpy
    # Key sun: azimuth 45deg, elevation ~50deg, warm-neutral, soft shadow.
    sun = bpy.data.objects.new("KeySun",
                               bpy.data.lights.new("KeySun", type="SUN"))
    bpy.context.scene.collection.objects.link(sun)
    sun.data.energy = 3.0
    sun.rotation_euler = (math.radians(40.0), 0.0, math.radians(ISO_ROT_Z_DEG))
    # Cool fill so shadow sides match the flat-shaded PIL sprites.
    fill = bpy.data.objects.new("FillHemi",
                                bpy.data.lights.new("FillHemi", type="SUN"))
    bpy.context.scene.collection.objects.link(fill)
    fill.data.energy = 0.4
    fill.rotation_euler = (math.radians(70.0), 0.0,
                           math.radians(ISO_ROT_Z_DEG + 180.0))
    # Consistent ground-contact ellipse (fake AO blob, same on every render).
    radius = max(root_w, root_d) / 2.0 + 0.6
    bpy.ops.mesh.primitive_circle_add(radius=radius, fill=True,
                                      location=(0.0, 0.0, 0.01))
    blob = bpy.context.view_layer.objects.active
    blob.name = "GroundEllipse"
    blob.scale = (1.0, GROUND_ELLIPSE_SQUASH_Y, 1.0)
    mat = bpy.data.materials.new("GroundEllipseMat")
    mat.use_nodes = True
    principled = mat.node_tree.nodes.get("Principled BSDF")
    if principled:
        principled.inputs["Base Color"].default_value = (0, 0, 0, 1)
        principled.inputs["Alpha"].default_value = GROUND_ELLIPSE_ALPHA
    mat.blend_method = "BLEND"
    blob.data.materials.append(mat)
    return sun, fill, blob


def _bake_ao(root):
    import bpy
    scene = bpy.context.scene
    if scene.render.engine != "CYCLES":
        print("[iso-render] --bake-ao needs CYCLES; skipping bake.")
        return
    # Minimal vertex-color AO bake target so the option exists headless.
    try:
        bpy.ops.object.bake(type="AO")
        print("[iso-render] AO bake complete.")
    except Exception as exc:  # never fail the batch on an optional bake
        print(f"[iso-render] AO bake skipped ({exc}).")


def _render_one(args, name, job, src):
    import bpy
    _clear_scene()
    _setup_scene(args, job["canvas"])
    root = _import_obj_centered(src)
    height, w, d = _model_height(root)
    _add_iso_camera(height, job["ortho_scale"], args.margin)
    _add_lights_and_ground(w, d)
    if args.bake_ao:
        _bake_ao(root)
    scene = bpy.context.scene
    out_png = os.path.join(args.out, name + "_iso.png")
    scene.render.filepath = out_png
    bpy.ops.render.render(write_still=True)
    print(f"[iso-render] {name}: h={height:.2f} canvas={job['canvas']} -> {out_png}")
    if args.web_out:  # web parity: identical bytes under web sprite name
        web_png = os.path.join(args.web_out, job["web_name"])
        shutil.copyfile(out_png, web_png)
        print(f"[iso-render]   parity copy -> {web_png}")


def main(argv=None):
    # Repo-root-relative defaults: script may run with CWD == Blender's, so
    # resolve default paths against the Zaggers project root (parent of tools/).
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)
    defaults = {"models": os.path.join(root, "assets", "models_3d"),
                "out": os.path.join(root, "assets", "renders"),
                "web-out": os.path.join(root, "web", "assets", "tiles_ff")}
    if "--" in sys.argv:
        raw = sys.argv[sys.argv.index("--") + 1:]
    elif argv is not None:
        raw = argv
    else:
        raw = sys.argv[1:]  # plain-python invocation without Blender's -- separator
    args = parse_args(raw)
    if args.models == "assets/models_3d":
        args.models = defaults["models"]
    if args.out == "assets/renders":
        args.out = defaults["out"]
    if args.web_out == "web/assets/tiles_ff":
        args.web_out = defaults["web-out"]

    if args.list_jobs:
        for k, v in job_list(args.only).items():
            print(f"{k}: canvas={v['canvas']} ortho={v['ortho_scale']} web={v['web_name']}")
        return 0

    try:
        import bpy  # noqa: F401
    except ImportError:
        print("bpy not available (plain Python, not Blender). Nothing rendered.")
        print(MANUAL_STEPS)
        return 2

    run_in_blender(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
