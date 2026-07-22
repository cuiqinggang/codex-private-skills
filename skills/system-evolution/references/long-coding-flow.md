# 长编程流程自动化

## 目标

强化 Cursor + Claude Code + DeepSeek V4Pro 的长时间综合编程能力，让低成本模型能在几个小时任务中保持可控、可恢复、可测试、可交接，而不是依赖一次性长聊天。

## 默认路线

1. Codex 先生成长编程任务包。
2. Cursor + Claude Code + DeepSeek V4Pro 按任务包执行局部编辑。
3. 每 30-90 分钟形成一个可验证阶段。
4. 阶段结束必须更新 execution-log、verification、handoff、next-actions。
5. Codex 或 Hermes 接手时只读取 handoff 和当前阶段，不靠聊天记忆。
6. 验证成功后沉淀为 skill、脚本、规则或昨日重现案例。

## 视频提炼的适用判定

长时间运行不是让 agent 无限聊天，而是把任务变成可循环、可验证、可暂停、可恢复的工程流程。

适合循环 = 目标明确 + 可以自动验证 + 可以分步推进 + 出错可回滚 + 风险可控。

适合使用：

- 有明确目标和边界的大型重构、迁移、测试补齐、文档化、批量修复。
- 能用 `test`、`build`、`lint`、脚本、截图、文件差异或固定验收清单自动验证。
- 可以拆成 30-90 分钟阶段，每阶段都有可交付输出。
- 失败后能回到上一个 checkpoint，不会损坏账号、密钥、生产数据或系统配置。

不适合使用：

- 需求还没定清楚，或者成功标准只能靠主观判断。
- 需要频繁账号授权、付款、登录、验证码、Cookie、API key 或真实用户操作。
- 需要一次性大范围删除、覆盖生产配置、修改全局系统规则。
- 没有测试、没有回滚点、没有日志，失败后无法判断原因。

## 四类长时间运行方法

### 方法 A：CLI/Shell 循环

用 PowerShell、Bash 或任务脚本循环调用 Claude Code/Codex/其他 agent，每轮只执行一个小目标。

必须具备：

- `MaxRounds`：最大轮数，禁止无限循环。
- `TimeboxMinutes`：总时限或单轮时限。
- `StopSignals`：`COMPLETE`、`NEED_APPROVAL`、`BLOCKED`、`TEST_FAIL_LIMIT`、`TIMEBOX_EXPIRED`。
- `VerifyCommand`：每轮或每阶段必须运行的验证命令。
- `LogPath`：追加写入命令、结果、失败原因、下一步。
- `Checkpoint`：每轮开始前记录当前 git diff、文件清单或备份路径。

基本循环：

```text
for each round:
  read 00-goal, 01-context, 02-plan, latest handoff
  choose one small next action
  edit only allowed files
  run VerifyCommand
  append execution-log and verification
  update handoff and next-actions
  stop if any StopSignal appears
```

### 方法 B：Ralph / Ralph Loop 类循环器

Ralph 类工具的价值是把“目标 -> 执行 -> 验证 -> 继续/停止”产品化，而不是替代工程判断。使用时仍要套本文件的任务包、日志、验证和停止条件。

适合：

- 目标清楚、验证命令稳定的长任务。
- 重复跑“实现一点 -> 测一点 -> 写 handoff”的任务。
- 希望 agent 在可控时限内自动推进多个小步。

必须限制：

- 不允许 Ralph 类循环器自己扩大范围。
- 不允许跳过失败分析继续改。
- 不允许在没有批准时接入账号、付费 API、后台服务或远程仓库权限。
- 每轮输出必须能被 Codex/Hermes 读取和接力。

### 方法 C：Hooks / Guardrails

Hooks 用来在 agent 执行前后自动加护栏，重点不是更聪明，而是减少长时间运行时的漂移。

建议 hook 点：

- `before_edit`：检查是否在允许目录内，是否触碰禁止文件。
- `after_edit`：记录 diff 摘要和改动文件。
- `before_command`：阻止删除、安装、全局配置、未知网络脚本等高风险命令。
- `after_command`：记录退出码、关键日志、失败片段。
- `before_continue`：确认 verification、handoff、next-actions 已更新。

### 方法 D：Harness / OmX / Goal 类长任务命令

把长任务封装成固定命令或 harness，让 agent 每次按同一协议运行。

应包含：

- 输入：目标、范围、允许文件、禁止事项、验证命令、阶段预算。
- 执行：按 G01-G10 阶段门推进，不允许跳门。
- 输出：日志、验证、handoff、next-actions、风险和待批准项。
- 恢复：下一次从 `05-handoff.md` 和最近一次验证结果继续。
- 沉淀：通过后把稳定流程同步到 skill、脚本或模板。

## 长流程阶段门

每个长时间编程任务必须先生成阶段门。默认用下面 G01-G10，不够时只能增加低风险子门，不能删除验证门和停止门。

- G01 目标门：写清目标、非目标、成功标准、禁止修改项。
- G02 环境门：确认仓库、分支、依赖、当前改动和可回滚点。
- G03 上下文门：读取项目规则、相关文件、历史报告和成熟方案。
- G04 拆分门：拆成 30-90 分钟阶段，每阶段只交付一个可验证结果。
- G05 验证门：确认每阶段的测试、构建、lint、脚本或人工验收点。
- G06 执行门：只执行当前阶段，不提前做后续阶段。
- G07 记录门：记录命令、输出、退出码、错误、文件改动。
- G08 修复门：失败时先定位 root cause，再做最小修复。
- G09 交接门：更新 handoff、next-actions、剩余风险和恢复入口。
- G10 沉淀门：验证通过后再更新 skill、模板、脚本或昨日重现案例。

