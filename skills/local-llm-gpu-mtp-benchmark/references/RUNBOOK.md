# Runbook

## Preflight

1. Confirm the user's model-size boundary and target use case.
2. Check `nvidia-smi` for GPU name, total/free VRAM, power state, and existing model process.
3. Check candidate GGUF file size against Hugging Face metadata when downloaded.
4. Confirm backend version:

```powershell
${REDACTED_SECRET}
```

5. Prefer official or reputable model repositories. Treat K drive as backup/reference unless the user explicitly asks to search it.

## Benchmark Order

1. Load baseline without speculative decoding.
2. Load MTP using `--spec-type draft-mtp --spec-default`.
3. Add `--spec-draft-p-min 0.5` and compare generation TPS plus output quality.
4. Test community MTP parameters only as short probes:
   - `--spec-draft-n-max 2`
   - `--spec-draft-n-max 4 --spec-draft-p-min 0.5`
   - `--spec-draft-n-max 16 --spec-draft-p-min 0.8`
   - KV cache variants `f16`, `q8_0`, `q4_0` when safe.
5. Test EAGLE/DFlash only if the exact draft model and backend support match. If official llama.cpp says `unknown model architecture`, record the failure and delete the failed draft model unless the user asks to keep it.

## Metrics

Always separate:

- model load time: process start to `/v1/models` ready
- TTFT: request sent to first streamed token
- generation speed: eval/completion tokens per second
- prompt processing speed: prompt eval tokens per second, not a substitute for generation speed
- Chinese output and JSON validity
- VRAM used/free

## Decision Gate

For this user:

- single-digit generation TPS: reject for daily use
- around 25-30 tok/s on a higher-quality 27B model: acceptable
- 50-80 tok/s claims require same hardware/model/backend proof before being used as a target
- keep a model only if it loads on GPU, responds normally, and improves either quality or privacy/cost enough to justify disk space

## Web Verification

When the user asks whether online speeds are reasonable, search current sources and record:

- GPU and VRAM
- dense vs MoE model
- quantization
- backend or fork
- CUDA/OS
- whether reported TPS is generation speed or prompt processing speed

Prefer primary sources: llama.cpp docs/releases, model cards, GitHub issues/releases, and detailed benchmark posts with command lines.
