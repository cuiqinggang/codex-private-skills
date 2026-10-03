# 收费转免费·开源替代技能包｜更新策略 v1.0

```ini
SKILL_VERSION=1.0.0
CATALOG_VERSION=2026-10-03-R1
LAST_VERIFIED=2026-10-03
```

## 更新触发

1. **关键迁移前强制复核**：任何生产级替换在执行前即时检查当前许可证、维护状态、版本、安全公告和平台支持。
2. **动态项目优先复核**：OpenCut、RapidRAW、Cal.diy、Webstudio、n8n、NocoDB、开放核心项目每次重大使用前都要重新查。
3. **目录定期刷新**：建议每月做一次轻量刷新；发现重大 license change / archive / security advisory 时立即更新。

## 健康检查字段

每个候选最少维护：
- `last_verified`
- `license_class`
- `license`
- `active_or_archived`
- `latest_release_or_activity`
- `platforms`
- `agent_interfaces`（API/CLI/MCP/Headless/SDK/GUI）
- `critical_gaps`
- `security_notes`
- `source_urls`

## 自动升降级

- 项目归档、重大安全问题长期未修、许可不再满足目标、关键 DONE_WHEN Reality 失败：**降级/移出默认**。
- W 项目稳定、接口兑现、代表性 Reality PASS：可升 B/A。
- 不能确认许可证时：不得写“开源”；先降到 `LICENSE_UNVERIFIED`。
- 商业软件仍是唯一 VALID 路线时：明确保留收费软件，不人为降低 DONE_WHEN。

## Agent 可操作性

默认评分：
- A = API / CLI / Headless / MCP 可直接调用；
- B = SDK/插件/脚本或稳定 GUI 自动化；
- C = 主要人工 GUI。

同等有效时优先 A，以降低长期 T_VALID 和人肉操作。
