# GPT直连Windows双路执行桥 V2｜B 路成熟差分、极限有效时间与当前验收（2026-10-15）

**范围**：B 路 GPT → GitHub 共同工作区 → GitHub Actions → Windows self-hosted Runner（DESKTOP-4A1EGTM-etal）→ PowerShell → 可验证的回执。A 自建 MCP 连接及 FlClash/系统代理、DCR 与 Runner 注册全部保持不变。

**方法**：《三人行》第2版按任务采用成熟方案优先、GOOD/BAD 差分、FIRST_DELTA、最小可逆修复、Freeze 后 Reality；有效墙钟时间只认同一业务完整成功、真实结果回读；UNKNOWN 禁止重复有副作用任务。

## 1. 本次重新打开 GitHub 官方工作流与独立运行记录

主生产：`.github/workflows/extreme-time-windows-bridge.yml`（HOSTED 合同静态检查 → Windows 受控执行 → `actions/upload-artifact@v4` 官方归档 → 可选 callback）。`windows-bridge-v1-fast.yml` 是已存在、仅手工触发、无外部 Action 的候选；无云端官方 artifact，**不能直接替代 FULL**。

| 同构证据 | 结果 | 端到端证据 |
|---|---|---|
| 2026-10-12 [FULL Run 38240277230](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38240277230) | **PASS**，约156s | Windows frozen fetch、BRIDGE_PASS、官方 Artifact ID 11742242568、可在云端读取 |
| 2026-10-12 [FULL Run 38264768349](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38264768349) | **FAIL**，约419s | Windows Job `Set up job` 失败，未进入业务 |
| 2026-10-13 [FULL Run 38405736959](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38405736959) | **FAIL**，422s | 13:33:07Z 下载固定 SHA `actions/upload-artifact@v4`；13:34:47Z、13:36:51Z、13:38:53Z 连续 100 秒下载超时；未执行 payload |
| 2026-10-13 [最小 Windows Run 38386260876](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38386260876) | **PASS**，墙钟约249s（含排队）；Runner 内本地计算 1000.225ms | 说明 GitHub调度 / Runner接单可用，但墙钟排队是独立可变瓶颈；此任务无官方 Artifact，不能与 FULL 直接按功能等价比较 |
| 2026-10-14 [Windows 只读取证 Run 38595535165](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38595535165) | **PASS** | 最新可定位的 Windows 实际接单、执行日志，属于只读诊断 |
| 2026-10-15 凌晨 [FULL工作流 Run 38599737148](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38599737148) | **STATIC_ONLY** | 绿色 success 只表示云端 contract-static 成功，Windows-reality = skipped，不是 B 路完整功能通过 |

### FIRST_DELTA（已证实）

- 坏点不在 Windows 本地业务计算，也不是 GitHub 调度系统整体断开；根因范围是 **Runner 的作业准备阶段从 `codeload.github.com` 下载外部 Action ZIP 的完整传输路径**。
- [Run 38419778688](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38419778688)：`codeload/_ping` 直连 HTTP200，约1550ms；当时现有 FlClash 本地端口 7890 对 ping HTTP200，约3104ms。
- [Run 38420210117](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38420210117)：完全相同固定 SHA ZIP 直连**仅响应头** HTTP200（1252ms）；显式走已有 127.0.0.1:7890 的**完整 ZIP** 在 2088ms 时返回 `SocketException_ConnectionRefused`，没有取得 ZIP 正文。
- `Runner .env` 过去未发现代理环境项，且其 Windows SERVICE 运行身份与交互用户不同；但**不能**仅凭这个事实认定代理设置缺失就是最终原因，更不能直接改 FlClash 或把不稳定的 7890 写入 Runner。

GitHub 官方诊断要求 Runner 连通 `api.github.com`、`codeload.github.com` 及作业/日志/Artifact 相关域名；其行为应以实际响应体传输而非 ping 或 headers 为准。官方资料：
- https://github.com/actions/runner/blob/main/docs/checks/actions.md
- https://docs.github.com/en/actions/how-tos/manage-runners/use-proxy-servers
- https://docs.github.com/en/actions/reference/runners/self-hosted-runners

## 2. 本次实际最小改动：去除纯文档更新带来的无效调度

`.github/workflows/extreme-time-windows-bridge.yml` **仅替换一处 `on.push.paths`**：
- 原：`skills/extreme-time-automation-bridge/**`
- 新：`skills/extreme-time-automation-bridge/bootstrap/**`

