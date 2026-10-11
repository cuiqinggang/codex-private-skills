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

## 2026-10-12 成熟组件组合判断

| 层级 | 组件 | 开源/收费边界 | 可复用能力 |
|---|---|---|---|
| 本地工具 | Desktop Commander MCP 0.2.52 | MIT；本地无厂商远程调用配额 | 文件读取/写入、终端、进程等；MCP initialize + tools/list 已在实际 Windows 上发现 26 项 |
| 检查工具 | MCP Inspector | MIT | MCP tools/list、tools/call、HTTP/stdio 验收；必要时使用，无需单独编写测试平台 |
| 私有隧道 | OpenAI Secure MCP Tunnel Client v0.0.16 | 开源客户端；官方控制平面与 ChatGPT 权限不因此免费或不受限 | 出站 HTTPS 隧道、healthz/readyz、日志/监控、stdio 代理 |
| 候选替代传输 | Supergateway + Cloudflare Tunnel | Supergateway MIT；Cloudflare 免费方案有服务条件 | stdio ↔ Streamable HTTP → HTTPS；不提升 ChatGPT 自定义 MCP 写入权限 |
| 现成执行保障 | GitHub Actions + Self-hosted Windows Runner | 本地 Runner 不计 GitHub 托管分钟；有 API、工作流、存储及账户限制 | 已有 v0.3.2 通道，能独立执行 Windows 任务并回收证据；不受 DCR 托管配额影响 |

**硬边界：**
- 开源工具无法解除 ChatGPT 平台对自定义 MCP 的权限审核、套餐限制、使用许可和确认规则。官方截至 2026-10 的说明：完整自定义 MCP 写入/修改权限适用于 Business、Enterprise/Edu；个人 Pro 自定义 MCP 主要允许只读。应按本账号实际可见功能验收。
- 官方 Secure MCP Tunnel 需要 Platform 管理的 Tunnel ID、具有 Tunnels Read+Use 的 runtime key，并关联目标 ChatGPT workspace；凭据必须由用户通过正式管理页面安全配置。**绝不提交到 Github**。官方地址：https://platform.openai.com/settings/organization/tunnels 。
- 准备连接的 Windows MCP 应在交互式 Windows 用户 A 会话中运行，而非默认假设 Windows Runner 服务账户就能操作用户桌面。到时独立验证会话身份及授权目录。
- 不对外开放未认证的 MCP HTTP 端口；Cloudflare/公开反向代理不是绕开权限或身份验证的替代方法。

**优先顺序：** 先保留 v0.3.2 GitHub Runner 可用执行，完成本地 MCP + 官方隧道文件安装，再检查当前帐号 Platform/ChatGPT 授权；能合规连接才走 Tunnel ChatGPT 端到端。最终真实读、写、Shell、会话保持、断线恢复、并发隔离经过验证，才可能宣布体验等价。否则执行任务继续走既有 GitHub Runner。

### 本轮真实记录
- run [38168747170](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38168747170)：Node v24.14.0；固定 npm 包 0.2.52 安装，MCP 初始化/列工具 PASS（26 项）；GitHub releases DNS 失败，故 Tunnel 安装未完成。
- run [38169151688](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38169151688)：Github 云端 SHA256 校验和 Windows Artifact 传递 PASS；安装脚本误查找 EXE 名，需差分修复。
- run [38169303390](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38169303390)：完整发行包的官方 SHA256 在 Windows 上 PASS，已见 `tunnel-client.exe` 和 `tunnel-client-runtime.exe`；脚本选错 runtime 版本调用完整 CLI，故验证失败，并非下载/安装完整性失败。
- run [38169435718](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38169435718)：按正确的 `tunnel-client.exe` 做非授权 CLI 和 MCP 实际工具调用验收；以实际日志结果为准。

原 v0.3.2 文档、流程及历史证据只读保留；当前 B 通道在没有 ChatGPT 端到端通过前 `FINAL_VALID=NO`。

### 最新 Reality 结果：2026-10-12 (北京时间)
- **run 38169533429：LOCAL_FUNCTIONAL_PASS**（Windows 主机 DESKTOP-4A1EGTM, Runner DESKTOP-4A1EGTM-etal）。官方 `tunnel-client.exe` CLI version 0.0.16 及 `help quickstart` PASS；MCP `tools/list=26`，真实 `tools/call list_directory` PASS，真实 `tools/call start_process` PowerShell 输出 `BRIDGE_B_LOCAL_COMMAND_PASS`，运行日志和 artifact 已上传。
- 标准验收严格区分：`LOCAL_FUNCTIONAL_PASS=YES`；`CHATGPT_REMOTE_READY=UNKNOWN/NO EVIDENCE`；`TUNNEL_AUTHENTICATED=NO`；`FINAL_VALID=NO`。本地功能通过不能冒充 ChatGPT 页面实际连通。
- 安装目录：`C:\AI\GPT-Windows-Bridge-B`。本次没有修改系统代理或覆盖原执行桥。
- 下一步若账号获得官方合法 Tunnel 权限，采用其 `tunnel-client init ... --mcp-command` 指向本目录已安装的 Desktop Commander MCP。将 Runtime Key 存在本机安全凭据存储，不写仓库或输出日志；从交互式用户会话启动隧道，确认 `readyz`、ChatGPT 注册工具的可见性、真实读写命令与授权确认规则。没有权限则停止这一受限步骤，改走现成 GitHub Runner 正式执行路径，不做绕过。

