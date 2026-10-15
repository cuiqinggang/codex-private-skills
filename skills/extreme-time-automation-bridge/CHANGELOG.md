# CHANGELOG

## V6.0 / 6.0.0｜C正式首选、A间歇性退出继续溯源、B复用V3捷径（2026-10-15）

- 权威 `SKILL.md` 正式版号为6.0.0；**路由 C（Remote Desktop Commander）第一 > A（OpenAI Tunnel自建MCP）第二 > B（GitHub Windows Runner）第三**，覆盖旧版所有主路优先级。新版 [V6单页冻结与故障事实](V6_C_FIRST_A_RECOVERY_B_ROUTE_20261015.md)。
- C同机实际文件/命令/写读核对通过，用户授权后日常直接走C；不再频繁调取A的配置视图。C额度耗尽、设备离线或业务权限不符时再转A、B；非幂等执行遵守Exactly-once。
- B原FULL Run38736230206下载 Action ZIP首次100秒超时，最后成功；V3已有FAST日志回执及V2 BOUNDED 5/5（30至38秒）成熟绕开路线，V6正式禁止小型普通任务误派旧FULL。
- A现场Supervisor于19:32/19:42北京时间记录Tunnel自然退出并自动重启；当时Exit0/Exit1，但原子进程原始日志被弃，根因未确认；目前读文件恢复成功但不能认定已完整修复。禁止试验性停止唯一Tunnel、修改FlClash/代理、传递Runtime Key。
- 此次GitHub技能包及使用优先级已实际提交回读；**只冻结路由与故障事实，不把文档变更冒称Windows A运行态已修好**。保留V5及以前全部事故/回滚证据。


## V3.0 / 3.0.0｜B路历史下载故障收敛、限定5/5验收与成熟分流（2026-10-15）

- **原技能包原位升级**：`SKILL.md` 版本由 2.0.0 升级至 3.0.0，正式入口为 [V3.0 B路修复验收与分流规范](GITHUB_WINDOWS_B_ROUTE_V3_20261015.md)，A 自建隧道、B 原 FULL / FAST / V2 有界路线和 R 第三方额度闸门、历史证据都保留，不新建执行系统。
- **真实故障第一差分**：原 FULL 自托管 Windows Runner 在执行前准备 `actions/upload-artifact@v4` 代码 ZIP，历史 419/422 秒失败；此次利用成熟官方 Actions 双作业机制，将该 Action 下载上传移到 GitHub 托管 Runner，避免 Windows 出站 ZIP 长尾成为此小型证据任务的前置阻塞。**不是旧 FULL Windows ZIP 故障永久根治**。
- **V3 冻结事实**：B V2 有界官方 Artifact 五次独立成功 Run 38603199346、38603459215、38603580797、38603712945、38603850316；耗时36/36/30/36/38秒，平均35.2秒、范围8秒，原 Artifact 真正上传并由先前 Reality 独立回读。FAST Run38602210133 27秒成功但无官方 Artifact；FULL Run38601884050 97秒和 Run38602538548 144秒成功，原历史超时风险依旧。
- **生产操作门**：按证据合同选择 FAST / V2 有界 Artifact / 原 FULL；V2仅无敏感且容量已知的小型成功证据，失败证据保全与回调未等价验收；Base64 Job Output 有日志暴露风险，严禁传输敏感数据。Exactly-once；超限后不盲目再次派发副作用任务。
- **停止与独立验收**：停止为1–2秒无依据重构；保留 A 隧道初始化409、自恢复等未被本轮B路5/5覆盖的独立验收门；不改动 Windows Runner、隧道、FlClash、代理或工作流业务代码。此次 V3 是文档/路由操作指南发布，不冒称新运行时代码已完成新的五次回归。


## V2.0 B路 Reality 增量｜2026-10-15：成熟官方组件拆分及五次完成时间

