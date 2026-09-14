# P0 E5 PERSISTENT_WEBSOCKET_ACROSS_RUNS
- Baseline 32.55975 ms / P95 58.1779 ms。
- 假设：每轮 WebSocket 生命周期造成 RESULT 开销；收益上限 1.0 ms。
- 单变量：23 runs 共用一个 WebSocket；prompt 事件关联、history、/view、PNG 完整验证均不变。
- Warmup 3/3；Measured 20/20；输出 23/23 PASS。
- Candidate Median 35.57205 ms；P95 38.2483 ms。
- Median improvement -9.2516%；P95 improvement 34.2563%。
- Decision ROLLBACK：Median 退化超过2%。
- Next E6 HISTORY_ON_EXECUTION_SUCCESS。
