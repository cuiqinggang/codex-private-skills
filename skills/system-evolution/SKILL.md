---
name: system-evolution
description: Use when the user says 系统进化, 情报支持系统进化方案, 执行系统进化, 跑系统进化, 长时间编程, 长编程流程, AI token 生意, 低成本 API, Cursor Claude Code DeepSeek V4Pro, DeepClaude, Ralph Loop, or asks to turn AI/IT intelligence, current projects, staged goals, feedback, and Codex/Hermes validation into a recurring personal system improvement loop.
---

# 系统进化

## 定位

“系统进化”是情报支持系统进化方案的短触发名。它不是新闻日报，而是把用户当前工作、未来阶段目标、公开成熟方案、优秀工具、优秀 skill、低成本路线、用户反馈和 Codex/Hermes 验证结果连成闭环。

## 固定边界

${REDACTED_SECRET}
- H 盘：仅历史资料，禁止写入、镜像、同步或更新
- K 盘备份：仅在 C 盘结果验证通过且用户逐次明确批准后执行
- 默认模式：`Approval`
- 自动模式：`Auto`，只允许执行低风险文件生成、报告、同步和验证任务包，不改生产配置。
- 禁止默认修改 Hermes、Codex 全局 AGENTS.md、Open WebUI 主配置、H/K 盘内容、账号、Cookie、Token、付费 API、长期后台服务。

## 触发说法

用户说这些话时使用本 skill：

- “系统进化”
- “执行系统进化”
- “跑一下系统进化”
- “情报支持系统进化方案”
- “把今天的情报变成系统升级方案”
- “根据我当前项目和未来目标改进系统”
- “长编程进化”
- “长编程流程”
- “Cursor 深度写代码”
- “DeepSeek V4Pro 长代码”
- “Claude Code 长时间编程”
- “长时间运行编程”
- “保持长时间运行”
- “Claude Code 循环运行”
- “DeepClaude”
- “Ralph Loop”
- “AI token 生意”
- “低成本 API 生意”
- “token 源头”
- “API 聚合分发”
- “模型网关”
- “低买高卖路线”
- “抖音情报”
- “视频情报源”
- “从我关注的视频里找方案”

## 子 skill 调度

- 长编程、DeepClaude、Ralph Loop、Cursor/Claude Code/DeepSeek V4Pro 几小时编码：优先使用 `long-coding-flow`。
- AI token 生意、低成本 API、模型网关、API 聚合分发、低买高卖：优先使用 `ai-token-business`。
- New API 本地部署、修复、健康检查、localhost:3001、Docker Compose、PostgreSQL、Redis：优先使用 `new-api-local-deploy`。
- 系统进化继续作为总入口：读取用户路线图、来源、反馈、报告，把验证成功的经验沉淀到对应子 skill。

## New API 与 AI token 双路线隔离

这两条路线必须并行推进但不能混在一起：

| 路线 | 对应 skill | 允许自动做 | 必须批准 |
|---|---|---|---|
| 本地 New API 自用网关 | `new-api-local-deploy` | 只读健康检查、localhost 端口检查、文档和报告 | 改 compose、读取 `.env`、创建 token、添加渠道、调用上游、公网暴露 |
| AI token / 低成本 API 商业路线 | `ai-token-business` | 公开资料研究、低买高卖报告、mock config、套餐模板、风险清单 | 真实 key、付费 API、登录供应商后台、客户账号、生产网关 |

`system-evolution` 只负责调度、总结、生成验证任务和沉淀经验；不得把 New API 生产操作和 AI token 商业策略写进同一个执行任务。

## 运行方式

首选运行脚本：

```powershell
${REDACTED_SECRET}
```

测试时禁用声音并强制跑一次：

```powershell
${REDACTED_SECRET}
```

## 输出

