# P2 Quality Enhance Runbook

## G01 Baseline Copy

Verify Blender portable, P1 script, P1 MP4, P1 preview frames, and the P1 skill package. Copy P1 artifacts into the P2 workspace under `baseline\`.

## G02 Quality Plan

Write `reports/p2-plan.md`. Keep the scope to a 5 second visual enhancement.

## G03 V2 Script

Create `blender/scripts/create_scene_5s_v2.py` from the P1 structure. Keep 150 frames, 30fps, 1080x1260, and P2-local output paths.

## G04 V2 Blend

Run:

```powershell
& "H:\AI\tools\Blender\blender-5.1.2-windows-x64\blender.exe" --background --python "<P2>\blender\scripts\create_scene_5s_v2.py"
```

PASS if the command exits 0 and the v2 `.blend` is larger than 80% of P1 `.blend`.

## G05 V2 MP4

Render frames with Blender and assemble MP4 with FFmpeg:

```powershell
ffmpeg -y -framerate 30 -i "<P2>\blender\renders\frames_v2\frame_%04d.png" -c:v libx264 -pix_fmt yuv420p "<P2>\blender\renders\replica_5s_v2.mp4"
```

PASS if the video is 4.8-5.3 seconds, vertical, fps >= 20, and larger than 100KB.

## G06 V1/V2 Comparison

Extract frames at 0.5s, 1.5s, 2.5s, 3.5s, and 4.5s from both P1 and P2. Generate a contact sheet with V1 on the left and V2 on the right.

## G07 Visual Score

Score the 8 required categories out of 5. PASS requires at least 26/40 and nonzero scores for red orb layering, magic circle, dark value structure, and overall reference mood.

## G08 Automatic Verification

Run `scripts/verify-p2-quality-enhance.py` and require `G08_PASS_P2_VERIFY_SCRIPT_PASS`.

## G09 Skill Extension

Save this extension under `v2-quality-enhance\` without rewriting the P1 baseline.

## G10 Final Report

Write `reports/final-report.md` and `reports/final-acceptance.json` after verification and skill extension checks pass.
