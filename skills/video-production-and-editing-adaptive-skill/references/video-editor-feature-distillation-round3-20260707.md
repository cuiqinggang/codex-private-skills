# Video Editor Feature Distillation Round 3

Date: 2026-07-07

## Status

Overall status: `JIANYING_GUI_SUBTITLE_PASS_EXPORT_SETTINGS_PASS_FINAL_EXPORT_UNVERIFIED`

This round continued from Round 2 and focused only on the unfinished Jianying
GUI items. Work stopped when the user said the page was laggy and asked to
package the completed work for continuation in a new page.

## Evidence

Evidence folder:

```text
${REDACTED_SECRET}
```

Important evidence files:

```text
jianying-subtitle-tab-click-label.png
jianying-manual-subtitle-entry.png
jianying-srt-import-result.png
jianying-srt-timeline-attempt.png
jianying-export-settings-window.png
jianying-export-trigger-round3.png
jianying-export-confirm-popup.png
```

## Completed In Round 3

### Stable UI Coordinate Lesson

The desktop uses a multi-monitor virtual screen. Full-screen screenshots are
8320x1629 and the virtual screen origin is:

```text
VirtualScreen logical: -3840,-189,8320x1629
```

For Jianying, avoid guessing from the cropped screenshot alone. Use the current
visible full-screen screenshot and account for the virtual origin before
clicking. In this run, the Jianying window was moved to approximately:

```text
logical x=80 y=80 width=1600 height=920
```

### Jianying Subtitle Tests

Passed without login/payment:

- Opened the subtitle tab.
- Observed `智能识别` with a visible monthly trial/usage hint. This is an AI
  quota boundary and was not consumed.
- Opened `新建字幕`.
- Confirmed manual subtitles are available.
- Confirmed local subtitle import supports:

```text
SRT, LRC, ASS
```

- Imported local `sample.srt`.
- Dragged imported SRT onto the timeline.
- Confirmed a subtitle track appeared above the video track.
- Confirmed the right-side subtitle text/style panel appeared.

Decision:

```text
local SRT/LRC/ASS import -> direct-use in Jianying, no-login PASS
automatic speech subtitle recognition -> boundary/reference only unless user approves using trial/quota
script route remains preferred for repeatable subtitles -> video-audio-transcription/Whisper + SRT + FFmpeg burn-in
```

### Jianying Export Tests

Passed without login/payment:

- Opened the export settings window titled `导出-7月7日`.
- Export settings showed local video export controls:
  - title
  - export path
  - video export enabled
  - resolution/original setting
  - format MP4
  - frame rate 30
  - video bitrate recommendation
  - audio export section
  - final `导出` button

Evidence:

```text
jianying-export-settings-window.png
```

Not fully completed:

- The final local export was clicked once, then a follow-up prompt/confirm
  window appeared.
- Work stopped before reading/confirming that prompt because the user asked to
  package the work for a new page.
- No Jianying-rendered MP4 was verified with ffprobe, so do not claim final
  export PASS yet.

Decision:

```text
export settings window -> no-login PASS
final local export -> UNVERIFIED_CONTINUE_NEXT_PAGE
```

## Current Feature Decisions

| Feature | Jianying status | Reusable route |
|---|---|---|
| Local video import | no-login PASS | direct-use or FFmpeg |
| Timeline placement | no-login PASS | direct-use for manual editing |
| Local SRT/LRC/ASS subtitle import | no-login PASS | direct-use; script route remains SRT/ASS + FFmpeg |
| Subtitle styling | visible panel PASS | direct-use for manual polish; script route ASS style |
| Auto subtitle recognition | visible but quota/AI boundary | do not consume without approval; prefer Whisper |
| Export settings | no-login PASS | direct-use possible |
| Final Jianying export | unverified | continue next page |
| Audio material library | visible; mixed cloud/download/member signals | reference only; use own assets/FFmpeg |
| Transitions/effects/templates | visible; mixed free/download/member signals | reference only; use FFmpeg/own templates |
| Digital human / AI packaging | not tested deeply | blocked until approval/login/quota boundary review |

## Next Page Continuation

Start here:

```text
${REDACTED_SECRET}
```

Then continue only the remaining Jianying GUI item:

1. Open or refocus the existing Jianying project.
2. Confirm SRT is still on the subtitle track.
3. Open export settings again if needed.
4. Read the follow-up prompt from `jianying-export-confirm-popup.png`.
5. If it is only a local export confirmation, continue export.
6. If it is login, publish, cloud, account, payment, member, AI point, or
   permission related, stop and record boundary.
7. If local export completes, locate the output MP4 and verify with ffprobe
   plus preview frame/contact sheet before claiming PASS.

