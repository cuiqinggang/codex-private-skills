# CASE-005 - AutoGen

## 项目定位

AutoGen 是 Microsoft Research 推动的多 Agent 应用框架，重点是 AgentChat、Core API、GroupChat/Teams、Human-in-the-loop、Studio。它对一人 AI 公司的价值是“把多 agent 对话、工具调用、人类协作和可视化调试放入统一开发模型”。

## 证据

- Raw README 快照：`H:\AI\_explore\one-person-ai-company-success-routes-20260528\sources\web\AutoGen-README.md`。
- 官方/源码 URL：`https://github.com/microsoft/autogen`，README raw URL `https://raw.githubusercontent.com/microsoft/autogen/main/README.md`。
- License：README 显示 code 为 MIT，docs 为 CC-BY-4.0。
- 关键 README 位置：`AutoGen-README.md:14-25` 显示 maintenance mode 与 Microsoft Agent Framework successor；`AutoGen-README.md:32-39` AgentChat/Studio 安装；`AutoGen-README.md:106-153` AgentTool 多 Agent；`AutoGen-README.md:156-167` Studio；`AutoGen-README.md:181-194` Core/AgentChat/Studio/Bench/Magentic-One。
- 本轮验证方式：raw README + 官方文档检索，不运行 Studio，不设置模型 key。

## 重点机制

- AgentChat：快速原型的 opinionated 多 agent 对话 API。
- Teams / GroupChat：多个 agents 通过协调协议完成任务。
- AgentTool：把一个 agent 包装成另一个 agent 可调用的工具，适合层级化组织。
- Human-in-the-loop：让人类作为协作者/审批者插入多 agent 过程。
- GraphFlow / Studio：可视化原型和调试路线值得吸收，但不能依赖云账号。
- AutoGen Bench：评估 agent 性能，提醒我们需要 replay/eval，而不是只看一次成功。

## 重要变化

README 明确提示 AutoGen 已进入 maintenance mode，新项目应关注 Microsoft Agent Framework。这不意味着 AutoGen 不值得研究，而是吸收其成熟模式，同时把“新项目直接重押 AutoGen”降级为 WATCH/迁移评估。

## 可吸收机制

| AutoGen 机制 | 本地吸收方式 |
|---|---|
| AgentChat | Codex/Hermes/OpenClaw 的会话式协作接口参考 |
| Teams/GroupChat | 多角色协作日志和发言顺序设计 |
| AgentTool | 把专长 agent 封装为可审计工具 |
| Studio | Polsia/AICompany Dashboard 的可视化调试参考 |
| Bench/evals | 周复盘和月度路线重评估指标 |
| Maintenance-mode warning | ROUTE-MATRIX 中加入 supersede/upgrade 状态 |

## 风险

- 维护模式意味着新项目需优先复查 Microsoft Agent Framework。
- Studio 原型可能给人“可视化已等于生产”的错觉，必须加审批和日志。
- 真运行涉及模型 key、浏览器/MCP 工具和外部资源，本轮不运行。

## 是否进入技能包

进入。吸收 AgentChat/Teams/HITL/Studio/Bench 的机制，同时把 AutoGen 本体标记为“吸收思想，观察继任路线”。
