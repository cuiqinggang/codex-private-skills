# Reality Test Command Contract — v0.2.1

TASK_STEP=3_REALITY_ANCHOR

目标：执行冻结的 v0.2.0 架构，不再设计架构。

- Benchmark: PE-P0-GENERAL-01
- Model: typesafe/jev-1.13
- Endpoint: POST https://openrouter.ai/api/alpha/decisions
- Objective: min T_E2E subject to COMMERCIAL_GATE=PASS
- Model barrier depth: 1
- Action dependency depth: 2
- Final verifier barrier: 1

## 测试矩阵

1. Auth probe，不计入 T_E2E。
2. 拓扑扫描：1 / 2 / 4 / 8 个并发 decision shards。
3. 每个拓扑：2 次 warm-up + 10 次 measured full E2E。
4. 一个拓扑只有全部 10 次 measured 均 PASS 才进入候选。
5. 候选中取最小有效 T_E2E 的拓扑。
6. 最快拓扑：3 次 warm-up + 30 次 measured full E2E。
7. 30/30 PASS 才允许 REAL_CERTIFIED=YES。
8. T_REAL* 与 T_P0 取该冻结环境下确认阶段最小有效 T_E2E。

P50/P95/MAX/FAIL_COUNT 只作为诊断，不成为第二目标。

## T0/T1

T0：每次 run 开始读取当前 public benchmark input 之前。
T1：24 项现实 receipt/state 已回读、独立 oracle verifier 完成，并且 run manifest 已写入之后。

## Anti-cheat

Engine 不读取 private oracle。
Executor outcomes 属于 action backend。
Key 不写入仓库、RESULT.json 或快照。
21–24 只能在真实 predecessor receipt 后提交最终动作。
允许预先计算 hypothetical receipt branches，但真实 receipt 只负责选择分支。
失败不得通过降低门槛改成 PASS。
