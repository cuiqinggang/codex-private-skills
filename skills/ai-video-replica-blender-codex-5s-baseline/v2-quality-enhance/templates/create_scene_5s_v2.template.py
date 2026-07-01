import math
from pathlib import Path

import bpy
from mathutils import Vector


SCRIPT_PATH = Path(__file__).resolve()
WORKSPACE = SCRIPT_PATH.parents[2]
BLEND_PATH = WORKSPACE / "blender" / "project" / "replica_5s_v2.blend"
FRAMES_DIR = WORKSPACE / "blender" / "renders" / "frames_v2"
MP4_PATH = WORKSPACE / "blender" / "renders" / "replica_5s_v2.mp4"


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
        bpy.data.textures,
    ):
        for datablock in list(collection):
            if datablock.users == 0:
                collection.remove(datablock)


def configure_render() -> None:
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 150
    scene.frame_set(1)
    scene.render.fps = 30
    scene.render.resolution_x = 1080
    scene.render.resolution_y = 1260
    scene.render.resolution_percentage = 100

    try:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    except TypeError:
        scene.render.engine = "BLENDER_EEVEE"

    if hasattr(scene, "eevee"):
        eevee_settings = {
            "taa_render_samples": 48,
            "taa_samples": 24,
            "use_gtao": True,
            "gtao_distance": 3.5,
            "gtao_factor": 1.8,
        }
        for attr, value in eevee_settings.items():
            if hasattr(scene.eevee, attr):
                setattr(scene.eevee, attr, value)

    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.render.filepath = str(ensure_inside_workspace(FRAMES_DIR / "frame_"))
    scene.view_settings.view_transform = "Filmic"
    scene.view_settings.look = "High Contrast"
    scene.view_settings.exposure = -0.55
    scene.view_settings.gamma = 1.0

    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    BLEND_PATH.parent.mkdir(parents=True, exist_ok=True)
    MP4_PATH.parent.mkdir(parents=True, exist_ok=True)
    for old_frame in FRAMES_DIR.glob("frame_*.png"):
        old_frame.unlink()
    if MP4_PATH.exists():
        MP4_PATH.unlink()


def set_alpha_rendering(material) -> None:
    material.diffuse_color = material.diffuse_color
    for attr, value in (
        ("blend_method", "BLEND"),
        ("surface_render_method", "BLENDED"),
        ("show_transparent_back", True),
    ):
        if hasattr(material, attr):
            try:
                setattr(material, attr, value)
            except Exception:
                pass


def principled_material(name: str, base_color, roughness=0.7, metallic=0.0, emission_color=None, emission_strength=0.0, alpha=1.0):
    material = bpy.data.materials.new(name)
    material.diffuse_color = base_color
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        values = {
            "Base Color": base_color,
            "Roughness": roughness,
            "Metallic": metallic,
            "Alpha": alpha,
        }
        if emission_color:
            values["Emission Color"] = emission_color
            values["Emission Strength"] = emission_strength
        for input_name, value in values.items():
            if input_name in bsdf.inputs:
                bsdf.inputs[input_name].default_value = value
    if alpha < 1:
        set_alpha_rendering(material)
    return material


