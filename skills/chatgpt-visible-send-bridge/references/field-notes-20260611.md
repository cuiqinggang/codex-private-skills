# Field Notes 2026-06-11

These notes preserve the successful route discovered during live ChatGPT Web
testing. They are evidence and operating memory for the unified
`chatgpt-visible-send-bridge` skill.

## Main Lesson

The reliable method is the simple human-eye method:

```text
see the browser -> perform one visible action -> screenshot -> confirm by eyes
-> continue
```

This applies equally to text, images, videos, and mixed inputs. Text is pasted.
Images and videos are dragged or pasted into the visible composer. Screenshots
are the gate.

## What Changed

Old thinking treated text, image, and video as separate technical routes. The
successful route treats them as one visible composer workflow:

```text
text prompt
text + image
text + video
text + images + videos
```

All are the same operation pattern:

```text
put visible input into ChatGPT composer -> screenshot-confirm -> send -> copy
or save result
```

## Rules Accepted From Testing

1. Direct drag/drop is the default for image and video files.
2. Screenshot after every visible action during immature testing.
3. If a thumbnail is too small or hidden, enlarge or zoom the browser and
   screenshot again.
4. Do not rely on negative coordinates, fixed window positions, or hidden
   window state.
5. Do not rely on old complex upload scripts as the default. Keep them only as
   backup or diagnostics.
6. If the screenshot does not show the expected state, the step is not accepted.
7. The answer's leftmost bottom copy button can directly copy text results.
8. Move the cursor away before final screenshots to avoid hand-cursor
   contamination over returned images.

## Drag Hover Confirmation Addendum 2026-06-11

Batch image drag/drop can visibly enter ChatGPT's drop zone without completing
the upload. If the screenshot shows a floating dragged-image stack, a drop-zone
overlay, or text such as "add content", do not count that as success yet.

Required gate:

```text
drag selected files into composer -> screenshot hover/drop-zone state -> click
the drop zone or dragged-image stack once -> screenshot composer thumbnails
```

Only the final screenshot with thumbnails inside the composer counts as
successful upload evidence.

## Text Retrieval

For text answers, use the visible copy button under the completed ChatGPT
answer:

```text
answer complete -> screenshot -> click leftmost copy button -> clipboard check
```

Clipboard verification must prove the copied text is the answer, not the input
prompt or a sentinel.

## Image Batch Evidence

Single-image screenshot route passed for three source frames:

```text
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
```

3-image batch passed:

```text
${REDACTED_SECRET}
```

5-image batch passed with five distinct inputs and distinct instructions:

```text
${REDACTED_SECRET}
```

Important image lesson:

```text
When selecting returned images from the right-side result thumbnails, select
each result separately, move the mouse away, screenshot-confirm the clean
selected result, then save.
```

## Video Batch Evidence

3-video direct-drag route passed:

```text
${REDACTED_SECRET}
```

Key screenshots:

```text
06_current_zoomed_three_visible.png
  Browser enlarged/zoomed; 3 video attachments visible.

07_prompt_pasted_3videos.png
  3 videos, prompt, and safe send arrow visible.

08_sent_3videos.png
  Request sent.

09_wait_45s_result.png
  Result visible; ChatGPT said it could see 3 attached video files.
```

ChatGPT recognized:

```text
video_01_empty_plate.mp4
video_02_hand_pass.mp4
video_03_fixture.mp4
```

Final observed completion time:

```text
about 35 seconds
```

Status:

```text
VIDEO_SCREENSHOT_GATE_BATCH3_PASS
```

## Maturity Path

Current stage:

```text
one action -> one screenshot
```

Later stable stage:

```text
checkpoint screenshots
```

Possible checkpoint set after repeated PASS runs:

```text
1. before input
2. all inputs visible
3. prompt ready with send arrow
4. sent
5. result complete
6. copied/saved output verified
```

If any wrong result appears, immediately return to one-action-one-screenshot.

## Default Skill Decision

Use `chatgpt-visible-send-bridge` as the default skill for sending text,
images, videos, or combinations to ChatGPT Web.

Use older scripts or deeper automation only when explicitly requested or when
diagnosing why the visible method failed.
