# Reality Evidence｜2026-10-12 Windows 隧道控制台隐藏、恢复脚本与兼容性复查

**任务定位**：`WINDOWS-TUNNEL-PERSISTENCE-20261012`，`GPT直连Windows双路执行桥 v0.3.4 文档升级`。设备 `DESKTOP-4A1EGTM`，登录用户 `A`。这是 **GPT-Windows-MCP-Bridge 对真实 Windows 执行桥的实际工具调用**，不是对软件自动启动完成的推测。

## 1. 现场发现（读取而非创建新的自启动）

- `tunnel-client.exe` PID `23692`，父进程 `powershell.exe` PID `27920`；由 `Get-Process` 得到原控制台句柄 `5573900` 且最初可见。隧道由 2026-10-12 06:02:45 创建，本次没有重启隧道。
- 实际调用 `Get-ScheduledTask`：`GPT-DesktopCommander-Remote-Autostart` 状态 Running，`MSFT_TaskLogonTrigger` + `Interactive`。**这是旧 DCR Remote 任务，不是新 OpenAI Tunnel 登录任务。**
- 实际读取 `C:\Users\A\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Codex_SystemEvolution_24h.vbs`，关键内容（成熟复用证据）：

~~~vbscript
Set shell = CreateObject("WScript.Shell")
shell.Run "powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File ""C:\Users\A\.codex\skills\system-evolution\scripts\run-system-evolution.ps1"" -Mode Approval -MinHoursBetweenRuns 24", 0, False
~~~

- 实际读取原 `GPT-LTMVH-Recovery-Watchdog.cmd`，关键机制：`start "" /min powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File ...`。证明旧系统多处已采用成熟静默运行手段。
- 实际读取 `C:\AI\GPT-Windows-Bridge-B\Launch-OpenAI-Real-MCP.ps1`：`Read-Host -AsSecureString`、`CONTROL_PLANE_API_KEY` 只置入进程环境，没有把 Runtime Key 保存到文件；因此该脚本**不能通过单纯隐藏窗口自动启动**。

## 2. 正式 Reality：先确保可撤销，再对现有窗口 SW_HIDE

先写入下面的 **会话专属** `Show-Current-Tunnel-Console.ps1` 并生成桌面 `GPT-Windows-MCP-Show-Console.lnk`，真实工具返回：
~~~text
UNDO_SHORTCUT_EXISTS=True
UNDO_TARGET_EXISTS=True
UNDO_PARSE_ERRORS=0
~~~

接着通过 Windows `user32.dll` 的 `GetWindowThreadProcessId` 对窗口句柄做 PID 27920 归属验证，`ShowWindowAsync(hwnd, 0)`（`SW_HIDE`），实际回执：
~~~text
BEFORE_VISIBLE=True
AFTER_VISIBLE=False
TUNNEL_ALIVE=True
UNDO_AVAILABLE=True
~~~

之后再次从 **仍有效的远程 Windows MCP** 独立调用 `start_process`，回读：
~~~text
TUNNEL_COUNT=1
TUNNEL_PID=23692
CONSOLE_PARENT_ALIVE=True
RESTORE_SCRIPT_EXISTS=True
RECOVERY_SHORTCUT_EXISTS=True
~~~

**已经证明：** 当前控制台隐藏成功、隧道保持运行、没有重复启动；仍能远端下发 PowerShell 命令。**没证明：** 桌面 Show 快捷方式已由用户双击成功、新登录自动启动、重启后自动恢复。

## 3. Windows 本机脚本精确快照（仅作为历史证据，不要按旧 PID/句柄直接重新部署）

### `Show-Current-Tunnel-Console.ps1` —— SHA256 `D4858C5C7E49507AB1F236671BE172CF1CCB16CB0B6BA9AE02367C2A514152F1`

