# AI Video Replica Blender Codex 5s Baseline

This skill package captures the first successful Blender + Codex 5 second replica loop.

It is not a one-click AI video generator. The baseline is: Codex creates a Blender Python scene, Blender builds and renders it, FFmpeg assembles a playable MP4, and a verification script proves the output is valid.

## Reuse

1. Create a new isolated workspace.
2. Run G01-G01C to find or prepare official Blender.
3. Write a 5 second scene design from the reference clip.
4. Adapt `templates/create_scene_5s.template.py`.
5. Render frames, assemble MP4, run verification, and extract preview frames.

## Extending Beyond 5 Seconds

For a 20 second version, keep the first pass simple:

- Increase `frame_end` to 600 at 30fps.
- Add 3-4 camera beats instead of one continuous push.
- Add secondary animation passes for particles, glow intensity, and object movement.
- Keep the same verification gates before adding ComfyUI/Wan style transfer or interpolation.
