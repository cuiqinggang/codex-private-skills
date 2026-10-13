# GPT直连Windows双路执行桥 V1.0｜主备路由与 GitHub 加速修复
VERSION=1.0.0
SKILL_PATH=skills/extreme-time-automation-bridge/
REF=main
DATE=2026-10-13
METHOD=SANRENXING_V2_TASK_SCOPED_REUSE (《三人行》V2仅用于本任务；不改变它原本的全局候选状态)
RELEASE_SCOPE=POLICY_AND_EVIDENCE_PASS
GITHUB_FAST_LANE=ISOLATED_CANDIDATE_NOT_REALITY_ACCEPTED
ORIGINAL_PRODUCTION_WORKFLOW=UNCHANGED
CURRENT_A_LIVE=SESSION_TERMINATED_LAST_ATTEMPT;CHECK_BEFORE_USE
CURRENT_B_MINIMAL=HISTORICAL_PASS;PRODUCTION_RECOVERY_NOT_PROVEN
DCR_REMOTE=QUOTA_EXHAUSTED_LAST_CHECK
AUTO_ROLLBACK=NOT_INSTALLED

## 1. 必须按此规则接入和派发
使用本技能包时先读取本文件及 [免费额度运营 V1.0](REMOTE_DCR_QUOTA_OPERATIONS_V1.md)，先以任务类型、能力、真实状态判路，不每次为探活浪费 Remote 配额。
- **A 日常首选**：GPT-Windows-MCP-Bridge（OpenAI Tunnel + Windows 开源 Desktop Commander MCP）处理文件、交互、短命令和本地 Codex；只有实际 Session 有效且能力足够才判 ready。**本次 2026-10-13 后段曾返回 Session terminated；不能把上午的 PASS 写成此刻在线。** 先按原恢复 SOP 做非侵入性排障。
- **B 备路**：GitHub → Actions → self-hosted Windows Runner。A不可用时选已有且覆盖任务的工作流；较长或需留痕可用正式生产 workflow。禁止用计算 smoke success 冒充任意业务成功。
- **R 厂商 Remote**：官方 10,000 工具调用额度；当前剩余额度上次实测为 0，禁止无意义调用；阈值与警告按运营 V1.0。
- 每个有副作用的任务必须有唯一 TASK_ID、冻结 SHA、授权与最终业务回执；UNKNOWN先对账，禁止盲重发。不得为了绕安全拒绝而转其他通道。

## 2. 根因差分：旧的快基线和坏链路
| Run | 日期 UTC | 完整耗时 | 状态 | 关键环节 |
|---|---|---:|---|---|
| 37193387268 | 2026-10-04 | 84秒 | PASS | Hosted static→Windows；Runner 09:50:04开始，09:50:06下载外部Action，09:50:40文件就绪，09:50:44业务 PASS |
| 38240277230 | 2026-10-12 | 156秒 | PASS | Static 11:04:22已识别；Runner 11:04:40领单、11:04:42下载 upload-artifact、11:06:22文件就绪、11:06:25业务PASS |
| 38264768349 | 2026-10-12 | 419秒 | FAIL | Windows Job在准备阶段 3 次尝试下载 actions/upload-artifact ZIP 均因 HttpClient.Timeout=100秒失败，业务payload未运行 |
| 38386260876 | 2026-10-13 | 19～27秒 | PASS×2 | 单个Windows Job，无checkout、无外部Action；本地计算约 0.9～1.0秒 |

**GOOD→BAD 的 FIRST_DELTA**：原生产流程包含 1 个云端 Windows `contract-static` 前置job，导致二次调度；自托管 Windows job 有 `uses: actions/upload-artifact@v4`，Runner 会在业务前尝试下载 ZIP，网络波动从几十秒扩大至100秒/次，并发生三次超时。可达性 HEAD 200 不足以证实完整ZIP稳定传输。
**不是**本地 Windows 计算性能不足，也不是 GitHub通道架构本身失效。GitHub Actions调度与日志回收本来有非零固定开销，不承诺与直连MCP同延迟。

