---
name: extreme-time-automation-bridge
version: "0.3.3"
description: GPT直连Windows双路执行桥。保留 Desktop Commander Remote 主路和 GitHub Actions 自托管 Runner 备路；v0.3.3 追加 OpenAI 官方 Tunnel 与 ChatGPT 演示 MCP 的完整创建、故障恢复及证据记录，不冒充生产 Windows 远程执行验收。
---

# GPT直连Windows双路执行桥 v0.3.3

**2026-10-12 OpenAI Tunnel 恢复首入口：** [逐步操作/故障树/原命令](OPENAI_TUNNEL_CONNECT_RECOVERY_20261012.md) ｜ [真实日志与回显证据](evidence/OPENAI_TUNNEL_DEMO_REALITY_20261012.md)。先读它们，再诊断；不得以聊天记忆代替。原有 A/B 双路照旧。

STATUS=REALITY_PARTIAL_PERSISTENCE
VERSION=0.3.3
PRIMARY_ROUTE_CURRENT=PASS
PRIMARY_DEVICE_NAME=DESKTOP-4A1EGTM
PRIMARY_DEVICE_ID=f6990966-5870-484b-bf79-409bc6fb963e
PRIMARY_APP_VERSION=0.2.52
PRIMARY_PING_REALITY=PASS
PRIMARY_WINDOWS_COMMAND_REALITY=PASS
OLD_DEVICE_ID=28ebd1ea-e749-466d-ad88-1b9f262d0651
OLD_DEVICE_STATUS=OFFLINE
FALLBACK_ROUTE_CURRENT=PASS
FALLBACK_RUNNER=DESKTOP-4A1EGTM-etal
DCR_AUTOSTART_TASK=GPT-DesktopCommander-Remote-Autostart
DCR_AUTOSTART_USER=A
DCR_AUTOSTART_ENABLED=YES
DCR_RECONNECT_LOOP=YES
REBOOT_PERSISTENCE_REALITY=NOT_YET_TESTED

## v0.3.0 新增：DCR 最短恢复法

当 Remote 离线且运行 npx -y @wonderwhy-er/desktop-commander@latest remote 出现 JSON/config 或 lock 错误时，按 DCR_RECOVERY.md 执行：停止旧实例 → 备份坏配置/旧配对 → 重新运行 remote → 原 Google 账号重新配对 → 独立 ping → Windows 命令验收。

本次 Reality：新设备 503e66bf-4f80-49fc-a90f-020ec8c71b1e Online；ping PASS；Windows 命令 PASS。旧设备仅保留为 Offline 历史记录。

## 后台自动连接

已创建 A 用户登录态计划任务 GPT-DesktopCommander-Remote-Autostart。
launcher：C:\Users\A\AppData\Local\DesktopCommanderRemote\Start-DesktopCommanderRemote.ps1

行为：A 用户登录后自动启动；Remote 退出后 5 秒自动重启；MultipleInstances=IgnoreNew。

注意：尚未经过真实 Windows 重启后的 Reality 测试，所以开机持久化只能标记“已配置、待验收”，不能标 PASS。

## 双路规则

1. DCR Online 且能力覆盖 → 主路。
2. DCR 离线 → 优先按最短恢复法恢复。
3. 主路暂不可恢复而 GitHub runner Online → 备路。
4. 两路都不可用 → 明确阻塞原因，不伪装成功。
5. 不修改 FlClash / Windows 网络代理。

## 2026-10-04 双路真实复验 R1（当前状态）

- 当前在线主设备 ID：f6990966-5870-484b-bf79-409bc6fb963e；历史503e设备已Offline，以实时list_devices为准。
- 主路：真实Windows命令、部署、循环检查与实际runtime inbox验证PASS。
- 备路：首测 Actions run 37192980220 在 Git checkout 阶段两次连接GitHub失败；不得把Online当畅通。
- 根因范围修复：Windows任务不再依赖Git partial clone补取blob；从同一github.sha经Contents API按需读取任务JSON、payload和Invoke-BridgeTask.ps1。每文件最多3次、每次30秒、间隔2秒；使用本次workflow临时token，不存入文件/日志。
- 复测 run 37193387268 全部success；实际runner=DESKTOP-4A1EGTM-etal，执行exit_code=0、duration_ms=2453.998，真实进程/文件循环4/4 PASS及唯一marker回传。
- 未修改FlClash、Windows网络代理；当前双路限定命令任务PASS不保证未来零故障，不替代重启/注销持久化Reality。
- 证据：../long-term-memory-super-virtual-human/evidence/V050-WINDOWS-GOAL-LOOP-REALITY-20261004-R1.json。

