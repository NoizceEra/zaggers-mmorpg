import os
import math

OUTPUT_DIR = r"D:\ai-studio\Zaggers\assets\models_3d"
os.makedirs(OUTPUT_DIR, exist_ok=True)

class ObjMesh:
    def __init__(self, name):
        self.name = name
        self.vertices = []
        self.normals = []
        self.uvs = []
        self.faces = [] # list of (material_name, [ (v_idx, uv_idx, n_idx), ... ])
        self.current_material = None
        self.materials = {} # mat_name: dict of properties

    def add_material(self, name, kd=(0.8, 0.8, 0.8), ka=(0.2, 0.2, 0.2), ks=(0.0, 0.0, 0.0), ns=10.0, d=1.0):
        self.materials[name] = {
            'Kd': kd,
            'Ka': ka,
            'Ks': ks,
            'Ns': ns,
            'd': d
        }

    def use_material(self, name):
        self.current_material = name

    def add_vertex(self, x, y, z):
        self.vertices.append((round(x, 4), round(y, 4), round(z, 4)))
        return len(self.vertices)

    def add_normal(self, nx, ny, nz):
        length = math.sqrt(nx*nx + ny*ny + nz*nz)
        if length > 0:
            nx, ny, nz = nx/length, ny/length, nz/length
        self.normals.append((round(nx, 4), round(ny, 4), round(nz, 4)))
        return len(self.normals)

    def add_uv(self, u, v):
        self.uvs.append((round(u, 4), round(v, 4)))
        return len(self.uvs)

    def add_face(self, v_indices, n_indices=None, uv_indices=None):
        face_verts = []
        for i in range(len(v_indices)):
            vi = v_indices[i]
            ui = uv_indices[i] if uv_indices and i < len(uv_indices) else None
            ni = n_indices[i] if n_indices and i < len(n_indices) else None
            face_verts.append((vi, ui, ni))
        self.faces.append((self.current_material, face_verts))

    def add_quad(self, v1, v2, v3, v4, n=None, mat=None):
        if mat: self.use_material(mat)
        n_idx = self.add_normal(*n) if n else None
        n_list = [n_idx]*4 if n_idx else None
        self.add_face([v1, v2, v3, v4], n_indices=n_list)

    def add_triangle(self, v1, v2, v3, n=None, mat=None):
        if mat: self.use_material(mat)
        n_idx = self.add_normal(*n) if n else None
        n_list = [n_idx]*3 if n_idx else None
        self.add_face([v1, v2, v3], n_indices=n_list)

    def add_box(self, cx, cy, cz, sx, sy, sz, mat=None):
        if mat: self.use_material(mat)
        hx, hy, hz = sx / 2.0, sy / 2.0, sz / 2.0
        v = [
            self.add_vertex(cx - hx, cy - hy, cz - hz),
            self.add_vertex(cx + hx, cy - hy, cz - hz),
            self.add_vertex(cx + hx, cy + hy, cz - hz),
            self.add_vertex(cx - hx, cy + hy, cz - hz),
            self.add_vertex(cx - hx, cy - hy, cz + hz),
            self.add_vertex(cx + hx, cy - hy, cz + hz),
            self.add_vertex(cx + hx, cy + hy, cz + hz),
            self.add_vertex(cx - hx, cy + hy, cz + hz),
        ]
        self.add_quad(v[0], v[3], v[2], v[1], (0, 0, -1))
        self.add_quad(v[4], v[5], v[6], v[7], (0, 0, 1))
        self.add_quad(v[0], v[1], v[5], v[4], (0, -1, 0))
        self.add_quad(v[1], v[2], v[6], v[5], (1, 0, 0))
        self.add_quad(v[2], v[3], v[7], v[6], (0, 1, 0))
        self.add_quad(v[3], v[0], v[4], v[7], (-1, 0, 0))

    def add_cylinder(self, cx, cy, z_bottom, z_top, r_bottom, r_top, sides=8, mat=None, cap_bottom=True, cap_top=True):
        if mat: self.use_material(mat)
        bot_verts = []
        top_verts = []
        for i in range(sides):
            angle = 2.0 * math.pi * i / sides
            cos_a, sin_a = math.cos(angle), math.sin(angle)
            bot_verts.append(self.add_vertex(cx + r_bottom * cos_a, cy + r_bottom * sin_a, z_bottom))
            top_verts.append(self.add_vertex(cx + r_top * cos_a, cy + r_top * sin_a, z_top))

        for i in range(sides):
            i_next = (i + 1) % sides
            angle_mid = 2.0 * math.pi * (i + 0.5) / sides
            n = (math.cos(angle_mid), math.sin(angle_mid), 0)
            self.add_quad(bot_verts[i], bot_verts[i_next], top_verts[i_next], top_verts[i], n=n)

        if cap_bottom:
            n_bot = self.add_normal(0, 0, -1)
            c_bot = self.add_vertex(cx, cy, z_bottom)
            for i in range(sides):
                i_next = (i + 1) % sides
                self.add_face([c_bot, bot_verts[i_next], bot_verts[i]], n_indices=[n_bot]*3)

        if cap_top:
            n_top = self.add_normal(0, 0, 1)
            c_top = self.add_vertex(cx, cy, z_top)
            for i in range(sides):
                i_next = (i + 1) % sides
                self.add_face([c_top, top_verts[i], top_verts[i_next]], n_indices=[n_top]*3)

    def add_cone(self, cx, cy, z_bottom, height, radius, sides=8, mat=None):
        if mat: self.use_material(mat)
        bot_verts = []
        for i in range(sides):
            angle = 2.0 * math.pi * i / sides
            bot_verts.append(self.add_vertex(cx + radius * math.cos(angle), cy + radius * math.sin(angle), z_bottom))
        apex = self.add_vertex(cx, cy, z_bottom + height)

        for i in range(sides):
            i_next = (i + 1) % sides
            angle_mid = 2.0 * math.pi * (i + 0.5) / sides
            n = (math.cos(angle_mid), math.sin(angle_mid), 0.5)
            self.add_triangle(bot_verts[i], bot_verts[i_next], apex, n=n)

        n_bot = self.add_normal(0, 0, -1)
        c_bot = self.add_vertex(cx, cy, z_bottom)
        for i in range(sides):
            i_next = (i + 1) % sides
            self.add_face([c_bot, bot_verts[i_next], bot_verts[i]], n_indices=[n_bot]*3)

    def add_hollow_ring(self, cx, cy, z_bottom, height, r_outer, r_inner, sides=12, mat_outer=None, mat_inner=None, mat_top=None):
        z_top = z_bottom + height
        outer_bot, outer_top = [], []
        inner_bot, inner_top = [], []

        for i in range(sides):
            angle = 2.0 * math.pi * i / sides
            cos_a, sin_a = math.cos(angle), math.sin(angle)
            outer_bot.append(self.add_vertex(cx + r_outer * cos_a, cy + r_outer * sin_a, z_bottom))
            outer_top.append(self.add_vertex(cx + r_outer * cos_a, cy + r_outer * sin_a, z_top))
            inner_bot.append(self.add_vertex(cx + r_inner * cos_a, cy + r_inner * sin_a, z_bottom))
            inner_top.append(self.add_vertex(cx + r_inner * cos_a, cy + r_inner * sin_a, z_top))

        if mat_outer: self.use_material(mat_outer)
        for i in range(sides):
            i_next = (i + 1) % sides
            angle_mid = 2.0 * math.pi * (i + 0.5) / sides
            n = (math.cos(angle_mid), math.sin(angle_mid), 0)
            self.add_quad(outer_bot[i], outer_bot[i_next], outer_top[i_next], outer_top[i], n=n)

        if mat_inner: self.use_material(mat_inner)
        for i in range(sides):
            i_next = (i + 1) % sides
            angle_mid = 2.0 * math.pi * (i + 0.5) / sides
            n = (-math.cos(angle_mid), -math.sin(angle_mid), 0)
            self.add_quad(inner_bot[i_next], inner_bot[i], inner_top[i], inner_top[i_next], n=n)

        if mat_top: self.use_material(mat_top)
        n_top = (0, 0, 1)
        for i in range(sides):
            i_next = (i + 1) % sides
            self.add_quad(outer_top[i], outer_top[i_next], inner_top[i_next], inner_top[i], n=n_top)

    def write_files(self, filepath_base):
        obj_path = filepath_base + ".obj"
        mtl_path = filepath_base + ".mtl"
        mtl_filename = os.path.basename(mtl_path)

        with open(mtl_path, 'w') as f:
            f.write(f"# Material file for {self.name}\n\n")
            for m_name, props in self.materials.items():
                f.write(f"newmtl {m_name}\n")
                f.write(f"Ka {props['Ka'][0]:.4f} {props['Ka'][1]:.4f} {props['Ka'][2]:.4f}\n")
                f.write(f"Kd {props['Kd'][0]:.4f} {props['Kd'][1]:.4f} {props['Kd'][2]:.4f}\n")
                f.write(f"Ks {props['Ks'][0]:.4f} {props['Ks'][1]:.4f} {props['Ks'][2]:.4f}\n")
                f.write(f"Ns {props['Ns']:.1f}\n")
                f.write(f"d {props['d']:.2f}\n")
                f.write("illum 2\n\n")

        with open(obj_path, 'w') as f:
            f.write(f"# Wavefront OBJ file for {self.name}\n")
            f.write(f"mtllib {mtl_filename}\n")
            f.write(f"o {self.name}\n\n")

            for v in self.vertices:
                f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")

            for uv in self.uvs:
                f.write(f"vt {uv[0]:.4f} {uv[1]:.4f}\n")

            for n in self.normals:
                f.write(f"vn {n[0]:.4f} {n[1]:.4f} {n[2]:.4f}\n")

            current_mat = None
            for mat_name, face in self.faces:
                if mat_name != current_mat:
                    f.write(f"usemtl {mat_name}\n")
                    current_mat = mat_name

                face_str = []
                for vi, ui, ni in face:
                    if ui is not None and ni is not None:
                        face_str.append(f"{vi}/{ui}/{ni}")
                    elif ni is not None:
                        face_str.append(f"{vi}//{ni}")
                    elif ui is not None:
                        face_str.append(f"{vi}/{ui}")
                    else:
                        face_str.append(f"{vi}")
                f.write("f " + " ".join(face_str) + "\n")

        print(f"Generated: {obj_path} ({len(self.vertices)} verts, {len(self.faces)} faces)")

