# GPT直连Windows三通道执行桥 V6.0｜正式路由与恢复边界（2026-10-15）

> 唯一权威入口：`skills/extreme-time-automation-bridge/SKILL.md`，分支 `main`。本页为 V6.0 决议及2026-10-15现场复验记录；历史 V5/V3 技术资料保留，只按日期使用，不覆盖此优先级。
>
> 状态：`V6_ROUTING_POLICY_PUBLISHED`；`C_CURRENT_REAL_EXEC_PASS`；`A_INTERMITTENT_EXIT_DIAGNOSING`；`B_FAST_AND_BOUNDED_HISTORICALLY_VALIDATED`；`A_ROOT_FIX_REALITY_NOT_YET_PASS`。

## 1. 三通道唯一正式优先级

1. **C｜日常第一入口**：官方 Remote Desktop Commander（Windows 本机远程执行）。此后 GPT → Windows 文件、命令、故障处理、日常编码优先调用 `Remote_Desktop_Commander` 的真实工具。先确认设备在线、额度/权限允许，执行任务；如果有异步 call_id，先通过 get_tool_result 对账，不自动重跑副作用任务。不要把单次免费额度可用视为永久无限额。
2. **A｜第二入口**：自建 `GPT_Windows_MCP_Bridge`（OpenAI 官方 Tunnel→本机 Desktop Commander MCP）。保留和维护原唯一 tunnel-client、原身份、DPAPI 和监督计划任务。只有 C 不可用/额度受限、或业务明确需要 A 时才交给 A。A 当前实测能读取，但发生过多次真实退出与初始化窗口，**不是长期无故障**。
3. **B｜第三入口**：`cuiqinggang/codex-private-skills`→GitHub Actions→Windows Self-hosted Runner。适合异步、长流程、需要GitHub审计和工件的业务；C/A不可用时也可用于隔离诊断。需保留唯一任务ID、冻结SHA、结果和Exactly-once；绝不能将 B 当作每次小任务最快的默认路径。

**日常零额外确认：用户明确授权的Windows任务在C可用时直接走C；不要为了“检测A/B是否也可用”而重复执行同一任务。** 所有历史文件出现的 `A主路`、`R仅补充`、`B默认` 均是历史记录，V6 覆盖其路由语义，不删除证据。

## 2. B 超时的已验证 FIRST_DELTA：有成熟捷径但被绕过

- 2026-10-15 Run [38736230206](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38736230206)：旧 FULL `.github/workflows/extreme-time-windows-bridge.yml` 的 Windows 作业准备阶段下载 `actions/upload-artifact@v4` ZIP，`codeload.github.com` 第一次连接触发100秒HttpClient Timeout；最终5分钟内执行PASS并上传Artifact。不能说整条B断线，也不能说 FULL 稳定。
- **成熟路线早在 V3 已冻结**：`.github/workflows/windows-bridge-v1-fast.yml`（FAST，短任务仅日志回执）；`.github/workflows/windows-bridge-v2-bounded-artifact.yml`（Windows不下载外部Artifact Action，安全小型成功证据移交 GitHub 托管环境后官方Artifact上传）。V2 BOUNDED 历史5次独立Run实际30/36/36/36/38秒 PASS；见 `GITHUB_WINDOWS_B_ROUTE_V3_20261015.md`。
- **V6 固定分流门**：日志回执足够→FAST；可审计、小型、非敏感、成功时不超过已知上下限→V2 BOUNDED；大结果/失败也需工件/强审计→旧 FULL，并明确提示Action下载长尾风险。未知副作用必须先看现有任务状态；不得因超时盲目重复派发。
- V6本身不删除或篡改FULL，也不改Runner、FlClash、Windows代理。原因是这些工作流承载不同交付合同，不能只为省时牺牲失败证据。

## 3. A 间歇性退出：现场事实、分层诊断、禁止冒领修复

