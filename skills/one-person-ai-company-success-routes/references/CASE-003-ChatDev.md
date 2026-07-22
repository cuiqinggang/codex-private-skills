# CASE-003 - ChatDev

## 项目定位

ChatDev 是“虚拟软件公司”范式：CEO、CTO、Programmer、Reviewer 等角色通过 ChatChain/Phase/Role 协作，覆盖设计、编码、测试、文档。它提供了多 agent 公司协作的早期经典样本，也提供了日志、replay、人机交互和自定义链路的经验。

## 证据

- 本地源码：`H:\AI\_explore\one-person-ai-company-success-routes-20260528\sources\repos\ChatDev`。
- Git HEAD：`a6a5cda5560053136897aa44301eacc6c48d8168`，提交时间 `2026-05-27T20:41:13+08:00`。
- License：`LICENSE` 为 Apache-2.0。
- README：`README.md:23` 描述 ChatDev 1.0 虚拟软件公司；`README.md:75` Git mode；`README.md:80` Human-Agent-Interaction；`README.md:93` online log/replay。
- 新工作流文档：`docs\user_guide\en\workflow_authoring.md`, `execution_logic.md`, `nodes\human.md`, `modules\memory.md`。
- 运行/服务结构：`server\services\workflow_run_service.py`, `server\services\session_execution.py`, `runtime\node\executor\agent_executor.py`, `human_executor.py`。
- 本轮验证方式：只读源码、README、docs，不运行模型或服务。

## 核心机制

- 虚拟公司角色：用公司职位映射软件生命周期，便于一人理解和监督。
- ChatChain/Phase/Role：把协作流程分成阶段，每阶段定义角色和输入输出。
- 日志与 replay：早期就强调在线日志和回放，对“昨日重现法”直接有价值。
- Human-Agent-Interaction：人类 reviewer 可以介入，说明多 agent 公司不能完全无人监督。
- 新版 workflow authoring：通过 YAML 定义 agent/human/subgraph/loop 等节点，向可视化/可配置工作流演进。

## 可复用经验

1. “公司模拟”适合让复杂流程变得可解释，但不能把职位表当作真实管理层照搬。
2. ChatChain 的核心价值是阶段边界和可回放日志，而不是具体 CEO/CTO 名称。
3. Human reviewer 节点是防止链式幻觉扩散的关键。
4. Git mode 的思想可映射到 Codex：所有代码任务必须留下 diff、commit/rollback 线索。

## 风险

- 角色聊天如果缺乏结构化验收，会产出貌似完整但不可运行的软件。
- 早期“虚拟公司”叙事容易过拟人化，应转成职责、输入、输出、验收标准。
- 真运行需要模型 key、依赖和可能的浏览器/工具能力，本轮不启用。

## 映射到 ECC / Codex / Claude-style 12 层流程

| ChatDev 机制 | 本地映射 |
|---|---|
| ChatChain/Phase | ECC 的分层闸门、任务阶段、复盘层 |
| Role | 技能包中的职责席位，而不是人格化员工 |
| Online log/replay | `reports/periodic-updates/` 和 run history |
| Human reviewer | 审批门、发送前确认、Level 3 停止规则 |
| Git mode | Codex diff/log/rollback 纪律 |

## 是否进入技能包

进入。吸收“阶段化协作、replay/log、人机 reviewer、YAML 工作流结构”，不吸收“过度角色拟人化和无验证自动开发”。
