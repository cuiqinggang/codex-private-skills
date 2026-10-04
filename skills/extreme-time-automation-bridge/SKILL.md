---
name: extreme-time-automation-bridge
version: "0.3.0"
description: GPT直连Windows双路执行桥。主路为 Desktop Commander Remote，备路为 GitHub Actions + Windows self-hosted runner；新增 DCR 配置损坏后的最短重配恢复与后台自启动自重连。
---

# GPT直连Windows双路执行桥 v0.3.0

STATUS=REALITY_PARTIAL_PERSISTENCE
VERSION=0.3.0
PRIMARY_ROUTE_CURRENT=PASS
PRIMARY_DEVICE_NAME=DESKTOP-4A1EGTM
PRIMARY_DEVICE_ID=f6990966-5870-484b-bf79-409bc6fb963e
PRIMARY_APP_VERSION=0.2.52
PRIMARY_PING_REALITY=PASS
PRIMARY_WINDOWS_COMMAND_REALITY=PASS
OLD_DEVICE_ID=28ebd1ea-e749-466d-ad88-1b9f262d0651
OLD_DEVICE_STATUS=OFFLINE
FALLBACK_ROUTE_CURRENT=PASS
FALLBACK_RUNNER=DESKTOP-4A1EGTM-etal
DCR_AUTOSTART_TASK=GPT-DesktopCommander-Remote-Autostart
DCR_AUTOSTART_USER=A
DCR_AUTOSTART_ENABLED=YES
DCR_RECONNECT_LOOP=YES
REBOOT_PERSISTENCE_REALITY=NOT_YET_TESTED

## v0.3.0 新增：DCR 最短恢复法

当 Remote 离线且运行 npx -y @wonderwhy-er/desktop-commander@latest remote 出现 JSON/config 或 lock 错误时，按 DCR_RECOVERY.md 执行：停止旧实例 → 备份坏配置/旧配对 → 重新运行 remote → 原 Google 账号重新配对 → 独立 ping → Windows 命令验收。

本次 Reality：新设备 503e66bf-4f80-49fc-a90f-020ec8c71b1e Online；ping PASS；Windows 命令 PASS。旧设备仅保留为 Offline 历史记录。

## 后台自动连接

已创建 A 用户登录态计划任务 GPT-DesktopCommander-Remote-Autostart。
launcher：C:\Users\A\AppData\Local\DesktopCommanderRemote\Start-DesktopCommanderRemote.ps1

行为：A 用户登录后自动启动；Remote 退出后 5 秒自动重启；MultipleInstances=IgnoreNew。

注意：尚未经过真实 Windows 重启后的 Reality 测试，所以开机持久化只能标记“已配置、待验收”，不能标 PASS。

## 双路规则

1. DCR Online 且能力覆盖 → 主路。
2. DCR 离线 → 优先按最短恢复法恢复。
3. 主路暂不可恢复而 GitHub runner Online → 备路。
4. 两路都不可用 → 明确阻塞原因，不伪装成功。
5. 不修改 FlClash / Windows 网络代理。

## 2026-10-04 双路真实复验 R1（当前状态）

- 当前在线主设备 ID：f6990966-5870-484b-bf79-409bc6fb963e；历史503e设备已Offline，以实时list_devices为准。
- 主路：真实Windows命令、部署、循环检查与实际runtime inbox验证PASS。
- 备路：首测 Actions run 37192980220 在 Git checkout 阶段两次连接GitHub失败；不得把Online当畅通。
- 根因范围修复：Windows任务不再依赖Git partial clone补取blob；从同一github.sha经Contents API按需读取任务JSON、payload和Invoke-BridgeTask.ps1。每文件最多3次、每次30秒、间隔2秒；使用本次workflow临时token，不存入文件/日志。
- 复测 run 37193387268 全部success；实际runner=DESKTOP-4A1EGTM-etal，执行exit_code=0、duration_ms=2453.998，真实进程/文件循环4/4 PASS及唯一marker回传。
- 未修改FlClash、Windows网络代理；当前双路限定命令任务PASS不保证未来零故障，不替代重启/注销持久化Reality。
- 证据：../long-term-memory-super-virtual-human/evidence/V050-WINDOWS-GOAL-LOOP-REALITY-20261004-R1.json。
