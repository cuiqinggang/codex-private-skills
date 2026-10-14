# A 路成熟修复｜PowerShell 5.1 原生错误流误判与 MCP 初始化（2026-10-15）

STATUS=SCRIPT_PATCHED_AND_INDEPENDENT_READBACK; ACTIVE_SUPERVISOR_RELOAD_NOT_TESTED; A_MCP_END_TO_END=FAIL_LAST_ATTEMPT
PARENT=GPT直连Windows双路执行桥 V3.0
INCIDENT=HERMES-ECO-20261014 / A-TUNNEL-PS002-20261015
METHOD=三人行V2任务级复用 + powershell-reliability-guard PS-002；不新增守护器或通信通道。
NO_AGENT_OR_PROXY_OR_TUNNEL_RESTART=TRUE

## GOOD / BAD / FIRST_DELTA

既有Windows任务计划程序`GPT-Windows-Tunnel-Recovery-v1`与`Recovery-Supervisor-v1.ps1`都曾运行。旧进程PID17876被一次附加的临时测试脚本中断后，守护日志确有五次`TUNNEL_START→TUNNEL_EXCEPTION→TUNNEL_EXIT`：北京时间01:40:54、01:41:05、01:41:26、01:42:06、01:43:07；返回异常种类均为`RemoteException`，未在100秒内恢复。之后用户手动启动单一进程PID46772。

FIRST_DELTA：原守护器在`$ErrorActionPreference='Stop'`环境下执行`& tunnel-client ... 2>&1 | Out-Null`。Windows PowerShell 5.1会把native stderr转成带`NativeCommandError`的PowerShell错误并触发终止，外层catch把正常CLI诊断输出误判为启动异常。已有技能包`skills/powershell-reliability-guard/references/error-catalog.md` 的PS-002正覆盖此故障族。

## 实际同构诊断、淘汰与成熟最小修复

已有GitHub只读工作流`.github/workflows/tunnel-r2-oob-readonly-20261014.yml`，不更改系统代理、Runner设置、权限、已登录浏览器或隧道：
- Run 38613246245：守护日志五次`RemoteException`；PowerShell 5.1原生命令stderr重定向复现实测`RemoteException / NativeCommandError`。
- Run 38613712678：候选`1>$null 2>$null`仍发生`RemoteException`，淘汰；没有部署。
- Run 38613908407：仅在native命令执行期间使用`ErrorActionPreference=Continue`且`finally`恢复，正常stderr示例退出码0、故意非零示例退出码19，PASS。
- Run 38614479599：全文件比对发现本机与在线参考还有其它差分，部署在写前的`NON_MINIMAL_PATCH_REJECTED`被阻断；不覆盖本机其他修改。
- Run 38614765358：按当前本机正式文件SHA`D5B2D1098F51794B6022B60035BA6D0E6A0E5F7C016FF346540A059744BA35`与唯一目标片段，保留所有本地差异，仅替换PS-002执行段；Windows PowerShell 5.1真实Parser通过，原文件备份保存在`C:\AI\GPT-Windows-Bridge-B\persistence\Recovery-Supervisor-v1.ps1.bak-ps002-20261015`；原子替换成功。
- 部署后正式文件SHA256=`649E7A939AA8A27B91FE5FBE130E842E131EB96D55F36A1C00FED405335270EF`，旧备份SHA与前值吻合，PID46772未变化。
- 从独立GitHub只读复验（Run 38613908407再次运行，Job 116027625193）：同一新SHA再次回读，隧道数1、PID46772，健康日志`mcp=initialized`、`poll_failures=0`、`dispatcher_failures=0`。

原技能包`bootstrap/Recovery-Supervisor-v1.ps1`源码也已同步只改上述执行段，源GitHub blob SHA=`0cf755c969a9ad4b86e8064546f5214465bb185d`。现有Windows正式文件因为保留本地差异，其字节SHA不同于GitHub参考源码，这是正常且刻意的。

## 未通过的门（不能扩大为已修复）

1. **守护器运行时生效**：当前Windows任务计划程序中的守护进程可能仍在执行替换前已加载的脚本。未在本轮重启它；不能把磁盘文件补丁PASS冒充新的实际无人值守恢复PASS。需要在获准用户A上下文按原计划任务的官方Start/Stop方法、且确认不会中断唯一Tunnel后重新加载；无合法权限时等待原任务下次自然启动，禁止借Runner的NETWORK SERVICE身份更改ACL或提升权限。
2. **MCP初始化**：新PID46772曾通过用户权限现场核实携带`--mcp.stdio-send-initialized-notification`；Windows健康快照正常，但ChatGPT真实`read_file`仍返回`Session terminated`。官方协议要求legacy调用方完成`initialize`；补丁仅在成功initialize后发送`notifications/initialized`，不能主动伪造initialize。调用方握手记录尚不可见，不能断言是哪一端遗漏。不得通过多隧道或重启代理尝试修复客户端会话状态。
3. **最终质量**：新守护器重新加载后的受控真实恢复、ChatGPT远程文件readback、连续8次初始化/调用和五次独立运行、Windows真实登录/开机、长期稳定尚未通过。标记`AUTO_RECOVERY_FINAL_VALID=NO; A_MCP_INIT_FINAL_VALID=NO`。

## 后续唯一操作次序

- 不执行遗留`Validate-OneTunnel-Recovery-20261015.ps1`的Stop-Process，不终止健康隧道；当前PID只作历史定位，后续按现场变化取证。
- 取得当前A会话真实读能力后，检查现有计划任务和隧道的父子关系，合法重新加载原守护脚本但保留单隧道，再等待真实恢复节点/已批准的唯一维护窗口按V2 A SOP验收。凭据只能由Windows本地DPAPI使用，严禁读取或上传。
- ChatGPT端仍失联时，只采用插件/隧道官方初始化诊断与平台提供的重新连接入口；错误原样记录。不能从Windows侧合成ChatGPT的initialize或改动FlClash。
- 故障修复后恢复原Hermes任务，状态`HERMES-ECO-20261014/F002`的首轮已因独立HTTP400标FAIL，不能计入五轮。
