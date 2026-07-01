# Phone And WeChat Video Acceptance

Use when the output will be watched on a phone or sent through WeChat.

## Preferred Export

- MP4 container
- H.264 video
- AAC audio
- `yuv420p`
- `+faststart`
- portrait videos remain portrait

## Image Showcase Rule

For phone/WeChat slideshow videos:

- prefer full-screen 9:16 image crop
- no small landscape image card floating in large blurred background
- no white border unless specifically requested
- no progress dots unless specifically requested
- no shake
- no pan
- no zoom unless the user asks
- use only cross-fade for calm PPT-like transitions

## Common Failure

Symptom:

```text
Only music/audio plays; no picture.
```

Likely cause:

```text
HEVC or an incompatible video stream was copied through.
```

Repair:

```text
transcode video to H.264 + yuv420p, keep/mix AAC audio, verify with ffprobe and preview frame
```

## Hand-Off

Final answer should include:

- direct file link
- folder link
- short spec: duration, dimensions, video codec, audio status
- note if the file was re-encoded for phone/WeChat compatibility
