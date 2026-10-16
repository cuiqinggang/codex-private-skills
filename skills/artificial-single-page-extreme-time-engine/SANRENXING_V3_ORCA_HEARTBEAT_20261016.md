# 《三人行》第3版候选补充：Orca–Codex 心跳隔离与结算恢复（2026-10-16）

> 类型：V3 待合并实证条目，不覆盖 SANRENXING_V2.md，不声称已经存在的 V3 主文件已更新。仅经过事实验收的部分标为 PASS。

## 确认事实及反例
- 2026-10-16 r3/pilot-B：Orca `orchestration send --type heartbeat` 超过25秒触发 `subprocess.TimeoutExpired`。
- r3 的 `run_model` 在真实 Codex 业务进程仍运行时执行心跳；未捕获的超时异常导致执行进入 `finally`，终止原 Codex 父子进程。故障类型是 **管理面失败传播到数据/业务面**。
- r3/pilot-B 最终 `passed=false`，本地耗时534799.4744ms，独立QA有失败；不得计入十轮或 A/B。
- r2/p01-B 业务检查 accepted=true，但管理层 task-list 25秒超时、服务启动10秒超时且缺最终 `result.json` / `local-acceptance.json`，结算 UNKNOWN，不能假定已完成。

## 成熟模式（最小改动）
1. 管理心跳（control plane）只影响状态记录；不能因单次心跳超时终止正常业务进程（data plane）。
2. 超时操作状态必须为 `UNKNOWN_RECONCILE`，不能等同失败，也不能盲重发。
3. 对结算采用唯一 `request_id` + 官方 `--retry-request` 幂等键；先按 `task_id` / `dispatch_id` 读取权威状态，对同一次业务恰好一次结算，回执未知时先对账。
4. 原有全局预算、独立 QA、资源底线 4 GiB、业务超时/清理及双方 A/B 公平条件均保持。
5. 先虚拟成熟整体路径 → 冻结最小差分 → 故障注入测试 → 一套真实完整业务 → 10组配对（不把 pilot 算入）。

## 本次物化证据
- C 通道 Remote Desktop Commander 于本次真实返回 pong、读取本地文件并执行测试。
- Windows 原样保留 r3，新增 `C:/AI/Orca-Codex-Validation-20261014/suite-ab-r4.py`。
- r4 SHA256: `39CEECBEFF894BA447E86F0F24FE6E0BF0356AEB820B7C7C38736EE5DBDE5DBD`。
- r4 Python 语法编译 PASS。
- 注入测试：`tools/test_r4_heartbeat_fault.py` 在提取的真实心跳处理 AST 内模拟 TimeoutExpired；验证留下 UNKNOWN 证据且不触发 terminate；2/2 PASS。
- 结算第二项测试仅静态验证 `--retry-request` 与单次 send 无自动写重试；**不代表官方服务端幂等性已通过新的端到端测试**。历史 V2 项目另有官方同 request 重放只得同一消息的已验记录。
- 新 `r4/pilot-B` 已通过 C 通道启动，**最终结果须以结果文件为准，不提前认证**。

## 当前边界
`F003` 旧失败不抹掉；r4 新 pilot 完成前不得计正式通过。新 pilot 必须核对 14/14 外部验收、三组离线回归、零残留、Orca 结算与来源哈希；随后才能开展十组 20 套公平 A/B。
GitHub 正式目录当前可见 V1/V2，但 **尚无 SANRENXING_V3.md**；本文件为 V3 专用补充，不代表正式 V3 主文件已发布。


## r4 新 pilot 真实终局回读（2026-10-16 21:29 中国标准时间）
- Windows C 通道真实回读 `suite-ab-20261016-r4/pilot-B/local-acceptance.json`：`accepted=true`，`local_wall_ms=608714.1439`（约10分08.7秒；范围为本地入口到最终独立QA、清理及结果回读，不包括云端后续归档）。
- 同一目录 `coordinator-done.json`：Orca `task_status=completed`、`dispatch_status=completed`、官方消息 `msg_130955edd5bf`、run `run_0d8ae9b7ec57`、task `task_c2614787c730`、dispatch `ctx_813f831378ae`。
- `business-inspection.json`：`accepted=true`，T01/T02/T03离线回归总计21项通过。业务阶段发生 Codex request timed out/reconnecting 2/5..5/5，最终降级 WebSockets→HTTPS、恢复执行并完成任务。不得将此前网络重连解读为已经证实的 Orca 心跳根因。
- r4 在正常网络重连条件下完成端到端，不等同于对官方心跳超时路径进行真实 Orca 服务端故障注入；该路径已有提取实际 AST 的本地注入测试2/2 PASS。历史 r3 心跳超时失败证据仍需永久保留。
- 该套是新版本 pilot，只可作为“完整三任务新版本首套实际通过”，**不计正式十组连续稳定性或配对A/B**。正式十组目前 0/10。
- 本次因果辨析：已确认的确定性逻辑缺陷是“管理心跳同步异常触发业务进程清理”，不是“网络连接必然不可恢复”。管理端偶发超时的具体上游因果尚未由服务端诊断唯一确认；禁止把假设写成已证实根因。
