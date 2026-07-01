---
name: chatgpt-visible-send-bridge
description: "Use when Codex needs to send text, images, videos, or mixed media to a visible logged-in ChatGPT web page and retrieve the answer. This is the unified screenshot-gated human-style route for GPT web work: paste text, drag media, confirm by screenshot, send only with a visible safe arrow, and copy the completed answer with the visible copy button."
---

# ChatGPT Visible Send Bridge

## Purpose

Use one unified skill for text, image, video, and mixed-media ChatGPT web
requests. Treat all inputs as visible composer content:

```text
text  -> paste into the composer
image -> drag from File Explorer into the composer
video -> drag from File Explorer into the composer
```

Do not split this into separate default skills. The stable method is human-eye
operation with screenshot gates.

## Core Rule

```text
one visible action -> one screenshot -> visual confirmation -> next action
```

If the screenshot does not show the expected state, the step failed. Fix the
visible state and screenshot again before continuing.

The only permitted control method is visual operation:

```text
screenshot -> inspect the visible page -> optionally crop/zoom the target area
-> visible mouse/keyboard action -> screenshot-confirm
```

For Codex execution, the determined default input method is virtual
mouse/keyboard on the visible desktop:

```text
virtual mouse move/click/drag -> virtual keyboard paste/Enter
-> screenshot-confirm -> clipboard/result verify
```

This is still the human-eye visible route because every state is judged from
screenshots. Do not replace it with CDP, DOM, browser takeover, hidden upload,
or dry-run. Do not claim success from a virtual action alone; success requires
the next screenshot or clipboard/output verifier.

Do not use browser takeover, debugging connections, DOM reads, CDP, hidden
browser APIs, scripted uploads, or any non-visual control path. These are not
fallbacks for this skill. If a visible click misses, solve that same visible
step with zoomed screenshots and candidate-area coverage clicks.

All elapsed time counts: screenshots, waiting, action time, judgement,
thinking, failure analysis, and repair attempts. Do not exclude thinking time
or tool recovery time from the run total.

This is a strict state machine, not a suggestion:

```text
no screenshot -> no state transition
no visual proof -> no success claim
failed gate -> repair visible state -> screenshot again
```

Do not choose a faster route because it looks easier. The default route is the
human-eye route: use the visible Windows/browser surface, act like a person,
take normal visible screenshots, and accept only what the screenshot proves.
Keep the physical operation simple. Do not add extra window switching,
per-file selection, coordinate experiments, or alternate upload methods when
the visible simple route is available.
If the simple visible method still cannot be made to work after local repair,
stop and ask the user instead of adding complex control paths.

## Acceptance Token Boundary

Fixed acceptance phrases are only test sentinels. They are allowed for synthetic
stability tests such as:

```text
Reply with exactly this token only:
GPT_V6_STABILITY_R01_PASS
```

They must not become the normal product/task behavior. For real image, video,
or mixed-media work, the prompt must ask for the actual requested content and
may include a separate verification marker only when needed:

```text
Describe what is visible in this image/video in one sentence.
End with: GPT_IMAGE_COORDINATE_TEST_PASS
```

Do not write normal media prompts as "only reply the fixed phrase" unless the
entire purpose of that run is a synthetic transport check. If a model replies
with meta-reasoning such as "the instruction says..." before the token, record
the prompt as contaminated and repair the prompt; do not treat that as a mature
task result.

Do not maximize the browser when the task benefits from seeing File Explorer,
ChatGPT, and the evidence/logging surface together. Keep the normal visible
layout unless the user explicitly asks to maximize.

## Fixed Three-Zone Visible Workbench

When the user keeps the desktop in the three-zone layout, preserve it and use it
as the default visible media workbench instead of fullscreening:

```text
screen: 2560 x 1440
left reserve / desktop evidence zone: x=0..853
middle browser zone: left=854 top=12 width=846 height=1375
right File Explorer zone: left=1705 top=16 width=846 height=1375
```

For this workbench, the browser is intentionally placed in the middle large
screen area and File Explorer is placed on the right. Do not move either window
unless a screenshot proves it is blocking the current step. If the user has
already arranged this layout, treat the layout itself as part of the state
contract.

