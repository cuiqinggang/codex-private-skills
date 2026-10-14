# GPT直连Windows双路执行桥 V3.0｜B路修复收敛、正式判路与五次 Reality 冻结

```ini
VERSION=3.0.0
DATE=2026-10-15
SKILL_PATH=skills/extreme-time-automation-bridge/
RELEASE_SCOPE=SKILL_AND_ROUTING_POLICY_ONLY
LIVE_WINDOWS_TUNNEL_CHANGED=NO
RUNNER_OR_PROXY_CHANGED=NO
PRODUCTION_ACTION_WORKFLOWS_CHANGED_IN_V3=NO
B_BOUNDED_ARTIFACT=SCOPED_REALITY_5_OF_5_PASS
B_ORIGINAL_FULL=INTERMITTENT_ACTION_ZIP_TIMEOUT_NOT_ERADICATED
A_OPENAI_TUNNEL=A_SEPARATE_HEALTH_AND_RECOVERY_ACCEPTANCE
ZERO_FAILURE_LONG_TERM=NOT_PROVEN
PHYSICAL_FASTEST_LIMIT=UNKNOWN
```

## 0. V3 范围（先判目标，禁止放大结论）

本版本是原 **GPT直连Windows双路执行桥** 技能包的规则及证据升级，保留 A 自建 OpenAI Tunnel→Windows MCP、B GitHub→Actions→Windows自托管Runner、R 第三方 Remote 免费额度闸门与旧功能、旧冻结。不替换任何仍在运行的 Windows 进程、隧道、认证凭据、FlClash、全局代理或 Runner 注册，不部署新通信系统。

**此次已经解决的是 B 路小型非敏感结果任务的可用性与典型性能问题**：采用已成熟官方 GitHub Actions 双作业复用路线，避开 Windows 本机下载外部 `actions/upload-artifact@v4` ZIP 的不稳定环节；并未证明旧 FULL 的那条 codeload ZIP 下载链路永久恢复，也未证明 A 主路的初始化/无人恢复问题已解决。

## 1. 原因与成熟最小修复（GOOD→BAD→FIRST_DELTA→最小复用）

- **GOOD**：旧 FULL 过去可成功执行 Windows 业务、上传官方 Artifact 并回读；2026-10-15 再次真实成功 [97秒 Run 38601884050](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38601884050) 与 [144秒 Run 38602538548](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38602538548)。
- **BAD**：旧 FULL [419秒失败 Run 38264768349](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38264768349)、[422秒失败 Run 38405736959](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38405736959)，Windows Runner 已接单，但业务开始前 `actions/upload-artifact@v4` 依赖 ZIP 完整下载连续超时；不能以 HEAD 200、ping或单次成功判定长期根治。
- **FIRST_DELTA**：网络上的第三方 Action 准备/完整 ZIP 下载，而不是 Windows 本地 PowerShell 负载、Runner 完全离线或整个 GitHub 通道不可用。
- **成熟修复**：复用原 `windows-bridge-v1-fast.yml`（从固定 SHA 读取现有 JSON、PS1、原 Invoke-BridgeTask，保留合同校验），另设官方 `windows-bridge-v2-bounded-artifact.yml` 双作业：Windows 无外部 Action→压缩小证据经 GitHub 原生 Job Outputs→GitHub 托管 Ubuntu Job 核验 result/stdout/stderr→官方 `actions/upload-artifact@v4` 上传。原 FULL、原 FAST 均保留。只需新工作流组合，不重造执行器、不更改用户网络代理。

## 2. Reality 证据：小证据 V2 路线 5/5 PASS

| 轮次 | Run ID | 全工作流时间 | 云端 Artifact ID | Windows执行及Artifact |
|---|---|---:|---:|---|
| R1 | [38603199346](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38603199346) | 36 s | 11913903599 | PASS |
| R2 | [38603459215](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38603459215) | 36 s | 11913529977 | PASS |
| R3 | [38603580797](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38603580797) | 30 s | 11914471832 | PASS |
| R4 | [38603712945](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38603712945) | 36 s | 11915146889 | PASS |
| R5 | [38603850316](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38603850316) | 38 s | 11914652213 | PASS |

五轮均为不同 Run ID、同一冻结 SHA `f55521366c8fb6e0fc9845c67def4993b9831df1`、同构无副作用计算负载、首次尝试成功，包含 Windows自托管执行和 GitHub 托管端官方 Artifact 上传。此前 [V2 原始 Reality 报告](GITHUB_WINDOWS_B_ROUTE_V2_REALITY_20261015.md) 已记录五份 Artifact 实际下载、`result.json`／`stdout.txt`／`stderr.txt` 对账 PASS。

统计：均值 **35.2秒**；中位数 **36秒**；最短 **30秒**；最长 **38秒**；极差 **8秒**；样本标准差约 **3.03秒**（变异系数约 **8.6%**）。这里是 GitHub `created_at→updated_at` 的观察总时长，不包含上游 GPT 派发前等待和用户外部下载检查成本；不是完整用户 T_VALID 或物理极限。

日志分层估计：Windows 接单前约11.1秒、Windows作业约8.4秒、跨 Job 交接约10.7秒、云端准备及上传收尾约5.0秒，边界为近似而非精确阶段服务指标；约 62% 时间花在调度/双作业交接，不能靠优化1～2秒业务计算消除。

另 [FAST Run 38602210133](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38602210133) 27秒 PASS，但**只有任务与日志回执，没有官方 Artifact**；不同功能合同不能按百分比直接宣称全面提速。FULL 97/144秒成功，但仍存在历史下载长尾的未证伪风险。

## 3. V3 正式执行前分流（不需为小幅提速再修改生产配置）

