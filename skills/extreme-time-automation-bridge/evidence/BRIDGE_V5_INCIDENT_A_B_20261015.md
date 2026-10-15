# GPT直连Windows双路执行桥 V5.0｜2026-10-15 故障核验与恢复记录

## 结论（截至北京时间 2026-10-15 19:51 后）
- A 路（ChatGPT -> OpenAI Secure MCP Tunnel -> 本地 Windows MCP）：**当前实际读文件、执行 PowerShell 均 PASS**；新进程 PID 25228；官方本机实时健康检查 2026-10-15T11:51:07Z 返回 HEALTHY、ready=true、control-plane=polling、mcp=initialized、mcp_child=running、initialize_epoch=20、dispatcher_failures=0、delivery_terminal_failures=0。
- B 路（GitHub Actions -> Windows self-hosted runner）：新任务实际执行 **PASS**，结果与 Artifact 上传成功。Run 38729014927，Artifact 11969392529，任务 ID BRIDGE-B-V5-RECOVERY-CHECK-20261015-R1，链接 https://github.com/cuiqinggang/codex-private-skills/actions/runs/38729014927。
- A 路只读隧道稽核：Run 38729166003，链接 https://github.com/cuiqinggang/codex-private-skills/actions/runs/38729166003。
- Remote Desktop Commander 云端远程工具为**独立第三方通路**；当前真实返回「You've reached this month's Desktop Commander usage... tool calls are paused」。设备可 Ping 不代表可使用额度受限的工具。不得将该限额误当作官方自建 A 隧道的已证实根因。

## A 路故障证据与时间线（UTC）
- 2026-10-15T11:20:47Z：旧 PID 43828 的健康记录为 HEALTHY，但累计 delivery_terminal_failures=1、dispatcher_failures=2。
- 2026-10-15T11:32:31Z：Supervisor 记载 TUNNEL_EXIT，exit code 0，运行 4362 秒。
- 2026-10-15T11:33:02Z：自动 TUNNEL_START。
- 2026-10-15T11:35:48Z：新 PID 52196 健康记录 MCP_NOT_INITIALIZED；未观察到 MCP initialize。
- 2026-10-15T11:42:38Z：再次 TUNNEL_EXIT，exit code 1，运行 577.2 秒。
- 2026-10-15T11:42:44Z：Supervisor 再次拉起新进程 PID 25228（一个进程）。
- 2026-10-15T11:45:47Z：新实例健康记录 MCP_NOT_INITIALIZED、initialize_epoch=0；随后 ChatGPT 页面对 A 路实际 read_file 与 start_process 多次成功。
- 2026-10-15T11:51:07Z：手动运行原有只读 Watch-Tunnel-Health.ps1，返回 HEALTHY、initialize_epoch=20、故障计数 0，和真实工具调用一致。

## 原有恢复能力验证
- 本地交互式用户上下文查询：GPT-Windows-Tunnel-Recovery-v1 计划任务状态 Running；GPT-Windows-Tunnel-HealthLog 状态 Ready。
- GitHub 自托管 Runner 上独立查询同名用户任务曾返回 NOT_FOUND：属于执行上下文可见性差异，不可据此断言服务缺失。
- Supervisor 主进程存活，实际负责恢复；确认仅 1 个 tunnel-client.exe，未重复创建隧道。
- PS002 Supervisor 修复已部署，SHA256 649E7A939AA8A27B91FE5FBE130E842E131EB96D55F36A1C00FED405335270EF。
- 未发现上次测试遗留临时防火墙拦截规则。

## 事实、未知与停止规则
- **已证明**：今天 A 路曾发生隧道退出（exit code 0、1）、初始化延迟与临时无法调用；现由已有 Supervisor 自动恢复，当前连续多次实际读取与 PowerShell 正常。B 路当前完整闭环 PASS。第三方 Remote Desktop Commander 额度受限。
- **尚未证明**：A 路 exit code 1 的底层触发原因；此次恢复能否保证以后不再退出。Supervisor 通过 2>&1 | Out-Null 丢弃了隧道原始输出，当前没有足够证据将 exit 1 精确归因于网络、官方控制平面或 MCP 子进程。
- **本轮不做**：不修改 FlClash、Windows 系统代理、浏览器、不重装或重启现有健康隧道；不绕过第三方额度；不把单次临时恢复夸大为永久稳定性修复。
- **故障复现时优先**：原有只读健康脚本与 Supervisor exit code / elapsed_seconds 对齐，然后取得安全脱敏的退出原因，定位 FIRST_DELTA；冻结小改动后才做一次验证。正式实际工作优先 A；A 不可用时改走不依赖第三方额度的 GitHub B 路。

## 本次代码变更
- 新增一次 B 路安全只读计算验收的任务 JSON，沿用既有成熟 payload，没有新增执行器。
- 原有 tunnel-r2-oob-readonly-20261014.yml 仅追加不改变行为的注释，用于触发一轮本机只读核验。
- **没有改动 Windows 现有隧道、Supervisor 或代理配置。**

状态：CURRENT_A=PASS / CURRENT_B=PASS / THIRD_PARTY_DCR_EXECUTION=QUOTA_PAUSED / PERMANENT_A_ROOT_CAUSE=UNPROVEN。
