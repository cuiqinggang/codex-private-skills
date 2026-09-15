# Reasonix 故障诊断与成熟修复

统一入口：`skills/reasonix-fault-repair`

版本：`1.1.0`

当前收录两类已验证成熟案例与一类历史间歇观察：

1. `cases/empty-session-race.md`：新建零消息会话 hydration/ready 竞态，已有前端最小补丁并完成运行验收。
2. `cases/startup-readiness-timeout.md`：启动 `startup_timeout/startup_failed`，后端已 Ready 但 Shell/Renderer readiness 误判；本次属于 transient cold-start anomaly，两次冷启动恢复，未打代码补丁。
3. `cases/react185-transcript-geometry-loop.md`：历史间歇 React #185；当前 v1.38.7 M build A-I 9/9 PASS，未复现，保留 TranscriptProjectionView geometry feedback 静态候选，不打补丁。

历史兼容技能：

```text
skills/reasonix-empty-session-race-repair
```

保留不删除，避免原有调用路径失效。以后优先从新的统一入口检索 Reasonix 故障。

推荐顺序：

```text
SKILL.md
→ DECISION-TREE.md
→ 对应 cases/*.md
→ RECURRENCE-RUNBOOK.md
→ ACCEPTANCE.md
```

核心原则：先匹配成熟案例，先取证，再做最小修复；成功态恢复后不为理论优化扰动正常系统。

v1.1.0 已完整并入空会话案例的 GPT/Codex 分工、existing-owner 浏览器协作、hotfix 决策、PowerShell 保护性部署、`10/30/20/10/5` 运行验收和 Reasonix catalog 成功接入链。原独立技能 v1.0.0 保留为历史兼容入口。
