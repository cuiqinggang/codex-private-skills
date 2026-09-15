# 材料价值与可执行经验

## 材料来源

- 来源：用户 2026-09-15 提供的 P0 极限时间接续说明与基础总则。
- 活跃项目：C:\Users\A\Documents\Codex\P0-EXTREME-MINIMAL-FASTPATH。

## 价值判断

结论：HIGH_VALUE。

满足：减少重复犯错、提升复杂任务质量、形成规则/SOP/checklist/template、改善长期工作流、转为自动开工检查，且用户明确要求长期部署和不落灰。

## 可执行内容

- 规则：Measurement engineering 不得替代 performance engineering。
- SOP：物理时间账、最大 gap、单变量、2+5、KEEP/ROLLBACK、重新分解、最终认证。
- Checklist：FAST-PATH.md。
- Template：候选时间账与第一屏裁决字段。
- AGENTS patch：AGENTS-PATCH-DRAFT.md。
- 失败入口：FAILURE-INDEX.md。
- 验收：ACCEPTANCE.html 与 P0 certification JSON。

## 防落灰绑定

- 触发：极限时间、T_END_TO_END、物理时间账、最大 gap、P0 99、烟花法。
- 开工动作：只读 SKILL.md 与 FAST-PATH.md；异常才读 Failure Index。
- 最近使用：USAGE-LOG.md。
- 下一次：先调用本技能；最终候选出现后才调用 performance-benchmark-convergence。
