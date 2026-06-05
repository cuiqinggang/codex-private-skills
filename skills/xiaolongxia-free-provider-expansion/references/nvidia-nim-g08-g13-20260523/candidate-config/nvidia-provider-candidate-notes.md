# NVIDIA OpenClaw Candidate Provider Notes

- This is a candidate config only. It does not overwrite current OpenRouter production pool.
- Key source must be `NVIDIA_API_KEY` or a local SecretRef provider. Do not paste a raw key into OpenClaw config.
- Models included are only G08/G09 A class marker-pass models.
- B class models are not included in provider config.
- C class models are excluded.
- Before switching any real route, rerun marker tests with the rotated NVIDIA key.
- Before real group chat, run dry-run tests for Chinese Q&A, Xiaolongxia-style short replies, 429 handling, and fallback.
- If NVIDIA returns 429 or becomes unavailable, keep using the current reduced OpenRouter pool.

## Included Models

- `meta/llama-3.1-8b-instruct` - marker `NVIDIA_LLAMA31_8B_OK`, latency 1652 ms.
- `nvidia/nemotron-3-super-120b-a12b` - marker `NVIDIA_NEMOTRON_SUPER_OK`, latency 3195 ms.
- `meta/llama-3.1-70b-instruct` - marker `NVIDIA_LLAMA31_70B_OK`, latency 10272 ms.

## Excluded Models

- `moonshotai/kimi-k2.5` - class C, HTTP 404, error WebException.
- `minimaxai/minimax-m2.5` - class C, HTTP 410, error WebException.
- `z-ai/glm5` - class C, HTTP 410, error WebException.
