# ChatGPT Web Trinity Bridge

This reference defines the reusable ChatGPT web bridge for the local video
workflow.

It has three branches:

```text
text  -> send prompt, copy answer
image -> upload/paste images, request generation or repair, save returned files
video -> upload video, request analysis or generation test, save answer/results
```

## Architecture (updated 2026-06-11)

Production default:

```text
Use the screenshot-gated human route for ChatGPT Web image work.
```

The older automated drag/window-detection scripts are no longer the default
production route. Keep them only as backup or diagnostic tools when there is a
specific reason to test automation internals. They must not replace the
one-action-one-screenshot route for production image repair.

Deprecated automated route (backup only):

```text
1. Paste the text prompt into the large bottom ChatGPT input band.
2. Drag the image or video from File Explorer onto the ChatGPT page.
3. Let ChatGPT automatically attach the file to the composer.
4. Wait for upload to complete before sending.
5. Click the visible ChatGPT send button inside the ChatGPT window.
6. Save screenshots, manifests, local result screenshot, and self_check.md.
7. If ChatGPT returns a generated/repaired image, save it into `local_outputs/`
   with `scripts/chatgpt_web_result_saver.py` before the video pipeline uses it.
```

Do not use this route first for production. The simplest and most reliable
method is the screenshot-gated human route below. Do not use the plus-button
file dialog, Chrome remote debugging, CDP, browser extensions, broad
session-control prompts, hidden window guessing, or Explorer fallback selection
as the primary route.

Send safety:

```text
Only click a verified send-arrow button.
Never click microphone, sound-wave, voice, start-speaking, stop, or end controls.
If the composer shows a voice/sound-wave button instead of a send arrow, do not click it.
Refocus the text input, paste text, and wait until the send arrow is visible.
```

Verified script:

```text
H:\AI\skills\comfyui-aaki-v3-video-baseline\scripts\chatgpt_web_attachment_bridge.py
H:\AI\skills\comfyui-aaki-v3-video-baseline\scripts\chatgpt_web_result_saver.py
H:\AI\skills\comfyui-aaki-v3-video-baseline\scripts\chatgpt_web_batch_manifest.py
H:\AI\skills\comfyui-aaki-v3-video-baseline\scripts\chatgpt_web_batch_runner.py
```

Verified command shape:

```powershell
python H:\AI\skills\comfyui-aaki-v3-video-baseline\scripts\chatgpt_web_attachment_bridge.py `
  --branch image `
  --upload-method drag `
  --prompt-order before `
  --file <image-or-video> `
  --prompt-file <prompt.md>
```

For video, use a longer upload wait:

```powershell
--attachment-wait 60
```

Save the visible generated/repaired image result. Prefer saving from the
attachment run's `state_result.png` screenshot because it is already tied to the
source item and avoids multi-window live screenshot drift:

```powershell
python H:\AI\skills\comfyui-aaki-v3-video-baseline\scripts\chatgpt_web_result_saver.py `
  --run-root <run-folder> `
  --output-name saved_result.png `
  --screenshot-file <attachment-run>\state_result.png
```

Verified generated-image save evidence:

```text
C:\Users\A\Desktop\1\gate_1_clean_base\bridge_validation_runs\result_saver\20260610-221849_result_save_51a91d\local_outputs\red_circle_generated_saved.png
```

The trinity bridge uses a **split architecture** across two agents:

| Channel | Agent | Why |
|---------|-------|-----|
| Text | **Hermes** | `chatgpt-screenshot-bridge` (pyautogui+mss) sufficient, 19s automated |
| Image | **Codex Desktop** | Computer Use + Chrome extension can drag/click/scroll natively |
| Video | **Codex Desktop** | Frame extraction → image bridge pipeline via Chrome extension |

> **Key finding (2026-06-10):** Hermes' pyautogui cannot reliably interact with
> ChatGPT Web's file upload dialog. Four methods tested — all failed.
> Codex Desktop's Computer Use + Chrome extension has native `drag` capability
> and is the only verified path for image upload to ChatGPT Web.

## Hard Boundary

