# Blender Scripting SOP

## Path Rules

- Derive the workspace from `Path(__file__).resolve()`.
- Keep `.blend`, frames, reports, and MP4 under the workspace.
- Guard output paths so scripts do not write outside the workspace.
- Use `config/blender-path.json` for command execution.

## Scene Rules

- Start with `bpy.ops.object.select_all(action="SELECT")` and delete the default scene.
- Set frame range, fps, vertical resolution, render engine, output format, and frame path before creating assets.
- Use generated meshes and curves for the first pass.
- Prefer emission materials for magic circles and energy objects.
- Use point lights for orb and candles, and one soft fill light.

## Animation Rules

- Keyframe only the minimum: orb location/scale, magic circle rotation, debris rotation, camera location, and light or emission intensity.
- Keep frame range explicit: 1-150 at 30fps for 5 seconds.
- Use a camera target and Track To constraint for stable composition.

## Repeatability Rules

- Clean old frame outputs inside the workspace before rendering.
- Save the `.blend` to a deterministic path.
- Fail loudly on missing paths; do not create reports that imply success after a Blender error.

## Quality Upgrade Path

- Add textured table and laptop materials.
- Replace simple candles with modeled wick/flame shapes.
- Add volumetric haze only after the baseline render is stable.
- Add more complex debris motion only after verification remains fast.
