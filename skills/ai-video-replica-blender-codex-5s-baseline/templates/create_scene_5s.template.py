import math
import shutil
from pathlib import Path

import bpy
from mathutils import Vector


SCRIPT_PATH = Path(__file__).resolve()
WORKSPACE = SCRIPT_PATH.parents[2]
BLEND_PATH = WORKSPACE / "blender" / "project" / "replica_5s.blend"
FRAMES_DIR = WORKSPACE / "blender" / "renders" / "frames"
MP4_PATH = WORKSPACE / "blender" / "renders" / "replica_5s.mp4"


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
        for attr, value in {
            "taa_render_samples": 32,
            "taa_samples": 16,
            "use_gtao": True,
            "gtao_distance": 3,
            "gtao_factor": 1.5,
        }.items():
            if hasattr(scene.eevee, attr):
                setattr(scene.eevee, attr, value)

    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.render.filepath = str(ensure_inside_workspace(FRAMES_DIR / "frame_"))
    scene.view_settings.view_transform = "Filmic"
    scene.view_settings.look = "Medium High Contrast"
    scene.view_settings.exposure = -0.2
    scene.view_settings.gamma = 1.0

    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    BLEND_PATH.parent.mkdir(parents=True, exist_ok=True)
    MP4_PATH.parent.mkdir(parents=True, exist_ok=True)
    for old_frame in FRAMES_DIR.glob("frame_*.png"):
        old_frame.unlink()
    if MP4_PATH.exists():
        MP4_PATH.unlink()


def emission_material(name: str, color, strength: float):
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    nodes.clear()
    output = nodes.new(type="ShaderNodeOutputMaterial")
    emission = nodes.new(type="ShaderNodeEmission")
    emission.inputs["Color"].default_value = color
    emission.inputs["Strength"].default_value = strength
    material.node_tree.links.new(emission.outputs["Emission"], output.inputs["Surface"])
    return material, emission


def principled_material(name: str, base_color, roughness=0.65, metallic=0.0, emission_color=None, emission_strength=0.0):
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = base_color
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = roughness
        if "Metallic" in bsdf.inputs:
            bsdf.inputs["Metallic"].default_value = metallic
        if emission_color and "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = emission_color
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = emission_strength
    return material


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
    return obj


def add_uv_sphere(name: str, radius: float, location, material, segments=48, ring_count=24):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=ring_count, radius=radius, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    return obj


def add_ico_rock(name: str, radius: float, location, scale, material):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=radius, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    obj.rotation_euler = (
        math.radians((hash(name) % 57) - 28),
        math.radians((hash(name) % 91) - 45),
        math.radians(hash(name) % 180),
    )
    obj.data.materials.append(material)
    return obj


