# Model Sources

## Default

`ggml-base-q8_0.bin`

- Primary source: `https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base-q8_0.bin`
- Mirror source used successfully on 2026-07-05:
  `https://hf-mirror.com/ggerganov/whisper.cpp/resolve/main/ggml-base-q8_0.bin`
- SHA1: `7BB89BB49ED6955013B166F1B6A6C04584A20FBE`

## Rules

- Prefer multilingual models for Chinese.
- Do not use `.en` models for Chinese videos.
- Verify SHA before transcribing.
- If a larger model is needed, add it here with source URL, expected size, and hash.
- If a download is interrupted or partial, delete it and retry from another source.