- `reports\system-evolution-report.md`：完整中文进化报告。
- `reports\report.md`：最终 PASS/PARTIAL/FAIL 汇报。
- `reports\latest-system-evolution-notice.md`：最新提醒摘要。
- `plans\evolution-plan.md`：三类计划：低风险自动动作、Codex/Hermes 验证动作、必须批准的生产升级。
- `actions\pending-approval.md`：当前需要用户批准的具体执行方案。
- `actions\codex-validation-tasks.md`：可交给 Codex/Hermes 的验证任务。
- `reports\cursor-claude-deepseek-long-coding-research.md`：Cursor + Claude Code + DeepSeek V4Pro 长编程成熟方案研究。
- `reports\video-source-strategy.md`：抖音、YouTube、TikTok、Bilibili 等视频情报源策略。
- `reports\ai-token-business-replay-YYYYMMDD.md`：AI token / 低成本 API 技术服务路线昨日重现。
- `plans\cursor-claude-deepseek-long-coding-workflow.md`：长编程阶段门、测试门、交接门和恢复流程。
- `actions\long-coding-task-package-template.md`：可交给 Cursor/Claude Code/Codex 的长任务包模板。
- `actions\ai-token-business-validation-tasks.md`：AI token / 低成本 API 技术服务验证任务。
- `actions\video-intelligence-card-template.md`：视频情报提取、评分和二次核实模板。
- `evidence\run-summary.json`：数量、安全和执行证据。

## 每日/开机任务

计划任务名称：`Codex_SystemEvolution_2h`

说明：沿用历史任务名以避免断开旧引用；实际调度语义是 24 小时内最多真正生成一次报告。

注册脚本：

```powershell
${REDACTED_SECRET}
```

任务使用隐藏窗口运行，默认每天执行一次 `Approval` 模式。固定时间只作为一个触发机会，不要求电脑必须在该时刻开机。runner 默认使用 `-MinHoursBetweenRuns 24`，所以任何触发来源都会先检查上次成功时间；24 小时内只记录跳过，不重复生成报告。

如果 Windows 计划任务因为权限不能更新为登录触发，注册脚本会写入当前用户启动项：

```text
${REDACTED_SECRET}
```

该启动项在用户登录/开机后补跑同一个 runner，仍受 24 小时冷却限制。声音提示由 runner 负责，不创建弹窗，不移动鼠标，不操作真实键盘。

## Periodic Self Improvement Audit

Use the periodic self-improvement audit when the user asks to review recent
Codex/Hermes/OpenClaw/ComfyUI/ECC/AI company work and turn repeated mature
paths into reusable assets.

Default cadence: every two weeks. This is frequent enough to capture repeated
work while leaving time for real tasks to produce evidence. Do not run it hourly
or daily by default. Run it manually only after a dense sprint where several
systems changed.

Read `references\self-improvement-audit-runbook.md` before changing this
workflow.

Manual run:

```powershell
${REDACTED_SECRET}
```

Register the two-week schedule:

```powershell
${REDACTED_SECRET}
```

The audit only writes reports under
${REDACTED_SECRET}
start or stop production services, read secret file bodies, or modify
production configuration.

## 执行策略

1. 读取 inventory、roadmap、sources、scoring、feedback。
2. 运行最小 PoC，生成日报、系统进化报告、升级计划、验证任务和 skill 草案。
3. 写入 `pending-approval.md`，把今天可执行方案分为：
   - 可以自动做的低风险动作。
   - 需要 Codex/Hermes 验证的动作。
   - 必须用户批准的生产升级。
4. 播放声音提示并写入 latest notice。
5. 同步 skill 和最新报告到 H 盘镜像。
6. 在用户明确批准后，才执行生产系统升级。

## 长编程重点项目

当用户要强化 Cursor + Claude Code + DeepSeek V4Pro 的长时间写代码能力时，本 skill 必须把它作为长期重点项目处理：

