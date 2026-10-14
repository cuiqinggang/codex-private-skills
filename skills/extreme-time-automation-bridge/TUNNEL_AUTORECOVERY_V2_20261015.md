# GPT直连Windows双路执行桥 V2.0｜成熟恢复与初始化规范（2026-10-15）

**范围**：原有 A=自建 OpenAI Tunnel + Windows Desktop Commander MCP（默认交互主路）；B=GitHub Actions + Windows self-hosted Runner（独立备路）；R=第三方 Desktop Commander Remote（配额闸门）。在原有技能包内升级，不重建隧道、不替换 B 路、不重造协议栈。

**唯一结论**：部署成熟的 Windows 任务计划程序 + Windows 用户级 DPAPI（本机加密凭据）+ 官方 tunnel-client + 已有 Watch-Tunnel-Health.ps1。**是否通过实际自恢复验收，要看进程更替和 ChatGPT 真实 read_file，而不是任务存在或 localhost ready。**

## 1. 给用户的最短操作（无需先断线）

1. 保留当前正常的 tunnel-client 进程，**不要先关闭连接**，不要再进行暂停/防火墙定向断线实验。
2. 首次授权才双击 Windows 桌面 `GPT-Windows-AutoRecovery-OneTimeSetup.lnk`，仅在本机的交互式窗口输入一次现有 Runtime Key。**不在聊天、仓库、日志提供密钥**。此步骤保存的只是当前 Windows 用户 DPAPI 加密文件，路径 `%LOCALAPPDATA%\GPT-Windows-Tunnel\runtime-key.dpapi`。若加密文件已存在，无须重复输入。
3. 恢复计划任务 `GPT-Windows-Tunnel-Recovery-v1` 负责**已登录的 Windows 用户 A 会话内**启动/守护：发现任何现有 tunnel-client 就保留，进程不存在且有合法凭据才可恢复，明确禁止同 Tunnel ID 双实例。
4. 保留旧手动恢复快捷方式 `GPT-Windows-MCP-一键恢复` 作为回退；如自动恢复异常，先看进程/任务/健康日志，再决定是否手动恢复。**不得同时启动两套进程管理器。**

## 2. 选型：成熟组件，不扩容自制系统

| 职责 | 复用成熟组件 | 当前实际状态 |
|---|---|---|
| 正式连接 | OpenAI `tunnel-client.exe v0.0.16`，原 Tunnel ID / stdio MCP | 原连接已在运行；运行期 409 曾复现 |
| 守护/登录 | Windows Task Scheduler：AtLogOn、Interactive、IgnoreNew、任务失败重启；额外 5 分钟触发检查 | 本机计划任务已注册并 Running（2026-10-15 00:24+08） |
| 凭据 | Windows PowerShell `ConvertFrom-SecureString` 默认 DPAPI，限定当前用户；ACL 收紧 | 本机路径 00:33+08 检查到加密文件存在；未读取密钥，也未验证异常退出后解密重连 |
| 状态 | `Watch-Tunnel-Health.ps1` 与既有每 5 分钟健康日志 | 单次健康信息 PASS，但不能替代远程 tools/call |
| 原生受管运行时 | 官方 `tunnel-client runtimes connect/status --json` 支持 stdio | 本机 CLI 已确认支持，`runtimes list --json` 为空；**未启用**，不得与当前独立守护并行 |
| MCP 初始化 | 官方 `--mcp.stdio-send-initialized-notification` | 启动脚本包含该参数，但 00:05 创建的 PID17876 未带参数；待下次合法启动后实测 |

官方文档：Windows Task Scheduler RestartOnFailure <https://learn.microsoft.com/en-us/windows/win32/taskschd/taskschedulerschema-restartonfailure-settingstype-element>；Windows DPAPI <https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/convertfrom-securestring>；官方 Tunnel stdio/409 <https://github.com/openai/tunnel-client/blob/master/docs/configuration.md>；官方受管运行时 <https://github.com/openai/tunnel-client/blob/master/plugins/tunnel-mcp/skills/tunnel-mcp/references/runtime-flows.md>。

**方案取舍**：已注册的 Task Scheduler 负责 Windows 登录与本机守护。官方 `runtimes connect` 是官方推荐的进程生命周期管理方案，宜在后续**单独切换且验收**后择优采用；不能在现有同 Tunnel ID 的 `run` 旁启动第二份官方受管实例。两套管理器同时启动禁止。

## 3. Windows 现场定位与已部署文件

- 主机：`DESKTOP-4A1EGTM`；同一 Windows 交互用户 `A`；原 Tunnel ID：`tunnel_6acbeee2ce888191b775cd53429c7597`。
- 正式连接根目录：`C:\AI\GPT-Windows-Bridge-B`。
- 原正式启动器：`Launch-OpenAI-Real-MCP.ps1`，现有 SHA256 = `B825462C8C0E94194B6022B60035BA6D0E6A0E5F7C016FF346540A059744BA35`（00:14 时的快照；如后续内容变化以现场为准）。
- 新增而非覆盖的本地文件：`persistence\Recovery-Supervisor-v1.ps1`、`persistence\Install-Recovery-Task-v1.ps1`、`persistence\Enroll-Recovery-Key-v1.ps1`。
- 守护日志：`persistence\Recovery-Supervisor-v1.jsonl`；既有只读健康日志：`persistence\Tunnel-Health.jsonl`。
- 新桌面快捷方式：`GPT-Windows-AutoRecovery-OneTimeSetup.lnk`，**只负责本机首次输入并 DPAPI 保存**；不作为停止/重启连接的按钮。
- 00:33 现场静态证据：三个脚本各 ParseErrors=0，恢复任务 Running，TunnelCount=1，加密凭据文件存在。脚本 SHA256 详见本节末尾。**这些结果不是异常退出自动恢复/开机自启或 409 补丁的端到端成功证据**。

