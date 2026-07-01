# Polsia / 一人 AI 公司吸收建议

## 1. HiveWard 哪些机制应进入 Polsia？

应进入：

- Company 作为顶层业务容器。
- CEO 作为全局总控席位，但只负责解释、编排、提案和风险汇总，不绕过人类审批。
- Leader 作为每条业务线/收入路径的长期负责人。
- Blueprint 作为可视化业务流程，不直接等于真实执行。
- Inbox 作为所有变更、委派、发送、导入的审批门。
- Run / History 作为昨日重现、任务复盘、失败分析和路线升级的证据层。
- Runtime adapter 概念，用于未来接 OpenClaw、Codex、Hermes、ComfyUI，但先 mock。

不应进入：

- 自动更新、自行安装、真实发送、直接读取 OpenClaw/Hermes 生产配置。
- 未验证的 Beta harness 生产接入。

## 2. CrewAI 哪些机制应进入 Polsia？

应进入：

- Agent / Task / Crew 的对象结构。
- sequential process 作为默认安全流程。
- hierarchical manager 作为后续 Manager 节点参考。
- Flow 的事件驱动表达，用于审批、重试、失败恢复。
- logs/traces/token usage 字段，进入每次运行报告。

不应进入：

- 直接依赖 CrewAI Control Plane 或云账号。
- 为每个小任务创建复杂 Crew。

## 3. AutoGen / LangGraph 哪些机制应进入 Polsia？

AutoGen 应进入：

- AgentChat/Teams 的对话编排思想。
- AgentTool：把专长 agent 封装成可审计工具。
- Studio：可视化调试和原型操作参考。
- Bench：路线评估和 replay/eval 概念。

LangGraph 应进入：

- durable execution。
- persistence/checkpoint。
- interrupt/human-in-the-loop。
- memory 分层。
- streaming events。
- failure recovery。

暂缓：

- 直接把 Polsia 控制台重写为 LangGraph 应用。
- 直接采用 AutoGen 作为新项目核心，因为 README 已标明 maintenance mode，应观察 Microsoft Agent Framework。

## 4. n8n / Dify 哪些 UI 和流程应进入 Polsia？

应进入：

- 可视化画布用于展示流程、节点状态、审批状态、历史记录。
- 节点类型：Agent、Tool/API、Human Approval、Memory、Report、ComfyUI Production、OpenClaw/Codex/Hermes Worker。
- Credential 管理只显示“缺失/已配置/需审批”，不显示明文。
- Workflow import/export，导入后默认进入 mock replay。
- Workflow history/run history，绑定每次输出、失败、审批、人工备注。
- 模板库/WATCHLIST，用于吸收外部 workflow 或路线。

## 5. 哪些东西不应进入，避免臃肿？

- 不内置所有第三方连接器。
- 不实现完整 SaaS 账号/权限/计费系统。
- 不复制 n8n/Dify/Flowise 的完整 UI。
- 不让 agent 自动管理真实支付、广告投放、外发消息。
- 不把所有项目都安装到本地。
- 不把“公司职位”过度拟人化；只保留职责、输入、输出、审批。

## 6. 最小可行版本应该做什么？

MVP 只做控制台原型和技能包规则：

1. Route intake：录入外部项目/案例。
2. Candidate matrix：ABSORB / REPLAY / WATCH / REJECT。
3. Case study：固定模板记录问题、机制、证据、风险、映射。
4. Blueprint mock：用文本/YAML 表达 Company -> Leader -> Blueprint -> Agent/Tool/Human Approval。
5. Run report：记录 mock replay 的输入、输出、审批、失败、下一步。
6. Skill sync：把成熟机制写回 H:\AI\skills。

## 7. 下一阶段是否应该只做控制台原型，不做真实接入？

是。下一阶段应只做控制台原型，不做真实接入。

理由：

- 当前最大价值是吸收成功路线和建立治理结构，不是跑真实 agent。
- 真实接入会触碰 OpenClaw/Hermes/New API/ComfyUI/发送渠道等生产边界。
- 控制台原型足以验证信息架构、审批门、run history、WATCHLIST 和路线矩阵。
- 只有当 mock replay 连续稳定后，才可逐个申请真实执行体接入。

推荐下一阶段状态码：`POLSIA_CONTROL_PANEL_MOCK_PROTOTYPE_RECOMMENDED`。

## 8. 2026-05-28 POSA / Polsia 零员工公司资料追加

用户截图中的 `POSA` 资料已核对并追加为 `CASE-008 Polsia / POSA 零员工 AI 公司模式`。公开证据显示它更可能对应 `Polsia`，而不是一个独立的 POSA 项目。

新增吸收建议：

- 把 Polsia 的 `company object + AI employee + task/run/report + public live dashboard` 当作控制台原型参考。
- 把 domain/payment/ad/outreach 都作为能力节点显示，但默认只进入审批门和 mock replay。
- 把订阅、run-now credit、extra company price 等机制转成本地预算/算力/时间额度门。
- 把 `80/20` 原则写入治理：AI 做标准化执行，人类保留品味、定位、价值观、付款、发送、投放、法律和融资判断。

新增禁止项：

- 不登录真实账号。
- 不创建账号。
- 不触发真实支付、域名购买、广告投放、邮件发送或投资人外联。
- 不把平台自报 ARR/MRR 当作独立验证事实。

追加状态码：`ONE_PERSON_AI_COMPANY_ROUTES_POSA_POLSIA_INTAKE_PASS`。