- 2026-10-12 Reality 增量验收：run [38169679396](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38169679396)，Windows 本机 MCP `tools/call` 实测目录读取 + PowerShell 命令输出 + 隔离目录 `write_file → read_file` 内容回读，全部 PASS；OpenAI 完整 CLI 0.0.16 通过。仅本地调用闭环 PASS，不代表隧道已鉴权或 ChatGPT 远程端到端通过。`B_LOCAL_FUNCTIONAL=PASS / B_CHATGPT_REMOTE=NOT_TESTED / FINAL_VALID=NO`。

## 2026-10-12 跨页新增：官方 Tunnel + ChatGPT 演示 MCP 远端回显通过（非 Windows 生产）

- 上游主技能包升级至 [`v0.3.3` 完整恢复手册](../extreme-time-automation-bridge/OPENAI_TUNNEL_CONNECT_RECOVERY_20261012.md)；[脱敏证据摘要](../extreme-time-automation-bridge/evidence/OPENAI_TUNNEL_DEMO_REALITY_20261012.md)。
- 用户已在 Platform 建立 `tunnel_6acbeee2ce888191b775cd53429c7597`，用 Windows 桌面完整版 `tunnel-client.exe` v0.0.16 启动官方 `--embedded-mcp-stub`，日志启动 PASS、`/readyz` 页面显示 `ready`。
- ChatGPT `https://chatgpt.com/plugins` 的「自定义 MCP」选择「隧道」，初选 OAuth 注册失败；针对**无敏感能力的官方 demo**改「无需身份验证」后，页面显示已连接；用户转交新页面的真实 echo 调用结果 `{"echoed":"hello from Windows"}`，`ECHO_REALITY_PASS=USER_RELAYED_INDEPENDENT_PAGE_REPORT`。
- 本目录的 `Desktop Commander MCP 0.2.52` 26 工具虽已由 Actions 在 **Windows 本机** 读、写、命令 Reality PASS，却**仍未**由刚建立的 ChatGPT Tunnel 插件直接远程调用。因此 `B_LOCAL_FUNCTIONAL=PASS / B_CHATGPT_DEMO_ECHO=PASS_USER_RELAYED / B_CHATGPT_REAL_WINDOWS_TOOLS=NOT_TESTED / PRODUCTION_FINAL_VALID=NO`。
- 保留已有 `C:\AI\GPT-Windows-Bridge-B`、DCR Remote、GitHub runner，不改 FlClash/系统代理。禁止把本次 demo 无身份验证扩展到生产 Windows 执行器。

## 2026-10-12 ChatGPT ↔ 官方 Tunnel ↔ Windows 开源 B 真实端到端 Reality PASS

- 真实 Windows 运行 Node.js 24.14.0 和已安装 Desktop Commander MCP v0.2.52；通过 OpenAI Tunnel Client v0.0.16 的 stdio `node.exe C:/AI/GPT-Windows-Bridge-B/mcp/node_modules/@wonderwhy-er/desktop-commander/dist/index.js --no-onboarding`。
- ChatGPT 工具目录刷新后新工具已发现，ChatGPT 当前会话直接调用 `list_directory`、`write_file`、`read_file`、`start_process`、`read_process_output`，目录读取、隔离文件写后读和无副作用 PowerShell 调用全部 PASS，PowerShell PID29708、exit code 0。
- 跨页可核验证据：[`../extreme-time-automation-bridge/evidence/OPENAI_TUNNEL_REAL_WINDOWS_REMOTE_PASS_20261012.md`](../extreme-time-automation-bridge/evidence/OPENAI_TUNNEL_REAL_WINDOWS_REMOTE_PASS_20261012.md)。
- `B_LOCAL_FUNCTIONAL=PASS / B_CHATGPT_REAL_WINDOWS_TOOLS=PASS / MINIMAL_FUNCTIONAL_FINAL_VALID=YES / REBOOT_PERSISTENCE=NOT_TESTED`。历史记录中的 `NOT_TESTED` 为当时的真实状态，按时间保留，不回写篡改；本条为后续真实进展。原 DCR 主路与 GitHub Runner 备路均保留。