## v0.3.1 新增：通用网络抖动容错（成熟方案复用）
适用于 Desktop Commander 主路、GitHub Actions 备路、n8n→MCP、HTTP API 等，禁止因为一次超时直接推翻成熟架构，亦禁止将所有错误概括为网络抖动。

- 先建立 GOOD 基线：区分连接探测、只读查询、写入命令、后台任务；记录正常响应区间、尾延迟、失败样本、任务最终完成率及总耗时。10次短测不能推断长期故障率。
- 优先使用成熟客户端/官方 SDK 已有超时、取消、有限重试、指数退避/抖动、会话恢复、任务结果查询接口；不得自研调度器/状态机。设定的调用内部 timeout 不等于云端远程请求会在该时间强制终止，须经 Reality 验证。
- 对 transient 错误（连接断开、超时、HTTP 429/502/503/504 等）才按官方 Retry-After/策略有限重试；403 Host 校验、授权/配置错误须修配置而非盲重试。连接恢复后沿原任务继续。
- 只读/幂等请求可安全重试；发送、写文件、业务动作等非幂等操作在 timeout/unknown 状态时必须先通过 call_id、进程 PID、任务 ID、最终回执、目标对象状态确认是否已执行，必要时幂等键/唯一标记保护后再继续。禁止对未知结果直接重发。
- Desktop Commander 主路：优先 list_devices → ping → 实际只读命令；离线用原 v0.3.0 的最短恢复法。若远程工具返回 running call_id，先 get_tool_result 或 list_remote_tool_calls，进程 PID 使用 read_process_output。未获 call_id/PID 时不得假设未执行。
- 失败恢复的净收益门：比较等待超时与安全恢复总时长；不将未验证的 3秒/8秒候选门限写为正式性能指标；只冻结有现实证据的配置。
- 禁止修改 FlClash/Windows 代理，禁止引入新的桥接层；允许对自己可控制的连接配置作最小适配，但任何取消/重试都须先确认不会破坏 Exactly-once。

### 2026-10-09 证据及限制
- 主路 Desktop Commander Remote 0.2.52 设备 f6990966-5870-484b-bf79-409bc6fb963e，通过原有 `npx -y @wonderwhy-er/desktop-commander@latest remote` 恢复持久会话，不必重新 Google 配对；GPT 端 Online、Ping、真实 Windows 命令回读 PASS。
- 曾测 10 次 Ping：第1次超时、随后9次 PASS；命令3次中2次回读、1次超时且执行结果未知。此为小样本，不能认定长期故障率或根因。
- 本版本冻结的是复用策略，不声称客户端已经实现可强制取消的短超时，也不声称 n8n 完整业务链路 FINAL_VALID。

## 阻塞不等于放弃｜成熟方案组合恢复门（2026-10-10增补）
**适用范围：** GPT、Codex、双路桥、工具/网络/本机命令的普通技术失败。默认动作是继续解决母任务，不能因一条命令或一次连接失败自动终止。失败层级必须精确标记（工具调用、命令、节点、任务），不可由局部失败推断整个成熟系统不可用。