For this video workflow, do not call Codex built-in image generation. Do not use
it for preview, fallback, draft, candidate frame, clean plate, keyframe, source
frame, or final repair.

Formal image generation and repair must use ChatGPT web official image tools
through a visible browser route with saved evidence.

## Foundation Rule

The image is the foundation of the video. When a ChatGPT web generated or
repaired image passes still-image review, it becomes the trusted base asset for
the next video build.

If a video attempt using that good image fails, classify the failure as video
construction, masking, alignment, interpolation, or assembly failure first. Do
not treat the high-quality image as failed merely because an old transfer or
rough reconstruction path failed. Rebuild the video from the good image base.

Low-quality built-in images and old damaged frames are not production
alternatives once the ChatGPT web image is better. Keep them only as comparison
evidence.

## Common Evidence Layout

Create one run folder per bridge call:

```text
<shot_or_gate_folder>/chatgpt_web_bridge/<YYYYMMDD-HHMMSS>_<branch>_<purpose>/
```

Recommended files:

```text
input_manifest.json
prompt.md
state_before.png
state_attached.png
state_sent.png
state_result.png
result_raw.md
result_manifest.json
local_outputs/
self_check.md
```

For image or video uploads, also save source copies or stable references in:

```text
inputs/
```

Never treat a web result as accepted without a local saved output and a
`self_check.md` PASS/FAIL note.

## Text Branch

Use for planning, prompt drafting, troubleshooting, shot notes, and analysis
that returns text.

Route:

```text
visible logged-in ChatGPT page
-> paste prompt through screenshot bridge
-> require safe send control
-> wait for completion
-> copy latest answer
-> verify copied text is not the sentinel or submitted prompt
-> save result_raw.md and result_manifest.json
```

### Verified Command (2026-06-10)

```powershell
python "C:\Users\A\.hermes\skills\productivity\chatgpt-screenshot-bridge\scripts\chatgpt_screenshot_bridge.py" `
  --prompt "Your prompt here" `
  --expect-contains "EXPECTED_MARKER" `
  --window-title-pattern "Request|ChatGPT|Response" `
  --allow-browser-window-fallback
```

Use flexible `--window-title-pattern` because ChatGPT window title changes
after each conversation. The pattern `"Request|ChatGPT|Response"` catches
most variations without needing per-conversation updates.

Required failure states:

```text
TEXT_BLOCKED_LOGIN_OR_CAPTCHA
TEXT_BLOCKED_ACCOUNT_OR_PAYMENT
TEXT_FAIL_NO_SAFE_SEND_BUTTON
TEXT_FAIL_COPY_SENTINEL_UNCHANGED
TEXT_FAIL_EMPTY_OR_WRONG_ANSWER
TEXT_PASS
```

Visible copy-button rule (accepted 2026-06-11):

```text
When the ChatGPT answer is complete, the leftmost button under the answer can
copy the answer directly. Prefer this visible button for text/result retrieval:
screenshot-confirm the answer is complete, click the leftmost copy button under
that answer, then verify the clipboard content is the new answer and not the
sentinel or the submitted prompt.
```

## Image Branch

Use for production image generation, image repair, failed-frame repair, clean
plates, texture references, keyframe replacement, and source frames.

### Screenshot-Gated Human Route (accepted 2026-06-11)

Use this route first for ChatGPT Web image repair when a visible logged-in
Chrome ChatGPT window is already open. This is the mature path from the
`screenshot-browser-100-percent-route` skill: operate like a human, and verify
every single action with a screenshot before continuing.

Core rule:

```text
one visible action -> one screenshot -> visual confirmation -> next action
```

Do not replace this with hidden window enumeration, broad coordinate logic,
resource-manager fallbacks, CDP, browser internals, or "largest window wins"
logic. If the screenshot does not show the expected state, the step did not
pass. Fix the visible step and screenshot again.

Single-image route:

