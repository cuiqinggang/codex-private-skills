# CHANGELOG

## 0.3.0 - 2026-10-03

- 正式升级为 GPT直连Windows双路执行桥 v0.3.0。
- 新增 Desktop Commander Remote 离线/配置损坏后的最短重配恢复法。
- 本轮真实故障症状：Failed to initialize config、Unexpected token ... is not valid JSON；此前还出现过 Lock file is already being held。
- 修复策略冻结：停止旧自启/残留实例 → 备份损坏配置与旧 Remote 身份 → 重新运行 npx -y @wonderwhy-er/desktop-commander@latest remote → 原 Google 账号重新授权/配对 → 外部独立验收。
- 新配对 Device ID：503e66bf-4f80-49fc-a90f-020ec8c71b1e，DESKTOP-4A1EGTM Online。
- Reality：独立 ping PASS；真实 Windows 命令 PASS。
- 旧 Device ID 28ebd1ea-e749-466d-ad88-1b9f262d0651 保留为 Offline 历史记录。
- 新增强制验收门：startAttempted=true、进程存在、计划任务成功都不能单独判定恢复；必须 Online + ping PASS + Windows 命令 PASS。
- 新增 A 用户后台 launcher：C:\Users\A\AppData\Local\DesktopCommanderRemote\Start-DesktopCommanderRemote.ps1。
- 计划任务 GPT-DesktopCommander-Remote-Autostart 已启用；AtLogOn、Interactive、MultipleInstances=IgnoreNew。
- launcher 在 Remote 退出后等待 5 秒自动重启。
- 尚未执行真实 Windows 重启 Reality，因此开机自动恢复标记 NOT_YET_TESTED。
- 新增 DCR_RECOVERY.md，作为以后 DCR 断线时的第一恢复入口。

## 0.2.0 - 2026-10-02
- 建立 Desktop Commander Remote 主路 + GitHub Actions self-hosted runner 备路。