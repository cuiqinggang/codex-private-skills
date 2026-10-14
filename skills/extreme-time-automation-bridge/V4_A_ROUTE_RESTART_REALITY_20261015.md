# GPT直连Windows双路执行桥 V4.0｜A路成熟修复冻结、轻入口与用户重启Reality验收

VERSION=4.0.0
DATE=2026-10-15
SKILL_PATH=skills/extreme-time-automation-bridge/
REF=main
METHOD=SANRENXING_V2_TASK_SCOPED_REUSE（只按用户本任务指定使用，不擅自改方法全局版本）
RELEASE_SCOPE=EXISTING_SKILL_INDEX_AND_VERIFIED_A_REPAIR
A_CURRENT_SCOPE=SHORT_READ_8_OF_8_PASS; MIXED_CALLS_AFTER_SUPERVISOR_RELOAD_5_OF_5_PASS
A_RESTART_AFTER_USER_CLOSE=AWAITING_USER_ACTION_AND_NEW_CHATGPT_READBACK
A_PROCESS_EXIT_UNATTENDED_RECOVERY=NOT_ACCEPTED
A_LOGIN_AUTOSTART=NOT_ACCEPTED
A_LONG_TERM_STABILITY=NOT_ACCEPTED
A_ALL_BUGS_FIXED=NOT_CLAIMED
B_BOUNDED_ARTIFACT=HISTORICAL_SCOPED_5_OF_5_PASS
B_FULL_GENERAL_RECOVERY=NOT_PROVEN
NO_PROXY_OR_RUNNER_OR_KEY_CHANGE=YES
NO_NEW_DAEMON_OR_TUNNEL=YES

## 0. 总入口和版本关系

这是**原** `extreme-time-automation-bridge` 技能包版本升级，不是新工作台、新隧道、新恢复系统，也不是另造PS守护器。
唯一当前版本为本V4.0规则；V3.0的B路路由成熟成果完整继承，旧V3、V2与历史V1附则均属其原日期的**证据快照**，不得用其“最高优先级”“仍未加载补丁”等旧状态覆盖本V4。
启动时只加载本文与SKILL.md顶端摘要。故障发生才按需打开指定资料；禁止将各历史文档全文压进执行上下文。

## 1. 这次A路 GOOD→BAD→FIRST_DELTA 与成熟修复

- 正常基线：ChatGPT→官方OpenAI Tunnel→单个Windows `@wonderwhy-er/desktop-commander` stdio MCP→真实read_file。人工本机合法登录密钥可恢复Tunnel；FlClash与Windows代理不改变。
- BAD-A：旧隧道由测试脚本终止后，旧恢复器启动五次均`TUNNEL_START→TUNNEL_EXCEPTION→TUNNEL_EXIT`，未在100秒自动恢复；其Windows PowerShell 5.1异常类型`RemoteException`。
- FIRST_DELTA-A：原 `Recovery-Supervisor-v1.ps1` 在 `$ErrorActionPreference='Stop'` 下把官方原生命令的stderr `2>&1`并入PowerShell管道，触发PS5.1 `NativeCommandError` 终止。符合已存成熟 `powershell-reliability-guard` 技能PS-002。
- 复用方案：仅在原生Tunnel调用期间将ErrorActionPreference临时设为Continue，读取`$LASTEXITCODE`，在finally恢复原设置；没有全局屏蔽错误或修改其他功能。故意stderr且退出码0被识别正常；故意返回19仍保留非零退出码。
- 修复备份：`C:\AI\GPT-Windows-Bridge-B\persistence\Recovery-Supervisor-v1.ps1.bak-ps002-20261015`；原SHA256=`D5B2D1098F51794E296233DEBD1E8F07AB71A3690525E014D84FC0644726B434`。正式文件SHA256=`649E7A939AA8A27B91FE5FBE130E842E131EB96D55F36A1C00FED405335270EF`。原仓库参考源代码已修复；Windows保留本机其他差分，不能拿参考源整套覆盖Windows文件。
- BAD-B：即使文件修复，旧守护进程PID46072未重新加载，02:35仍发生一次启动异常。首次正常Tunnel重启依靠用户输入密钥，不能冒称自动恢复。
- FIRST_DELTA-B/已处理：使用**原Windows Task Scheduler**对`GPT-Windows-Tunnel-Recovery-v1`执行受控Stop/Start，严格确认它不是Tunnel父进程；新守护PID8580、Tunnel PID30820不变、仅一个实例，`SUPERVISOR_STARTED`与`EXISTING_TUNNEL`日志通过；未重启Tunnel、不需用户再次输入密钥。
- 独立实测：真实ChatGPT到Windows `read_file`连续8/8正确，毫秒：5700、5294、5851、6064、3949、7868、3956、3904，均值5323.25ms；守护器重载后5类MCP调用5/5通过（含实际目录、文件和状态读取）。一次嵌套JSON观察器`ok=false`属于字符串比较误报，已用原始成功回执复核。
- **验收范围严格限定**：这些测试均处同一Windows登录/隧道生命周期下。正常读取和守护器重载PASS，不等于关闭隧道后的新一轮登录、无人值守异常恢复、开机自启、长期零故障已PASS。

