# Example: Add Soft Music And Export H.264

Use when a user gives a video and asks for beautiful soft music at low volume.

Pattern:

```powershell
ffmpeg -y `
  -i input.mp4 `
  -stream_loop -1 -i soft_music.mp3 `
  -filter_complex "[0:v]scale=720:1280:flags=lanczos,format=yuv420p[vout];[0:a]volume=0.85[a0];[1:a]atrim=0:DURATION,asetpts=PTS-STARTPTS,volume=0.22,afade=t=in:st=0:d=1.2,afade=t=out:st=OUTSTART:d=1.4[a1];[a0][a1]amix=inputs=2:duration=first:dropout_transition=0[aout]" `
  -map "[vout]" -map "[aout]" `
  -c:v libx264 -preset medium -crf 20 -profile:v high -pix_fmt yuv420p `
  -c:a aac -b:a 160k -movflags +faststart `
  output_h264.mp4
```

Replace:

- `DURATION` with the source duration
- `OUTSTART` with duration minus fade-out length
- scale with the original dimensions when appropriate

Always verify with:

```powershell
ffprobe -v error -show_entries format=duration,size:stream=index,codec_type,codec_name,width,height,r_frame_rate -of json output_h264.mp4
ffmpeg -y -ss 00:00:05 -i output_h264.mp4 -frames:v 1 -update 1 preview.jpg
```
