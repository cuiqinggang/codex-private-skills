# FAST PATH

## WHAT_TO_DO_FIRST

1. 固定 TASK、成功条件、输入输出、质量底线和 T_START/T_END。
2. 冻结当前真实 best 与可恢复实现。
3. 把非任务必需动作移到 RESULT_READY 后。
4. 建立最小 runner，只保留 REQUEST、QUEUE、EXECUTE、FINAL BYTES、最低验证。
5. 运行 2 warmup + 5 measured；只看真实绝对 P50/P95、有效性和 KEEP/ROLLBACK。

## 时间账

只拆 REQUEST_MS / QUEUE_MS / EXECUTE_MS / RESULT_MS。最大块再细分。每个候选先填：

    CURRENT_BEST_MS=
    TARGET_BLOCK=
    CURRENT_BLOCK_MS=
    PHYSICAL_REQUIRED_MS=
    REMOVABLE_MS=
    OVERLAPPABLE_MS=
    EXPECTED_GAIN_MS=
    EXPECTED_NEW_TOTAL_MS=
    IMPLEMENTATION_COST=

一次只改一个主要变量。若预计小于 1 ms，停止；优先至少 2 ms。

## 最低验证

- 自己提交并匹配的 prompt identity；
- success completion；
- 最终 PNG bytes；
- PNG 格式、256×256、完整 decode；
- 必要结果身份确认。

同一语义不要重复 decode、hash、history fetch 或文件 reopen。

## 裁决

    PREVIOUS_BEST_MS=
    NEW_P50_MS=
    NEW_P95_MS=
    ABSOLUTE_GAIN_MS=
    IMPROVEMENT_PERCENT=
    VALID=5/5
    KEEP_OR_ROLLBACK=

明显更快才 KEEP；否则立即回滚并检查目标路径是否仍存在、新同步点、重复 encode/copy
或新增等待。不要扩大统计。

## 99 / FREEZE

当不存在可行、低风险、预计至少 1 ms 的候选，剩余时间能由必要 IPC、队列、执行、
内存编码/传输、最低验证和 OS 调度解释时，进入最终 certification。冻结报告必须给出：

FINAL_P0_99_TIME_MS / REALITY_FLOOR_MS / PHYSICAL_GAP_MS /
LARGEST_REMAINING_REMOVABLE_BLOCK_MS / P0_99 / P0_FREEZE。

## WHAT_NOT_TO_DO

- 不以 Measurement engineering 代替性能工程。
- 不让 evidence、Git、日志或知识同步进入计时段。
- 不把启动耗时误当稳态关键路径。
- 不同时改两个主要变量。
- 不为卡死检测给毫秒路径添加 watchdog/polling。
- 不扫描 H/K；K 只在用户明确批准具体备份时使用。
