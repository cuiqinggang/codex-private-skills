# Codex 全局接收门禁 — first-principles v4.0.0

> 本门禁 supersedes 旧 first-principles v3.x 的“三核心第四字段”规则；其他无关 Agent/技能规则不受影响。

任何来自 GPT/用户、要求执行实际工作的 first-principles 正式命令，必须包含：

```text
【页面名｜任务名｜序号｜阶段】
```

第四字段只允许：

```text
虚拟成熟
实际验证
```

缺失任一字段、第四字段不是上述两个值之一、正文实际工作与阶段冲突：

```text
PHASE_GATE=BLOCKED
ACTION=STOP
```

Codex / Reasonix / 本地执行器：
- 只执行冻结合同；
- 不得自行修复、重新设计、改变路线；
- 实际验证失败只记录 Reality Delta；
- 然后 STOP 并返回 GPT 虚拟成熟。

如果存在合法标签，最终汇报最后一行原样回显同一标签。
