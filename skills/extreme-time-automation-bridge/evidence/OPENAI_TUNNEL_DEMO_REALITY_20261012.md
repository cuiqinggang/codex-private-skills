# 2026-10-12｜OpenAI Tunnel + ChatGPT Demo MCP Reality 证据摘要（已脱敏）

**TASK_ID**：OPENAI-TUNNEL-DEMO-20261012  
**TUNNEL_ID**：tunnel_6acbeee2ce888191b775cd53429c7597  
**插件名称**：GPT-Windows-MCP-Bridge  
**CLIENT**：tunnel-client v0.0.16+5f99daabd4aa4a77049e6d81d54a0d8c18335397（运行日志）  
**时间锚**：2026-10-12 04:56:54–04:56:56（Windows/日志时间）；2026-10-12 05:09:15–05:09:32 有 Harpoon 路由错误  
**原始材料类型**：用户上传 PowerShell 全量文本（386 行）、操作截图、用户转交的独立 ChatGPT 页 echo 工具调用报告。本文件摘录决定性的非秘密字段；不回传密钥、不伪造新工具日志。

## 1. 完整 Windows CLI / MCP 探针（原始日志）

以下都是从用户上传的 `粘贴的文本 (1)(20261011-205910).txt` 摘录，保留原英文关键字：

~~~text
PS C:\Windows\system32> powershell -NoExit -Command "& (Join-Path ([Environment]::GetFolderPath('Desktop')) 'tunnel-client-v0.0.16-windows-amd64\tunnel-client.exe') help quickstart"
Quickstart:
...
Embedded MCP stub enabled.
  MCP URL: http://127.0.0.1:55999/mcp
...
2026/10/12 04:56:54 INFO mcp channel route resolved ... channel=main transport=http-streamable ... target_host=127.0.0.1:55999 ... route_mode=direct
2026/10/12 04:56:54 INFO control-plane route resolved ... target_host=api.openai.com:443 route_mode=proxy proxy_source=env:HTTPS_PROXY proxy_url=http://127.0.0.1:7890
2026/10/12 04:56:54 INFO dispatcher channels registered ... [{Name:harpoon Priority:0 RoutableNow:false SupportsMCP:true SupportsOAuth:false} {Name:main Priority:0 RoutableNow:true SupportsMCP:true SupportsOAuth:true}]
2026/10/12 04:56:54 INFO health server listening ... addr=127.0.0.1:56000
2026/10/12 04:56:54 INFO mcp session initialized ... protocol_version=2026-07-28 server_name=mcp-stub server_version=0.1.0
2026/10/12 04:56:54 INFO 🌐 WEB UI: http://127.0.0.1:56000/ui ... health_url=http://127.0.0.1:56000
2026/10/12 04:56:54 INFO tunnel-client startup summary ... mcp_target_kind=http-streamable mcp_target_value=http://127.0.0.1:55999/mcp first_failing_dependency="" codex_detected=true codex_plugin_installed=false
2026/10/12 04:56:56 INFO tunnel metadata fetched ... name=GPT-Windows-MCP-Bridge description="Connect local Windows MCP services to ChatGPT and Codex."
2026/10/12 04:56:56 INFO 🟢 tunnel-client started ... tunnel_id=tunnel_6acbeee2ce888191b775cd53429c7597
~~~

**注**：API Key 输入在 PowerShell `Read-Host -AsSecureString` 下显示星号掩码；上传文本未包含实际秘密值。健康检查的本机浏览器截图显示 `http://127.0.0.1:56000/readyz` → `ready`（独立 UI 证据，非本文件推测），且没有修改代理。

## 2. 已出现的错误和后续真实校正

最初 ChatGPT 自定义 MCP 创建：连接方式 = 隧道；身份验证 = OAuth。点击「创建为插件」：
~~~text
无法发现 OAuth 设置。请检查服务器 URL，或手动输入设置。
~~~

Windows 在 04:56:54 时记录：
~~~text
WARN harpoon host auto-registration failed ... url=http://127.0.0.1:55999 ... base URL must use https
INFO harpoon enabled ... target_count=0 allow_plaintext_http=false
~~~

在 05:09:15–05:09:32 又记录：
~~~text
ERROR dispatcher received unsupported channel ... channel=harpoon
WARN failed to process polled command ... error="unsupported channel \"harpoon\""
~~~

**有用的差分结果**：
- `main` 仍 `RoutableNow:true`，且 MCP 会话初始化成功。
- ChatGPT 页面实际展开身份验证下拉：`OAuth`、`无需身份验证`、`OAuth 或无需身份验证`。选择了演示用途的 `无需身份验证`。
- 随后跳到「连接 GPT-Windows-MCP-Bridge」确认弹窗；用户点击连接并看到 **「已连接」**。
- 用户转交另一个真实 ChatGPT 页面验收报告：`echo` 输入 `hello from Windows`，实际返回 `{"echoed":"hello from Windows"}`，报告给出 `ECHO_REALITY_PASS`。**这是用户转交独立页测试，不是本会话重新执行工具的独立调用日志**。
- 由于 main demo 可用，先前声称“Harpoon target_count=0 导致所有 MCP 调用均不可用”不成立。Harpoon 错误只说明某些通道/授权发现请求失败，不足以否定 main demo 的远端工具调用。
- 因未接真实 Windows MCP，**不允许**从 echo PASS 推出 Windows 远端文件、命令、桌面操作 PASS。真实服务不得沿用无身份验证设置。

