# G11 Xiaolongxia Free Pool Two-layer Strategy

## Current Production Layer - Keep Unchanged

The current production route remains the reduced OpenRouter pool:

- Primary: `xiaolongxia-free/liquid/lfm-2.5-1.2b-instruct:free`
- Formal backups: `xiaolongxia-free/openai/gpt-oss-120b:free`, `xiaolongxia-free/openai/gpt-oss-20b:free`
- Final fallback: `xiaolongxia-free/openrouter/free`

Do not replace this production route with NVIDIA yet.

## Candidate Layer - NVIDIA NIM

NVIDIA NIM is now a candidate provider because G07 connectivity passed and G08 found marker-pass models.

A class NVIDIA candidates from G08/G09:

- `meta/llama-3.1-8b-instruct`
- `nvidia/nemotron-3-super-120b-a12b`
- `meta/llama-3.1-70b-instruct`

These models can be used for local dry-run only. They are not connected to real group chats and do not replace production primary.

## Why Not Directly Overwrite Production

- The NVIDIA key used here was previously exposed in chat and should be rotated before formal integration.
- G08 only checked marker behavior, not Chinese Q&A quality, Xiaolongxia style, stability, budget, or rate limits.
- Production OpenRouter reduced pool is already working and has rollback evidence.
- NVIDIA availability, model ids, and quota behavior can change.

## Upgrade Path From Candidate To Formal Backup

A NVIDIA model can become formal backup only after:

1. Same model passes marker tests in 3 consecutive rounds.
2. At least one Chinese Q&A test passes.
3. At least one Xiaolongxia-style short reply test passes.
4. No 401 / 403 / 404.
5. 429 is not severe.
6. Average latency is acceptable.
7. No key leak in reports/logs.
8. Rollback plan exists and is tested.

## Next Minimal Action

Use the candidate config only in a local dry-run adapter test. Do not attach real group chat.
