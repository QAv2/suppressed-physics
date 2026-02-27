"""
Blender Export — Bench-Scale Reference Frame Engine Prototype

Generates a 3D model of the device with all verified dimensions from
prototype-spec.md and simulator config.py. Run headless:

    ~/blender/blender --background --python simulator/export/blender_export.py

Output: device-design/prototype-model.blend  (editable Blender file)
        device-design/prototype-render.png   (preview render)
"""

import bpy
import math
import os
import sys

# ---------------------------------------------------------------------------
# PARAMETERS — all from prototype-spec.md (VERIFIED or design choice)
# ---------------------------------------------------------------------------

# Device geometry (meters)
SPHERE_RADIUS = 0.05          # 5 cm ceramic sphere
SPHERE_WALL = 0.003           # 3 mm wall thickness (ceramic)
CORE_RADIUS = 0.008           # 8 mm Pb core
CORE_EQUILIBRIUM_Y = -0.0105  # 10.5 mm below center (VERIFIED, clean rerun exp 1)

# Coil geometry — Helmholtz pairs (wire-bundle toroids), nested at decreasing radii
# Helmholtz spacing: each pair at ±R/2 along its axis
COIL_Z_RADIUS = 0.225         # 22.5 cm — outermost pair
COIL_Y_RADIUS = 0.18          # 18 cm — middle pair
COIL_X_RADIUS = 0.14          # 14 cm — innermost pair
WIRE_BUNDLE_RADIUS = 0.01     # 1 cm wire bundle cross-section radius

# Mercury fills interior (sphere minus core)
MERCURY_RADIUS = SPHERE_RADIUS - SPHERE_WALL  # Inner cavity

# Scene scale — work in meters, scale for nice viewport
SCALE = 1.0  # Keep 1:1, Blender handles meters fine

# Colors (linear RGB, 0-1 range)
COLOR_CERAMIC = (0.85, 0.88, 0.90, 0.3)    # Translucent white/grey
COLOR_MERCURY = (0.70, 0.76, 0.82, 0.6)    # Silvery, semi-transparent
COLOR_LEAD = (0.35, 0.35, 0.40, 1.0)       # Dark grey
COLOR_COIL_X = (0.86, 0.23, 0.23, 1.0)     # Red
COLOR_COIL_Y = (0.23, 0.86, 0.23, 1.0)     # Green
COLOR_COIL_Z = (0.23, 0.39, 0.86, 1.0)     # Blue
COLOR_SUPPORT = (0.3, 0.3, 0.3, 1.0)       # Dark frame


# ---------------------------------------------------------------------------
# UTILITY FUNCTIONS
# ---------------------------------------------------------------------------

def clear_scene():
    """Remove all default objects."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    # Remove orphan data
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)


def make_material(name, color, metallic=0.0, roughness=0.5, transmission=0.0):
    """Create a Principled BSDF material."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    mat.surface_render_method = 'BLENDED' if color[3] < 1.0 else 'DITHERED'
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Metallic'].default_value = metallic
        bsdf.inputs['Roughness'].default_value = roughness
        if transmission > 0:
            bsdf.inputs['Transmission Weight'].default_value = transmission
        bsdf.inputs['Alpha'].default_value = color[3]
    return mat


def move_to_collection(obj, target_col):
    """Move object from all current collections into target_col."""
    for col in obj.users_collection:
        col.objects.unlink(obj)
    target_col.objects.link(obj)


