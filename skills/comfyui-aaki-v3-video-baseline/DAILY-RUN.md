# Daily Run

Use this for normal daily operation of the existing 秋葉aaaki ComfyUI-aki-v3 Wan2.2-TI2V-5B baseline.

## Boundaries

- Do not install new models.
- Do not upgrade ComfyUI core or custom nodes during daily production.
- Do not switch to Wan2.2 14B, S2V, Fun InP, LTX, or FramePack.
- Do not modify Hermes, New API, 小龙虾, Open WebUI, or Remotion.
- Do not delete previous outputs, workflows, or models.

## Start ComfyUI

Preferred direct start:

```powershell
C:\AI\ComfyUI_Aaki_v3\START_COMFYUI_C_DRIVE_OUTPUT_D.bat
```

Open the UI in Google Chrome:

```powershell
Start-Process -FilePath 'C:\Program Files\Google\Chrome\Application\chrome.exe' -ArgumentList @('--new-window','http://127.0.0.1:8188')
```

## Health Check

Run the no-generation smoke check:

```powershell
${REDACTED_SECRET}
```

Expected:

- HTTP root returns `200`
- `/system_stats` returns `200`
- three Wan2.2 5B model files exist
- pinned workflow and API prompt exist
- output directories exist

## Daily Clip Flow

1. Put key images in `D:\AI_ComfyUI_Outputs\ComfyUI_Aaki_v3\input`.
${REDACTED_SECRET}
3. Keep the three model nodes unchanged.
4. Change only prompt, seed, input image, and filename prefix for the shot.
5. Generate one shot at a time.
6. Raw output appears in `D:\AI_ComfyUI_Outputs\ComfyUI_Aaki_v3\output\video`.
7. Copy keepers to `D:\AI_ComfyUI_Outputs\ComfyUI_Aaki_v3\output\video_selected`.
8. Copy final clips for Remotion to `D:\AI_ComfyUI_Outputs\ComfyUI_Aaki_v3\output\remotion_inbox`.

## Mobile PPT Image Showcase

For simple phone-format image slideshow videos, use the accepted static PPT
showcase baseline instead of Wan2.2 generation when the user wants stable image
display without motion. For WeChat/mobile preview, prefer the full-screen 9:16
crop version over the older centered-card layout.

Reference:

```text
${REDACTED_SECRET}
```

Accepted style:

- 1080x1920 vertical video
- one source image per slide
- static image, no zoom, no pan, no shake
- cross-fade only
- soft light music
- full-screen 9:16 image crop
- no white border
- no progress dots
- avoid small landscape cards with large blurred empty areas

## Naming

Use stable names before Remotion:

```text
scene##_shot##_take##_wan22_5b_512x512_12fps.mp4
```

Example:

```text
scene01_shot03_take01_wan22_5b_512x512_12fps.mp4
```

## Known-Good Baseline

- Workflow: `workflows\wan22_5b_lowrisk_ui_workflow.json`
- API prompt: `prompts\wan22_5b_lowrisk_api_prompt.json`
- Resolution: `512x512`
- Frames: `37`
- FPS: `12`
- Duration: `3.083333` seconds
- Steps: `12`
- Peak observed VRAM: `16946 MiB`
- First successful output: historical H-drive run, now superseded by the C-drive root and D-drive output layout.
