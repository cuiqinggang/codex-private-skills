# OpenAI Tunnel → Windows Desktop Commander MCP｜远程真实验收 PASS

DATE=2026-10-12
TASK_ID=GPT-TUNNEL-WINDOWS-REAL-R1-20261012
SKILL=GPT直连Windows双路执行桥 v0.3.3
TUNNEL_ID=tunnel_6acbeee2ce888191b775cd53429c7597
PLUGIN=GPT-Windows-MCP-Bridge
CLIENT=openai-mcp
REMOTE_MCP=Desktop Commander MCP 0.2.52
REMOTE_HOST=DESKTOP-4A1EGTM
REMOTE_IDENTITY=desktop-4a1egtm\\a
EVIDENCE_ORIGIN=ChatGPT当前会话真实调用 mcp__GPT_Windows_MCP_Bridge__ 工具
RESULT=REAL_WINDOWS_REMOTE_FUNCTIONAL_PASS
SCOPE_FINAL_VALID=YES
REBOOT_PERSISTENCE=NOT_TESTED
PRODUCTION_ACCESS_REVIEW=OPEN

## 前提与故障演进

- 此前用户已通过 OpenAI 官方完整 `tunnel-client v0.0.16`，隧道 ID 如上，ChatGPT 自定义插件「隧道」连接，成功调用过官方演示 MCP `echo`。
- 2026-10-12 05:54 第一次切换真实 Desktop Commander 时，因 stdio 命令中 `C:\\Program Files\\nodejs\\node.exe` 的反斜杠/空格在 Go 命令解析器中变为 `C:Program`，启动失败：`exec: "C:Program": executable file not found in %PATH%`。
- 使用成熟最小修复：`node.exe C:/AI/GPT-Windows-Bridge-B/mcp/node_modules/@wonderwhy-er/desktop-commander/dist/index.js --no-onboarding`，不改变 FlClash/Windows 代理，未重建 Tunnel/插件/Key；Windows 上由现有 GitHub Runner 部署了修复版启动脚本。
- 用户在交互式 Windows A 会话重新启动，真实日志 `2026/10/12 06:02:45 INFO stdio MCP command started`，`2026/10/12 06:02:46 INFO 🟢 tunnel-client started`，当次动态管理 UI `http://127.0.0.1:63623/ui`。
- 原 ChatGPT 工具列表曾还保留 demo 的 `server_info/echo/uppercase`；实际调用 `server_info` 得到 `Unknown tool: server_info`。用户在插件设置完成工具刷新，并打开新的 ChatGPT 页面后，**本当前会话工具发现也实际出现 26 个 Desktop Commander MCP 工具**。

## 真实 ChatGPT → OpenAI Tunnel → Windows MCP 工具调用记录

以下每项是在 ChatGPT 页面真实调用 `mcp__GPT_Windows_MCP_Bridge__*` 获得的服务返回，并非模拟终端输出或仅本地 GitHub Runner 运行。

### 1. 工具目录更新｜PASS

经过插件刷新，实际可见包括 `list_directory, get_config, read_file, write_file, start_process, read_process_output` 等 Desktop Commander MCP 工具；不再是演示 `server_info/echo/uppercase`。本轮直接调用成功。

### 2. 目录真实读取｜PASS

实际工具：`mcp__GPT_Windows_MCP_Bridge__list_directory`
输入：`{"path":"C:\\AI\\GPT-Windows-Bridge-B\\evidence","depth":1}`
真实返回的文件名：

```text
[FILE] bridge-b-install-evidence.json
[FILE] bridge-b-local-functional.json
[FILE] b_mcp_write_read_probe.txt
[FILE] npm-install.log
```

实际 `get_config` 得到 `version=0.2.52`, `currentClient.name=openai-mcp`, `systemInfo.platform=win32` 和 Windows Node.js v24.14.0。该配置在本轮返回 `allowedDirectories=[]`；这**不证明目录被限制**。不要未经用户要求修改配置；后续安全评审应区分终端执行权限与文件 API 允许目录。

### 3. 远程写入并独立读回｜PASS