Observed media source coordinates in this workbench:

```text
single video icon center in right File Explorer: about x=1935 y=186
single image icon center in right File Explorer: about x=1935 y=186
broad browser drop target: x=1200 y=760, or any visible middle-browser blank area
release-confirm click: same broad browser area after release
```

The required media upload action in this workbench remains:

```text
hold visible file icon -> drag into middle browser page -> release
-> click middle browser page once -> screenshot-confirm thumbnail landed
```

Do not aim at a tiny composer coordinate for media. The whole point of this
workbench is that the right-side file icon and middle browser page are both
visible, so the drag route is short and repeatable.

## Local Repair Rule

When a state fails, repair that same state. Do not restart the run, open a new
conversation, change windows, or change method unless the screenshot proves the
current visible state is unrecoverable.

For target-position failures such as send arrows, confirmation buttons,
drop targets, composer focus, or copy buttons, use candidate-area coverage:

```text
1. Screenshot the current visible state.
2. Crop or zoom the target area until the likely target bounds are clear.
3. Define a small high-probability rectangle around the visible target.
4. Cover that rectangle with several visible clicks or click+Enter attempts.
5. Screenshot once after the coverage batch and judge the state.
```

Candidate-area coverage is not random clicking. First locate the target's
probable area from a zoomed screenshot; then cover only that small area. Use
this for small UI targets instead of restarting or switching to non-visual
automation.

## Strict State Machine

Every run must create a run folder first. Advance through these states in order.
Each state has an exit gate. If the gate fails, stay in the same state, repair
the visible condition, and screenshot again. Each state record must include:

```text
planned time
actual elapsed time
evidence screenshot(s)
PASS/FAIL
failure reason when failed
local repair action when repaired
```

