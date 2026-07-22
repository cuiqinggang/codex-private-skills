---
name: comfyui-aaki-v3-video-baseline
description: Use when the user asks to make, restore, verify, or troubleshoot AI video/PPT video/image production with the local ComfyUI-aki-v3/Aaki/秋叶 aaaki workflow on Windows. Trigger on Chinese or English requests mentioning ComfyUI, Aaki, 秋叶, 制作视频, PPT视频, 图片制作, 修图, Wan2.2, Flux Kontext, ControlNet, or restoring the mature video skill pack. Always use the C-drive production root C:\AI\ComfyUI_Aaki_v3, D-drive input/output folders, smoke-check before production, official-source-only downloads, and no v2/V9.5/Desktop fallback.
---

# ComfyUI-aki-v3 Video Baseline

Use this skill for the user's fixed local ComfyUI video engine:

`GPT script/storyboard/key image -> 秋葉aaaki ComfyUI-aki-v3 -> Wan2.2-TI2V-5B short clips -> Remotion composition`

Current production layout:

- Engine: `C:\AI\ComfyUI_Aaki_v3`
- Launcher: `C:\AI\ComfyUI_Aaki_v3\START_COMFYUI_C_DRIVE_OUTPUT_D.bat`
- Input: `D:\AI_ComfyUI_Outputs\ComfyUI_Aaki_v3\input`
- Output: `D:\AI_ComfyUI_Outputs\ComfyUI_Aaki_v3\output`
- Temp: `D:\AI_ComfyUI_Outputs\ComfyUI_Aaki_v3\temp`
${REDACTED_SECRET}

At the start of any real production task, run `scripts/smoke-check.ps1`.
If it fails, read `RECOVERY.md` before changing models, nodes, or paths.

## ChatGPT web repair branches

Read [chatgpt-web-repair-branches.md](references/chatgpt-web-repair-branches.md) only for ChatGPT web image repair or Trinity bridge work.

## Hard Boundaries

- Use the existing install at `C:\AI\ComfyUI_Aaki_v3` unless the user explicitly changes it. H is history-only and K is backup/restore-only; never use either as a runtime fallback.
- Do not use `ComfyUI-aki-v2.7z`, V9.5, third-party repacks, fan packs, Quark parsers, or ComfyUI Desktop.
- Do not install multiple video models.
- Do not install Wan2.2 14B, S2V, Fun InP, LTX-2.3, FramePack, or model bundles.
- Do not modify Hermes, New API, 小龙虾, Open WebUI, or Remotion.
- Do not delete old ComfyUI installs, models, workflows, or outputs.

## Required Gate Order

1. Read `references/phase1-install-gates.md` before reinstalling or repairing the base.
2. Run `scripts/freeze-baseline.ps1` before model installation or workflow changes.
3. Read `references/wan22-5b-test-gates.md` before any Wan2.2-TI2V-5B test.
4. Verify official/allowed model sources before download.
5. Download or place only these files:
   - `ComfyUI\models\diffusion_models\wan2.2_ti2v_5B_fp16.safetensors`
   - `ComfyUI\models\text_encoders\umt5_xxl_fp8_e4m3fn_scaled.safetensors`
   - `ComfyUI\models\vae\wan2.2_vae.safetensors`
6. Use the official ComfyUI Wan2.2 5B workflow/template when available.
7. Run one low-risk test first: 512-ish resolution, 36-48 frames, 12-16 fps, low/offload options.
8. Save report, workflow JSON, output video, model paths, timing, and VRAM observation.

## Visual Repair Gate

Before accepting or blocking a shot/video, run this gate:

1. Generate contact sheets or keyframes for the failed clip.
2. Identify the exact frames or image regions causing failure.
3. If the problem is image-quality based, call the ChatGPT web official image
   tool through the screenshot/computer-use route.
4. Save GPT repaired images beside the shot evidence, with prompt and source
   frame notes.
5. Use the repaired image as a new key image, texture reference, clean plate,
   mask target, or Remotion/ComfyUI input.
6. Re-render or repair the video segment.
7. Re-check the rendered video, not only the repaired still image.

Allowed status after this gate:

```text
VISUAL_REPAIR_SELF_PASS_READY_FOR_VIDEO_REVIEW
VISUAL_REPAIR_INTERNAL_FAIL_CONTINUE
VISUAL_REPAIR_BLOCKED_AFTER_IMAGE_AND_VIDEO_ATTEMPTS
```

## Daily Stabilized Use

- Read `DAILY-RUN.md` for normal launch and health checks.
- Read `WAN22-5B-SHOT-SOP.md` before producing daily video clips.
- Read `RECOVERY.md` when the service, model visibility, queue, or output path is wrong.
- For phone-format static PPT-style image showcase videos, read
  `references/mobile-ppt-showcase-baseline-20260612.md`.
- For C-drive still-image 8K conservative upscale and a small PPT-video
  recovery test, read
  `references/c-drive-image-8k-and-ppt-video-test-20260704.md`.
- Run `scripts/smoke-check.ps1` for a no-generation baseline check.
- Use the pinned workflow in `workflows/` and the pinned API prompt in `prompts/` as the known-good Wan2.2-TI2V-5B baseline.

## Output Layout

- Raw ComfyUI video outputs: `D:\AI_ComfyUI_Outputs\ComfyUI_Aaki_v3\output\video`
- Human-selected keepers: `D:\AI_ComfyUI_Outputs\ComfyUI_Aaki_v3\output\video_selected`
- Clips ready for Remotion import: `D:\AI_ComfyUI_Outputs\ComfyUI_Aaki_v3\output\remotion_inbox`

## Stop Conditions

Stop and report instead of branching if:

- an official source cannot be confirmed
- a required model file is missing or download-restricted
- CUDA/torch cannot see RTX 2080 Ti
- workflow nodes are missing and the minimal missing dependency is unclear
- the first test OOMs and one lower-resolution retry also fails
- fixing the problem would require broad upgrades or installing unrelated nodes/models

## Known Baseline

First-stage verified install:

- Install root: `C:\AI\ComfyUI_Aaki_v3`
- URL: `http://127.0.0.1:8188/`
- Current launcher: `C:\AI\ComfyUI_Aaki_v3\START_COMFYUI_C_DRIVE_OUTPUT_D.bat`
- Do not launch legacy H/K copies. If the C-drive launcher is missing, stop with `BLOCKED_C_SOURCE_MISSING`.
- Direct start command:

```powershell
C:\AI\ComfyUI_Aaki_v3\python\python.exe -s ComfyUI\main.py --windows-standalone-build --port 8188 --output-directory D:\AI_ComfyUI_Outputs\ComfyUI_Aaki_v3\output --input-directory D:\AI_ComfyUI_Outputs\ComfyUI_Aaki_v3\input --temp-directory D:\AI_ComfyUI_Outputs\ComfyUI_Aaki_v3\temp
```

- Verified GPU: RTX 2080 Ti 22GB, compute capability 7.5
- Verified torch: `2.9.1+cu130`
- Verified ComfyUI: `0.9.2`

