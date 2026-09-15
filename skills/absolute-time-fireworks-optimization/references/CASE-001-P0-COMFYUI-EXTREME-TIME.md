# CASE-001：P0 ComfyUI 极限时间

## 冻结结果

```text
INITIAL=32.55975 ms
MACRO_R1=21.9215 ms
FINAL=12.6782 ms
OBSERVED_REALITY_FLOOR=10.4729 ms
TOTAL_GAIN=19.88155 ms
TOTAL_IMPROVEMENT=61.0617403%
P95=16.724915 ms
VALID=40/40
AA_95CI=[-0.247058,1.408138] ms
```

正式措辞是 `OBSERVED_REALITY_FLOOR（观测现实下界）=10.4729 ms`：真实 40-run 中实际出现过该完整有效时间。它不是数学证明的绝对物理极限。任何早期 `10–20 ms` 范围只属于 `HISTORICAL MODEL / ESTIMATE（历史模型/估算）`。

## 为什么 CASE-001 重要

P0 的意义不只是让一个 ComfyUI 脚本变快。它第一次用真实工程数据证明：固定 `TASK_COMPLETED` 后，把时间作为唯一优化指标，用第一性原理持续删除非必要路径，能够把一个已经工作的系统从 `32.55975 ms` 推到 `12.6782 ms`，进入接近当前观测现实下界 `10.4729 ms` 的区域。

## 去重甲贡献

| 已删除或减少的大块 | 时间 |
|---|---:|
| FILE-BACKED OUTPUT / PUBLISH / REOPEN | 10.63825 ms |
| HISTORY / FULL JSON / DOUBLE DECODE | 4.4220 ms |
| REPEATED TENSOR → PNG ENCODE | 3.3357 ms |
| 合计 | 18.39595 ms |

总收益为 `19.88155 ms`。三个已确认大块合计 `18.39595 ms`，证明 P0 的绝大多数收益来自广义 `De-Armoring（去重甲）`：删除非必要路径和重复工作。

## TASK_COMPLETED 没有改变

任务始终是：提交固定任务，并得到正确的最终 256×256 PNG 结果。最终链仍确认 prompt identity、成功完成、最终 PNG bytes、PNG 结构、完整 decode、尺寸和结果身份。

被删除的是不属于任务完成本身的 file publish/reopen、history polling、重复 decode、重复 encode、watchdog、monitor 与同步 evidence。

## Watchdog 教训

watchdog、monitor 和 polling 不能因为“看起来更稳”就默认进入关键链。它们首先是 `ARMOR CANDIDATE（重甲候选）`；确有需要时放在关键路径外或 `RESULT_READY（结果就绪）` 后。

## 证据入口

- 完整 v1.1 四列案例：[FOUR-COLUMN-P0-99.md](FOUR-COLUMN-P0-99.md)
- 冻结状态：[CURRENT-STATE.md](CURRENT-STATE.md)
- 原始工程：`workspaces/absolute-time-fireworks-optimization/P0-EXTREME-MINIMAL-FASTPATH`
- 40-run 认证：`workspaces/absolute-time-fireworks-optimization/P0-EXTREME-MINIMAL-FASTPATH/certification-20260915-193531/results.json`
- 完整 SHA：`workspaces/absolute-time-fireworks-optimization/P0-EXTREME-MINIMAL-FASTPATH/MANIFEST.json`