# ==========================================
# 1. PRONTERA FOUNTAIN
# ==========================================
def build_prontera_fountain():
    f = ObjMesh("prontera_fountain")
    f.add_material("stone_dark", kd=(0.35, 0.35, 0.40))
    f.add_material("stone_light", kd=(0.75, 0.75, 0.78))
    f.add_material("stone_trim", kd=(0.60, 0.55, 0.50))
    f.add_material("water_blue", kd=(0.15, 0.65, 0.90), ks=(0.8, 0.8, 0.8), ns=50.0, d=0.85)
    f.add_material("gold_accent", kd=(0.95, 0.78, 0.20), ks=(0.9, 0.9, 0.5), ns=30.0)

    f.add_cylinder(0, 0, 0.0, 0.2, 3.4, 3.4, sides=12, mat="stone_dark")
    f.add_cylinder(0, 0, 0.2, 0.4, 3.1, 3.1, sides=12, mat="stone_light")
    f.add_hollow_ring(0, 0, 0.4, 0.7, 3.0, 2.5, sides=16, mat_outer="stone_light", mat_inner="stone_dark", mat_top="stone_trim")
    f.add_cylinder(0, 0, 0.4, 0.95, 2.5, 2.5, sides=16, mat="water_blue", cap_bottom=False, cap_top=True)
    f.add_cylinder(0, 0, 0.4, 1.8, 0.8, 0.7, sides=12, mat="stone_dark")
    f.add_cylinder(0, 0, 1.6, 1.8, 0.95, 0.95, sides=12, mat="stone_trim")
    f.add_hollow_ring(0, 0, 1.8, 0.4, 1.4, 1.1, sides=12, mat_outer="stone_light", mat_inner="stone_dark", mat_top="stone_trim")
    f.add_cylinder(0, 0, 1.8, 2.1, 1.1, 1.1, sides=12, mat="water_blue", cap_bottom=False, cap_top=True)
    f.add_cylinder(0, 0, 2.2, 3.2, 0.45, 0.35, sides=8, mat="stone_dark")
    f.add_hollow_ring(0, 0, 3.2, 0.3, 0.8, 0.6, sides=8, mat_outer="stone_light", mat_inner="stone_dark", mat_top="stone_trim")
    f.add_cylinder(0, 0, 3.2, 3.45, 0.6, 0.6, sides=8, mat="water_blue", cap_bottom=False, cap_top=True)

    f.add_cylinder(0, 0, 3.5, 3.8, 0.25, 0.15, sides=6, mat="gold_accent")
    f.add_cone(0, 0, 3.8, 0.7, 0.3, sides=6, mat="gold_accent")
    for i in range(4):
        ang = i * math.pi / 2
        ca, sa = math.cos(ang), math.sin(ang)
        v1 = f.add_vertex(ca * 0.15, sa * 0.15, 3.7)
        v2 = f.add_vertex(ca * 0.6, sa * 0.6, 4.3)
        v3 = f.add_vertex(ca * 0.5, sa * 0.5, 3.6)
        f.add_triangle(v1, v2, v3, n=(sa, -ca, 0.3), mat="gold_accent")

    for i in range(4):
        ang = i * math.pi / 2 + math.pi/4
        ca, sa = math.cos(ang), math.sin(ang)
        f.add_cylinder(ca * 0.9, sa * 0.9, 0.95, 2.1, 0.08, 0.05, sides=6, mat="water_blue")

    f.write_files(os.path.join(OUTPUT_DIR, "prontera_fountain"))