```text
S0_TASK_READY
  Input: task text, media files, and target ChatGPT page are known.
  Action: create the run folder.
  Exit gate: run folder exists.

S1_PAGE_VISIBLE
  Action: screenshot the current visible browser state.
  Evidence: 01_before.png
  Exit gate: screenshot shows a logged-in ChatGPT page or usable composer.
  Clean-start rule: for every new validation/test run, start from a fresh
  ChatGPT conversation unless the user explicitly asks to continue an existing
  thread. Old attachments, old prompts, and old result pages contaminate timing
  and state verification.

S2_TEXT_VISIBLE
  Action: paste required text into the visible composer when text is required.
  Evidence: 02_text_visible.png
  Exit gate: screenshot shows the expected text in the composer.
  If no text is required, write "SKIPPED: no text input" in self_check.md.
  Ordering rule: complete text input before media upload. Text needs composer
  focus; media does not need precise composer targeting.

S3_MEDIA_DROPPED
  Action: hold the visible image/video thumbnail body in File Explorer, drag it
  into any broad visible area of the ChatGPT page, and release. For one visible
  file in the folder, do not add a separate select step; press, drag, release.
  For batches, select the intended group only when needed, then use the same
  broad-page drag.
  Evidence: 03_media_drop_state.png
  Exit gate: screenshot shows the drag/release reached ChatGPT. This does not
  prove upload success.
  Required precheck: screenshot-confirm the selected File Explorer items are
  exactly the intended media files before dragging.
  Selection rule: when the media folder contains only the intended files, use a
  simple select-all in that folder. Do not Ctrl-click files one by one unless
  select-all would include wrong files.
  Drop target rule: do not over-aim at a tiny composer coordinate. Drag the
  selected files into the broad visible ChatGPT page area.
  Codex input rule: perform this with virtual mouse drag when Codex is the
  operator. Use File Explorer's visible thumbnail/icon body as the drag source.
  Do not use scripted upload, file-dialog automation, DOM/CDP, or path paste as
  the default media route.

S4_CONFIRM_DROP_CLICK
  Action: after releasing dragged media on the broad visible ChatGPT page area,
  click the ChatGPT page once. The release-plus-click pair is the required
  simple route:
  `drag into ChatGPT page -> release -> click the ChatGPT page once`.
  Do not aim at a tiny composer coordinate; the file should fall into the
  composer after the confirmation click. This confirmation click is mandatory
  for every image, video, or mixed-media upload attempt.
  Repair: if a single confirmation click does not land the files, crop/zoom the
  drop target or floating media stack and use candidate-area coverage clicks in
  that same visible area.
  Evidence: 04_attachments_visible.png
  Exit gate: screenshot shows composer thumbnails for every required media file
  and the count is correct. Drag hover alone is FAIL.
  Codex input rule: the confirmation click is also a virtual mouse click. If it
  misses, use visible candidate-area coverage on the page/drop stack, then take
  one screenshot to judge whether thumbnails landed.

S5_PROMPT_READY
  Action: ensure all required text, media thumbnails, and the safe send arrow
  are visible together.
  Evidence: 05_prompt_ready.png
  Exit gate: screenshot shows all required attachments, prompt text when
  required, and a visible safe send arrow.

S6_SENT
  Action: click only the visible safe send arrow, or focus the visible composer
  text area and press Enter when the send arrow is visibly available.
  Repair: if the send action misses, do not restart. Crop/zoom the composer
  lower-right area, locate the visible up-arrow button, and cover the small
  arrow-button area with several visible clicks. For Enter sending, cover the
  likely text-entry area with click+Enter attempts. Screenshot after the
  coverage batch.
  Coordinate rule: when using a saved screenshot or scaled preview for target
  location, convert to the real screenshot/desktop coordinate size first. A
  click based on a scaled preview can visibly land in the composer instead of
  on the arrow.
  Evidence: 06_sent.png
  Exit gate: screenshot shows the request has been sent.

S7_RESULT_COMPLETE
  Action: wait until the answer or result is complete. The preferred visible
  completion signal is: generation has stopped and a down-arrow appears near
  the lower middle of the ChatGPT page. Click this down-arrow to jump to the
  bottom of the conversation before retrieving output.
  Evidence: 07_result_complete.png
  Exit gate: screenshot shows completion, not an in-progress generation, and
  after clicking the down-arrow the bottom of the latest answer is visible.

S8_OUTPUT_RETRIEVED
  Action: for text, after S7 has jumped to the bottom, locate the latest answer's
  bottom action row. Click the leftmost button in that bottom row: this is the
  copy button. Do not copy from an older answer. If the copy button is small,
  crop/zoom that bottom action row and use small candidate-area coverage on the
  leftmost button only.
  For images or files, open/select each output separately, move the mouse away,
  screenshot-confirm the clean output, then save.
  Evidence: 08_output_retrieved.png
  Exit gate: copied or saved output exists.

S9_OUTPUT_VERIFIED
  Action: verify the copied/saved result.
  Evidence: result_raw.md, result_files.txt, or equivalent.
  Exit gate: output is not empty, not the submitted prompt, and not a clipboard
  sentinel.

S10_SELF_CHECK_DONE
  Action: write self_check.md with every state, evidence file, and PASS/FAIL.
  Exit gate: self_check.md proves all required states passed or records the
  exact failure state.
```

## Default Route

1. Use the already visible logged-in ChatGPT browser page when available.
   For a new validation/test run, click New Chat first and screenshot-confirm a
   clean composer.
2. Screenshot the current browser state before acting.
3. Paste text directly into the visible composer and screenshot-confirm it
   first.
4. Screenshot-confirm File Explorer has selected exactly the intended
   image/video files.
5. Drag image/video files from File Explorer into the broad visible ChatGPT page
   area. Do not over-target a tiny composer coordinate.
6. After release, always click the visible ChatGPT page, drop zone, or
   dragged-image stack once to confirm the drop. This is an independent gate,
   not an optional cleanup action.
7. If ChatGPT shows a drag-hover drop zone or a floating dragged-image stack
   after release, click the drop zone or the dragged image stack once to
   confirm the drop, then screenshot-confirm the files have landed as composer
   thumbnails. Do not treat drag hover alone as upload success.
