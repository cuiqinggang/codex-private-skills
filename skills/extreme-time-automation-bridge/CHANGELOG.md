# CHANGELOG

## 0.3.3 - 2026-10-12｜OpenAI Secure MCP Tunnel 自定义插件接入与恢复

- **保留**原 DCR Remote 主路 / GitHub Actions self-hosted Runner 备路，且不重建旧配置。
- 增加 `OPENAI_TUNNEL_CONNECT_RECOVERY_20261012.md`：从 OpenAI Platform 隧道创建、工作区选择陷阱、完整 Windows amd64 安装包与 runtime 误选、CLI quickstart、Runtime API Key、PowerShell 原始启动命令、本地 readyz、ChatGPT 插件创建、身份验证选项、连接和真实 echo 工具回执的逐步操作。
- 增加 `evidence/OPENAI_TUNNEL_DEMO_REALITY_20261012.md`：原 PowerShell 日志决定性证据、`harpoon` 局部错误与 `main` 通道差分、浏览器 `ready`、用户转交独立页 `echo` 报告；不保存秘密密钥。
- 修复旧错误判断：`unsupported channel "harpoon"` 和 `target_count=0` 不足以推翻已可用的 `main` 演示 MCP 通道；demo 切换无身份验证后远端 echo 实际成功。警告保留以便后续真实 OAuth 诊断。
- 状态严分：`TUNNEL_DEMO_ECHO=PASS_USER_RELAYED`；`CHATGPT_REMOTE_REAL_WINDOWS_MCP=NOT_TESTED`；`PRODUCTION_FINAL_VALID=NO`。正式 Windows 读写、PowerShell、重启常驻和授权须单独 Reality。
- 安全：Demo「无需身份验证」不得用于具 Windows 命令/文件权限的真实 MCP；Runtime Key 应轮换到最小 `Tunnels Read+Use`；严禁把 Key 写入仓库；FlClash、系统代理、已登录浏览器及原自启动原样保留。

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

## 0.3.3 用户授权增量 - 2026-10-12
- 明确获用户同意：保留 `GPT-Windows-MCP-Bridge` 的 `Allow all actions` 和 「无需身份验证」选项，不将「必须改为 Always ask」作为启动前置条件。高权限风险和平台可能强制限制仍明确披露。
- 改动正式真实 Windows MCP 切换脚本并经 GitHub Runner 部署（复验状态以 Actions 记录为准）；密钥继续仅由用户在本机输入。
- Windows 主运行隧道尚未主动切换，真实远端读、写、命令仍待正式调用验收。