1. **A 主路｜GPT→OpenAI Tunnel→Windows MCP**：在远端真实读取/命令可用、权限允许且任务适合交互时仍优先；遇409、Session terminated、进程退出时遵循 [A路 V2 恢复 SOP](TUNNEL_AUTORECOVERY_V2_20261015.md)，不得把 B 的五轮通过当作 A 也通过。禁止关闭在线实例测试、制造双隧道或要求用户反复提供密钥。
2. **B FAST｜无需官方 Artifact**：已有 [`.github/workflows/windows-bridge-v1-fast.yml`](../../.github/workflows/windows-bridge-v1-fast.yml)，只处理合同允许日志回执的短任务，要求冻结输入、可核对 Task ID 与结果，按用户授权手工派发。
3. **B V2 有界官方 Artifact｜小型非敏感成功证据**：已有 [`.github/workflows/windows-bridge-v2-bounded-artifact.yml`](../../.github/workflows/windows-bridge-v2-bounded-artifact.yml)，五次 Reality 通过后可在审核合同边界的任务中优先使用；**仍是手工触发，禁止无条件自动替代原 FULL**。任务输出必须已知很小、不含任何密钥或隐私/业务机密，容忍失败时官方证据归档不等价。
4. **B FULL｜大文件／未知大小／失败证据／强审计任务**：保留 `extreme-time-windows-bridge.yml` 正式回退，不自动降级证据质量。原 FULL 能成功但其本机 Action ZIP 长尾风险未根除；若新故障出现才回 GOOD/BAD/FIRST_DELTA，并走官方成熟修复与可逆验证。
5. **R 第三方 Remote**：仅在真实账户额度、权限和任务收益允许时使用；遵从 [额度运营及路由闸门](REMOTE_DCR_QUOTA_OPERATIONS_V1.md)，不可将额度阻断误认网络断线。

### V2 有界路线的不可越界限制

- Windows Job 当前检查 ZIP **Base64 字符 ≤480000**，GitHub 托管 Job 解码 ZIP **≤360000字节**；不是任意大工件传输工具。
- 现有托管 Job 仅在 Windows Job success 时执行，**失败任务的官方 Artifact 保全不等价**。五轮 `CALLBACK_NOT_CONFIGURED`，故**没有回调成功 Reality**。
- GitHub Actions Job 日志可能打印整个 Base64 证据变量；**禁止把敏感 stdout/stderr、个人身份信息、认证材料、商业秘密放进此通道**。不能把 Base64 误当保密。
- 超限/失败可能发生在 Windows 副作用完成之后。按 Exactly-once：必须查原任务状态、结果和有无副作用；`UNKNOWN` 不得盲目改投 FULL 自动重做，必要时人工对账。
- 提升认证只对相同质量/权限/边界与证据合同成立。不得因成功 5/5 推断长期故障率为零或未来每轮 ≤38秒。

## 4. 故障分类及最短恢复

- **GitHub 排队/调度抖动**：先看 Run ID、job 分配时间、Windows实际执行回执；正常偶发延迟且成功→不折腾代理或 Runner。
- **Windows Runner 可接单但 Action ZIP 下载失败**：这是原 FULL 已证实的风险层。**先判适用合同，已有安全小证据可用 V2；有强回执需求则保留 FULL、按 GitHub 官方 Runner 网络/代理规则取证。**绝不直接设置 127.0.0.1:7890 或修改 FlClash/全局代理；历史已观察代理 ZIP 连接被拒。
- **V2 超限、证据缺失、回调未配置、敏感输出**：承认合同不满足，停止把它当等价 PASS；用审查过的安全替代路径，已发生的副作用先对账，不盲重发。
- **A MCP 409/断线**：走 A 自己的初始化、进程与网络恢复分层 SOP，不把 GitHub B 的已通过状态借给 A。
- **远程配额耗尽**：R 的额度问题不等于 A/B 故障。

## 5. 停止规则、回退、验收与状态

- **到此停止性能微调**：该范围 5/5 真实成功，平均35.2秒、观察极差8秒；在不改善安全/任务等价的前提下，为削减几秒而重构/重装/变更代理没有净收益证据，不执行。
- **不定期反复刷同一烟测**：只在真实新故障、任务合同扩大、需要验证失败工件/敏感输出保护/回调或跨时间长期稳定性时按成熟方案重新开受控实验。
- **冻结回退**：现有 FAST、V2有界、FULL 保持并存；V3仅为技能操作/取证说明升级，原V2工作流名称及历史版本不改。回退只需按任务特征选旧成熟路径，不撤销历史 Freeze、也不自动重发同一业务。
- **证据等级**：`B_BOUNDED_SCOPE_FINAL_VALID=YES`；`B_GENERAL_FULL_5_5=NO`；`A_AUTORECOVERY_FULL_REALITY=NOT_ESTABLISHED_BY_THIS_WORK`；`LONG_TERM_ZERO_FAILURE=UNKNOWN`；`THEORETICAL_PHYSICAL_LIMIT=UNKNOWN`。
- **所有关键入口仍需真实回执**：工作流绿色不等于 Windows 业务成功，除非 Windows Job、任务 Result、需要的 Artifact 和回读全部匹配。V3仅文档发布且回读成功时可写 `SKILL_V3_PUBLISHED=PASS`，不得据此写 `V3_NEW_RUNTIME_REALITY_PASS`。

历史证据和冻结规则继续参考 [V2 实测记录](GITHUB_WINDOWS_B_ROUTE_V2_REALITY_20261015.md)、[V2 差分分析](GITHUB_WINDOWS_B_ROUTE_V2_20261015.md) 与 [工作区最新状态](../../workspaces/extreme-time-automation-loop-v2.0/bridge/README.md)。
