# XIAOLONGXIA-NVIDIA-NIM-G08-G09-CANDIDATE-20260523 Final Report

## Final Status

`XIAOLONGXIA_NVIDIA_NIM_CANDIDATE_CONFIG_PASS`

## 1. G07 Connectivity

G07 minimum connectivity had already passed:

- Status: `NVIDIA_NIM_G07_CONNECT_PASS`
- Base URL: `https://integrate.api.nvidia.com/v1`
- Endpoint: `/chat/completions`
- Baseline model: `meta/llama-3.1-8b-instruct`
- HTTP: 200
- Conclusion: NVIDIA NIM OpenAI-compatible path is usable.

PowerShell displayed Chinese text as mojibake in the G07 terminal output. This is treated as a display-layer issue, not an API connectivity failure.

## 2. G08 Marker Results

Status: `G08_PASS_NVIDIA_MARKER_CANDIDATE_FOUND`

Marker passed:

- `meta/llama-3.1-8b-instruct` -> `NVIDIA_LLAMA31_8B_OK`, HTTP 200, about 1652 ms
- `nvidia/nemotron-3-super-120b-a12b` -> `NVIDIA_NEMOTRON_SUPER_OK`, HTTP 200, about 3195 ms
- `meta/llama-3.1-70b-instruct` -> `NVIDIA_LLAMA31_70B_OK`, HTTP 200, about 10272 ms

Marker failed / unavailable:

- `moonshotai/kimi-k2.5` -> HTTP 404
- `minimaxai/minimax-m2.5` -> HTTP 410
- `z-ai/glm5` -> HTTP 410

Evidence files:

- `G08-nvidia-marker-tests.md`
- `G08-nvidia-marker-tests.json`

## 3. G09 A/B/C Ranking

A class candidates:

- `meta/llama-3.1-8b-instruct`
- `nvidia/nemotron-3-super-120b-a12b`
- `meta/llama-3.1-70b-instruct`

B class observation:

- None in this run.

C class not recommended now:

- `moonshotai/kimi-k2.5`
- `minimaxai/minimax-m2.5`
- `z-ai/glm5`

Recommended primary candidate: `meta/llama-3.1-8b-instruct`.

Recommended fallback candidates: `nvidia/nemotron-3-super-120b-a12b`, `meta/llama-3.1-70b-instruct`.

## 4. G10 Candidate Provider Config

Status: `G10_PASS_NVIDIA_CANDIDATE_CONFIG_READY`

Generated candidate config directory:

`C:\Users\A\Desktop\1\output\XIAOLONGXIA-NVIDIA-NIM-G08-G09-CANDIDATE-20260523\candidate-config`

Files:

- `nvidia-provider-candidate.json`
- `nvidia-provider-candidate-notes.md`
- `nvidia-openclaw-rollback.md`

The config uses provider id `nvidia`, base URL `https://integrate.api.nvidia.com/v1`, and key placeholder `${NVIDIA_API_KEY}`. It does not contain the raw key.

Only A class models are included in the candidate provider config.

## 5. Production Config

Production config was not modified.

Current production remains the OpenRouter reduced pool:

- Primary: `xiaolongxia-free/liquid/lfm-2.5-1.2b-instruct:free`
- Backups: `xiaolongxia-free/openai/gpt-oss-120b:free`, `xiaolongxia-free/openai/gpt-oss-20b:free`
- Final fallback: `xiaolongxia-free/openrouter/free`

NVIDIA is only a candidate provider for local dry-run.

## 6. Key Handling

- The user previously exposed the NVIDIA API key in chat. Treat that key as temporary.
- No full key was printed in reports.
- No full key was saved in candidate config.
- No global long-term environment variable was written.
- No production config was changed.
- Before formal provider integration, rotate the NVIDIA key and use only the rotated key.

## 7. Skill Update

Status: `G12_PASS_SKILL_UPDATED`

Updated skill:

`C:\Users\A\.codex\skills\xiaolongxia-free-provider-expansion`

Synced to:

`H:\CodexSkills\xiaolongxia-free-provider-expansion`

Hash check: local and H drive mirror match.

## 8. Next Minimal Action

Run a local dry-run only, still without real group chat:

1. Use rotated NVIDIA key.
2. Re-run marker tests for A class models.
3. Add one Chinese Q&A test.
4. Add one Xiaolongxia-style short reply test.
5. Only after 3 consecutive marker-pass rounds consider promotion from candidate provider to formal backup.
