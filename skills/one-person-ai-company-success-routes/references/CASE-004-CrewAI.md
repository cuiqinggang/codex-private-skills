# CASE-004 - CrewAI

## 项目定位

CrewAI 是多 Agent 编排框架路线，核心是把 Agent、Task、Crew、Process、Flow 分层。对一人 AI 公司来说，它的价值是“把角色协作和生产流程拆成可配置对象”，同时提供更接近生产的 flow/control plane/observability 思路。

## 证据

- Raw README 快照：`H:\AI\_explore\one-person-ai-company-success-routes-20260528\sources\web\CrewAI-README.md`。
- 官方/源码 URL：`https://github.com/crewAIInc/crewAI`，README raw URL `https://raw.githubusercontent.com/crewAIInc/crewAI/main/README.md`。
- License：README 显示 MIT License。
- 关键 README 位置：`CrewAI-README.md:54-62` 多 Agent automation；`CrewAI-README.md:71-79` tracing/logs/control plane；`CrewAI-README.md:162-180` Crews 与 Flows；`CrewAI-README.md:329-375` Agent/Crew/Process/Task 示例；`CrewAI-README.md:432` hierarchical process/manager。
- 本轮验证方式：raw README + 官方文档检索，不安装 `crewai`，不设置 `.env`，不调用模型。

## 重点机制

- Crew：一组有共同目标的 agents。
- Agent：角色、目标、backstory、tool、model 等执行单元。
- Task：明确 description、expected output、agent owner、上下游依赖。
- Process：sequential 或 hierarchical；hierarchical 会引入 manager 进行委派和验证。
- Flow：更精确的事件驱动工作流，适合生产编排。
- Memory / callback / logs / token usage：应作为运行报告和成本控制的标准字段。
- Control Plane tracing：证明多 agent 系统必须可观测，而不是只看最终答案。

## 可吸收机制

| CrewAI 机制 | 本地吸收方式 |
|---|---|
| Agent/Task/Crew | 技能包模板中的角色、任务、团队字段 |
| Process.sequential | 默认安全流水线，适合初期 replay |
| Hierarchical manager | Polsia/HiveWard 控制台中的 Manager 节点原型 |
| Flow | 长流程/审批流程的状态机表达 |
| Tracing/logs | 运行报告、WATCHLIST 更新证据、token/时间记录 |
| Human review in task design | 审批门作为 task 级属性 |

## 风险

- 真实运行需要模型 key；本轮不运行。
- CrewAI 概念很容易诱导“为每个想法都建 crew”，会造成组织臃肿。
- Control Plane 可能涉及账号/云服务，应只吸收观测字段，不依赖 SaaS。

## 是否进入技能包

进入。直接吸收 Agent/Task/Crew/Process/Flow 的命名和结构，作为本技能包的 route evaluation 模型；暂缓真实安装和 control plane 接入。
