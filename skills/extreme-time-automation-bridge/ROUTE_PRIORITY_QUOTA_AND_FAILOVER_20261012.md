# GPT直连Windows双路执行桥 v0.3.4｜路由优先级、月度额度与故障切换（2026-10-12）

> **定位：运行策略增补**。不删除旧通道、不重新创建基础架构、不改变已经冻结的脚本和历史证据。若旧文档的“主路”与本文件冲突，按本文件的**当前可用性/配额路由策略**调度；原主备名称作为历史版本保留。
>
> 权威位置：`cuiqinggang/codex-private-skills` → `skills/extreme-time-automation-bridge/` → `main`。完整技术细节继续参考 [SKILL.md](SKILL.md)、[DUAL_ROUTE.md](DUAL_ROUTE.md)、[OPENAI_TUNNEL_CONNECT_RECOVERY_20261012.md](OPENAI_TUNNEL_CONNECT_RECOVERY_20261012.md)、[TUNNEL_WINDOW_VISIBILITY_AND_RECOVERY_20261012.md](TUNNEL_WINDOW_VISIBILITY_AND_RECOVERY_20261012.md)。

## 用户已确认的长期调度偏好

1. **优先自建、可控、已验收的免费执行能力，减少受第三方月配额影响**。当前包含两个相互独立的可控入口：
   - **ChatGPT → OpenAI 官方 Tunnel → Windows 本地开源 Desktop Commander MCP**：在自己的 Windows 上运行、由用户建立的隧道和 MCP 接入（底层官方/开源组件，不声称自研 OpenAI 隧道协议）。此前真实远程文件读取、隔离写回、PowerShell 命令已 PASS；但 2026-10-12 19:01 左右实际调用返回 `Session terminated`，同日 19:06 左右的 GitHub Runner 只读报告 `OPENAI_TUNNEL_MATCH_COUNT=0`，**该时点不可用，必须先按既有恢复流程恢复并重新远程验收**。
   - **ChatGPT/GitHub → 私有共同工作区 → GitHub Actions → Windows self-hosted Runner**：仓库 `cuiqinggang/codex-private-skills`；Windows Runner `DESKTOP-4A1EGTM-etal`，`NETWORK SERVICE` 身份，Windows 本地自动启动服务。当前有新的 Reality 实测：任务 `BRIDGE-LINK-CHECK-20261012-1901`，GitHub Actions [Run 38240277230](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38240277230) 的 `windows-reality=success`，下载的 `result.json.status=PASS`、`exit_code=0`、`runner_name=DESKTOP-4A1EGTM-etal`；stdout 中 `GH_TO_WINDOWS_REALITY_PROBE_PASS`。**这条现在作为首选可用通道**，不依赖 Desktop Commander Remote 厂商的月度配额。
2. **第三方 Desktop Commander Remote（DCR）只作为额度充足时的可选补充**。2026-10-12 实测设备 `f6990966-5870-484b-bf79-409bc6fb963e` 仍显示 Online、`ping` 返回 `pong`，但 `start_process` 被厂商明确拒绝：`You've reached this month's Desktop Commander usage, so tool calls are paused. Your device remains connected and paired — do not retry or reconnect.`。所以 **ONLINE/PING=PASS，REMOTE_EXECUTION=MONTHLY_QUOTA_BLOCKED**。这是第三方服务端配额限制，**不是 Windows 离线、账号配对丢失、网络代理问题**；不要重配、重试、升级收费包或误删旧设备。
3. **按用户提出的月度使用经验记录**：DCR 免费额度一般约用到一个月中的前半月，后半月可能提前耗尽；**这只是用户个人经验，不是官方承诺的“保证可用 15 天”**。本次用完后，用户希望在 **2026-11-01** 再检查配额是否恢复，可恢复后酌情继续调用；**准确重置日期、免费额度、是否每月自动续期和实际可用天数必须届时根据账户/真实工具回执核验**，不能现在写成必然恢复或保底 15 天。未恢复就继续自建路线。
4. 自建 OpenAI Tunnel 暂时不通时，**优先通过现有 GitHub Runner 做合法诊断/最小修复**，不绕过权限/密钥安全控制，不创建第二隧道，不更换网络代理。OpenAI Runtime API Key 只能在 Windows 本机由用户按已有脚本交互输入，不能写入 GitHub、聊天、Actions logs、脚本明文或自动绕过授权。
5. **真正执行前先作能力选择而非重新选架构**：优先 **正在通过 Reality 验收**、能覆盖任务能力、无额度阻塞的入口；当自建 OpenAI Tunnel 实时 PASS 且存在用户交互会话时，可按延迟与任务适合度使用它；Tunnel 不通时直接 GitHub Runner。只有自建路径覆盖不了且 DCR 当月额度已核实可用时才考虑旧 DCR。不能把 GitHub Runner Session 0 的 `NETWORK SERVICE` 当作可代输 Runtime Key 的交互式用户 A 桌面。
6. **原有能力绝不删改**：原 DCR 主路/设备及自动登录任务、GitHub Runner、OpenAI Tunnel、桌面恢复快捷方式、Windows 隧道隐藏/显示证据、历史 SHA、故障差分和配置均保留。不得修改 FlClash、Windows 代理、用户已登录浏览器，不以一次局部错误宣称全部失效。

