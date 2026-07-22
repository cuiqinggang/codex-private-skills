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
${REDACTED_SECRET}
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
${REDACTED_SECRET}
```

Completed evidence:

```text
GPT image: 10/10 completed with screenshot evidence.
Contact sheet:
${REDACTED_SECRET}

GPT video: R01 completed with screenshot evidence.
Drop confirmation:
${REDACTED_SECRET}
Result:
${REDACTED_SECRET}
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
${REDACTED_SECRET}
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
${REDACTED_SECRET}
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
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
```

DeepSeek fullscreen long-answer case:

```text
long prompt marker: DEEPSEEK_LONG_COPY_TEST_DONE
down-arrow coordinate: x=1770 y=1210
latest answer copy button: x=1042 y=1201
clipboard verification: PASS, copied text contained DEEPSEEK_LONG_COPY_TEST_DONE
copied length: 9889
evidence:
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
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

## Verified Fullscreen Custom Toolbar Sidebar Basemap

Latest verified case: 2026-07-02, maximized Chrome on `DISPLAY2`, `2560 x 1440`,
browser zoom `100%`, ChatGPT home/clean composer page, custom black toolbar
visible under the bookmarks bar.

Evidence root:

```text
${REDACTED_SECRET}
```

Actual virtual-click tested points:

```text
sidebar_closed open sidebar:  x=25   y=151  PASS
sidebar_open collapse:        x=220  y=152  PASS
sidebar_closed input:         x=1045 y=751  PASS
sidebar_open input:           x=1175 y=751  PASS
sidebar_closed Type toolbar:  x=123  y=156  PASS
sidebar_closed Tone toolbar:  x=244  y=156  PASS by overlap observation
```

Sidebar closed coordinate set:

```text
left rail:
  open sidebar / ChatGPT logo: x=25 y=151
  new chat icon:               x=25 y=204
  search icon:                 x=25 y=240
  pinned/sidebar item:         x=25 y=276
  history/chat bubble:         x=25 y=312

custom toolbar:
  Type:       x=123  y=156
  Tone:       x=244  y=156
  Length:     x=365  y=156
  Dig Deeper: x=486  y=156
  Developer:  x=608  y=156
  Creative:   x=730  y=156
  Excel Pro:  x=850  y=156
  Reset:      x=2359 y=156
  Export:     x=2480 y=156

composer:
  plus:       x=947  y=751
  input:      x=1045 y=751
  dropdown:   x=1569 y=751
  mic:        x=1620 y=751
  black btn:  x=1664 y=751
  image chip: x=1171 y=824
  write chip: x=1306 y=824
  search chip:x=1444 y=824
```

Sidebar open coordinate set:

```text
left sidebar:
  collapse toggle: x=220 y=152
  new chat row:    x=122 y=204
  search row:      x=122 y=240
  library row:     x=122 y=276
  projects row:    x=122 y=312
  scheduled row:   x=122 y=348
  apps row:        x=122 y=384
  more row:        x=122 y=420

custom toolbar:
  Type:       x=333  y=156
  Tone:       x=452  y=156
  Length:     x=573  y=156
  Dig Deeper: x=692  y=156
  Developer:  x=814  y=156
  Creative:   x=934  y=156
  Excel Pro:  x=1054 y=156
  Reset:      x=2359 y=156
  Export:     x=2480 y=156

composer:
  plus:       x=1052 y=751
  input:      x=1175 y=751
  dropdown:   x=1680 y=751
  mic:        x=1725 y=751
  black btn:  x=1768 y=751
  image chip: x=1275 y=824
  write chip: x=1413 y=824
  search chip:x=1544 y=824
```

Safety rule: do not mix sidebar-open and sidebar-closed coordinates. The same
screen point can target different controls after the sidebar changes. Do not
click mic, voice/send, Reset, or Export during coordinate calibration unless
the user explicitly asks for that exact action.

## Verified Ordinary Text State Machine - 2026-07-04

Latest verified case: 2026-07-04, maximized Chrome, `2560 x 1440`, browser zoom
`100%`, sidebar open, custom black toolbar visible.