~~~powershell
$ErrorActionPreference = 'Stop'
$ExpectedPid = 27920
$WindowHandle = [IntPtr]5573900
$source = @'
using System;
using System.Runtime.InteropServices;
public static class TunnelWindow {
 [DllImport("user32.dll")] public static extern bool IsWindow(IntPtr h);
 [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
 [DllImport("user32.dll")] public static extern bool ShowWindowAsync(IntPtr h, int cmd);
 [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
}
'@
Add-Type -TypeDefinition $source
if (-not (Get-Process -Id $ExpectedPid -ErrorAction SilentlyContinue)) { throw 'Original PowerShell PID has exited; recovery shortcut is still available.' }
if (-not [TunnelWindow]::IsWindow($WindowHandle)) { throw 'Original console window is no longer present.' }
[uint32]$owner = 0
[void][TunnelWindow]::GetWindowThreadProcessId($WindowHandle, [ref]$owner)
if ($owner -ne $ExpectedPid) { throw 'Window owner mismatch; refusing to open a different window.' }
[void][TunnelWindow]::ShowWindowAsync($WindowHandle, 9)
Write-Host "SHOW_CURRENT_TUNNEL_CONSOLE_REQUESTED PID=$owner"
Start-Sleep -Seconds 3
~~~

### `Restore-Interactive.ps1` —— SHA256 `27B47071686B602F2EFDBF8C6C01F06B2E91CE4A4FD93DB0B3C64161E0CD4738`

~~~powershell
$ErrorActionPreference='Stop'
$tunnelId='tunnel_6acbeee2ce888191b775cd53429c7597'
$launcher='C:\AI\GPT-Windows-Bridge-B\Launch-OpenAI-Real-MCP.ps1'
$existing=@(Get-CimInstance Win32_Process -Filter "Name='tunnel-client.exe'" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*$tunnelId*" })
if($existing.Count -gt 0){
    Write-Host ('GPT-Windows MCP is already running, PID '+($existing.ProcessId -join ','))
    Write-Host 'No second tunnel will be started.'
    Start-Sleep -Seconds 4
    exit 0
}
if(!(Test-Path -LiteralPath $launcher)){throw "Launcher missing: $launcher"}
Write-Host 'Starting GPT-Windows MCP in this interactive window.'
Write-Host 'Paste the existing OpenAI runtime API key when prompted; do not paste it in ChatGPT.'
& $launcher -Launch
~~~

已经有之前真实执行的重复启动拒绝回执：
~~~text
GPT-Windows MCP is already running, PID 23692
No second tunnel will be started.
Process completed with exit code 0
~~~
该结果不是桌面双击回执；双击仍 NOT_TESTED。

### `Make-Manual-Shortcut.ps1` —— SHA256 `12A11E572BFEF81EB3F6A3A58CD510F3CE5E985F3274A0F3D803397B8595A35B`

~~~powershell
$ErrorActionPreference='Stop'
$desktop=[Environment]::GetFolderPath('Desktop')
$link=Join-Path $desktop 'GPT-Windows-MCP-一键恢复.lnk'
$wsh=New-Object -ComObject WScript.Shell
$shortcut=$wsh.CreateShortcut($link)
$shortcut.TargetPath=Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
$shortcut.Arguments='-NoProfile -ExecutionPolicy Bypass -File "C:\AI\GPT-Windows-Bridge-B\persistence\Restore-Interactive.ps1"'
$shortcut.WorkingDirectory='C:\AI\GPT-Windows-Bridge-B'
$shortcut.Description='手动恢复 ChatGPT 到 Windows MCP；会在本机安全提示输入运行密钥'
$shortcut.Save()
Write-Output ('SHORTCUT_CREATED='+$link)
Write-Output ('TARGET_EXISTS='+[bool](Test-Path $shortcut.TargetPath))
Write-Output ('LAUNCHER_EXISTS='+[bool](Test-Path 'C:\AI\GPT-Windows-Bridge-B\persistence\Restore-Interactive.ps1'))
~~~

这个 **创建器** 曾由 PowerShell 7 真正运行创建快捷方式，但本次执行额外发现：在 Windows PowerShell 5.1 中 `ParseErrors=2`（中文 UTF-8 编码导致引号未终止）；调用 `C:\Program Files\PowerShell\7\pwsh.exe` 的解析器结果 `PS7_ERRORS=0`。请勿把旧编码问题误判为恢复脚本本身失效。

## 4. 独立 SHA/文件预检

~~~text
SCRIPT=Restore-Interactive.ps1 EXISTS=True PARSE_ERRORS=0
SHA256=27B47071686B602F2EFDBF8C6C01F06B2E91CE4A4FD93DB0B3C64161E0CD4738
SCRIPT=Make-Manual-Shortcut.ps1 EXISTS=True PARSE_ERRORS=2   # Windows PowerShell 5.1；PS7_ERRORS=0
SHA256=12A11E572BFEF81EB3F6A3A58CD510F3CE5E985F3274A0F3D803397B8595A35B
SCRIPT=Show-Current-Tunnel-Console.ps1 EXISTS=True PARSE_ERRORS=0
SHA256=D4858C5C7E49507AB1F236671BE172CF1CCB16CB0B6BA9AE02367C2A514152F1
LINK=GPT-Windows-MCP-一键恢复.lnk EXISTS=True TARGET_EXISTS=True
LINK=GPT-Windows-MCP-Show-Console.lnk EXISTS=True TARGET_EXISTS=True
~~~

**待测/禁止推断**：显示快捷方式没有双击验收，未进行真实关机/开机；未保存 API Key，未创建隧道专用计划任务；本轮没有修改 FlClash、系统代理、已有浏览器、DCR/Runner 任务。

**后续唯一有效启动验收**：下一次真正重启/登录后记录 `TUNNEL_COUNT、PID、可见窗口、MCP远端只读调用`；必要时按原交互恢复入口（本机人工输入 Key）恢复，再对新会话窗口隐藏。原本 2026-10-12 这次 Hide PASS **不重复测试**。
