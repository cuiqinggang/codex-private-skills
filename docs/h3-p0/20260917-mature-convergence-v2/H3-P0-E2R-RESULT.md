# H3-P0 E2R — E1 慢尾只读归因结果

状态：ATTRIBUTION_INCONCLUSIVE=YES；NEXT_GPU_CANDIDATE_MATURE=NO；GPU_RUNS_EXECUTED=0；NEXT_ACTION=RETURN_TO_GPT。

## 范围与证据

方法源为 first-principles-physical-limit-convergence v1.8.0。本轮只读取远端 E1/Post-E1 报告与 C:\AI\H3-P0-Acceptance\mature-convergence-v2\20260917-e0-e1-01 的既有证据；未提交新 prompt、未运行 GPU、未增添 instrumentation，未修改模型、workflow、Star7、ComfyUI 或 Python 环境。项目远端执行前 HEAD：64f5b9aa07621e78bae613e39f75343caeb0274b。

以下 pre/post 数值只由既有 run JSON 的 submit、Generation start/end、RESULT_READY epoch 标记相减得到。Generation/Path/Total 仍以 E1 原有 CUDA Event 与 Total 定义为权威；没有创造新计时边界。三条 formal 的 path_stage_events 均为空。日志证据均指 candidate/server-E1_STAR7.log，具体文件 SHA-256 见同名 JSON。

| seed | Generation CUDA s | Path s | Total s | submit→Generation start s | Generation end→RESULT_READY s | 日志行 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 910100 | 11.5185 | 3.4304 | 14.9489 | 0.7130 | 2.7143 | 75–81 |
| 910102 | 3.1019 | 3.3823 | 6.4843 | 0.7338 | 2.6456 | 82–89 |
| 910103 | 2.4698 | 8.0919 | 10.5618 | 5.0662 | 3.0196 | 90–96 |

## 五个归因问题

1. **910100 Generation tail：**相对 910102，Generation 多 8.4166 s。日志第 76–77 行记录“0 models unloaded”和 H3 dynamic VRAM preparation，第 79 行记录 11.5185 s CUDA Event；但 910102 和 910103 也分别有同类准备日志（83–84、91–92 行）。没有区分实际权重 load、offload、residency miss 或 reload 的事件与持续时间。H3 load/offload/residency/reload 是否导致这条慢尾：**UNKNOWN**。可证明的只是慢尾位于 Generation 计时内。

2. **910103 Path tail：**相对 fast path 910102，Path 多 4.7096 s，其中已有 epoch 标记显示 Generation 前多 4.3325 s，约占这段 Path 差额的 92%。日志第 90–92 行只有 got prompt、0 models unloaded、H3 dynamic VRAM preparation；第 95 行的 Video VAE preparation 在 Generation timer（第 94 行）之后。故 VAE decode 或 H3→VAE 后段不能解释主要的 **pre-Generation** 差额；它们各自实际耗时仍为 **UNKNOWN**。Qwen3-VL conditioning、H3 驻留/调度或其他前段事件究竟是哪一个造成差额：**UNKNOWN**。

3. **910102 fast path：**既有标记显示前段 0.7338 s、Generation 3.1019 s、后段 2.6456 s。相对 910100，它主要少了 8.4166 s Generation；相对 910103，它主要少了 4.3325 s Generation 前时间。三条 formal 都记录 H3 dynamic VRAM preparation、0 models unloaded 和 Video VAE preparation；日志没有能唯一解释 fast path 的差异事件。具体因果机制：**UNKNOWN**。

4. **formal seed 与 Qwen conditioning/cache：**MiniMaxH3TE/Qwen 载入请求只在 warmup 的第 56–57 行出现；formal 段没有新的 TE load 请求。但没有 conditioning 节点执行记录或明确 cache HIT 标记。“未记录新的 TE load”不能证明 conditioning 没有重新执行，也不能证明已缓存。formal seed 变化时 conditioning rerun 或 cache HIT：**UNKNOWN**。

5. **≥10% Total 残余块：**已有计时能确认两个大于 10% 的**时间区间**：910100 的 Generation 超出 910102 8.4166 s，占该条 Total 的约 56.3%；910103 的 Generation 前区间超出 910102 4.3325 s，占该条 Total 的约 41.0%。这些是可靠的时间定位，尚无证据把任一区间唯一归因于 H3 residency、Qwen、VAE 或 host sync。可确认的机制级 ≥10% Total 残余块：**UNKNOWN**。

## 归因矩阵与后续候选状态

| seed | Generation tail | Path tail | conditioning rerun/cache | H3 residency/load | VAE/transition | 置信度 |
| --- | --- | --- | --- | --- | --- | --- |
| 910100 | 8.4166 s 差额位于 Generation | 与 fast path 接近 | UNKNOWN | 同类 dynamic VRAM 准备日志；因果 UNKNOWN | 准备日志在 timer 后；耗时 UNKNOWN | 时间定位高；机制低 |
| 910102 | fast Generation 3.1019 s | fast Path 3.3823 s | UNKNOWN | 同类准备日志；因果 UNKNOWN | 准备日志存在；耗时 UNKNOWN | 时间定位高；机制低 |
| 910103 | Generation 2.4698 s | 4.3325 s 差额在 Generation 前 | UNKNOWN | 同类准备日志；因果 UNKNOWN | 后段不能解释主要前段差额；耗时 UNKNOWN | 时间定位高；机制低 |

- Conditioning cache、INT8 ConvRot text encoder、Star7 时代 residency policy、最小 host-sync patch：UNKNOWN_NEEDS_FUTURE_BOUNDED_TEST。本轮没有足够因果证据选择其中一个 GPU 候选。
- INT8 ConvRot VAE：HIGH_RISK_DEFER；沿用 Post-E1 状态，本轮没有新增可归因的 VAE 时间证据。
- W4A8 diffusion：UNSUPPORTED_ON_CURRENT_HW；沿用 Post-E1 状态，本轮没有重新测试或改变此裁决。

## QC、远端与停止点

NO_NEW_GPU_PROMPT=PASS；NO_NEW_INSTRUMENTATION=PASS；NO_EVIDENCE_FILE_MODIFICATION=PASS；ALL_CLAIMS_TRACEABLE_TO_EXISTING_EVIDENCE=PASS。E1 结果与 QC 未改动；无 runtime 变更，因此无需 rollback。

REMOTE_COMMIT=PENDING_FIRST_PUSH；REMOTE_VERIFY=PENDING_FIRST_PUSH。推送后写入实际远端核验回执并再次核验。随后 STOP，RETURN TO GPT；不得自行启动下一 GPU 候选。
