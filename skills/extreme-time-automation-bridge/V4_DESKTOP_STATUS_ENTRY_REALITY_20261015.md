# V4.0｜桌面“一键恢复”窗口误判故障：成熟入口最小修复及实测

STATUS=WINDOWS_SCRIPT_PATCHED_AND_NONINTERACTIVE_REALITY_PASS; DESKTOP_INTERACTIVE_VISUAL_CONFIRMATION_PENDING
DATE=2026-10-15
SCOPE=Only C:\AI\GPT-Windows-Bridge-B\persistence\Restore-Interactive.ps1
SOURCE=skills/extreme-time-automation-bridge/bootstrap/Restore-Interactive-V4-Status.ps1
METHOD=原V4 A路SOP、PowerShell Reliability Guard、GOOD/BAD/FIRST_DELTA

## 现场证据及原因
用户连续两张真实截图，均来自已有桌面快捷方式 `GPT-Windows-MCP-一键恢复`。
第一张：`Tunnel health: MCP_NOT_INITIALIZED; PID: 46156`，入口提示不启动第二实例，然后窗口消失。
第二张：`Tunnel health: HEALTHY; PID: 46156`，`Tunnel process is already running; no second instance will start.`，依然窗口消失。
现场只读Windows检查确认唯一进程PID46156，由现有恢复Supervisor PID8580启动，官方初始化通知参数已启用。独立原生健康检查 `HEALTHY`、`mcp=initialized`、`poll_failures=0`、`dispatcher_failures=0`；本次ChatGPT真实read_file成功。
**FIRST_DELTA**：桌面快捷方式调用 `Restore-Interactive.ps1`，它在检测到已存在Tunnel时，健康/非健康分支都仅`Start-Sleep -Seconds 2; exit`。结束的是状态检查PowerShell窗口，而不是Tunnel。初始MCP初始化阶段会被过早提示为故障。

## 成熟最小修改
保持原启动器、Tunnel ID、Task Scheduler、Supervisor、加密凭据位置及代理完全不变，只替换原 `if ($all.Count -gt 0)` 的状态处理分支：
- 有且仅有一个旧Tunnel，追踪固定PID。
- 状态 `MCP_NOT_INITIALIZED` / `NOT_READY` 时，最多180秒检查同PID、5秒一次；不再立刻退出，也绝不新建第二实例。
- `HEALTHY` / `HEALTHY_PATH_ONLY` 时显示“现有连接已运行”，交互窗口等待用户按回车才关闭。窗口关闭与Tunnel生命周期无关。
- 身份变化、健康探测异常或超时，保留错误信息，要求用户回车关闭；不盲目终止Tunnel。
- 当本机无任何 `tunnel-client.exe` 时，原有用户手工输入密钥的合法启动流程完全保留。

## 已执行真实验收
- 修改前原始SHA256：`A97F5B735C531B76C46B96A5DE66682A4F79F3A30267C99FA6511ABDF60027E6`。
- 新正式SHA256：`070E8921F7E27D0BA82057C98F183C1EFFE65C43A6F9AB651C059F9432B26921`。
- 备份：`C:\AI\GPT-Windows-Bridge-B\persistence\Restore-Interactive.ps1.bak-20261015-v4-window`，原文件SHA回读匹配。
- Windows PowerShell 5.1 Parser无错误；对比候选与正式原文件前后不变，仅已有Tunnel检测分支调整。
- 静态预检PASS，独立正式脚本实际运行：`DEPLOYED_V4_STATUS_ENTRY_REALITY=PASS`、退出码0、约7780ms、健康状态确认、PID46156前后未变化、Tunnel仍只有1个实例。
- 使用 `powershell.exe -NonInteractive` 的真实测试中无法输入，正确进入`Interactive input unavailable`并退出0；**这不等同于人手双击后的窗口停留可视验收**。交互式 `Read-Host` 分支已存并且语法通过，仍需用户实际双击观察、按Enter关闭确认。
- 未修改FlClash、Windows系统代理、MCP授权、Runner、已有Supervisor、浏览器或运行中的Tunnel。未读取密钥内容；未新建Tunnel。
- 之前隔离预备候选可能未通过初次观察器的纯文本匹配，现已按实际输出与有效进程进行独立核验。

## 下一步
用户只需**双击原桌面快捷方式一次**：若健康，应显示`Existing tunnel ready: HEALTHY`及`Status HEALTHY. Press Enter to close this status window`，窗口停留直到用户按Enter；关闭窗口后现有连接应持续运行。期间如显示真实异常，保留截图和原始错误，不反复点击尝试。此测试不是进程退出无人自主恢复或跨登录长期稳定性验收，二者仍单独待验。
