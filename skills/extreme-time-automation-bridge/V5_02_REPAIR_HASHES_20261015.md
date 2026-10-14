# V5.0 附件二｜可复用成熟修复、精确文件证据、回滚

## 固定方法和执行入口
本版仍用原有OpenAI Tunnel v0.0.16、Desktop Commander MCP、Windows Task Scheduler，不新建守护器。原路径`C:\AI\GPT-Windows-Bridge-B\`，`persistence\`保存守护器、健康检查、快捷方式入口。主路失败时才按原V3.0合同选择FAST/V2有界Artifact/FULL备路。

## PS-002故障：Windows PowerShell5.1错误流转成致命异常
原守护器将官方native命令的stderr `2>&1`合并，在`$ErrorActionPreference='Stop'`时记录`RemoteException / NativeCommandError`。复用已有`skills/powershell-reliability-guard` PS-002成熟规则：只在原生命令调用期间局部`Continue`，立即保存`$LASTEXITCODE`，finally恢复原偏好，后续真实非零退出仍保留。Windows负例Exit19与正例Exit0均通过。
正式守护器：`persistence\Recovery-Supervisor-v1.ps1`
- 修前SHA256：`D5B2D1098F51794B6022B60035BA6D0E6A0E5F7C016FF346540A059744BA35`
- 修后SHA256：`649E7A939AA8A27B91FE5FBE130E842E131EB96D55F36A1C00FED405335270EF`
- 原备份：同目录`Recovery-Supervisor-v1.ps1.bak-ps002-20261015`。
- 备份/新文件哈希实际回读PASS；不能用仓库参考文件整份覆盖本机差分。
- 文件更改以后旧进程PID46072仍运行旧代码，所以通过已有Windows任务计划程序合法Stop/Start该**守护任务**，确认当时隧道PID30820不变，新守护PID8580。这不等于重启隧道。

## 桌面状态窗口故障：MCP初始化窗口误报+2秒后消失
桌面快捷方式`GPT-Windows-MCP-一键恢复`指向`persistence\Restore-Interactive.ps1`。已存在Tunnel时，旧脚本无论健康与否均约2秒退出，终止的是状态窗口，不是后台服务。新脚本仅重写“已有进程”分支：只允许唯一PID；MCP_NOT_INITIALIZED/NOT_READY在同PID最多180秒、每5秒复查；HEALTHY时明确显示状态并等待人工按Enter关闭窗口。异常提示可见且拒绝二次启动。不存在进程时继续原交互启动流程。
正式入口`persistence\Restore-Interactive.ps1`
- 修前SHA256：`A97F5B735C531B76C46B96A5DE66682A4F79F3A30267C99FA6511ABDF60027E6`
- 修后SHA256：`070E8921F7E27D0BA82057C98F183C1EFFE65C43A6F9AB651C059F9432B26921`
- 原备份：同目录`Restore-Interactive.ps1.bak-20261015-v4-window`。
- 实测：PS5.1 Parser0错误，原子备份及哈希匹配、非交互正式脚本退出码0、PID46156不变、无第二实例；用户实际双击确认窗口持续显示`Status HEALTHY. Press Enter to close this status window`，交互目视PASS。
- 仓库镜像：`bootstrap/Restore-Interactive-V4-Status.ps1`；窗口关闭不影响隧道。

## 真实启动与保留边界
原恢复任务`GPT-Windows-Tunnel-Recovery-v1`配置AtLogOn用户A、每5分钟循环、Interactive Limited、IgnoreNew；修复后的守护PID8580实际创建隧道PID46156并能远程读文件。这是**已登录环境下某次自动启动成功**的证据，不是整机重启/首次登录后五轮成功。任务最近结果码出现过`0x800710E0`，应保留事实，不以Running判定所有能力PASS。

## 回滚规则
任何回滚必须在合法用户上下文、确认当前SHA匹配和单实例后，针对故障文件单独使用原备份，不能因为旧参考代码存在就盲覆盖。若没有新的真实故障，停止改动生产脚本和代理。此次V5是原技能包方法/证据升级，不更换现有Windows配置。
