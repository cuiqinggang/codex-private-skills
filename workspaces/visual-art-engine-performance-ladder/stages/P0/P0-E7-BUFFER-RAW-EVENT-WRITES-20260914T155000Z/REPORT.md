# P0 E7 BUFFER_RAW_EVENT_WRITES_AFTER_TIMING
- 假设：正式计时内同步事件写盘/flush 是测量开销；收益上限估计 6 ms。
- 单变量：保留全部事件和 monotonic 时间戳，run 后批量落盘。
- Warmup 3/3；Measured 20/20；输出 23/23 PASS。
- Candidate Median 42.34235 ms；P95 54.0572 ms。
- Decision ROLLBACK：Median 未改善。
- Baseline 32.55975 ms 保持。
- Next E8 EXACT_BASELINE_REPRODUCTION_CONTROL。
