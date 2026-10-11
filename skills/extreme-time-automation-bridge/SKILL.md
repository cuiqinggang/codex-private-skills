---
name: extreme-time-automation-bridge
version: "0.3.2"
description: GPT直连Windows双路执行桥。主路为 Desktop Commander Remote，备路为 GitHub Actions + Windows self-hosted runner；新增 DCR 配置损坏后的最短重配恢复与后台自启动自重连。
---

# GPT直连Windows双路执行桥 v0.3.2

STATUS=REALITY_PARTIAL_PERSISTENCE
VERSION=0.3.2
PRIMARY_ROUTE_CURRENT=PASS
PRIMARY_DEVICE_NAME=DESKTOP-4A1EGTM
PRIMARY_DEVICE_ID=f6990966-5870-484b-bf79-409bc6fb963e
PRIMARY_APP_VERSION=0.2.52
PRIMARY_PING_REALITY=PASS
PRIMARY_WINDOWS_COMMAND_REALITY=PASS
OLD_DEVICE_ID=28ebd1ea-e749-466d-ad88-1b9f262d0651
OLD_DEVICE_STATUS=OFFLINE
FALLBACK_ROUTE_CURRENT=PASS
FALLBACK_RUNNER=DESKTOP-4A1EGTM-etal
DCR_AUTOSTART_TASK=GPT-DesktopCommander-Remote-Autostart
DCR_AUTOSTART_USER=A
DCR_AUTOSTART_ENABLED=YES
DCR_RECONNECT_LOOP=YES
REBOOT_PERSISTENCE_REALITY=NOT_YET_TESTED

## v0.3.0 新增：DCR 最短恢复法

当 Remote 离线且运行 npx -y @wonderwhy-er/desktop-commander@latest remote 出现 JSON/config 或 lock 错误时，按 DCR_RECOVERY.md 执行：停止旧实例 → 备份坏配置/旧配对 → 重新运行 remote → 原 Google 账号重新配对 → 独立 ping → Windows 命令验收。

本次 Reality：新设备 503e66bf-4f80-49fc-a90f-020ec8c71b1e Online；ping PASS；Windows 命令 PASS。旧设备仅保留为 Offline 历史记录。

## 后台自动连接

已创建 A 用户登录态计划任务 GPT-DesktopCommander-Remote-Autostart。
launcher：C:\Users\A\AppData\Local\DesktopCommanderRemote\Start-DesktopCommanderRemote.ps1

行为：A 用户登录后自动启动；Remote 退出后 5 秒自动重启；MultipleInstances=IgnoreNew。

注意：尚未经过真实 Windows 重启后的 Reality 测试，所以开机持久化只能标记“已配置、待验收”，不能标 PASS。

## 双路规则

1. DCR Online 且能力覆盖 → 主路。
2. DCR 离线 → 优先按最短恢复法恢复。
3. 主路暂不可恢复而 GitHub runner Online → 备路。
4. 两路都不可用 → 明确阻塞原因，不伪装成功。
5. 不修改 FlClash / Windows 网络代理。

## 2026-10-04 双路真实复验 R1（当前状态）

- 当前在线主设备 ID：f6990966-5870-484b-bf79-409bc6fb963e；历史503e设备已Offline，以实时list_devices为准。
- 主路：真实Windows命令、部署、循环检查与实际runtime inbox验证PASS。
- 备路：首测 Actions run 37192980220 在 Git checkout 阶段两次连接GitHub失败；不得把Online当畅通。
- 根因范围修复：Windows任务不再依赖Git partial clone补取blob；从同一github.sha经Contents API按需读取任务JSON、payload和Invoke-BridgeTask.ps1。每文件最多3次、每次30秒、间隔2秒；使用本次workflow临时token，不存入文件/日志。
- 复测 run 37193387268 全部success；实际runner=DESKTOP-4A1EGTM-etal，执行exit_code=0、duration_ms=2453.998，真实进程/文件循环4/4 PASS及唯一marker回传。
- 未修改FlClash、Windows网络代理；当前双路限定命令任务PASS不保证未来零故障，不替代重启/注销持久化Reality。
- 证据：../long-term-memory-super-virtual-human/evidence/V050-WINDOWS-GOAL-LOOP-REALITY-20261004-R1.json。

## v0.3.1 新增：通用网络抖动容错（成熟方案复用）
适用于 Desktop Commander 主路、GitHub Actions 备路、n8n→MCP、HTTP API 等，禁止因为一次超时直接推翻成熟架构，亦禁止将所有错误概括为网络抖动。