8. Screenshot-confirm every input is present in the composer.
9. Paste or verify the prompt text in the same composer.
10. Screenshot-confirm attachments, prompt text, and a safe send arrow.
11. Click only the visible safe send arrow.
12. Screenshot-confirm the request was sent.
13. Wait for the answer or result and screenshot-confirm completion. Completion
    is confirmed when generation has stopped and the lower-middle down-arrow is
    visible.
14. Click the lower-middle down-arrow to jump to the bottom of the conversation.
15. At the bottom of the latest answer, click the leftmost button in the bottom
    action row; this is the copy button.
16. Verify the copied answer is new content, not the submitted prompt or a
    clipboard sentinel.
17. Save evidence in the run folder.

## Mixed Input Rules

Ordering rule:

```text
text first -> screenshot-confirm text -> media after
```

For mixed text/image/video inputs, paste or type the text first and
screenshot-confirm it in the composer before adding media. After media is
attached, do not rely on repositioning the text cursor in the composer; cursor
placement is harder once thumbnails are present.

For text-only:

```text
screenshot -> paste text -> screenshot -> send -> screenshot
-> wait for stopped generation + lower-middle down-arrow
-> click down-arrow to jump to bottom
-> click latest answer bottom-row leftmost copy button
-> verify clipboard content
```

For images:

```text
screenshot -> drag each image from File Explorer -> screenshot count check -> paste prompt
-> screenshot -> send -> result screenshot -> save/copy result
```

For videos:

```text
screenshot -> drag each video -> screenshot count check -> paste prompt
-> screenshot -> send -> answer screenshot -> copy answer
```

For mixed media, use the same sequence. The composer must visibly contain all
required text, image, and video inputs before sending.

## Visible Copy/Paste Fallback

Direct drag/drop remains the default media route. If visible drag/drop fails or
is unreliable, use this human-visible fallback:

```text
select the exact intended files in File Explorer -> screenshot precheck ->
Ctrl+C -> click the ChatGPT composer -> Ctrl+V -> screenshot attachment count
```

This fallback copies selected file objects, not file paths and not image/video
clipboard pixels. The precheck screenshot must show the exact intended files
selected in File Explorer before `Ctrl+C`. For mixed inputs, complete and
screenshot-confirm text first, then paste image/video files. If `Ctrl+V`
pastes text instead of media attachments, mark FAIL with reason:

```text
clipboard did not contain the selected file object
```

Then reselect the exact files visibly in File Explorer and retry that same
media step.

## Evidence Requirements

Create one run folder per task. Recommended files:

```text
01_before.png
02_text_visible.png
03_media_drop_state.png
04_attachments_visible.png
05_prompt_ready.png
06_sent.png
07_result_complete.png
08_output_retrieved.png
result_raw.md
result_files.txt
self_check.md
```

For batches, use numbered screenshots such as:

```text
02_after_image1.png
03_after_image2.png
04_after_video1.png
```

The screenshot is the proof. Do not claim a file was uploaded, a prompt was
sent, or an answer was copied unless the evidence shows it.

`self_check.md` must include a state manifest like this:

```text
S1_PAGE_VISIBLE: PASS -> 01_before.png -> planned/actual seconds
S2_TEXT_VISIBLE: PASS/SKIPPED -> 02_text_visible.png or reason -> planned/actual seconds
S3_MEDIA_DROPPED: PASS/SKIPPED -> 03_media_drop_state.png or reason -> planned/actual seconds
S4_CONFIRM_DROP_CLICK: PASS/SKIPPED -> 04_attachments_visible.png or reason -> planned/actual seconds
S5_PROMPT_READY: PASS -> 05_prompt_ready.png -> planned/actual seconds
S6_SENT: PASS -> 06_sent.png -> planned/actual seconds
S7_RESULT_COMPLETE: PASS -> 07_result_complete.png -> planned/actual seconds
S8_OUTPUT_RETRIEVED: PASS -> 08_output_retrieved.png -> planned/actual seconds
S9_OUTPUT_VERIFIED: PASS -> result_raw.md/result_files.txt -> planned/actual seconds
```

For any local repair or coverage batch, `self_check.md` must also record:

