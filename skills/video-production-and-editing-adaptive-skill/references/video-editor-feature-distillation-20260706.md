# Video Editor Feature Distillation Evidence And Handoff

Date: 2026-07-06

Chinese trigger phrases:

- 剪映平替
- 剪映功能蒸馏
- CapCut 功能蒸馏
- Shotcut / Kdenlive 开源平替
- 自动剪辑能力沉淀
- 自动字幕 / 智能剪口播 / 去静音 / 视频导入测试
- 视频制作剪辑一体化

## Why This Lives In This Skill

The user decided that video production, editing, audio import, subtitles, and
editor feature distillation are one workflow family. This reference is now part
of the main `video-production-and-editing-adaptive-skill` package.

The temporary standalone skill
${REDACTED_SECRET}
source copy, but the durable entry point is this main video skill.

## Current Installed Editors

Verified by `winget list` on 2026-07-06:

| Editor | Package ID | Version | Role |
|---|---|---|---|
| 剪映专业版 | `ByteDance.JianyingPro` | `10.9.0.14199` | product reference + optional manual editor |
| Shotcut | `Meltytech.Shotcut` | `26.6.25` | lightweight open-source GUI editor |
| Kdenlive | `KDE.Kdenlive` | `26.04.2` | fuller open-source timeline editor |

Confirmed executable paths:

```text
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
```

## Evidence Folder

All evidence from this run was copied into the main skill:

```text
${REDACTED_SECRET}
```

Original working evidence remains at:

```text
${REDACTED_SECRET}
```

Important evidence files:

```text
stack-scan.json
stack-scan-after-kdenlive.json
feature-test\distillation-test-report.json
feature-test\sample_input.mp4
feature-test\sample_trimmed.mp4
feature-test\sample_vertical.mp4
feature-test\sample_subtitled.mp4
feature-test\cover.jpg
feature-test\contact_sheet.jpg
screenshots\shotcut-region.png
screenshots\kdenlive-initial.png
screenshots\kdenlive-main.png
screenshots\jianying-env-detector.png
screenshots\jianying-main.png
screenshots\jianying-editor-empty.png
screenshots\jianying-editor-no-tutorial.png
screenshots\jianying-import-dialog-after-clipboard-fail.png
screenshots\jianying-import-result.png
```

## What Was Actually Tested

### Script Distillation Test

Script:

```text
scripts\distill_common_video_features.py
```

Result:

```text
PASS
```

The script generated and verified free replacements for common editor
features:

- sample video generation
- trim/cut
- vertical video export
- cover frame extraction
- contact sheet generation
- SRT subtitle file
- subtitle burn-in
- ffprobe stream checks

This proves these Jianying/CapCut-style features should be distilled into
FFmpeg-based workflows rather than depending on a GUI editor.

### Stack Scan

Script:

```text
scripts\scan_video_editor_stack.py
```

Result:

```text
PASS
```

It detects:

- FFmpeg / ffprobe
- Python
- Auto-Editor
- PySceneDetect
- installed Jianying / Shotcut / Kdenlive packages
- feature decision buckets

Auto-Editor and PySceneDetect were installed with:

```text
python -m pip install --user auto-editor scenedetect
```

They installed successfully, but their `.exe` shims live under:

```text
${REDACTED_SECRET}
```

The scanner handles that path explicitly.

## Visual GUI Test Results

### Shotcut

Status: `DIRECT_USE_PASS`

Evidence:

```text
screenshots\shotcut-region.png
```

Findings:

- Shotcut opened successfully.
- The visible UI showed playback list, open file, export, filters, subtitles,
  timeline, keyframes, tasks, and editing panels.
- Use Shotcut directly for lightweight GUI editing and manual verification.
- Do not recreate Shotcut itself.

### Kdenlive

Status: `DIRECT_USE_PASS`

Evidence:

```text
screenshots\kdenlive-initial.png
screenshots\kdenlive-main.png
```

Findings:

- Initial setup page appeared.
- Safe "开始编辑" button was clicked.
- Main timeline opened successfully.
- UI showed project bin, monitors, V/A tracks, audio mixer, export, effects,
  and editing panels.
- Use Kdenlive directly for fuller open-source timeline editing.
- Do not recreate Kdenlive itself.

### Jianying / 剪映专业版

Status: `PARTIAL_DIRECT_USE_PASS_WITH_PAID_BOUNDARY`

Evidence:

```text
screenshots\jianying-env-detector.png
screenshots\jianying-main.png
screenshots\jianying-editor-empty.png
screenshots\jianying-editor-no-tutorial.png
screenshots\jianying-import-dialog-after-clipboard-fail.png
screenshots\jianying-import-result.png
```

