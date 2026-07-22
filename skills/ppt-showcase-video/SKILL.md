---
name: ppt-showcase-video
description: "Use when creating or updating PPT-style image showcase videos for Douyin, WeChat Moments, short-video posting, AI drawing promotion, learning-material ads, image collection displays, or raw-to-processed image sequences. Covers vertical 9:16 big-image layouts, category-contiguous image ordering, stable no-shake slide transitions, mature background music reuse, ffmpeg verification, and saving reusable source materials."
---

# PPT Showcase Video

Use this skill to turn image collections into simple, stable, social-platform-ready PPT-style videos.

## Default Style

Prefer the proven 2026-06-07 example:

- Canvas: `1080x1920` vertical 9:16 for Douyin and WeChat Moments.
- Layout: large image presentation, not a 16:9 video inside a vertical phone frame.
- Image treatment: fit most portrait images up to `1060x1888`; use a blurred cover background only as edge fill.
- Motion: no shake, no handheld movement, no zoom jitter. Use static slides with smooth crossfades.
- Timing: 8 images, `4.0s` each, `0.6s` crossfade, final duration about `27.8s`.
- Audio: use soft complete light music, not generated tones, not bird/environment sounds, not urgent beats.
- Output naming: include style in the filename, for example `*_竖屏大图轻音乐版.mp4`.

## Quick Workflow

1. Locate source images and inspect dimensions.
2. Classify every image by role before ordering: `raw/source`, `process/bridge`, or `processed/result`.
3. Keep each category contiguous. Default order: `raw/source group -> process/bridge group -> processed/result group`.
4. Honor explicit positional constraints such as "put this image last" before any automatic sort.
5. Generate a numbered, category-labeled contact sheet and visually inspect adjacency before rendering.
6. Choose vertical output unless the user explicitly asks for horizontal.
7. Reuse a complete user-approved music asset when available. Only fall back to another verified complete track when needed.
8. Reuse the bundled light music asset when it exists and the user accepts it:
   `assets/calm-piano-background-music-free-orange-free-sounds.mp3`.
9. Run `scripts/make_vertical_big_ppt_video.py` with image folder, output path, and optional audio path.
10. Verify with `ffprobe`:
   - video stream is `1080x1920`
   - audio stream exists
   - duration is expected
11. Extract one representative frame and inspect it. The image should appear large on a phone screen.

## Image Sequence Gate

For image sets that show an editing, generation, transformation, or manufacturing process:

- Do not sort only by filename, timestamp, face identity, or superficial story association.
- First identify the process role of each image.
- Keep same-role images together; do not interleave raw images with result variants.
- Use transition/portal/process images between raw sources and results.
- If the user supplies a new related result and says it belongs at the end, place it at the end of the result block.
- The numbered contact sheet is a blocking pre-render check. If category blocks are broken, do not render.

Failure review: [image-sequence-music-failure-review-20260720.md](references/image-sequence-music-failure-review-20260720.md).

Recent use: [RECENT-USE-LOG.md](references/RECENT-USE-LOG.md).

${REDACTED_SECRET}

## Script

Use the script directly:

```powershell
${REDACTED_SECRET}
  --images "C:\path\to\images" `
${REDACTED_SECRET}
```

Optional arguments:

- `--audio`: MP3/WAV/M4A music file. Defaults to the bundled calm piano asset.
- `--workdir`: intermediate slide directory. Defaults to a temp folder.
- `--seconds-per-slide`: default `4.0`.
- `--fade-seconds`: default `0.6`.
- `--crf`: default `18`.

## Music Guidance

Do not synthesize simple generated tones for the user unless explicitly asked. For this user's accepted style, use complete light music with a soft opening.

Music selection priority:

1. A complete track the user previously listened to and approved.
2. A complete locally available track with verified provenance/license and a matching mood.
3. A newly sourced complete track that can be reviewed.
4. Procedural/synthesized music only when the user explicitly requests it.

For simple happy showcase videos, prefer acoustic or natural-instrument character, a complete melodic phrase, and gentle rhythmic variation. Reject procedural electronic ticking, single-note loops, mechanical repetition, or music that sounds like a temporary technical test.

Bundled accepted music:

```text
assets/calm-piano-background-music-free-orange-free-sounds.mp3
Source: Orange Free Sounds, Calm piano background music free
Source URL: https://orangefreesounds.com/calm-piano-background-music-free/
License noted during the successful run: commercial use allowed, CC BY 4.0
Accepted use: soft light music for AI image showcase, no bird/environment intro.
```

If replacing music, avoid:

- urgent upbeat rock/pop loops
- bird sounds, water sounds, or ambient nature intros
- single-note or obvious generated repetition
- loud foreground music

Target audio check:

```text
mean_volume around -32 dB is acceptable for background music.
```

## Proven Case

Read references/ai-beauty-vertical-case.md [MIRROR_REFERENCE_OMITTED] when recreating the exact successful example or when the user says "use the previous successful video flow".

The accepted visual reference is:

```text
assets/example-vertical-big-frame.jpg
```

## Verification Commands

```powershell
${REDACTED_SECRET}
& $ffprobe -v error -show_entries format=duration,size:stream=index,codec_type,codec_name,width,height,avg_frame_rate -of default=noprint_wrappers=1 "C:\path\to\video.mp4"
```

For audio volume:

```powershell
${REDACTED_SECRET}
& $ffmpeg -hide_banner -i "C:\path\to\video.mp4" -filter:a volumedetect -f null NUL 2>&1 | Select-String -Pattern "mean_volume|max_volume"
```

