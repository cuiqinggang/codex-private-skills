# P0 E4 MINIMAL_DEFER_WEBSOCKET_CLOSE

- Baseline 32.55975 ms / P95 58.1779 ms。
- 单一假设：WebSocket close 是 RESULT 内可移出的清理，收益上限 1.0 ms。
- 修改：仅从 baseline runner 将 ws.close 移到 RESULT_READY 后；合同兼容。
- Warmup 3/3；Measured 20/20；23/23 输出有效。
- Candidate median 34.0632 ms；P95 39.9397 ms。
- Median improvement -4.6175%；P95 improvement 31.349%。
- Decision ROLLBACK：P95 虽改善超过20%，但 Median 退化超过2%。
- Baseline 保持 32.55975 ms。
- Next E5 PERSISTENT_WEBSOCKET_ACROSS_RUNS。
