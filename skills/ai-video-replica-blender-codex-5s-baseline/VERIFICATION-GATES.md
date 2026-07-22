# Verification Gates

## Required Artifacts

- `config/blender-path.json`
- `reports/environment-check.md`
- `reports/blender-install-log.md` when Blender had to be prepared
- `reports/scene-design.md`
- `blender/scripts/create_scene_5s.py`
- `blender/project/replica_5s.blend`
- `blender/renders/frames/frame_0001.png` through `frame_0150.png`
- `blender/renders/replica_5s.mp4`
- `reports/blend-generation-log.md`
- `reports/render-log.md`
- `scripts/verify-5s-replica.py`
- `reports/verification-result.md`
- `reports/visual-check.md`
- `reports/final-report.md`

## Automatic Checks

- Blender executable exists and `--version` exits 0.
- `.blend` exists and is larger than 50KB.
- MP4 exists and is larger than 100KB.
- ffprobe reads duration, resolution, and fps.
- Duration is 4.8 to 5.3 seconds.
- Width is less than height.
- FPS is at least 20.

## Manual Visual Checks

- Red glowing ball.
- Magic circle.
- Dark tabletop.
- Candles or warm light.
- Debris or particles.
- Black central body.
- Camera motion.
- Red pulse.
- Vertical composition.

## Final PASS

Only report `AI_VIDEO_REPLICA_BLENDER_CODEX_5S_VERIFY_PASS` when automatic verification, visual check, and skill package persistence all pass.
