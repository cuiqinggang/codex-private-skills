import math
from pathlib import Path

import bpy
from mathutils import Vector


SCRIPT_PATH = Path(__file__).resolve()
WORKSPACE = SCRIPT_PATH.parents[2]
BLEND_PATH = WORKSPACE / "blender" / "project" / "replica_15s_p3.blend"
FRAMES_DIR = WORKSPACE / "blender" / "renders" / "frames_15s"
MP4_PATH = WORKSPACE / "blender" / "renders" / "replica_15s_p3.mp4"

FRAME_START = 1
FRAME_ESTABLISH_END = 150
FRAME_INTENSIFY_END = 300
FRAME_END = 450


def ensure_inside_workspace(path: Path) -> Path:
    resolved = path.resolve()
    resolved.relative_to(WORKSPACE.resolve())
    return resolved


def reset_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for collection in (
        bpy.data.meshes,
        bpy.data.materials,
        bpy.data.curves,
        bpy.data.lights,
        bpy.data.cameras,
        bpy.data.objects,
    ):
        for datablock in list(collection):
            if datablock.users == 0:
                collection.remove(datablock)


def configure_render() -> None:
    scene = bpy.context.scene
    scene.frame_start = FRAME_START
    scene.frame_end = FRAME_END
    scene.frame_set(FRAME_START)
    scene.render.fps = 30
    scene.render.resolution_x = 1080
    scene.render.resolution_y = 1260
    scene.render.resolution_percentage = 100
    try:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    except TypeError:
        scene.render.engine = "BLENDER_EEVEE"
    if hasattr(scene, "eevee"):
        settings = {
            "taa_render_samples": 32,
            "taa_samples": 16,
            "use_gtao": True,
            "gtao_distance": 3.5,
            "gtao_factor": 1.8,
        }
        for attr, value in settings.items():
            if hasattr(scene.eevee, attr):
                setattr(scene.eevee, attr, value)
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = str(ensure_inside_workspace(FRAMES_DIR / "frame_"))
    scene.render.film_transparent = False
    scene.view_settings.view_transform = "Filmic"
    scene.view_settings.look = "High Contrast"
    scene.view_settings.exposure = -0.62
    scene.view_settings.gamma = 1.0
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    BLEND_PATH.parent.mkdir(parents=True, exist_ok=True)
    MP4_PATH.parent.mkdir(parents=True, exist_ok=True)
    for old_frame in FRAMES_DIR.glob("frame_*.png"):
        old_frame.unlink()
    if MP4_PATH.exists():
        MP4_PATH.unlink()


def set_alpha(material) -> None:
    for attr, value in (("blend_method", "BLEND"), ("surface_render_method", "BLENDED"), ("show_transparent_back", True)):
        if hasattr(material, attr):
            try:
                setattr(material, attr, value)
            except Exception:
                pass


def principled_material(name, color, roughness=0.75, metallic=0.0, alpha=1.0, emission=None, emission_strength=0.0):
    material = bpy.data.materials.new(name)
    material.diffuse_color = color
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        values = {
            "Base Color": color,
            "Roughness": roughness,
            "Metallic": metallic,
            "Alpha": alpha,
        }
        if emission:
            values["Emission Color"] = emission
            values["Emission Strength"] = emission_strength
        for input_name, value in values.items():
            if input_name in bsdf.inputs:
                bsdf.inputs[input_name].default_value = value
    if alpha < 1:
        set_alpha(material)
    return material


