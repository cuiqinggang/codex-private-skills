# G10 NVIDIA Candidate Config Summary

Status: `G10_PASS_NVIDIA_CANDIDATE_CONFIG_READY`

## Files

- `candidate-config\nvidia-provider-candidate.json`
- `candidate-config\nvidia-provider-candidate-notes.md`
- `candidate-config\nvidia-openclaw-rollback.md`

## Rules Satisfied

- Candidate config exists.
- It uses provider id `nvidia`.
- Base URL is `https://integrate.api.nvidia.com/v1`.
- API style is OpenAI-compatible chat completions via `openai-completions`.
- API key is not embedded; config uses `${NVIDIA_API_KEY}` placeholder.
- Models included are A class marker-pass models only.
- Current OpenRouter production pool was not modified.

## A Class Models Included

- `meta/llama-3.1-8b-instruct`
- `nvidia/nemotron-3-super-120b-a12b`
- `meta/llama-3.1-70b-instruct`