已部署脚本的本机 SHA256：Supervisor `D5B2D1098F51794E296233DEBD1E8F07AB71A3690525E014D84FC0644726B434`；Task Installer `10857F5DAC0927FFF2CB9BD9697612BCD4FEB09C6270943ACF8EBD2F212FC8DD`；DPAPI Enrollment `424C9B8F947B1ACA184BCB84E757886E34143A35CB07FCBD7822A5C6EAEBEE9C`。

**注意**：当前守护器的 `EXISTING_TUNNEL` 路径只看进程存在，不会因 409、健康退化或僵死进程而盲目杀进程。这是刻意的安全限界。之前 `Supervisor.INCOMPLETE.txt` 为隔离的旧失败方案，不得当作新版脚本执行。凭据文件绝不能上传到 GitHub。

## 4. 一条简单的故障树

1. **仅偶发网络波动，原进程还在**：不重启，不动 FlClash/系统代理，允许自然恢复控制平面；恢复后通过真实远程文件读取验收。网络本身短时失败不等于协议 bug。
2. **主进程不存在/前台窗口被关闭**：守护器在用户 A 已登录、密钥可合法解密的前提下可尝试启动官方进程；必须记录新的 PID、创建时间、退出日志，再做真正的远程调用。当前此分支**尚未实际验收**。
3. **进程还在却返回 `409 mcp_initialization_required`**：这是 MCP 初始化时序条件异常，不当作单纯进程退出处理。官方 stdio guard 要求旧式调用前成功 `initialize` 并收到 `notifications/initialized`；shim 仅在成功 initialize 后补发通知，不会伪造 initialize。记录请求时间、PID、child_generation、initialize_epoch、原始错误，定位 FIRST_DELTA。不能靠显示健康状态判定已修好。
4. **GitHub 独立备路**：A 不可用时用原 B 路诊断/执行，保持 Exactly-once；不会将 DCR 额度耗尽误判为网络故障；禁止无证据重复有副作用任务。

## 5. 验收（有证据才 PASS，避免为了测试而测试）

| 门 | 最小必要验证 | 截至本次状态 |
|---|---|---|
| G0 已部署 | 任务 Running、唯一 tunnel、脚本 ParseErrors=0、无代理更改 | PASS（配置/静态与局部现实） |
| G1 本机凭据 | 加密文件存在；在相同已登录用户计划任务上下文里**可用** | 文件存在 PASS；任务实际解密使用未验收 |
| G2 旧会话不受影响 | 安装任务后仍能真实调用 MCP；无第二进程 | 单次已有通过；仍发生过独立 409 |
| G3 自动恢复 | 在受控维护或自然异常退出后，无人工输入密钥，出现唯一新 PID、MCP 初始化成功、真实远程调用恢复 | **NOT_TESTED**；不能因手动重连成功而填 PASS |
| G4 初始化兼容 | 确认新启动 PID 真正带 shim 标志；连续同构只读 8/8、独立操作 5/5，按原合同记录异常 | **NOT_TESTED**；历史 8 次有 1 次 409 |
| G5 登录/开机 | 实际重登录/重启后无重复进程、可远程读文件 | **NOT_TESTED** |
| 长时稳定 | 后续自然运行证据；可恢复的网络波动与协议错误分开统计 | **NOT_ACCEPTED** |

**优先顺序**：保留当前正在运行的连接；不主动断线；用户完成一次性授权后，先做非破坏性读/健康监测。后续维护窗口只做一次可回滚的进程生命周期 Reality，再执行必要同构调用；发生首例失败即记录原始证据并停止机械复测。不能把 5 次同一会话短读冒充 5 个独立运行周期。

## 6. 回滚与安全

- 如果守护策略自身异常，在确保运行隧道仍存活时，可先禁用 `GPT-Windows-Tunnel-Recovery-v1` 任务、保留原人工恢复入口；不要停止当前健康的进程。恢复计划任务名称仅适用于本机，不影响原 DCR 或 GitHub Runner。
- 已经部署的守护器不会改变 FlClash、代理、浏览器、第三方 DCR 与 GitHub Runner，也不抓取已运行进程的密钥；所有凭据只由用户本机交互输入。
- DPAPI 加密文件属于敏感凭据，即使加密也应限制文件 ACL。不得输出密钥内容/日志，亦不得上传仓库或附在报告里；Windows 用户配置丢失/更换账户时需重新授权。
- 当前自定义 MCP 插件沿用用户历史选择的高权限/无需额外认证配置，**不因此获得生产安全认证**；需要严格控制隧道、账号和执行权限。原安全记录保留，不抹掉此前受阻的方案或安全限制。
- **最终状态**：`SKILL=V2.0`; `PLANNED_ARCHITECTURE=FROZEN`; `WINDOWS_WATCHDOG=DEPLOYED_RUNNING`; `KEY_FILE=EXISTS`; `AUTO_RECONNECT_REALITY=NOT_TESTED`; `MCP_409_FIX=NOT_VALIDATED`; `FINAL_VALID=NO`。