- 先建立 GOOD 基线：区分连接探测、只读查询、写入命令、后台任务；记录正常响应区间、尾延迟、失败样本、任务最终完成率及总耗时。10次短测不能推断长期故障率。
- 优先使用成熟客户端/官方 SDK 已有超时、取消、有限重试、指数退避/抖动、会话恢复、任务结果查询接口；不得自研调度器/状态机。设定的调用内部 timeout 不等于云端远程请求会在该时间强制终止，须经 Reality 验证。
- 对 transient 错误（连接断开、超时、HTTP 429/502/503/504 等）才按官方 Retry-After/策略有限重试；403 Host 校验、授权/配置错误须修配置而非盲重试。连接恢复后沿原任务继续。
- 只读/幂等请求可安全重试；发送、写文件、业务动作等非幂等操作在 timeout/unknown 状态时必须先通过 call_id、进程 PID、任务 ID、最终回执、目标对象状态确认是否已执行，必要时幂等键/唯一标记保护后再继续。禁止对未知结果直接重发。
- Desktop Commander 主路：优先 list_devices → ping → 实际只读命令；离线用原 v0.3.0 的最短恢复法。若远程工具返回 running call_id，先 get_tool_result 或 list_remote_tool_calls，进程 PID 使用 read_process_output。未获 call_id/PID 时不得假设未执行。
- 失败恢复的净收益门：比较等待超时与安全恢复总时长；不将未验证的 3秒/8秒候选门限写为正式性能指标；只冻结有现实证据的配置。
- 禁止修改 FlClash/Windows 代理，禁止引入新的桥接层；允许对自己可控制的连接配置作最小适配，但任何取消/重试都须先确认不会破坏 Exactly-once。

### 2026-10-09 证据及限制
- 主路 Desktop Commander Remote 0.2.52 设备 f6990966-5870-484b-bf79-409bc6fb963e，通过原有 `npx -y @wonderwhy-er/desktop-commander@latest remote` 恢复持久会话，不必重新 Google 配对；GPT 端 Online、Ping、真实 Windows 命令回读 PASS。
- 曾测 10 次 Ping：第1次超时、随后9次 PASS；命令3次中2次回读、1次超时且执行结果未知。此为小样本，不能认定长期故障率或根因。
- 本版本冻结的是复用策略，不声称客户端已经实现可强制取消的短超时，也不声称 n8n 完整业务链路 FINAL_VALID。

## 阻塞不等于放弃｜成熟方案组合恢复门（2026-10-10增补）
**适用范围：** GPT、Codex、双路桥、工具/网络/本机命令的普通技术失败。默认动作是继续解决母任务，不能因一条命令或一次连接失败自动终止。失败层级必须精确标记（工具调用、命令、节点、任务），不可由局部失败推断整个成熟系统不可用。

1. **定位证据：** 保留原始错误、时间、调用 ID/PID、运行环境、授权范围；先以已成功的 GOOD 基线做正反差分，判断网络、配置、命令包装、权限、工具自身或业务逻辑。
2. **成熟复用：** 先查本技能包、历史可回读成功案例、官方已有接口/恢复功能与已授权工具；禁止优先自研替代桥、调度器或状态机。已成功能力不重复折腾，例如 GPT-DCR 的 `whoami` 真实 PASS，不因 Codex 自己的 `exec_command` 受限而判 GPT 主路失败。
3. **候选空间：** 允许在虚拟阶段检索、组合、淘汰数十/数百甚至更多有根据的成熟方法；这不是强制做几千次现实调用。每轮保留最多3个高净收益候选，依次复核前提、失败模式、依赖、兼容性、风险、时间成本；模拟多个迭代，旧证据和失败路径不丢失。
4. **受控现实：** 选最小授权验证动作，按 Freeze 后必要的一次现实验证或经用户任务规则允许的诊断执行；非幂等动作先查回执，严格 Exactly-once；成功后沿原任务恢复，而不是重新从头开始。
5. **继续门：** 普通阻塞即使多次失败，也要先判断是否还有新证据、新成熟候选或有正净收益的合法诊断；不可只因“又失败了”停止。禁止盲目重复相同失败、机械凑次数和无上限消耗。
6. **停止条件：** FINAL_VALID；已无证据支持继续且下一候选净收益≤0；用户明确终止；资源/时间明确上限；或当前受限动作触及硬性安全/权限拒绝。**硬性拒绝只停止该受限动作，不能换渠道绕过；其他合法独立节点继续。** 暂不可完成时冻结状态、记录精确阻塞和可执行下一步，不宣称整体 PASS。
7. **诚实边界：** 成熟组合显著增加可解机会，但并不能保证每个问题一定可解决，特别是授权、物理限制或不可用外部依赖；不得用“必然解决”代替现实证据。

记录字段：BLOCKER_ID、GOOD_BASELINE、FIRST_DELTA、ERROR_CLASS、MATURE_CANDIDATES、VIRTUAL_FILTER、AUTHORIZED_REALITY、EXACTLY_ONCE_STATE、T_VALID、NEXT、STOP_REASON。此为方法规则增补，不代表双路全部新场景已现实验收。


