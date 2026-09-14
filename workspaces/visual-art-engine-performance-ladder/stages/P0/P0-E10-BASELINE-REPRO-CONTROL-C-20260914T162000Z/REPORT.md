# P0 E10 EXACT_BASELINE_REPRODUCTION_CONTROL_C
- 未修改 baseline runner。
- Warmup 3/3；Measured 20/20；输出 23/23 PASS。
- Median 33.20215 ms；P95 40.2249 ms；MIN 29.939；MAX 40.3413。
- 三控制批次 Median：39.15 / 30.0504 / 33.20215 ms。
- 基线可复现，但批间抖动主要分布于 RESULT，其次 REQUEST/QUEUE；不向上或向下替换正式32.55975ms。
- Next：R4 LOAD_SAVE_DECOMPOSITION。