调用 `mcp__GPT_Windows_MCP_Bridge__write_file`：
- `path=C:\\AI\\GPT-Windows-Bridge-B\\evidence\\GPT_TUNNEL_REAL_REMOTE_R1_20261012.txt`
- `mode=rewrite`
- `content`：

```ini
TASK_ID=GPT-TUNNEL-WINDOWS-REAL-R1-20261012
SOURCE=ChatGPT-custom-MCP-via-OpenAI-Tunnel
MARKER=REAL_WINDOWS_REMOTE_FILE_WRITE_READ_PASS
EXPECTED=2026-10-12
```

真实返回：`Successfully wrote to C:\\AI\\GPT-Windows-Bridge-B\\evidence\\GPT_TUNNEL_REAL_REMOTE_R1_20261012.txt (5 lines)`。

随后单独调用 `mcp__GPT_Windows_MCP_Bridge__read_file`，真实输出 `[Reading 4 lines from start (total: 4 lines, 0 remaining)]` 且读取到全部四个字段，`MARKER=REAL_WINDOWS_REMOTE_FILE_WRITE_READ_PASS` 与预期严格一致。写入工具返回中标的五行与读回四个非空行是尾部换行统计差异，不是数据错乱。

### 4. PowerShell 真实命令执行及进程退出｜PASS

调用 `mcp__GPT_Windows_MCP_Bridge__start_process`：

```json
{"command":"powershell -NoProfile -NonInteractive -Command \"Write-Output GPT_TUNNEL_REAL_WINDOWS_SHELL_PASS; whoami\"","timeout_ms":10000}
```

真实返回：

```text
Process started with PID 29708 (shell: powershell.exe)
Initial output:
GPT_TUNNEL_REAL_WINDOWS_SHELL_PASS
desktop-4a1egtm\\a
```

继续实际调用 `mcp__GPT_Windows_MCP_Bridge__read_process_output`（`pid=29708, timeout_ms=4000`）取得：

```text
GPT_TUNNEL_REAL_WINDOWS_SHELL_PASS
desktop-4a1egtm\\a
✅ Process completed with exit code 0 (runtime: 1.42s)
```

因此这里不仅证实了 PowerShell 启动和 stdout，还**独立回读证实退出码 0**。命令仅 `Write-Output` 与 `whoami`，没有系统配置副作用。

## 严格验收状态

| 项目 | 判定 |
| --- | --- |
| tunnel-client 正式服务及 stdio MCP 子进程成功启动 | PASS |
| ChatGPT 刷新、发现真实 26 个 MCP 工具 | PASS |
| ChatGPT → 远程 Windows 目录工具 `list_directory` | PASS |
| ChatGPT → 远程 Windows 文件 `write_file` | PASS |
| ChatGPT → 远程 Windows 文件 `read_file` 内容一致 | PASS |
| ChatGPT → 远程 PowerShell `start_process` | PASS |
| 远程 PowerShell `read_process_output` 退出码 0 | PASS |
| Windows 重启/注销后常驻及自动恢复 | NOT_TESTED |
| 多任务并发、跨日保持、业务破坏性命令 | NOT_TESTED（不是本次目标） |

`FINAL_VALID=YES` **仅限用户本次要求的「真实 Windows 文件读写与命令执行」端到端最小闭环**。不代表开机自启动、生产多并发、全部 26 个工具或安全隔离已经验收。

## 不改变的设置与后续建议

- 用户明确同意保留 ChatGPT 插件的 `Allow all actions` 与 MCP「无需身份验证」；本次没有修改两个设置，没有修改 FlClash、Windows 代理或原有 DCR、GitHub Runner 路由。
- 生产风险：没有每次操作确认的远端 Shell 具备很高权限，且本轮 `allowedDirectories=[]`，不能当作已启用文件目录白名单。隧道仍依赖 Platform Runtime API Key、隧道访问权限与 ChatGPT 工作区绑定，应检查访问边界；如未来需要在多人工作区共享，应单独决定是否设置服务端身份验证/最小权限。
- 当前服务以前台 Windows PowerShell 进程运行；关闭窗口将结束隧道。自动启动/自愈未验收，因此不要将其写成常驻服务 PASS。
- 以后直接复用本次的成功命令、路径和技能包，不要重跑 demo echo，不要重建现有 Tunnel，不要切换代理。
