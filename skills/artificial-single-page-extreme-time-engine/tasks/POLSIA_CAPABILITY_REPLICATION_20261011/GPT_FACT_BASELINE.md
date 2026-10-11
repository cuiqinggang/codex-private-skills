# Polsia 成熟参照：GPT 独立事实基线（供 Codex 与下一页复用）
TASK_ID=POLSIA_CAPABILITY_REPLICATION_20261011
SOURCE_CHECK_DATE=2026-10-11
AUTHOR=GPT
RESULT=RESEARCH_BASELINE_ONLY
FINAL_VALID=NO

## 事实核验
- 本次截图标题声称“估值20亿”，未说明货币；2026年公开报道融资3000万美元、估值2.5亿美元，折人民币约18亿元。绝不能改写为估值20亿美元。
- Polsia 官网 https://polsia.com/：声称规划路线图、写代码、投放广告、回客服、签销售、发社媒；属于产品公开声称，不等于所有能力通过独立验收。
- 官方 pitch deck https://polsia.com/deck：工程、冷外联、Meta广告、研究、bug监控、客服、支付、社媒。称 Agents 报错→工程 Agent 修复→基础设施自监控自愈；同时宣称80%自治。这里80%系公司自述而非独立测量。
- WSJ 2026-07 报道：单人创始人 Ben Broca、约1万付费客户、全年收入目标约1000万美元，AI处理邮件、代码/调试、客服、订阅、退款。报道同样指出一些客户账号上模型费用高于收入，说明高自治不等于极限成本或盈利。
- 历史研究日期 2026-05-28：本地已存在 C:\Users\A\.codex\skills\one-person-ai-company-success-routes\references\CASE-008-Polsia-Zero-Employee-Company.md；及其 ROUTE-MATRIX.md、CASES.md、REPLAY-METHOD.md；过去记录公开主页/前端 JS/公共仪表盘/API 路由等源证据，数据较早应按日期隔离。历史文件对创始人姓名有 Ben Cera/Ben Broca 混杂，以本次官方 pitch deck 的 Ben Broca 为优先，不直接覆盖历史原件。
- 本机克隆/录制技能 C:\AI\record-and-replay-evaluation\SKILL.md；GitHub main skills/operation-demo-to-skill/SKILL.md（第3版）；skills/mature-outcome-automation/SKILL.md。record-and-replay 能录操作事件并抽象为可执行技能，但不能仅凭网站 UI 恢复第三方闭源后端。
- 当前29版 methods: skills/artificial-single-page-extreme-time-engine/ENGINE_V29_DRAFT.md 基本流程 Freeze=ENGINE29-BASIC-F001，完整公共总纲尚为28版；禁止把候选29版写成已发布或完成实测。

## 已有成熟方案应优先核验
- n8n 官方 Error Trigger + Error Workflow, failed execution retry: https://docs.n8n.io/build/flow-logic/handle-errors-gracefully ；https://docs.n8n.io/workflows/executions/all-executions/ 。已有第三方社区自动重试模板 https://n8n.io/workflows/3144-auto-retry-engine-error-recovery-workflow/ ，须审计其认证、安全与幂等机制，不直接用于真实付款/邮件/广告。
- Temporal 官方 Durable Execution：https://docs.temporal.io/ai ；长期状态保持、崩溃自动恢复、审批等待。仅在现成 n8n 和 GitHub 持久状态不满足证明的真实需求时才考虑引入，避免重造/增大成本。
- 用户本地既有一人公司案例库包含 CASE-008 Polsia、CASE-015 Ploy/Webflow、OpenPolsia（当时仅 WATCH），以及 MetaGPT/ChatDev/LangGraph 等索引。优先重读原证据，不重新调研同一旧问题。

## 应复刻的运行语义
公司目标→按能力选现有成熟 Agent/技能→授权任务合同→持久执行记录→可重放完成判定→对普通故障自动分类、查GOOD/BAD首差分、最小成熟恢复→任务续跑→有效成果→经验回写。
高风险动作（支付、广告、真人邮件、账户变更）保留人工审批。Exactly-once=幂等键/执行回执确认，不能对已可能提交成功的写动作盲目重试。

## 必须分开的四种结果
1. 产品已公开声称；2. 第三方证实；3. 本地真实测试通过；4. 生产自主执行通过。
用户当前要求针对3形成真实可复现证据；4不得未经授权假设已达成。
时间一律 X分Y秒Z毫秒，缺真实始末日志则 T_VALID_REAL=UNKNOWN。
