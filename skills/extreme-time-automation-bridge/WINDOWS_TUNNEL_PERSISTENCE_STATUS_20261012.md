# Windows OpenAI Tunnel 后台常驻与快速恢复：2026-10-12 现场状态

所属正式技能：GPT直连Windows双路执行桥 v0.3.4。以下保留了 v0.3.3 时代的原始历史记录；**最新状态以文末「v0.3.4 Freeze」为准**。详见 [正式显隐/恢复手册](TUNNEL_WINDOW_VISIBILITY_AND_RECOVERY_20261012.md) 和 [原始 Reality 证据+脚本SHA](evidence/OPENAI_TUNNEL_WINDOW_VISIBILITY_REALITY_20261012.md)。

## 真实验收结论

- REAL_WINDOWS_REMOTE_FUNCTIONAL=PASS：此前通过新连接的 MCP 插件实际完成 Windows 目录读取、隔离文件写后读、PowerShell 标记输出及退出码 0。
- AUTOSTART_AND_HIDDEN_SUPERVISOR=NOT_IMPLEMENTED：自动隐藏常驻尚未配置，也没有通过真实 Windows 开机/登录后自动恢复验收。
- MANUAL_DESKTOP_RECOVERY=STAGED：已创建桌面快捷方式，目标与脚本均存在；快捷方式尚未经过用户双击验收。
- **隐藏前的历史告知**：正常工作的前台 PowerShell 原来必须保持窗口打开，可以最小化。**后续已验证使用 SW_HIDE 隐藏窗口而不结束进程**，现在可以没有可见窗口；仍然**不得关闭其进程/控制台宿主**，更不能把它称为 Windows 服务或重启自动恢复。

## 已真实执行的预检

目标 Windows 电脑 DESKTOP-4A1EGTM，用户 A，交互会话 Session 11。
PowerShell 7 路径 C:\Program Files\PowerShell\7\pwsh.exe。
官方 tunnel-client.exe 与开源 Desktop Commander MCP index.js 都存在。
Windows Register-ScheduledTask 命令可用。
原运行隧道 PID=23692，进程命令行确实绑定 ID tunnel_6acbeee2ce888191b775cd53429c7597。
未修改 FlClash、代理、DCR Remote、GitHub Runner 或原自动启动任务。

## 自动隐藏后台候选为何未部署

原计划使用 Windows 任务计划程序以用户 A 身份登录时启动，利用 Windows 当前用户 DPAPI 加密保存 Runtime Key，用官方 tunnel-client.exe 隐藏运行并提供重试与健康检查。

在写入包含密钥解密和隐蔽后台常驻动作的脚本时，当前执行环境触发了明确的安全检查拦截。已经停止该项动作，不通过其他渠道规避拦截。之前写入的无效 Supervisor.ps1 片段已在 Windows 真实重命名为：

C:\AI\GPT-Windows-Bridge-B\persistence\Supervisor.INCOMPLETE.txt

它不会作为脚本被计划任务执行。实际没有创建 GPT-Windows-Tunnel-Autostart 任务，没有保存 Runtime Key，也没有宣称自动常驻成功。

## 已经完成的明天快速恢复入口

实际写入到 Windows：

- C:\AI\GPT-Windows-Bridge-B\persistence\Restore-Interactive.ps1
- C:\AI\GPT-Windows-Bridge-B\persistence\Make-Manual-Shortcut.ps1
- C:\Users\A\Desktop\GPT-Windows-MCP-一键恢复.lnk

通过 PowerShell 7 实际运行快捷方式创建器，得到 SHORTCUT_CREATED，TARGET_EXISTS=True 与 LAUNCHER_EXISTS=True。
通过原 MCP 工具再次读取目录，确认这两个完整脚本与已重命名的 INCOMPLETE.txt。
第一次使用 Windows PowerShell 5.1 运行 UTF-8 中文快捷方式创建器时发生编码/语法解析错误；改用已安装的 PowerShell 7 对相同脚本运行后实际 PASS。

双击该快捷方式时：
1. 检查 Tunnel ID 对应的 tunnel-client 进程，已运行则显示状态，不启动重复进程。
2. 未运行则复用已经验收的正式 Launch-OpenAI-Real-MCP.ps1 -Launch 入口。
3. 只在本机提示输入已有 OpenAI Runtime API Key，不写入聊天或 GitHub。
4. 看到 stdio MCP command started / tunnel-client started 后保持出现的 PowerShell 窗口运行；窗口可以最小化。
5. ChatGPT 如果未识别真实工具，通过已安装插件的 Refresh 更新工具清单。
6. 真实双击及重启后的效果尚未验收，因此状态只能写 CREATED_UNTESTED_DOUBLECLICK。