1. **定位证据：** 保留原始错误、时间、调用 ID/PID、运行环境、授权范围；先以已成功的 GOOD 基线做正反差分，判断网络、配置、命令包装、权限、工具自身或业务逻辑。
2. **成熟复用：** 先查本技能包、历史可回读成功案例、官方已有接口/恢复功能与已授权工具；禁止优先自研替代桥、调度器或状态机。已成功能力不重复折腾，例如 GPT-DCR 的 `whoami` 真实 PASS，不因 Codex 自己的 `exec_command` 受限而判 GPT 主路失败。
3. **候选空间：** 允许在虚拟阶段检索、组合、淘汰数十/数百甚至更多有根据的成熟方法；这不是强制做几千次现实调用。每轮保留最多3个高净收益候选，依次复核前提、失败模式、依赖、兼容性、风险、时间成本；模拟多个迭代，旧证据和失败路径不丢失。
4. **受控现实：** 选最小授权验证动作，按 Freeze 后必要的一次现实验证或经用户任务规则允许的诊断执行；非幂等动作先查回执，严格 Exactly-once；成功后沿原任务恢复，而不是重新从头开始。
5. **继续门：** 普通阻塞即使多次失败，也要先判断是否还有新证据、新成熟候选或有正净收益的合法诊断；不可只因“又失败了”停止。禁止盲目重复相同失败、机械凑次数和无上限消耗。
6. **停止条件：** FINAL_VALID；已无证据支持继续且下一候选净收益≤0；用户明确终止；资源/时间明确上限；或当前受限动作触及硬性安全/权限拒绝。**硬性拒绝只停止该受限动作，不能换渠道绕过；其他合法独立节点继续。** 暂不可完成时冻结状态、记录精确阻塞和可执行下一步，不宣称整体 PASS。
7. **诚实边界：** 成熟组合显著增加可解机会，但并不能保证每个问题一定可解决，特别是授权、物理限制或不可用外部依赖；不得用“必然解决”代替现实证据。

记录字段：BLOCKER_ID、GOOD_BASELINE、FIRST_DELTA、ERROR_CLASS、MATURE_CANDIDATES、VIRTUAL_FILTER、AUTHORIZED_REALITY、EXACTLY_ONCE_STATE、T_VALID、NEXT、STOP_REASON。此为方法规则增补，不代表双路全部新场景已现实验收。


## n8n 常驻可调用诊断与入口区分（2026-10-10）
**现场证据：** Windows Docker 容器 `n8n-local`（`n8nio/n8n:stable`）健康运行，127.0.0.1:5678/healthz HTTP200，浏览器Chrome CDP 127.0.0.1:9223/json/version HTTP200；n8n `/rest/workflows` 未带会话返回401，只表示受保护管理接口未认证，**绝不能据此判断n8n故障、要求用户重新授权或停止任务。**
**正确三层检查：**
1. `docker ps` 核验健康；`Invoke-WebRequest http://127.0.0.1:5678/healthz` 核验服务；此层不代表业务成功。
2. 使用已经配置好的、获准的n8n容器原生CLI只读枚举 `docker exec n8n-local n8n list:workflow --all`；必要时 `export:workflow --all --output=/tmp/<临时文件>.json` 检查 `active`、节点类型、Webhook方法和路径，禁止把敏感凭据输出日志。Manual Trigger（手动触发）与已激活Webhook是两种不同运行入口。
3. 仅对已知、获准且副作用范围清楚的Webhook提交任务，必须取回业务回执并核验Exactly-once；不能把任意活跃Webhook当作无副作用测试接口。非幂等任务如结果UNKNOWN，先查既有执行记录，绝不盲目重复。
**已回读的2026-10-10实例事实：** 容器共7个已有工作流，其中 `PY9w2v8FnZmj7nff`（N8N-DEPLOY-03｜Reasonix 本机成果闭环）`active=true`，POST `/webhook/n8n-deploy-03-task`，后续有本机Reasonix执行节点；`v27McpReadonly20261009`（V27-MCP-READONLY-DISCOVERY-20261009）`active=false`，入口为Manual Trigger，没有现成可直接外部POST的业务Webhook。**二者合同不同，不可当作同一浏览器竞速任务。**
**端口冲突诊断：** 对已运行容器执行 `docker exec n8n-local n8n execute --id=...` 报 `n8n Task Broker's port 5679 is already in use`，是该命令在运行容器内启动新的CLI执行上下文引发端口冲突，**并非n8n主服务离线，也不是授权错误**。不要停止现有服务、改端口或重建容器来“修复”此只读测试。改用已存在的正常触发入口；缺少匹配的合法入口时记录缺口，在获准范围内按成熟n8n功能对工作流做最小适配并单独验收。
**常驻健康标准：** docker健康 + 正确现有工作流激活状态 + 匹配其合同的获准触发 + 可回读最终业务结果；前两项不能代替后二项。断线按原DCR v0.3.1恢复流程处理，不修改FlClash或Windows代理。当前n8n服务在线且有一个可触发的历史Reasonix工作流，但“GPT↔n8n↔现有浏览器同任务竞速”仍`NOT_TESTED`。

