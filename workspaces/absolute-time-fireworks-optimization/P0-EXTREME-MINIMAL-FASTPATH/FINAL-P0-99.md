# P0 99 最终冻结

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

## Certification

- Profile：P0-99-CERTIFICATION-V1
- 40/40 valid
- P95：16.724915 ms
- A/A effect：0.58054 ms
- A/A 95% CI：[-0.247058, 1.408138] ms
- Equivalence：[-2, 2] ms
- Label leak：0/0/0
- Disk write in critical path：NO
- Evidence：certification-20260915-193531/results.json

## 最终时间账

- REQUEST_MS=4.8033
- QUEUE_MS=5.0928
- EXECUTE_MS=0.32975
- RESULT_MS=1.87085

观测下界来自完整有效运行 min=10.4729 ms。冻结中位数与下界之间 2.2053 ms
主要由必要 loopback request、ComfyUI 条件队列/线程调度和客户端完整 decode 的运行波动解释。

## 冻结实现

- runner：run.py
- output node：p0_cached_png_websocket.py
- certifier：certify.py
- profile：CERTIFICATION-PROFILE.md

重新打开条件：出现保留安全验证、可证明至少节省 1 ms 的低风险方案，或硬件/runtime/固定任务改变。
