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
PRIMARY_DEVICE_ID=503e66bf-4f80-49fc-a90f-020ec8c71b1e
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