## 任务包必须包含

- `00-goal.md`：目标、范围、禁止修改项、预算、预期输出。
- `01-context.md`：相关文件、现有规则、已知风险、成熟方案链接。
- `02-plan.md`：阶段计划、验证命令、成功标准、失败停止条件。
- `03-execution-log.md`：命令、结果、错误、证据路径。
- `04-verification.md`：测试结果、失败原因、下一假设。
- `05-handoff.md`：已完成、未完成、阻塞、下一轮第一步。
- `06-next-actions.md`：低风险下一步、需批准项、暂不做项。
- `07-loop-control.md`：最大轮数、时限、停止信号、允许目录、禁止命令。
- `08-rollback.md`：checkpoint、备份、git diff、恢复步骤。
- `09-decisions.md`：关键取舍、为什么采用、后续可调整点。

## 单轮执行协议

每一轮必须按顺序执行：

1. 读取 `00-goal.md`、`02-plan.md`、最新 `05-handoff.md` 和 `07-loop-control.md`。
2. 明确本轮只做一个小目标，并写入 execution-log。
3. 修改前确认允许目录、禁止文件、当前 diff 和回滚点。
4. 执行最小改动，不做顺手重构。
5. 运行本轮 `VerifyCommand`。
6. 验证失败时，先记录失败层级、错误片段、root cause 假设，再修。
7. 验证通过或停止时，更新 `03-execution-log.md`、`04-verification.md`、`05-handoff.md`、`06-next-actions.md`。
8. 只有当前阶段达到成功标准，才进入下一轮。

## DeepSeek V4Pro 加固规则

- 只给当前阶段所需上下文，避免一次性塞入全历史。
- 先读项目规则和测试，再改代码。
- 先写/确认验证命令，再执行实现。
- 失败时必须输出 root cause、证据和最小修复，不允许连续猜修。
- 长任务中固定产出 handoff，使下一轮可恢复。
- 不把上一轮全部聊天记录塞回模型，只回传任务包、最新 handoff、验证结果和必要 diff。
- 如果使用 reasoning 模型，不把 `reasoning_content` 当作下一轮上下文传回。
- 对低成本模型要缩小自由度：明确允许文件、禁止操作、输出格式、停止信号。

## Business Intelligence Engineering Flow

当聚合分发网站商业情报转化为工程任务时，必须使用长时间 gated engineering 流程。

适用任务包括：本地静态聚合站原型、公开信息 report-only 采集脚本、情报归档目录结构、上游价格对比表生成、竞品栏目结构分析工具、客户套餐报价模板、本地仪表盘原型、skill 自动校验脚本。

执行规则：先由 GPT 网页 super-brain 给出成熟路径和 gated plan；Codex 不自行发明业务路线；先实现最小可用验证，不做大而全系统；每个 gate 必须有成功判定和失败停止条件；写代码前必须知道测试命令；每轮完成后必须生成 report；成功流程必须沉淀回 system-evolution skill；不创建非本 skill 的长期后台服务；不接入真实账号、Cookie、Token 或付费 API；不把 demo 误报为生产可用系统。
- 每 3-5 轮必须做一次汇总压缩，删除无用日志，只保留事实、决策、失败证据和下一步。

## DeepClaude / Claude Code 后端路线边界

DeepClaude 的价值是保留 Claude Code 的 agent loop、文件编辑、命令执行和长任务推进方式，同时把模型后端临时切到 DeepSeek V4Pro 或 Anthropic-compatible 路由以降低成本。

本 skill 只沉淀长时间编程流程，不默认接入模型后端：

- 不自动配置 API key、OpenRouter、Fireworks、DeepSeek 官方 key 或本地代理。
- 不自动修改 Claude Code 全局配置、PATH、系统环境变量或 Cursor 配置。
- 只允许在用户明确批准后，用临时 PowerShell 进程环境变量测试。
- 长编程流程验证通过后，再决定是否把后端接入方案沉淀为单独安装 skill。

## 长时间运行输出要求

每 30-90 分钟至少产生一次可检查输出：

- 已改文件清单。
- 当前 diff 摘要。
- 已运行命令和退出码。
- 验证通过/失败证据。
- 下一轮第一步。
- 需要用户批准的事项。
- 是否继续、停止或回滚。

完成判定只能来自验证通过和成功标准达成，不能因为“已经运行很久”或“代码已经写完”就判定完成。

## 必须停止并请求批准

- 需要 API key、Cookie、账号登录或付费调用。
- 需要修改 Hermes、Codex 全局规则、Open WebUI 主配置。
- 需要启用 Cursor Background Agents API、GitHub App、Codex cloud 或长期后台服务。
- 需要删除文件、批量改生产代码或运行未知安装脚本。
- 连续两轮同类测试失败且 root cause 不清楚。
- 需要扩大目标范围、改变成功标准或跳过验证。
- 发现用户已有未提交改动会被覆盖。
- 需要真实桌面鼠标键盘、浏览器账号操作或隐私敏感页面。