- 使用《三人行》第2版（本任务指定，V2全局仍待审查）；原生产FULL实测Run 38601884050耗时97s PASS、Run38602538548耗时144s PASS，正式Artifact皆下载回读；不因短期PASS消除历史419/422秒ZIP超时失败。
- 既有无外部Action FAST 手工Run 38602210133成功27s，仅Job日志回执。
- 新增 `.github/workflows/windows-bridge-v2-bounded-artifact.yml` 作为隔离成熟组合候选（Windows本机执行+GitHub hosted官方Artifact上传，Job Output有限大小上限）；五次独立GitHub运行Run38603199346、38603459215、38603580797、38603712945、38603850316 **全部PASS**，耗时36/36/30/36/38s，均值35.2s；5份Artifact真实下载核对均PASS；原FULL第二轮Artifact追加回读PASS，合计6/6。原独立工作流不替换。
- **适用边界**：只有事先确定为小体积且无敏感stdout/stderr、容忍错误时无等价失败归档的任务才可使用；输出超限发生在执行后，不能把任务重发到原 FULL。任意大型输出、失败证据/回调等严格合同继续原 FULL；其 codeload/action ZIP 长尾稳定性未最终修复。
- **取证**：[GITHUB_WINDOWS_B_ROUTE_V2_REALITY_20261015.md](GITHUB_WINDOWS_B_ROUTE_V2_REALITY_20261015.md)，提交快照与Run ID可回读。FlClash、系统代理、旧Runner、原FULL、A直连、DCR原样保留，`THEORETICAL_PHYSICAL_LIMIT=UNKNOWN`，不误称无条件全面性能认证。


## V2.0 / 2.0.0｜Windows Tunnel 原生守护＋DPAPI 用户授权＋初始化分层验收（2026-10-15）

- **原包升级，不建重复包**：保留 A 自建官方 OpenAI Tunnel + 本地 MCP、B GitHub Actions Windows self-hosted Runner、R 第三方 Remote 额度运营、历史证据、原手动恢复与 GitHub FULL 工作流；统一正式版本为 V2.0。
- **核心 SOP**：[TUNNEL_AUTORECOVERY_V2_20261015.md](TUNNEL_AUTORECOVERY_V2_20261015.md)，分开认定网络瞬断后自行重连、主进程退出恢复、409 初始化条件、登录/重启恢复；不把本机健康探测等于真实 ChatGPT MCP 调用。
- **成熟技术复用**：Windows Task Scheduler 原生 AtLogOn/Interactive/IgnoreNew/RestartOnFailure、Windows 用户级 DPAPI、官方 tunnel-client v0.0.16（官方 `--mcp.stdio-send-initialized-notification` / `runtimes connect/status` 适用性已在本机确认）。官方受管实例尚未启用，避免同 Tunnel ID 双实例。
- **实际部署**：Windows `GPT-Windows-Tunnel-Recovery-v1` 已 Running，`Recovery-Supervisor-v1.ps1` 记录 `EXISTING_TUNNEL`，隧道唯一进程；桌面已建立 `GPT-Windows-AutoRecovery-OneTimeSetup.lnk`；00:33 Windows 只读检查 `KEY_ENROLLED=True`（仅证明加密文件存在，不读取密钥）。
- **无密钥脚本入库**：[bootstrap/Recovery-Supervisor-v1.ps1](bootstrap/Recovery-Supervisor-v1.ps1)、[bootstrap/Install-Recovery-Task-v1.ps1](bootstrap/Install-Recovery-Task-v1.ps1)、[bootstrap/Enroll-Recovery-Key-v1.ps1](bootstrap/Enroll-Recovery-Key-v1.ps1)。本机三份脚本语法 ParseErrors=0；未存凭据、用户密钥、环境变量值或用户加密文件到 GitHub。
- **严格未通过**：守护器仅凭已有进程存在做保守等待，尚未证明异常退出后使用 DPAPI 解密并自动新建隧道；未证明真实登录后可用；00:05 PID17876 未启用后来加到正式脚本的初始化 shim；两次连续远程 read_file 曾出现第2次 409，`409_FIXED=NO`；五次独立完整运行和长期稳定未通过。
- **安全边界**：不要求先关闭隧道重输 Key；用户一次性本机授权后应保留当前连接；不修改 FlClash/代理/浏览器/Runner/DCR，不恢复旧隔离 `Supervisor.INCOMPLETE.txt`；只有受控维护或自然退出后才做单次 Reality，拒绝盲目重复已执行任务。


## V1.0 / 1.0.0｜自建 MCP 主路＋GitHub 成熟备路性能差分（2026-10-13）

