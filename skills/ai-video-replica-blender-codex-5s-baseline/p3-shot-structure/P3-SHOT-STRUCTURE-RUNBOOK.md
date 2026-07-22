# P3 Shot Structure Runbook

## Inputs

- Blender portable path.
- P1 baseline workspace.
- P2 quality-enhanced workspace.
- Existing skill package.

## Steps

1. Verify Blender, P1, P2, and skill package paths.
2. Copy P2 script, P2 video, and P2 comparison artifacts into a new P3 workspace.
3. Write a 15 second shot-structure plan with establish, intensify, and climax phases.
4. Create `create_scene_15s_p3.py`.
5. Generate `replica_15s_p3.blend` in Blender background mode.
6. Render 450 PNG frames at 30fps.
7. Assemble `replica_15s_p3.mp4` with FFmpeg.
8. Extract stage preview frames at representative times.
9. Write visual shot-structure check.
10. Run `verify-p3-shot-structure.py`.
11. Save this P3 extension under the existing skill package.

## PASS Criteria

- MP4 duration is 14.8-15.3 seconds.
- Video is vertical.
- FPS is at least 20.
- 450 frames exist.
- Stage previews cover establish, intensify, and climax.
- Visual score is at least 26/40.
- Verification script returns `G08_PASS_P3_VERIFY_SCRIPT_PASS`.
