$ErrorActionPreference = 'Stop'

$root = 'H:\AI\workspaces\AI-PROMO-PPT-STYLE-VIDEO-20260531'
$sourceVideo = 'H:\AI\workspaces\VIDEO-BASE-TRACK-RECONSTRUCTION-STAGE1-20260531\output\base_clean_candidate.mp4'
$silentVideo = "$root\renders\ai_promo_ppt_style_video_1080x1920.mp4"
$audioOut = "$root\audio\existing_music_from_prior_base_clean_candidate.m4a"
$videoOut = "$root\renders\ai_promo_ppt_style_video_1080x1920_with_music.mp4"

New-Item -ItemType Directory -Force -Path "$root\audio", "$root\reports" | Out-Null

ffmpeg -y -i $sourceVideo -vn `
  -af "atrim=0:17.733333,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.8,afade=t=out:st=16.7:d=1.0,volume=0.30" `
  -c:a aac -b:a 128k $audioOut

ffmpeg -y -i $silentVideo -i $audioOut `
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a copy -shortest $videoOut

ffprobe -v error -print_format json -show_streams -show_format $videoOut |
  Set-Content -LiteralPath "$root\reports\existing-music-ffprobe-report.json" -Encoding UTF8

ffmpeg -hide_banner -i $videoOut -af volumedetect -f null NUL 2>&1 |
  Select-String -Pattern 'mean_volume|max_volume' |
  Set-Content -LiteralPath "$root\reports\audio-volume-check.txt" -Encoding UTF8
