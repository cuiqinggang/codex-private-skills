# P0-EXTREME-MINIMAL-FASTPATH

这是 P0 99 冻结工程。性能实现已冻结；不要为了文档整理修改 `run.py`、`p0_cached_png_websocket.py`、`certify.py` 或认证 JSON。

## 第一屏

```text
INITIAL_BEST_MS=32.55975
POST_MACRO_R1_MS=21.9215
FINAL_P0_99_TIME_MS=12.6782
TOTAL_IMPROVEMENT_PERCENT=61.0617403%
LARGEST_REMAINING_REMOVABLE_BLOCK_MS=<0.5
REALITY_FLOOR_MS=10.4729
PHYSICAL_GAP_MS=2.2053
MACRO_SCORE=99
P0_99=YES
P0_FREEZE=YES
```

## 入口

- 冻结报告：`FINAL-P0-99.md`
- runner：`run.py`
- server node / adapter：`p0_cached_png_websocket.py`
- certifier：`certify.py`
- 原始认证：`certification-20260915-193531/results.json`
- workflow：`workflow/fixed-workflow.json`
- 启动配置：`runtime/START_COMFYUI_C_DRIVE_OUTPUT_D.ps1`
- fixture：`fixtures/`
- 复现说明：`REPRODUCTION.md`
- 完整哈希清单：`MANIFEST.json`

本轮收口没有重新运行 benchmark，也没有修改冻结性能代码。