- 2026-10-15 20:50 北京时间，使用C渠道现场 `Watch-Tunnel-Health.ps1` 返回 `HEALTHY`、MCP initialized、单tunnel PID25228、控制平面polling、dispatcher failures 0、response-delivery failures 0；ChatGPT 对A `read_file` 也真实成功。
- Supervisor日志：北京时间 **19:32:31**（UTC11:32:31）Tunnel exit `code=0`，运行4362秒；19:33:02再次启动；**19:42:38**（UTC11:42:38） exit `code=1`，运行577.2秒；19:42:44再次启动。健康采样在19:35（PID52196）和19:45（PID25228）显示 `MCP_NOT_INITIALIZED`，稍后恢复。该故障不是纯UI弹窗，也不是永久断线。
- 原Supervisor在 `Recovery-Supervisor-v1.ps1` 中将官方Tunnel `2>&1 | Out-Null`，只记录ExitCode与耗时，**没有保留官方子进程的原始退出原因**。在没有完整错误证据前，不能把Exit1认作代理、409、TTL或单个确凿根因。保留已有V5 PS-002错误流兼容补丁及程序唯一实例约束。
- 官方`openai/tunnel-client` 文档规定stdio旧协议必须完成 initialize/initialized 时序，若未完成返回409；官方也曾报告请求response deadline导致shared stdio失效/进程关闭的故障族（GitHub issue #34），**仅为同类成熟参考，尚未与本机Exit1对应证实**。
- 成熟处理顺序：读取真实A工具错误→唯一PID/父进程→控制平面、MCP子进程代次与initialized epoch→Supervisor exit时间→官方Tunnel诊断或有界、去敏日志→仅在匹配FIRST_DELTA后做最小修复→合法新进程Reality→跨自然运行窗口检验。绝不因当前健康而重启工作中的唯一Tunnel、不得测试性Stop-Process、不读取或上传Runtime Key。
- A尚未通过完整异常退出根因修复、跨多日稳定、真实登录冷启动全链路验收。C担任默认工作入口不等于A的问题自动解决。

## 4. 用户截图中“View config · Desktop Commander”界面

- 截图位于**ChatGPT的GPT-Windows-MCP-Bridge工具结果区域**，展示MCP服务器配置（Blocked Commands、Allowed Folders、Default Shell、Telemetry、文件行数限制）；`Unable to generate preview in this environment` 表示工具内容预览不可用，**不是Windows弹出系统故障对话框，也不是隧道断开的证明**。
- A/C底层均用Desktop Commander能力，`get_config` 等响应可能展示配置卡片。V6日常禁止无必要时调用 `get_config`、`get_usage_stats`、onboarding工具；优先直接执行`read_file`/`start_process`，只展示业务结果。ChatGPT平台是否显示工具卡片由客户端决定，**不声称可凭本地脚本强制隐藏**。
- 当前正式A launcher的MCP命令已经带 `--no-onboarding`，因此不能再将这块配置展示误判为“脚本漏设关闭onboarding”。

## 5. 质量合同、额外权限与接续

- 不修改FlClash/系统代理、Windows桌面权限、已登录浏览器、Runner注册或密钥。只在副作用已授权且目标明确时执行；安全变更要备份、冻结SHA和验收。禁止创建第二Tunnel或第二Supervisor。
- C官方账户/调用额度可能变化；C失败先判断quota、离线、权限、任务异步，必要时按路由序列A→B，不无限重试。
- 回归验收：C真实Ping+文件/PowerShell PASS；B按任务证据合同选FAST/BOUNDED/FULL并检查工作流和真实机器回执；A当前只可记`SCOPED_REAL_READ_PASS`，不能记`ROOT_CAUSE_FIXED`。
- 新聊天第一行可写：`使用《GPT直连Windows三通道执行桥 V6.0》；正式优先级 C>A>B；权威仓库 cuiqinggang/codex-private-skills，skills/extreme-time-automation-bridge/SKILL.md。`
