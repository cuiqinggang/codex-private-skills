# CHANGELOG

## 0.2.0 — 2026-09-21

Added:
- C/P/S/V 成熟方案集群。
- Core② Virtual-99 结构冻结。
- speculative policy compilation。
- 机器可读 schedule proof。

Changed:
- 废弃 bare D_MIN 同时代表概率与动作深度。
- MODEL_BARRIER_DEPTH_MIN=1。
- ACTION_DEPENDENCY_DEPTH_MIN=2。
- v0.1.0 JEV_ROUNDS_MIN=2 标记 superseded。
- T_PHY 改为一个 model barrier + 两层 action chain 的最大值结构。
- TASK_CONTRACT 升为 v1.1 clarification：允许 receipt 前计算 conditional policy；dependent final action 仍必须 receipt 后提交。
- Jev 基准固定 versioned model jev-1.13.0；Provider/transport/sharding 留给现实锚定。

Reality:
MATURE_CLUSTER=FROZEN_V0.2
VIRTUAL_99_STRUCTURAL=PASS
T_REAL*=NOT_MEASURED
T_P0=NOT_MEASURED
REAL_CERTIFIED=NO

## 0.1.0 — 2026-09-21

首次建立长期技能包并冻结 Step-1。旧 D_MIN=2/JEV_ROUNDS_MIN=2 作为历史保留，由 0.2.0 更精确 barrier 模型取代。
