# V1.5 持续故障提醒部署与验收

2026-11-10，北京时间。用户要求连接持续异常时有声音和窗口，不确认则间隔几秒持续提醒；网络恢复继续自动接续。

## 部署

根`C:/AI/DevSpace-Benchmark-20261031`。原2分钟健康任务、固定域名、ngrok、认证与代理配置不变。原`ensure-connector.cjs`追加通知hook，备份为`ensure-connector.cjs.before-alert-1794323842957`；读取`connector-fixed/autostart-health.json`，写`connection-alert.json`，触发交互式按需任务`GPT-D-Connection-Alert`。

按需任务以当前用户Interactive、LeastPrivilege运行；IgnoreNew、ExecutionTimeLimit=PT0S、无定时触发器；窗口mutex二次去重。它与健康任务分离，未确认窗口不会占住2分钟健康检查。只有持续失败时启动UI，健康时无驻留UI轮询。

安装必须先复用原PowerShell Reliability Guard，复制其Invoke-GuardedPowerShell.ps1、Test-PowerShellArtifact.ps1、Add-PowerShellFailure.ps1和PSScriptAnalyzerSettings.psd1到根的connection-alert-guard目录；不要用本技能另造脚本执行核心。复制版checker的`Issues = @($issues)`按PowerShell官方仓库已知问题改为`$issues.ToArray()`，保留before-list-array原件。启动时显式传LearnedCatalogPath，避免该旧guard在-File方式下默认参数中PSScriptRoot为空。新PS脚本使用UTF-8 BOM、Windows PowerShell5.1，经原guard预检及执行。安装器只接入现有文件，不自动下载/安装模块。

## 状态与用户行为

两份不同utc的失败回执→PENDING→ALARM；同份回执不虚增。提示音调用立即一次，此后每5秒；窗口“已知晓，停止声音”或X写入本事件ack。ACKNOWLEDGED抑制同事件；恢复HEALTHY清空事件，下次失败重新触发。UI读取最新健康与ack；恢复自动关闭。健康时间戳非法时按异常继续提醒，不让DateTime解析错误终止声音循环。

按2分钟检查，通常约2—4分钟发现持续异常；不承诺检测/恢复硬上限。系统睡眠/关机、无交互登录、静音、服务调度异常均可能影响桌面/声音。本提醒检测的是服务/公网健康回执，不遍历ChatGPT私密会话和凭据，也不认证所有OAuth/MCP客户端故障。

## 实际证据

- Node测试已在本机运行：首次失败、重复回执不增数、第二次报警、ack抑制、恢复复位、新事件重报、陈旧及非法时间记录。
- GUI测试一：23:12:10 WINDOW_SHOWN，23:12:10/15/20/25 SOUND_REQUESTED，23:12:25 ACKNOWLEDGED；原guard返回退出0。
- 交互式后台任务测试：23:16:27 WINDOW_SHOWN，23:16:27/32/37 SOUND_REQUESTED，23:16:39 ACKNOWLEDGED。测试没有切断真实网络。
- 恢复测试中窗口被提前确认，保留ACK记录，不冒称该轮自然关闭。随后23:19:00 WINDOW_SHOWN，23:19:01 AUTO_CLOSED验证已恢复状态的GUI关闭路径；未请求声音。周期检查与首次Shown使用同一tick函数，但不将首次关闭等同长时间恢复稳定性测试。
- 正式原健康任务接入后23:18:04回执HEALTHY、failures=0、episode=null，当前正常连接没有故障窗口。
- 系统声音API已按5秒调用；无法通过日志证明物理扬声器实际可听。PSScriptAnalyzer本机不可用，未声称其检查通过；未运行Pester。已有Node状态测试、原PS语法/兼容检查和真实桌面执行分别记录。

## 失败保留与成熟修正

初版直接detached拉起PowerShell的后台路径未显示窗口，不认证。改为Windows交互式按需任务后通过。旧guard的List[object]数组转换在5.1报Argument types do not match，使用既有ToArray解决；其-File默认PSScriptRoot空值以显式LearnedCatalogPath适配。仅改复制版，不扩散到其他项目。独立只读代码审核发现非法utc会阻断UI tick，已改TryParse并补状态负例。原固定ensure首先await异步端口检查，hook可在退出前注册；正式HEALTHY产物见证其实际调用。

## 收尾与回退

验证任务D-Connection-Alert-Validation仅用于测试，收尾删除；测试窗口已关闭。保留原事件记录，不伪造故障回执到正式健康文件。回退时恢复上述原ensure备份并删除按需提醒任务，原健康任务和ngrok继续保留；先确认没有待处理窗口。

## 成熟依据

- https://learn.microsoft.com/en-us/dotnet/api/system.windows.forms.timer （官方含5秒报警示例）
- https://learn.microsoft.com/en-us/dotnet/desktop/winforms/controls/how-to-play-a-system-sound-from-a-windows-form
- https://github.com/PowerShell/PowerShell/issues/27558 （ToArray适配）
- 原项目已验Task Scheduler、ngrok和PowerShell Reliability Guard。


[本轮源码快照](../assets/connection-alert-v1_5-source.json)
