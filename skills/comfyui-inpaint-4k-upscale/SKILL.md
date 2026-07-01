---
name: comfyui-inpaint-4k-upscale
description: Use when Codex needs to run or maintain the local ComfyUI workflow for portrait/person image local inpainting, Ultimate SD Upscale 2x/4K upscaling, and Topaz-style final enhancement on this Windows machine. Covers the installed ComfyUI path, Manager and Ultimate SD Upscale verification, recommended workflow order, parameters, failure recovery, and acceptance checks.
---

# ComfyUI Inpaint 4K Upscale

## Quick Start

Use this skill for local AI portrait image repair/upscale tasks on this machine. The locked mature route is:

1. Open the local ComfyUI environment.
2. Import the user's original image.
3. Inpaint only the masked repair area.
4. Preserve face, body silhouette, clothing identity, and key subject details.
5. Run Ultimate SD Upscale for 2x tile diffusion upscale toward 4K.
6. Use Topaz Photo AI/Gigapixel as a final manual enhancement step when available.

Installed environment:

- ComfyUI: `C:\Users\A\Desktop\1\output\TASK-COMFYUI-UPSCALE-SKILL-REPLAY-20260521\ComfyUI`
- Python venv: `C:\Users\A\Desktop\1\output\TASK-COMFYUI-UPSCALE-SKILL-REPLAY-20260521\.venv-comfyui`
- Default URL: `http://127.0.0.1:8188`
- Startup command: `python main.py --listen 127.0.0.1 --port 8188 --disable-auto-launch --enable-manager`

## Before Running

Run the verification script before claiming the environment is ready:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\A\.codex\skills\comfyui-inpaint-4k-upscale\scripts\verify-comfyui.ps1"
```

If ComfyUI is not running, start it:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\A\.codex\skills\comfyui-inpaint-4k-upscale\scripts\start-comfyui.ps1"
```

## Operating Workflow

Load these references as needed:

- `references/operator-guide.md`: short user-image handling guide.
- `references/workflow.md`: recommended inpaint -> Ultimate SD Upscale -> Topaz workflow.
- `references/parameters.md`: stable parameter ranges.
- `references/install.md`: install and update commands.
- `references/troubleshooting.md`: failure points and recovery.
- `references/acceptance.md`: PASS/FAIL checks.
- `references/report.md`: original installation report and evidence.

## Constraints

- Do not switch the main route to A1111, Magnific, or a cloud paid platform.
- Do not install random model packs or opaque third-party bundles as the primary source.
- Treat Chinese bundled-package tutorials as experience references only.
- Do not run destructive cleanup against model directories or custom node folders unless the user explicitly asks.
- If Topaz is unavailable because of license/download limits, keep it as a manual final enhancement step.
- Do not claim image processing is ready for a real user image unless required base models/checkpoints are present or the user supplies them.

## Verification Standard

A ready environment must show:

- `GET /system_stats` returns 200.
- `GET /v2/manager/version` returns Manager version.
- `GET /object_info` includes `UltimateSDUpscale`.
- Startup logs contain no custom-node import failure for Ultimate SD Upscale.

Use `references/acceptance.md` for exact commands and evidence format.