## v0.3.2 变更摘要
- 增补n8n常驻调用入口的诊断和恢复规程；修复把401误判为服务故障、把CLI端口冲突误判为需要重授权的排障错误。
- 保留v0.3.1已验证的DCR/Actions双路结构、设备和执行器配置，未重建系统。
- 此为规范和现存入口的只读现场验收升级；n8n与浏览器同合同端到端竞速仍待Reality，不能宣称已经完成。

## 开源 B 通道隔离实验（2026-10-12，保留 v0.3.2 主体）
- 单独目录 `skills/windows-open-source-bridge-b/` 记录成熟开源组件组合、官方限制及本地真实证据；**不替换、不删除**本技能包原有 DCR 主路 / GitHub Runner 备路。
- Windows `C:\AI\GPT-Windows-Bridge-B` 安装成功：MIT 开源 Desktop Commander MCP 0.2.52，26 工具发现、真实目录工具调用及 PowerShell 标记回执通过；OpenAI Secure MCP Tunnel Client 0.0.16 官方 SHA256 验证与本地 CLI PASS。证据 run=38169533429。
- 月度配额为厂商 Remote Desktop Commander **托管**版限制，本地开源执行器不受这项厂商远程配额影响；但 OpenAI 自定义 MCP 权限和 Tunnel 身份验证独立存在，不可通过修改网络组件取消。
- 当前状态 `B_LOCAL_FUNCTIONAL=PASS / B_CHATGPT_END_TO_END=NOT_TESTED / B_FINAL_VALID=NO`。在官方权限允许并完成实际端到端验收前，保持已验证的 GitHub Runner 正式执行通路。禁止改 FlClash、代理和原自动启动任务。

- 2026-10-12 Reality 增量验收：run [38169679396](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38169679396)，Windows 本机 MCP `tools/call` 实测目录读取 + PowerShell 命令输出 + 隔离目录 `write_file → read_file` 内容回读，全部 PASS；OpenAI 完整 CLI 0.0.16 通过。仅本地调用闭环 PASS，不代表隧道已鉴权或 ChatGPT 远程端到端通过。`B_LOCAL_FUNCTIONAL=PASS / B_CHATGPT_REMOTE=NOT_TESTED / FINAL_VALID=NO`。

## v0.3.3 增量｜OpenAI Tunnel/ChatGPT 自定义 MCP 全链路恢复（2026-10-12）

**先读：** [OPENAI_TUNNEL_CONNECT_RECOVERY_20261012.md](OPENAI_TUNNEL_CONNECT_RECOVERY_20261012.md)；[证据与错误差分](evidence/OPENAI_TUNNEL_DEMO_REALITY_20261012.md)；[开源 Windows B 通道原安装/26 工具验收](../windows-open-source-bridge-b/README.md)。这三份是后续任何相关排障的**首选可回读来源**，不再靠聊天记忆猜测。

### 当日冻结状态与范围

```ini
TUNNEL_ID=tunnel_6acbeee2ce888191b775cd53429c7597
CLIENT=tunnel-client-v0.0.16-windows-amd64.zip
CLIENT_EXE=用户桌面\tunnel-client-v0.0.16-windows-amd64\tunnel-client.exe
TUNNEL_NAME=GPT-Windows-MCP-Bridge
WIN_DEMO_MCP=127.0.0.1:55999/mcp  # 本次动态端口
WIN_DEMO_READY=127.0.0.1:56000/readyz  # 本次动态端口，返回ready
CHATGPT_PLUGIN_AUTH=NONE_FOR_DEMO_ONLY
CHATGPT_PLUGIN_CONNECTED=PASS_USER_UI
ECHO_REALITY_PASS=USER_RELAYED_INDEPENDENT_PAGE_REPORT
ECHO_VALUE={"echoed":"hello from Windows"}
CHATGPT_REMOTE_WINDOWS_FILES_AND_SHELL=NOT_TESTED
OPENAI_TUNNEL_BOOT_AUTOSTART=NOT_TESTED
PRODUCTION_FINAL_VALID=NO
```

