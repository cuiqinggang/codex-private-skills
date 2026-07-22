# 07 五轴独立审查

必须分别执行：

A. Spec Compliance Review：逐条核对规格与用户行为。
B. Engineering Standards Review：核对仓库规范、可维护性和测试。
C. Safety Boundary Review：确认未触碰禁止资产、Git 或全局配置。
D. Runtime Evidence Review：检查命令、日志和实际运行结果。
E. Delivery Completeness Review：检查文件、文档、回滚与证据是否齐全。

每轴独立记录 findings，再汇总到 templates/CODE_REVIEW.md。只读报告不能直接宣布最终 PASS；运行 gates/REVIEW_GATE.md 后交回上层 Verification Plane。
