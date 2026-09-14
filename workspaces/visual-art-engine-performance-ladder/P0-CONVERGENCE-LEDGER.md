# P0 Convergence Ledger

固定合同：P0-CONTROL-V1；方法：mature-replication-four-column V4.0；起始正式基线：32.55975 ms，P95 58.1779 ms。

| 实验 | 假设 | 理论收益上限 | 实际结果 | 决策 | 原因 | 下一影响 |
|---|---|---:|---|---|---|---|
| E1 RESULT_PATH_DECOMPOSITION | RESULT 含可分解客户端延迟 | 16.99775 ms | 观测中位 36.74075 ms；OUTPUT_VISIBLE→CLIENT 13.25845 ms | OBSERVATION_ONLY | 增加观测点，不竞争基线 | E2 对比本地读取与 /view |
| E2 LOCAL_OUTPUT_FILE_READ_VS_HTTP_VIEW | /view 是 13.25845 ms 主因 | 13.25845 ms | 3/3、20/20；总中位 35.6235 ms；本地取得 8.79895 ms | DIAGNOSTIC_ONLY | 本地读违反冻结合同的 HTTP 取得语义 | E3 延后 WebSocket close，保持 /view |
| E3 DEFER_WEBSOCKET_CLOSE | WS close 约 1ms 可移出 RESULT | 1.0 ms | 3/3、20/20；中位 39.73105 ms；P95 47.4519 ms | ROLLBACK | 未改善且携带 E1 观测负担 | E4 用 baseline runner 重测最小变量 |
| E4 MINIMAL_DEFER_WS_CLOSE | close 可移出正式边界 | 1.0 ms | 3/3、20/20；Median 34.0632，P95 39.9397 | ROLLBACK | Median 退化超2% | E5 跨 run 持久 WebSocket |
| E5 PERSISTENT_WEBSOCKET | 跨 run 复用 WS 可降低连接生命周期 | 1.0 ms | 3/3、20/20；Median 35.57205，P95 38.2483 | ROLLBACK | Median 退化超2% | E6 execution_success 触发 history |
| E6 HISTORY_ON_EXECUTION_SUCCESS | success 可提前 history | 7.5893 ms P95 | warmup-01 history missing；measured 未执行 | ROLLBACK / INVALID | success 早于 history 可见 | E7 缓冲 raw event 写盘 |
| E7 BUFFER_RAW_EVENT_WRITES | 同步 flush 属测量开销 | 6.0 ms | 3/3、20/20；Median 42.34235，P95 54.0572 | ROLLBACK | 无稳定改善 | E8 精确 baseline 重现控制 |
| E8 BASELINE_REPRO_CONTROL_A | 检查正式基线可复现性 | N/A | 3/3、20/20；Median 39.15，P95 49.4881 | CONTROL_FAIL_REPRO | 未复现32.55975 | 控制批次B |
| E9 BASELINE_REPRO_CONTROL_B | 第二独立控制批次 | N/A | 3/3、20/20；Median 30.0504，P95 36.6619 | CONTROL_PASS | 成功复现但批间抖动大 | 控制批次C |
| E10 BASELINE_REPRO_CONTROL_C | 第三独立控制批次 | N/A | 3/3、20/20；Median 33.20215，P95 40.2249 | CONTROL_PASS | 基线可复现但批间抖动显著 | R4 Load/Save 分解 |
| E11 BASELINE_REPRO_CONTROL_D | 第四控制/最终确认第三批 | N/A | 3/3、20/20；Median 35.60995，P95 42.9792 | CONTROL_PASS | B/C/D 三批均有效 | R1-R8 最终审核 |
