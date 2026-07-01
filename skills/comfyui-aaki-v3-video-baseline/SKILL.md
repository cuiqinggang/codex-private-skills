---
name: comfyui-aaki-v3-video-baseline
description: Use when installing, verifying, preserving, or extending the local 秋葉aaaki ComfyUI-aki-v3 video-generation baseline on Windows, especially Wan2.2-TI2V-5B first-run tests. Enforces official-source-only downloads, no v2/V9.5/Desktop fallback, no multi-model expansion, and gated PowerShell execution.
metadata:
  short-description: 秋葉aaaki ComfyUI-aki-v3 video baseline gates
---

# ComfyUI-aki-v3 Video Baseline

Use this skill for the user's fixed local ComfyUI video engine:

`GPT script/storyboard/key image -> 秋葉aaaki ComfyUI-aki-v3 -> Wan2.2-TI2V-5B short clips -> Remotion composition`

## ChatGPT Web Image Repair Branch

ChatGPT web image generation/editing is the preferred image repair route for
this video baseline. It is not an optional afterthought. Use it whenever the
video result is failing because one or more source images, keyframes, inpainted
frames, texture patches, clean plates, or visual reference frames are not good
enough.

For the reusable browser bridge design, read:

```text
references/chatgpt-web-trinity-bridge.md
```

It defines the three formal ChatGPT web branches for this video workflow:

```text
text  -> existing screenshot bridge prompt/send/copy route
image -> official ChatGPT web image generation/editing, max 10 images per batch
video -> controlled upload/analysis/generation test route, not production until accepted
```

Preference order:

```text
1. ChatGPT web official image tool through screenshot/computer-use route
2. Local ComfyUI/other mature image workflow only when the user explicitly asks
3. Codex built-in image tool is forbidden
```

For production video repair and production video source images, use the
ChatGPT web official image tool. Do not use Codex Desktop's built-in image tool
as a formal video source, clean plate, keyframe, texture reference, or final
visual repair image.

Absolute ban:

```text
Do not call Codex built-in image generation for this video-making workflow.
Do not use it for preview.
Do not use it as fallback.
Do not use it for drafts.
Do not use it for temporary candidate frames.
Do not promote any prior built-in generated image into this workflow.
```

Formal rule:

```text
Any image created, repaired, or selected for this video-making pipeline must be
created or repaired through ChatGPT web official image generation/editing, then
saved into the project evidence folder with screenshots proving the web route.
```

Foundation rule:

```text
High-quality source images are the foundation of the video. If a ChatGPT web
image passes still-image review, treat it as the trusted base asset for the next
video build. Do not downgrade, discard, or blame the good image because an old
transfer, backfeed, or assembly attempt failed. Rebuild the video from the good
image foundation with better keyframes, masks, alignment, interpolation, or a
fresh video construction method.
```

Old low-quality or Codex built-in images are not meaningful baselines once a
better ChatGPT web image exists. They may be kept only as negative comparison
evidence, not as production sources.

Required rule:

```text
video visual fail -> find failing keyframes -> repair still images with
ChatGPT web image editing -> verify repaired stills -> use the repaired stills
as keyframe replacement / clean plates / texture references -> rebuild the
video segment -> create contact sheet and review the whole video again
```

Use this branch especially for:

- object/plant/person removal that leaves visible patches or silhouettes
- unnatural desk, wall, skin, fabric, product, or background texture
- key image composition defects before Wan2.2 generation
- frame-level artifacts that make an otherwise usable video fail review
- clean-base, mask, layer, or reference-frame repair before final video assembly

Do not mark a video blocked merely because OpenCV, a mask pass, or one Wan2.2
take failed, if the defect is still-image-repairable. First try ChatGPT web
image repair on representative failing frames or key images, then use the
repaired images as controlled inputs for the next video attempt.

The repaired image must not be accepted alone. It must be returned to the video
pipeline and checked as video evidence: playable clip, contact sheet, original
vs repaired comparison, self-check notes, and explicit PASS/FAIL status.

Use the logged-in ChatGPT web image tool through the screenshot/computer-use
route when the user has provided the exact file and intent. The route is:

```text
open logged-in ChatGPT web -> upload/paste exact failed frame -> send image edit
request -> wait for generated image -> save/crop/download the returned image ->
use it as a high-quality keyframe / clean plate / replacement source ->
rerender video evidence
```