## 2. V4唯一轻入口｜按合同用成熟能力

### A 主路：需要本机交互时优先
用户现有插件`GPT-Windows-MCP-Bridge` + 官方`tunnel-client.exe v0.0.16` + 已安装Desktop Commander MCP。先实际调用一次`read_file`确认控制面与MCP完整可用，不以插件页面、工具发现成功、HTTP健康、PID在线代替。
- 当前合法运行时已有一个Tunnel→保留，不再启动第二个，不要求再次输密钥。
- 用户主动关闭→用户自行复用已有桌面恢复入口，必要时只在本机窗口输入Runtime Key；恢复后用新一轮真正read_file验收，确认新PID、Tunnel ID、shim与实物文件内容。旧短测不作重启后成绩。
- 进程存在但返回`409 mcp_initialization_required`→按原[A路恢复SOP](TUNNEL_AUTORECOVERY_V2_20261015.md)核查initialize/notifications/initialized；官方shim不能伪造initialize。不要强行重启、不要借平台工具合成握手。
- 进程存在而ChatGPT显示`Session terminated`→区分当前连接客户端代次、Tunnel子进程和ChatGPT工具会话，不凭进程存在就宣布已通；只用官方连接刷新与真实只读调用验收。若工具失败仅记录原始错误，立即停掉连续写/未知副作用操作。
- 进程不存在且用户未主动重启→让原Task Scheduler恢复器自行接管；需新PID及真实工具调用双回执才算无人值守恢复成功。若它失败，保留原日志和用户手动恢复入口，不新建守护器或强制循环重启。
- 如健康而业务偶发网络抖动，允许自然恢复；恢复后实测才PASS。

### B 备路：沿用V3已成熟路由，不重测无关项目
按[现有V3 B路规则](GITHUB_WINDOWS_B_ROUTE_V3_20261015.md)分流：
日志合同短任务→现有FAST；小型、非敏感、仅成功证据→V2有界官方Artifact（历史五次完整Run与Artifact读取通过，观察30/36/36/36/38秒）；大证据、失败也需保全、未知规模与强审计→原FULL并承认其历史外部Action ZIP超时长尾。不能把B的5/5拿来证明A，不能为了追求微秒级提速删证据或改运行网络。
第三方R只有授权与可用额度真实存在且收益成立时启用。网络代理、FlClash、Runner配置、浏览器与MCP认证策略全部保持不变。

## 3. 用户即将执行的Reality：关闭→已有入口启动→刷新页面