## n8n 常驻可调用诊断与入口区分（2026-10-10）
**现场证据：** Windows Docker 容器 `n8n-local`（`n8nio/n8n:stable`）健康运行，127.0.0.1:5678/healthz HTTP200，浏览器Chrome CDP 127.0.0.1:9223/json/version HTTP200；n8n `/rest/workflows` 未带会话返回401，只表示受保护管理接口未认证，**绝不能据此判断n8n故障、要求用户重新授权或停止任务。**
**正确三层检查：**
1. `docker ps` 核验健康；`Invoke-WebRequest http://127.0.0.1:5678/healthz` 核验服务；此层不代表业务成功。
2. 使用已经配置好的、获准的n8n容器原生CLI只读枚举 `docker exec n8n-local n8n list:workflow --all`；必要时 `export:workflow --all --output=/tmp/<临时文件>.json` 检查 `active`、节点类型、Webhook方法和路径，禁止把敏感凭据输出日志。Manual Trigger（手动触发）与已激活Webhook是两种不同运行入口。
3. 仅对已知、获准且副作用范围清楚的Webhook提交任务，必须取回业务回执并核验Exactly-once；不能把任意活跃Webhook当作无副作用测试接口。非幂等任务如结果UNKNOWN，先查既有执行记录，绝不盲目重复。
**已回读的2026-10-10实例事实：** 容器共7个已有工作流，其中 `PY9w2v8FnZmj7nff`（N8N-DEPLOY-03｜Reasonix 本机成果闭环）`active=true`，POST `/webhook/n8n-deploy-03-task`，后续有本机Reasonix执行节点；`v27McpReadonly20261009`（V27-MCP-READONLY-DISCOVERY-20261009）`active=false`，入口为Manual Trigger，没有现成可直接外部POST的业务Webhook。**二者合同不同，不可当作同一浏览器竞速任务。**
**端口冲突诊断：** 对已运行容器执行 `docker exec n8n-local n8n execute --id=...` 报 `n8n Task Broker's port 5679 is already in use`，是该命令在运行容器内启动新的CLI执行上下文引发端口冲突，**并非n8n主服务离线，也不是授权错误**。不要停止现有服务、改端口或重建容器来“修复”此只读测试。改用已存在的正常触发入口；缺少匹配的合法入口时记录缺口，在获准范围内按成熟n8n功能对工作流做最小适配并单独验收。
**常驻健康标准：** docker健康 + 正确现有工作流激活状态 + 匹配其合同的获准触发 + 可回读最终业务结果；前两项不能代替后二项。断线按原DCR v0.3.1恢复流程处理，不修改FlClash或Windows代理。当前n8n服务在线且有一个可触发的历史Reasonix工作流，但“GPT↔n8n↔现有浏览器同任务竞速”仍`NOT_TESTED`。

## v0.3.2 变更摘要
- 增补n8n常驻调用入口的诊断和恢复规程；修复把401误判为服务故障、把CLI端口冲突误判为需要重授权的排障错误。
- 保留v0.3.1已验证的DCR/Actions双路结构、设备和执行器配置，未重建系统。
- 此为规范和现存入口的只读现场验收升级；n8n与浏览器同合同端到端竞速仍待Reality，不能宣称已经完成。

## 开源 B 通道隔离实验（2026-10-12，保留 v0.3.2 主体）
- 单独目录 `skills/windows-open-source-bridge-b/` 记录成熟开源组件组合、官方限制及本地真实证据；**不替换、不删除**本技能包原有 DCR 主路 / GitHub Runner 备路。
- Windows `C:\AI\GPT-Windows-Bridge-B` 安装成功：MIT 开源 Desktop Commander MCP 0.2.52，26 工具发现、真实目录工具调用及 PowerShell 标记回执通过；OpenAI Secure MCP Tunnel Client 0.0.16 官方 SHA256 验证与本地 CLI PASS。证据 run=38169533429。
- 月度配额为厂商 Remote Desktop Commander **托管**版限制，本地开源执行器不受这项厂商远程配额影响；但 OpenAI 自定义 MCP 权限和 Tunnel 身份验证独立存在，不可通过修改网络组件取消。
- 当前状态 `B_LOCAL_FUNCTIONAL=PASS / B_CHATGPT_END_TO_END=NOT_TESTED / B_FINAL_VALID=NO`。在官方权限允许并完成实际端到端验收前，保持已验证的 GitHub Runner 正式执行通路。禁止改 FlClash、代理和原自动启动任务。

- 2026-10-12 Reality 增量验收：run [38169679396](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38169679396)，Windows 本机 MCP `tools/call` 实测目录读取 + PowerShell 命令输出 + 隔离目录 `write_file → read_file` 内容回读，全部 PASS；OpenAI 完整 CLI 0.0.16 通过。仅本地调用闭环 PASS，不代表隧道已鉴权或 ChatGPT 远程端到端通过。`B_LOCAL_FUNCTIONAL=PASS / B_CHATGPT_REMOTE=NOT_TESTED / FINAL_VALID=NO`。