def noisy_principled_material(name: str, base_color, roughness=0.82, metallic=0.0, bump_strength=0.08, noise_scale=32.0):
    material = principled_material(name, base_color, roughness=roughness, metallic=metallic)
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    if not bsdf:
        return material
    noise = nodes.new(type="ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = noise_scale
    noise.inputs["Detail"].default_value = 9.0
    noise.inputs["Roughness"].default_value = 0.62
    bump = nodes.new(type="ShaderNodeBump")
    bump.inputs["Strength"].default_value = bump_strength
    bump.inputs["Distance"].default_value = 0.08
    links.new(noise.outputs["Fac"], bump.inputs["Height"])
    if "Normal" in bsdf.inputs:
        links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return material


def emission_material(name: str, color, strength: float, alpha=1.0):
    material = bpy.data.materials.new(name)
    material.diffuse_color = color
    material.use_nodes = True
    nodes = material.node_tree.nodes
    nodes.clear()
    output = nodes.new(type="ShaderNodeOutputMaterial")
    emission = nodes.new(type="ShaderNodeEmission")
    emission.inputs["Color"].default_value = color
    emission.inputs["Strength"].default_value = strength
    if alpha < 1:
        transparent = nodes.new(type="ShaderNodeBsdfTransparent")
        mix = nodes.new(type="ShaderNodeMixShader")
        mix.inputs["Fac"].default_value = 1.0 - alpha
        material.node_tree.links.new(transparent.outputs["BSDF"], mix.inputs[1])
        material.node_tree.links.new(emission.outputs["Emission"], mix.inputs[2])
        material.node_tree.links.new(mix.outputs["Shader"], output.inputs["Surface"])
        set_alpha_rendering(material)
    else:
        material.node_tree.links.new(emission.outputs["Emission"], output.inputs["Surface"])
    return material, emission


def add_cube(name: str, location, scale, material):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    return obj


def add_cylinder(name: str, radius: float, depth: float, location, material, vertices=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    bevel = obj.modifiers.new("soft bevel", "BEVEL")
    bevel.width = 0.012
    bevel.segments = 3
    obj.modifiers.new("weighted normals", "WEIGHTED_NORMAL")
    return obj


def add_uv_sphere(name: str, radius: float, location, material, segments=48, ring_count=24):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=ring_count, radius=radius, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    return obj


def add_ico_rock(name: str, radius: float, location, scale, material, index=0):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=radius, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    obj.rotation_euler = (
        math.radians((index * 29) % 71 - 35),
        math.radians((index * 47) % 95 - 47),
        math.radians((index * 83) % 180),
    )
    obj.data.materials.append(material)
    return obj


def add_curve_line(name: str, points, material, bevel_depth=0.01, parent=None):
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


def circle_points(radius: float, z: float, count=192, close=True):
    pts = []
    total = count + 1 if close else count
    for i in range(total):
        angle = 2 * math.pi * (i % count) / count
        pts.append((math.cos(angle) * radius, math.sin(angle) * radius, z))
    return pts


def polygon_points(radius: float, z: float, sides: int, offset=0.0):
    pts = []
    for i in range(sides + 1):
        angle = offset + 2 * math.pi * (i % sides) / sides
        pts.append((math.cos(angle) * radius, math.sin(angle) * radius, z))
    return pts


def animate_object(obj, frame_values):
    for frame, attrs in frame_values:
        bpy.context.scene.frame_set(frame)
        for attr, value in attrs.items():
            setattr(obj, attr, value)
            obj.keyframe_insert(data_path=attr, frame=frame)


def animate_data(data, data_path: str, frame_values):
    for frame, value in frame_values:
        bpy.context.scene.frame_set(frame)
        setattr(data, data_path, value)
        data.keyframe_insert(data_path=data_path, frame=frame)


def add_torus(name: str, major_radius: float, minor_radius: float, location, material, rotation=(0, 0, 0), parent=None):
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


def add_candle(index: int, position, wax_mat, wick_mat, flame_inner_mat, flame_outer_mat):
    x, y = position
    wax = add_cylinder(f"v2 candle wax body {index}", 0.12, 0.52, (x, y, 0.26), wax_mat, vertices=40)
    top = add_cylinder(f"v2 candle melted top {index}", 0.128, 0.025, (x, y, 0.535), wax_mat, vertices=40)
    wick = add_cylinder(f"v2 candle black wick {index}", 0.012, 0.13, (x, y, 0.61), wick_mat, vertices=12)
    flame_outer = add_uv_sphere(f"v2 candle outer flame {index}", 0.095, (x, y, 0.70), flame_outer_mat, segments=24, ring_count=12)
    flame_outer.scale = (0.75, 0.75, 1.55)
    flame_inner = add_uv_sphere(f"v2 candle inner flame {index}", 0.048, (x, y, 0.71), flame_inner_mat, segments=16, ring_count=8)
    flame_inner.scale = (0.65, 0.65, 1.3)
    light_data = bpy.data.lights.new(f"v2 warm candle flicker light {index}", type="POINT")
    light_data.color = (1.0, 0.50, 0.18)
    light_data.energy = 120
    light_data.shadow_soft_size = 1.25
    light = bpy.data.objects.new(f"v2 warm candle flicker light {index}", light_data)
    bpy.context.collection.objects.link(light)
    light.location = (x, y, 0.72)
    flicker = [
        (1, 100 + index * 8),
        (35, 152 + index * 5),
        (70, 116 + index * 9),
        (110, 165 + index * 4),
        (150, 125 + index * 7),
    ]
    animate_data(light.data, "energy", flicker)
    return wax, top, wick, flame_outer, flame_inner, light


def main() -> None:
    ensure_inside_workspace(BLEND_PATH)
    ensure_inside_workspace(FRAMES_DIR)
    ensure_inside_workspace(MP4_PATH)
    reset_scene()
    configure_render()

    table_mat = noisy_principled_material("v2 dark oiled rough desktop", (0.015, 0.012, 0.010, 1), roughness=0.88, metallic=0.03, bump_strength=0.055, noise_scale=44)
    panel_mat = noisy_principled_material("v2 matte black notebook background", (0.005, 0.006, 0.008, 1), roughness=0.92, metallic=0.0, bump_strength=0.025, noise_scale=18)
    core_mat = noisy_principled_material("v2 black stone metal core", (0.004, 0.0035, 0.003, 1), roughness=0.46, metallic=0.48, bump_strength=0.11, noise_scale=24)
    wick_mat = principled_material("v2 black candle wick", (0.002, 0.001, 0.001, 1), roughness=0.95)
    wax_mat = noisy_principled_material("v2 warm dark candle wax", (0.13, 0.095, 0.065, 1), roughness=0.62, metallic=0.0, bump_strength=0.035, noise_scale=30)
    rock_mats = [
        noisy_principled_material(f"v2 debris rough stone {i}", color, roughness=0.9, metallic=0.04, bump_strength=0.1, noise_scale=35 + i * 8)
        for i, color in enumerate(
            [
                (0.012, 0.011, 0.010, 1),
                (0.020, 0.017, 0.015, 1),
                (0.028, 0.021, 0.017, 1),
            ]
        )
    ]
    red_core_mat, red_core_emission = emission_material("v2 red hot core emission", (1.0, 0.015, 0.0, 1), 14.0)
    red_halo_mat, red_halo_emission = emission_material("v2 translucent red halo emission", (1.0, 0.035, 0.0, 0.33), 4.5, alpha=0.34)
    red_soft_halo_mat, soft_halo_emission = emission_material("v2 soft outer red haze shell", (0.75, 0.02, 0.0, 0.16), 1.3, alpha=0.18)
    red_line_mat, red_line_emission = emission_material("v2 saturated magic line emission", (1.0, 0.02, 0.0, 1), 5.2)
    red_dark_line_mat, _ = emission_material("v2 dark red secondary line emission", (0.70, 0.01, 0.0, 1), 2.8)
    warm_inner_mat, _ = emission_material("v2 candle inner warm emission", (1.0, 0.78, 0.36, 1), 11.0)
    warm_outer_mat, _ = emission_material("v2 candle outer amber emission", (1.0, 0.40, 0.09, 0.65), 4.5, alpha=0.72)
    haze_mat, _ = emission_material("v2 faint red atmospheric haze", (0.55, 0.015, 0.0, 0.12), 0.35, alpha=0.16)

    table = add_cube("v2 dark desktop with procedural roughness", (0, 0, -0.065), (7.5, 7.5, 0.12), table_mat)
    add_cube("v2 front edge shadow vignette", (0, -2.9, 0.002), (7.5, 0.55, 0.012), panel_mat)
    add_cube("v2 notebook keyboard base", (0, 2.02, 0.035), (5.15, 2.1, 0.08), panel_mat)
    screen = add_cube("v2 dark notebook background panel", (0, 3.02, 1.22), (5.15, 0.12, 2.55), panel_mat)
    screen.rotation_euler[0] = math.radians(-7)
    add_cube("v2 low red screen reflection strip", (0, 2.93, 0.35), (4.8, 0.022, 0.035), haze_mat)

    outer_circle_parent = bpy.data.objects.new("v2 outer clockwise magic circle parent", None)
    inner_circle_parent = bpy.data.objects.new("v2 inner counter magic circle parent", None)
    bpy.context.collection.objects.link(outer_circle_parent)
    bpy.context.collection.objects.link(inner_circle_parent)
    add_curve_line("v2 outer magic ring thick", circle_points(1.68, 0.045), red_line_mat, 0.015, outer_circle_parent)
    add_curve_line("v2 outer magic ring hairline", circle_points(1.48, 0.052), red_dark_line_mat, 0.007, outer_circle_parent)
    for i in range(36):
        angle = 2 * math.pi * i / 36
        inner = 1.50 if i % 3 else 1.40
        outer = 1.69
        add_curve_line(
            f"v2 outer clock tick {i:02d}",
            [(math.cos(angle) * inner, math.sin(angle) * inner, 0.065), (math.cos(angle) * outer, math.sin(angle) * outer, 0.065)],
            red_line_mat,
            0.005 if i % 3 else 0.008,
            outer_circle_parent,
        )
    add_curve_line("v2 inner magic ring A", circle_points(1.16, 0.062), red_line_mat, 0.010, inner_circle_parent)
    add_curve_line("v2 inner magic ring B", circle_points(0.74, 0.070), red_dark_line_mat, 0.007, inner_circle_parent)
    add_curve_line("v2 upright triangle sigil", polygon_points(1.30, 0.078, 3, math.radians(90)), red_line_mat, 0.012, inner_circle_parent)
    add_curve_line("v2 inverted triangle sigil", polygon_points(1.30, 0.082, 3, math.radians(270)), red_line_mat, 0.012, inner_circle_parent)
    for i in range(24):
        angle = 2 * math.pi * i / 24
        radius = 0.92 + 0.08 * (i % 2)
        dot = add_uv_sphere(f"v2 red rune bead {i:02d}", 0.025 + 0.005 * (i % 3), (math.cos(angle) * radius, math.sin(angle) * radius, 0.09), red_line_mat, segments=12, ring_count=6)
        dot.parent = inner_circle_parent
    animate_object(outer_circle_parent, [(1, {"rotation_euler": Vector((0, 0, 0))}), (150, {"rotation_euler": Vector((0, 0, math.radians(-44)))})])
    animate_object(inner_circle_parent, [(1, {"rotation_euler": Vector((0, 0, 0))}), (150, {"rotation_euler": Vector((0, 0, math.radians(34)))})])
    for frame, strength in [(1, 4.0), (45, 6.6), (90, 4.8), (150, 6.0)]:
        bpy.context.scene.frame_set(frame)
        red_line_emission.inputs["Strength"].default_value = strength
        red_line_emission.inputs["Strength"].keyframe_insert(data_path="default_value", frame=frame)

    core = add_ico_rock("v2 central black stone metal monolith", 0.47, (0, 0, 0.36), (0.82, 0.58, 1.34), core_mat, index=99)
    core.rotation_euler = (math.radians(13), math.radians(-20), math.radians(30))

    orb_core = add_uv_sphere("v2 floating red energy core sphere", 0.29, (0, 0, 1.33), red_core_mat, segments=64, ring_count=32)
    orb_halo = add_uv_sphere("v2 translucent red halo sphere", 0.50, (0, 0, 1.33), red_halo_mat, segments=48, ring_count=24)
    orb_soft = add_uv_sphere("v2 soft outer red atmospheric shell", 0.78, (0, 0, 1.33), red_soft_halo_mat, segments=48, ring_count=24)
    energy_parent = bpy.data.objects.new("v2 orbiting energy particles parent", None)
    bpy.context.collection.objects.link(energy_parent)
    for obj in (orb_core, orb_halo, orb_soft, energy_parent):
        animate_object(
            obj,
            [
                (1, {"location": Vector((0, 0, 1.22))}),
                (75, {"location": Vector((0.02, -0.01, 1.45))}),
                (150, {"location": Vector((-0.01, 0.01, 1.25))}),
            ],
        )
    animate_object(orb_halo, [(1, {"scale": Vector((0.96, 0.96, 0.96))}), (75, {"scale": Vector((1.18, 1.18, 1.18))}), (150, {"scale": Vector((1.02, 1.02, 1.02))})])
    animate_object(orb_soft, [(1, {"scale": Vector((0.92, 0.92, 0.92))}), (75, {"scale": Vector((1.25, 1.25, 1.25))}), (150, {"scale": Vector((1.00, 1.00, 1.00))})])
    animate_object(energy_parent, [(1, {"rotation_euler": Vector((0, 0, 0))}), (150, {"rotation_euler": Vector((0, 0, math.radians(145)))})])
    for i in range(14):
        angle = 2 * math.pi * i / 14
        particle = add_uv_sphere(f"v2 orbiting red energy point {i:02d}", 0.028 + 0.008 * (i % 3), (0, 0, 0), red_line_mat, segments=12, ring_count=6)
        particle.parent = energy_parent
        particle.location = (math.cos(angle) * 0.55, math.sin(angle) * 0.55, 0.10 * math.sin(angle * 2.0))
    for frame, strength in [(1, 10.0), (40, 18.0), (80, 12.5), (120, 20.0), (150, 14.0)]:
        bpy.context.scene.frame_set(frame)
        red_core_emission.inputs["Strength"].default_value = strength
        red_core_emission.inputs["Strength"].keyframe_insert(data_path="default_value", frame=frame)
        red_halo_emission.inputs["Strength"].default_value = max(2.8, strength * 0.33)
        red_halo_emission.inputs["Strength"].keyframe_insert(data_path="default_value", frame=frame)
        soft_halo_emission.inputs["Strength"].default_value = max(0.8, strength * 0.10)
        soft_halo_emission.inputs["Strength"].keyframe_insert(data_path="default_value", frame=frame)
    for rot, name in [
        ((math.radians(90), 0, 0), "v2 red orbital halo ring X"),
        ((0, math.radians(67), 0), "v2 red orbital halo ring Y"),
        ((math.radians(28), math.radians(0), math.radians(35)), "v2 red orbital halo ring tilted"),
    ]:
        ring = add_torus(name, 0.48, 0.008, (0, 0, 1.33), red_dark_line_mat, rotation=rot)
        animate_object(ring, [(1, {"rotation_euler": Vector(rot)}), (150, {"rotation_euler": Vector((rot[0] + math.radians(80), rot[1], rot[2] + math.radians(120)))})])

    red_light_data = bpy.data.lights.new("v2 pulsing red orb light", type="POINT")
    red_light_data.color = (1.0, 0.025, 0.0)
    red_light_data.energy = 760
    red_light_data.shadow_soft_size = 5.5
    red_light = bpy.data.objects.new("v2 pulsing red orb light", red_light_data)
    bpy.context.collection.objects.link(red_light)
    animate_object(red_light, [(1, {"location": Vector((0, 0, 1.23))}), (75, {"location": Vector((0.02, -0.01, 1.46))}), (150, {"location": Vector((-0.01, 0.01, 1.26))})])
    animate_data(red_light.data, "energy", [(1, 520), (40, 1050), (80, 640), (120, 1180), (150, 780)])

    for index, pos in enumerate([(-1.55, -0.95), (1.48, -0.82), (-0.28, 1.52)], start=1):
        add_candle(index, pos, wax_mat, wick_mat, warm_inner_mat, warm_outer_mat)

    debris_parent = bpy.data.objects.new("v2 animated debris and particle ring", None)
    bpy.context.collection.objects.link(debris_parent)
    for i in range(54):
        angle = 2 * math.pi * i / 54
        radius = 1.78 + 0.27 * math.sin(i * 1.618) + 0.05 * math.cos(i * 0.7)
        z = 0.055 + 0.025 * (i % 5)
        rock = add_ico_rock(
            f"v2 irregular orbiting debris {i:02d}",
            0.042 + 0.032 * ((i * 7) % 5) / 4.0,
            (math.cos(angle) * radius, math.sin(angle) * radius, z),
            (0.78 + 0.42 * (i % 3), 0.58 + 0.2 * (i % 2), 0.42 + 0.22 * (i % 4)),
            rock_mats[i % len(rock_mats)],
            index=i,
        )
        rock.parent = debris_parent
        if i % 7 == 0:
            base = Vector((rock.location.x, rock.location.y, rock.location.z))
            animate_object(
                rock,
                [
                    (1, {"location": base}),
                    (75, {"location": Vector((base.x, base.y, base.z + 0.075))}),
                    (150, {"location": Vector((base.x, base.y, base.z + 0.015))}),
                ],
            )
    animate_object(debris_parent, [(1, {"rotation_euler": Vector((0, 0, 0))}), (150, {"rotation_euler": Vector((0, 0, math.radians(-31)))})])

    add_cube("v2 dim left haze card", (-2.6, 0.2, 0.55), (0.05, 3.4, 1.1), haze_mat)
    add_cube("v2 dim right haze card", (2.6, 0.1, 0.45), (0.05, 3.0, 0.9), haze_mat)

    overhead = bpy.data.lights.new("v2 soft dark overhead fill", type="AREA")
    overhead.energy = 34
    overhead.size = 5.5
    overhead_obj = bpy.data.objects.new("v2 soft dark overhead fill", overhead)
    bpy.context.collection.objects.link(overhead_obj)
    overhead_obj.location = (0, -2.2, 4.0)
    rim = bpy.data.lights.new("v2 red rear rim light", type="POINT")
    rim.color = (1.0, 0.015, 0.0)
    rim.energy = 140
    rim.shadow_soft_size = 3.5
    rim_obj = bpy.data.objects.new("v2 red rear rim light", rim)
    bpy.context.collection.objects.link(rim_obj)
    rim_obj.location = (-1.9, 1.8, 1.2)

    target = bpy.data.objects.new("v2 camera focus target", None)
    bpy.context.collection.objects.link(target)
    target.location = (0, 0, 0.98)
    camera_data = bpy.data.cameras.new("v2 vertical cinematic ritual camera")
    camera_data.lens = 46
    camera_data.dof.use_dof = True
    camera_data.dof.focus_object = orb_core
    camera_data.dof.aperture_fstop = 3.2
    camera = bpy.data.objects.new("v2 vertical cinematic ritual camera", camera_data)
    bpy.context.collection.objects.link(camera)
    bpy.context.scene.camera = camera
    constraint = camera.constraints.new(type="TRACK_TO")
    constraint.track_axis = "TRACK_NEGATIVE_Z"
    constraint.up_axis = "UP_Y"
    constraint.target = target
    animate_object(
        camera,
        [
            (1, {"location": Vector((2.60, -4.82, 2.72))}),
            (75, {"location": Vector((2.18, -4.28, 2.52))}),
            (150, {"location": Vector((1.76, -3.82, 2.37))}),
        ],
    )

    world = bpy.context.scene.world or bpy.data.worlds.new("World")
    bpy.context.scene.world = world
    world.color = (0.0018, 0.0013, 0.0012)

    bpy.context.scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=str(ensure_inside_workspace(BLEND_PATH)))
    print(f"P2_V2_BLEND_SAVED={BLEND_PATH}")
    print(f"P2_V2_FRAME_OUTPUT={FRAMES_DIR / 'frame_'}")


if __name__ == "__main__":
    main()