**当前状态：PENDING / NOT YET VERIFIED。** 用户明确计划自行关闭现有连接、通过既有成熟启动方式恢复，再刷新ChatGPT页面。不要在本段创建自动任务、远程强制停止或提前给新进程编造PID。

冻结验收步骤（不改变原有启动器）：
1. USER_STOPPED（用户自主关闭后）：若插件临时不可用属预期，不误判代理/网络永久故障；切忌自动启动另一条Tunnel制造重复实例。
2. USER_STARTED（用户用已有桌面入口启动，密码只在其本机输入）：观察官方启动回执及一个合法Tunnel进程；若未完成启动，直接按真实错误定位，不额外开新实例。
3. CHATGPT_REFRESHED（用户刷新ChatGPT并回到本会话，发“已重启并刷新”）：这一明确用户通知是新轮任务接受点。首先工具`GPT-Windows-MCP-Bridge.read_file`**恰好一次**，目标`C:/AI/GPT-Windows-Bridge-B/Launch-OpenAI-Real-MCP.ps1`，`offset=0,length=12`，逐字核对已知前12行。失败原样回报，禁止“为凑PASS”重试。
4. 仅当第3步PASS，再无侵入地查询`tunnel-client`实例数、PID与父PID、`--mcp.stdio-send-initialized-notification`标志、已注册`GPT-Windows-Tunnel-Recovery-v1`运行状态和SHA256；不读取、打印、上传Runtime Key或私密环境变量。
5. 第4步PASS且用户还要求稳定性复验时，在该**新实例**上5次独立、同输入只读工具调用；记录每轮真实耗时、错误、PID，若任何一次出现409/Session terminated/502则停下取证，回GOOD/BAD/FIRST_DELTA，不继续盲目发新任务。
6. 结果声明分级：
   - `V4_SKILL_PUBLISHED`：在线技能包索引、版本号、证据回读PASS。
   - `USER_RESTART_REALITY_PASS`：用户关闭后确有新进程，重启后ChatGPT真实read_file成功。
   - `POST_RESTART_SCOPED_5_5`：重启后新实例上五次独立读均通过；不是跨五次Windows启动。
   - `UNATTENDED_RECOVERY_FINAL_VALID`：仅当非人工恢复的实际进程退出→原Supervisor重启→完全重新初始化→ChatGPT真实读取全链路有可核对证据才可PASS；手动重启成功不算。
   - `WIN_LOGIN_AUTOSTART`、`LONG_DURATION_ZERO_FAILURE`、`PHYSICAL_TIME_OPTIMUM`维持UNKNOWN/NOT_TESTED直至有各自真实回执。

## 4. Freeze、回滚与后续页面接续

任务定位：`A-V4-USER-RESTART-20261015`。页面自然节点：`METHOD_FREEZE_PUBLISHED→WAIT_USER_RESTART→POST_REFRESH_REALITY→FINAL_SCOPED_OR_FAIL`。
计时唯一标准：从新轮用户已启动与发回“已重启并刷新”到该轮真实合格工具回执；以前3.9–7.9秒历史只读性能用于比较，不能把旧轮局部速度相加。
这轮升级只改仓库技能包元数据及成熟规则索引，不强改当前Windows启动器/任务/证书/密钥。原有历史V3/B工件及修复前PowerShell脚本备份全部保留。
回退如新V4规则自身有错误：仓库上一个V3的SKILL.md blob SHA是`e7f13d79d55d067c3cbf2e3201169a0b0f0b9f81`，可用Git历史原文件回退，而不动用户的在线Tunnel。任何改动先对比当前SHA并验收后才操作。
证据来源：[A路重载+8/8报告](A_ROUTE_LIVE_STABILITY_20261015.md)、[PS-002修复](A_ROUTE_PS002_REALITY_20261015.md)、[A路官方恢复SOP](TUNNEL_AUTORECOVERY_V2_20261015.md)、[B路V3 Reality](GITHUB_WINDOWS_B_ROUTE_V3_20261015.md)。