This case exists because a normal human can send text in ChatGPT reliably with
simple visible operations. Codex must not turn this into a complex automation
problem. For ChatGPT text-only official-site work, the default route is the
ordinary visible route below. Do not replace it with DOM, CDP, browser takeover,
debug APIs, window-message paste/send, or hidden controls.

Validated ordinary route:

```text
if generation is still running:
  click the visible stop button once
  wait until the composer is usable

click New Chat
wait for the clean composer
screenshot-confirm clean or repair before counting the run
click composer input at sidebar_open x=1175 y=751
Ctrl+A
Backspace
paste exactly one prompt with Ctrl+V
screenshot-confirm the intended prompt is visible
press Enter to send
wait for answer completion
screenshot-confirm the expected answer or validation marker
```

Important: pressing Enter after screenshot-confirmed text is preferred for this
state. It avoids small send-arrow drift when the composer height changes. Fixed
send-arrow coordinates are less robust than Enter for text-only work.

Observed coordinates in this state:

```text
New Chat row: x=60 y=203
sidebar_open composer input: x=1175 y=751
safe send arrow when single-line prompt is visible: about x=1768 y=751
```

Use the send-arrow coordinate only after a fresh screenshot proves the visible
arrow is actually there. For text-only runs, prefer Enter.

Observed proof runs:

```text
Simple text calibrated run:
  prompt: What is the capital of France? Answer briefly.
  route: New Chat -> clear composer -> paste -> screenshot -> Enter -> wait -> screenshot
  result: 10/10 PASS
  observed success probability in this state: 100% (10/10)
  evidence:
${REDACTED_SECRET}

Complex short-answer calibrated run:
  prompt type: Chinese complex decision analysis, bounded to 8 short points plus marker
  route: same ordinary route
  result: R02-R11 = 10/10 PASS
  observed success probability in this state: 100% (10/10)
  evidence:
${REDACTED_SECRET}
```

Known failure samples from the same session:

```text
1. Clicked send at y=730 instead of the visible arrow around y=751.
   Result: prompt remained in the composer. The input box was large enough to
   survive coordinate drift; the small send arrow was not.

2. Tried an unrestricted long complex answer with only a 45 second wait.
   Result: the prompt sent, but the result screenshot still showed generation
   in progress and no final marker. This is not a full PASS.

3. After stopping a previous long generation, counted the next run without a
   clean-composer screenshot gate.
   Result: first complex-short round did not start clean. R02-R11 passed after
   the normal state stabilized.
```

Rules created from the failures:

```text
Do not count a run until the clean composer is screenshot-confirmed.
Do not trust a scaled screenshot preview for coordinates; use real desktop
coordinates or visible Enter sending.
Do not use a small send-arrow coordinate when Enter can send text.
Do not use long-answer marker tests for quick transport validation unless the
workflow includes a completion wait, down-arrow/bottom jump, and marker proof.
If a prior generation was stopped, treat the next clean-composer screenshot as
mandatory and do not count the first post-stop action until it passes the gate.
```

Abnormal-state interpretation rule:

```text
Most visible ChatGPT "abnormal" states are not true blockers. Treat them as
ordinary state-normalization work unless the screenshot proves login, captcha,
account/security, network outage, or service outage.

Examples of repairable states:
  page not open -> open chatgpt.com
  old conversation visible -> click New Chat
  composer contains old text -> Ctrl+A, Backspace
  long answer still generating -> click visible stop, then clean-start gate
  page visually stale or focus broken -> refresh once, then clean-start gate
  wrong tab or old chat selected -> select ChatGPT tab or open a new one
  send arrow coordinate drift -> use Enter after prompt screenshot gate

These are not reasons to abandon the ordinary coordinate route. They are
branches inside the route. Only after the ordinary repair branches fail with
screenshot evidence should the method be marked failed.
```

Acceptance standard:

```text
PASS for text transport requires:
  prompt visibly present before send
  sent prompt visible in conversation
  answer visible
  expected answer or unique marker visible

For quick reliability checks, use bounded answers. For long answers, use the
long-answer bottom-jump/copy protocol instead of a short fixed wait.
```
