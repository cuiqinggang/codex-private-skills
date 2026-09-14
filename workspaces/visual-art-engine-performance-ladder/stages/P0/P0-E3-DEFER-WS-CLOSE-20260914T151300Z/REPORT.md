# P0 E3 DEFER_WEBSOCKET_CLOSE_AFTER_RESULT_READY

- Baseline: 32.55975 ms; P95 58.1779 ms
- Hypothesis: WebSocket close 位于 RESULT 内，延后清理可降低正式时间。
- Gain ceiling: 1.0 ms
- Single variable: 延后 WebSocket close；合同兼容。
- Warmup 3/3；Measured 20/20；输出验证 23/23 PASS。
- Candidate median: 39.73105 ms；P95: 47.4519 ms。
- Decision: ROLLBACK。
- Reason: Median 未改善；且该 runner 继承 E1 观测负担，不适合作为最小 A/B。
- Baseline remains 32.55975 ms。
- Next: E4 从正式 baseline runner 做最小 defer-close 单变量。
