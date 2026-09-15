# 重大失败经验：把测量工程当成主优化循环

`MAJOR_FAILURE_CASE=MEASUREMENT_ENGINEERING_AS_PRIMARY_OPTIMIZATION_LOOP`

中文解释：把 Measurement Engineering（测量工程）当作主要性能优化循环。

## 为什么当初看起来合理

A/A（同实现校准）、MDE（最小可检测效应）、order effect（顺序效应）、drift（漂移）与 paired statistics（配对统计）能够提高比较可信度，所以容易被误当成寻找主要优化方向的方法。

## 最终为什么失败

- 大量迭代用于证明尺子，而不是删除真实关键路径。
- 绝对 `T_END_TO_END` 没有持续下降，多次产生比冻结基线更差的绝对结果。
- 原接续资料将一类退化记为约 `3141 ms`；旧 v1.0 摘要写作约 `31–41 ms`。两份原文均保留，不伪造二者等价关系。
- 过度关注 A/A、MDE、order effect、drift、relative effect（相对效应）与复杂 Measurement V2 evidence（证据）。
- 环境和统计解释遮蔽了 file-backed output 这一约 10 ms 的物理大块。

## 后来什么真正成功

回到第一性原理四列法 V4.0 的宏观工程迭代：

`32.55975 ms → 21.9215 ms → 12.6782 ms`

总提升 `61.0617403%`。第一轮通过删除 file-backed output / publish / reopen，真实结果 `21.9215 ms` 与事前物理模拟约 `21.97–22.30 ms` 高度一致。

## 以后直接走

先调用 `absolute-time-fireworks-optimization`，执行物理时间账、最大 gap、单变量真实结果与 KEEP（保留）/ROLLBACK（回滚）。只有明显更快的最终 candidate（候选）形成后，才调用 `performance-benchmark-convergence` 做 CERTIFICATION（最终认证）。

# 测量工程不能替代性能工程。

旧 `performance-benchmark-convergence`、Measurement V2 报告与原始证据全部保留，不删除、不改写；它们作为重大失败证据与最终认证工具，默认不进入优化主循环。
