# GPT直连Windows双路执行桥 V1.0.1｜统一接续、根因分层与Reality验收表

> 更新依据：2026-10-14 22:50（UTC+8）健康日志及同次会话远程工具结果。状态：`INITIALIZATION_FIX_STAGED_NOT_VALIDATED`；`LONG_STABILITY_NOT_ACCEPTED`。本文是唯一简版接续摘要；完整历史与证据见 `TUNNEL_STABILITY_INCIDENT_20261014.md`。

## 1. 目标与边界
保留原 ChatGPT→官方 Tunnel→本机 Desktop Commander MCP、原 Tunnel ID、GitHub Runner 备路、FlClash及Windows代理；不重新建隧道/重装MCP/修改认证和已登录浏览器。先完成虚拟差分/冻结，再经获准的受控现实切换验证。Runtime Key仅由Windows本机用户交互输入，不读旧进程环境/内存、不入日志或GitHub。Exactly-once、禁止安全检查绕行。

- 主机：`DESKTOP-4A1EGTM`，Tunnel ID：`tunnel_6acbeee2ce888191b775cd53429c7597`。
- 官方程序：`C:\AI\GPT-Windows-Bridge-B\tunnel\v0.0.16\tunnel-client.exe`。
- MCP：`C:\AI\GPT-Windows-Bridge-B\mcp\node_modules\@wonderwhy-er\desktop-commander\dist\index.js`。
- **唯一正式启动入口文件名：`Launch-OpenAI-Real-MCP.ps1`**，全路径：`C:\AI\GPT-Windows-Bridge-B\Launch-OpenAI-Real-MCP.ps1`。当前原生产入口；不得在未批准切换前覆盖。
- **隔离候选（不是正式入口）：`Launch-Initialized-Shim-Candidate.ps1`**，路径：`C:\AI\GPT-Windows-Bridge-B\persistence\Launch-Initialized-Shim-Candidate.ps1`。
- **人工恢复入口（不是启动器另一正式版本）：`Restore-Interactive.ps1`**，路径：`C:\AI\GPT-Windows-Bridge-B\persistence\Restore-Interactive.ps1`；它在进程为0时调用正式启动入口。
- 健康记录：`C:\AI\GPT-Windows-Bridge-B\persistence\Tunnel-Health.jsonl`，每5分钟只读记录；无自动恢复。

## 2. 当前证据（过去时点不得冒充实时状态）

| 项目 | 证据 | 结论 |
|---|---|---|
| 已发生进程退出导致 `Session terminated` | 10月12、14日曾观察 tunnel-client 进程为0 | 确认“进程消失”；退出触发原因未知 |
| 409 `mcp_initialization_required` | 前8次真实 `read_file` 有7成功1失败；同一运行代次仍有失败 | 条件性、间歇且可复发；不能推出长期12.5%故障率 |
| 2026-10-14 22:50:46（UTC+8）本地健康日志 | clients=1，PID=38324，child_generation=`eda367644b637e0a296f2c6cab2ae1c3`，control-plane=polling，proxy=healthy，response-delivery=accepted，initialize_epoch=94，dispatcher_failures=8，delivery_terminal_failures=0，state=HEALTHY_PATH_ONLY | 此时组件健康、身份仅限路径级别；不证明每个远程调用成功 |
| 2026-10-14 同页只读验证 | 首次读取健康日志PASS，随后读取正式启动脚本FAIL，原文 `CONFLICT: MCP server is not initialized; send initialize and notifications/initialized before operational requests` | 再次证明同一短时间范围内“可读→409”可切换；调用错误后未重复读、未重启 |
| 官方配置文档 | 旧式stdio `tools/call` 在成功 `initialize` + `notifications/initialized` 前被409/-32002保护门拒绝 | **拒绝条件确定；导致握手状态缺失的具体触发机制仍未知** |
| 现有监控/恢复 | 健康计划任务、只读日志、防重复人工恢复均部署验证过 | 监控已落地，不代表故障消除或自动常驻 |

注意：快照和409不在同一原子瞬间，不能证明在409精确时刻所有健康指标完全未变。绝不以 `readyz=200` 取代真实 `tools/call`。

## 3. 明确的因果边界与成熟候选

**已知机制**：官方旧式stdio初始化保护门要求成功 `initialize` 后收到 `notifications/initialized`，否则拦截操作请求。错误发生在工具调用进入本地 MCP 子进程之前。异常不是“单纯网络慢”，也不由启动PID存在与否决定。

**仍待区分**：
- H1 调用端对失败请求未发送 `initialize`；仅加通知shim无效。
- H2 `initialize` 已成功但缺少 `notifications/initialized`；官方shim可能直接修复。
- H3 请求在共享子进程初始化状态更迭/重建窗口内到达。
- H4 多会话并发交错；需逐请求时序证据，不先改并发参数。
- 进程退出另立故障树（终端会话关闭、外部终止、异常崩溃、旧stdio超时耦合等），尚未确认触发者。

