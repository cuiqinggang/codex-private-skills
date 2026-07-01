# 任务元数据 Schema v1.0

```json
{
  "task_id": "UF-TASK-001",
  "created": "2026-06-16T23:00:00Z",
  "question_hash": "md5 of original question",
  "complexity": "MEDIUM",
  "risk_level": "LOW",
  "domain": "general",
  "executor": "hermes-agent | codex-cli | gpt-web",
  "run_count": 1,
    "fusion_mode": "core_2_bootstrap",
  "fusion_mode_options": ["core_2_bootstrap", "core_3_default", "core_3_plus_qwen_ablation", "restricted_single_model"],
  "search_fact_pool": {
    "enabled": true,
    "search_required": true,
    "search_reason": [],
    "queries": [],
    "sources": [],
    "unresolved_items": [],
    "search_limit_reached": false
  },

}
```
