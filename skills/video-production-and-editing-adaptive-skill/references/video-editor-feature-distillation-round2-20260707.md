# Video Editor Feature Distillation Round 2

Date: 2026-07-07

## Status

Overall status: `SCRIPT_DISTILLATION_PASS_GUI_PARTIAL`

This round continued the Jianying/Shotcut/Kdenlive feature distillation work.
The main improvement is that common editor capabilities are now tested as a
20-item executable matrix, not only a small smoke test.

## Evidence

Evidence folder:

```text
${REDACTED_SECRET}
```

Important files:

```text
stack-scan-round2-fixed.json
feature-test\distillation-test-report.json
feature-test\sample_input.mp4
feature-test\sample_trimmed.mp4
feature-test\sample_joined.mp4
feature-test\sample_vertical_9x16.mp4
feature-test\sample_square.mp4
feature-test\sample_subtitled.mp4
feature-test\sample_fade_text.mp4
feature-test\sample_color_adjusted.mp4
feature-test\sample_background_music_mix.mp4
feature-test\sample_audio_normalized.mp4
feature-test\sample_speed_125.mp4
feature-test\sample_transition_xfade.mp4
feature-test\sample_silence_removed.mp4
feature-test\scene_detection\sample_scene_source-Scenes.csv
feature-test\scene_detection\sample_scene_source-Scene-*.jpg
jianying-import-sample-round2.png
jianying-timeline-round2.png
jianying-tab-audio-round2.png
jianying-tab-transitions-round2.png
```

## Script Changes

Updated:

```text
scripts\scan_video_editor_stack.py
scripts\distill_common_video_features.py
```

Scanner fixes:

- Added shorter timeouts around `winget list`.
- Use local executable paths as fallback when `winget` is slow or unavailable.
- Fixed PySceneDetect version probing from `--version` to `version`.
- Avoid false `manual GUI editing ready=false` when Shotcut/Kdenlive paths exist.

Distillation script expansion:

- The script now verifies 20 feature routes.
- It outputs JSON report, rendered media, preview frames, contact sheet, scene
  CSV/thumbnails, and ffprobe stream probes.
- It uses ASS subtitles for title overlays because FFmpeg `drawtext` can crash
  on this Windows setup when fontconfig has no default config.

## 20 Tested Script-Distilled Features

All 20 passed in this round:

| Source editor feature | Distilled route |
|---|---|
| Local media import/preview sample | FFmpeg synthetic H.264/AAC test asset |
| Trim/cut | FFmpeg `-ss` / `-t` |
| Multi-clip join | FFmpeg concat demuxer |
| Vertical social export | FFmpeg scale/pad to 1080x1920 H.264/AAC yuv420p |
| Square social export | FFmpeg crop/scale |
| Cover extraction | FFmpeg frame export |
| Contact sheet QA | FFmpeg fps/tile |
| SRT subtitle burn-in | FFmpeg subtitles/libass |
| Title text overlay | ASS overlay + FFmpeg subtitles filter |
| Fade in/out | FFmpeg fade/afade |
| Color adjustment | FFmpeg eq filter |
| Background music import/mix | FFmpeg amix/volume/afade |
| Loudness normalization | FFmpeg loudnorm |
| Speed change | FFmpeg setpts/atempo |
| Transition | FFmpeg xfade/acrossfade |
| Silence test asset | FFmpeg loud/silent/loud synthetic clip |
| Silence removal/rough cut | Auto-Editor audio detection |
| Scene test asset | FFmpeg hard-cut source |
| Scene detection | PySceneDetect detect-content/list-scenes/save-images |
| Stream verification | ffprobe JSON probes |

Verified examples:

- `sample_vertical_9x16.mp4`: H.264, 1080x1920, yuv420p.
- `sample_subtitled.mp4`: H.264, 1280x720, yuv420p.
- PySceneDetect produced 3 detected scenes, CSV, and 9 thumbnails.

## Jianying GUI Round 2

Status: `GUI_PARTIAL_PASS`

Passed without login/payment:

- Opened Jianying Professional 10.9.0.14199.
- Entered editor with no login.
- Imported local `sample_input.mp4`.
- Previewed imported media.
- Dragged media to the timeline.
- Confirmed visible editable timeline track and right-side clip parameter panel.
- Opened visible audio and transition/effect material panels.

Observed boundaries:

- Audio library shows downloadable/cloud-style assets and some badge markers.
  Treat as product reference/manual material selection, not a source to copy.
- Transition/effect panels show mixed free/download/member-style items.
  Distill generic transition behavior with FFmpeg `xfade`; do not copy assets.
- Top-right SVIP/member button remains visible; do not click.
- Login/account/cloud/publish/payment actions were not clicked.

Not completed in this round:

- Jianying subtitle panel was not reliably opened because the top tab click
  coordinates drifted during multi-window testing.
- Jianying export dialog was not reliably opened because multi-display focus
  made the visible export button miss.
- No final GUI export from Jianying was claimed.

## Decisions

| Feature family | Decision |
|---|---|
| Shotcut/Kdenlive manual editing | `direct-use` |
| Jianying local import/timeline preview | `direct-use` as optional manual editor |
| Jianying templates/stickers/effects/audio assets | `hybrid` or `do-not-copy`; use own assets |
| Repeatable editing/export/subtitle/audio operations | `script-distill` |
| Account/SVIP/AI/digital-human/cloud/publish features | `blocked-until-approved` or `do-not-copy` |

## Next Run Checklist

1. Start from this main video skill.
2. Run `scripts\scan_video_editor_stack.py`.
3. Run `scripts\distill_common_video_features.py --workdir <workdir>`.
4. For Jianying GUI continuation, begin from an active editor project with a
   clip already on the timeline.
5. Re-test only the unfinished GUI items:
   - subtitle tab and local/manual subtitle insertion
   - export dialog and local export settings
   - whether export requires login or SVIP
6. Stop at any login, payment, cloud, publish, account security, AI points, or
   member prompt.

