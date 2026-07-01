# ChatGPT Web Trinity Bridge Validation - 2026-06-10

## Final Status

```text
PASS_WITH_NOTES
```

The bridge is now a tested skill route:

```text
text  -> ChatGPT page preflight passed
image -> prompt + dragged image sent; ChatGPT confirmed attachment visible
video -> prompt + dragged video sent; ChatGPT confirmed video analyzable
image result save -> ChatGPT web generated image saved to local_outputs PNG
```

## Mature Route

Use this simple route:

```text
1. Open/focus logged-in ChatGPT.
2. Paste text into the large bottom input band.
3. Drag image/video from File Explorer onto the ChatGPT page.
4. Wait until upload completes.
5. Click the visible ChatGPT send button.
6. Save state_before, prompt, attached, sent, and result screenshots.
7. Save input_manifest.json, result_manifest.json, local_outputs/result_screen.png, self_check.md.
```

Do not use the plus-button file dialog as the primary path.
Do not use Chrome remote debugging/session-control prompts.
Do not use Codex built-in image generation.

## Script

```text
H:\AI\skills\comfyui-aaki-v3-video-baseline\scripts\chatgpt_web_attachment_bridge.py
```

Important defaults:

```text
--upload-method drag
--prompt-order before
--attachment-wait 25 for images
--attachment-wait 60 for video
```

## Image Evidence

Successful image route:

```text
C:\Users\A\Desktop\1\gate_1_clean_base\bridge_validation_runs\attachment\20260610-201251_image_g02_image_drag_upload_analysis_r7_f1952f
C:\Users\A\Desktop\1\gate_1_clean_base\bridge_validation_runs\manual_send_after_wait_result.png
```

Observed ChatGPT result:

```text
TEST_ID: IMAGE_BRIDGE_DRAG_G02_R7
ATTACHMENT_VISIBLE: yes
ONE_SENTENCE_CONTENT: A black smartphone lies face up on a gray fabric surface.
```

## Video Evidence

Successful video route:

```text
C:\Users\A\Desktop\1\gate_1_clean_base\bridge_validation_runs\attachment\20260610-212533_video_g03_video_drag_upload_analysis_r2_7ff92f
C:\Users\A\Desktop\1\gate_1_clean_base\bridge_validation_runs\video_visual_button_send_result.png
```

Observed ChatGPT result:

```text
TEST_ID: VIDEO_BRIDGE_DRAG_G03_R2
ATTACHMENT_VISIBLE: yes
CAN_ANALYZE_VIDEO: yes
ONE_SENTENCE_CONTENT: A hand points at dark spots on a gray fabric mat below a keyboard with pink backlighting.
```

## Issues Found And Fixed

```text
CF_HDROP clipboard upload failed -> made clipboard route backup-only.
Attachment-after-prompt focus was unreliable -> changed to prompt first, file drag second.
Negative Chrome coordinates caused black screenshots -> clamp screenshot regions.
Uploads can outlive send-button appearance -> use conservative upload waits.
File Explorer item matching was brittle -> added first-visible-item fallback.
Send clicks can hit the wrong window -> scoped send click to ChatGPT window.
```

## Verification

```text
PASS: py_compile for attachment bridge script.
PASS: quick_validate.py reports Skill is valid.
PASS: text preflight found ChatGPT composer.
PASS: image drag upload and prompt route works.
PASS: video drag upload and prompt route works.
```

## Residual Work

The bridge can upload, send, and save result screenshots. A local result saver
has been added and tested:

```text
H:\AI\skills\comfyui-aaki-v3-video-baseline\scripts\chatgpt_web_result_saver.py
```

It saves the currently visible ChatGPT image result into `local_outputs/` by
detecting the largest image-like region in the ChatGPT window.

Verified generated-image save:

```text
C:\Users\A\Desktop\1\gate_1_clean_base\bridge_validation_runs\result_saver\20260610-221849_result_save_51a91d\local_outputs\red_circle_generated_saved.png
```

This proves the required pipeline closure:

```text
ChatGPT web image generation -> visible result -> local PNG file -> usable by downstream video pipeline
```

The next maturity gate should add original-file download:

```text
detect generated image result
open/download generated image
save to local_outputs/
verify local file opens
```
