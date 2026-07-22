# Audio Guide For PPT-Style Promo Videos

## Why This Guide Exists

The 2026-05-31 `AI_PROMO_PPT_STYLE_VIDEO_FROM_EXISTING_SKILL` run exposed an audio quality failure:

1. The first deliverable was visually acceptable but silent.
2. A locally synthesized "soft music" track was added with Python oscillators.
3. The user rejected it as unpleasant, monotonous, and not comfortable to hear.
4. The corrected version reused an existing audio track from a prior local video, trimmed it to the current duration, added fade in/out, lowered the volume, and muxed it into the MP4.

This failure is now part of the skill. For PPT-style promotional videos, audio quality is a first-class acceptance item, not an afterthought.

## Default Audio Rule

Do not generate crude music from raw sine waves, oscillator loops, or simple procedural tones for client-facing promo videos.

Prefer this order:

1. Reuse an existing local music track or prior approved video soundtrack that already sounds acceptable.
2. Use a known-good royalty-free or user-provided music file when available.
3. Use a mature music-generation or audio library route only if explicitly requested and verified by listening.
4. Leave the video silent only when the user asks for a silent version.

## Required Audio Checks

Every final "with music" MP4 must be checked for:

- has an audio stream: `ffprobe -select_streams a`
- duration matches the video within about 0.2 seconds
- uses a common codec such as AAC
- has fade in/out to avoid hard cuts
- volume is background-level, usually around `mean_volume -18 dB` to `-30 dB`
- not clipped, usually `max_volume` below about `-3 dB`
- subjective fit: calm, pleasant, non-repetitive enough, not harsh, not distracting

`volumedetect` only checks level. It cannot judge whether music is pleasant. Always treat listening or reuse of an already accepted track as the real quality gate.

## Reusing Existing Audio From A Prior Video

Use this pattern when a prior local video already has acceptable music:

```powershell
$sourceVideo = 'H:\AI\workspaces\VIDEO-BASE-TRACK-RECONSTRUCTION-STAGE1-20260531\output\base_clean_candidate.mp4'
$silentVideo = 'H:\AI\workspaces\AI-PROMO-PPT-STYLE-VIDEO-20260531\renders\ai_promo_ppt_style_video_1080x1920.mp4'
$audioOut = 'H:\AI\workspaces\AI-PROMO-PPT-STYLE-VIDEO-20260531\audio\existing_music_from_prior_base_clean_candidate.m4a'
$videoOut = 'H:\AI\workspaces\AI-PROMO-PPT-STYLE-VIDEO-20260531\renders\ai_promo_ppt_style_video_1080x1920_with_music.mp4'

ffmpeg -y -i $sourceVideo -vn `
  -af "atrim=0:17.733333,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.8,afade=t=out:st=16.7:d=1.0,volume=0.30" `
  -c:a aac -b:a 128k $audioOut

ffmpeg -y -i $silentVideo -i $audioOut `
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a copy -shortest $videoOut
```

Adjust `atrim`, fade-out start, and `volume` for the current video duration.

## Verification Commands

```powershell
ffprobe -v error -show_entries stream=index,codec_type,codec_name,duration -show_entries format=duration,size -of json <with_music.mp4>
ffmpeg -hide_banner -i <with_music.mp4> -af volumedetect -f null NUL 2>&1 | Select-String -Pattern 'mean_volume|max_volume'
```

## Failure Pattern To Avoid

Do not accept a track just because it is technically valid AAC and has safe volume. The failed track passed `ffprobe` and `volumedetect`, but still sounded bad. Technical audio validation must be combined with either:

- a known-good source track, or
- an explicit listening pass, or
- direct user approval when the music source is new.

## Recommended Final Outputs

Keep both versions:

- silent or base visual version: `renders\<name>.mp4`
- final audio version: `renders\<name>_with_music.mp4`
- extracted or source music: `audio\<source-name>.m4a`
- audio report: `reports\audio-validation.md` or `reports\<name>-ffprobe-report.json`