- 正式把 `SKILL.md` 由 v0.3.4 升级为 V1.0，保留旧版本所有验收、配额策略与恢复脚本不删除；采用《三人行》V2 的本任务按需成熟复用，不改变《三人行》方法全局激活状态。
- 新 [V1.0 运行/证据/安全文档](V1_GITHUB_WINDOWS_SPEED_AND_ROUTING.md)：原工作流上传 Action ZIP 100秒三次超时、原 84/156/419秒与最简 19～27秒对照，确认第一差异。
- 原 FULL `extreme-time-windows-bridge.yml` 不改，保留已有 artifact、静态合同、回调能力。新增 `windows-bridge-v1-fast.yml` 为手工触发的**隔离候选**，复用受版本锁定的任务 JSON＋原 Invoke-BridgeTask，省略外部 Action 下载，但尚未通过实际任务验收。
- 一次 FAST 自动触发测试提交遭安全检查阻断，未绕过；A 自建隧道在本轮调用 Session terminated。不得宣称 FAST 已完成实测或 A 当前在线。
- 第三方 Remote 免费配额闸门继续生效；真实 Windows 判路脚本在 v0.3.4 功能逻辑曾 15/15 PASS，升级版本字段没有替代现场再验。V1.0 不改变本机代理/FlClash/浏览器/Runner。


## v0.3.4 运行规则增量｜Remote 免费配额运营 V1.0 正式纳入（2026-10-13）

- **正式入口更新**：SKILL.md 顶部加入使用前必读/判路/违规提醒合同，并标明 10 月 12 日临时 GitHub 首选状态只是历史快照。
- **新可执行附则**：[REMOTE_DCR_QUOTA_OPERATIONS_V1.md](REMOTE_DCR_QUOTA_OPERATIONS_V1.md)：自建 A 快速交互、GitHub B 长/异步、官方托管 R 额度受控；6000/7500/8000/9500 四级门；在线≠可执行、官方用量≠本地 MCP 统计。
- **零副作用判路脚本**：[bootstrap/Invoke-Remote-Quota-Route-Gate.ps1](bootstrap/Invoke-Remote-Quota-Route-Gate.ps1)：输入已验证的通道状态、任务类型、官方余额与用户选路，输出路由+警告；不连接、不派发、不改本机配置；不声称自动拦截 ChatGPT 插件。
- **历史不覆盖**：2026-10-13 A 短任务实际 PASS，B 轻任务独立派发 PASS、复杂生产 B 的历史故障仍需独立修复；Remote who_am_i=0%。保留 v0.3.4 版本号与原执行器/隧道/代理/浏览器，不重建。
- **验收门**：测试 R=0、R=6000、R=8000、R=9500、A/B可用/不可用和误选 R 等规则，再称静态判路通过；重启、长时等运营表现仍需 Reality。


## v0.3.4 月度用量/自建通道路由增量（2026-10-12 晚）

- **路由优先级明确调整**：现在优先使用自建 GitHub 共同工作区 → Actions → Windows Runner；OpenAI 官方 Tunnel + 用户本机开源 MCP 接入恢复正常后也可使用；第三方托管 Desktop Commander Remote 只在配额充足、能力合适时作为补充。原 A/B 路、设备和技能包历史全部保留，无删除、无重建、无改变 FlClash/系统代理。
- **第三方用量到顶并非掉线**：DCR 设备 `f6990966-5870-484b-bf79-409bc6fb963e` 仍 Online，Ping 真正 `pong`，但远程命令因 `You've reached this month's Desktop Commander usage` 被服务端暂停。停止重复调用或重配，用户目标 `2026-11-01` 复查月度配额是否续用。个人体验“约半个月能用”仅为观察，不是每月保底或厂商重置承诺。
- **自建 GitHub 端到端最新 Reality**：[Run 38240277230](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38240277230) 已执行新 Windows 任务 `BRIDGE-LINK-CHECK-20261012-1901`，`result.status=PASS`、`exit_code=0`、`DESKTOP-4A1EGTM-etal`，`GH_TO_WINDOWS_REALITY_PROBE_PASS`；Runner 服务 Running/Auto。
- **OpenAI Tunnel 当前不是 PASS**：自定义 MCP 调用 `Session terminated`；上述 Windows 自建 Runner 首次报告 `OPENAI_TUNNEL_MATCH_COUNT=0`。文件检查 R1 [Run 38240736338](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38240736338) 因 `NETWORK SERVICE` 无权读取 A 桌面快捷方式而 FAIL，不能误判为文件坏；隔离此权限边界后的只读 R2 [Run 38241065083](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38241065083) 完整 PASS，正式 launcher、Tunnel EXE、MCP 入口、恢复/显隐脚本均存在且 PowerShell ParseErrors=0，`TOTAL_TUNNEL_CLIENTS=0`、旧 PowerShell PID27920不存在；恢复仍需用户本机 Runtime Key 输入，未擅自保存凭据或绕过既有限制。
- **新增规则**：[ROUTE_PRIORITY_QUOTA_AND_FAILOVER_20261012.md](ROUTE_PRIORITY_QUOTA_AND_FAILOVER_20261012.md)，记录同日证据、2026-11-01 复查日期、额度性质、三个入口状态、Exactly-once 规则及恢复边界；更新正式 `SKILL.md` 和旧双路策略页，保留 v0.3.4 以前全部历史。


