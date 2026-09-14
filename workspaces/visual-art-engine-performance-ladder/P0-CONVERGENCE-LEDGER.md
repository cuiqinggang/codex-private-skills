# P0 Convergence Ledger

固定合同：P0-CONTROL-V1；方法：mature-replication-four-column V4.0；起始正式基线：32.55975 ms，P95 58.1779 ms。

| 实验 | 假设 | 理论收益上限 | 实际结果 | 决策 | 原因 | 下一影响 |
|---|---|---:|---|---|---|---|
| E1 RESULT_PATH_DECOMPOSITION | RESULT 含可分解客户端延迟 | 16.99775 ms | 观测中位 36.74075 ms；OUTPUT_VISIBLE→CLIENT 13.25845 ms | OBSERVATION_ONLY | 增加观测点，不竞争基线 | E2 对比本地读取与 /view |
| E2 LOCAL_OUTPUT_FILE_READ_VS_HTTP_VIEW | /view 是 13.25845 ms 主因 | 13.25845 ms | 3/3、20/20；总中位 35.6235 ms；本地取得 8.79895 ms | DIAGNOSTIC_ONLY | 本地读违反冻结合同的 HTTP 取得语义 | E3 延后 WebSocket close，保持 /view |
