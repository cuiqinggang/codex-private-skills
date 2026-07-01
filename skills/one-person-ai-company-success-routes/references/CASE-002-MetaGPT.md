# CASE-002 - MetaGPT

## 项目定位

MetaGPT 是“软件公司多角色流水线”的经典路线：把自然语言需求拆成 PM、Architect、Engineer、QA 等角色和结构化中间产物。它对一人 AI 公司最重要的启发不是安装框架，而是将“成功软件公司 SOP”固化为可复用 agent 协议。

## 证据

- 本地源码：`H:\AI\_explore\one-person-ai-company-success-routes-20260528\sources\repos\MetaGPT`。
- Git HEAD：`11cdf466d042aece04fc6cfd13b28e1a70341b1f`，提交时间 `2026-01-21T18:12:32+08:00`。
- License：`LICENSE` 为 MIT。
- 角色文件：`metagpt\roles\product_manager.py`, `architect.py`, `engineer.py`, `qa_engineer.py`, `project_manager.py`。
- 测试/验证痕迹：`tests\metagpt\test_team.py`, `tests\metagpt\test_software_company.py`, `tests\metagpt\utils\test_cost_manager.py`, `tests\mock\mock_llm.py`。
- 本轮验证方式：只读源码和 mock/test 文件，不安装依赖、不调用 LLM。

## 核心机制

- SOP 化：把“需求 -> PRD -> 设计 -> 代码 -> 测试/评审”的流程变成角色链和文档链。
- 角色分工：Product Manager 产出需求/PRD，Architect 产出架构，Engineer 产出代码，QA/Reviewer 评估输出。
- 中间产物：每一步有可检查的文档或代码结果，降低一次性端到端幻觉。
- Team/Role/Action：将 agent 行为拆成可审查单元，适合映射到技能包模板。
- Mock 测试：源码中存在 mock LLM 和大量测试，说明项目承认 LLM 结果需要隔离验证。

## 成熟经验

1. 一人 AI 公司不能只靠“一个强 agent 连续做完所有事”。应拆成 SOP、角色和产物。
2. 角色要输出可被下一角色消费的结构化文档，而不是自由聊天记录。
3. 流水线每一步都要允许人类检查，否则多 agent 链式幻觉会被放大。
4. 成本和 token 统计应成为运行报告的一部分，而不是事后估算。

## 风险

- 运行真实 MetaGPT 需要模型 API key 和依赖安装，本轮不运行。
- 软件开发 SOP 很适合代码任务，但直接迁移到内容、私域、视频生产时会过重。
- 多角色越多，错误传播面越大；必须引入审批门和中间产物验证。

## 映射到 ECC / Codex / Claude-style 12 层流程

| MetaGPT 机制 | 本地映射 |
|---|---|
| SOP | ECC canonical 的阶段化流程和昨日重现步骤 |
| PM/Architect/Engineer/QA | Codex 规划、架构、实现、验证四席位 |
| 中间产物 | `reports/`, `case-studies/`, `templates/` 中的可审查文件 |
| mock_llm/test | 本地 mock replay 和无真实 API key 验证 |
| cost/token | 运行报告中的成本/时间/风险字段 |

## 是否进入技能包

进入。吸收“SOP + 中间产物 + 角色分工 + mock 验证”，不吸收“直接安装并运行完整 MetaGPT 做业务”的重路线。
