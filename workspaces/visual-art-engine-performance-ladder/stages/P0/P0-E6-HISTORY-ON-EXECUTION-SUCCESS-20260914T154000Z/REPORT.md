# P0 E6 HISTORY_ON_EXECUTION_SUCCESS
- 假设：execution_success 可提前约 1.3741 ms 触发 history，尾部收益上限 7.5893 ms。
- 唯一变量：在 execution_success 后立即进入既有 history 请求。
- Warmup: 0/3 valid；第1次出现 matching history entry is missing。
- Measured: 0/20，按合同未启动。
- TIME=INVALID_RESULT；Decision=ROLLBACK。
- 结论：execution_success 不能冒充 history/task_done 可见性，必须保留更晚的可靠完成边界。
- Baseline 保持 32.55975 ms。
- Next E7 BUFFER_RAW_EVENT_WRITES_AFTER_TIMING。
