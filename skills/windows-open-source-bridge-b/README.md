# GPT ↔ Windows 开源 B 通道（隔离试验版）

- 任务：BRIDGE-B-OPEN-SOURCE-20261012
- 权威来源：本仓库；此目录只是 B 通道的部署证据和操作契约，不替换双路执行桥 v0.3.2。
- 目的：验证本地 MIT 开源 Desktop Commander MCP 0.2.52 + OpenAI Secure MCP Tunnel 客户端 v0.0.16 是否能提供 GPT ↔ Windows 的替代直连。
- 安装：由 `.github/workflows/windows-open-source-bridge-b.yml` 运行到 Windows self-hosted Runner；落盘 `C:\AI\GPT-Windows-Bridge-B`；不覆盖原 DCR 和原 Runner。
- 不得修改：FlClash、系统代理、现有浏览器、原 DCR 自动启动、系统 PATH、原 v0.3.2 桥接配置。
- 无凭据不启动远端隧道：官方 Tunnel 需要 OpenAI Platform 的 `CONTROL_PLANE_TUNNEL_ID` 和 `CONTROL_PLANE_API_KEY`，且目标 ChatGPT 工作区需要合适的隧道权限。不得将密钥写入仓库、workflow、日志或对话。
- 成熟组件：`@wonderwhy-er/desktop-commander@0.2.52`，`openai/tunnel-client v0.0.16 Windows amd64`。均固定版本；升级必须重新验证。
- 安全：未经鉴权不得公网暴露本地 MCP；仅按 OpenAI 官方隧道协议接入；生产启用前审查目录访问、危险命令、用户批准。
- 验收：Node 版本≥22.12、MCP npm 安装成功、JSON-RPC initialize + tools/list 实际成功、官方 Tunnel zip SHA256 匹配、tunnel-client.exe 可运行 → `LOCAL_READY`；远端 `doctor` 和 `readyz` 健康、ChatGPT 实际调用工具并收到 Windows 回执 → `FINAL_VALID=YES`。
- 每次运行 GitHub Actions 日志和 artifact，以及 Windows 独立目录 evidence.json，必须保留真实错误；不可用本地成功冒充云端连通成功。
- 故障处置：优先对照正确基线，依据第一处真实差异修复；不删除、重建现有桥接系统。
- 官方说明：https://github.com/wonderwhy-er/DesktopCommanderMCP 与 https://github.com/openai/tunnel-client/blob/master/docs/onboarding.md