**运行记录：** 本次客户端日志 `🟢 tunnel-client started`、main MCP 会话初始化成功、Platform 隧道元数据获取成功、健康检查浏览器显示 `ready`。ChatGPT 页面 OAuth 注册最初提示「无法发现 OAuth 设置」，部分 Harpoon 注册报 `base URL must use https` / `unsupported channel "harpoon"`；只针对**无敏感能力的演示 mcp-stub**改为「无需身份验证」后，用户看到「已连接」，并从新页面转交了真实 `echo` 工具回执。由于主 `main` 通道可用，不能把 Harpoon 的局部告警认作整条隧道不可用。见证据文档。

**必须保留的选项差分：** 完整包 `tunnel-client-v0.0.16-windows-amd64.zip`（约26.8MB）而不是 `tunnel-client-runtime-...`（约7.2MB）；网页 `https://chatgpt.com/plugins` 的「添加自定义 MCP」而非已安装插件清单；连接方式「隧道」而非服务器 URL；隧道 ID 不是密钥；API Runtime Key 由 Windows 本地安全输入，不能发送聊天或写 GitHub。创建 Tunnels 时底部 GPT 工作区选项曾造成失败，这次未额外点击后成功：仅为本次UI经验，不意味着绕开权限。具体每一步、全部正确输入项、命令、回滚、故障树见恢复手册。

**安全与路由边界：** 演示服务使用「无需身份验证」**禁止**直接延用给真实 Windows 文件/Shell MCP。生产前必须建立合理的用户/工作区鉴权与操作审批、最小权限和允许目录策略。密钥截图曾选择「全部权限」「永不过期」，应核验并轮换为受限制 `Tunnels Read + Use`，不能把 Runtime Key 写到仓库。保留 DCR 主路/GitHub runner 备路与其当前稳定部署，不修改 FlClash/Windows 代理、浏览器、原自动启动；此新增线路尚非正式第三条生产路由。真实 Windows OpenAI Tunnel 远程读、写、Shell **未通过验收前不得写 FINAL_VALID=YES**。

**下一节点**：已安装的 `C:\AI\GPT-Windows-Bridge-B` 内开源 Desktop Commander MCP 0.2.52 真实本地 26 工具，采用官方 `tunnel-client init` 成熟配置模板对接其经过核验的 stdio/HTTP 启动命令；`doctor → run → ChatGPT 实际 tools/list → 只读 → 授权隔离写/命令 → 重启恢复`。这条生产迁移是**未执行候选**，不能把本次 demo 的 echo PASS 混同它的验收。

**证据可信度**：本次 echo 成功来自用户转交独立 ChatGPT 页的工具执行报告，而非本页面直接调用，因此 `ECHO_REALITY_PASS` 附 `USER_RELAYED` 来源标签；原始 PowerShell 和截图另行保留。禁止擅自提升级别。


## 2026-10-12 真正 Windows MCP 接入现场增量：STAGED，尚未远程验收