1. 不直接相信模型一次性完成大任务，先生成任务包、阶段计划、测试命令、停止条件和回滚说明。
2. 每个子任务控制在 30-90 分钟，要求写 `execution-log`、`verification`、`handoff`、`next-actions`。
3. Cursor + Claude Code + DeepSeek V4Pro 负责主要编辑；Codex 负责任务包、验证、报告和沉淀；Hermes 后续只接收已验证流程。
4. 任何账号授权、API key、Cursor Background Agents、GitHub App、Codex cloud 或长期后台任务都必须用户批准。
5. 每次系统进化运行都继续搜索成熟公开方案，并把有效改进写回 roadmap/source/state。

细则见 `references\long-coding-flow.md`。

${REDACTED_SECRET}

## AI token / 低成本 API 技术服务重点

当用户要研究 AI token 生意、低成本 API、token 源头、模型网关或低买高卖路线时，本 skill 必须转入 `ai-token-business` 经验包。默认判断：

1. 不做灰产 API key/token 转售。
2. 不共享、出租或拆分个人/企业账号。
3. 主路线是合规 AI API 网关、BYOK、virtual key、budget、rate limit、cost tracking、fallback 和客户套餐服务。
4. 只允许公开资料、报告、mock config、套餐模板和验证任务；真实 API key、付费调用、登录、生产网关部署必须用户批准。

${REDACTED_SECRET}

## 视频情报源重点

当用户要求从抖音、YouTube、TikTok、Bilibili 或其他视频平台获取 AI/科技/工具分享时，本 skill 必须把视频作为一等信息源处理：

1. 抖音关注流是高价值个性化来源；用户已明确把视频情报纳入任务后，可直接只读浏览、截图、转写和记录，不逐条等待批准。
2. 默认不得执行账号写操作，不得点赞、关注、评论、私信、收藏、发布或修改账号；出现验证码、账号安全提示、付费墙或隐私内容时停止。
3. 视频候选必须记录平台、作者、链接、标题、发布时间、公开热度、截图/字幕/转写和采集时间。
4. 高赞视频不能直接当结论，必须用官方文档、GitHub、release、公开案例或评论区实测做二次核实。
5. 只有能对应用户系统模块并生成验证任务、skill、脚本或流程的内容才进入升级计划。

细则见 `references\video-source-intelligence.md`。

## 模式

| 模式 | 行为 |
|---|---|
| `Approval` | 只生成报告、待批准清单、声音提示和 H 盘同步；不执行生产升级。 |
| `Auto` | 自动执行低风险文件类动作和验证任务包生成；生产升级仍需批准。 |
| `ReportOnly` | 只生成报告，不同步 H 盘，不播放声音。 |

## 失败处理

- 如果 PoC 未达标，写入 `reports\latest-system-evolution-notice.md` 并播放失败提示。
- 如果 H 盘不存在，只跳过 H 盘同步，不判定主任务失败。
- 如果声音组件不可用，只记录 warning，不阻止报告生成。
- 如果计划任务注册失败，不修改其他系统配置，报告失败原因。

## Long-term Focus: 聚合分发网站商业情报增强系统

system-evolution 必须把聚合分发网站作为长期重点业务域持续增强。核心目标是先服务用户自用，形成可复用信息库、判断材料、验证任务和 skill 更新草案；后续在找到真实用户后，把稳定服务、组合方案、运营支持和交付能力推给客户。

执行时必须同时覆盖低买和高卖。低买关注稳定、合规、可规模化的上游供应、批量议价、开源替代和自动化降本。高卖关注客户痛点、增值服务、组合交付、售后运营、长期维护和标准化套餐。

每日循环输出不应是零散新闻，而应转化为可复用信息库、决策材料、验证任务、风险提示和 skill 更新草案。

必须优先读取 references/aggregation-distribution-biz-intel.md、references/execution-policy.md、references/video-source-intelligence.md、references/long-coding-flow.md。

GPT 网页 super-brain 负责成熟路径判断和复杂规划。Codex 负责按合规计划执行、验证、归档、回报。Codex 不自行做商业路线判断。不得修改账号、Cookie、Token、付费 API、生产配置或非本 skill 的长期后台服务。