# ==========================================
# 2. GUILD CLOCKTOWER
# ==========================================
def build_guild_clocktower():
    t = ObjMesh("guild_clocktower")

    t.add_material("stone_gray", kd=(0.50, 0.50, 0.52))
    t.add_material("brick_main", kd=(0.58, 0.46, 0.38))
    t.add_material("brick_dark", kd=(0.35, 0.30, 0.28))
    t.add_material("wood_beam", kd=(0.38, 0.24, 0.12))
    t.add_material("clock_face", kd=(0.92, 0.90, 0.75), ks=(0.3, 0.3, 0.3), ns=15.0)
    t.add_material("brass_trim", kd=(0.82, 0.65, 0.22), ks=(0.7, 0.6, 0.2), ns=25.0)
    t.add_material("roof_slate", kd=(0.22, 0.32, 0.45))
    t.add_material("roof_spire", kd=(0.15, 0.22, 0.35))
    t.add_material("gold_accent", kd=(0.95, 0.80, 0.20), ks=(0.9, 0.9, 0.5), ns=30.0)

    t.add_box(0, 0, 0.25, 5.2, 5.2, 0.5, mat="stone_gray")
    t.add_box(0, 0, 0.75, 4.4, 4.4, 0.5, mat="stone_gray")
    t.add_box(0, 0, 2.5, 4.0, 4.0, 3.0, mat="brick_dark")
    t.add_box(0, -2.01, 1.8, 1.4, 0.1, 2.2, mat="wood_beam")
    t.add_box(0, -2.02, 1.8, 1.2, 0.1, 2.0, mat="brick_dark")

    for x_sgn in [-1, 1]:
        for y_sgn in [-1, 1]:
            t.add_box(x_sgn * 2.1, y_sgn * 2.1, 2.5, 0.6, 0.6, 3.0, mat="stone_gray")

    t.add_box(0, 0, 4.15, 4.2, 4.2, 0.3, mat="stone_gray")
    t.add_cylinder(0, 0, 4.3, 11.0, 2.4, 2.1, sides=4, mat="brick_main")

    for ang_deg in [45, 135, 225, 315]:
        rad = math.radians(ang_deg)
        ca, sa = math.cos(rad), math.sin(rad)
        t.add_cylinder(ca * 2.3, sa * 2.3, 4.3, 11.0, 0.25, 0.2, sides=4, mat="stone_gray")

    for i in range(4):
        ang = i * math.pi / 2
        ca, sa = math.cos(ang), math.sin(ang)
        t.add_box(ca * 1.95, sa * 1.95, 7.5, 0.4 if ca != 0 else 0.1, 0.4 if sa != 0 else 0.1, 1.2, mat="wood_beam")

    t.add_box(0, 0, 11.2, 4.2, 4.2, 0.4, mat="stone_gray")
    t.add_cylinder(0, 0, 11.4, 15.0, 2.3, 2.3, sides=8, mat="brick_dark")
    t.add_cylinder(0, 0, 11.4, 15.0, 2.45, 2.45, sides=8, mat="wood_beam", cap_bottom=False, cap_top=False)

    for i in range(4):
        ang = i * math.pi / 2
        ca, sa = math.cos(ang), math.sin(ang)
        cx, cy, cz = ca * 2.25, sa * 2.25, 13.2
        t.add_cylinder(cx, cy, cz - 1.1, cz + 1.1, 1.15, 1.15, sides=12, mat="brass_trim")
        t.add_cylinder(ca * 2.3, sa * 2.3, cz - 0.95, cz + 0.95, 0.98, 0.98, sides=12, mat="clock_face")
        t.add_box(ca * 2.35, sa * 2.35, cz + 0.2, 0.1 if ca != 0 else 0.5, 0.1 if sa != 0 else 0.5, 0.08, mat="wood_beam")
        t.add_box(ca * 2.35 + (sa*0.3), sa * 2.35 + (ca*0.3), cz - 0.1, 0.1 if ca != 0 else 0.6, 0.1 if sa != 0 else 0.6, 0.08, mat="wood_beam")

    t.add_cylinder(0, 0, 15.0, 15.4, 2.6, 2.6, sides=8, mat="stone_gray")
    t.add_cone(0, 0, 15.4, 5.1, 2.5, sides=8, mat="roof_slate")

    for i in range(4):
        ang = i * math.pi / 2
        ca, sa = math.cos(ang), math.sin(ang)
        t.add_box(ca * 1.8, sa * 1.8, 16.5, 0.6, 0.6, 0.8, mat="roof_spire")

    t.add_cylinder(0, 0, 20.5, 22.0, 0.1, 0.05, sides=6, mat="gold_accent")
    t.add_cylinder(0, 0, 21.3, 21.6, 0.3, 0.3, sides=8, mat="gold_accent")
    t.add_box(0, 0, 21.8, 1.2, 0.06, 0.2, mat="gold_accent")
    t.add_box(0, 0, 21.8, 0.06, 1.2, 0.2, mat="gold_accent")

    t.write_files(os.path.join(OUTPUT_DIR, "guild_clocktower"))

