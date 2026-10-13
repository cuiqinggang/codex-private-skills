# Remote Desktop Commander 免费额度成熟运营 V1.0｜v0.3.4 正式执行附则
METHOD=REMOTE_DCR_QUOTA_OPERATIONS_V1
PARENT=skills/extreme-time-automation-bridge/SKILL.md@v0.3.4
EFFECTIVE=2026-10-13
STATUS=ACTIVE_POLICY;STATIC_GATE_EXECUTABLE;NOT_AUTO_INTERCEPTOR

> **每次使用本技能包进行 Windows 远程执行之前必须做“任务判路+额度门”**。这不是新通道、不是新的后台调度器，也不要求每次调用额外远程探针。本页中的 A、B、R 是执行路线，不是历史“DCR主路、GitHub备路”的命名。

## 1. 三路及基本优先级

| 路由 | 链路 | 通常适用 | 真实使用门 |
|---|---|---|---|
| A | ChatGPT → 用户自建 GPT-Windows-MCP-Bridge（OpenAI 官方 Tunnel）→ 本机开源 Desktop Commander MCP | 日常小任务、频繁读写、PowerShell、本地 Codex CLI、低延迟交互 | 对目标能力实测可用；独立于官方 DCR 托管月配额 |
| B | GitHub 私有共同工作区 → Actions → Windows self-hosted Runner | 异步/长任务、隔离执行、A暂不可用时备用 | 工作流真实覆盖目标业务，任务ID/权限/回执完整；最简 smoke PASS 不自动代表复杂生产 PASS |
| R | Remote Desktop Commander 官方托管免费版 | A/B 不覆盖、特殊低延迟故障恢复，且本月配额充足时的补充 | 在线 + 授权 + 远程执行能力 + 新鲜官方用量证据 + 额度门通过 |

**默认 A 优先短任务；B 优先真正的长/异步任务（必须确认业务工作流可用）；R 不得因设备 Online/ping 就自动启用。** 只有任务明确需要 R 的特有能力，或 A/B 当前均不适用且 R 通过额度门，才考虑 R。浏览器模拟 ChatGPT 不是新的执行主路。

## 2. 每次使用的短判路合同（先判路再调用，不能先试几次）

第一步：确定 TASK_ID、任务类别（interactive、batch、long、recovery）、是否有副作用、授权和 DONE_WHEN。检查已经掌握的最近 A/B/R 真实回执及是否覆盖本任务能力；已证实的同状态结果复用，不为探活重复调用 R。
第二步：优先按 A/B 选择路线；R 只有必要时才读最近一次 **官方 Remote 托管账号剩余额度**，以官方仪表板或 who_am_i 百分比为准。**不得用自建 MCP 的 get_usage_stats 累计 8733 次冒充 Remote 托管消耗**。
第三步：R 申请必须填写预计调用次数、预算状态、任务价值、A/B 不适用的客观原因及核验方式。不具备官方有效余额证据时，不消耗 R 去“试一下”；优先 A/B。
第四步：如判路或调用方式违反本页规则，**先提醒后执行**：指出 ROUTE_RULE、预计浪费的调用、推荐 A/B 路线，以及一条可落地的改法。普通违规应主动改路；用户特意要求 R 但额度不足，明确说明限制，不用换账号/反复配对绕过配额。
第五步：执行后记录任务成功与否、实际路由、任务ID或 run_id/call_id、调用数（未可靠获取记 UNKNOWN）、是否重复尝试、一次完整验收结论。UNKNOWN 副作用先对账后重试。

## 3. 月度预算（规划阈值，不是厂商自动分配的额度）
- 免费包标称 10000 **工具调用**／月，非 10000 次登录或“连接”；额度规则以当下服务官方面板为准。具体重置日未证实，旧“2026-11-01 复查”只是提醒日期。
- 日常计划 6000/月，弹性 2000/月，紧急储备 2000/月；200/天是软目标，**不是官方每天充值或不准正常业务超出**。
- 已用 0–5999：R 仍需证明必要性；不允许拿它代替可用 A 来批量重复调用。
- 已用 6000–7499：黄色提醒；普通 Remote 调用应转 A/B，R 只保留确实需要的关键交互。
- 已用 7500–7999：橙色警戒；R 非必要停用并提醒剩余的紧急空间。
- 已用 8000–9499：红色熔断；R 常规调用暂停，仅经过明确人工同意的紧急任务例外，且确保单次预计数不突破 9500。
- 已用 >=9500：停用自动 Remote；仅用户逐次明确批准且剩余足够时允许紧急调用。达到10000或服务提示 quota exhausted 时彻底阻止 R，**禁止重试**。
- 如果只拿到 remaining_pct，将其作为近似预警而非精确计数；>=40%余额属于宽松、<=40%黄色、<=25%橙色、<=20%红色、<=5%严格人工门、=0阻断。若用量快照不新鲜或统计口径未知，默认阻止新增 R 批量任务、改走 A/B。
- 用户当前（2026-10-13）官方账号 who_am_i 实测 remote_calls_left_pct=0，R=QUOTA_BLOCKED；本地 MCP 自建 A 同日仍成功实际读写/计算，B 自托管 Runner 在 2026-10-13 的最简任务两次 PASS。
- 本策略不以升级厂商套餐或新购 VPS 为默认动作，也不使用多账号规避厂商限制。

