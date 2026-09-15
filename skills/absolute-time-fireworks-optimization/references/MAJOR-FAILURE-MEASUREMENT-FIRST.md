# MAJOR FAILURE REFERENCE

MAJOR_FAILURE_CASE=MEASUREMENT_ENGINEERING_AS_PRIMARY_OPTIMIZATION_LOOP

## 为什么当初看起来合理

A/A、MDE、order effect、drift、paired statistics 能提高比较可信度。

## 为什么作为主路线失败

- 大量迭代用于证明尺子，而非删除真实关键路径。
- 绝对 T_END_TO_END 没有持续下降，出现过约 31–41 ms 的更差结果。
- 相对效应与环境解释遮蔽了 file-backed output 这一约 10 ms 的物理大块。

## 真正成功的方法

回到物理关键路径后，删除 file-backed output / publish / reopen，一轮把
32.55975 ms 降到 21.9215 ms；再脱 history/double-decode 重甲并缓存固定输出
encode，最终认证中位数为 12.6782 ms。

## 以后直接走

先调用 absolute-time-fireworks-optimization。只有出现明显更快的最终 candidate 后，
才调用 performance-benchmark-convergence 做 certification。

旧技能和原始证据保留，不删除、不改写；默认不进入新项目运行路径。
