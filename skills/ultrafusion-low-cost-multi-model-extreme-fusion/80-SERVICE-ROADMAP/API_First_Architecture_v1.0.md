# API-First 架构 v1.0

## 设计原则
- 核心逻辑 = API
- 前端 = 任意调用方（Hermes / Codex / Web UI / CLI）
- 所有模型调用 = Provider Adapter 抽象

## 核心 API

```
POST /run
  body: { question, options? }
  response: { run_id, status }

GET /run/{run_id}/status

GET /run/{run_id}/D_Final

GET /run/{run_id}/artifacts
```
