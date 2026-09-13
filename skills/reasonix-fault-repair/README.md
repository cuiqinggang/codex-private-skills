# Reasonix 故障诊断与成熟修复

统一入口：`skills/reasonix-fault-repair`

当前收录两类已验证成熟案例：

1. `cases/empty-session-race.md`：新建零消息会话 hydration/ready 竞态，已有前端最小补丁并完成运行验收。
2. `cases/startup-readiness-timeout.md`：启动 `startup_timeout/startup_failed`，后端已 Ready 但 Shell/Renderer readiness 误判；本次属于 transient cold-start anomaly，两次冷启动恢复，未打代码补丁。

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