Findings:

- Installed and launched.
- First visible gate was an SVIP/new-user promo.
- "立即开通" is a payment/member action and was not clicked.
- "放弃福利" was clicked to continue without login/payment.
- Main homepage opened without login.
- "开始创作" opened an editor project without login.
- Editor UI showed: 素材, 音频, 文本, 贴纸, 特效, 转场, 字幕, 智能包装,
  滤镜, 调节, 模板, 数字人.
- Import dialog opened successfully for local media.
- Import continuation was in progress when the user requested handoff. The last
  file to inspect is `screenshots\jianying-import-result.png`.

Important boundary:

- Do not log in in the first test round.
- Do not click payment, SVIP, publish, account, cloud, AI points, or security
  prompts without explicit user approval.
- Jianying is valuable as a product reference and manual tool, but script-
  friendly features should be distilled into free routes.

## Feature Map

| Feature | Preferred Route | Decision |
|---|---|---|
| Local import | Jianying/Shotcut/Kdenlive direct use | direct-use |
| Manual timeline polish | Shotcut/Kdenlive/Jianying | direct-use |
| Cut/trim/join | FFmpeg | script-distill |
| Auto subtitles | video-audio-transcription / whisper.cpp | script-distill |
| Subtitle burn-in | FFmpeg subtitles filter | script-distill |
| Silence removal / rough cut | Auto-Editor | script-distill |
| Scene detection | PySceneDetect | script-distill |
| Background music/fade | FFmpeg audio filters | script-distill |
| Vertical 9:16 social export | FFmpeg / ppt-showcase-video | script-distill |
| Cover extraction | FFmpeg frame extract | script-distill |
| Contact sheet QA | FFmpeg tile | script-distill |
| Templates/stickers/effects | own assets only; GUI for manual use | hybrid |
| Jianying paid/SVIP/AI features | product reference only unless user approves | do-not-copy |
| Digital human / account AI / cloud material | requires login/member boundary check | blocked-until-approved |

## Rule For Future Runs

When the user asks for video editing, automatic editing, subtitle, audio import,
Jianying replacement, or CapCut feature distillation:

1. Start from this main video skill.
2. Read `references/video-editor-feature-distillation-20260706.md`.
3. Run `scripts\scan_video_editor_stack.py` if the local stack status matters.
4. Use direct GUI editors only when manual timeline work is helpful.
5. Distill repeatable operations into script routes first.
6. For rendered outputs, always verify with ffprobe plus preview/contact sheet.

## Next-Page Continuation

If continuing in a new page:

1. Open this reference first.
2. Inspect `screenshots\jianying-import-result.png`.
3. Continue Jianying no-login test from the import dialog / imported media
   state.
4. Verify whether the test media imported into the media bin.
5. If imported, drag/drop or add to timeline only if safe.
6. Test which visible functions are free vs login/SVIP gated:
   - subtitles
   - text
   - audio
   - effects
   - transitions
   - export
7. Stop at login, payment, cloud, publish, or account prompts.

## Round 2 Continuation

On 2026-07-07, a second round expanded the script-distilled feature matrix from
the initial smoke test into 20 tested routes. Read this file next:

```text
${REDACTED_SECRET}
```

Round 2 evidence:

```text
${REDACTED_SECRET}
```

Round 2 status:

```text
SCRIPT_DISTILLATION_PASS_GUI_PARTIAL
```

Key update: FFmpeg/Auto-Editor/PySceneDetect routes now cover trim, join,
vertical/square export, cover, contact sheet QA, SRT burn-in, ASS title overlay,
fade, color adjustment, background music mix, loudness normalization, speed,
transition, silence removal, and scene detection. Jianying GUI passed no-login
local import, preview, and timeline placement, but subtitle tab and export
dialog still require a more stable GUI coordinate run before claiming PASS.

## Round 3 Continuation

On 2026-07-07, a third round completed more Jianying GUI testing. Read this file
next when continuing Jianying-specific work:

```text
${REDACTED_SECRET}
```

Round 3 evidence:

```text
${REDACTED_SECRET}
```

Round 3 status:

```text
JIANYING_GUI_SUBTITLE_PASS_EXPORT_SETTINGS_PASS_FINAL_EXPORT_UNVERIFIED
```

Key update: Jianying no-login local subtitle workflow is now tested: subtitle
tab, new subtitles, local `SRT/LRC/ASS` import, SRT import into media, drag to
timeline, and right-side subtitle styling panel all passed. Jianying export
settings window also opened without login and showed MP4 export controls. Final
export is still unverified because a follow-up prompt appeared and the user
asked to package the work for a new page before continuing.