- 经 GitHub Runner 实际只读诊断 [run 38176840327](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38176840327)：`DESKTOP-4A1EGTM` 上开源 MCP 入口存在、OpenAI 完整 CLI v0.0.16 存在；原 `tunnel-client.exe` PID 42156 在交互会话 Session=11，`/readyz` HTTP200=`ready`；GitHub Runner 身份为 `NT AUTHORITY\NETWORK SERVICE` / Session=0。因此不能用 Runner 后台进程替代交互式 A 用户会话。
- 经 GitHub Runner 实际投放 [run 38177110566](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38177110566)：`C:\AI\GPT-Windows-Bridge-B\Launch-OpenAI-Real-MCP.ps1` 写入成功、语法检查通过、SHA256=`7F9688C62AEA418D3FA3919C007473EC0EDA4B0A90EA5BB6CEB81AFB3BE9DD07`，原 demo 保持运行、未读取或存储任何运行 Key。源脚本 `workspaces/extreme-time-automation-loop-v2.0/bridge/payloads/OPENAI-TUNNEL-REAL-MCP-STAGE-20261012.ps1`。
- 当前连接的自定义插件通过真实 `server_info` 工具调用确认仍只有 `echo/server_info/uppercase`，服务器 `mcp-stub 0.1.0`；**Windows 远端真实目录、文件写入、Shell = NOT_TESTED**。
- 通过插件权限只读检查，`GPT-Windows-MCP-Bridge` 当前为**App-specific Allow all actions（无需额外确认）**；在切换真实 MCP 前需明确获用户授权改为 `Always ask` 并落实安全控制，原 ChatGPT 插件仍选择「无需身份验证」且不适宜全系统长期开通。真实密钥只能由用户在交互 PowerShell 隐藏输入。
- 脚本 `-Launch` 会检查用户会话，显示高权限风险并请求输入 `YES`，再以隐藏输入方式获取 Runtime Key；仅当发现且确认原 demo 的同 Tunnel ID 进程时才安全停止原 demo 并运行真实 MCP。该**执行尚未发生**，故不得标 FINAL_VALID。切换后必须由 ChatGPT 刷新工具列表并实际远程完成只读、隔离写后读和无副作用命令，再更新验收状态。



## 2026-10-12 明确授权修正：保留自定义插件当前默认策略

- 用户明确同意 `GPT-Windows-MCP-Bridge` 继续使用 **`Allow all actions`（允许所有操作）＋「无需身份验证」**，**不需要**每次为该设置重新征求同意；仅在 OpenAI 平台的客观权限/兼容性/安全要求阻止时再提出必须调整的具体原因，不能擅自更改。此处批准适用用户本人已建立的隧道及设备，不表示向陌生用户开放访问。
- 关键区别：`Allow all actions` 是 **ChatGPT 端确认策略**；「无需身份验证」是 **MCP 服务端身份验证方式**；OpenAI Tunnel 客户端仍需要合法的 Platform Runtime Key 与隧道 `Read+Use` 访问权限。两个开关不等于隧道或 Windows 已经具备充分隔离；高权限远程 Shell 存在未授权访问和误操作风险，平台也可能限制部分工具。
- 之前要求必须改成 `Always ask` 的**启动脚本前置条件已撤销**，修复源码 `workspaces/extreme-time-automation-loop-v2.0/bridge/payloads/OPENAI-TUNNEL-REAL-MCP-STAGE-20261012.ps1`，并通过独立 GitHub Runner 节点更新 Windows 本地 `C:\AI\GPT-Windows-Bridge-B\Launch-OpenAI-Real-MCP.ps1`；源码提交 `441281cc0d928e953409a67c56341470efaf11c3`，部署任务 `OPENAI-TUNNEL-REAL-MCP-RESTAGE-AUTH-20261012`。启动仍需用户在自己 Windows 交互终端**隐藏输入 API Key**，不能由 ChatGPT 或 GitHub 工作流代填密钥。
- 切换/验收原则不变：同一 Tunnel 先验证再停 demo；真实 MCP `tools/list`、只读、隔离写后读、无副作用命令的远端真实回执之前 `FINAL_VALID=NO`；不得改动 FlClash、系统代理、已有浏览器、原 DCR/Runner 自启动配置。
- **安全声明**：上述是用户认可的便利性风险选择，并非推荐所有人默认关闭高权限 MCP 的认证，且不能绕过平台强制权限策略。


