# GPT直连Windows双路执行桥V3.0｜A路真实短周期稳定性与原守护器重新加载

TASK=A-SHORT-READ-SUPERVISOR-RELOAD-20261015
TIME_WINDOW=2026-10-15 02:41–02:45 +08:00
SCOPE=Existing interactive Windows A, no tunnel restart, no proxy change
STATE=A_SHORT_SCOPED_REALITY_PASS; SUPERVISOR_RELOAD_PASS; AUTO_RECOVERY_AFTER_PROCESS_EXIT_NOT_TESTED

## 背景与 FIRST_DELTA
本技能包已有成熟PS-002修复文件 `C:\AI\GPT-Windows-Bridge-B\persistence\Recovery-Supervisor-v1.ps1`，SHA256=`649E7A939AA8A27B91FE5FBE130E842E131EB96D55F36A1C00FED405335270EF`。
但原守护进程PID46072创建于此修复前，仍运行旧版代码。其实际日志2026-10-15 02:35:57+08:00再次进入`TUNNEL_START`，约1.9秒后`TUNNEL_EXCEPTION/TUNNEL_EXIT`，随后02:38:59检测到人工恢复的新隧道。因此文件补丁已写入不等于后台进程已经加载。异常的全部原因仍不能仅从本次旧进程日志反推出。

## 冻结后的实际主路调用
通过`GPT-Windows-MCP-Bridge.read_file`同一固定文件、相同0–2行、八次连续独立工具调用：
| 次数 | 毫秒 | 实际结果 |
|---|---:|---|
| 1 | 5700 | PASS |
| 2 | 5294 | PASS |
| 3 | 5851 | PASS |
| 4 | 6064 | PASS |
| 5 | 3949 | PASS |
| 6 | 7868 | PASS |
| 7 | 3956 | PASS |
| 8 | 3904 | PASS |

合计8/8，均值5323.25ms，中位数约5497ms，最短3904ms，最长7868ms。均为真实ChatGPT端到端文件工具调用，未循环补偿失败；此结果不等于8个独立隧道生命周期或72小时无故障。

## 原生任务计划程序受控重新加载
变更前门禁实际PASS：
- 唯一隧道PID30820，父进程PID39468，不属于旧守护PID46072；
- `GPT-Windows-Tunnel-Recovery-v1`任务为Interactive用户A、状态Running、动作匹配现有恢复脚本；
- 正式脚本SHA匹配，Windows PowerShell Parser错误数0，原本已知备份SHA正确。
- 原有任务最近结果`0x800710E0`，需按Task Scheduler具体执行上下文解释；不能把Running状态本身等同自动恢复通过。

仅通过官方`Stop-ScheduledTask`停止此恢复任务，确认旧PID46072退出、现有Tunnel仍为PID30820后，使用`Start-ScheduledTask`加载同一任务，没有关闭隧道，也没有新增Supervisor/任务/隧道、调整权限或代理。
新Supervisor PID8580于2026-10-15 02:44:04+08:00写入`SUPERVISOR_STARTED`、`EXISTING_TUNNEL`；隧道PID30820前后不变；任务继续Running；新代码SHA不变。

重新加载后5项真实MCP工具验收：
- read_file: PASS，4657ms
- list_directory: PASS，3990ms
- read_multiple_files: PASS，8820ms
- read_file现有PS-002执行片段: PASS，3826ms
- start_process只读查询运行状态: PASS，6803ms

**观察器误判说明**：最后一项工具原始成功回执包含 `current_tunnel_pid=30820`、`new_supervisor_alive=true`、`task_state=Running`，但临时观察器对嵌套JSON文本做未解码子串匹配，结果误写为`ok=false`。这是验收器自身的格式匹配错误，不是Windows或MCP错误，独立核对原始数据后为通过。不得将误报计入A实际失败。

## 技能包运行边界、待验与停止门
已通过：当前单进程运行、原官方shim参数存在、本次同构短读8/8、含不同工具类型的主路操作5/5、原守护器经Task Scheduler合法重新加载、安全保护现有隧道、修复文件与备份哈希复核。
尚未通过：无人值守异常退出后自动恢复；断网/网络抖动自然恢复；真正Windows注销/开机登录自动恢复；跨长时间独立周期；ChatGPT侧偶发409永久根治。当前守护器仅检查`tunnel-client.exe`进程数，不主动终止仍在线但协议异常的实例，这是既有安全边界，不能通过“进程存在”获得MCP恢复PASS。
不要重复之前额外的`Validate-OneTunnel-Recovery-20261015.ps1` Stop-Process测试，不为统计漂亮再主动切断当前已登录实例。凭据仅在本机留存；不读/传/打印；不修改FlClash或系统代理。
下一自然故障发生时保留原生Supervisor日志、Tunnel-Health日志及ChatGPT真实工具错误，从GOOD/BAD与FIRST_DELTA判断，依据V2 A路专门恢复SOP采取唯一恢复行动，不盲目重发未知副作用。
