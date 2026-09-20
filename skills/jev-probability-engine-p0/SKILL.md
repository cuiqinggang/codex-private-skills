---
name: jev-probability-engine-p0
description: 用“可商用门槛内只计端到端时间”的第一性原理，把现实任务编译为最少模型屏障、最大现实并行的概率执行图；以 Jev 为高速概率核心，配合确定性状态、动作与独立现实验证。用于 Probability Engine P0 的冻结、更新、Virtual-99、测时与复用。
---

# JEV Probability Engine P0

版本：0.2.0（Core② 成熟方案集群 + Virtual-99 结构冻结版）。

## 三核心

1. 时间唯一标准：先 COMMERCIAL_GATE=PASS，门内唯一优化量 min T_E2E。
2. 成熟方案集群：复用成熟概率原语、schema validation、状态机/transition table、并发调度、现实 verifier，不从零发明概率理论。
3. 超级智能体虚拟成熟：现实执行前删除伪串行和重复层；Virtual-99 是结构收敛，不是第二评分指标。

## E=(C,P,S,V)

C：TypeScript deterministic binder + Ajv standalone + speculative-policy compiler。
P：固定 jev-1.13.0；Choice-first；独立问题同 model barrier 并行。
S：in-process finite-state reducer；immutable receipts；per-dependency unlock。
V：独立 preloaded harness；private oracle；strict compare；SHA-256。

## 当前物理量

任务仍为 PE-P0-GENERAL-01，业务语义未改。

```text
SEMANTIC_FINAL_DECISIONS=24
SPECULATIVE_POLICY_BRANCHES=12
V99_MODEL_QUESTION_COUNT=32
MODEL_BARRIER_DEPTH_MIN=1
ACTION_DEPENDENCY_DEPTH_MIN=2
FINAL_VERIFY_BARRIERS_MIN=1
```

v0.1.0 的 D_MIN=2 / JEV_ROUNDS_MIN=2 被发现混淆 model dependency 与 action dependency，已被 0.2.0 更精确的 barrier 模型取代，但历史永久保留。

21–24 可以提前对 predecessor 的 SUCCESS / FAIL_TEMP / FAIL_PERM 三种结果求 conditional Choice；真实 receipt 到达以后只选择预计算分支，最终动作仍必须 receipt 后提交。

## 关键路径规则

最少 serial barriers + 最大合法 overlap。
节点总数 N 不是唯一物理目标。
不能因为动作有两层就推导模型必须两轮。
同一 model barrier 可以一个 batch 或多个 concurrent shards；现实最快拓扑由 Step 3 同门槛实测。

## 状态

Step 1：任务、COMMERCIAL_GATE、T0/T1 已冻结。
Step 2：MATURE_CLUSTER=FROZEN_V0.2；VIRTUAL_99_STRUCTURAL=PASS。
Step 3：未运行。T_REAL* / T_P0 尚未测量，REAL_CERTIFIED=NO。

## 读取顺序

CURRENT_STATE.md
HISTORY.md
TASK_CONTRACT.md
PHYSICAL_LIMIT.md
MATURE_CLUSTER.md
VIRTUAL_99.md
UPDATE_PROTOCOL.md

禁止覆盖旧历史；发现新成熟结构、伪依赖、Jev/Provider 或现实环境变化，按 UPDATE_PROTOCOL 产生新版本。


## 现实认证

2026-09-21，v0.2.2 reality command 完成首轮真实运行：

```text
SWEEP_s1/s2/s4/s8=ALL_PASS
SWEEP_WINNER_SHARDS=2
CONFIRM_s2=30/30_PASS
COMMERCIAL_GATE_SERIES=PASS
T_REAL_STAR_MS=840.6046999999962
T_P0_MS=840.6046999999962
REAL_CERTIFIED=YES
```

840.605 ms 是当前固定现实环境下的已认证最短有效观测值，不是永久物理常数。模型、Provider、网络、机器、代理、action backend 或 verifier 改变时必须按 UPDATE_PROTOCOL 重测。