**候选A：协议shim**，在原 `tunnel-client run` 命令上仅新增 `--mcp.stdio-send-initialized-notification`；官方文档确认仅在成功forwarded initialize之后发送通知，不替调用方合成initialize。Windows本地v0.0.16支持该参数。未正式切换，故不能宣布修复有效。

**候选B：官方受管 `runtimes connect/status --json`**，仅在A验收后独立验证，目标是不依赖当前前台控制台，需单实例、合法凭据交接、实际重启/注销/异常退出恢复证据。当前aliases为空，尚未迁移。

**候选C：`--mcp.max-concurrent-requests=1`**，仅有并发与失败相关的证据时才隔离评估，不和A或B混改。

官方参照：`https://github.com/openai/tunnel-client/blob/master/docs/configuration.md`、`https://github.com/openai/tunnel-client/blob/master/docs/onboarding.md`、issues #34/#45/#46。相似问题案例不等于当前v0.0.16已证实有同一bug。

## 4. 切换前新发现的BLOCKER（必须排除）
仓库 `bootstrap/Launch-Initialized-Shim-Candidate.ps1` 的 **不带 `-Launch` 分支会执行 `[IO.File]::WriteAllText($installed,$code,...)`，把候选脚本覆盖到正式 `Launch-OpenAI-Real-MCP.ps1`**。所以它的“预备/staging”不是纯只读，无条件调用会破坏单变量对照并改变正式入口。

必须在Windows本机比对**真实当前正式启动器与隔离候选**，确保除官方参数及明示防重保护外无其他运行行为差异；保留正式脚本SHA256与回滚副本。不要在未验证前调用无 `-Launch` 的预备分支，更不准把“部署候选成功”写成“协议修复成功”。

## 5. 下一步Reality验收表（严格按门执行）

| 门 | 动作（单变量、受控） | PASS证据 | FAIL/回滚与停止条件 |
|---|---|---|---|
| G0 当前状态只读 | 核对原PID、脚本版本/SHA、5分钟快照最后时间、真实调用错误与原实例身份 | 与现实一致，确定旧实例数/身份，无未知正在执行写操作 | 身份不明、状态变化或安全阻断：停止切换，继续保全证据 |
| G1 候选静态差分 | 逐行比较正式启动器和候选；修复候选预备分支的覆盖风险；冻结参数、备份和回滚命令 | 精确diff及HASH；实际生产命令仅增加官方通知参数；候选不覆盖正式入口 | 有非预期差分或无回滚：不进入G2 |
| G2 一次受控切换 | 已获必要批准；合法本机人工输入原Runtime Key；确认旧实例关闭且进程数0，再按冻结候选启动原Tunnel ID | PID唯一、真实MCP进程初始化、健康指标与ChatGPT远程只读可用 | 新实例失败则按已冻结方案回滚；不得双实例或抓取密钥 |
| G3 同构A/B对照 | 同G0基线条件下8次真实只读文件读取；记录每次T_VALID/状态/epoch/PID | 8/8功能PASS，0次409/502/断线；只表明短时功能通过 | 首例失败立即保全原始错误及FIRST_DELTA；不盲重试 |
| G4 质量门 | ≥5次**独立**真实运行周期（分开初始化/会话或可独立验证的业务周期），含实际只读与受授权写操作的独立确认 | 5/5以上独立PASS、无未知副作用、完整T_VALID可比较 | 任一失败，按同代次初始化事件、进程/健康差分分析并停止机械重复 |
| G5 常驻迁移 | G4通过后另立变更：官方 `runtimes connect/status --json`，隔离验证前台关闭、用户登录/注销、Windows重启及异常退出 | 管理器确实维持/恢复进程且真实远程工具调用PASS | 不得把隐藏窗口、status或本机健康200当成自动恢复 |
| G6 长期运行 | 记录72小时运行证据、失效次数/时刻、阶段性真实工具调用，统计端到端T_VALID和恢复成本 | 符合既定质量门且证据连续；分别结算协议稳定与生命周期稳定 | 72小时未完成/有故障则保留NOT_ACCEPTED，不伪造完成 |

注：8/8与5/5通过仅能支持对应的短期验收，不可计算长期“零故障概率”；恢复测试不允许用此前被安全阻断的批量重复启动方法绕行。

## 6. 接续最终四字段

`VERSION=V1.0.1`
`STATE=INITIALIZATION_FIX_STAGED_NOT_VALIDATED`
`CURRENT_REALITY=HEALTH_LOG_READ_PASS_THEN_OPERATIONAL_READ_409_FAIL`
`NEXT=G0_READ_ONLY_REALITY_CHECK_THEN_G1_STATIC_DIFF_AND_FREEZE`

下一页唯一优先任务是 **G0→G1**，而不是重复安装、立刻重启或直接迁移受管运行器。完成后才执行具备审批/凭据交接的G2/G3。