def create_pancake_coil(name, outer_radius, inner_radius, height, location, rotation, material):
    """Create a flat annular disc (pancake coil) using bmesh.

    Builds an annular cylinder: outer ring, inner bore, top/bottom faces, walls.
    64 segments for smooth circles.
    """
    import bmesh

    segments = 64
    half_h = height / 2.0

    bm = bmesh.new()

    # Create vertex rings: outer-top, outer-bottom, inner-top, inner-bottom
    rings = []
    for r, z in [(outer_radius, half_h), (outer_radius, -half_h),
                 (inner_radius, half_h), (inner_radius, -half_h)]:
        verts = []
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            verts.append(bm.verts.new((r * math.cos(angle), r * math.sin(angle), z)))
        rings.append(verts)

    outer_top, outer_bot, inner_top, inner_bot = rings

    # Top face (outer_top → inner_top, reversed for correct normal)
    for i in range(segments):
        j = (i + 1) % segments
        bm.faces.new([outer_top[i], outer_top[j], inner_top[j], inner_top[i]])

    # Bottom face (outer_bot → inner_bot)
    for i in range(segments):
        j = (i + 1) % segments
        bm.faces.new([outer_bot[j], outer_bot[i], inner_bot[i], inner_bot[j]])

    # Outer wall (outer_top → outer_bot)
    for i in range(segments):
        j = (i + 1) % segments
        bm.faces.new([outer_top[j], outer_top[i], outer_bot[i], outer_bot[j]])

    # Inner wall (inner_top → inner_bot, reversed winding for inward-facing normal)
    for i in range(segments):
        j = (i + 1) % segments
        bm.faces.new([inner_top[i], inner_top[j], inner_bot[j], inner_bot[i]])

    bm.normal_update()

    # Create mesh and object
    mesh = bpy.data.meshes.new(f"{name}_mesh")
    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    # Set transform
    obj.location = location
    obj.rotation_euler = rotation

    # Apply material
    obj.data.materials.append(material)

    # Smooth shading
    for face in obj.data.polygons:
        face.use_smooth = True

    return obj


def create_helmholtz_pair(name, coil_radius, wire_radius, axis, material, coils_col):
    """Create a Helmholtz pair: two torus coils at ±R/2 along the specified axis.

    axis: 'X', 'Y', or 'Z'
    Returns list of two torus objects.
    """
    half_sep = coil_radius / 2.0  # Helmholtz spacing: ±R/2
    coils = []

    for sign, label in [(+1, "A"), (-1, "B")]:
        offset = sign * half_sep

        # Position along the pair's axis
        if axis == 'Z':
            loc = (0, 0, offset)
            rot = (0, 0, 0)  # Torus default is in XY plane — correct for Z-axis pair
        elif axis == 'Y':
            loc = (0, offset, 0)
            rot = (math.pi / 2, 0, 0)  # Rotate torus from XY into XZ plane
        elif axis == 'X':
            loc = (offset, 0, 0)
            rot = (0, math.pi / 2, 0)  # Rotate torus from XY into YZ plane

        bpy.ops.mesh.primitive_torus_add(
            major_radius=coil_radius,
            minor_radius=wire_radius,
            major_segments=64,
            minor_segments=24,
            location=loc,
            rotation=rot,
        )
        torus = bpy.context.active_object
        torus.name = f"{name}_{label}"
        torus.data.materials.append(material)

        # Smooth shading
        for face in torus.data.polygons:
            face.use_smooth = True

        move_to_collection(torus, coils_col)
        coils.append(torus)

    return coils


# ---------------------------------------------------------------------------
# BUILD THE DEVICE
# ---------------------------------------------------------------------------

