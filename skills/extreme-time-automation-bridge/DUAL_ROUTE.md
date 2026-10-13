# GPT直连Windows双路执行桥｜双路执行策略 v0.3.0

> **最新 V1.0（2026-10-13）覆盖入口**：日常首选已验 A 自建 MCP，B GitHub 独立备援与长任务，第三方 R 用免费额度运营 V1.0 控制。详见 [V1.0 GitHub 速度与路由报告](V1_GITHUB_WINDOWS_SPEED_AND_ROUTING.md)。以下静态旧路由仅为历史，不得覆盖新冻结。

> **现行 v0.3.4 操作覆盖（2026-10-13）：** 每次远程执行前先读 [Remote 免费额度成熟运营 V1.0](REMOTE_DCR_QUOTA_OPERATIONS_V1.md) 并按需运行 [无副作用判路器](bootstrap/Invoke-Remote-Quota-Route-Gate.ps1)。日常在线短操作优先 A 自建 MCP，异步/长任务优先 B GitHub，托管 R 必须通过免费额度闸门；R 截至 2026-10-13 已显示剩余 0%。本文件历史“DCR 主路”和 2026-10-12 状态均保留以备回溯，不是当前默认。发现误用应在调用前提醒并改路。

> **2026-10-12 v0.3.4 最新运行覆盖规则：** 本文 v0.3.0 的“DCR 主路/Runner 备路”是原架构的历史命名，不代表此刻应优先耗用 DCR。现按用户明确要求改为 **自建可用路线优先**：GitHub 共同工作区 → Actions → Windows Runner 今日真实任务 `BRIDGE-LINK-CHECK-20261012-1901` PASS；OpenAI Tunnel 当前 `Session terminated` 且 Windows 隧道进程=0，需依原手动恢复入口重连；第三方 DCR 在线/Ping 但本月额度耗尽，暂停远程执行，**2026-11-01 为用户预定的额度复查日，不保证重置成功或保底 15 天**。完整状态、证据及具体切换规则请读 [ROUTE_PRIORITY_QUOTA_AND_FAILOVER_20261012.md](ROUTE_PRIORITY_QUOTA_AND_FAILOVER_20261012.md)。原 DCR 配对、已运行任务、自启配置、Runner、原故障恢复手册均保留，不删除。


## 路由
主路：ChatGPT → Desktop Commander Remote → Windows
备路：ChatGPT/GitHub → GitHub Actions → Windows self-hosted runner

## 主路当前 Reality
- DESKTOP-4A1EGTM
- 当前有效 Device ID：503e66bf-4f80-49fc-a90f-020ec8c71b1e
- App 0.2.52
- Online=PASS
- ping=PASS
- Windows 命令=PASS
- 旧 Device ID 28ebd1ea-e749-466d-ad88-1b9f262d0651：Offline，仅历史记录。

## v0.3.0 主路恢复门
若主路 Offline：先直接运行 npx -y @wonderwhy-er/desktop-commander@latest remote。
若出现 JSON/config 或 lock 错误，执行 DCR_RECOVERY.md。
重新配对后必须同时满足 list_devices=Online、ping=PASS、真实 Windows 只读命令=PASS。
startAttempted=true、计划任务启动成功、进程存在、device.json 存在均不能单独判定恢复。

## 后台自启动/自重连
计划任务：GPT-DesktopCommander-Remote-Autostart
用户：A
launcher：C:\Users\A\AppData\Local\DesktopCommanderRemote\Start-DesktopCommanderRemote.ps1
AtLogOn + Interactive；Remote 退出后 5 秒重启；MultipleInstances=IgnoreNew。

AUTOSTART_CONFIGURED=YES
AUTORECONNECT_CONFIGURED=YES
REBOOT_REALITY=NOT_YET_TESTED

下次 Windows 真重启后的唯一验收：无需手工运行 npx，设备自动 Online，随后 ping PASS、Windows 命令 PASS。

## 备路
GitHub Actions + self-hosted runner：DESKTOP-4A1EGTM-etal，Reality PASS，用于 DCR 主路不可达时的独立控制与修复。

## 安全边界
- 不修改 FlClash。
- 不修改 Windows 网络代理。
- 不重复执行同一副作用任务。
- 所有恢复结果以最终外部验收为准。