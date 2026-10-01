# 成熟方案竞争 R2｜FREE-FIRST｜极限短时间自动化闭环 v2.0

```ini
ROUND=R2
DATE=2026-10-01
STATE=10
PRODUCTION_COST_GATE=ZERO_PAID_DEPENDENCY
PAID_BENCHMARK=Manus 2.0
PRODUCTION_WINNER=NOT_YET_CERTIFIED
```

## 1. R2 改变了什么

R1 把 ChatGPT Work 与 Manus 2.0 都当成完整整解候选。

R2 加入正式生产硬约束后：
- ChatGPT Work：从生产候选移除。官方明确 Work 面向 eligible paid plans，Free / Go 不包含。
- Manus 2.0：从生产候选移除，只保留付费 Benchmark；用户已有积分可用于一次受控 Reality 对照。
- Microsoft Copilot Studio Computer Use：按 credit 计费，不进入免费生产候选。
- Zapier / n8n Cloud 付费方案：不进入免费主链。
- n8n Community Edition：保留为成熟免费组件。
- OpenClaw：提升为当前最重要的免费成熟整解候选。
- ChatGPT Free / Codex Free：保留为免费成熟智能 / 编码组件，而不是完整后台自动化整解。

## 2. 当前生产候选

### P1｜OpenClaw（主候选）

官方当前事实：
- OpenClaw 是 MIT 开源，无付费产品层；
- 本地运行，一个 Gateway，可接模型、渠道、工具、memory、skills、sessions；
- 有持久 Automations / scheduler；
- 有 Browser；
- 有 Computer Use；Windows 路径官方仍标 experimental，因此不能直接把 Windows Computer Use 当成熟已证实能力；
- 官方 Codex plugin 可使用 ChatGPT/Codex subscription auth；
- 当前仓库已存在 OpenClaw Windows 历史资产、18789 Gateway、boot replay、安全恢复以及免费模型池技能。

生产意义：
- 它最接近“免费完整壳层”；
- 不需要新造 orchestrator；
- 缺口可由已经存在的成熟免费组件补，而不是自研。

### P2｜OpenClaw + 成熟免费执行组件最小组合

仅在 P1 原生能力未达到 VALID 时启用：
- Browser：优先 OpenClaw 当前 Browser；若 Reality 证明特定任务不可靠，再竞争既有成熟 JEV-native / Playwright 路径；
- Coding：Codex Free（官方说明 Codex 包含于 Free / Go；Cloud 不包含）；
- Model：现有免费模型池 / 免费额度；
- deterministic automation：OpenClaw Automations；必要时 n8n Community Edition 仅作为成熟免费组件；
- GitHub：共同私库作为现实事实源。

这不是新架构开发，而是现有成熟能力最小组合。

## 3. Benchmark

### B1｜Manus 2.0

角色：
```ini
PRODUCTION=NO
BENCHMARK=YES
USE_EXISTING_CREDITS_ONLY=YES
```

同一个 Reality Task 测出：
`T_REF_MANUS`

以后每次攻击免费路径，只问：

> 免费成熟路径与成熟付费整解之间的时间差具体损失在哪里？

而不是复制 Manus 的实现。

## 4. 排除项

### ChatGPT Work
官方当前仅 eligible paid plans；因此即使能力很强，也不满足生产 FREE-FIRST VALID。

### Microsoft Copilot Studio Computer Use
官方按每个 Computer Use step 消耗 Copilot Credits；不满足零付费长期运行。

### Manus 2.0
Agent Mode 使用 credits。免费方案有 Lite / 每日额度，但用户已明确 Manus 不进入最终生产主链。

## 5. 当前最短实验顺序

```text
① 先跑 Manus 2.0 一次真实 Benchmark
   得到 T_REF_MANUS

② 对本机现有 OpenClaw 做只读现状核验
   不升级、不重构、不接新收费能力

③ 若现有版本明显落后当前稳定版且升级路径成熟，
   只做已有成熟升级流程

④ 用 OpenClaw + 免费模型 / Codex Free
   跑同一个 Reality Task

⑤ 比较：
   VALID
   T_REF_MANUS
   T_VALID_FREE
   GAP
   人工介入
   恢复
   验收

⑥ 只攻击 GAP 中最大的现实时间损失点

⑦ 只使用成熟免费能力替换/配置/组合
   不新增自研出口
```

## 6. 为什么当前不先上 n8n

n8n Community Edition 的确可以自托管且不收 SaaS 订阅费用，但它更适合确定性 workflow 编排。

当前第一目标是：
“用户说目标后，系统自己理解、检索、恢复、跨工具推进”。

OpenClaw 更接近完整成熟 Agent 壳层；n8n CE 只在明确证明能降低完整 T_VALID 的节点上加入。

## 7. 当前判断

```ini
FREE_PRODUCTION_FRONT_RUNNER=OpenClaw
FREE_SUPPORT_COMPONENTS=Codex Free;Existing Free Model Pool;n8n Community Edition;Existing Mature Browser Skills
PAID_REFERENCE=Manus 2.0
CHATGPT_WORK_PRODUCTION=EXCLUDED_PAID
```

这不是最终胜负；必须由 Reality 产生 T_VALID。
