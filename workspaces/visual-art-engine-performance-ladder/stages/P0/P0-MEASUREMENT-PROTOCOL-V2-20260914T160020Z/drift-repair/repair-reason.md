# Drift analyzer repair reason

原分析器把 early-vs-late、Theil–Sen span 和 pattern effect 三者的最大绝对值直接与 MDE 比较，混淆了趋势幅度、随机分组差异和方向证据。它导致两批 CI 含 0 的 A/A 被单个摘要值否决。

修复后环境漂移要求 Theil–Sen 预测幅度超过 MDE 且时间顺序置换检验 p<0.05。Order effect 不再因 p>0.05 自动 PASS，而使用独立 block contrast 的 bootstrap 等价性 CI 三态判定。旧批次保持原状态，不回写。