```text
1. Screenshot the visible ChatGPT composer.
2. Paste the exact source JPG/PNG image into the visible composer.
3. Screenshot-confirm the composer contains an image thumbnail, not a file name
   such as events.jsonl and not an empty composer.
4. Paste the repair prompt into the same composer.
5. Screenshot-confirm image thumbnail + prompt text + safe send arrow are all
   in the same composer.
6. Click the visible send arrow.
7. Screenshot-confirm the message was sent and ChatGPT is generating.
8. Wait until a real repaired image is visible; do not wait in blind fixed
   loops after the screenshot already shows completion.
9. Save the visible result with `chatgpt_web_result_saver.py`.
10. Test that the saved local output exists.
```

Batch-image route:

```text
1. Start from a clean visible ChatGPT composer.
2. Paste or drag images one by one, or as a group only if the visible UI
   confirms every thumbnail.
3. After each paste/drop, take a screenshot immediately. The screenshot is the
   gate; no screenshot means the step did not happen.
4. Read the screenshot visually and confirm the thumbnail count increased.
5. Before sending, screenshot-confirm the composer shows exactly the requested
   number of image thumbnails and the prompt text in the same composer.
6. If the screenshot shows zero thumbnails, fewer thumbnails than requested, a
   wrong file, or an empty composer, the step is FAIL. Do not send.
7. Only after the screenshot proves the batch input is complete, click the
   visible send arrow and screenshot-confirm generation started.
8. Save outputs only from screenshots that visibly contain real returned
   images, not loading cards or empty composer states.
```

For batch testing, do not optimize away the screenshots. The productive path is
not "paste fast and assume"; it is:

```text
paste image 1 -> screenshot confirms 1 thumbnail
paste image 2 -> screenshot confirms 2 thumbnails
paste image 3 -> screenshot confirms 3 thumbnails
paste prompt -> screenshot confirms thumbnails + prompt + send arrow
send -> screenshot confirms generation
result -> screenshot confirms returned image(s)
save -> local file check
```

When selecting returned images from the right-side thumbnail strip, move the
mouse pointer away from the image and thumbnails before taking the save
screenshot. A hover cursor or hand pointer visible in the screenshot is UI
evidence contamination; retake the screenshot before saving.

Accepted 5-image batch evidence from 2026-06-11:

```text
C:\Users\A\Desktop\1\gate_1_clean_base\bridge_validation_runs\v2_maturity_runs_final\screenshot_gate_20260611_batch5_distinct
```

This run used five visually distinct inputs and one prompt with five different
instructions. The screenshots prove:

```text
01_clean_composer.png                  clean composer
02_after_image1.png ... 06_after_image5.png
                                      thumbnail count increased to 5
07_prompt_pasted.png                  5 thumbnails + long per-image prompt
08_sent.png                           submitted request
09_wait_90s.png                       5 returned result thumbnails visible
10_result_01_selected_clean.png ... 10_result_05_selected_clean.png
                                      each returned image selected with cursor
                                      moved away before saving
```

Saved local outputs:

```text
...\screenshot_gate_20260611_batch5_distinct\result_01\20260611-025118_result_save_c0f55a\local_outputs\batch5_result_01.png
...\screenshot_gate_20260611_batch5_distinct\result_02\20260611-025119_result_save_25158b\local_outputs\batch5_result_02.png
...\screenshot_gate_20260611_batch5_distinct\result_03\20260611-025120_result_save_4edaa7\local_outputs\batch5_result_03.png
...\screenshot_gate_20260611_batch5_distinct\result_04\20260611-025121_result_save_4aebd3\local_outputs\batch5_result_04.png
...\screenshot_gate_20260611_batch5_distinct\result_05\20260611-025122_result_save_a8db5e\local_outputs\batch5_result_05.png
```

Accepted evidence from 2026-06-11 single-image production test:

```text
C:\Users\A\Desktop\1\gate_1_clean_base\bridge_validation_runs\v2_maturity_runs_final\screenshot_gate_20260611_0208_i01
C:\Users\A\Desktop\1\gate_1_clean_base\bridge_validation_runs\v2_maturity_runs_final\screenshot_gate_20260611_0208_i02_retry
C:\Users\A\Desktop\1\gate_1_clean_base\bridge_validation_runs\v2_maturity_runs_final\screenshot_gate_20260611_0208_i03
```