If a web-generated frame is visually much better than the old damaged frame,
treat it as the better source and the foundation for the rebuilt video. Do not
call the good frame bad merely because a naive video transfer creates new
artifacts. Instead, rebuild the video method around the good image: generate
more keyframes, replace the bad frames directly, tighten masks, align the frame,
interpolate between multiple web-repaired frames, or restart the video segment
with the high-quality image as the base.

Hard boundary for ChatGPT web image repair: the returned good still must be
protected. If video assembly creates new dark spots, phone/hand corruption, or
flicker, the assembly/rebuild method failed; the correct next step is more
ChatGPT web keyframes or better replacement/interpolation/reconstruction, not
downgrading to the old broken frame or returning to any built-in image route.

Required operating method for web image generation/editing:

1. Put the exact failed frame, key image, or reference image in the task folder.
2. Focus the logged-in ChatGPT web page in the browser.
3. Paste or upload the exact image into ChatGPT web.
4. Paste an explicit edit/generation prompt with remove/preserve constraints.
5. Send only after a screenshot confirms the image thumbnail is attached.
6. Wait for the web-generated image.
7. Download, crop, or screenshot-save the returned image into the project folder.
8. Save evidence screenshots for upload, send, generated result, and local file.
9. Use the returned image as the production keyframe/clean plate/source frame.
10. Rebuild the video and verify with contact sheet and video self-check.

Batch rule:

```text
Default maximum batch size: 10 images per ChatGPT web image task.
```

Use at most 10 failed frames/key images in one web-image batch, then split the
rest into numbered batches such as `batch_01`, `batch_02`, and `batch_03`.
This matches the known practical ChatGPT web file batch boundary. If the web UI
shows a lower current limit, obey the web UI and split smaller. Do not exceed
10 images in one formal web-image generation/editing request.

## ChatGPT Web Trinity Bridge (verified 2026-06-10)

Use the trinity bridge reference when the task needs a reusable ChatGPT web
transport for text, image, or video work:

```text
H:\AI\skills\comfyui-aaki-v3-video-baseline\references\chatgpt-web-trinity-bridge.md
```

Verified bridge status:

| Branch | Status | Method |
|--------|--------|--------|
| Text | ✅ Production | `chatgpt-screenshot-bridge` automated (19s avg) |
| Image | ⚠️ Semi-auto | Text via bridge + manual drag-drop + visual gates |
| Video | 🔄 Redesigned | `ffmpeg extract → image bridge → reconstruct` pipeline |

Required outputs for any formal bridge run:

```text
input_manifest.json
prompt.md
state_before.png
state_attached.png
state_sent.png
state_result.png
result_manifest.json
self_check.md
local_outputs/
```

Platform notes:
- Cloudflare blocks CDP; always use screenshot route (pyautogui + mss + vision)
- ChatGPT window title changes after each conversation; use flexible title patterns
- pyautogui file upload is unreliable; image upload must be manual drag-drop
- ChatGPT Web does NOT support video upload; use ffmpeg frame extraction

## Hard Boundaries

- Use the existing install at `H:\AI\ComfyUI_Aaki_v3` unless the user explicitly changes it.
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
- Run `scripts/smoke-check.ps1` for a no-generation baseline check.
- Use the pinned workflow in `workflows/` and the pinned API prompt in `prompts/` as the known-good Wan2.2-TI2V-5B baseline.

## Output Layout

- Raw ComfyUI video outputs: `H:\AI\ComfyUI_Aaki_v3\ComfyUI\output\video`
- Human-selected keepers: `H:\AI\ComfyUI_Aaki_v3\ComfyUI\output\video_selected`
- Clips ready for Remotion import: `H:\AI\ComfyUI_Aaki_v3\ComfyUI\output\remotion_inbox`

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

- Install root: `H:\AI\ComfyUI_Aaki_v3`
- URL: `http://127.0.0.1:8188/`
- Launcher: `H:\AI\ComfyUI_Aaki_v3\绘世启动器.exe`
- Direct start command:

```powershell
H:\AI\ComfyUI_Aaki_v3\python\python.exe -s ComfyUI\main.py --windows-standalone-build --port 8188
```

- Verified GPU: RTX 2080 Ti 22GB, compute capability 7.5
- Verified torch: `2.9.1+cu130`
- Verified ComfyUI: `0.9.2`
