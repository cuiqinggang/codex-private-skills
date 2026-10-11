# GPT-Windows-MCP 隧道窗口显隐、人工恢复与开机验收｜v0.3.4

> 正式技能包入口：[SKILL.md](SKILL.md)。本文件是 **2026-10-12 真实 Windows 现场的成熟方法与操作规范**，而非新的后台驻留程序。不得把「当前窗口已隐藏 PASS」写成「开机自动隐藏连接 PASS」。
>
> 权威仓库：`cuiqinggang/codex-private-skills` → `skills/extreme-time-automation-bridge/` → `main`；绝不先去本机找方法。原始时间序列和失败历史保留在 [WINDOWS_TUNNEL_PERSISTENCE_STATUS_20261012.md](WINDOWS_TUNNEL_PERSISTENCE_STATUS_20261012.md)；重建/首次连接见 [OPENAI_TUNNEL_CONNECT_RECOVERY_20261012.md](OPENAI_TUNNEL_CONNECT_RECOVERY_20261012.md)。[本轮独立实测与本机脚本快照](evidence/OPENAI_TUNNEL_WINDOW_VISIBILITY_REALITY_20261012.md)。

## 一、已验证结论（将各级验收严格区分）

| 能力 | 2026-10-12 最新现场证据 | 状态 |
|---|---|---|
| ChatGPT → 官方隧道 → 真实 Desktop Commander MCP（Windows 读/隔离写回/PowerShell 命令）| 已有独立真实远端工具输出，详见原远程验收证据 | PASS（限定能力） |
| 正常运行时仅隐藏原 PowerShell 控制台、不停止隧道 | `BEFORE_VISIBLE=True` → `AFTER_VISIBLE=False`；PID23692存活 | **PASS** |
| 隐藏后再次查询唯一隧道进程 | `TUNNEL_COUNT=1`，`TUNNEL_PID=23692`；父进程27920存活 | **PASS** |
| 找回当前窗口的桌面快捷方式及脚本存在/语法 | 链接及目标存在，显示脚本 `ParseErrors=0` | **文件预检 PASS，实际双击 NOT_TESTED** |
| 桌面手工恢复快捷方式及防重复启动 | 旧脚本真实回执「already running」「No second tunnel will be started」；快捷方式存在 | **脚本防重 PASS，真实双击 NOT_TESTED** |
| 登录自动隐藏启动本隧道 | 没有注册该隧道专属自动启动任务 | **NOT_IMPLEMENTED** |
| 断电/注销/重启后，无人输入密钥自动恢复 | 原正式 launcher 需手工输入 Runtime Key，没有保存 | **NOT_TESTED / 未实现** |
| 授权/安全检查 | 原 DPAPI + Supervisor 候选曾被执行环境安全拦截 | **该方案停止，禁止绕行** |

上面 Windows 进程 PID 及窗口句柄均是 **2026-10-12 单次会话的证据值**，不是永久定位 ID。新登录后必须重新检测，不得照抄旧 PID/句柄操作别的进程。

## 二、当前部署实物：不重复发明、不删除原来的

