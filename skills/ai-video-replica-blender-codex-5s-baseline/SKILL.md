---
name: ai-video-replica-blender-codex-5s-baseline
description: Use when creating a minimum 5 second Blender + Codex video replica baseline from a reference clip, including Blender Python scene generation, frame rendering, FFmpeg MP4 assembly, verification reports, and skill-package capture. Not for ComfyUI/Wan workflows, AI video model installation, or full cinematic/pixel-level recreation.
---

# AI Video Replica Blender Codex 5s Baseline

Use this skill to run a small, verifiable Blender replica loop:

1. Check or prepare official Blender.
2. Lock the Blender executable path in `config/blender-path.json`.
3. Write a focused 5 second scene design.
4. Generate a repeatable Blender Python script.
5. Build the `.blend` in background mode.
6. Render PNG frames and assemble MP4 with FFmpeg.
7. Verify duration, vertical format, fps, file sizes, and required reports.
8. Extract preview frames and perform a minimum visual check.

## Applies To

- 5 second Blender proof-of-process replicas.
- Reference clips whose essence can be represented with generated geometry, lights, materials, camera motion, and keyframes.
- Workflows where Codex writes or modifies Blender Python and Blender performs deterministic rendering.

## Does Not Apply To

- Full 20-30 second production replicas.
- Pixel-level or asset-perfect reconstruction.
- ComfyUI, Wan, or other AI video generation pipelines.
- Installing large AI video models.
- API-key, Open WebUI, Hermes, Xiaolongxia, or New API operations.

## Blender + Codex Split

- Codex owns planning, script generation, path safety, logs, verification scripts, and reports.
- Blender owns scene construction from Python, `.blend` generation, frame rendering, and animation evaluation.
- FFmpeg/ffprobe own MP4 assembly and media-parameter verification.

## Minimum Gates

- G01/G01B: Blender is found or prepared from official sources and `blender.exe --version` exits 0.
- G01C: `config/blender-path.json` records a real executable path.
- G02: `scene-design.md` names the 5 second scope and all core visual elements.
- G03/G04: `create_scene_5s.py` runs and writes a `.blend` larger than 50KB.
- G05: MP4 exists, is larger than 100KB, lasts about 5 seconds, is vertical, and has fps >= 20.
- G06: verification script passes.
- G07: preview frames confirm the minimum visual read.

## Common Failures

- Blender not in PATH: use absolute path from `config/blender-path.json`.
- Installer requires administrator interaction: use the official portable zip under a tool directory.
- MP4 missing but frames exist: rerun FFmpeg with the `frame_%04d.png` pattern.
- Render too slow: reduce resolution to 540x630 and document the fallback.
- Scene looks blank: check camera target, light energy, material emission, and output frame paths.