def noisy_material(name, color, roughness=0.85, metallic=0.0, bump_strength=0.06, noise_scale=30):
    material = principled_material(name, color, roughness=roughness, metallic=metallic)
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    if not bsdf:
        return material
    noise = nodes.new(type="ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = noise_scale
    noise.inputs["Detail"].default_value = 8.0
    noise.inputs["Roughness"].default_value = 0.6
    bump = nodes.new(type="ShaderNodeBump")
    bump.inputs["Strength"].default_value = bump_strength
    bump.inputs["Distance"].default_value = 0.07
    links.new(noise.outputs["Fac"], bump.inputs["Height"])
    if "Normal" in bsdf.inputs:
        links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return material


def emission_material(name, color, strength=5.0, alpha=1.0):
    material = bpy.data.materials.new(name)
    material.diffuse_color = color
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    nodes.clear()
    output = nodes.new(type="ShaderNodeOutputMaterial")
    emission = nodes.new(type="ShaderNodeEmission")
    emission.inputs["Color"].default_value = color
    emission.inputs["Strength"].default_value = strength
    if alpha < 1.0:
        transparent = nodes.new(type="ShaderNodeBsdfTransparent")
        mix = nodes.new(type="ShaderNodeMixShader")
        mix.inputs["Fac"].default_value = 1.0 - alpha
        links.new(transparent.outputs["BSDF"], mix.inputs[1])
        links.new(emission.outputs["Emission"], mix.inputs[2])
        links.new(mix.outputs["Shader"], output.inputs["Surface"])
        set_alpha(material)
    else:
        links.new(emission.outputs["Emission"], output.inputs["Surface"])
    return material, emission


def add_cube(name, location, scale, material):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    return obj


def add_cylinder(name, radius, depth, location, material, vertices=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    bevel = obj.modifiers.new("soft bevel", "BEVEL")
    bevel.width = 0.01
    bevel.segments = 2
    obj.modifiers.new("weighted normals", "WEIGHTED_NORMAL")
    return obj


def add_uv_sphere(name, radius, location, material, segments=48, rings=24):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, radius=radius, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    return obj


def add_ico_rock(name, radius, location, scale, material, index):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=radius, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    obj.rotation_euler = (
        math.radians((index * 31) % 79 - 39),
        math.radians((index * 47) % 97 - 48),
        math.radians((index * 83) % 180),
    )
    obj.data.materials.append(material)
    return obj


def curve_line(name, points, material, bevel_depth=0.01, parent=None):
    curve = bpy.data.curves.new(name, type="CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 2
    curve.bevel_depth = bevel_depth
    curve.bevel_resolution = 3
    spline = curve.splines.new("POLY")
    spline.points.add(len(points) - 1)
    for point, co in zip(spline.points, points):
        point.co = (co[0], co[1], co[2], 1)
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)
    if parent:
        obj.parent = parent
    return obj


def circle_points(radius, z, count=192):
    return [
        (math.cos(2 * math.pi * (i % count) / count) * radius, math.sin(2 * math.pi * (i % count) / count) * radius, z)
        for i in range(count + 1)
    ]


def polygon_points(radius, z, sides, offset=0.0):
    return [
        (math.cos(offset + 2 * math.pi * (i % sides) / sides) * radius, math.sin(offset + 2 * math.pi * (i % sides) / sides) * radius, z)
        for i in range(sides + 1)
    ]


def animate_object(obj, frames):
    for frame, attrs in frames:
        bpy.context.scene.frame_set(frame)
        for attr, value in attrs.items():
            setattr(obj, attr, value)
            obj.keyframe_insert(data_path=attr, frame=frame)


def animate_input(input_socket, values):
    for frame, value in values:
        bpy.context.scene.frame_set(frame)
        input_socket.default_value = value
        input_socket.keyframe_insert(data_path="default_value", frame=frame)


def animate_data(data, data_path, values):
    for frame, value in values:
        bpy.context.scene.frame_set(frame)
        setattr(data, data_path, value)
        data.keyframe_insert(data_path=data_path, frame=frame)


def add_torus(name, major_radius, minor_radius, location, material, rotation=(0, 0, 0), parent=None):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major_radius,
        minor_radius=minor_radius,
        major_segments=96,
        minor_segments=8,
        location=location,
        rotation=rotation,
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    if parent:
        obj.parent = parent
    return obj


def add_candle(index, x, y, wax_mat, wick_mat, flame_inner, flame_outer):
    add_cylinder(f"p3 candle body {index}", 0.12, 0.52, (x, y, 0.26), wax_mat, vertices=40)
    add_cylinder(f"p3 candle melted lip {index}", 0.13, 0.025, (x, y, 0.535), wax_mat, vertices=40)
    add_cylinder(f"p3 candle wick {index}", 0.012, 0.13, (x, y, 0.61), wick_mat, vertices=12)
    outer = add_uv_sphere(f"p3 candle outer flame {index}", 0.095, (x, y, 0.70), flame_outer, segments=24, rings=12)
    outer.scale = (0.75, 0.75, 1.55)
    inner = add_uv_sphere(f"p3 candle inner flame {index}", 0.047, (x, y, 0.71), flame_inner, segments=16, rings=8)
    inner.scale = (0.65, 0.65, 1.3)
    light_data = bpy.data.lights.new(f"p3 candle flicker light {index}", type="POINT")
    light_data.color = (1.0, 0.50, 0.18)
    light_data.energy = 85
    light_data.shadow_soft_size = 1.25
    light = bpy.data.objects.new(f"p3 candle flicker light {index}", light_data)
    bpy.context.collection.objects.link(light)
    light.location = (x, y, 0.72)
    animate_data(light.data, "energy", [(1, 70), (100, 110 + index * 8), (220, 145 + index * 7), (340, 180 + index * 5), (450, 135)])


def main() -> None:
    ensure_inside_workspace(BLEND_PATH)
    ensure_inside_workspace(FRAMES_DIR)
    ensure_inside_workspace(MP4_PATH)
    reset_scene()
    configure_render()

    table_mat = noisy_material("p3 dark rough desktop", (0.014, 0.011, 0.009, 1), roughness=0.9, metallic=0.03, bump_strength=0.055, noise_scale=44)
    panel_mat = noisy_material("p3 black notebook background", (0.004, 0.005, 0.007, 1), roughness=0.92, bump_strength=0.025, noise_scale=18)
    core_mat = noisy_material("p3 black stone metal core", (0.004, 0.0035, 0.003, 1), roughness=0.48, metallic=0.5, bump_strength=0.11, noise_scale=24)
    wax_mat = noisy_material("p3 warm dark candle wax", (0.13, 0.095, 0.065, 1), roughness=0.63, bump_strength=0.035, noise_scale=30)
    wick_mat = principled_material("p3 black candle wick", (0.002, 0.001, 0.001, 1), roughness=0.95)
    rock_mats = [
        noisy_material(f"p3 debris stone {i}", color, roughness=0.9, metallic=0.04, bump_strength=0.1, noise_scale=36 + i * 8)
        for i, color in enumerate([(0.012, 0.011, 0.010, 1), (0.021, 0.017, 0.014, 1), (0.030, 0.022, 0.017, 1)])
    ]
    red_core_mat, red_core_emission = emission_material("p3 red energy core emission", (1.0, 0.012, 0.0, 1), 8.0)
    red_halo_mat, red_halo_emission = emission_material("p3 red energy halo emission", (1.0, 0.03, 0.0, 0.35), 2.8, alpha=0.34)
    red_shell_mat, red_shell_emission = emission_material("p3 soft red outer shell", (0.75, 0.018, 0.0, 0.16), 0.8, alpha=0.16)
    red_line_mat, red_line_emission = emission_material("p3 saturated magic line emission", (1.0, 0.02, 0.0, 1), 2.8)
    red_dark_line_mat, _ = emission_material("p3 dark red secondary line", (0.72, 0.01, 0.0, 1), 1.7)
    warm_inner, _ = emission_material("p3 candle inner emission", (1.0, 0.78, 0.36, 1), 9.0)
    warm_outer, _ = emission_material("p3 candle outer emission", (1.0, 0.40, 0.09, 0.65), 3.8, alpha=0.72)
    haze_mat, haze_emission = emission_material("p3 faint red haze panels", (0.55, 0.015, 0.0, 0.12), 0.16, alpha=0.12)

    add_cube("p3 dark desktop plane", (0, 0, -0.065), (7.5, 7.5, 0.12), table_mat)
    add_cube("p3 notebook keyboard base", (0, 2.02, 0.035), (5.15, 2.1, 0.08), panel_mat)
    screen = add_cube("p3 dark notebook panel", (0, 3.02, 1.22), (5.15, 0.12, 2.55), panel_mat)
    screen.rotation_euler[0] = math.radians(-7)
    left_haze = add_cube("p3 left red haze atmosphere", (-2.62, 0.2, 0.55), (0.05, 3.5, 1.1), haze_mat)
    right_haze = add_cube("p3 right red haze atmosphere", (2.62, 0.1, 0.45), (0.05, 3.1, 0.9), haze_mat)
    animate_object(left_haze, [(1, {"scale": Vector((0.65, 0.65, 0.65))}), (300, {"scale": Vector((1.0, 1.0, 1.0))}), (450, {"scale": Vector((1.2, 1.2, 1.2))})])
    animate_object(right_haze, [(1, {"scale": Vector((0.55, 0.55, 0.55))}), (300, {"scale": Vector((0.95, 0.95, 0.95))}), (450, {"scale": Vector((1.12, 1.12, 1.12))})])
    animate_input(haze_emission.inputs["Strength"], [(1, 0.08), (150, 0.16), (300, 0.28), (450, 0.36)])

    outer_parent = bpy.data.objects.new("p3 outer circle clockwise parent", None)
    inner_parent = bpy.data.objects.new("p3 inner circle counter parent", None)
    bpy.context.collection.objects.link(outer_parent)
    bpy.context.collection.objects.link(inner_parent)
    curve_line("p3 outer ritual ring", circle_points(1.68, 0.045), red_line_mat, 0.014, outer_parent)
    curve_line("p3 outer ritual hairline", circle_points(1.48, 0.052), red_dark_line_mat, 0.007, outer_parent)
    for i in range(40):
        angle = 2 * math.pi * i / 40
        inner = 1.50 if i % 4 else 1.38
        outer = 1.70
        curve_line(
            f"p3 outer clock mark {i:02d}",
            [(math.cos(angle) * inner, math.sin(angle) * inner, 0.065), (math.cos(angle) * outer, math.sin(angle) * outer, 0.065)],
            red_line_mat,
            0.0048 if i % 4 else 0.008,
            outer_parent,
        )
    curve_line("p3 inner ritual ring A", circle_points(1.16, 0.062), red_line_mat, 0.010, inner_parent)
    curve_line("p3 inner ritual ring B", circle_points(0.74, 0.070), red_dark_line_mat, 0.007, inner_parent)
    curve_line("p3 upright triangle sigil", polygon_points(1.30, 0.078, 3, math.radians(90)), red_line_mat, 0.012, inner_parent)
    curve_line("p3 inverted triangle sigil", polygon_points(1.30, 0.082, 3, math.radians(270)), red_line_mat, 0.012, inner_parent)
    for i in range(28):
        angle = 2 * math.pi * i / 28
        radius = 0.90 + 0.10 * (i % 2)
        bead = add_uv_sphere(f"p3 rune bead {i:02d}", 0.022 + 0.006 * (i % 3), (math.cos(angle) * radius, math.sin(angle) * radius, 0.09), red_line_mat, segments=12, rings=6)
        bead.parent = inner_parent
    animate_object(outer_parent, [(1, {"rotation_euler": Vector((0, 0, 0))}), (150, {"rotation_euler": Vector((0, 0, math.radians(-28)))}), (300, {"rotation_euler": Vector((0, 0, math.radians(-82)))}), (450, {"rotation_euler": Vector((0, 0, math.radians(-150)))})])
    animate_object(inner_parent, [(1, {"rotation_euler": Vector((0, 0, 0))}), (150, {"rotation_euler": Vector((0, 0, math.radians(22)))}), (300, {"rotation_euler": Vector((0, 0, math.radians(70)))}), (450, {"rotation_euler": Vector((0, 0, math.radians(130)))})])
    animate_input(red_line_emission.inputs["Strength"], [(1, 2.4), (150, 3.8), (300, 6.0), (420, 8.2), (450, 7.0)])

    core = add_ico_rock("p3 central black monolith", 0.47, (0, 0, 0.36), (0.82, 0.58, 1.34), core_mat, index=99)
    core.rotation_euler = (math.radians(13), math.radians(-20), math.radians(30))

    orb_core = add_uv_sphere("p3 red energy core sphere", 0.28, (0, 0, 1.22), red_core_mat, segments=64, rings=32)
    orb_halo = add_uv_sphere("p3 red halo sphere", 0.50, (0, 0, 1.22), red_halo_mat, segments=48, rings=24)
    orb_shell = add_uv_sphere("p3 outer soft red shell", 0.78, (0, 0, 1.22), red_shell_mat, segments=48, rings=24)
    energy_parent = bpy.data.objects.new("p3 orbiting energy points parent", None)
    bpy.context.collection.objects.link(energy_parent)
    for obj in (orb_core, orb_halo, orb_shell, energy_parent):
        animate_object(obj, [(1, {"location": Vector((0, 0, 1.15))}), (150, {"location": Vector((0.01, 0.0, 1.28))}), (300, {"location": Vector((0.025, -0.012, 1.42))}), (450, {"location": Vector((-0.015, 0.015, 1.35))})])
    animate_object(orb_core, [(1, {"scale": Vector((0.82, 0.82, 0.82))}), (150, {"scale": Vector((1.0, 1.0, 1.0))}), (300, {"scale": Vector((1.16, 1.16, 1.16))}), (450, {"scale": Vector((1.10, 1.10, 1.10))})])
    animate_object(orb_halo, [(1, {"scale": Vector((0.60, 0.60, 0.60))}), (150, {"scale": Vector((0.95, 0.95, 0.95))}), (300, {"scale": Vector((1.22, 1.22, 1.22))}), (450, {"scale": Vector((1.34, 1.34, 1.34))})])
    animate_object(orb_shell, [(1, {"scale": Vector((0.45, 0.45, 0.45))}), (150, {"scale": Vector((0.84, 0.84, 0.84))}), (300, {"scale": Vector((1.24, 1.24, 1.24))}), (450, {"scale": Vector((1.48, 1.48, 1.48))})])
    animate_object(energy_parent, [(1, {"rotation_euler": Vector((0, 0, 0))}), (150, {"rotation_euler": Vector((0, 0, math.radians(90)))}), (300, {"rotation_euler": Vector((0, 0, math.radians(245)))}), (450, {"rotation_euler": Vector((0, 0, math.radians(450)))})])
    for i in range(16):
        angle = 2 * math.pi * i / 16
        particle = add_uv_sphere(f"p3 orbiting energy point {i:02d}", 0.024 + 0.008 * (i % 3), (0, 0, 0), red_line_mat, segments=12, rings=6)
        particle.parent = energy_parent
        particle.location = (math.cos(angle) * 0.57, math.sin(angle) * 0.57, 0.10 * math.sin(angle * 2.0))
    animate_input(red_core_emission.inputs["Strength"], [(1, 5.5), (150, 10.0), (300, 18.0), (420, 24.0), (450, 19.0)])
    animate_input(red_halo_emission.inputs["Strength"], [(1, 1.5), (150, 3.2), (300, 6.5), (420, 8.0), (450, 6.8)])
    animate_input(red_shell_emission.inputs["Strength"], [(1, 0.35), (150, 0.9), (300, 1.8), (420, 2.4), (450, 2.0)])

    for rot, name in [
        ((math.radians(90), 0, 0), "p3 red halo orbit ring X"),
        ((0, math.radians(67), 0), "p3 red halo orbit ring Y"),
        ((math.radians(28), 0, math.radians(35)), "p3 red halo orbit ring tilted"),
    ]:
        ring = add_torus(name, 0.48, 0.008, (0, 0, 1.25), red_dark_line_mat, rotation=rot)
        animate_object(ring, [(1, {"location": Vector((0, 0, 1.15)), "rotation_euler": Vector(rot), "scale": Vector((0.45, 0.45, 0.45))}), (150, {"location": Vector((0, 0, 1.28)), "rotation_euler": Vector((rot[0] + math.radians(40), rot[1], rot[2] + math.radians(55))), "scale": Vector((0.8, 0.8, 0.8))}), (300, {"location": Vector((0.025, -0.012, 1.42)), "rotation_euler": Vector((rot[0] + math.radians(110), rot[1], rot[2] + math.radians(145))), "scale": Vector((1.08, 1.08, 1.08))}), (450, {"location": Vector((-0.015, 0.015, 1.35)), "rotation_euler": Vector((rot[0] + math.radians(170), rot[1], rot[2] + math.radians(240))), "scale": Vector((1.18, 1.18, 1.18))})])

    red_light_data = bpy.data.lights.new("p3 pulsing red orb light", type="POINT")
    red_light_data.color = (1.0, 0.025, 0.0)
    red_light_data.energy = 360
    red_light_data.shadow_soft_size = 5.5
    red_light = bpy.data.objects.new("p3 pulsing red orb light", red_light_data)
    bpy.context.collection.objects.link(red_light)
    animate_object(red_light, [(1, {"location": Vector((0, 0, 1.16))}), (150, {"location": Vector((0.01, 0, 1.29))}), (300, {"location": Vector((0.025, -0.012, 1.43))}), (450, {"location": Vector((-0.015, 0.015, 1.36))})])
    animate_data(red_light.data, "energy", [(1, 300), (150, 640), (300, 1200), (420, 1550), (450, 1120)])

    for index, (x, y) in enumerate([(-1.55, -0.95), (1.48, -0.82), (-0.28, 1.52)], start=1):
        add_candle(index, x, y, wax_mat, wick_mat, warm_inner, warm_outer)

    debris_parent = bpy.data.objects.new("p3 debris ring parent", None)
    bpy.context.collection.objects.link(debris_parent)
    for i in range(56):
        angle = 2 * math.pi * i / 56
        radius = 1.78 + 0.27 * math.sin(i * 1.618) + 0.05 * math.cos(i * 0.7)
        z = 0.055 + 0.022 * (i % 5)
        base = Vector((math.cos(angle) * radius, math.sin(angle) * radius, z))
        rock = add_ico_rock(
            f"p3 orbiting debris {i:02d}",
            0.041 + 0.031 * ((i * 7) % 5) / 4.0,
            base,
            (0.78 + 0.42 * (i % 3), 0.58 + 0.2 * (i % 2), 0.42 + 0.22 * (i % 4)),
            rock_mats[i % len(rock_mats)],
            i,
        )
        rock.parent = debris_parent
        if i % 5 == 0:
            animate_object(rock, [(1, {"location": base}), (150, {"location": Vector((base.x, base.y, base.z + 0.025))}), (300, {"location": Vector((base.x, base.y, base.z + 0.085))}), (450, {"location": Vector((base.x, base.y, base.z + 0.12))})])
    animate_object(debris_parent, [(1, {"rotation_euler": Vector((0, 0, 0))}), (150, {"rotation_euler": Vector((0, 0, math.radians(-22)))}), (300, {"rotation_euler": Vector((0, 0, math.radians(-72)))}), (450, {"rotation_euler": Vector((0, 0, math.radians(-135)))})])

    overhead = bpy.data.lights.new("p3 soft overhead fill", type="AREA")
    overhead.energy = 26
    overhead.size = 5.5
    overhead_obj = bpy.data.objects.new("p3 soft overhead fill", overhead)
    bpy.context.collection.objects.link(overhead_obj)
    overhead_obj.location = (0, -2.2, 4.0)
    rim_data = bpy.data.lights.new("p3 red rear rim light", type="POINT")
    rim_data.color = (1.0, 0.015, 0.0)
    rim_data.energy = 90
    rim_data.shadow_soft_size = 3.5
    rim = bpy.data.objects.new("p3 red rear rim light", rim_data)
    bpy.context.collection.objects.link(rim)
    rim.location = (-1.9, 1.8, 1.2)
    animate_data(rim.data, "energy", [(1, 70), (150, 110), (300, 180), (450, 240)])

    target = bpy.data.objects.new("p3 camera focus target", None)
    bpy.context.collection.objects.link(target)
    target.location = (0, 0, 1.02)
    camera_data = bpy.data.cameras.new("p3 vertical 15s ritual camera")
    camera_data.lens = 42
    camera_data.dof.use_dof = True
    camera_data.dof.focus_object = orb_core
    camera_data.dof.aperture_fstop = 3.2
    camera = bpy.data.objects.new("p3 vertical 15s ritual camera", camera_data)
    bpy.context.collection.objects.link(camera)
    bpy.context.scene.camera = camera
    constraint = camera.constraints.new(type="TRACK_TO")
    constraint.track_axis = "TRACK_NEGATIVE_Z"
    constraint.up_axis = "UP_Y"
    constraint.target = target
    animate_object(
        camera,
        [
            (1, {"location": Vector((2.95, -5.35, 2.92))}),
            (150, {"location": Vector((2.52, -4.75, 2.72))}),
            (300, {"location": Vector((2.06, -4.15, 2.50))}),
            (450, {"location": Vector((1.70, -3.75, 2.34))}),
        ],
    )
    animate_object(
        target,
        [
            (1, {"location": Vector((0, 0, 0.86))}),
            (150, {"location": Vector((0, 0, 0.98))}),
            (300, {"location": Vector((0, 0, 1.10))}),
            (450, {"location": Vector((0, 0, 1.05))}),
        ],
    )

    world = bpy.context.scene.world or bpy.data.worlds.new("World")
    bpy.context.scene.world = world
    world.color = (0.0015, 0.0011, 0.0010)

    bpy.context.scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=str(ensure_inside_workspace(BLEND_PATH)))
    print(f"P3_15S_BLEND_SAVED={BLEND_PATH}")
    print(f"P3_15S_FRAME_OUTPUT={FRAMES_DIR / 'frame_'}")
    print("P3_SHOT_STRUCTURE=establish_frames_1_150,intensify_frames_151_300,climax_frames_301_450")


if __name__ == "__main__":
    main()