原来的完整恢复手册：同目录 OPENAI_TUNNEL_CONNECT_RECOVERY_20261012.md。
原来的远程工具正式验收：evidence/OPENAI_TUNNEL_REAL_WINDOWS_REMOTE_PASS_20261012.md。

## 安全边界

用户明确选择继续使用 Allow all actions（允许所有操作）和 MCP 无需身份验证；这与无人值守、全权限 Windows Shell 叠加时构成额外安全风险。该便利性选择不等于自动后台常驻的身份/凭据安全检查已经通过。更完整的自动启动方案应先满足平台授权、端点访问限制、加密凭据、Windows 用户身份隔离，以及真实登录/断线后的远程工具调用验证。不能修改网络代理或绕过访问控制。

## Freeze

TASK=WINDOWS-TUNNEL-PERSISTENCE-20261012
SKILL_VERSION=0.3.3
TUNNEL_ID=tunnel_6acbeee2ce888191b775cd53429c7597
READ_WRITE_SHELL_REMOTE=PASS
CURRENT_INTERACTIVE_RUNTIME=RUNNING_AT_LAST_PROBE
LOGIN_AUTOSTART=NOT_IMPLEMENTED
HIDDEN_SUPERVISOR=NOT_IMPLEMENTED
REBOOT_RECOVERY=NOT_TESTED
MANUAL_SHORTCUT=CREATED_BUT_NOT_DOUBLECLICK_TESTED
API_KEY_STORED=NO
NEXT=Keep current PowerShell running; after reboot double-click desktop recovery shortcut and enter Runtime Key locally


## 2026-10-12 追加现场验证：当前控制台已隐藏（不是开机自启动）

已用已连接的 GPT-Windows-MCP-Bridge 实际读取 Windows 文件与进程状态，不是虚拟验证：

- 历史成熟机制：登录启动目录中存在 `Codex_SystemEvolution_24h.vbs`，使用 `WScript.Shell.Run(..., 0, False)`，将 PowerShell 窗口隐藏；另有已运行的 `GPT-DesktopCommander-Remote-Autostart`，实际触发器为 Logon、用户登录模式 Interactive。
- 当前官方隧道 PID=23692，父进程 `powershell.exe` PID=27920。父进程拥有可见控制台窗口。
- 对**已经正常运行**的父进程窗口，用 Windows 标准 `ShowWindowAsync(handle, SW_HIDE)` 隐藏窗口，实际得到 `BEFORE_VISIBLE=True`、`AFTER_VISIBLE=False`、`TUNNEL_ALIVE=True`。没有关闭 PowerShell、没有杀进程、没有重启隧道、没有修改 FlClash/代理。
- 为避免隐藏后无法找回，Windows 本机已写入 `C:\AI\GPT-Windows-Bridge-B\persistence\Show-Current-Tunnel-Console.ps1`，并创建桌面 `GPT-Windows-MCP-Show-Console.lnk`。恢复脚本语法解析错误数为 0，桌面快捷方式与脚本存在；**实际双击恢复尚未测试**。此入口只适用于当前 PID/窗口句柄，不是跨重启恢复程序。
- 已复核 `Launch-OpenAI-Real-MCP.ps1` 每次用 `Read-Host -AsSecureString` 从本机人工读取 OpenAI Runtime API Key，且不持久化密钥。因此，**隐藏窗口成功不意味着重新开机后可以无输入自动建立隧道**。不能直接在隐藏的 PowerShell 中启动这段交互脚本，否则密钥提示会不可见。
- 以前的凭据解密 + 隐藏持久化 Supervisor 方案曾遭执行环境安全阻止：本轮没有规避安全检查、没有保存密钥、没有注册新的隧道自动登录任务。

### 下一次真实开机验收

登录 Windows 后：①检查能否无命令行窗口启动；②确认隧道唯一进程和对应 Tunnel ID；③实际调用一次远程 MCP echo/只读命令；④确认无重复进程；⑤若失败，使用现有桌面 `GPT-Windows-MCP-一键恢复`，本机人工输入 Runtime Key。不可将「当前窗口已隐藏」填为「重启后自动恢复 PASS」。