## 3. 真实能力与未完成边界

| 层级 | 证据 | 判定 |
|---|---|---|
| 完整 Windows CLI 的 quickstart | Windows 控制台原文 | PASS |
| Windows 本地 MCP-stub 启动 + initialize | 原始日志 | PASS |
| OpenAI 隧道元数据 + 客户端启动 | 原始日志 | PASS |
| 本地 health /readyz | 用户浏览器截图 `ready` | PASS |
| ChatGPT 自定义 MCP 创建和连接 | 用户实际页面「已连接」 | PASS_USER_UI |
| ChatGPT → Tunnel → Windows mcp-stub echo | 用户转交独立页面工具调用结果 | PASS_USER_RELAYED |
| Windows 本机 Desktop Commander 26 工具与只读、写后读、PowerShell | 原有 Actions run 38169533429 / 38169679396 | PASS_LOCAL_ONLY |
| ChatGPT → Tunnel → 真实 Desktop Commander 文件读写与 Windows Shell | **未进行** | NOT_TESTED |
| 开机重启后的官方 Tunnel 常驻恢复 | **未进行** | NOT_TESTED |
| 正式生产身份验证 + 最小权限 | **未实施** | NOT_TESTED |

**本次独立来源**：
- 原始用户贴出运行日志（386 行）及浏览器截图；
- 用户贴出独立页面验收文本：`真实调用成功 · PASS` / `{"echoed":"hello from Windows"}` / `ECHO_REALITY_PASS`；
- 既有本地开源 MCP Actions run：https://github.com/cuiqinggang/codex-private-skills/actions/runs/38169533429 和 https://github.com/cuiqinggang/codex-private-skills/actions/runs/38169679396 。

**结果冻结**：
~~~ini
TUNNEL_DEMO_CLI=PASS
TUNNEL_DEMO_READY=PASS
TUNNEL_DEMO_CHATGPT_CONNECTED=PASS_USER_UI
TUNNEL_DEMO_ECHO=PASS_USER_RELAYED_INDEPENDENT_PAGE_REPORT
CHATGPT_REMOTE_REAL_WINDOWS_TOOLS=NOT_TESTED
PRODUCTION_FINAL_VALID=NO
~~~

下一节点与完整恢复说明见 `../OPENAI_TUNNEL_CONNECT_RECOVERY_20261012.md`。

## 4. 追加证据：真实服务切换脚本预部署（不属于正式远端执行 PASS）

- 用户要求立即验收真实文件与命令能力后，使用已有双路桥通过 GitHub Runner 实际诊断：[read-only run 38176840327](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38176840327)，返回 `current_user=NT AUTHORITY\NETWORK SERVICE`，真实 Desktop Commander MCP 的 `index.js` 存在、完整版 OpenAI CLI 存在；交互式用户已有 Tunnel PID42156 Session11，`127.0.0.1:56000/readyz` HTTP200=`ready`。
- 工具端真实调用 `GPT-Windows-MCP-Bridge.server_info` 返回 `mcp-stub`，工具仅 `server_info/echo/uppercase`，仍是演示服务。
- Runner [staging run 38177110566](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38177110566)：Windows `C:\AI\GPT-Windows-Bridge-B\Launch-OpenAI-Real-MCP.ps1` 投放成功，SHA256=`7F9688C62AEA418D3FA3919C007473EC0EDA4B0A90EA5BB6CEB81AFB3BE9DD07`，未触碰 Key，原 demo 保留。脚本在用户会话中交互式启动尚未执行。
- ChatGPT 插件配置只读检查显示 App-specific `Allow all actions`。准备真实 Windows 全权限工具前应明确改为 `Always ask`，并保障鉴权、操作确认和风险隔离。文档不能替代用户真正完成这一步。
- `STAGED_PASS=YES`，`CHATGPT_REMOTE_WINDOWS_FILE_WRITE_AND_COMMAND=NOT_TESTED`，`FINAL_VALID=NO`。


## 5. 真实服务首次启动失败与 PATHFIX 现实部署（2026-10-12 05:54 后）

- 用户实际交互 Windows 命令：`powershell -NoProfile -NoExit -ExecutionPolicy Bypass -File "C:\AI\GPT-Windows-Bridge-B\Launch-OpenAI-Real-MCP.ps1" -Launch`；使用 A 用户，已输入真实密钥（以星号掩码，未泄露）。准确日志 `Stopping only confirmed demo tunnel process PID 42156`，`channel=main transport=stdio`，随后 `exec: "C:Program": executable file not found in %PATH%`，`TUNNEL_REAL_MCP_EXIT_1`。**失败位置在启动 MCP 子进程**，不代表真实 MCP tools/call 已执行。
- SOURCE FIX：`a9f78b62eff037f481087ed04ce984beb0f6a5c9` 以 `node.exe` + 正斜杠且无空格的路径取代出错的完整 Node 路径嵌套引号。
- Windows 重新部署事实：[run 38178400910](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38178400910)，`result.json status=PASS`；`REAL_TUNNEL_STAGE_PASS`；落盘 SHA256=`34A1EF6DFB8F0D41A56106384A738D7F0BDF5C7AD8BB152EE4195CB1B53070DE`。
- **未验收**：修复后用户会话重新输入 Key，`node.exe` 真实子进程通过官方隧道启动，ChatGPT 发现真实 26 工具，远端读/写/命令。保留 `FINAL_VALID=NO` 等待 Reality。
