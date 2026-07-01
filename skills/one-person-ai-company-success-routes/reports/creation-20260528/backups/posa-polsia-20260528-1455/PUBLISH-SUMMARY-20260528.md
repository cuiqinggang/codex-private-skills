# 一人 AI 公司成功路线技能包成果发布版 - 2026-05-28

## 这次成果保存在哪里

最终技能包保存在：

```text
H:\AI\skills\one-person-ai-company-success-routes
```

调研过程、源码快照、证据和工作日志保存在：

```text
H:\AI\_explore\one-person-ai-company-success-routes-20260528
```

已经登记回 AI 公司主技能包：

```text
H:\AI\skills\ai-company-evolving-revenue-portfolio
```

主技能包登记文件：

```text
H:\AI\skills\ai-company-evolving-revenue-portfolio\ONE_PERSON_AI_COMPANY_SUCCESS_ROUTES_INDEX_20260528.md
```

## 一句话成果

这次不是只研究 HiveWard，也不是安装一堆项目，而是把“一人 AI 公司 / Agent Company OS / 多 Agent 软件公司 / 可视化 AI 工作流 / AgentOps”这些外部路线整理成一个可长期更新、可安全复盘、可吸收进本地体系的技能包。

最终状态码：

```text
ONE_PERSON_AI_COMPANY_SUCCESS_ROUTES_CONTINUOUS_SKILL_PASS
```

## 最重要的成果文件

| 文件 | 用途 |
|---|---|
| `SKILL.md` | 技能包入口。以后遇到一人 AI 公司、多 Agent 公司、外部成功路线吸收任务，先读它。 |
| `README.md` | 普通阅读入口，说明这个技能包是什么、怎么用、多久更新。 |
| `RUNBOOK.md` | 实际运行手册，说明一次标准搜索、判断、吸收、同步怎么做。 |
| `ROUTE-MATRIX.md` | 候选路线矩阵，记录 30+ 个项目/案例的类型、价值、风险、推荐动作。 |
| `WATCHLIST.md` | 长期观察列表，后续每 2 天、7 天、30 天更新都从这里开始。 |
| `CASES.md` | 7 个深度案例的索引。 |
| `SOURCE-OF-TRUTH-MAP.md` | 来源证据地图，说明哪些内容来自本地 clone、raw README、公开文档。 |
| `ABSORPTION-RULES.md` | 判断 ABSORB / REPLAY / WATCH / REJECT 的规则。 |
| `REPLAY-METHOD.md` | 昨日重现法的安全验证流程。 |
| `GOVERNANCE.md` | 审批门、安全边界、密钥和真实发送规则。 |
| `CONTINUOUS-UPDATE-RUNBOOK.md` | 长期持续更新流程。 |
| `UPDATE-CADENCE.md` | 2 天轻量更新、7 天周复盘、30 天月度重评估。 |
| `CHANGELOG.md` | 每次更新记录。 |
| `reports\creation-20260528\final-report.md` | 本轮完整最终报告。 |

## 这次实际研究了哪些方向

### 1. 公司组织型 Agent OS

代表对象：HiveWard、Polsia / OpenPolsia、one-person AI company、AI company operating system、agent company。

核心吸收：

- Company：公司级业务容器。
- CEO：公司总控席位，负责全局理解、风险、审批和调度。
- Leader：每条业务线或蓝图的长期负责人。
- Blueprint：业务流程图或任务 DAG。
- Inbox：所有正式变更、委派、发送、导入都必须进入审批。
- Run / History：每次运行都要能复盘和昨日重现。

结论：HiveWard 进入 CASE-001，但它只是案例之一，不是唯一路线。

### 2. 软件公司模拟型

代表对象：MetaGPT、ChatDev、AgileCoder、AutoAgents。

核心吸收：

- SOP 化：需求、产品、架构、实现、测试、复盘分阶段。
- PM / Architect / Engineer / QA 的角色分工。
- 中间产物必须可检查，不能只看最终回答。
- 多 agent 链式幻觉风险必须用人工审核、测试、日志和 replay 降低。

结论：吸收 MetaGPT/ChatDev 的成熟流水线，不直接运行完整项目做业务。

### 3. 多 Agent 编排框架型

代表对象：CrewAI、AutoGen、LangGraph、AG2、Agency Swarm。

核心吸收：

- CrewAI：Agent / Task / Crew / Process / Flow。
- AutoGen：AgentChat / Teams / Studio / Bench / human-in-the-loop。
- LangGraph：durable execution、persistence、interrupt、memory、streaming、failure recovery。

结论：先吸收工程机制和治理语言，不急着把本地体系重写成某个框架。

### 4. 可视化 AI 工作流型

代表对象：n8n、Dify、Flowise、LangFlow、Activepieces。

核心吸收：

- 可视化画布。
- Agent node、Tool/API node、Human Approval node。
- credential status 只显示状态，不显示密钥。
- workflow history、import/export、模板库。
- human fallback 不能是临时补救，应该是一等节点或节点属性。

结论：这些最适合作为 Polsia / AICompany Dashboard 控制台原型参考。

### 5. 执行体 / 本地 Agent 型

代表对象：Codex Desktop、OpenClaw / 小龙虾、Hermes、Claude Code、OpenHands、Aider、ComfyUI。

核心吸收：

- 执行体应该被组织和审计，而不是直接失控执行。
- OpenClaw、Codex、Hermes、ComfyUI 更适合作为未来 worker/runtime。
- 本轮不接真实生产配置，不读真实密钥，不真实发送。