## 4. 防浪费触发器与改法（遇到即提醒）
| 触发 | 风险/误用 | 立刻处理 |
|---|---|---|
| R 额度=0/错误提示 reached usage | 无效调用/继续失败 | 标 QUOTA_BLOCKED，一次即停止，切 A/B；禁重连重配 |
| R 请求批量读取/大量命令且 A 可用 | 浪费付费托管池 | 改 A；相邻文件使用 read_multiple_files 或一次性安全批处理 |
| start_process 后持续 read_process_output 无新输出 | 高密度轮询 | 先复用现有 PID/状态，必要时延长间隔；不得为凑探测不停查询 |
| B 被用于高频短命令但 A PASS | 19–27s级调度开销（历史小样本） | 改 A，减少 GitHub 工作流启动频次 |
| R online/pong 但 exec 失败 | 把可达误判可执行 | 区分 QUOTA / AUTH / DEVICE / NETWORK / TOOL；只做最小合法排障 |
| R 用量证据缺失或过期 | 超支不可控 | 暂停 R 非必要执行，核对官方面板；其他通道继续 |
| 非幂等任务 UNKNOWN 后打算重发 | 重复副作用 | 先通过 task_id/run_id/PID/目标状态对账，Exactly-once |
| 降低验证次数以省配额 | 错误交付风险 | 保留必要独立验收，优先换 A/B 而非取消验收 |

## 5. 可执行判路器、输入与返回
- **可选零副作用预检脚本**：[`bootstrap/Invoke-Remote-Quota-Route-Gate.ps1`](bootstrap/Invoke-Remote-Quota-Route-Gate.ps1)。接受任务类别、各通道实际可执行状态、经核验的 Remote 已用次数或剩余百分比、是否紧急以及用户指定路由。输出 JSON 的 `selected_route`、`warnings` 和 `status`；本身不连接、不派发、不写文件、不使用 Remote 配额。用于判路**不是**长流程自动运行器。
- 用前最小人工判断也等效；不要求为此新启动 Windows 或 GitHub，避免“省额度脚本反而浪费时间”。
- 示例：`pwsh -NoProfile -File bootstrap/Invoke-Remote-Quota-Route-Gate.ps1 -TaskKind interactive -AState ready -BState ready -RState quota_blocked -RemoteRemainingPercent 0 -RequestedRoute R` → 选择 A，给出“R 禁用，改 A”的警告。
- 对 R 的正式动作调用：先看判路结果及授权，再通过相应工具执行；脚本不是 MCP 拦截层。**没有运行此脚本或没人工复核的外部会话，不保证会自动出现提醒**；必须在每个新页面/Agent 的运行入口按本附则加载。

## 6. 与旧文件兼容、更新/验收
- 该附则由 SKILL.md 顶部“进入即判路”的规则明确引用，优先于旧 DUAL_ROUTE.md 的静态“DCR 主路”、10月12日晚 GitHub 临时优先的历史快照；历史故障事实保留。
- 原 DCR 登录配置、OpenAI 隧道、GitHub Runner、Windows 运行脚本、用户浏览器、FlClash/代理 **全部不改变**，绝不触碰 Remote 配额服务器。
- 目前状态：`RULE_IN_SKILL=ACTIVE`、`AUTO_PROXY_HOOK=NOT_INSTALLED`、`REMOTE_QUOTA_EXHAUSTED=YES_AS_OF_20261013`、`REBOOT_RECOVERY=NOT_TESTED`。
- 修改任何调度/判路实现前，需用 R=0、R=6000、R=8000、R=9500、quota_blocked、A/B中断、用户误选R、UNKNOWN等案例验证；通过不意味着长时业务自动化全部 PASS。