```text
target area
whether the target area was zoomed/cropped before clicking
coverage pattern such as center/edges/3x3/4x4
number of clicks or click+Enter attempts
elapsed seconds including thinking and judgement
before/after screenshot evidence
```

## Human-Style Constraints

- Use only the visible screenshot-driven route. Browser takeover, debugging
  connections, DOM inspection, CDP, hidden browser APIs, and scripted upload or
  send actions are prohibited for this skill.
- Codex must use virtual mouse and virtual keyboard for actual visible tests
  unless the user explicitly asks for physical/manual intervention. The virtual
  device actions must be short, visible, screenshot-gated, and verifiable.
- Images and videos must use direct drag/drop from File Explorer by default.
- Input text first, then drag media. Text needs precise composer focus; media
  only needs the broad visible ChatGPT page area plus a confirmation click.
- Before dragging media, screenshot-confirm the selected File Explorer files are
  exactly the intended images/videos. If File Explorer navigates away or the
  selection changes, stop and reopen the exact media folder.
- When the folder contains only the intended media files, select all files once,
  then slowly drag the selected group into ChatGPT. Avoid per-file Ctrl-click
  selection in this normal case because it can change focus or navigate away.
- Drop media into the broad ChatGPT page area, then click once after release to
  confirm the drop. The confirmation click is required.
- Drag-hover is not success. After dropping a batch, click the visible drop
  target or image stack once if needed, then require thumbnails inside the
  composer before pasting the prompt.
- Prefer visible copy buttons for answer retrieval.
- Enlarge the screenshot crop or zoom the visible page region if thumbnails,
  send arrows, or confirmation buttons are too small to locate accurately.
- For small targets, use candidate-area coverage clicks after locating the
  small high-probability target area. A coverage batch may contain several
  clicks or click+Enter attempts before the next screenshot.
- Move the mouse pointer away before taking final result screenshots, so hover
  cursors do not contaminate evidence.
- Do not depend on fixed coordinates after the user moves the browser.
- Do not treat one missed click as a reason to restart. Repair the current
  state with zoomed visual localization and candidate-area coverage.
- Do not reuse already uploaded attachments by mistake.
- Do not use hidden DOM/CDP/browser internals.
- Do not use the plus-button file dialog as the default upload route.
- Do not click microphone, sound-wave, voice, stop, or end controls.

## Forbidden Shortcuts

These are forbidden as the default route, even if they look faster:

```text
hidden DOM inspection
CDP/browser internals
browser takeover or debugging connection
DOM reads or browser automation APIs
scripted upload
scripted send/click
plus-button file dialog as the upload path
copying or pasting image/video file paths into the composer
pasting image/video clipboard content as the primary media upload path
fixed-coordinate clicking without fresh screenshot confirmation
restarting a recoverable state instead of repairing that same state
claiming success from drag hover or a drop-zone overlay
copying before the result is visibly complete
reusing old attachments already present in the composer
skipping self_check.md
```

Non-visible automation is prohibited for this skill even as a fallback. If a
visible action fails, use zoomed screenshots and candidate-area coverage in the
same visible state.

## Maturity Model

During exploration or any new media type, keep one screenshot after every
visible action.

For tiny targets, a "visible action" may be a bounded coverage batch:

```text
zoomed target screenshot -> 5-12 candidate clicks/click+Enter attempts inside
the small target area -> screenshot confirmation
```

Use this only after the target area has been visually located. Record the
coverage area, number of attempts, and elapsed time in `self_check.md`.

After repeated PASS evidence, some screenshots may become checkpoints:

```text
before -> all inputs visible -> prompt ready/send arrow -> sent -> result
```

Do not remove a checkpoint until prior runs prove that the skipped actions are
stable. If a later result looks wrong, go back to one-action-one-screenshot.

## Failure States

Stop or mark FAIL when:

```text
login/captcha/payment/account/security prompt appears
safe send arrow is not visible
attachment count is wrong
wrong file is attached
composer is empty after input
result screenshot does not show completion
copy button does not change clipboard content
browser state changed and no fresh screenshot exists
```

## Field Notes

For the 2026-06-11 successful text/image/video consolidation and evidence, read
`references/field-notes-20260611.md`.

