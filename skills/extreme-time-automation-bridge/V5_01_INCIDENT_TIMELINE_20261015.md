# V5.0 附件一｜A路事故全时间线与证据等级

版本：5.0.0；日期：2026-10-15；方法：《三人行》第2版（任务级指定）；目标：升级既有桥，不新建连接。
资料原则：按“成熟基线GOOD→真实坏例BAD→第一差分FIRST_DELTA→最小修复→一次完整Reality→Freeze”。所有时间为Windows北京时间；旧PID是历史定位，绝不作为下次操作的PID。

## 故障族一：旧进程退出与协议初始化并不等价
2026-10-14实际出现`Session terminated`、409 `mcp_initialization_required`；同PID时也能返回409。故障树必须分别判断进程是否消失、MCP子进程是否初始化、ChatGPT是否真实read_file成功。本地健康正常不能替代远程调用。
2026-10-15 00:05前后的旧PID17876没有加载正式启动器后加入的官方初始化通知参数；只修了PS1文件，不等于该PID正在使用新版参数。之后新实例确实带官方参数，但曾仍出现工具会话问题；不能将所有409认定为该参数未加载。

## 故障族二：人为断线暴露Supervisor PS5.1旧错误
曾有临时验证文件`persistence/Validate-OneTunnel-Recovery-20261015.ps1`对PID17876执行Stop-Process，造成实际连接中断，违反“非必要不触碰健康隧道”的质量原则。对应100秒内无人恢复回执为`NO_AUTORECOVERY_WITHIN_100_SECONDS`。
旧守护器PID46072在01:40:54、01:41:05、01:41:26、01:42:06、01:43:07连续五次写`TUNNEL_START→TUNNEL_EXCEPTION→TUNNEL_EXIT`；B备路独立日志中异常类型是`RemoteException`。用户后来重新输入密钥才恢复。具体的旧进程退出原因未证明，不得猜测是代理波动或客户端崩溃。

## 同构负例和实际补丁
Run 38613246245：Windows PowerShell 5.1中原生命令stderr经过`2>&1`在`$ErrorActionPreference='Stop'`场景会变成`NativeCommandError / RemoteException`。与既有`powershell-reliability-guard`技能的PS-002故障族一致。
Run 38613712678：`1>$null 2>$null`仍产生同类异常；淘汰，未落地。
Run 38613908407：仅将native执行的错误动作临时设`Continue`、finally还原，正常退出码0与明确失败退出码19均正确区分；同构PASS。
Run 38614479599：整文件参考与本机文件差分不符合“只改一层”，`NON_MINIMAL_PATCH_REJECTED`阻止部署，原文件不动。
Run 38614765358：依据本机原文件SHA+唯一代码片段修正，备份、原子替换并回读通过；独立只读Job116027625193复核新SHA。修复只处理原生错误流，不更改网络、登录、隧道或权限。

## 故障族三：文件修复≠正在运行的旧守护器换代码
即使修复文件已落盘，PID46072仍运行修复前代码，02:35:57再次`TUNNEL_START`，1.9秒后异常退出。这证明缺少“守护进程合法重新加载”环节。
02:44在确认唯一隧道PID30820的父进程独立后，仅通过Windows现有任务计划程序Stop/Start该恢复任务：守护PID46072→8580，隧道PID30820未变化。新PID8580日志`SUPERVISOR_STARTED`、`EXISTING_TUNNEL`。随后八次ChatGPT真实read_file全部通过，重新加载后另五项MCP功能操作通过（仅同一登录/隧道生命周期）。一次嵌套JSON字符串观察器误标FALSE，原始回执实际成功，属于验收器错误。

## 故障族四：自动启动后初始化窗口和状态窗口误判
02:54:58，新守护PID8580写`TUNNEL_START`；之后唯一Tunnel PID46156的父PID为8580，具有官方通知参数。这是真实的一次Supervisor建起Tunnel的证据，不是空任务。旧隧道何时/为何消失尚无法独立确认。
用户第一张真实截图：快捷方式检测同一PID46156，但`MCP_NOT_INITIALIZED`，2秒后退出。
第二张：PID46156已`HEALTHY`，仍2秒后退出。原因是原`Restore-Interactive.ps1`在已存在Tunnel分支，无论健康还是暂时未初始化，都只暂停2秒退出。退出的是**状态窗口**，不是后台Tunnel。
V4仅修“已有Tunnel状态分支”：同PID最多180秒（5秒间隔）复查初始化；HEALTHY后交互等待按Enter，身份/健康异常时展示错误不启动第二隧道。已实测正式脚本退出码0、原SHA备份、进程不变。用户后来明确反馈窗口持续停在`Status HEALTHY. Press Enter to close this status window`，交互目视门PASS。

## 故障族五：当前短时可用≠开机自动使用永久保证
后续本机PID46156、父PID8580、一个Tunnel；MCP initialized、控制面polling、失败计数0。ChatGPT侧实际读文件、只读PowerShell通过，本轮4次读文件全部PASS（首次约5.245秒，其后4.241/7.828/5.439秒）。
03:18左右Windows任务信息：`GPT-Windows-Tunnel-Recovery-v1`=Running，用户A、Interactive、Limited；有AtLogOn触发和每5分钟重复（365天），IgnoreNew，StartWhenAvailable、RestartCount=3、RestartInterval=1分钟。本地加密凭据文件存在，未读取其内容。看到一次真实Supervisor启动Tunnel，**不等于真实关机重启并重新登录的端到端测试完成**。未登录Windows之前自动连接不属于当前方案保证范围。

## B路成熟结果继承但不能借给A路
原FULL历史419/422秒有下载`actions/upload-artifact`依赖ZIP超时，另有97/144秒成功。旧FAST只有日志证据，曾27秒PASS。V3新增双作业有界官方Artifact已五次独立Run和工件下载PASS，观察36/36/30/36/38秒，均值35.2秒，仅限小型、非敏感、成功证据合同。FULL长尾未证实根除，大结果/失败证据/强审计不应换成有界方案。V5不修改生产B路。

## 跨项目边界
Hermes生态站F002另有一次HTTP400、42项合成验收测试，不是桥接A路409根因，也不属于本技能包的五轮质量证据。GitHub Runner在NETWORK SERVICE身份访问用户A目录曾遭Access Denied，不能通过改变ACL绕过。V5不重派那些未知副作用任务。

参考：`A_ROUTE_PS002_REALITY_20261015.md`、`A_ROUTE_LIVE_STABILITY_20261015.md`、`V4_DESKTOP_STATUS_ENTRY_REALITY_20261015.md`、`GITHUB_WINDOWS_B_ROUTE_V3_20261015.md`，均在同一技能包目录。
