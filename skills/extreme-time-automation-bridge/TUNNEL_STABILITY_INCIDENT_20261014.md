# GPT直连Windows双路执行桥 V1.0.1｜2026-10-14 断线分层取证与健康补丁

STATUS=PARTIAL_STABILITY_REPAIR;NOT_FINAL_STABILITY_ACCEPTED
DATE=2026-10-14
EVIDENCE_SCOPE=WINDOWS_REALITY_AND_GITHUB_SKILL
SKILL_PATH=skills/extreme-time-automation-bridge/
TUNNEL_ID=tunnel_6acbeee2ce888191b775cd53429c7597
RUNTIME=tunnel-client v0.0.16; Desktop Commander MCP 0.2.52
ORIGINAL_TUNNEL_AND_PROXY=UNCHANGED
UNATTENDED_RECOVERY=NOT_IMPLEMENTED
REBOOT_STABILITY=NOT_TESTED

## 1. 已知历史与本次故障，必须分层
- 2026-10-12：`Session terminated` 之后，Runner 查到目标 tunnel-client 进程=0，原父 PowerShell 已退出；原恢复只做进程存在判断，不能证明会话健康。
- 2026-10-14 20:43（Windows UTC+8）：远程直连查询发现唯一 tunnel-client 进程，实际文件读取和 PowerShell 曾成功。
- 2026-10-14 20:35–20:47：Windows PowerShell 400/403 记录显示多次执行原 `Restore-Interactive.ps1`；它过去按 Tunnel ID 命令行筛进程，存在时仅打印“already running”并退出。事件日志没有记录旧隧道准确的退出原因。
- 2026-10-14 21:47：本机真实快照 `TOTAL_TUNNEL_PROCESSES=0`，原启动脚本可读。**“进程退出”是真实证据；“是谁关闭/异常崩溃”仍 UNKNOWN**。
- 2026-10-14 21:50：用户在原 Windows 会话本机手动输入 Runtime API Key，复用已有 `Launch-OpenAI-Real-MCP.ps1 -Launch` 启动原 Tunnel ID；`stdio MCP command started`、`tunnel-client started` 出现在实际日志中。
- 2026-10-14 21:53：ChatGPT 从自建 Windows MCP 真实读取启动脚本前12行 PASS；隧道唯一进程 PID 38324、/healthz=200、/readyz=200。
- 21:58 健康快照：control-plane polling，无轮询失败；MCP initialized，子进程运行，dispatcher无业务失败，proxy healthy。
- **本轮新复现：** 在一次编排会话中连续发出若干 `write_file`，首段成功，后段再次返回 `409 mcp_initialization_required`；隔离新调用的健康查询仍看到相同隧道PID及相同 MCP `child_generation=eda367644b637e0a296f2c6cab2ae1c3`，且 initialization_epoch 从5上升到22。**这支持“初始化/调用状态异常”与“整进程退出”是两类事故；不证明具体客户端竞态根因。**
- 已检查 Windows Application 错误、System重启/关机及相关日志；未取得可信的旧进程终止行为归因，不写假根因。

## 2. 根因分级 / First Delta
**CONFIRMED-1 结构性风险：** 正式启动脚本采用前台 `tunnel-client run` + 当前 PowerShell + 人工输入 Key。历史有父 PowerShell 离开/目标进程0记录，没有已验收的专用自动重启或登录恢复。只要进程退出就断开 ChatGPT。
**CONFIRMED-2 恢复判路缺口：** 原 `Restore-Interactive.ps1` 仅按 `CommandLine` 中 Tunnel ID 判定进程存在；若权限较低导致 `CommandLine` 不可读，可能漏认已经运行的进程并准备启动第二份。且存在时不查健康。
**CONFIRMED-3 运行期协议错误：** 出现过409（未初始化）及此前502、Session terminated；此次409之后原隧道/子进程仍在线，因此不得把所有409都解释成主进程崩溃。
**UNKNOWN：** 10月14日旧实例准确退出触发事件；409 是服务端客户端哪一层握手竞态；完整端到端 P95 / 连续72h稳定率。

