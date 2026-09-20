# HISTORY — 方法收敛过程

旧版本不删除。

## H1–H9

简单任务 → 节点可简单、任务图可复杂。
多指标 → COMMERCIAL_GATE 内只优化 min T_E2E。
节点数量 N → 关键路径/串行屏障。
同题重复 → 独立证据、状态约束、现实反馈、verifier。
逐行业案例库 → E=(C,P,S,V)。
先开发再找任务 → 任务就是测功机。
Jev latency → 完整 T_E2E。
历史基础设施成本与本次现场时间分开。
“99 分” → 逼近物理/现实极限的收敛状态。

## H10 — 0.1.0

首次冻结 PE-P0-GENERAL-01、COMMERCIAL_GATE、T0/T1 与旧链路：
P1 → A1/receipts → P2 → A2 → Verify。
当时写为 D_MIN=2 与 JEV_ROUNDS_MIN=2。

## H11 — 0.2.0 根本纠偏

成熟 TypeSafe pattern 明确：只有第二请求在第一结果前根本无法构造时才是真模型依赖；否则应 speculative fan-out。

21–24 的真实动作确实等待 17–20 receipt，但有限 receipt 状态空间可预先做条件策略计算。因此：

动作依赖 ≠ 模型依赖。

从 0.2.0 起分别记录：
MODEL_BARRIER_DEPTH_MIN=1
ACTION_DEPENDENCY_DEPTH_MIN=2

0.1.0 JEV_ROUNDS_MIN=2 被 supersede，但原历史不删除。

## H12 — 0.2.0 成熟集群

C：TypeScript deterministic binder + Ajv standalone。
P：pinned jev-1.13.0 + speculative fan-out。
S：in-process finite-state reducer + immutable receipts + per-dependency unlock。
V：independent preloaded harness + private oracle + strict compare + SHA-256。

Virtual-99 删除固定 post-receipt Jev round、全局 wait-all、生成式 planner、runtime schema compile、无条件重采样和 LLM verifier。