def build_device():
    """Construct the full device assembly."""

    clear_scene()

    # -- Collection for organization --
    device_col = bpy.data.collections.new("Device Assembly")
    bpy.context.scene.collection.children.link(device_col)

    coils_col = bpy.data.collections.new("Coils")
    device_col.children.link(coils_col)

    internals_col = bpy.data.collections.new("Internals")
    device_col.children.link(internals_col)

    # ===================================================================
    # CERAMIC SPHERE (outer shell) — translucent
    # ===================================================================
    mat_ceramic = make_material("Ceramic", COLOR_CERAMIC, roughness=0.3, transmission=0.7)

    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=SPHERE_RADIUS,
        segments=64, ring_count=32,
        location=(0, 0, 0),
    )
    sphere = bpy.context.active_object
    sphere.name = "Ceramic_Sphere"
    sphere.data.materials.append(mat_ceramic)
    bpy.ops.object.shade_smooth()
    move_to_collection(sphere, device_col)

    # ===================================================================
    # MERCURY (inner volume) — semi-transparent silver
    # ===================================================================
    mat_mercury = make_material("Mercury", COLOR_MERCURY, metallic=0.9, roughness=0.1, transmission=0.3)

    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=MERCURY_RADIUS,
        segments=48, ring_count=24,
        location=(0, 0, 0),
    )
    mercury = bpy.context.active_object
    mercury.name = "Mercury"
    mercury.data.materials.append(mat_mercury)
    bpy.ops.object.shade_smooth()
    move_to_collection(mercury, internals_col)

    # ===================================================================
    # LEAD CORE — at verified equilibrium position (10.5mm below center)
    # ===================================================================
    mat_lead = make_material("Lead", COLOR_LEAD, metallic=0.6, roughness=0.4)

    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=CORE_RADIUS,
        segments=32, ring_count=16,
        location=(0, 0, CORE_EQUILIBRIUM_Y),  # Z is up in Blender; core below center
    )
    core = bpy.context.active_object
    core.name = "Pb_Core"
    core.data.materials.append(mat_lead)
    bpy.ops.object.shade_smooth()
    move_to_collection(core, internals_col)

    # ===================================================================
    # HELMHOLTZ COIL PAIRS — 3 orthogonal axes, 2 coils each
    # Wire-bundle toroids at decreasing radii for nesting clearance
    # Z (outermost, blue), Y (middle, green), X (innermost, red)
    # ===================================================================
    mat_x = make_material("Coil_X", COLOR_COIL_X, metallic=0.8, roughness=0.3)
    mat_y = make_material("Coil_Y", COLOR_COIL_Y, metallic=0.8, roughness=0.3)
    mat_z = make_material("Coil_Z", COLOR_COIL_Z, metallic=0.8, roughness=0.3)

    # Z pair (outermost): torus in XY plane, at z = ±11.25 cm
    create_helmholtz_pair("Coil_Z", COIL_Z_RADIUS, WIRE_BUNDLE_RADIUS, 'Z', mat_z, coils_col)

    # Y pair (middle): torus in XZ plane, at y = ±9 cm
    create_helmholtz_pair("Coil_Y", COIL_Y_RADIUS, WIRE_BUNDLE_RADIUS, 'Y', mat_y, coils_col)

    # X pair (innermost): torus in YZ plane, at x = ±7 cm
    create_helmholtz_pair("Coil_X", COIL_X_RADIUS, WIRE_BUNDLE_RADIUS, 'X', mat_x, coils_col)

    # ===================================================================
    # AXIS INDICATORS — thin cylinders showing X, Y, Z through sphere
    # ===================================================================
    axis_length = COIL_Z_RADIUS * 1.3  # Sized to outermost pair
    axis_radius = 0.001  # 1mm thin line
    axis_configs = [
        ("Axis_X", (axis_length / 2, 0, 0), (0, math.pi / 2, 0), COLOR_COIL_X),
        ("Axis_Y", (0, axis_length / 2, 0), (math.pi / 2, 0, 0), COLOR_COIL_Y),
        ("Axis_Z", (0, 0, axis_length / 2), (0, 0, 0), COLOR_COIL_Z),
    ]
    for name, loc, rot, color in axis_configs:
        mat = make_material(f"Mat_{name}", (*color[:3], 0.5), roughness=0.8)
        bpy.ops.mesh.primitive_cylinder_add(
            radius=axis_radius,
            depth=axis_length,
            location=loc,
            rotation=rot,
        )
        ax = bpy.context.active_object
        ax.name = name
        ax.data.materials.append(mat)
        move_to_collection(ax, device_col)

    # ===================================================================
    # ANNOTATIONS — empties marking key positions
    # ===================================================================
    # Core equilibrium marker
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, CORE_EQUILIBRIUM_Y), radius=0.015)
    eq_marker = bpy.context.active_object
    eq_marker.name = "Pb_Equilibrium_10.5mm"
    move_to_collection(eq_marker, internals_col)

    # Sphere center marker
    bpy.ops.object.empty_add(type='SPHERE', location=(0, 0, 0), radius=0.005)
    center_marker = bpy.context.active_object
    center_marker.name = "Sphere_Center"
    move_to_collection(center_marker, internals_col)

    return device_col


# ---------------------------------------------------------------------------
# CAMERA & LIGHTING
# ---------------------------------------------------------------------------

