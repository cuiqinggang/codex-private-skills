# Codex 12 Layer Execution Evidence Return Template

```text
TASK_ID:
任务名称：
工作区路径：
使用的技能包：

Claude-style 12 Layer 执行摘要：

Layer 1 — Control Plane / Orchestrator
中文名：主控调度层
状态：
证据路径：

Layer 2 — Short Entry / Memory
中文名：短入口 / 项目记忆层
状态：
证据路径：

Layer 3 — Skills / Progressive Disclosure
中文名：技能按需加载 / 渐进加载层
状态：
证据路径：

Layer 4 — Planning / Work Decomposition
中文名：任务拆解层
状态：
证据路径：

Layer 5 — Subagents / Context Isolation
中文名：子智能体 / 上下文隔离层
状态：
证据路径：

Layer 6 — Execution Plane
中文名：执行平面
状态：
Execution Plane claims：
证据路径：

Layer 7 — Hooks / Lifecycle Triggers
中文名：生命周期钩子层
状态：
证据路径：

Layer 8 — Scripts / Deterministic Checks
中文名：脚本确定性检查层
状态：
输出摘要：
证据路径：

Layer 9 — Verification Plane
中文名：独立验证平面
状态：
acceptance / rejection：
证据路径：

Layer 10 — Repair Loop
中文名：返修循环层
状态：
repair 记录：
证据路径：

Layer 11 — Compact / Handoff
中文名：压缩交接层
状态：
摘要：
证据路径：

Layer 12 — Final Acceptance
中文名：最终验收层
状态：
final-acceptance.md 核心内容：
final-acceptance.json 核心内容：

最终状态码：
仍然存在的问题：
请求 GPT 最终验收：YES
```

硬规则：

```text
只返回文件夹路径 = FAIL。
只返回“已完成” = FAIL。
没有核心证据摘要 = FAIL。
```