## Verified Simple Drag Case

Latest verified case: 2026-06-12, `T02_single_image`.

Validated route:

```text
hold visible image thumbnail -> drag to broad ChatGPT page -> release
-> click ChatGPT page once -> screenshot confirms attachment in composer
-> type prompt -> click visible send arrow -> screenshot confirms result
```

Evidence run:

```text
C:\Users\A\Documents\Codex\2026-06-12\chatgpt-visible-send-bridge-text-h\outputs\visible-send-bridge-tests\run_20260612_191831_T02_drag_retest_simple
```

Evidence files:

```text
01_before_fixed_layout.png
02_after_drag_release.png
03_after_release_confirm_click_wait8.png
04_prompt_visible.png
05_after_send_wait8.png
06_result_wait30.png
self_check.md
```

Measured result:

```text
S1-S4 drag/release/confirm-click: 12.69 seconds, PASS
S5-S7 prompt/send/result wait: 36.07 seconds, PASS
```

Conclusion: the simple route is verified. Do not replace it with browser
takeover, debugging connections, DOM/CDP, clipboard upload, fullscreening, or
window movement. If this simple visual route fails in a future run, repair the
same visible state with screenshots and small candidate-area coverage. If it
still cannot be made to work, stop and ask the user.

## Verified Three-Zone Media Workbench Case

Latest verified case: 2026-06-22, three-zone visible workbench.

Validated layout:

```text
screen: 2560 x 1440
middle browser zone: left=854 top=12 width=846 height=1375
right File Explorer zone: left=1705 top=16 width=846 height=1375
file icon center: about x=1935 y=186
broad browser drop/confirm target: about x=1200 y=760
```

Validated route:

```text
hold visible file icon in the right File Explorer zone
-> drag into the middle browser page
-> release
-> click the middle browser page once
-> screenshot confirms attachment in composer
-> paste content prompt
-> click visible up-arrow send button
-> screenshot confirms result
```

Evidence root:

```text
C:\Users\A\Desktop\coordinate-method-real-browser-test-v3\coordinate-click-automation\reports\media-actual\20260622_current
```

Completed evidence:

```text
GPT image: 10/10 completed with screenshot evidence.
Contact sheet:
C:\Users\A\Desktop\coordinate-method-real-browser-test-v3\coordinate-click-automation\reports\media-actual\20260622_current\gpt_image_10round_result_contact_sheet.png

GPT video: R01 completed with screenshot evidence.
Drop confirmation:
C:\Users\A\Desktop\coordinate-method-real-browser-test-v3\coordinate-click-automation\reports\media-actual\20260622_current\gpt_video_10round\R01_after_drag_confirm_fixed_three_zone.png
Result:
C:\Users\A\Desktop\coordinate-method-real-browser-test-v3\coordinate-click-automation\reports\media-actual\20260622_current\gpt_video_10round\R01_result_wait80_fixed_three_zone.png
```

Measured points:

```text
Image R01 drag/release/confirm-click: 10.00 seconds, PASS.
Image R02-R10 each completed in about 55 seconds including wait and screenshots.
Video R01 drag/release/confirm-click: 14.28 seconds, PASS.
Video R01 send/result wait: 80.70 seconds, PASS.
```

Important correction: when the right File Explorer window is in the three-zone
workbench, the media icon center is around `x=1935 y=186`, not the old
single-window value around `x=1315 y=186`. Always screenshot-confirm the current
three-zone layout before reusing coordinates.

User stop instruction: on 2026-06-22 the user stopped further image/video
testing after these completed points. Do not claim unrun video 10-round
coverage. Resume from this evidence only if the user explicitly asks to
continue media testing.

## Verified Three-Zone Text Cases

Latest verified text cases: 2026-06-22, same three-zone visible workbench.

Workbench:

```text
screen: 2560 x 1440
middle browser zone: left=854 top=12 width=846 height=1375
right File Explorer zone: left=1705 top=16 width=846 height=1375
```

GPT text one-shot:

```text
prompt: Reply with exactly this token only: GPT_THREE_ZONE_TEXT_PASS
input click: about x=1040 y=1320
send click: about x=1598 y=1320
elapsed: 24.46 seconds
result: PASS, visible reply contained GPT_THREE_ZONE_TEXT_PASS exactly as answer
evidence:
C:\Users\A\Desktop\coordinate-method-real-browser-test-v3\coordinate-click-automation\reports\three-zone-text\20260622_gpt_deepseek_once\gpt_03_result_wait22.png
```

DeepSeek text one-shot:

```text
prompt: Reply with exactly this token only: DEEPSEEK_THREE_ZONE_TEXT_PASS
initial input click: about x=1035 y=760
initial send click: about x=1570 y=826
elapsed: 22.46 seconds
coordinate/send/result visibility: PASS
strict exact-token behavior: FAIL, DeepSeek added an explanatory bullet before
the token
evidence:
C:\Users\A\Desktop\coordinate-method-real-browser-test-v3\coordinate-click-automation\reports\three-zone-text\20260622_gpt_deepseek_once\deepseek_03_result_wait20.png
```

Interpretation: the middle fixed browser workbench is valid for GPT text and
DeepSeek text coordinate operation. For DeepSeek synthetic exact-token tests,
do not treat a reply that includes explanatory text as exact PASS; either record
it as coordinate PASS / exact-token FAIL, or rerun with a stronger no-explanation
prompt if exact output is the acceptance criterion.

## Verified Fullscreen Long-Answer Bottom Jump And Copy Coordinates

Latest verified case: 2026-06-22, maximized browser, `2560 x 1440`, browser zoom
`100%`, long answer requiring scrolling.

Purpose:

```text
For long answers, the latest answer's copy button may not be visible until the
page jumps to the bottom. Use the visible down-arrow first, then copy from the
latest answer bottom action row.
```

GPT fullscreen long-answer case:

```text
long prompt marker: GPT_LONG_COPY_TEST_DONE
down-arrow coordinate: x=1309 y=1274
latest answer copy button: x=926 y=1232
clipboard verification: PASS, copied text contained GPT_LONG_COPY_TEST_DONE
copied length: 4035
evidence:
C:\Users\A\Desktop\coordinate-method-real-browser-test-v3\coordinate-click-automation\reports\fullscreen-long-answer-copy\20260622\gpt\gpt_06_after_send_wait90.png
C:\Users\A\Desktop\coordinate-method-real-browser-test-v3\coordinate-click-automation\reports\fullscreen-long-answer-copy\20260622\gpt\gpt_07_after_down_arrow_click.png
C:\Users\A\Desktop\coordinate-method-real-browser-test-v3\coordinate-click-automation\reports\fullscreen-long-answer-copy\20260622\gpt\gpt_08_after_copy_click.png
```

DeepSeek fullscreen long-answer case:

```text
long prompt marker: DEEPSEEK_LONG_COPY_TEST_DONE
down-arrow coordinate: x=1770 y=1210
latest answer copy button: x=1042 y=1201
clipboard verification: PASS, copied text contained DEEPSEEK_LONG_COPY_TEST_DONE
copied length: 9889
evidence:
C:\Users\A\Desktop\coordinate-method-real-browser-test-v3\coordinate-click-automation\reports\fullscreen-long-answer-copy\20260622\deepseek\deepseek_03_after_send_wait90.png
C:\Users\A\Desktop\coordinate-method-real-browser-test-v3\coordinate-click-automation\reports\fullscreen-long-answer-copy\20260622\deepseek\deepseek_04_scrolled_up_down_arrow_visible.png
C:\Users\A\Desktop\coordinate-method-real-browser-test-v3\coordinate-click-automation\reports\fullscreen-long-answer-copy\20260622\deepseek\deepseek_06_after_copy_click.png
```

Observed difference:

```text
GPT down-arrow: near lower middle above the composer.
DeepSeek down-arrow: near the answer area's right-lower side above the composer.
```

Rule: for long answers, do not try to copy while the bottom action row is not
visible. First screenshot-confirm the down-arrow, click it, screenshot-confirm
the final lines and bottom action row, then click the latest answer's leftmost
copy button.
