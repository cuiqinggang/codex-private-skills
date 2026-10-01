# CHANGELOG

## v0.3.0 — 2026-10-01 — FROZEN

Freeze ID: `ETAC-v0.3-FREEZE-R1`  
Supersedes: `ETAC-v0.2-FREEZE-R1`

核心变化：
- 删除“前述成熟方案均不能满足 VALID 时才考虑新增实现”这一出口；
- 将 `MATURE_SOLUTION_EXISTS=TRUE` 从检索工作假设提升为当前任务域固定前提；
- 新增 `NO_NEW_IMPLEMENTATION_ESCAPE=TRUE`；
- 候选空间限定为现有成熟方案、成熟配置、成熟接口和成熟组件最小组合；
- 成熟方案采用后继续攻击对完整 `T_VALID` 有现实收益的瓶颈；
- 优化必须优先使用成熟替代、配置、接口、并行、缓存、恢复等已有成熟能力；
- 继续保留 `CHANGE_SCOPE=ROOT_CAUSE_SCOPE`、删除非必要复杂度和最低充分智能资源原则。

说明：v0.3 宪法冻结不等于具体项目 Freeze。

## v0.2.0 — 2026-10-01 — SUPERSEDED

Freeze ID: `ETAC-v0.2-FREEZE-R1`

历史贡献：
- 单一端到端 `T*=min(T_VALID)`；
- 成熟完整方案优先；
- `CHANGE_SCOPE=ROOT_CAUSE_SCOPE`；
- 实现层与普适宪法分离。

被 v0.3 替代原因：
- v0.2 仍保留“最终考虑新增实现”的出口，与当前成熟解固定前提不一致。
