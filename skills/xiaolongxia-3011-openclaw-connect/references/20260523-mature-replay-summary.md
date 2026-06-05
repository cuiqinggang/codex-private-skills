# 2026-05-23 Mature Replay Summary

- Provider id: `xiaolongxia-free`
- API Base: `http://localhost:3011/v1`
- Gateway: `127.0.0.1:18789`
- Smoke marker: `XIAOLONGXIA_3011_MODEL_OK`
- Primary: `xiaolongxia-free/liquid/lfm-2.5-1.2b-instruct:free`
- Formal backups after per-model evidence: `openai/gpt-oss-120b:free`, `openai/gpt-oss-20b:free`
- Candidate only after per-model evidence: `baidu/cobuddy:free`
- Gemma status after per-model evidence: `UNAVAILABLE_OR_LIMITED` due 429
- Final fallback: `openrouter/free`
- OpenRouter free result: marker passed, final fallback only
- Fallback placement: Xiaolongxia application layer or message adapter
- Rate-limit placement: Xiaolongxia message adapter
- Real group chat entrance: not connected
- Evidence status: `XIAOLONGXIA_3011_MODEL_EVIDENCE_REDUCED_PASS`