- **已复验完成的实际部署证据**：[GitHub Actions Run 38177972930](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38177972930)，任务 `OPENAI-TUNNEL-REAL-MCP-RESTAGE-AUTH-20261012`，Windows 回执 `REAL_TUNNEL_STAGE_PASS`，落盘 `C:\AI\GPT-Windows-Bridge-B\Launch-OpenAI-Real-MCP.ps1`，SHA256=`01DBE10E79F24975F0CC7CE05E936BFF2D41EAAB37EB0F33D2DCB0F0959547BC`。`DEMO_TUNNEL_LEFT_UNCHANGED=YES`，`NO_RUNTIME_KEY_USED=YES`。注意**仅脚本部署已验收**；用户交互式 `-Launch` 和 ChatGPT 远端真实 MCP 调用未进行。


## 2026-10-12 真实 Windows MCP 初次切换失败：PATHFIX（已重部署，远端验收待续）

- 用户在 A 交互会话实际执行 `C:\AI\GPT-Windows-Bridge-B\Launch-OpenAI-Real-MCP.ps1 -Launch` 并隐藏输入 Runtime Key；准确证据：2026-10-12 **05:54:12** 日志。原演示 tunnel PID `42156` 已按规则停止，真实目标 route 解析为 `transport=stdio`，但无法启动 MCP 子进程：`mcpclient: start stdio command: exec: "C:Program": executable file not found in %PATH%`，随后 `TUNNEL_REAL_MCP_EXIT_1`。这不是密钥/FlClash/隧道 ID 导致的失败。
- FIRST_DELTA：旧脚本使用 `$mcpCmd = '"' + $node + '" "' + $entry + '" --no-onboarding'`，其中 Node 在 `C:\Program Files\...`；隧道客户端的命令字符串解析对嵌套引号和 Windows 反斜杠不兼容，导致路径错误被读为 `C:Program`。
- 最小成熟修复：保留 `Get-Command node.exe` 核验；`$mcpCmd = 'node.exe ' + $entry.Replace('\','/') + ' --no-onboarding'`。只使用 PATH 可发现的 `node.exe` 和不含空格的 MCP 入口路径 `C:/AI/GPT-Windows-Bridge-B/mcp/node_modules/@wonderwhy-er/desktop-commander/dist/index.js`，不增加自研解析器，不改 PATH/代理，不复制敏感密钥。
- 源文件 [Windows MCP 启动器](../../workspaces/extreme-time-automation-loop-v2.0/bridge/payloads/OPENAI-TUNNEL-REAL-MCP-STAGE-20261012.ps1) 提交 `a9f78b62eff037f481087ed04ce984beb0f6a5c9`；通过已有 Runner 按 Exactly-once 单次重新部署 [run 38178400910](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38178400910)，Windows artifact 真实回执 `PASS`，`REAL_TUNNEL_STAGE_PASS`，新启动脚本落盘 SHA256=`34A1EF6DFB8F0D41A56106384A738D7F0BDF5C7AD8BB152EE4195CB1B53070DE`。自动工具调用尚未获得新的 `node.exe` stdio 实际运行结果，故标 `LAUNCHER_PATHFIX_STAGED=PASS; REAL_MCP_TUNNEL_REMOTE_FINAL=NOT_TESTED`。
- 原 demo 已经停止、旧窗口回到 PowerShell 提示符。必须在**相同 Windows 交互用户会话**重新运行已经部署好的 `-Launch` 脚本并安全输入 Runtime Key；运行成功后通过 ChatGPT 新会话重新发现真实 MCP 工具，实际读目录、隔离文件写后读、PowerShell marker。**不能**把修复版脚本投放成功误写成真实远程执行成功。

## 2026-10-12 06:02 真实 Windows MCP 的 stdio 启动 PASS；ChatGPT 工具目录待刷新

