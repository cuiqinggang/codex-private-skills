# P0 Convergence Ledger

固定合同：P0-CONTROL-V1；方法：mature-replication-four-column V4.0；起始正式基线：32.55975 ms，P95 58.1779 ms。

| 实验 | 假设 | 理论收益上限 | 实际结果 | 决策 | 原因 | 下一影响 |
|---|---|---:|---|---|---|---|
| E1 RESULT_PATH_DECOMPOSITION | RESULT 含可分解客户端延迟 | 16.99775 ms | 观测中位 36.74075 ms；OUTPUT_VISIBLE→CLIENT 13.25845 ms | OBSERVATION_ONLY | 增加观测点，不竞争基线 | E2 对比本地读取与 /view |
| E2 LOCAL_OUTPUT_FILE_READ_VS_HTTP_VIEW | /view 是 13.25845 ms 主因 | 13.25845 ms | 3/3、20/20；总中位 35.6235 ms；本地取得 8.79895 ms | DIAGNOSTIC_ONLY | 本地读违反冻结合同的 HTTP 取得语义 | E3 延后 WebSocket close，保持 /view |
| E3 DEFER_WEBSOCKET_CLOSE | WS close 约 1ms 可移出 RESULT | 1.0 ms | 3/3、20/20；中位 39.73105 ms；P95 47.4519 ms | ROLLBACK | 未改善且携带 E1 观测负担 | E4 用 baseline runner 重测最小变量 |
| E4 MINIMAL_DEFER_WS_CLOSE | close 可移出正式边界 | 1.0 ms | 3/3、20/20；Median 34.0632，P95 39.9397 | ROLLBACK | Median 退化超2% | E5 跨 run 持久 WebSocket |
| E5 PERSISTENT_WEBSOCKET | 跨 run 复用 WS 可降低连接生命周期 | 1.0 ms | 3/3、20/20；Median 35.57205，P95 38.2483 | ROLLBACK | Median 退化超2% | E6 execution_success 触发 history |
