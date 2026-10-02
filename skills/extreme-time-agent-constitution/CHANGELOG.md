# CHANGELOG

## v0.3.1 — 2026-10-02 — FROZEN

Freeze ID: `ETAC-v0.3.1-FREEZE-R1`  
Supersedes: `ETAC-v0.3-FREEZE-R1`

核心变化：
- 删除“禁止自研逃生 / NO_NEW_IMPLEMENTATION_ESCAPE”这一不清晰且过于绝对的表述；
- 将规则改为“成熟能力优先，但不把实现方式写死”；
- 暂时没找到成熟方案时先重定义、重映射、重检索；
- 如果现实证据证明现成方案不够快、不可达或不能满足 VALID，允许最小必要实现；
- 所有候选继续按同一 `VALID → 完整 T_VALID` 标准竞争；
- 保留 `CHANGE_SCOPE=ROOT_CAUSE_SCOPE`、删除非必要复杂度、最低充分智能资源原则。

说明：v0.3.1 宪法冻结不等于具体项目 Freeze。

## v0.3.0 — 2026-10-01 — SUPERSEDED

Freeze ID: `ETAC-v0.3-FREEZE-R1`

历史贡献：
- 强化成熟能力优先；
- 强调先重定义、重映射和重检索；
- 继续保留 `T*=min(T_VALID)`。

被 v0.3.1 替代原因：
- “禁止自研逃生”容易造成误解，并把实现策略写得过于绝对。

## v0.2.0 — 2026-10-01 — SUPERSEDED

Freeze ID: `ETAC-v0.2-FREEZE-R1`

历史贡献：
- 单一端到端 `T*=min(T_VALID)`；
- 成熟完整方案优先；
- `CHANGE_SCOPE=ROOT_CAUSE_SCOPE`；
- 实现层与普适宪法分离。