# ==========================================
# 3. SHOP BUILDING
# ==========================================
def build_shop_building():
    s = ObjMesh("shop_building")

    s.add_material("plaster_wall", kd=(0.88, 0.85, 0.78))
    s.add_material("wood_frame", kd=(0.35, 0.22, 0.12))
    s.add_material("stone_base", kd=(0.45, 0.45, 0.48))
    s.add_material("roof_tile", kd=(0.68, 0.26, 0.18))
    s.add_material("cloth_red", kd=(0.85, 0.18, 0.18))
    s.add_material("cloth_white", kd=(0.92, 0.90, 0.85))
    s.add_material("wood_door", kd=(0.42, 0.28, 0.15))
    s.add_material("iron_trim", kd=(0.20, 0.20, 0.22))
    s.add_material("brick_chimney", kd=(0.52, 0.36, 0.30))
    s.add_material("wood_sign", kd=(0.55, 0.38, 0.22))

    s.add_box(0, 0, 0.2, 5.2, 4.2, 0.4, mat="stone_base")
    s.add_box(0, 0, 1.7, 4.8, 3.8, 2.6, mat="plaster_wall")
    s.add_box(0, 0, 0.45, 4.86, 3.86, 0.12, mat="wood_frame")
    s.add_box(0, 0, 2.95, 4.86, 3.86, 0.12, mat="wood_frame")
    for x_sgn in [-1, 1]:
        for y_sgn in [-1, 1]:
            s.add_box(x_sgn * 2.38, y_sgn * 1.88, 1.7, 0.16, 0.16, 2.6, mat="wood_frame")

    s.add_box(-1.4, -1.91, 1.4, 0.9, 0.08, 1.9, mat="wood_door")
    s.add_box(-1.4, -1.92, 1.4, 1.0, 0.06, 2.0, mat="wood_frame")
    s.add_box(-1.05, -1.95, 1.3, 0.08, 0.08, 0.12, mat="iron_trim")

    s.add_box(0.9, -1.91, 1.3, 1.8, 0.1, 1.3, mat="wood_frame")
    s.add_box(0.9, -2.15, 0.9, 1.9, 0.4, 0.1, mat="wood_door")

    awning_y_center = -2.35
    awning_z_center = 1.95
    for idx in range(6):
        stripe_mat = "cloth_red" if idx % 2 == 0 else "cloth_white"
        x_pos = -0.0 + idx * 0.35
        s.add_box(x_pos, awning_y_center, awning_z_center, 0.35, 0.8, 0.15, mat=stripe_mat)
    s.add_box(-0.0, -2.2, 1.5, 0.06, 0.5, 0.06, mat="wood_frame")
    s.add_box(1.75, -2.2, 1.5, 0.06, 0.5, 0.06, mat="wood_frame")

    s.add_box(-2.3, -2.1, 2.4, 0.06, 0.6, 0.06, mat="iron_trim")
    s.add_box(-2.3, -2.3, 2.1, 0.6, 0.06, 0.4, mat="wood_sign")

    s.add_box(0, 0, 3.9, 5.0, 4.0, 1.8, mat="plaster_wall")
    s.add_box(0, 0, 3.05, 5.06, 4.06, 0.12, mat="wood_frame")
    s.add_box(0, 0, 4.75, 5.06, 4.06, 0.12, mat="wood_frame")
    for x_sgn in [-1, 1]:
        for y_sgn in [-1, 1]:
            s.add_box(x_sgn * 2.48, y_sgn * 1.98, 3.9, 0.16, 0.16, 1.8, mat="wood_frame")

    s.add_box(-1.2, -2.01, 3.9, 0.6, 0.08, 0.7, mat="wood_frame")
    s.add_box(1.2, -2.01, 3.9, 0.6, 0.08, 0.7, mat="wood_frame")

    num_roof_steps = 10
    for i in range(num_roof_steps):
        t_val = i / float(num_roof_steps)
        z_curr = 4.8 + t_val * 2.0
        width_y = (1.0 - t_val) * 4.4
        s.add_box(0, 0, z_curr + 0.1, 5.4, max(width_y, 0.1), 0.22, mat="roof_tile")

    s.add_box(-2.52, 0, 5.6, 0.1, 3.8, 1.6, mat="plaster_wall")
    s.add_box(2.52, 0, 5.6, 0.1, 3.8, 1.6, mat="plaster_wall")
    s.add_box(-2.55, 0, 5.8, 0.12, 4.2, 0.2, mat="wood_frame")
    s.add_box(2.55, 0, 5.8, 0.12, 4.2, 0.2, mat="wood_frame")

    s.add_box(1.8, 1.3, 5.2, 0.6, 0.6, 2.4, mat="brick_chimney")
    s.add_box(1.8, 1.3, 6.45, 0.7, 0.7, 0.12, mat="stone_base")

    s.write_files(os.path.join(OUTPUT_DIR, "shop_building"))

