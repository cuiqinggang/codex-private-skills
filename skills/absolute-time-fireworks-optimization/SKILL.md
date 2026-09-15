---
name: absolute-time-fireworks-optimization
description: Minimize real end-to-end time for a fixed task by removing the largest physical critical-path block, building a minimal fast path, and keeping only absolute wins. Use for 极限时间、T_END_TO_END、物理时间账、最大 gap、90→99、P0 99/FREEZE；do not use it as a certification-only statistics workflow.
metadata:
  version: "1.0.0"
  short-description: 极限时间烟花优化法
---

# 极限时间烟花优化法

固定任务合同后，唯一优化目标是最小化真实 T_END_TO_END。默认先读
[FAST PATH](references/FAST-PATH.md)，不要先读历史。

## 核心循环

冻结 current best → 脱重甲 → REQUEST/QUEUE/EXECUTE/RESULT 时间账 → 最大现实可消除块
→ 单变量实现 → 2 warmup + 5 measured → 绝对更快 KEEP，否则 ROLLBACK → 重新分解。

- 先用物理/软件因果链说明将删除哪个同步步骤、encode、copy、I/O 或等待。
- 预计收益小于 1 ms 时不做；优先攻击至少 2 ms 的低风险块。
- 物理模型预计明显收益却未兑现时，先检查实现是否真正删除目标路径。
- 不用 drift、MDE 或更多统计解释一个未变快的优化。
- 日志、证据、Git、Knowledge Brain 和技能更新全部放在 RESULT_READY 后。
- 核心链不放 watchdog、poll loop、monitor、profiling、tracing 或同步写盘。

## 完成门禁

只有固定任务、最低结果验证、简单复跑、剩余时间账与最终 certification 都成立时，
才能输出 P0_99=YES 和 P0_FREEZE=YES。最终验收阶段才读取并调用
performance-benchmark-convergence；它不得成为优化主循环。

## 按需读取

- 正常优化：只读 [FAST PATH](references/FAST-PATH.md)。
- 遇到异常：再读 [FAILURE INDEX](references/FAILURE-INDEX.md)。
- 需要案例数字或物理原因：读 [P0 成功案例](references/CASE-P0-20260915.md)。
- 有人建议先做复杂 Measurement：读
  [重大失败索引](references/MAJOR-FAILURE-MEASUREMENT-FIRST.md)。
- 每解决一个新坑，阶段结束时按 Failure Index 格式追加；不得污染计时路径。

最近使用记录见 [USAGE-LOG](USAGE-LOG.md)，部署验收见
[ACCEPTANCE](ACCEPTANCE.html)。
