# GPT直连Windows双路执行桥｜双路执行策略 v0.3.0

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