def setup_camera_and_lights():
    """Set up camera for a good 3/4 view and studio-style lighting."""

    # Camera — 3/4 view, slightly above
    bpy.ops.object.camera_add(
        location=(0.45, -0.45, 0.30),
        rotation=(math.radians(65), 0, math.radians(45)),
    )
    camera = bpy.context.active_object
    camera.name = "Camera"
    camera.data.lens = 50  # mm
    camera.data.clip_end = 10
    bpy.context.scene.camera = camera

    # Key light — warm, from upper right
    bpy.ops.object.light_add(type='AREA', location=(0.5, -0.3, 0.5))
    key = bpy.context.active_object
    key.name = "Key_Light"
    key.data.energy = 50
    key.data.size = 0.5
    key.data.color = (1.0, 0.95, 0.9)

    # Fill light — cooler, from left
    bpy.ops.object.light_add(type='AREA', location=(-0.4, -0.2, 0.3))
    fill = bpy.context.active_object
    fill.name = "Fill_Light"
    fill.data.energy = 20
    fill.data.size = 0.8
    fill.data.color = (0.9, 0.92, 1.0)

    # Rim light — from behind
    bpy.ops.object.light_add(type='AREA', location=(-0.1, 0.5, 0.2))
    rim = bpy.context.active_object
    rim.name = "Rim_Light"
    rim.data.energy = 30
    rim.data.size = 0.3

    # World background — dark
    world = bpy.data.worlds.get("World")
    if world and world.use_nodes:
        bg = world.node_tree.nodes.get("Background")
        if bg:
            bg.inputs['Color'].default_value = (0.02, 0.02, 0.04, 1.0)
            bg.inputs['Strength'].default_value = 0.5


# ---------------------------------------------------------------------------
# RENDER SETTINGS
# ---------------------------------------------------------------------------

def setup_render(output_path, engine='CYCLES'):
    """Configure render. engine='BLENDER_EEVEE_NEXT' or 'CYCLES'."""
    scene = bpy.context.scene

    scene.render.engine = engine
    if engine == 'CYCLES':
        scene.cycles.device = 'CPU'
        scene.cycles.samples = 32  # Fast preview — re-render from .blend for quality
        scene.cycles.use_denoising = False  # Denoising was the 60-min bottleneck
    else:
        scene.eevee.taa_render_samples = 64

    # Resolution
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100

    # Output
    scene.render.filepath = output_path
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'

    # Film transparent background (nice for docs)
    scene.render.film_transparent = True


# ---------------------------------------------------------------------------
# TEXT LABELS (as mesh text objects)
# ---------------------------------------------------------------------------

def add_labels():
    """Add dimension labels as text objects."""
    labels = [
        ("R = 5 cm", (0.06, 0, 0), 0.008),
        ("Pb core (r=8mm)", (0.02, 0, CORE_EQUILIBRIUM_Y - 0.015), 0.005),
        ("10.5 mm below center", (-0.06, 0, CORE_EQUILIBRIUM_Y), 0.004),
        ("Z pair: R=22.5cm", (0, 0, COIL_Z_RADIUS / 2 + 0.02), 0.005),
        ("Y pair: R=18cm", (0, COIL_Y_RADIUS / 2 + 0.02, 0), 0.004),
        ("X pair: R=14cm", (COIL_X_RADIUS / 2 + 0.02, 0, 0), 0.004),
    ]
    for text, loc, size in labels:
        bpy.ops.object.text_add(location=loc)
        txt = bpy.context.active_object
        txt.name = f"Label_{text[:15]}"
        txt.data.body = text
        txt.data.size = size
        txt.data.align_x = 'LEFT'
        # Face camera (rotate to face -Y)
        txt.rotation_euler = (math.radians(90), 0, 0)
        mat = make_material(f"Mat_Label_{text[:10]}", (0.9, 0.9, 0.9, 1.0), roughness=0.9)
        txt.data.materials.append(mat)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    # Determine output paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    design_dir = os.path.join(project_root, "device-design")
    os.makedirs(design_dir, exist_ok=True)

    blend_path = os.path.join(design_dir, "prototype-model.blend")
    render_path = os.path.join(design_dir, "prototype-render.png")

    print(f"Building device model...")
    print(f"  .blend → {blend_path}")
    print(f"  render → {render_path}")

    # Build
    build_device()
    add_labels()
    setup_camera_and_lights()
    setup_render(render_path)

    # Save .blend
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"Saved: {blend_path}")

    # Render preview
    print("Rendering preview (Cycles, 128 samples)...")
    bpy.ops.render.render(write_still=True)
    print(f"Saved: {render_path}")

    print("Done.")


if __name__ == "__main__":
    main()
