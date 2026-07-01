# Runbook

## G01 Environment Check

Run `where.exe blender`, `blender --version`, `where.exe ffmpeg`, `ffmpeg -version`, `where.exe ffprobe`, and `ffprobe -version`. Also scan `C:\Program Files\Blender Foundation` for `blender.exe`.

PASS if Blender runs. If not found, continue to G01B.

## G01B Blender Install Or Preparation

Use official Blender sources only. Prefer the Windows Installer when non-interactive administrator execution is available. Otherwise use the official Windows portable zip and extract it to a tool directory such as `H:\AI\tools\Blender`.

Record source URL, install/extract path, `blender.exe` path, SHA256 status when available, version output, and PATH status.

## G01C Blender Path Config

Write `config/blender-path.json` with `blender_exe`, `source`, and `version_checked`. Later commands must read this path instead of depending on PATH.

## G02 Scene Design

Write the 5 second design: resolution, fps, frame count, elements, animations, performance boundary, and success criteria.

## G03 Blender Python Script

Create `blender/scripts/create_scene_5s.py`. The script must clear the scene, set render parameters, create the scene, add keyframes, set frame output paths, and save the `.blend`.

## G04 Blend Generation

Run:

```powershell
$config = Get-Content .\config\blender-path.json -Raw | ConvertFrom-Json
& $config.blender_exe --background --python .\blender\scripts\create_scene_5s.py
```

PASS if exit code is 0 and `.blend` exists and is larger than 50KB.

## G05 MP4 Render

Render frames:

```powershell
& $config.blender_exe --background .\blender\project\replica_5s.blend --render-anim
```

Assemble MP4:

```powershell
ffmpeg -y -framerate 30 -i .\blender\renders\frames\frame_%04d.png -c:v libx264 -pix_fmt yuv420p .\blender\renders\replica_5s.mp4
```

PASS if MP4 is larger than 100KB, about 5 seconds, vertical, and fps >= 20.

## G06 Automatic Verification

Run `scripts/verify-5s-replica.py`. It must write `reports/verification-result.md` and `.json`.

## G07 Visual Check

Extract preview frames with FFmpeg at 1fps. Confirm red orb, magic circle, tabletop, candles/warm light, debris, black center body, camera motion, red pulse, and vertical framing.

## G08 Skill Package

Save the workflow, SOP, gates, templates, and first run report into a new skill package. Do not modify old skill packages.

## G09 Final Acceptance

Create `reports/final-report.md` only after automated verification passes. Final PASS requires Blender ready, `.blend`, MP4, visual check, verification script PASS, and skill package saved.
