# CLAUDE-STYLE-12-LAYER-REPLICA-RULE

本文件是 12 Layer 复刻规则。简洁核心思想以 `CLAUDE-STYLE-12-LAYER-COMPACT-CORE.md` 为准。

## 总规则

Claude-style 12 Layer 必须按原顺序复刻：

```text
1. Control Plane / Orchestrator：主控调度层
2. Short Entry / Memory：短入口 / 项目记忆层
3. Skills / Progressive Disclosure：技能按需加载 / 渐进加载层
4. Planning / Work Decomposition：任务拆解层
5. Subagents / Context Isolation：子智能体 / 上下文隔离层
6. Execution Plane：执行平面
7. Hooks / Lifecycle Triggers：生命周期钩子层
8. Scripts / Deterministic Checks：脚本确定性检查层
9. Verification Plane：独立验证平面
10. Repair Loop：返修循环层
11. Compact / Handoff：压缩交接层
12. Final Acceptance：最终验收层
```

## 禁止改写

- 不能改成普通 12 步。
- 不能改名、不能压缩、不能重解释。
- 不能使用“目标确认 / 现状读取 / 风险识别”等替代原始 12 层。
- 不能把 Execution Plane 的 claim 当成 acceptance。
- 不能把 final-report、execution summary、verification-result 或文件夹路径当 final acceptance。

## 必须继承的边界

- Execution Plane 只能 claim，不能 self-accept。
- Verification Plane 负责 acceptance / rejection。
- Repair Loop 处理 rejected claims。
- Final Acceptance 才是最终 PASS 权威。
- 没有 final acceptance，没有 final PASS。
- 只返回文件夹路径 = FAIL。

## 命令包格式

任何长任务命令包必须使用 `TASK-PACKAGE-MUST-CLONE-12-LAYER.md` 的固定格式。
