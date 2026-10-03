# DCR_RECOVERY｜Desktop Commander Remote 最短恢复手册

版本：v0.3.0

## 触发条件
当 DESKTOP-4A1EGTM 为 Offline，或运行 npx -y @wonderwhy-er/desktop-commander@latest remote 出现：
- Failed to initialize config
- Unexpected token ... is not valid JSON
- Lock file is already being held

## 最短恢复
1. 禁用旧任务 GPT-DesktopCommander-Remote-Autostart，避免旧实例重新抢锁。
2. 停止 Desktop Commander / DesktopCommanderRemote 相关残留进程。
3. 备份而不是删除旧状态目录：
   - C:\Users\A\.claude-server-commander
   - C:\Users\A\.desktop-commander-device
4. A 用户 PowerShell 重新运行：npx -y @wonderwhy-er/desktop-commander@latest remote
5. 按浏览器流程使用原 Google 账号授权/重新配对。
6. ChatGPT 侧强制验收：list_devices=Online、ping=PASS、真实 Windows 只读命令=PASS。

不得用 startAttempted=true、进程存在、task=Running、device.json 存在替代最终验收。

## 本轮 Reality
DATE=2026-10-03
DEVICE_NAME=DESKTOP-4A1EGTM
NEW_DEVICE_ID=503e66bf-4f80-49fc-a90f-020ec8c71b1e
APP_VERSION=0.2.52
PING=PASS
WINDOWS_COMMAND=PASS
OLD_DEVICE_ID=28ebd1ea-e749-466d-ad88-1b9f262d0651
OLD_DEVICE_STATUS=Offline

## 自动保持连接
launcher：C:\Users\A\AppData\Local\DesktopCommanderRemote\Start-DesktopCommanderRemote.ps1
计划任务：GPT-DesktopCommander-Remote-Autostart
- A 用户登录后启动
- Interactive 用户态
- Remote 退出后 5 秒自动重启
- MultipleInstances=IgnoreNew

当前：已配置；尚未经过真实 Windows 重启后的 Reality 验收。