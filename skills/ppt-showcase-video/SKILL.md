---
name: ppt-showcase-video
description: "Use when creating or updating PPT-style image showcase videos for Douyin, WeChat Moments, short-video posting, AI drawing promotion, learning-material ads, or image collection displays. Covers vertical 9:16 big-image layouts, stable no-shake slide transitions, background music selection/reuse, ffmpeg verification, and saving reusable source materials."
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
- Output naming: include style in the filename, for example `*_ÊúÆÁ´óÍ¼ÇáÒôÀÖ°æ.mp4`.

## Quick Workflow

1. Locate source images and inspect dimensions.
2. Choose vertical output unless the user explicitly asks for horizontal.
3. Reuse the bundled light music asset when the user accepts it:
   `assets/calm-piano-background-music-free-orange-free-sounds.mp3`.
4. Run `scripts/make_vertical_big_ppt_video.py` with image folder, output path, and optional audio path.
5. Verify with `ffprobe`:
   - video stream is `1080x1920`
   - audio stream exists
   - duration is expected
6. Extract one representative frame and inspect it. The image should appear large on a phone screen.

## Script

Use the script directly:

```powershell
python "C:\Users\A\.codex\skills\ppt-showcase-video\scripts\make_vertical_big_ppt_video.py" `
  --images "C:\path\to\images" `
  --output "C:\Users\A\Desktop\Õ¹Ê¾ÊÓÆµ_ÊúÆÁ´óÍ¼ÇáÒôÀÖ°æ.mp4"
```

Optional arguments:

- `--audio`: MP3/WAV/M4A music file. Defaults to the bundled calm piano asset.
- `--workdir`: intermediate slide directory. Defaults to a temp folder.
- `--seconds-per-slide`: default `4.0`.
- `--fade-seconds`: default `0.6`.
- `--crf`: default `18`.

## Music Guidance

Do not synthesize simple generated tones for the user unless explicitly asked. For this user's accepted style, use complete light music with a soft opening.

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

Read [references/ai-beauty-vertical-case.md](references/ai-beauty-vertical-case.md) when recreating the exact successful example or when the user says "use the previous successful video flow".

The accepted visual reference is:

```text
assets/example-vertical-big-frame.jpg
```

## Verification Commands

```powershell
$ffprobe = "C:\Users\A\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffprobe.exe"
& $ffprobe -v error -show_entries format=duration,size:stream=index,codec_type,codec_name,width,height,avg_frame_rate -of default=noprint_wrappers=1 "C:\path\to\video.mp4"
```

For audio volume:

```powershell
$ffmpeg = "C:\Users\A\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
& $ffmpeg -hide_banner -i "C:\path\to\video.mp4" -filter:a volumedetect -f null NUL 2>&1 | Select-String -Pattern "mean_volume|max_volume"
```