def add_curve_line(name: str, points, material, bevel_depth=0.01, parent=None):
    curve = bpy.data.curves.new(name, type="CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 1
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


def circle_points(radius: float, z: float, count=160, close=True):
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


def main() -> None:
    ensure_inside_workspace(BLEND_PATH)
    ensure_inside_workspace(FRAMES_DIR)
    ensure_inside_workspace(MP4_PATH)
    reset_scene()
    configure_render()

    dark_table = principled_material("dark rough tabletop", (0.025, 0.021, 0.019, 1), roughness=0.92)
    dark_panel = principled_material("nearly black notebook panel", (0.012, 0.014, 0.018, 1), roughness=0.8)
    black_stone = principled_material("black stone metal core", (0.006, 0.005, 0.005, 1), roughness=0.5, metallic=0.35)
    rock_mat = principled_material("charcoal debris", (0.02, 0.018, 0.016, 1), roughness=0.85)
    wax_mat = principled_material("dark candle wax", (0.11, 0.085, 0.06, 1), roughness=0.55)
    warm_emit, _ = emission_material("warm candle flame emission", (1.0, 0.46, 0.12, 1), 8.0)
    red_emit, red_emission_node = emission_material("red energy emission", (1.0, 0.02, 0.0, 1), 9.0)
    red_line_emit, _ = emission_material("red magic circle emission", (1.0, 0.025, 0.0, 1), 4.0)

    add_cube("dark desktop plane", (0, 0, -0.055), (7.0, 7.0, 0.1), dark_table)
    add_cube("flat notebook keyboard base", (0, 1.95, 0.03), (4.8, 2.2, 0.08), dark_panel)
    screen = add_cube("dark notebook background panel", (0, 2.95, 1.25), (4.8, 0.12, 2.4), dark_panel)
    screen.rotation_euler[0] = math.radians(-8)

    circle_empty = bpy.data.objects.new("animated magic circle parent", None)
    bpy.context.collection.objects.link(circle_empty)
    add_curve_line("outer red magic circle", circle_points(1.55, 0.045), red_line_emit, 0.012, circle_empty)
    add_curve_line("inner red magic circle", circle_points(1.18, 0.05), red_line_emit, 0.009, circle_empty)
    add_curve_line("center red magic circle", circle_points(0.72, 0.055), red_line_emit, 0.007, circle_empty)
    add_curve_line("upright triangle sigil", polygon_points(1.28, 0.065, 3, math.radians(90)), red_line_emit, 0.01, circle_empty)
    add_curve_line("inverted triangle sigil", polygon_points(1.28, 0.067, 3, math.radians(270)), red_line_emit, 0.01, circle_empty)
    for i in range(24):
        angle = 2 * math.pi * i / 24
        inner = 1.35 if i % 2 else 1.43
        outer = 1.51
        pts = [
            (math.cos(angle) * inner, math.sin(angle) * inner, 0.075),
            (math.cos(angle) * outer, math.sin(angle) * outer, 0.075),
        ]
        add_curve_line(f"rune radial mark {i:02d}", pts, red_line_emit, 0.006, circle_empty)
    for i in range(18):
        angle = 2 * math.pi * i / 18
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.025, location=(math.cos(angle) * 0.95, math.sin(angle) * 0.95, 0.08))
        dot = bpy.context.object
        dot.name = f"red rune dot {i:02d}"
        dot.data.materials.append(red_line_emit)
        dot.parent = circle_empty

    core = add_ico_rock("central black stone metal body", 0.42, (0, 0, 0.32), (0.8, 0.62, 1.25), black_stone)
    core.rotation_euler = (math.radians(12), math.radians(-18), math.radians(28))

    orb = add_uv_sphere("floating red energy orb", 0.34, (0, 0, 1.28), red_emit)
    animate_object(
        orb,
        [
            (1, {"location": Vector((0, 0, 1.20)), "scale": Vector((1.0, 1.0, 1.0))}),
            (75, {"location": Vector((0, 0, 1.42)), "scale": Vector((1.12, 1.12, 1.12))}),
            (150, {"location": Vector((0, 0, 1.22)), "scale": Vector((1.0, 1.0, 1.0))}),
        ],
    )
    for frame, strength in [(1, 7.0), (45, 13.0), (90, 8.0), (150, 12.0)]:
        bpy.context.scene.frame_set(frame)
        red_emission_node.inputs["Strength"].default_value = strength
        red_emission_node.inputs["Strength"].keyframe_insert(data_path="default_value", frame=frame)

    red_light_data = bpy.data.lights.new("pulsing red point light", type="POINT")
    red_light_data.color = (1.0, 0.035, 0.02)
    red_light_data.energy = 450
    red_light_data.shadow_soft_size = 4.0
    red_light = bpy.data.objects.new("pulsing red point light", red_light_data)
    bpy.context.collection.objects.link(red_light)
    red_light.location = (0, 0, 1.35)
    for frame, energy in [(1, 350), (45, 820), (90, 430), (150, 700)]:
        bpy.context.scene.frame_set(frame)
        red_light.data.energy = energy
        red_light.data.keyframe_insert(data_path="energy", frame=frame)

    candle_positions = [(-1.45, -0.88, 0.22), (1.45, -0.88, 0.22), (0.0, 1.48, 0.22)]
    for i, pos in enumerate(candle_positions):
        add_cylinder(f"candle wax column {i+1}", 0.105, 0.44, pos, wax_mat, vertices=32)
        flame = add_uv_sphere(f"warm candle flame {i+1}", 0.08, (pos[0], pos[1], pos[2] + 0.3), warm_emit, segments=24, ring_count=12)
        flame.scale = (0.72, 0.72, 1.35)
        light_data = bpy.data.lights.new(f"warm candle light {i+1}", type="POINT")
        light_data.color = (1.0, 0.47, 0.16)
        light_data.energy = 95
        light_data.shadow_soft_size = 1.2
        light = bpy.data.objects.new(f"warm candle light {i+1}", light_data)
        bpy.context.collection.objects.link(light)
        light.location = (pos[0], pos[1], pos[2] + 0.36)

    debris_empty = bpy.data.objects.new("animated debris ring parent", None)
    bpy.context.collection.objects.link(debris_empty)
    for i in range(36):
        angle = 2 * math.pi * i / 36
        radius = 1.85 + 0.16 * math.sin(i * 1.7)
        z = 0.06 + 0.035 * (i % 4)
        rock = add_ico_rock(
            f"orbiting charcoal shard {i:02d}",
            0.055 + 0.025 * (i % 3),
            (math.cos(angle) * radius, math.sin(angle) * radius, z),
            (1.0 + 0.5 * (i % 2), 0.7, 0.45 + 0.2 * (i % 3)),
            rock_mat,
        )
        rock.parent = debris_empty

    animate_object(
        circle_empty,
        [
            (1, {"rotation_euler": Vector((0, 0, 0))}),
            (150, {"rotation_euler": Vector((0, 0, math.radians(38)))}),
        ],
    )
    animate_object(
        debris_empty,
        [
            (1, {"rotation_euler": Vector((0, 0, 0))}),
            (150, {"rotation_euler": Vector((0, 0, math.radians(-24)))}),
        ],
    )

    ambient = bpy.data.lights.new("soft overhead fill", type="AREA")
    ambient.energy = 80
    ambient.size = 5
    ambient_obj = bpy.data.objects.new("soft overhead fill", ambient)
    bpy.context.collection.objects.link(ambient_obj)
    ambient_obj.location = (0, -2.4, 4.0)

    target = bpy.data.objects.new("camera target red orb", None)
    bpy.context.collection.objects.link(target)
    target.location = (0, 0, 0.82)
    camera_data = bpy.data.cameras.new("vertical ritual camera")
    camera_data.lens = 38
    camera_data.dof.use_dof = True
    camera_data.dof.focus_object = orb
    camera_data.dof.aperture_fstop = 4.5
    camera = bpy.data.objects.new("vertical ritual camera", camera_data)
    bpy.context.collection.objects.link(camera)
    bpy.context.scene.camera = camera
    constraint = camera.constraints.new(type="TRACK_TO")
    constraint.track_axis = "TRACK_NEGATIVE_Z"
    constraint.up_axis = "UP_Y"
    constraint.target = target
    animate_object(
        camera,
        [
            (1, {"location": Vector((2.45, -4.75, 2.65))}),
            (75, {"location": Vector((2.15, -4.25, 2.45))}),
            (150, {"location": Vector((1.82, -3.95, 2.32))}),
        ],
    )

    world = bpy.context.scene.world or bpy.data.worlds.new("World")
    bpy.context.scene.world = world
    world.color = (0.005, 0.002, 0.002)

    bpy.context.scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=str(ensure_inside_workspace(BLEND_PATH)))
    print(f"BLEND_SAVED={BLEND_PATH}")
    print(f"FRAME_OUTPUT={FRAMES_DIR / 'frame_'}")


if __name__ == "__main__":
    main()
