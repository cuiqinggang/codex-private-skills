---
name: hermes-windows-native-screen-capture
description: Provide Windows native desktop screenshot capture for Hermes / Ai Ma Shi using windows-capture / Windows Graphics Capture. Use when Hermes needs a real Windows desktop or Chrome GPU-rendered window PNG, white-screen analysis, or a reusable capture_router.py screenshot channel without clicking, messaging, account actions, or safety bypasses.
---

# Hermes Windows Native Screen Capture

## Purpose

Use this skill to give Hermes / Ai Ma Shi a Windows native screenshot channel.
The default backend is `windows-capture`, which uses Windows Graphics Capture.

Use the scripts in this skill when Hermes needs to capture the current Windows
desktop and pass the resulting PNG path to a multimodal model for recognition.

## Verified Evidence

Baseline proof:

```text
H:\AI\workspaces\HERMES-WINDOWS-CAPTURE-MINIMAL-PROOF-20260530
```

Status code:

```text
HERMES_WINDOWS_CAPTURE_MINIMAL_PROOF_PASS
```

Verified results from the proof:

- `windows-capture` installed successfully.
- WGC capture succeeded.
- Screenshot dimensions: `3840x2160`.
- Screenshot file size: `5,101,697` bytes.
- White pixel ratio: `16.49%`.
- Suspected white screen: `False`.
- The PNG showed the real desktop and current Chrome GPU-rendered page.
- `dxcam` was not needed for the proof run.

## Boundaries

- Only capture screenshots.
- Do not click, type, move the mouse, or automate UI actions.
- Do not send WeChat, Telegram, browser, or other account messages.
- Do not operate accounts, credentials, payments, or security prompts.
- Do not bypass platform or application safety mechanisms.
- Do not use `pyautogui` or `mss` as the default capture channel.
- Do not install `dxcam` automatically.

## Recommended Hermes Integration

Call:

```powershell
python H:\AI\skills\hermes-windows-native-screen-capture\scripts\capture_router.py
```

Read the returned JSON. If `ok` is `true`, use `image_path` as the screenshot
artifact and pass that PNG to the multimodal model. Treat `analysis` as the
minimum quality gate before model recognition.

## Script Map

- `scripts/capture_router.py`: Stable Hermes entrypoint. Defaults to
  `windows-capture`, analyzes the PNG, and returns unified JSON.
- `scripts/capture_wgc_once.py`: Single-frame Windows Graphics Capture helper.
- `scripts/analyze_capture.py`: PNG existence, size, dimensions, brightness,
  and white-screen analysis.
- `scripts/test_chrome_capture.py`: Uses the current open desktop/Chrome state,
  captures through the router, analyzes the PNG, and writes
  `reports/chrome-capture-test.md`.
- `tests/verify_skill.py`: Runs the verification flow and writes
  `reports/verification-result.md`.

## Operational Notes

The public `--monitor-index` API uses `0` for "primary/auto". With
`windows-capture` 2.0.0 on the proof machine, the effective native monitor index
must be greater than zero, so the helper maps requested `0` to effective `1`.

