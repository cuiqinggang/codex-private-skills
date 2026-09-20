# PHYSICAL LIMIT — v0.2.0

## v0.1.0 的结构纠偏

v0.1.0 因 21–24 必须等待 17–20 的真实 receipt，把 D_MIN=2 与 JEV_ROUNDS_MIN=2 一起冻结。

Core② / Virtual-99 证明：这只能证明现实动作依赖深度为 2，不能证明 Jev 模型屏障必须为 2。有限 receipt 状态可以提前 speculative policy evaluation，真实 receipt 只负责选择已经得到的分支。

从 0.2.0 起废弃裸 D_MIN 同时表达两类深度。

## 修正后的结构量

```text
SEMANTIC_FINAL_DECISIONS=24
SPECULATIVE_POLICY_BRANCHES=12
V99_MODEL_QUESTION_COUNT=32

MODEL_BARRIER_DEPTH_MIN=1
ACTION_DEPENDENCY_DEPTH_MIN=2
FINAL_VERIFY_BARRIERS_MIN=1
```

01–20：20 个当前动作 Choice。
21–24：对 predecessor EXECUTE 的三个真实结果 SUCCESS / FAIL_TEMP / FAIL_PERM，各提前生成一个直接条件 Choice，共 12 个 conditional-policy Choice。

这些语义问题可在同一个 model barrier 中完成。它可以是一个大 batch，也可以是多个 concurrent shard；实际最快拓扑留给 Step 3 实测。

21–24 的真实动作仍只能在对应 receipt 后提交，因此 ACTION_DEPENDENCY_DEPTH_MIN=2 不变。

## Virtual-99 DAG

T0
→ BIND: parse + standalone schema validate + dependency bind + question build
→ J_SPEC: all current-action + conditional-policy semantic judgments
→ A01..A20 parallel
   A17→receipt17→policy lookup→A21
   A18→receipt18→policy lookup→A22
   A19→receipt19→policy lookup→A23
   A20→receipt20→policy lookup→A24
→ V: one final independent verifier barrier
→ OUT: manifest/commit
→ T1

不存在物理必需的 receipt → Jev network round → dependent action。

## T_PHY v2

`T_PHY_v2 = t_bind* + t_Jspec* + max(max(first-wave-only paths), max_{j=17..20}(t_Aj* + t_Adep(j)*)) + t_Vtail* + t_out*`

局部验证、增量 hash、日志整理若可与 action 并行，不得重复串行相加。

T_PHY_V2_FORMULA=DERIVED
T_PHY_NUMERIC=REQUIRES_REALITY_CONSTANTS
T_REAL_STAR=NOT_MEASURED
T_P0=NOT_MEASURED
