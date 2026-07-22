# C Drive Image 8K And PPT Video Test - 2026-07-04

Use this note when a still image should be upscaled or turned into a simple
phone-format PPT-style test video with the C-drive Aaki v3 baseline.

## Scope

- Primary root: `C:\AI\ComfyUI_Aaki_v3`
- Input/output root: `D:\AI_ComfyUI_Outputs\ComfyUI_Aaki_v3`
- Knowledge/skill search starts from C drive hot paths, not K drive backups.
- This route is for conservative still-image enlargement and PPT-style video
  verification. It is not a generative image repair route.

## Image 8K Smoke Route

1. Run `scripts\smoke-check.ps1`.
2. Start `C:\AI\ComfyUI_Aaki_v3\START_COMFYUI_C_DRIVE_OUTPUT_D.bat` if HTTP is not ready.
3. Copy the source image into:
   `D:\AI_ComfyUI_Outputs\ComfyUI_Aaki_v3\input`
4. Submit a conservative ComfyUI graph:

```text
LoadImage
-> optional ImageCrop
-> ImageScale(lanczos, long edge 8192)
-> ImageSharpen(radius=1, sigma=0.8, alpha=0.35)
-> SaveImage
```

5. Validate output dimensions and visually compare against the source.

Use this route when preserving identity, pose, and scene is more important than
AI redraw. If true detail hallucination or object/UI removal is required, use
the formal ChatGPT Web image repair branch instead.

## PPT Video Recovery Test

Use the accepted mobile PPT showcase rules:

- 1080x1920 vertical.
- 30 fps.
- one image per slide.
- full-screen 9:16 center crop.
- static images only; no zoom, pan, or shake.
- cross-fade only.
- H.264 video + AAC audio.
- soft light music with fade in/out.

Minimal proof output should include:

```text
final mp4
ffprobe.json
preview_01.jpg
preview_02_transition.jpg
preview_03.jpg
video-preview-contact-sheet.jpg
source_manifest.txt
test-report.md
```

## 2026-07-04 Verified Result

${REDACTED_SECRET}
${REDACTED_SECRET}
- Specs: 1080x1920, 30 fps, H.264, AAC audio, 7.05s.
- Status: `AAKI_IMAGE_PPT_VIDEO_TEST_PASS`