结论：先做控制台和 mock replay，后续再逐个申请真实接入。

### 6. AgentOps / 观察与安全型

代表对象：LangSmith、AgentOps、Langfuse、Phoenix、Opik、human-in-the-loop、audit log / run history。

核心吸收：

- trace、session、run、cost、token usage、score、eval、prompt version。
- 每次运行必须可审计、可复盘、可回滚。
- 失败不是结束，而是进入复盘和 route upgrade。

结论：这些字段应该进入未来 AICompany Dashboard 和每次周期报告。

## 7 个深度案例

| Case | 文件 | 结论 |
|---|---|---|
| CASE-001 HiveWard | `references\CASE-001-HiveWard.md` | 进入技能包，吸收 Company/CEO/Leader/Blueprint/Inbox/Run/History。 |
| CASE-002 MetaGPT | `references\CASE-002-MetaGPT.md` | 进入技能包，吸收 SOP、角色流水线、中间产物验证。 |
| CASE-003 ChatDev | `references\CASE-003-ChatDev.md` | 进入技能包，吸收虚拟软件公司、Phase/Role、log/replay、human reviewer。 |
| CASE-004 CrewAI | `references\CASE-004-CrewAI.md` | 进入技能包，吸收 Agent/Task/Crew/Process/Flow。 |
| CASE-005 AutoGen | `references\CASE-005-AutoGen.md` | 吸收 AgentChat/Teams/Studio/Bench，同时观察 successor 路线。 |
| CASE-006 LangGraph | `references\CASE-006-LangGraph.md` | 必须吸收 durable execution、HITL、memory、failure recovery。 |
| CASE-007 Visual AI Workflow | `references\CASE-007-Visual-AI-Workflow.md` | 吸收 n8n/Dify/Flowise/LangFlow/Activepieces 的控制台和工作流机制。 |

## 最有用的可复用机制

1. 外部项目先进入候选矩阵，不直接安装。
2. 每个路线必须判断 ABSORB / REPLAY / WATCH / REJECT。
3. REPLAY 只能 mock / read-only / demo。
4. Company / CEO / Leader / Blueprint 是一人 AI 公司控制台的核心骨架。
5. Inbox / Approval 是防止 agent 擅自行动的边界。
6. Run History / Audit Log 是昨日重现法的核心资产。
7. SOP / 中间产物验证可以减少多 agent 链式幻觉。
8. 可视化画布适合做“理解和审批”，不等于直接生产执行。
9. credential 管理只显示状态，不显示明文。
10. 持续更新比一次性总结更重要。

## 已经建立的长期运行机制

```text
每 2 天运行一次轻量更新
每 7 天运行一次中等深度复盘
每 30 天运行一次路线矩阵重评估
```

对应文件：

- `CONTINUOUS-UPDATE-RUNBOOK.md`
- `UPDATE-CADENCE.md`
- `WATCHLIST.md`
- `CHANGELOG.md`
- `DEPRECATION-RULES.md`
- `templates\PERIODIC-UPDATE-REPORT-TEMPLATE.md`
- `templates\NEW-ROUTE-INTAKE-TEMPLATE.md`
- `reports\periodic-updates\20260528-initial-light-update.md`

## 对 Polsia / AICompany Dashboard 的建议

下一阶段应该只做控制台原型，不做真实接入。

最小可行版本：

1. Route Intake：录入外部项目/案例。
2. Candidate Matrix：判断 ABSORB / REPLAY / WATCH / REJECT。
3. Case Study：固定模板沉淀证据和机制。
4. Blueprint Mock：Company -> Leader -> Blueprint -> Agent/Tool/Human Approval。
5. Run Report：记录输入、输出、审批、失败、下一步。
6. Skill Sync：把成熟机制写回 H:\AI\skills。

不要做：

- 不接真实微信、飞书、Telegram、邮件。
- 不接真实广告、支付、客户触达。
- 不改 Hermes、OpenClaw、小龙虾、New API 3011、Open WebUI 3000、ComfyUI、ECC 生产配置。
- 不复制 Polsia、n8n、Dify、HiveWard 的品牌或私有设计。

## 怎么继续用

如果以后要继续更新，优先打开：

```text
H:\AI\skills\one-person-ai-company-success-routes\WATCHLIST.md
H:\AI\skills\one-person-ai-company-success-routes\ROUTE-MATRIX.md
H:\AI\skills\one-person-ai-company-success-routes\CONTINUOUS-UPDATE-RUNBOOK.md
```

如果要新增一个外部路线，使用：

```text
H:\AI\skills\one-person-ai-company-success-routes\templates\NEW-ROUTE-INTAKE-TEMPLATE.md
```

如果要做深度分析，使用：

```text
H:\AI\skills\one-person-ai-company-success-routes\templates\CASE-STUDY-TEMPLATE.md
```

如果要同步到主技能包，先看：

```text
H:\AI\skills\ai-company-evolving-revenue-portfolio\ONE_PERSON_AI_COMPANY_SUCCESS_ROUTES_INDEX_20260528.md
```

## 安全结果

- 没有读取或打印真实 API key、token、密码。
- 没有修改生产配置。
- 没有真实发送消息。
- 没有自动创建 Windows 计划任务。
- GitHub 限流后没有保存明文 token，改用公开 raw README、浅克隆和本地证据。

## 发布结论

这个技能包现在已经可以作为“一人 AI 公司外部成功路线吸收系统”的发布版入口使用。它的价值不是某一个项目，而是一套持续发现、判断、mock replay、吸收、治理、复盘和同步到本地 AI 公司体系的机制。

