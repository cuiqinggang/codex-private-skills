---
name: local-llm-gpu-mtp-benchmark
description: Use when testing, optimizing, deploying, or cleaning up local Windows GPU GGUF LLMs, especially 14B-27B Qwen/Gemma models, llama.cpp CUDA, LM Studio/OpenAI-compatible servers, MTP/speculative decoding, DFlash/EAGLE draft models, Kilo Code local provider routing, startup latency, first-token latency, and keep/delete decisions after local model benchmarks.
---

# Local LLM GPU MTP Benchmark

## Core Rule

Use real local evidence first, then compare with current online/community reports. Do not judge a local model only by parameter size, and do not treat online 50-80 tok/s claims as comparable unless hardware, model type, quantization, backend, and metric definition match.

## Workflow

1. Read `references/RUNBOOK.md` before changing model files, llama.cpp, Kilo, Hermes, or cleanup state.
2. Check GPU, free VRAM, model file size, backend version, and current `llama-server.exe` owner.
3. Respect the user's size boundary. For the 2026-07 baseline, skip 7B/8B as too low quality and skip 30B/32B as too large; focus on 14B-27B.
4. Run a no-spec baseline, then MTP/speculative variants, then any community method that can be verified safely.
5. Separate prompt-processing speed from generation speed. Use generation/eval/completion TPS for usability.
6. Measure startup load time, first-token latency, total response time, and characters per second, not only tok/s.
7. If integrating with Kilo, keep OpenRouter DeepSeek V4 Pro as default unless the user explicitly asks to switch default. Add local 27B as an optional provider/model.
8. Preserve results into this skill or a report, then delete failed draft models, failed fork downloads, and temporary benchmark work folders.

## Known Good Baseline

Read `references/RESULTS-20260706.md` when the user asks whether the current 27B route is usable, why online speeds differ, or what to keep.

Known good local service:

```powershell
${REDACTED_SECRET}
${REDACTED_SECRET}
  --host 127.0.0.1 --port 1234 `
  --ctx-size 4096 `
  --gpu-layers all --main-gpu 0 `
  --flash-attn on `
  --cache-type-k f16 --cache-type-v f16 `
  --jinja --reasoning off --no-warmup `
  -np 1 -b 2048 -ub 1024 `
  --alias qwen3.6-27b-iq4-xs-mtp `
  --spec-type draft-mtp --spec-default `
  --spec-draft-p-min 0.5
```

## Scripts

- `scripts/start-qwen27b-mtp.ps1`: start the verified 27B MTP server on `127.0.0.1:1234`.
- `scripts/stop-local-llm.ps1`: stop local `llama-server.exe` processes.
- `scripts/check-local-llm.ps1`: check `/v1/models`, GPU memory, and process owner.
- `scripts/latency-probe.py`: stream a short request and report first-token latency, total time, characters per second, and preview.

## Cleanup

Read `references/CLEANUP-POLICY.md` before deleting anything. Keep verified main models and user-facing reports. Delete failed or non-useful draft models only after recording why they failed.

## Kilo

Read `references/KILO-INTEGRATION.md` before changing Kilo. Preferred route: keep DeepSeek V4 Pro default, add `lmstudio/qwen3.6-27b-iq4-xs-mtp` or an equivalent OpenAI-compatible local provider as a selectable local model.

## Recent Use

Append every completed local benchmark or cleanup to `references/recent-use-log.md` with date, model, backend, fastest verified generation speed, keep/delete decision, and report path.