保留业务任务 JSON 变更触发、桥工作区触发、工作流本身变更触发，Windows任务执行、静态合同、唯一任务选择、原官方 Artifact、原 Runner、原 callback 均不变。技能包 Markdown 文档更新时不再启动空任务静态检查，但 `bootstrap` 脚本变更仍触发解析。

**提交**：[bcad8ba3](https://github.com/cuiqinggang/codex-private-skills/commit/bcad8ba3ff29a083ad7f84acf08a976df54414f5)。

**Reality**：[Run 38601018542](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38601018542) conclusion=success；`contract-static` 解析 PowerShell、合同验证、任务发现全部成功；`windows-reality` 跳过是符合“没有任务 JSON”的预期。这证明仅触发路径最小修复的**静态功能无回退**，不证明 FULL 的 ZIP 下载已经恢复。

## 3. 成熟修复优先级：拒绝继续自研和重复超时

1. **第一优先（真正 FULL 修复）：** 按 GitHub self-hosted Runner 官方代理说明，在有权限且能获得真实 Runner 环境/完整固定 SHA ZIP GET 的证据后，仅考虑该 Runner 层的 `https_proxy`/专用 `.env` 继承，不修改 FlClash 本体、Windows 全局代理、Runner 注册。先保存原配置及回滚，再验证进程账户上下文；不得在已有代理 ZIP 连接拒绝的情况下武断设为 7890；Runner 重启需先确认无运行中任务。
2. **第二优先（短任务净时间）：** 已有 `windows-bridge-v1-fast.yml` 可在业务**不需要官方 Artifact 和 callback**的情况下采用，但必须用受审授权的固定 SHA、现有合同验证和真实 Windows 回执通过一次或多次端到端验收后才能选择。不要用无 Action 计算 smoke 证明 FULL 已修好。
3. **第三优先：** 若无法让 Runner 本体稳定获取外部 Action ZIP，需另立隔离、可回滚的固定 SHA 官方 Action 本地化候选，计算维护/供应链/兼容性成本；在没有取得同等官方归档回执之前，不替换生产 FULL。
4. **绝不应做**：重复让 FULL 白等 3×100 秒；仅因为一次 HEAD200 判定网络恢复；修改 FlClash、系统代理；重装 Runner；同一 UNKNOWN 业务重发；删掉官方 Artifact 后宣称 FULL 等价且更快。

## 4. 实际端到端效率/质量验收合同

同一任务、相同负载与冻结 SHA：

`TASK_ACCEPTED → RUN_CREATED → RUNNER_ASSIGNED → JOB_SETUP → FROZEN_FETCH_DONE → PAYLOAD_DONE → RESULT_READY → ARTIFACT_UPLOADED → RESULT_READBACK → FINAL_VALID`

记录 UTC 原始时标和同一 Run ID；比较完整 `T_VALID`，不拼不同运行的局部最快时间。**不能事先承诺某个固定秒数**，GitHub 排队与公共网络出站并不由 Windows 本地计算控制。

验收分类：
- `STATIC_TRIGGER_FILTER` = **PASS**（新提交已通过静态 Actions 检查）
- `RUNNER_CAN_ACCEPT_JOB` = **PASS_SCOPED_HISTORICAL**（最近已知 10月14日独立只读任务）
- `FULL_PRODUCTION_CURRENT` = **FAIL_HISTORY / NOT_RETESTED**（最后一次真实带业务 FULL 为 10月13日失败）
- `EXACT_ACTION_ZIP_FULL_BODY_CURRENT` = **NOT_CONFIRMED**（历史直接头部 HTTP200，不等于 ZIP）
- `FAST_EQUIVALENCE` = **NO**（功能合同不同）
- `FIVE_INDEPENDENT_FULL_REALITY` = **NOT_DONE**；`ZERO_FAILURE_STABILITY` = **NOT_CERTIFIED**
- 当前执行环境的一次本机 Runner 诊断命令受到安全检查限制，**不通过其他连接绕行**。因此不能制造已完成 Runner 修复或五次真实验收的结论。

**Freeze**：V2；`B_PATH=RUNNER_RECEIVES_SCOPED_JOBS`; `FIRST_DELTA=CODELOAD_ACTION_ZIP_BODY_TRANSFER`; `SCOPE_REPAIR=STATIC_PUSH_NOOP_FILTER_PASS`; `FULL_RECOVERY=NOT_ACCEPTED`; `NEXT=AUTHORIZED_RUNNER_NETWORK_EVIDENCE_AND_ONE_EQUIVALENT_FULL_RUN_THEN_FIVE_INDEPENDENT_RUNS`.
