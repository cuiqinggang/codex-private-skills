# AGENTS.md 补丁草案

> 草案；不自动覆盖现有 AGENTS.md。

## 极限时间性能项目

- 触发：极限时间、T_END_TO_END、物理时间账、P0 99、烟花优化。
- 开工先调用 C:\Users\A\.codex\skills\absolute-time-fireworks-optimization。
- 默认只读 SKILL.md 与 references/FAST-PATH.md；异常才读 FAILURE-INDEX.md。
- 主循环只做最大物理 gap、单变量、2 warmup + 5 measured、KEEP/ROLLBACK。
- 所有证据、Git、Knowledge Brain、技能更新在 RESULT_READY 或阶段结束后进行。
- 只有最终候选形成后才调用 performance-benchmark-convergence 做 certification。
- 每个已解决新坑在阶段结束时追加到 Failure Index；同一个坑不得完整探索第二次。