## 0.3.4 - 2026-10-12｜现有 Windows 隧道静默隐藏 PASS、恢复入口与历史成熟机制沉淀

- **操作事实**：GPT-Windows-MCP-Bridge 通过真实 Windows 工具读取原进程 `tunnel-client.exe` PID23692、父 PowerShell PID27920，校验控制台窗口句柄和归属；使用 Windows 原生 `ShowWindowAsync(SW_HIDE)` 在不停止进程的前提下隐藏现有窗口。实际回执 `BEFORE_VISIBLE=True / AFTER_VISIBLE=False / TUNNEL_ALIVE=True`。独立再次回读 `TUNNEL_COUNT=1`、远程 Shell 仍可用。**仅当前会话隐藏 PASS**。
- **可逆工具已落盘**：桌面 `GPT-Windows-MCP-Show-Console.lnk` + `C:\AI\GPT-Windows-Bridge-B\persistence\Show-Current-Tunnel-Console.ps1`；文件、目标和语法预检 PASS，实际双击未执行。该脚本绑定当前 PID/窗口句柄，未来不能盲目照抄。
- **保留手动恢复**：桌面 `GPT-Windows-MCP-一键恢复.lnk` + `Restore-Interactive.ps1`；已有防重复运行真实回执；本地需要人工输入 Runtime Key，双击与重启后均尚未 Reality。
- **旧成熟方案回读**：现有 `Codex_SystemEvolution_24h.vbs` 使用 `WScript.Shell.Run(...,0,False)`；`GPT-LTMVH-Recovery-Watchdog.cmd` 使用 `start /min -WindowStyle Hidden`；原 `GPT-DesktopCommander-Remote-Autostart` 是 DCR Remote 的 Logon/Interactive 计划任务。与新 OpenAI Tunnel 自启动严格区分，旧机制不删除。
- **兼容性差分**：中文快捷方式创建器 `Make-Manual-Shortcut.ps1` 使用 UTF-8；Windows PowerShell 5.1 解析出现 2 错（编码），PowerShell 7 同文件解析 0 错。保存三份真实 Windows 脚本的本地 SHA256 与完整证据快照，避免以后凭记忆重造。
- **未通过项如实保留**：`TUNNEL_LOGIN_AUTOSTART=NOT_IMPLEMENTED`、`REBOOT_RECOVERY=NOT_TESTED`、`SHOW_SHORTCUT_DOUBLECLICK=NOT_TESTED`；现有 `Read-Host -AsSecureString` 仍要求本机 Key，简单藏窗口不能替代凭据来源。DPAPI + 隐藏 Supervisor 旧候选曾被安全拦截，继续禁止规避并保留隔离残件。
- **文档结构**：新增 [标准操作手册](TUNNEL_WINDOW_VISIBILITY_AND_RECOVERY_20261012.md)、[Windows 原始实测和脚本 SHA 快照](evidence/OPENAI_TUNNEL_WINDOW_VISIBILITY_REALITY_20261012.md)；同步更新 `SKILL.md` 首页状态、原状态文件和原全流程恢复入口。其余 v0.3.0–0.3.3 内容保留。
- **不会发生的变更**：不删除旧 A/B 路、不修改 FlClash/Windows 代理、不改已登录浏览器、不新建 Tunnel 专属登录任务、不触碰 Runtime Key、不重启现有 Tunnel。v0.3.4 **是技能包和证据升级**，不是自动开机服务的部署结果。


## 0.3.3 - 2026-10-12｜OpenAI Secure MCP Tunnel 自定义插件接入与恢复

