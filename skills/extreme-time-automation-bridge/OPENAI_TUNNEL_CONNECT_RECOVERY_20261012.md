# OpenAI Secure MCP Tunnel → ChatGPT 插件 → Windows｜全流程与故障恢复（2026-10-12）

> **所属正式技能包**：GPT直连Windows双路执行桥 v0.3.3（文档增强）。  
> **性质**：2026-10-12 用户实际操作的原样复盘 + 可复用最短恢复手册；不是第三条正式 Windows 生产执行路由的认证。  
> **权威地址**：私有仓库 \`cuiqinggang/codex-private-skills\`，\`main\`，本文件；原双路与安全边界见同目录 \`SKILL.md\`、\`DUAL_ROUTE.md\`、\`DCR_RECOVERY.md\`。  
> **冻结定位**：\`OPENAI-TUNNEL-DEMO-20261012\`；客户端 \`v0.0.16\`；隧道 \`tunnel_6acbeee2ce888191b775cd53429c7597\`；插件名 \`GPT-Windows-MCP-Bridge\`。  
> **终局**：本地 CLI、客户端就绪、ChatGPT 插件注册与 demo echo 调用 **PASS（echo 为用户转交独立页面的真实工具调用报告）**；**ChatGPT 经该隧道调用真实 Windows 文件/命令执行器 = NOT_TESTED；PRODUCTION_FINAL_VALID=NO**。

## 0. 总目标、历史系统保护、证据级别

目标是把 ChatGPT 发出的任务通过 OpenAI 官方出站隧道传到 Windows 本地 MCP；后续再将「官方演示 MCP」换成已装好的开源 Desktop Commander MCP。**不要把演示工具的成功误写成 Windows 远端命令执行通过。**

既有正式双路严格保留：
- A 主路：ChatGPT → Desktop Commander Remote（托管）→ Windows。2026-10-12 本页面曾真实 \`list_devices\` 显示 \`DESKTOP-4A1EGTM\` 新设备 \`f6990966-5870-484b-bf79-409bc6fb963e\` Online，\`ping\` PASS；随后的 \`start_process\` 遭到托管方本月调用额度上限拦截（不是电脑离线）。此状态有时效性。
- B 备路：ChatGPT/GitHub → Actions → Windows self-hosted runner（\`DESKTOP-4A1EGTM-etal\`），见原技能包已验证的任务证据。
- 开源 B 隔离实验：\`skills/windows-open-source-bridge-b/README.md\`，本地 Desktop Commander MCP 0.2.52 共发现 26 工具，已在 Windows 本机验证目录读取、PowerShell、隔离目录写后读；与本次 demo 隧道 **尚未组合完成真实 Windows 远程测试**。
- 新增官方 Tunnel 是未来可能的直连实现；本次仅证实“隧道+演示MCP+ChatGPT插件”完整链路，**不替换** A/B 已有生产路径。

证据等级：
1. \`CLI_REALITY=PASS\`：用户贴出的 PowerShell 真实运行日志，包含启动、MCP 初始化、隧道元数据；
2. \`READY_REALITY=PASS\`：浏览器截图 \`http://127.0.0.1:56000/readyz\` 返回 \`ready\`；
3. \`CHATGPT_PLUGIN_CONNECTED=PASS_USER_UI\`：用户亲眼确认网页出现「已连接」；
4. \`ECHO_REALITY_PASS=USER_RELAYED_INDEPENDENT_PAGE_REPORT\`：用户转交新 ChatGPT 页的 \`echo\` 工具真实输出报告；本页面没有独立捕获该次工具调用日志，禁止把“用户转交”写成“本页面亲自调用”；
5. \`WINDOWS_REMOTE_READ_WRITE_SHELL=NOT_TESTED\`：演示 server 是 mcp-stub，不是 Desktop Commander 26 工具。

证据见 \`evidence/OPENAI_TUNNEL_DEMO_REALITY_20261012.md\`。**任何 API Key、Token、凭据、OAuth secret 严禁写入本仓库、聊天、截图、命令参数/日志。**

## 1. 组件/文件/URL 选择：曾选错的选项完整保留

| 项 | 这次正确选择或实际观察 | 错误/误区 |
|---|---|---|
| 官方隧道管理 | https://platform.openai.com/settings/organization/tunnels | 只出现“创建隧道”指令页、未在列表看到记录时，不能声称创建成功 |
| 创建出的隧道 | \`GPT-Windows-MCP-Bridge\` / \`tunnel_6acbeee2ce888191b775cd53429c7597\` | \`tunnel_\` 后 32 位，不是尾部截断片段；ID 不是密钥 |
| 创建页底部工作区 | 这次用户反馈：**不要额外点击底部“GPT 工作区”选项**，按实际可用默认工作区完成创建 | 这是**本次 UI 的真实恢复经验**，不能推广为绕过工作区授权；最终以列表出现 ID 为准 |
| Windows 安装包 | **\`tunnel-client-v0.0.16-windows-amd64.zip\`**，截图约 26.8 MB | 别下载成 \`tunnel-client-runtime-v0.0.16-windows-amd64.zip\`（截图约 7.2 MB）；后者是精简 runtime，缺少所需完整管理命令；别选 Linux、arm64、spdx、licenses、源码 |
| 正确解压程序 | \`tunnel-client.exe\` + \`cloudflared.exe\` 等 | \`tunnel-client-runtime.exe\` 不能替代完整 CLI；\`cloudflared.exe\` 也不是本次手工要启动的主程序 |
| 本次解压位置 | Windows 用户桌面 \`tunnel-client-v0.0.16-windows-amd64\` 文件夹 | 不要因资源管理器路径/下载位置变化而假设 EXE 位于系统 PATH |
| OpenAI API 密钥入口 | https://platform.openai.com/settings/organization/api-keys | 不是「管理员密钥」；运行时用 \`CONTROL_PLANE_API_KEY\`，不要把管理员密钥放入常驻守护进程 |
| 密钥新建时 UI | 所有者「你」，名称 \`GPT-Windows-Tunnel-Runtime\`；「默认项目」曾长时间显示「正在加载项目…」；用户在项目可用后生成密钥 | 项目加载中不等于密钥创建成功；这次截图曾选择「全部权限」「永不过期」，安全上应后续轮换为最小权限，不能把高权限密钥提交仓库 |
| 官方 Runtime Key 权限 | 账号/运行者需要隧道 \`Tunnels Read + Use\`；键值只输入本机 | **ID、API Key、OAuth 授权三者不同**；不需要用 \`OPENAI_ADMIN_KEY\` 启动 |
| ChatGPT 设置页面 | https://chatgpt.com/plugins → 添加自定义 MCP 服务器 | 原先走 \`设置 → 插件\` 管理列表，无法在该页直接找到创建入口；网页 UI 版本变化时据当前显示操作 |
| 连接方式 | **隧道**，填写上述 \`tunnel_\` ID | 不选服务器 URL，不粘 \`127.0.0.1\`，不把密钥填进名称/描述 |
| 身份验证 | 本次 **演示** MCP 最终选择「无需身份验证」并成功连上 | 初始 OAuth 下报「无法发现 OAuth 设置」，有 Harpoon 错误；**无身份验证仅限无敏感能力的 demo，不允许照搬到真实 Windows 读写/Shell 服务** |
| 同意与激活 | 勾选 MCP 风险确认 →「创建为插件」→「连接 GPT-Windows-MCP-Bridge」→ 页面「已连接」 | 创建按钮可点 ≠ 已连接；已连接 ≠ 已完成真实 tools/call |
| 独立工具测试 | 新 ChatGPT 页面调用 \`echo("hello from Windows")\` 返回 \`{"echoed":"hello from Windows"}\` | 不能把文本模拟回显当成工具调用，也不能由 echo 推断系统文件/命令能力 |

截图中的工作区、项目选择仅是用户 2026-10-12 对当时 UI 的实际记录；未来 API/平台界面变动，应优先读官方 \`tunnel-client help quickstart\` 和当前 UI，**不绕过平台权限**。

## 2. 从零安装成功流程（可逐步重放；已有隧道时跳过建隧道）

### 2.1 创建并验证隧道

1. 打开上面的 OpenAI Platform \`Tunnels\` 页面。最初页面中央显示“目前还没有隧道”时表示列表确实为空，不是“安装了客户端就创建了”。
2. 点击右上角 **创建隧道**。名称填 \`GPT-Windows-MCP-Bridge\`，描述填 \`Connect local Windows MCP services to ChatGPT and Codex.\`。
3. 这次第一次选择/点击了页面最下面的 GPT 工作区项后，用户返回列表仍见“目前还没有隧道”；第二次**未额外点击该项**创建成功。以真实列表有新记录为准，不依据生成了一长段命令即判成功。
4. 保存完整隧道 ID（本次 \`tunnel_6acbeee2ce888191b775cd53429c7597\`），**如果列表里已有这个 ID，不重复创建**。ID 用于客户端和 ChatGPT 双侧绑定，本身不代替 API Key。

### 2.2 下载与 CLI 核验

1. 官方发布页 https://github.com/openai/tunnel-client/releases/tag/v0.0.16 → 下载 \`tunnel-client-v0.0.16-windows-amd64.zip\` **完整客户端** → Windows 「全部解压缩」到用户桌面。压缩包内有 \`tunnel-client.exe\` 与 \`cloudflared.exe\`。旧 runtime ZIP 可保留，但不拿它做本次配置。
2. Win+R，粘贴下面单行；或者在解压目录地址栏输入 \`powershell\` 打开终端后运行 \`.\tunnel-client.exe help quickstart\`：

~~~powershell
powershell -NoExit -Command "& (Join-Path ([Environment]::GetFolderPath('Desktop')) 'tunnel-client-v0.0.16-windows-amd64\tunnel-client.exe') help quickstart"
~~~

3. 实测输出标题 \`Quickstart:\`；其内容明确给出 \`CONTROL_PLANE_TUNNEL_ID\`、\`CONTROL_PLANE_API_KEY\`、\`doctor\`、\`run\`、\`runtimes connect\` 等规则。**本机 CLI 运行 PASS，并不等于隧道已连接**。

### 2.3 API Runtime Key：生成与边界

1. OpenAI Platform \`API 密钥 → 创建新的密钥\`；UI 名称 \`GPT-Windows-Tunnel-Runtime\`，所有者曾选「你」，项目选择为「默认项目」；如果始终显示 \`正在加载项目...\`，先刷新确认项目可用。
2. 完成正式密钥创建后，密钥通常只能在当时看见完整值；安全保存于 Windows 本机。**不要复制给 GPT**。
3. **本次已发生的风险**：截图显示「永不过期」和「全部权限」曾处于选择状态；实际所生成密钥权限应回 Platform 核验。稳定部署应轮换成 \`Tunnels Read + Use\` 的受限制密钥，按合适有效期/定期轮换，撤销旧高权限密钥。测试暂时可沿用已颁发 Key，避免反复创建。
4. 运行时的 \`CONTROL_PLANE_API_KEY\` 是 Windows → OpenAI 控制平面的认证；ChatGPT 创建插件的 OAuth/无身份验证是另一层设置。**ChatGPT 端不选 OAuth 不代表 Windows 端无 Key**。

### 2.4 本次真正成功的 PowerShell 启动命令（官方内置演示 MCP）

在**新 PowerShell 窗口**执行以下已由用户实测的命令；使用 \`Read-Host -AsSecureString\`，密码输入不显示。此运行方式是**前台 demo 会话**；关闭 PowerShell/电脑或 \`Ctrl+C\` 后不会自动保持连接。不要将 Key 写在命令行、ps1、GitHub、聊天中。

~~~powershell
$exe = Join-Path ([Environment]::GetFolderPath('Desktop')) 'tunnel-client-v0.0.16-windows-amd64\tunnel-client.exe'
$key = Read-Host "请粘贴刚创建的API密钥" -AsSecureString
$ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($key)
try {
    $env:CONTROL_PLANE_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr)
} finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr)
}
try {
    & $exe run --embedded-mcp-stub --control-plane.tunnel-id tunnel_6acbeee2ce888191b775cd53429c7597 --health.listen-addr 127.0.0.1:0
} finally {
    Remove-Item Env:\CONTROL_PLANE_API_KEY -ErrorAction SilentlyContinue
}
~~~

补充：SecureString 在上例中为启动原生 EXE 被暂时转换为进程环境变量，**并非持久凭据库**；终端保持运行期间变量可能被具备足够权限的本机主体读取。生产必须使用合适本机凭据存储、最小权限与轮换；不把这段 demo 脚本等同于完整安全部署。默认环境 \`HTTPS_PROXY\` 若已配置，客户端可继承；本次日志显示 \`env:HTTPS_PROXY → http://127.0.0.1:7890\`，**没有修改 FlClash 或 Windows 代理**。

### 2.5 实际端口、健康检查和启动证据

本次运行（2026-10-12 04:56:54–04:56:56）的真实日志：
- \`Embedded MCP stub enabled\`；MCP URL：\`http://127.0.0.1:55999/mcp\`；这是演示 MCP/OAuth 本地监听，**不是填入 ChatGPT「服务器 URL」的公网地址**。
- \`mcp session initialized\`，\`server_name=mcp-stub\`，\`protocol_version=2026-07-28\`。
- \`health server listening addr=127.0.0.1:56000\`；\`WEB UI http://127.0.0.1:56000/ui\`；\`readyz http://127.0.0.1:56000/readyz\`。
- \`tunnel metadata fetched name=GPT-Windows-MCP-Bridge\`；\`🟢 tunnel-client started\`；\`tunnel_url=https://api.openai.com/v1/tunnel/tunnel_6acbeee2ce888191b775cd53429c7597\`。
- 原截图浏览器 \`http://127.0.0.1:56000/readyz\` 页面仅显示文字 \`ready\` → **本地就绪 PASS**。
- **端口 55999/56000 是本次动态分配结果**，因为启动参数 \`--health.listen-addr 127.0.0.1:0\`；重启后必须查新日志中的真实端口，不能固化成永久固定端口。

如果同一实例还在运行，可以用新浏览器标签页访问 \`http://127.0.0.1:56000/ui\` 观测，但 UI 显示不能替代 \`readyz\` 与远端真实工具调用。

### 2.6 ChatGPT 注册与两个明确不同的认证选项

1. 打开 https://chatgpt.com/plugins （非「设置→插件」已装插件清单），选「添加自定义 MCP 服务器」。
2. 实际输入：
   - **名称**：\`GPT-Windows-MCP-Bridge\`（普通显示名称，**不是密码**）。
   - **描述**：\`连接 Windows 本地 MCP 服务，用于文件管理、命令执行和自动化任务。\`。注：这是原表单填写的愿景描述，当前连接到的仍是 demo。
   - **连接**：点右侧 **隧道**（非「服务器 URL」），粘贴 \`tunnel_6acbeee2ce888191b775cd53429c7597\`。
   - **身份验证**：第一次保留 OAuth，点击「创建为插件」提示 **\`无法发现 OAuth 设置。请检查服务器 URL，或手动输入设置\`**。此时 **不要假设 Tunnel ID 错误，也不要使用管理 Key 来充当 OAuth**。
   - **仅为了演示 stub 的排障**：在「身份验证」下拉列表选择 **无需身份验证**（另有 \`OAuth\` / \`OAuth 或无需身份验证\`），保留其余字段和安全风险勾选，重新「创建为插件」。
3. 改为 demo 无身份验证后，出现「连接 GPT-Windows-MCP-Bridge」的确认弹窗，点击黑色连接按钮，随后用户在网页看到「已连接」。
4. 新开 ChatGPT 页面（令可用工具列表刷新），**通过插件真实执行** \`echo("hello from Windows")\`。用户转交新页执行报告，工具返回：
   ~~~json
   {"echoed":"hello from Windows"}
   ~~~
   报告 \`ECHO_REALITY_PASS\`；此结果来自用户独立页回传，不是本页直接工具调用。
5. 安全提醒：一旦换成有读写、PowerShell、桌面控制的真实 Windows MCP，**必须重新审查身份验证、工作区访问权限、审批、允许目录和危险命令限制**；不要把“无身份验证 demo”直接升级生产或将本地服务公网裸露。

## 3. 关键报错的正确归因：不要因局部警告重建系统

**已观察的日志真实关键字段**：
- \`dispatcher channels registered [{Name:harpoon ... RoutableNow:false ...} {Name:main ... RoutableNow:true SupportsMCP:true SupportsOAuth:true}]\`
- \`harpoon enabled target_count=0 allow_plaintext_http=false\`
- 多条 \`WARN harpoon host auto-registration failed ... base URL must use https\`，目标 URL 是 \`http://127.0.0.1:55999\`；
- 当 ChatGPT 尝试 OAuth/发现时出现 \`ERROR dispatcher received unsupported channel ... channel=harpoon\`，\`failed to process polled command\`；
- **但后续切换为 demo「无需身份验证」后，ChatGPT 端成功连接并实际 echo 回显。**

因此，\`harpoon\` 警告/失败**不等同于** \`main\` MCP 通道失败，更不能仅凭警告认定需要关闭 HTTPS 校验或换代理。已证实的有效路径是：**针对无敏感能力演示 stub 在 ChatGPT 侧选择无身份验证**。此前把所有失败归因于 Harpoon 无目标、认为不修 Harpoon 就完全无法连通，是过度推断，已经由后续 echo 结果纠正。

\`codex_detected=true\` 同时 \`codex_plugin_installed=false\` 是 Codex 插件**可选**状态，不影响本次 ChatGPT demo echo 连接。需要 Codex 客户端接入时另行运行并验收 \`tunnel-client codex plugin install\`，不要与 ChatGPT 自定义 MCP 插件混淆。

## 4. 故障树：以后坏了按现象精准恢复（不准盲目重建）

| 现象 | 优先检查 / 正确动作 | 禁止误判或副作用 |
|---|---|---|
| Platform 隧道列表仍显示「目前还没有隧道」 | 重新核对当前组织与实际 Tunnels 列表；确认创建动作完成且有完整 \`tunnel_\` ID；本次底部工作区选择曾引起困惑 | 不要凭出现命令/长文本认定创建成功；已有 ID 不重建 |
| ID 只有 \`ee2...\` 尾部 | 用上次创建记录的完整 \`tunnel_6acbeee2ce888191b775cd53429c7597\` | 不能把截断 ID 当 API Key |
| 只看到 \`tunnel-client-runtime.exe\` | 找完整 \`tunnel-client-v0.0.16-windows-amd64.zip\` 并解压；运行 \`tunnel-client.exe help quickstart\` | 不拿 runtime/arm64/linux/许可证/JSON 当正式管理客户端 |
| PowerShell 报找不到 exe | \`Test-Path (Join-Path ([Environment]::GetFolderPath('Desktop')) 'tunnel-client-v0.0.16-windows-amd64\tunnel-client.exe')\`；校对桌面 OneDrive 重定向及实际解压目录 | 不改 PATH 或重装系统作为首选 |
| \`Quickstart\` 正常但 /readyz 不开 | 检查原 \`run\` 前台窗口是否仍在；找最新 \`health server listening\` 地址；确认进程/日志有无退出 | 文档中的 \`56000\` 是本次临时端口，不能永久硬编码 |
| \`readyz=ready\` 但 ChatGPT 未见插件 | 去 https://chatgpt.com/plugins 的创建/连接流程核验，确认前台 runtime 仍运行且账户/工作区匹配 | 健康 PASS 不等于 ChatGPT 插件已注册 |
| 密钥/控制平面报 401/403 | 核实 Runtime API key 有效、项目、用户/工作区、Tunnels Read+Use、密钥是否过期或已撤销；安全本机重新输入 | 不乱用 admin key、不贴密钥到聊天/仓库，不靠改代理绕授权 |
| OAuth 发现失败 | 区分本次 **demo stub** 可选无身份验证；正式服务器应配置合规 OAuth/授权元数据后再注册 | 不对真实命令执行器关闭身份验证；不造假的 OAuth 地址 |
| \`unsupported channel "harpoon"\` / HTTPS 目标警告 | 查 \`main RoutableNow\`、\`mcp session initialized\`、远端实际 tools/call；按 OAuth 与 main 两条链分别查 | 不把 Harpoon 一处警告判整条隧道失败；不建议用 \`--harpoon.allow-plaintext-http\` 作为默认“修复” |
| \`codex_plugin_installed=false\` | ChatGPT 插件测试无需处理；只有独立 Codex 集成需求才安装 Codex 插件 | 不把缺 Codex 插件误判为 ChatGPT 接不通 |
| 已连接但只有 \`echo\`、\`uppercase\` | 本来启动的是 \`--embedded-mcp-stub\`，应在**单独生产验收节点**接真实 Desktop Commander MCP | 不能用演示 echo 声称 Windows 文件/命令/桌面已打通 |
| 重新开机后不可用 | 本次 \`run\` 为前台模式；用户登录后需重启；未来用官方 \`runtimes connect\` 管理并检查 \`runtimes status <alias> --json\`，但**本次未实施自动常驻** | 不把「这次 Ready」升级为「开机常驻 PASS」 |
| DCR 托管调用提示本月额度耗尽 | 原托管 Remote 配额与本地开源 MCP/官方 Tunnel 是不同层；可继续使用已验证 GitHub runner，等待托管额度恢复 | 不重复配对/改设备配置来“解决”账期限制 |
| FlClash/代理故障疑似 | 本次 \`HTTPS_PROXY\` 使用 \`127.0.0.1:7890\`，先对照环境变量/已知 GOOD 日志做只读诊断 | **严格禁止修改 FlClash、系统代理、打开虚拟网卡、再启动另一个浏览器** |

### 最短无副作用只读诊断（Windows PowerShell）

以下查询不会重新提交隧道创建、不会重发业务命令：
~~~powershell
$exe = Join-Path ([Environment]::GetFolderPath('Desktop')) 'tunnel-client-v0.0.16-windows-amd64\tunnel-client.exe'
Test-Path $exe
Get-Process tunnel-client -ErrorAction SilentlyContinue | Select-Object Name,Id,StartTime
# 如果仍是本次未重启的进程且日志端口为 56000，可查：
Invoke-WebRequest 'http://127.0.0.1:56000/readyz' -UseBasicParsing
~~~
本次截图 \`ready\` 已通过；重启后的端口必须重新从控制台日志或本地 UI 配置确定。如果服务已运行，**不要再启动第二个同隧道的前台客户端与旧实例抢会话**。

## 5. 正式 Windows MCP 接入下一节点：不能用 demo 偷换验收

已在仓库另一独立目录保存成熟的本地开源 Desktop Commander MCP 环境，位置 \`C:\AI\GPT-Windows-Bridge-B\`，由 GitHub Actions 的 Windows Runner 安装并真实本地调用过。**此次 ChatGPT 直接连接的却是官方内置 \`mcp-stub\`**。

后续建议的**候选路线（NOT_YET_EXECUTED）**：
1. 保留当前已验证 demo 的记录和 Key/Tunnel ID，明确新执行窗口的授权范围；先确认本地真实 MCP 26 工具如何由 \`stdio\` 启动及 Windows 会话身份（不可直接假定 Runner 服务用户等于桌面 A 用户）。
2. 不与 demo 前台运行抢同一隧道：按现场状态安全停止 demo（必要时在其窗口 \`Ctrl+C\`），再用官方支持的初始化模板 \`tunnel-client init --sample sample_mcp_stdio_local --profile <已批准名称> --tunnel-id <已有ID> --mcp-command <核验过的本机启动命令>\` 或官方 HTTP 模板对接真实 MCP；先 \`doctor --profile ... --explain\`，再 \`run --profile ...\`。这里的占位符不得无核验直接复制执行。
3. 启用真实 Windows 服务前审查 ChatGPT 平台账户的自定义 MCP 读写权限、用户/目录授权、交互确认、OAuth/访问控制；**禁止直接沿用「无需身份验证」生产暴露命令执行器**。
4. 验收分层：\`remote tools/list\` 看见真实工具 → 实际远端只读目录工具回读 → 隔离目录写后读（明确授权）→ 无副作用 PowerShell 标记输出 → 重连/恢复 → 权限边界、并发与 Exactly-once。每层保留工具原始回执、调用时间与所属独立会话；失败时先恢复，不能覆盖此前已通过的 GOOD 基线。
5. 真实 ChatGPT 远程调用文件与 Windows Shell **都 PASS** 后，才能另行升级正式业务通路或声明 \`PRODUCTION_FINAL_VALID=YES\`；否则保留原 A/B 路由保障生产任务。

## 6. 一页恢复快照（给明天/新 CEO 页面）

~~~ini
SKILL=GPT直连Windows双路执行桥
VERSION=0.3.3
REPO=cuiqinggang/codex-private-skills
REF=main
SKILL_PATH=skills/extreme-time-automation-bridge/
DOC=OPENAI_TUNNEL_CONNECT_RECOVERY_20261012.md
TUNNEL_ID=tunnel_6acbeee2ce888191b775cd53429c7597
TUNNEL_NAME=GPT-Windows-MCP-Bridge
CLIENT=OpenAI tunnel-client v0.0.16 (full windows-amd64; not runtime)
EXE=<Windows用户桌面>\tunnel-client-v0.0.16-windows-amd64\tunnel-client.exe
KEY_NAME=GPT-Windows-Tunnel-Runtime
KEY_VALUE=NEVER_STORE_IN_REPO
DEMO_MCP=http://127.0.0.1:55999/mcp  # 仅本次运行
DEMO_HEALTH=http://127.0.0.1:56000/readyz  # 动态端口,重启后查日志
DEMO_READY=PASS
CHATGPT_PLUGIN_CREATED=PASS_USER_UI
CHATGPT_PLUGIN_CONNECTED=PASS_USER_UI
CHATGPT_PLUGIN_AUTH_FOR_DEMO=NONE
DEMO_ECHO=PASS_USER_RELAYED_INDEPENDENT_PAGE_REPORT
DEMO_ECHO_OUTPUT={"echoed":"hello from Windows"}
WINDOWS_REMOTE_REAL_TOOLS=NOT_TESTED
PRODUCTION_FINAL_VALID=NO
CODEx_PLUGIN=NOT_INSTALLED_AS_OF_20261012_LOG
DCR_AND_GITHUB_RUNNER=KEEP_UNCHANGED
DO_NOT_CHANGE=FlClash,WindowsProxy,ExistingBrowsers,OriginalAutostart
NEXT=替换 demo 为经授权的真实 Desktop Commander MCP、最小权限与实际远端工具验收
~~~

最后要明确：**本文件是故障恢复的可回读方法资产，文档写入 PASS 不等于候选正式连接部署 PASS**。