## 当前状态机（2026-10-12 19:xx 北京时间；这是时间快照）

```ini
SKILL_VERSION=0.3.4
ROUTING_POLICY=SELF_MANAGED_FIRST;QUOTA_GATED_DCR_LAST
GITHUB_SHARED_WORKSPACE_READ_WRITE=PASS_RECENT
GITHUB_ACTIONS_WIN_RUNNER_REALITY=PASS_20261012_RUN_38240277230
GITHUB_RUNNER=DESKTOP-4A1EGTM-etal
DCR_REMOTE_DEVICE_ONLINE=YES
DCR_PING=PASS
DCR_REMOTE_EXECUTION=MONTHLY_USAGE_EXHAUSTED
DCR_NEXT_CHECK_TARGET=2026-11-01
DCR_RESET_GUARANTEE=UNVERIFIED
DCR_HALF_MONTH_ALLOWANCE=USER_ESTIMATE_NOT_SLA
OPENAI_TUNNEL_REMOTE=SESSION_TERMINATED
OPENAI_TUNNEL_EXPECTED_PROCESS_COUNT=0_AT_20261012_1906_CHECK
OPENAI_TUNNEL_RECOVERY=NOT_YET_VALIDATED
TUNNEL_LOGIN_AUTOSTART=NOT_IMPLEMENTED
REBOOT_AUTO_RECOVERY=NOT_TESTED
MANUAL_RECOVERY=EXISTING_DESKTOP_SHORTCUT_REQUIRES_LOCAL_KEY
DO_NOT_CHANGE=FlClash,WindowsProxy,ExistingBrowsers,InstalledDCR,GitHubRunner
```

## 以后接续的最短规则

- **正常接单**：确认 GitHub Runner 最近 Reality 和执行权限；通过唯一任务 JSON + 受版本控制的 PowerShell payload 派发，等待 `result.json`、`stdout.txt`、`stderr.txt`、run/job 最终结论。含副作用任务严守 Exactly-once；任务状态 UNKNOWN 时先查询 run/call_id，不自动重派。
- **OpenAI Tunnel 回归**：先检查隧道进程与旧 ID（`tunnel_6acbeee2ce888191b775cd53429c7597`）；沿 [原恢复手册](OPENAI_TUNNEL_CONNECT_RECOVERY_20261012.md) 与 [桌面一键恢复/显隐手册](TUNNEL_WINDOW_VISIBILITY_AND_RECOVERY_20261012.md) 从原程序修复；必须由 Windows 用户在本机输入 Runtime Key，不要求新建隧道/插件/密钥；同一 Tunnel ID 只允许一个进程；恢复后需要真实 ChatGPT MCP 只读命令验收，不能仅凭 PID 判 PASS。
- **DCR 配额重置日**：2026-11-01 先核对厂商账户配额/可用性，执行最小的 Online + ping + 无副作用 Windows 命令（只有配额可用时才发实际命令），记录剩余额度及真实结果。若还提示额度耗尽，立即停止调用并沿自建通道继续，不重新配对。
- **防止错误知识覆盖**：历史 `DCR=PRIMARY`、`TUNNEL_HIDE=PASS`、`DCR_WINDOWS_COMMAND=PASS` 皆是不同日期/能力门的事实，不能覆盖当前 **DCR_QUOTA_BLOCKED** 或 **TUNNEL_SESSION_TERMINATED**。留存以前的成功证据，但“现在能否执行”一律以最新真实调用为准。

**版本策略**：这是 v0.3.4 内的运行政策增补；没有在 Windows 上更改系统/启动器，不假装修复已失败的 OpenAI Tunnel，也没有提前恢复第三方用量。更改应在成功后实际回写本文件与状态表。