- **保留**原 DCR Remote 主路 / GitHub Actions self-hosted Runner 备路，且不重建旧配置。
- 增加 `OPENAI_TUNNEL_CONNECT_RECOVERY_20261012.md`：从 OpenAI Platform 隧道创建、工作区选择陷阱、完整 Windows amd64 安装包与 runtime 误选、CLI quickstart、Runtime API Key、PowerShell 原始启动命令、本地 readyz、ChatGPT 插件创建、身份验证选项、连接和真实 echo 工具回执的逐步操作。
- 增加 `evidence/OPENAI_TUNNEL_DEMO_REALITY_20261012.md`：原 PowerShell 日志决定性证据、`harpoon` 局部错误与 `main` 通道差分、浏览器 `ready`、用户转交独立页 `echo` 报告；不保存秘密密钥。
- 修复旧错误判断：`unsupported channel "harpoon"` 和 `target_count=0` 不足以推翻已可用的 `main` 演示 MCP 通道；demo 切换无身份验证后远端 echo 实际成功。警告保留以便后续真实 OAuth 诊断。
- 状态严分：`TUNNEL_DEMO_ECHO=PASS_USER_RELAYED`；`CHATGPT_REMOTE_REAL_WINDOWS_MCP=NOT_TESTED`；`PRODUCTION_FINAL_VALID=NO`。正式 Windows 读写、PowerShell、重启常驻和授权须单独 Reality。
- 安全：Demo「无需身份验证」不得用于具 Windows 命令/文件权限的真实 MCP；Runtime Key 应轮换到最小 `Tunnels Read+Use`；严禁把 Key 写入仓库；FlClash、系统代理、已登录浏览器及原自启动原样保留。

## 0.3.0 - 2026-10-03

- 正式升级为 GPT直连Windows双路执行桥 v0.3.0。
- 新增 Desktop Commander Remote 离线/配置损坏后的最短重配恢复法。
- 本轮真实故障症状：Failed to initialize config、Unexpected token ... is not valid JSON；此前还出现过 Lock file is already being held。
- 修复策略冻结：停止旧自启/残留实例 → 备份损坏配置与旧 Remote 身份 → 重新运行 npx -y @wonderwhy-er/desktop-commander@latest remote → 原 Google 账号重新授权/配对 → 外部独立验收。
- 新配对 Device ID：503e66bf-4f80-49fc-a90f-020ec8c71b1e，DESKTOP-4A1EGTM Online。
- Reality：独立 ping PASS；真实 Windows 命令 PASS。
- 旧 Device ID 28ebd1ea-e749-466d-ad88-1b9f262d0651 保留为 Offline 历史记录。
- 新增强制验收门：startAttempted=true、进程存在、计划任务成功都不能单独判定恢复；必须 Online + ping PASS + Windows 命令 PASS。
- 新增 A 用户后台 launcher：C:\Users\A\AppData\Local\DesktopCommanderRemote\Start-DesktopCommanderRemote.ps1。
- 计划任务 GPT-DesktopCommander-Remote-Autostart 已启用；AtLogOn、Interactive、MultipleInstances=IgnoreNew。
- launcher 在 Remote 退出后等待 5 秒自动重启。
- 尚未执行真实 Windows 重启 Reality，因此开机自动恢复标记 NOT_YET_TESTED。
- 新增 DCR_RECOVERY.md，作为以后 DCR 断线时的第一恢复入口。

## 0.2.0 - 2026-10-02
- 建立 Desktop Commander Remote 主路 + GitHub Actions self-hosted runner 备路。

## 0.3.3 用户授权增量 - 2026-10-12
- 明确获用户同意：保留 `GPT-Windows-MCP-Bridge` 的 `Allow all actions` 和 「无需身份验证」选项，不将「必须改为 Always ask」作为启动前置条件。高权限风险和平台可能强制限制仍明确披露。
- 改动正式真实 Windows MCP 切换脚本并经 GitHub Runner 部署（复验状态以 Actions 记录为准）；密钥继续仅由用户在本机输入。
- Windows 主运行隧道尚未主动切换，真实远端读、写、命令仍待正式调用验收。

## 0.3.3 Reality 增量 - 2026-10-12｜真实 Windows 远程执行闭环

- 修复 `--mcp.command` 在 Windows 的 `C:Program` 路径解析问题；PowerShell 06:02 客户端真实成功启动 stdio MCP。
- ChatGPT 插件手动刷新工具目录后，真实发现 Desktop Commander MCP 26 个工具；直接调用 `list_directory`、`write_file`、`read_file`、`start_process`、`read_process_output` 取得真实 Windows 回执。PowerShell exit code 0，身份 `desktop-4a1egtm\a`。
- 证据文件：[`evidence/OPENAI_TUNNEL_REAL_WINDOWS_REMOTE_PASS_20261012.md`](evidence/OPENAI_TUNNEL_REAL_WINDOWS_REMOTE_PASS_20261012.md)。
- `SCOPE_FINAL_VALID=YES` 仅指真实文件读写与命令执行；重启自动恢复、无人值守常驻、并发压力以及生产安全隔离仍 `NOT_TESTED`，不得夸大。
