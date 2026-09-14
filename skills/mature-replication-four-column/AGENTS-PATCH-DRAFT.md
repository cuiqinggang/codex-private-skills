# AGENTS.md 补丁草案：第一性原理四列法 V4.0

> 合并到目标项目的 `AGENTS.md` 前先审阅；本草案不授权覆盖既有规则。

当任务涉及性能优化、成熟方案复刻、阶段性 99 分、新增能力或数量级时间退化时，使用 `mature-replication-four-column` V4.0。

先固定 TASK：目标、成功条件、输入输出、必须保留能力、不可删除步骤、安全、稳定性和质量底线。任务固定后只优化 `T_END_TO_END`；通过删要求、缩范围、跳过必要验证或降质量获得的时间标为 `INVALID_RESULT`。

按顺序记录四列：`CURRENT`（当前实测时间）、`EXTERNAL FRONTIER`（现实已证明的可比前沿）、`FIRST-PRINCIPLES PHYSICAL TIME`（从不可避免物理步骤推导的 `T_PHY`/范围）、`ITERATIVE CONVERGENCE`（一次一个局部假设，实测后保留或回滚）。成熟方案是证据和路径参考，不是终极参照。

99 仅表示当前环境和已知可验证方法下已无显著稳定的可行收益；仍须记录 `PHYSICAL_GAP`。存在显著更快且真正可比的外部结果时不得封 99。新增能力必须记录 `ΔT`；数量级退化先判 `PATH_ARCHITECTURE_ERROR`，不得把时间崩塌接受为新常态。