CURRENT_RUNNING_CONSOLE_HIDDEN=PASS
CURRENT_TUNNEL_ALIVE_AFTER_HIDE=PASS
REVERSIBLE_SHOW_CONSOLE_SHORTCUT=CREATED_UNTESTED_EXECUTION
LOGIN_AUTOSTART=NOT_IMPLEMENTED
REBOOT_RECOVERY=NOT_TESTED
RUNTIME_KEY_PERSISTED=NO


## v0.3.4 Freeze｜旧记录继续保留，以下为最新权威判定

**可回读正式材料：** [SKILL v0.3.4](SKILL.md)、[显隐与恢复 SOP](TUNNEL_WINDOW_VISIBILITY_AND_RECOVERY_20261012.md)、[Windows 实测和 3 个原始脚本 SHA256 快照](evidence/OPENAI_TUNNEL_WINDOW_VISIBILITY_REALITY_20261012.md)、[CHANGELOG](CHANGELOG.md)。

本页面通过 **已连接的 Windows MCP 插件** 实际读取旧登录文件夹 `Codex_SystemEvolution_24h.vbs`（`WScript.Shell.Run(...,0,False)`）、`GPT-LTMVH-Recovery-Watchdog.cmd`（`start /min -WindowStyle Hidden`），以及现有 `GPT-DesktopCommander-Remote-Autostart`（Logon/Interactive）。确认 Windows 成熟隐藏策略早已存在；该任务**属于旧 DCR**，不是 OpenAI Tunnel 新增任务。

随后实际用 `ShowWindowAsync(SW_HIDE=0)` 对既有控制台执行，回读 `BEFORE_VISIBLE=True / AFTER_VISIBLE=False / TUNNEL_ALIVE=True`，经新一轮真实 Windows MCP 执行确认 `TUNNEL_COUNT=1`，PID=23692、父 PowerShell 27920 存活，无第二条同隧道进程。新增桌面 `GPT-Windows-MCP-Show-Console.lnk` 和本地显示脚本（0 语法错误）；脚本有 session-specific PID/handle，未双击。原桌面 `GPT-Windows-MCP-一键恢复.lnk` 存在，防重复脚本已真实测试，但尚未双击；当前 Runtime Key **未存储**，恢复仍需用户在本机输入。

**新发现的兼容问题：** `Make-Manual-Shortcut.ps1` 在 Windows PowerShell 5.1 下 UTF-8 中文文本使解析出现 `2` 错误，PowerShell 7 同文件 `0` 错；已保存 SHA256、快照和正确解释。旧 `Supervisor.INCOMPLETE.txt` 仅作为失败隔离证据保留，禁止当作正式计划任务启动。

~~~ini
TASK=WINDOWS-TUNNEL-PERSISTENCE-20261012
SKILL_VERSION=0.3.4
TUNNEL_ID=tunnel_6acbeee2ce888191b775cd53429c7597
REAL_WINDOWS_REMOTE_FILE_READ_WRITE_SHELL=PASS_SCOPED
CURRENT_TUNNEL_CONSOLE_HIDE=PASS
CURRENT_TUNNEL_ALIVE_AFTER_HIDE=PASS
TUNNEL_UNIQUE_PROCESS=PASS_AT_PROBE
SHOW_CONSOLE_SHORTCUT_CREATED_AND_PARSED=PASS
SHOW_CONSOLE_SHORTCUT_DOUBLECLICK=NOT_TESTED
MANUAL_RECOVERY_SHORTCUT_EXISTS=PASS
MANUAL_RECOVERY_SCRIPT_ANTIDUP=PASS
MANUAL_RECOVERY_SHORTCUT_DOUBLECLICK=NOT_TESTED
LOGIN_HIDDEN_AUTOSTART=NOT_IMPLEMENTED
REBOOT_REMOTE_RECOVERY=NOT_TESTED
RUNTIME_KEY_STORED=NO
DPAPI_SUPERVISOR_PROPOSAL=BLOCKED_NOT_IMPLEMENTED
DO_NOT_CHANGE=FlClash,WindowsProxy,ExistingBrowser,DCR,GitHubRunner
NEXT=After actual Windows reboot, inspect single tunnel PID and remote MCP read/command; if absent use existing desktop manual recovery and enter Runtime Key locally; never conceal an interactive Key prompt.
~~~

**注意**：旧字段如 `NEXT=Keep current PowerShell running`、`CURRENT_INTERACTIVE_RUNTIME=RUNNING_AT_LAST_PROBE` 属旧时点记录；现在的含义是**保持原进程继续存活，允许控制台不可见**。不要删去或改写历史结论为从未发生；以后以本节的新 `LATEST Freeze` 接续。