Local saved outputs:

```text
...\screenshot_gate_20260611_0208_i01\result\20260611-020147_result_save_261331\local_outputs\01_frame_00_0.0s_repaired.png
...\screenshot_gate_20260611_0208_i02_retry\result\20260611-020919_result_save_458584\local_outputs\01_frame_01_0.5s_repaired.png
...\screenshot_gate_20260611_0208_i03\result\20260611-021149_result_save_6c0746\local_outputs\01_frame_02_1.0s_repaired.png
```

Key lesson:

```text
The successful path was screenshot-confirmed human operation, not the older
automatic drag fallback. The old fallback that dragged the first visible
Explorer item is invalid because it can attach the wrong file.
```

Batch rule:

```text
Maximum formal batch size: 10 images.
```

If the web UI shows a lower current upload or generation limit, obey the lower
visible limit. Split larger sets into:

```text
batch_01
batch_02
batch_03
```

Route:

```text
1. Put exact source images in inputs/.
2. Write prompt.md with preserve/remove constraints and output naming intent.
3. Paste prompt text first into the large bottom ChatGPT input band.
4. Drag image from File Explorer onto the ChatGPT page (automated via
   chatgpt_web_attachment_bridge.py --upload-method drag).
5. Wait for upload to complete (--attachment-wait 25 for images).
6. Screenshot-confirm every required thumbnail is attached (state_attached.png).
7. Click the visible ChatGPT send button inside the ChatGPT window.
8. Screenshot-confirm sent state (state_sent.png).
9. Wait for generated or edited image results.
10. Save result screenshots (state_result.png).
11. Save returned image via chatgpt_web_result_saver.py into local_outputs/.
12. Write result_manifest.json and self_check.md.
```

### V2 Batch Route

Use the V2 sequential route for production batches. Do not rely on one ChatGPT
message returning N repaired images for N inputs; live tests showed the web app
may return only one image for a multi-image request. Sequential mode is slower
but gives stable source-to-output mapping.

```powershell
python H:\AI\skills\comfyui-aaki-v3-video-baseline\scripts\chatgpt_web_batch_manifest.py `
  --inputs <folder-or-files> `
  --run-root <batch-run-root>

python H:\AI\skills\comfyui-aaki-v3-video-baseline\scripts\chatgpt_web_batch_runner.py `
  --manifest <batch>\input_manifest.json `
  --run-root <batch-run-root> `
  --attachment-wait 45 `
  --timeout-finish 480 `
  --send-retries 3 `
  --send-confirm-timeout 10
```

V2 status semantics:

```text
BATCH_PASS
  Every item produced a saved local repaired image and no warnings were recorded.

BATCH_PASS_WITH_WARNINGS
  Every item produced a saved local repaired image, but one or more intermediate
  web/attachment steps returned a nonzero status. Keep the warning and evidence,
  but the production output exists.

BATCH_FAIL
  At least one source image has no saved repaired local output.
```

Acceptance is output-driven:

```text
source image -> ChatGPT web result screenshot -> local_outputs/*_repaired.png
```

Do not call a batch mature if it only reports that text was pasted or a send
button was clicked. The local repaired output file is the required closure.

Sequential safety:

```text
If an item fails before `state_result.png` exists, stop the batch immediately.
Do not continue to the next source image, because unfinished ChatGPT generations
can stack in the same conversation and contaminate later items.
Use `--continue-on-item-fail` only for deliberate debugging, not production.
```

Windows path safety:

```text
Keep per-item run folders short, such as i01, i02, i03.
Keep attachment purpose short, such as b01, b02, b03.
Do not put long source names into every nested folder name; preserve mapping in
the manifest instead. Long nested paths can make PIL/OpenCV screenshot saves
fail with misleading "No such file or directory" errors.
```

Image prompt must preserve required invariants unless the user explicitly asks
to change them:

```text
camera angle
subject identity
subject pose
foreground object geometry
phone/keyboard/device geometry
lighting and shadows
scene composition
```

