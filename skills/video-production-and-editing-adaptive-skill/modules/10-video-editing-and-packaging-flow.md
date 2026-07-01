# Video Editing And Packaging Flow

Use for user-shot video, reference video, tutorial video, voiceover video,
material cleanup, AI-generated clip post-processing, subtitles, music, joins,
cuts, and export.

## Basic Flow

1. Probe input media.
2. Identify existing streams, duration, resolution, rotation, codec, and audio.
3. Choose the smallest transform:
   - trim
   - add or replace music
   - mix original audio and background music
   - resize or crop
   - transcode for compatibility
   - add subtitles
   - concatenate clips
4. Export to a new output folder.
5. Probe the output.
6. Extract one preview frame or contact sheet.
7. Report paths and checks.

## Music Mix Defaults

For soft background music:

- keep original audio if useful: `volume=0.75` to `0.90`
- background music: `volume=0.15` to `0.30`
- fade in: about `1.0` to `1.5` seconds
- fade out: about `1.0` to `1.5` seconds
- output audio: AAC

If the user says the music is too loud, lower background music first.

## Compatibility Defaults

For phone/WeChat delivery:

- video codec: H.264
- pixel format: `yuv420p`
- audio codec: AAC
- keep portrait dimensions when the source is portrait
- use `+faststart`

Avoid shipping HEVC-only outputs when the user expects broad playback. If a
file plays audio but no video, transcode the video stream to H.264.

## Preview Evidence

For each final video:

- `ffprobe` stream summary
- preview frame at 3-5 seconds, or contact sheet for longer edits
- final path

If visual verification is important, inspect the preview frame before final
reply.
