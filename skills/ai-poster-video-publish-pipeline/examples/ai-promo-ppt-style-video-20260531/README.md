# AI Promo PPT-Style Video Case, 2026-05-31

## Purpose

This example records a real run where five existing images were turned into a vertical PPT-style AI promotional video. The important lesson is audio: the first music attempt used crude procedural synthesis and was rejected. The corrected version reused an existing soundtrack from a prior local video.

## Source Workspace

`H:\AI\workspaces\AI-PROMO-PPT-STYLE-VIDEO-20260531`

## Original Image Assets

${REDACTED_SECRET}

The images were copied into the workspace before processing. Original images were not modified.

## Skill Reused

`H:\AI\skills\ai-poster-video-publish-pipeline`

The base skill provided the stable slideshow route and verification discipline. The task added PPT-style Chinese overlays and a corrected audio workflow.

## Final Outputs From The Run

- `H:\AI\workspaces\AI-PROMO-PPT-STYLE-VIDEO-20260531\renders\ai_promo_ppt_style_video_1080x1920.mp4`
- `H:\AI\workspaces\AI-PROMO-PPT-STYLE-VIDEO-20260531\renders\ai_promo_ppt_style_video_1080x1920_with_music.mp4`
- `H:\AI\workspaces\AI-PROMO-PPT-STYLE-VIDEO-20260531\previews\contact_sheet.jpg`
- `H:\AI\workspaces\AI-PROMO-PPT-STYLE-VIDEO-20260531\reports\final-report.md`
- `H:\AI\workspaces\AI-PROMO-PPT-STYLE-VIDEO-20260531\reports\existing-music-ffprobe-report.json`

## Audio Correction

Rejected route:

- Generated music locally with Python oscillator logic.
- It technically produced valid AAC after muxing.
- It sounded monotonous and uncomfortable.

Accepted route:

- Extracted existing audio from `H:\AI\workspaces\VIDEO-BASE-TRACK-RECONSTRUCTION-STAGE1-20260531\output\base_clean_candidate.mp4`.
- Trimmed it to `17.733333` seconds.
- Added fade in/out.
- Lowered volume to background level.
- Muxed it with the silent visual MP4.

Verification:

- final MP4 had video stream `h264`
- final MP4 had audio stream `aac`
- duration was about `17.733s`
- `volumedetect`: mean volume about `-24.4 dB`, max volume about `-10.9 dB`

## Reuse Command

See `run-example.ps1`.

## Lessons

1. For short PPT-style promo videos, visual quality alone is not enough.
2. If the user says prior videos had acceptable music, search prior local videos or audio files first.
3. Do not use crude procedural music as a default.
4. Keep the silent visual MP4 and the final with-music MP4 separately.
5. Save audio source, mux command, ffprobe report, and volume check in the run report.