Required failure states:

```text
IMAGE_BLOCKED_LOGIN_OR_CAPTCHA
IMAGE_BLOCKED_ACCOUNT_OR_PAYMENT
IMAGE_FAIL_TOO_MANY_FILES
IMAGE_FAIL_ATTACHMENT_NOT_VISIBLE
IMAGE_FAIL_NO_SAFE_SEND_BUTTON
IMAGE_FAIL_NO_GENERATED_IMAGE
IMAGE_FAIL_SAVE_OUTPUT
IMAGE_FAIL_OUTPUT_WORSE_THAN_SOURCE
IMAGE_PASS_READY_FOR_VIDEO_USE
```

Acceptance rule:

```text
An image branch pass means the still image is good enough to enter the video
pipeline. It does not mean the video passed.
```

If video assembly creates dark spots, flicker, pasted texture, or geometry
corruption from a visually strong ChatGPT web image, keep the good image and
repair or restart the video construction method: more keyframes, direct
replacement, tighter masks, alignment, interpolation, or a fresh build from the
high-quality image base.

## Video Bridge — Verified Working (2026-06-10)

ChatGPT Web CAN analyze uploaded videos through the drag route.
Codex Desktop test confirmed:

```text
TEST_ID: VIDEO_BRIDGE_DRAG_G03_R2
ATTACHMENT_VISIBLE: yes
CAN_ANALYZE_VIDEO: yes
ONE_SENTENCE_CONTENT: A hand points at dark spots on a gray fabric mat
                       below a keyboard with pink backlighting.
```

For video repair workflows, use the frame extraction pipeline:

```text
video → ffmpeg extract frames → Image Bridge repair → reconstruct → verify
```

Direct video upload for analysis is also available via the attachment bridge:

```powershell
python chatgpt_web_attachment_bridge.py --branch video --upload-method drag `
  --prompt-order before --attachment-wait 60 --file video.mp4 --prompt-file prompt.md
```

### Screenshot-Gated Video Route (initial PASS 2026-06-11)

Use the same human-style screenshot route for video uploads. Direct drag/drop
from File Explorer is the default because the visible browser confirms the
actual uploaded files. Do not rely on fixed coordinates, hidden window state, or
previously uploaded attachments.

Core video route:

```text
1. Screenshot the visible ChatGPT composer and current browser position.
2. Drag the intended video files from File Explorer into the visible composer.
3. Screenshot-confirm the composer shows the expected number of video
   attachments.
4. If the browser is zoomed or the thumbnails are too small, enlarge/zoom the
   visible browser and screenshot again until every attachment is visible.
5. Paste the prompt.
6. Screenshot-confirm video attachments + prompt + safe send arrow are all in
   the same composer.
7. Click the visible send arrow.
8. Screenshot-confirm the message was sent.
9. Wait for the answer and screenshot-confirm the result text.
10. Copy the answer with the visible leftmost copy button under the completed
    answer, then verify clipboard text.
```

Accepted 3-video direct-drag evidence from 2026-06-11:

```text
C:\Users\A\Desktop\1\gate_1_clean_base\bridge_validation_runs\video_screenshot_gate_20260611\batch3_video
```

Key screenshots:

```text
06_current_zoomed_three_visible.png   browser enlarged; 3 video attachments visible
07_prompt_pasted_3videos.png          3 videos + prompt + send arrow visible
08_sent_3videos.png                   sent state visible
09_wait_45s_result.png                result visible; ChatGPT says it can see
                                      3 video files attached
```

Observed result:

```text
ChatGPT recognized all three uploaded MP4 files:
video_01_empty_plate.mp4
video_02_hand_pass.mp4
video_03_fixture.mp4