- 用户提供的新 PowerShell 日志证明先前 `C:Program` 路径故障已修复：`MCP_STDIO_COMMAND=node.exe C:/AI/GPT-Windows-Bridge-B/mcp/node_modules/@wonderwhy-er/desktop-commander/dist/index.js --no-onboarding`、`NODE_VERSION=v24.14.0`；`2026/10/12 06:02:45 INFO stdio MCP command started`；`health server listening 127.0.0.1:63623`；`2026/10/12 06:02:46 INFO 🟢 tunnel-client started`；`mcp_target_kind=stdio`，故 `REAL_WINDOWS_MCP_STDIO_START=PASS`。
- 本页面实际调用了旧插件接口 `GPT-Windows-MCP-Bridge.server_info`，取得 `Unknown tool: server_info`：指向**ChatGPT 保存的演示 MCP 工具目录已过时**，因为新服务不再含旧的 `server_info`。这不是新服务的真实 26 工具已被 ChatGPT 发现的证据。
- 官方：[ChatGPT 开发者模式与 MCP 应用](https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt)，服务器工具变更后要在自定义插件的设置中手动 `Refresh`（刷新工具），不能仅刷新浏览器/重复运行 echo；已有绑定不必重新创建隧道、Key。刷新后在新 ChatGPT 会话中检查真实 `list_directory`/ `read_file` / `write_file` / `start_process` 工具，并做有证据的远端隔离测试。
- 此次 `/readyz` 尚无新运行时的 HTTP 响应截图，且对 stdio 其 Ready 可能早于协议初始化；不能仅据启动 PASS 推断远端正式能力。当前 `REAL_MCP_PROCESS_STARTED=PASS`，`CHATGPT_REMOTE_WINDOWS_TOOLS=NOT_TESTED`，`FINAL_VALID=NO`。
- 请保持现有 Windows PowerShell 前台进程，不要第二次启动 `tunnel-client` 或更改 FlClash/代理。新管理 UI：`http://127.0.0.1:63623/ui`，本次动态端口仅对当前运行有效。

## 2026-10-12 正式 Reality｜ChatGPT 直连 Windows 真实文件读写及命令执行验收 PASS

**优先回读证据**：[OPENAI_TUNNEL_REAL_WINDOWS_REMOTE_PASS_20261012.md](evidence/OPENAI_TUNNEL_REAL_WINDOWS_REMOTE_PASS_20261012.md)。

- 原 `mcp-stub` 演示已被真实 `@wonderwhy-er/desktop-commander@0.2.52` 替换；用户 06:02 Windows 前台日志 `stdio MCP command started`、`🟢 tunnel-client started`。ChatGPT 插件 `GPT-Windows-MCP-Bridge` 手动刷新工具目录后，此对话实际看到真实 26 个工具。旧 `server_info` 返回 `Unknown tool` 的缓存故障已经解决，不需要新建隧道。
- **真实远程目录读取 PASS**：`mcp__GPT_Windows_MCP_Bridge__list_directory` 查询 `C:\AI\GPT-Windows-Bridge-B\evidence`，回显既有文件 `bridge-b-install-evidence.json`、`bridge-b-local-functional.json`、`b_mcp_write_read_probe.txt`、`npm-install.log`。
- **真实远程文件写后读 PASS**：`write_file` 在 Windows 隔离 evidence 目录写 `GPT_TUNNEL_REAL_REMOTE_R1_20261012.txt`，真实回执成功；随后 `read_file` 单独取回准确标记 `REAL_WINDOWS_REMOTE_FILE_WRITE_READ_PASS`。
- **真实远程 Windows PowerShell PASS**：`start_process` 运行 `Write-Output GPT_TUNNEL_REAL_WINDOWS_SHELL_PASS; whoami`，返回 `PID=29708`，标记及 `desktop-4a1egtm\a`；随后 `read_process_output` 真正回读 `exit code 0`（runtime 1.42s）。
- `REAL_WINDOWS_REMOTE_FUNCTIONAL_PASS=YES`、`SCOPE_FINAL_VALID=YES` **仅限用户要求的读取、隔离写回、命令执行最小闭环**。`REBOOT_AUTOSTART_REALITY=NOT_TESTED`，长期常驻、复杂业务、全 26 工具验收与安全评审均未完成，不混同。
- 用户已授权保持 ChatGPT 插件 `Allow all actions` 与 MCP「无需身份验证」，本次未改用户设置；但不能把这解释为公网裸露全系统执行权限的安全认证。继续保留两条原路由 DCR/Actions、FlClash、系统代理与已有浏览器。当前官方 Tunnel 前台 PowerShell 不可关闭；再次接续无需重跑演示测试。
