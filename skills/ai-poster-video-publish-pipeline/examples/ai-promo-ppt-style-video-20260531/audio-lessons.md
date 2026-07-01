# Audio Lessons From The 2026-05-31 Run

## What Went Wrong

The first audio implementation created music procedurally with simple tones. It passed technical checks but failed the user taste check. The sound was too artificial, repetitive, and uncomfortable for a promo video.

## Prevention Rule

When the user asks for "悠扬", "轻音乐", "好听", "舒服", or references earlier acceptable videos, do not synthesize raw-tone music. Search existing local videos and audio files first.

## Search Targets

Useful locations from this run:

```text
H:\AI\workspaces
H:\AI\skills
H:\Hermes_Skills
C:\Users\A\Desktop\1\output
```

Useful command pattern:

```powershell
Get-ChildItem -LiteralPath <candidate-root> -Recurse -File -Filter '*.mp4' |
  ForEach-Object {
    $audio = ffprobe -v error -select_streams a -show_entries stream=codec_name,duration -of csv=p=0 $_.FullName 2>$null
    if ($audio) { $_.FullName }
  }
```

## Accepted Source In This Run

`H:\AI\workspaces\VIDEO-BASE-TRACK-RECONSTRUCTION-STAGE1-20260531\output\base_clean_candidate.mp4`

## Quality Gate

Technical PASS means:

- audio stream exists
- duration matches
- codec is AAC or similar
- volume is background-level

Taste PASS means:

- not harsh
- not monotonous
- not synthetic in a cheap way
- supports the video rather than drawing attention

If taste is uncertain, produce 2-3 candidate with-music MP4s using different existing tracks and ask the user to pick.