## 3. 现实中已部署的最小补丁
- 新增 `C:\AI\GPT-Windows-Bridge-B\persistence\Watch-Tunnel-Health.ps1`（仓库镜像 `bootstrap/Watch-Tunnel-Health.ps1`），可手工无副作用运行；`-Persist` 时仅追加脱敏 JSONL。
- 新增 Windows 计划任务 `GPT-Windows-Tunnel-HealthLog`，以普通用户 A、有限权限，每5分钟执行一次只读检查，忽略重入，执行时间上限1分钟。日志为 `C:\AI\GPT-Windows-Bridge-B\persistence\Tunnel-Health.jsonl`（达到512KiB后最多保留上次轮转文件），不保存 API Key，不重启进程、不更改任何代理。
- 交互调用已实测 `HEALTHY`，定时任务因 Windows 低权限读不到原进程 CommandLine/ExecutablePath，最新结果为 `HEALTHY_PATH_ONLY`（进程及健康组件正常，但未独立核实 Tunnel ID）。**不能把这个状态写成全身份认证**；此前的 `PROCESS_AMBIGUOUS` 为最初监控器权限误判，已调整为保守身份分级。
- 原恢复脚本先备份到 `Restore-Interactive.ps1.backup-20261014`，SHA256=`27B47071686B602F2EFDBF8C6C01F06B2E91CE4A4FD93DB0B3C64161E0CD4738`。
- 现有 `Restore-Interactive.ps1` 已改为：只要发现 ANY tunnel-client 进程就不直接启动，先调用本地健康脚本；有多个进程、身份不能确认或健康异常时提示并拒绝重复实例；只有进程总数为0才调用原人工输入密钥启动器。与仓库 `bootstrap/Restore-Interactive-Safe.ps1` 对应。
- 恢复脚本语法检查0错误；在当前隧道在线时单次现实试跑 `HEALTHY`、退出码0、前后隧道数1、PID不变。**未触发离线分支以避免破坏当前会话**。

## 4. 后续成熟路径（不能用监控替代恢复）
- 官方成熟候选：`tunnel-client runtimes connect` 管理长时运行，`runtimes status --json` 回读状态。当前 v0.0.16 本地 `--help` 实测具备此入口。官方参考 https://github.com/openai/tunnel-client/blob/master/docs/onboarding.md 和 plugins/tunnel-mcp/README.md 。它可脱离前台终端，但 **不等同于已证明 Windows 开机/崩溃自动恢复**。
- 任何从当前前台 `run` 迁移到受管运行器的操作必须先 Freeze：合法 Runtime Key 来源、运行身份、阻止同 Tunnel ID 双实例、备份回滚、由本机用户交互输入凭据、单次切换、实测 MCP 文件读取。禁止抓取现有进程内存/环境变量提取 Key，禁止将 Key 入库/日志/ChatGPT，也不自动执行此前曾被安全检查阻止的 DPAPI Supervisor 方案。
- 如409再现：记时间/工具请求/同子进程代次及 initialize_epoch，从健康快照区分“本地仍在线但握手异常”与“本机进程为0”；不盲目重启、不对未知副作用重复写操作。审查客户端 initialize + notifications/initialized 时序，必要时向官方提交脱敏证据。
- `tools_list.ok=false` 可表示未观测到工具枚举，不等于所有 MCP 失败；以同子进程的真实工具调用和组件状态联合判断。
- 本地 HTTP健康接口只绑定 loopback；此补丁不得改变 FlClash、Windows代理、已登录浏览器、已有 DCR/Runner、MCP插件认证/权限。

## 5. 验收/回滚边界
- 完成：原链路恢复读文件；健康快照脚本语法 PASS 和真实运行 PASS；定时任务已注册并手工触发成功（LastTaskResult=0）；防重恢复脚本一次真实 PASS；脚本归档共同工作区。
- 未完成：72小时/开机/注销/异常退出恢复、受管运行器迁移、5次真实独立跨会话不掉线验收、409根因彻底消除。禁止将“当前一次健康/五次短测”写成长期稳定 PASS。
- 可回滚健康任务：`Disable-ScheduledTask -TaskName GPT-Windows-Tunnel-HealthLog`；脚本仅附加本地日志。
- 可回滚恢复入口：先确保当前隧道不在恢复中，再用 `Restore-Interactive.ps1.backup-20261014` 还原原脚本。**但原脚本的命令行权限盲区会一起恢复，先审查。**
- 若被动发现当前隧道掉线，先用独立 Windows 入口读取 `Tunnel-Health.jsonl` 末尾和当前进程状态，确认身份后再使用原交互式启动方式，禁止重复无效指令。

## 6. 2026-10-14 22:25 追加现实验收
- 当前唯一隧道PID仍38324、启动时间21:50:16、同一MCP子进程代次；控制平面 polling、proxy healthy、response delivery accepted；健康任务按计划运行并写入 JSONL，Task Scheduler 最近退出码0。
- 在同一次工具编排中实际连续调用5次 `GPT-Windows-MCP-Bridge.read_file` 读取启动脚本首行，**5/5 PASS**。这是短时、只读、同一会话的功能样本，**不等于5个独立生产周期、长期稳定或已排除偶发409**。
- 监控的任务计划为每5分钟一次，当前计划的重复有效期为创建日起365天；任务身份是用户A的 `Interactive / Limited`，需要对应交互登录态。不得把任务存在解释为Windows无人登录仍能自动检查，更不得称为自动重新建连。