### 2026-10-13 追加确认：故障在本轮再次真实复现
- 推送隔离测试所需的旧 `bridge/tasks/*.json` 时，**旧 FULL 生产工作流被其原有 push 路径自动触发**：Run [38405736959](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38405736959)，创建 13:32:04 UTC、结束 13:39:06 UTC，约 **422 秒**，结果 FAIL。
- Windows Runner `DESKTOP-4A1EGTM-etal` 于 13:33:01 已接单，13:33:07 开始下载 `actions/upload-artifact@v4`；13:34:47、13:36:51、13:38:53 三次明确报告 `HttpClient.Timeout 100 seconds`，未执行受测 payload。该结果与 10 月 12 日 419 秒失败同构，确认**故障并非偶发一次的错误归因**。
- 因旧生产工作流将整个 `bridge/**` 目录纳入 push 触发，新建任务 JSON 会实际触发 FULL。今后必须在任何新合同写入前确认是否已有触发的同一 TASK_ID，避免额外自触发与重复执行。
- 本次另一候选 Fast 自动触发配置在提交中产生无 jobs 的失败 [38406812258](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38406812258)。已撤回自动 push 触发并恢复手工专用候选工作流（commit `0428c239`）；**从未把该失败算成 FAST 业务实测**。
- 此外自建 A 隧道在计划主动 dispatch 时回 `Session terminated`，所以本页不称该次派发成功。被平台安全检查拦截的任务写入也未绕行。

## 3. 成熟复用的最小修复（保留现有生产能力）
- 原正式 `.github/workflows/extreme-time-windows-bridge.yml` 原样保留，因它仍提供静态检查、冻结 payload、artifact 和可选 callback。历史失败需对该 **FULL** 路线单独复验；未经等价验证绝不删掉 artifact 或旧功能。
- 新增隔离 `.github/workflows/windows-bridge-v1-fast.yml`：**仅 workflow_dispatch，当前未加入自动 push 触发**。仅一个 self-hosted Windows job；不运行 checkout、setup、upload-artifact 等外部 actions；从 GitHub Contents API 按同一个提交 SHA 精确获取 task JSON、payload、旧 `Invoke-BridgeTask.ps1`，复用原执行器（合同验证、限时、目录边界、stdout/stderr/result.json），结果摘要在 GitHub Job 日志记录（任务ID、PASS/FAIL、退出码、SHA256、用时）。
- 候选属于 **FAST** 简化模式：只在日志给出简要回执，本机临时目录仍有 result/stdout/stderr，**不等价于 FULL 的云端 artifact/回调/长期取证**。没有经过合法实际触发和远端回读验收之前只能标记 CANDIDATE，不能宣布完成性能修复或自动切换。
- 已在共同工作区建立隔离无副作用 payload：`workspaces/extreme-time-automation-loop-v2.0/bridge/payloads/BRIDGE-V1-FAST-SMOKE-20261013.ps1` 和任务合同 `bridge/tasks/BRIDGE-V1-FAST-SMOKE-20261013.json`；**没有得到 FAST 实际运行 PASS**。
- 尝试发起自建 A→Github测试时，A MCP返回 Session terminated；尝试提交自动触发隔离任务时操作被平台安全检查阻止。**未通过其它工具绕行**；新候选自动 push 已撤下，仅保留手工触发、不可自动运行的方案。
- 仅在安全授权许可、现有用户明确派发权限及合法平台执行界面允许时，按 **Freeze→1次 Reality** 对 FAST 执行端到端测试；如仍受限制，继续使用原已验收的 FULL/最简健康通道，不复测被拒绝操作。

## 4. 分阶段计时与验收合同
严格记录：TASK_ACCEPTED、DISPATCH_ACK、RUN_CREATED、RUNNER_ASSIGNED、JOB_SETUP、FROZEN_FETCH_DONE、PAYLOAD_START/END、RESULT_READY、RESULT_READBACK、FINAL_VALID；使用日志 UTC 差分和单调时钟，不把不同运行的最快局部片段拼接成同一次有效总耗时。
**指标**：同任务同输入质量/授权条件的 `T_VALID`、中位/P95/最慢、业务最终成功率、第三方 Action 下载耗时与失败次数、是否恢复原文件取证能力。
- FAST 候选结果若缺云端 artifact，就只能归入日志回执型轻任务，**不能替换 FULL**。
- FULL 真正修复必须保留并验证 artifact、回调/留痕功能或经过审核的等价成熟机制；不得靠删步骤换“速度提升”的虚假成绩。
- 异步 B 无法消除 GitHub 控制平面调度成本；若业务目标是最小墙钟时间且 A PASS，日常短任务直接走 A。
- 登录/重启/72小时、长任务、并发和真实生产 FULL 均独立验收；当前这些没有完成。

## 5. 时间唯一标准下的决策
A 已确认可执行的日常操作 → A；A失联且B的 FULL 本业务合同已有真实PASS或可合法验收 → B；A/B均受限且R有真实额度/权限 → R。对“失败、用错、浪费额度、跳过验收”先提出错误分类、GOOD/BAD第一差异、预计净收益最高的成熟改法，才执行副作用动作。
无论什么新页面，只要用户说“GPT直连Windows双路执行桥 V1.0”，入口强制先读本页、当下状态和 R 运营规则。不更改 FlClash、代理、已登录浏览器；不关闭和重建原桥，也不新增未经许可的公网命令接口。
