# Usage Log

## 2026-07-05

- Task: transcribe WeChat video `6593f5b04aefe433128294692c6f4aef.mp4`.
- Route: FFmpeg audio extraction -> whisper.cpp base-q8_0 CPU -> TXT/SRT/JSON.
- Result: completed full 5m02s transcript.
- Timing: CPU full run about 860 seconds.
- GPU: CUDA package installed and detected RTX 2080 Ti; short smoke test worked but had high overhead.
- Lesson: default to audio transcription, keep GPU/CPU auto selection, use frame extraction only for explicit on-screen text tasks.

