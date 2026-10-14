# V5.0 附件四｜日常极简入口、首故障决策树、验收门与断点接续

## 0. 用户最少操作（运行入口轻）
日常：用户登录Windows后，由已有`GPT-Windows-Tunnel-Recovery-v1`计划任务负责检查并维护单隧道；正常工作**无需反复双击桌面**。桌面“GPT-Windows-MCP-一键恢复”是**状态检查/必要时人工启动入口**，不是唯一后台服务。若显示`HEALTHY`及PID，按Enter关闭状态窗口不关闭Tunnel。需要人工Runtime Key只在本机输入，勿发送聊天。
现有任务为`AtLogOn`（用户A登录后）以及5分钟重复、IgnoreNew、防重运行、Interactive Limited；其功能**不保证Windows尚未登录时自动运行**。尚未完成真正关机/重启后自动联网端到端验收。

## 1. 唯一故障分流（从源头、具体状态）
| 真实现象 | 第一观察项 | 成熟动作 | 终止条件 |
|---|---|---|---|
| ChatGPT远程`read_file`成功 | 正确文件内容、时间、Tunnel唯一PID | 直接业务，无需调试 | 接入合格结束 |
| 桌面窗口`HEALTHY`但黑框停住 | `Status HEALTHY. Press Enter` | 按Enter关闭状态窗，不停隧道 | 当前窗口关闭而工具保持可读 |
| 刚启动`MCP_NOT_INITIALIZED` | 同一PID、控制平面、子进程代次 | 入口最多180s按5s复查同一进程，不另起 | 变HEALTHY或有明确超时错误 |
| `PROCESS_MISSING` | 任务计划和Supervisor事件、是否用户A已登录 | 让已有Supervisor按原规则接单，不盲启动第二个 | 新PID+真实read_file双证 |
| `409 mcp_initialization_required` | 官方initialize/notifications/initialized时序，子进程代次 | 原A路SOP，必要时平台插件刷新/官方初始化，不能伪造握手 | 确认真实工具成功或原错保留 |
| `Session terminated` | Tunnel PID是否变化、parent、控制平面/业务回执 | 先分“真实进程退出”或“ChatGPT调用会话状态”，仅官方既有恢复 | 不自动重试未知副作用 |
| 健康但业务调用502/超时 | 健康组件、dispatcher、delivery与真实请求编号 | 差分诊断，尽可能保留匿名证据 | 发现FIRST_DELTA后最小修复 |
| A不可用且任务需继续 | 冻结任务合同、是否已经执行 | B FAST/V2 bounded/FULL成熟路径分流 | 无法保护Exactly-once则停止派发 |

## 2. 验收三层，不得混用
**第一层：配置存在。** 任务已注册、用户A登录触发、5min重复、加密文件存在；“有这个能力/已配置”，不是每次开机都保证成功。
**第二层：同登录与进程短期可用。** 2026-10-15已实测ChatGPT端8/8 `read_file`，耗时毫秒5700、5294、5851、6064、3949、7868、3956、3904；算术均值5323.25ms。Supervisor重载后五项不同工具真实通过；后续同新PID46156一次read_file约5.245s+三次4.241/7.828/5.439s都成功，且只读PowerShell成功。前后短读不能合并成“五次独立异常恢复”。
**第三层：真正完整生命周期。** 仍待实际整机重启→用户A首次登录→无人手动密钥输入（仅合法既有DPAPI）→单Tunnel启动→MCP初始化→ChatGPT真实read_file；以及自然/明确获批的进程异常退出后Supervisor独立启动再成功远程read_file，并需要多次跨周期无故障证据。不打断当前用户业务制造测试。
**B路单独验收**：历史V3有界小工件5次独立Windows+GitHub Run、实际Artifact回读PASS，30至38秒；FULL长尾尚未根治，与A无关。

## 3. 日常/变更保护与回滚
部署脚本修改前：核对真实当前SHA→只改故障片段→PS5.1解析与正反例测试→本地备份→原子替换→独立readback；常驻进程必须确认是否需要安全重载，且不能关闭Tunnel父进程。只用原Windows Task Scheduler操作原守护器，不增加第二套管理器。
- 原Supervisor当前SHA：`649E7A939AA8A27B91FE5FBE130E842E131EB96D55F36A1C00FED405335270EF`；旧备份以`D5B2D109...`开头。
- 桌面入口当前SHA：`070E8921F7E27D0BA82057C98F183C1EFFE65C43A6F9AB651C059F9432B26921`；旧备份以`A97F5B...`开头。
- 不变更现有FlClash、系统代理、隧道身份、登录授权、Runner设置、浏览器或Hermes其他业务；无需动作的已合格组件停止重复测试。

## 4. 下次页面最短接续
唯一权威 `skills/extreme-time-automation-bridge/SKILL.md` V5入口；涉及事故才按需参考四份V5附件，历史V4/V3/V2按原日期使用。冻结定位：`BRIDGE-A-V5-20261015|USER_A_LOGON_CAPABILITY_CONFIGURED|A_SCOPED_REAL_CALLS_PASS|POST_REBOOT_UNKNOWN`。如仍正常，直接恢复用户原业务；如出现新故障，先读一条真实工具回执、再查唯一PID与健康/日志，只在FIRST_DELTA明确时行动。运行态PID不是固定配置，不能据旧PID直接kill。
STATE：`V5_SKILL=RELEASE_PENDING_READBACK`；`AUTO_START_AFTER_USER_LOGIN=CONFIGURED`；`ONE_OBSERVED_SUPERVISOR_TUNNEL_START=PASS`；`POST_REAL_REBOOT=NOT_TESTED`；`LONG_TERM_STABILITY=UNKNOWN`；`A_ALL_BUGS_GONE=NOT_CLAIMED`。
