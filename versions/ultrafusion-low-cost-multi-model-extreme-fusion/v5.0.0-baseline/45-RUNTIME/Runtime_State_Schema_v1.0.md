# 运行时状态 Schema v1.0

```json
{
  "run_id": "UF-20260616-001",
  "question": "用户原始问题",
  "v15": {
    "version": "v15",
    "sha256": "abc123...",
    "guard_present": true
  },
  "models": {
    "GPT": {"status": "PASS", "contributions": 8},
    "DeepSeek": {"status": "PASS", "contributions": 12},
    "MiniMax": {"status": "PASS", "contributions": 5}
  },
  "layers": {
    "A": {"status": "COMPLETE", "v15_injected": true, "models": 3},
    "B": {"status": "COMPLETE", "v15_injected": true, "models": 3},
    "C": {"status": "COMPLETE", "v15_injected": true},
    "D": {"status": "COMPLETE", "v15_injected": true}
  },
  "final_score": 92,
  "deductions": [],
  "hard_failures": []
}
```