The answer completed in about 35 seconds in the final observed run.
```

Video route acceptance:

```text
VIDEO_SCREENSHOT_GATE_BATCH3_PASS
```

## Platform-Specific Pitfalls (verified 2026-06-10)

### False positive send/completion is P0

Do not use "the page stopped changing" as proof that ChatGPT finished. A page
that never sent the message is also stable. The attachment bridge must verify:

```text
1. a safe send arrow was visible before click
2. click changed the composer/send state
3. new response/result content appeared
4. result screenshot was saved
5. local output was saved or an explicit failure was recorded
```

Known failure statuses:

```text
ATTACHMENT_FAIL_WRONG_TARGET_WINDOW
ATTACHMENT_FAIL_SEND_NOT_CONFIRMED
ATTACHMENT_FAIL_NO_NEW_RESPONSE
ATTACHMENT_FAIL_TIMEOUT
RESULT_FAIL_NO_IMAGE_REGION
```

If `RESULT_FAIL_NO_IMAGE_REGION` is caused by a black screenshot, treat it as a
window capture failure, not proof that ChatGPT produced no image. Use
`--screenshot-file <attachment-run>\state_result.png` for deterministic replay.

### Loading spinner is not an image result

For the image branch, `state_result.png` must contain a real generated/repaired
image region. A ChatGPT loading card, dot pattern, "generating image" message,
or spinner is not a result and must not be saved as a repaired frame. Keep
waiting until an image-like region is visible, or fail with evidence.

### Cloudflare blocks CDP browser

`browser_navigate` to chatgpt.com lands on a Cloudflare "请验证您是真人" page.
The CDP browser path is dead for ChatGPT access. **Always use the screenshot
route** (pyautogui + mss + vision verification) for ChatGPT web interaction.

### Window title changes after every conversation

ChatGPT Chrome window title changes dynamically (e.g., `ChatGPT - Google Chrome`
→ `Response Request - Google Chrome`). The `chatgpt-screenshot-bridge` must use
flexible patterns like `"Request|ChatGPT|Response"` or position-based matching.

### Multiple Chrome windows cause misidentification

When multiple Chrome/Codex windows exist, broad visual matching can paste the
same prompt into the wrong app. This is a P0 contamination bug: it can duplicate
the task text into both Codex and ChatGPT, pollute the working thread, and make
the evidence invalid.

Current production rule:

```text
Use only the middle-screen ChatGPT Chrome window.
Verified workstation target: left=857, top=16, width about 1656, height about 1375.
Reject negative-coordinate windows.
Reject right-screen windows.
Reject Codex windows even if they have a send-like button.
All click/paste fallback points must be relative to the verified target window.
One bridge call may target exactly one composer/input box.
If the same prompt appears in Codex and ChatGPT, or in two ChatGPT composers,
the run is contaminated and must be marked failed evidence, not PASS.
If the verified middle-screen ChatGPT window is not found, stop with
ATTACHMENT_FAIL_WRONG_TARGET_WINDOW.
```

Do not use generic `"Google Chrome"` matching or "largest window wins" logic for
production image/video bridge work.
Do not use auto-move or auto-resize fallback logic to salvage a bad target
window; that can silently switch screens and recreate the double-send bug.

### pyautogui file upload is unreliable

Clicking "+" → navigating the menu → interacting with the Windows file dialog
is OS-dependent and unreliable via pyautogui. Image/video upload MUST be done
manually (drag-drop into the ChatGPT input area) with screenshot verification
before sending.

### ChatGPT video upload works through drag route

Our text-only capability query got a misleading answer ("videos not supported").
**Codex Desktop drag-upload test confirmed:** ChatGPT analyzed a dragged video
correctly — `CAN_ANALYZE_VIDEO: yes`. Use `--branch video --upload-method drag`.

## Stop Conditions

Stop before acting if ChatGPT web shows:

```text
login
captcha
payment
account or security prompt
privacy-sensitive form
unknown destructive action
```

Stop instead of guessing if:

```text
the safe send button is not visible
the attachment is not visible
the UI shows a lower limit than the requested batch
the returned output cannot be saved locally
the task would require using Codex built-in image generation
```

## Completion Checklist

A bridge run is complete only when these are true:

```text
inputs are recorded
prompt is saved
screenshots prove the browser state
outputs are saved locally or the failure is recorded
result_manifest.json exists
self_check.md states PASS or FAIL
the next pipeline action is named
```