# ==========================================
# 4. DUNGEON BRAZIER
# ==========================================
def build_dungeon_brazier():
    b = ObjMesh("dungeon_brazier")

    b.add_material("dungeon_stone", kd=(0.30, 0.30, 0.32), ks=(0.2, 0.2, 0.2), ns=10.0)
    b.add_material("iron_dark", kd=(0.15, 0.15, 0.18), ks=(0.5, 0.5, 0.5), ns=20.0)
    b.add_material("coal_ember", kd=(0.28, 0.08, 0.04), ka=(0.3, 0.1, 0.0))
    b.add_material("fire_orange", kd=(0.95, 0.45, 0.05), ka=(0.8, 0.3, 0.0), ks=(0.8, 0.4, 0.1), ns=10.0)
    b.add_material("fire_yellow", kd=(0.98, 0.85, 0.15), ka=(0.9, 0.8, 0.1), ks=(1.0, 1.0, 0.5), ns=30.0)
    b.add_material("fire_core", kd=(1.00, 0.95, 0.70), ka=(1.0, 0.95, 0.7))

    b.add_cylinder(0, 0, 0.0, 0.25, 1.3, 1.3, sides=8, mat="dungeon_stone")
    b.add_cylinder(0, 0, 0.25, 0.55, 1.05, 1.05, sides=8, mat="dungeon_stone")
    b.add_cylinder(0, 0, 0.55, 0.9, 0.9, 0.55, sides=8, mat="dungeon_stone")
    b.add_cylinder(0, 0, 0.9, 1.8, 0.55, 0.55, sides=8, mat="dungeon_stone")
    b.add_cylinder(0, 0, 1.8, 2.2, 0.55, 0.85, sides=8, mat="dungeon_stone")
    b.add_cylinder(0, 0, 1.3, 1.45, 0.65, 0.65, sides=8, mat="dungeon_stone")

    for i in range(4):
        ang = i * math.pi / 2
        ca, sa = math.cos(ang), math.sin(ang)
        b.add_box(ca * 0.7, sa * 0.7, 2.2, 0.12 if ca != 0 else 0.3, 0.12 if sa != 0 else 0.3, 0.6, mat="iron_dark")

    b.add_hollow_ring(0, 0, 2.3, 0.8, 1.35, 1.15, sides=12, mat_outer="iron_dark", mat_inner="iron_dark", mat_top="iron_dark")
    b.add_cylinder(0, 0, 2.3, 2.45, 1.18, 1.18, sides=12, mat="iron_dark", cap_bottom=True, cap_top=True)
    b.add_cylinder(0, 0, 2.45, 2.65, 1.17, 1.17, sides=12, mat="coal_ember", cap_bottom=False, cap_top=True)

    for i in range(6):
        ang = i * math.pi / 3
        ca, sa = math.cos(ang), math.sin(ang)
        b.add_cone(ca * 0.5, sa * 0.5, 2.65, 1.8, 0.45, sides=5, mat="fire_orange")

    for i in range(4):
        ang = i * math.pi / 2 + math.pi / 4
        ca, sa = math.cos(ang), math.sin(ang)
        b.add_cone(ca * 0.25, sa * 0.25, 2.65, 2.2, 0.38, sides=4, mat="fire_yellow")

    b.add_cone(0, 0, 2.65, 2.6, 0.35, sides=6, mat="fire_core")

    sparks = [
        (0.3, 0.2, 4.8, 0.12),
        (-0.25, 0.35, 5.1, 0.1),
        (0.1, -0.4, 4.6, 0.14),
        (-0.35, -0.2, 4.9, 0.11),
        (0.0, 0.0, 5.4, 0.15)
    ]
    for sx, sy, sz, s_rad in sparks:
        b.add_cone(sx, sy, sz, s_rad * 2, s_rad, sides=4, mat="fire_yellow")
        b.add_cone(sx, sy, sz - s_rad * 2, s_rad * 2, s_rad, sides=4, mat="fire_orange")

    b.write_files(os.path.join(OUTPUT_DIR, "dungeon_brazier"))

if __name__ == "__main__":
    print("Generating 3D Low-Poly Models for Zaggers Pipeline...")
    build_prontera_fountain()
    build_guild_clocktower()
    build_shop_building()
    build_dungeon_brazier()
    print("All 3D models generated successfully!")