- 电脑 `DESKTOP-4A1EGTM`，Windows 登录用户 `A`。PowerShell 7 位于 `C:\Program Files\PowerShell\7\pwsh.exe`。
- 官方 OpenAI Tunnel `tunnel-client.exe` 属 `C:\AI\GPT-Windows-Bridge-B\tunnel\v0.0.16\`，开源 Desktop Commander MCP `@wonderwhy-er/desktop-commander@0.2.52`；Tunnel ID：`tunnel_6acbeee2ce888191b775cd53429c7597`（不是密钥）。
- 正式交互式入口：`C:\AI\GPT-Windows-Bridge-B\Launch-OpenAI-Real-MCP.ps1 -Launch`；它调用 `Read-Host -AsSecureString` 获取本机 Runtime API Key，没有持久化 Key。
- 手动恢复脚本：`C:\AI\GPT-Windows-Bridge-B\persistence\Restore-Interactive.ps1`，桌面快捷方式 `GPT-Windows-MCP-一键恢复.lnk`。运行前按 **Tunnel ID** 检测在运行进程，防止第二条相同隧道。
- 当前窗口显示（撤销隐藏）：`C:\AI\GPT-Windows-Bridge-B\persistence\Show-Current-Tunnel-Console.ps1`，桌面 `GPT-Windows-MCP-Show-Console.lnk`。此脚本写死当前 PID 27920 / 窗口句柄 5573900 且验证 owner，仅适用于本次会话；不要把它当重启后的通用 Show 工具。
- 快捷方式创建脚本：`C:\AI\GPT-Windows-Bridge-B\persistence\Make-Manual-Shortcut.ps1`；不必在日常使用中重跑。
- 未完成 Supervisor 仅以 `Supervisor.INCOMPLETE.txt` 隔离保留；不是可执行启动项、也不得改名直接运行。
- 原 A 路 Desktop Commander Remote 主路、GitHub Actions 自托管 Runner 备路仍保留。原登录任务 `GPT-DesktopCommander-Remote-Autostart` 属 **DCR Remote**，不是这个新的官方 Tunnel；不能当作 Tunnel 自启 PASS。

### 旧成熟方案已核验，优先复用

1. Windows 用户启动文件夹 `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup` 中已存在 `Codex_SystemEvolution_24h.vbs`；它采用 `WScript.Shell.Run(..., 0, False)` 启动隐藏 PowerShell。即 **Windows 原生脚本宿主隐藏启动**，不是新的自研架构。
2. `GPT-DesktopCommander-Remote-Autostart` 为计划任务 `LogonTrigger` + `Interactive` 身份；已有应用使用这种标准 Windows 登录触发策略。**不要改动此任务**。
3. 另有既有 `GPT-LTMVH-Recovery-Watchdog.cmd` 使用 `start "" /min powershell.exe -WindowStyle Hidden ...`；仅证明旧的静默/最小化机制存在。**这两个证据均不等于官方隧道的新自启动任务已配置。**
4. Windows 任务计划程序中的「隐藏任务」选项不等价于隐藏程序窗口；需选择与实际程序交互要求相容的窗口机制。

## 三、已验证的「只隐藏当前正在工作的窗口」方案

### 必要前提（先验证，再操作）

- 用户授权的是**视觉上不出现控制台**，不是改变隧道登录身份/加密方式、不是后台窃取密钥，也不是新建随系统运行的高权限服务。
- 用 `Get-CimInstance Win32_Process` 按 `tunnel-client.exe` 和唯一 Tunnel ID 找到正在运行的隧道，核对唯一进程数、父进程 PowerShell PID、`Get-Process` 窗口句柄。
- Windows 标准 API `GetWindowThreadProcessId` 验证句柄归属父进程，避免误隐藏其他窗口。
- 确保 **显示/撤销快捷方式预先写入、语法通过、目标存在**；只调用 `ShowWindowAsync(handle, SW_HIDE=0)`，**不调用 Stop-Process，不关闭 PowerShell**，不改代理、不动浏览器。
- 核验 `IsWindowVisible` 从 `True` 变成 `False`，隧道 PID 仍存活；再通过远程工具做无副作用读/命令确认链路可用。

### 2026-10-12 现实回执

`tunnel-client.exe` PID `23692` → 父 `powershell.exe` PID `27920`；会话中窗口句柄 `5573900`。实际运行 Windows 标准 API：

~~~text
BEFORE_VISIBLE=True
AFTER_VISIBLE=False
TUNNEL_ALIVE=True
UNDO_AVAILABLE=True

TUNNEL_COUNT=1
TUNNEL_PID=23692
CONSOLE_PARENT_ALIVE=True
RESTORE_SCRIPT_EXISTS=True
RECOVERY_SHORTCUT_EXISTS=True
~~~

**正确解释：** 进程继续运行，只是窗口隐藏了；如果用户结束原 PowerShell 进程或直接关闭对应控制台，stdio 隧道可能终止。**SW_HIDE 不是服务化、持久化或自动重启机制。** 本次没有安排真正重启 Windows。

### 如果要重新显示当前窗口

双击桌面 `GPT-Windows-MCP-Show-Console.lnk`（`SW_RESTORE=9`）。若旧 PID/窗口句柄已失效，此脚本会拒绝操作，**不要强行替换成新的任意句柄**。该快捷方式的文件/脚本解析已验证，**尚无用户真实双击验收**。不要将「可显示」判为 PASS。

## 四、下一次登录/开机——最短且真实的恢复

1. **不重建隧道**。登录 Windows 后先检查是否有官方 `tunnel-client.exe` 且命令行包含上述 Tunnel ID；检查实际远程 MCP 是否可调用。单纯发现 PID 不足以验收外部访问。
2. 已可调用则无需操作：由 GPT 使用真实 `list_directory` 或无副作用 `start_process` / echo（依已安装工具）验收，并确认同 Tunnel ID 仅有一个进程、窗口不显示。
3. 若没有有效隧道，双击桌面 `GPT-Windows-MCP-一键恢复.lnk`；脚本先查原同 ID 进程，已存在则不启动第二份；不存在则通过正式 launcher 本地**人工**输入已有 Runtime API Key。密钥不得发送聊天或提交 GitHub。因交互输入存在，这一步 **不能预先隐藏提示窗口**。
4. 成功看到官方 `tunnel-client started` + `stdio MCP command started` 后，使用远程 MCP 实际读目录/只读命令，并检查文件/执行结果。若用户只希望安静，再对**新会话重新发现**的原窗口执行有可撤销入口的单次隐藏；不能使用本次写死的旧句柄。
5. 如果 ChatGPT 端还显示演示 `echo/server_info` 或 `Unknown tool`，先从插件设置 `Refresh` 更新工具目录，不是重建隧道；如果进程断线/授权失败，先精确定位进程、健康端口、日志/权限，不因一个局部错误修改 FlClash、网络代理。
6. **禁止假验收：** 必须有登录/重启后状态回执 + 唯一隧道进程 + 完整远端实际工具调用 + 窗口不显示，才可分别填 `LOGIN_AUTOSTART_PASS`、`REMOTE_TOOL_PASS`、`HIDDEN_AFTER_LOGON_PASS`。否则分别保留 NOT_TESTED/NOT_IMPLEMENTED。

## 五、这次发现且以后不应重复的故障和安全边界

- 正式 launcher 使用 `Read-Host -AsSecureString` 并只将 Key 用于当前进程环境，**没有保存/自动获取 Key**。把整个 launcher 加 `-WindowStyle Hidden`、VBS `0`，只会把输入提示藏起来，**不会凭空获得密钥**。这解释了「隐藏现有运行窗口 PASS」与「下一次开机自动建连未实现」同时成立。
- 曾尝试「DPAPI 解密 + 隐藏 Supervisor + 计划任务」候选，执行环境明确安全拦截。**已停止该特定受限动作，不转换入口规避拦截、不保留半成品任务。**
- Make-Manual-Shortcut.ps1 使用包含中文内容的 UTF-8 文本：Windows PowerShell 5.1 对该文件 **ParseErrors=2**（编码使字符串引号解析失效），同一文件使用已安装的 **PowerShell 7 ParseErrors=0**。以前成功运行的创建器使用 pwsh7；若重跑，先选 PS7，且核对生成的快捷方式指向的 `Restore-Interactive.ps1` 和本机真实文件。恢复脚本本身本轮检测解析错误数=0。
- 原 MCP `--mcp.command` 若使用带空格的 Node 路径会触发 `exec: "C:Program"`，正确修复和 Runner 验收已保存于 SKILL / 完整恢复手册；绝不因此重装代理/密钥/隧道。
- 插件当前允许全部操作、MCP 无身份验证是用户认可的设置，**但实际远程 Windows 文件/命令能力风险高**；平台鉴权、工作区可访问性、最小凭据权限和密钥不出本机的要求仍有效；自动常驻或更换身份需单独合规安全评估。
- 本次文档升级不修改 Windows 任何运行脚本、不更改现有隐藏状态、不新建登录启动项、不创建密钥文件、不要求用户重复实际测试。

## 六、下次执行的四项交付/验收门

- `CURRENT_HIDE=PASS`：已证实，勿复测；`CURRENT_TUNNEL_ALIVE=PASS`（当时现场快照，随时间变化）。
- `RESTORE_SHOW_DOUBLECLICK=NOT_TESTED`；`MANUAL_RECOVERY_DOUBLECLICK=NOT_TESTED`。先核对现有脚本与快捷方式，不重写。
- `LOGIN_AUTOSTART=NOT_IMPLEMENTED`；`REBOOT_RECOVERY=NOT_TESTED`。如未来用户仍要求重启后无需输入 Key，先解决合法凭据来源/权限，**不得通过藏掉输入框来伪实现**。
- 变动必须记录 `GOOD_BASELINE / FIRST_DELTA / 真实命令与实际 stdout / PROCESS_PID / TUNNEL_ID / KEY_POLICY / ROLLBACK / FINAL_VALID`；条件不全时继续保留准确的部分通过状态。

关联来源：[当前隐藏实测记录](evidence/OPENAI_TUNNEL_WINDOW_VISIBILITY_REALITY_20261012.md) ｜ [原手动/自动状态](WINDOWS_TUNNEL_PERSISTENCE_STATUS_20261012.md) ｜ [原全流程恢复](OPENAI_TUNNEL_CONNECT_RECOVERY_20261012.md) ｜ [远端真实 Windows 验收](evidence/OPENAI_TUNNEL_REAL_WINDOWS_REMOTE_PASS_20261012.md) ｜ [原 DCR 恢复](DCR_RECOVERY.md)。
