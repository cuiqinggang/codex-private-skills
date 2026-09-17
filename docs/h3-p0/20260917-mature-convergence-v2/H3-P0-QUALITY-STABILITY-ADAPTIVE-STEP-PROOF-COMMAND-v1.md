# H3-P0 质量稳定性 Adaptive-Step 候选实证命令 v1

状态：`READY_TO_EXECUTE / ONE_CANDIDATE_ONLY / MAX_GPU_RUNS=6`

依据：

- `H3-P0-QUALITY-STABILITY-ADAPTIVE-STEP-VIRTUAL-99-v1.md`
- `H3-P0-QUALITY-STABILITY-FALLBACK-PROOF-RESULT-v1.md`
- `H3-P0-QUALITY-STABILITY-ACT32-PROOF-RESULT-v2.md`
- `first-principles-physical-limit-convergence v1.9.0`

唯一候选：

```text
STAR7_ADAPTIVE_MIN_STEP_V1
```

## 1. 最高规则

```text
NO_FREE_EXPLORATION=YES
CODEX_ROLE=DETERMINISTIC_EXECUTOR
```

本轮只证明“同 seed 最小通过步数”；不得测试第二候选。

禁止：

- 修改 Star7 源码；
- ACT32 / BF16 / W4A8 / block14 / late-block；
- 原始 UNETLoader fallback；
- 改 seed；
- 改 prompt / sampler / scheduler / 分辨率 / 帧数；
- 4 step 或更多；
- 参数/版本 sweep；
- profiler；
- kernel trace；
- 自动派生下一实验。

## 2. 固定环境

保持当前冻结栈：

```text
GPU = RTX 2080 Ti 22GB / sm75
ComfyUI = 8a33128f2f8c5585c57486c07de481241e70a39c
Loader = MiniMaxH3FP16LoaderStar7
Diffusion = minimax_h3_fl2va_pruned_int8_convrot.safetensors
Text Encoder = qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors
VAE = minimax_h3_video_vae_fp16.safetensors
Flags = --fast-disk --reserve-vram 1.0 --disable-pinned-memory
```

源码身份：

```text
Star7 nodes.py SHA256 = 8F6D3EB42D5123A36A814F3EFE6910D499CDF618E190DE74F3BCA0D5935E232B
MiniMax model.py SHA256 = 3267343A034C6DA91234D20FB63F74A0A439EFC4E468F473C9477D436B3BFC8A
```

本轮禁止改源码；开始和结束都核对 Star7 SHA256。

## 3. 固定任务

除 step 外全部不变：

```text
T2VA
32x32
5 frames
prompt=static frame
sampler=res_multistep
scheduler=beta
no input audio
real MP4
```

已冻结事实：`930103` 和 `920108` 在 Star7 1-step 下均 QC FAIL；`920108` 在原始 UNETLoader 1-step 下也 FAIL。因此本轮不重复 1-step 失败。

## 4. 预热

先做 2 条 Star7 / 2-step 预热，不计正式质量证明：

```text
950098
950099
```

记录 Total / Generation / Path / QC；QC PASS/FAIL 都只记录，不改变正式执行顺序。

## 5. 正式质量证明

### Seed 930103

先运行：

```text
seed=930103
steps=2
```

若 QC PASS：

```text
930103_MINIMUM_PASSING_STEP=2
```

不得再跑该 seed 的 3-step。

若 QC FAIL：才运行：

```text
seed=930103
steps=3
```

若 PASS：

```text
930103_MINIMUM_PASSING_STEP=3
```

若仍 FAIL：

```text
ADAPTIVE_STEP_PROOF=FAIL_QUALITY
STOP
```

不得继续 920108，也不得增加 4-step。

### Seed 920108

仅在 930103 已通过时继续。

先运行：

```text
seed=920108
steps=2
```

若 QC PASS：

```text
920108_MINIMUM_PASSING_STEP=2
```

不得再跑 3-step。

若 QC FAIL：才运行：

```text
seed=920108
steps=3
```

若 PASS：

```text
920108_MINIMUM_PASSING_STEP=3
```

若仍 FAIL：

```text
ADAPTIVE_STEP_PROOF=FAIL_QUALITY
STOP
```

总 GPU 提交不得超过 6：2 预热 + 最多 4 正式。

## 6. QC

每条正式运行必须：

```text
history complete
real MP4 exists
ffprobe = 32x32x5
ffmpeg decode succeeds
all pixels finite
non-black / non-flat
every frame range >= 8
every frame std >= 1.5
artifact SHA256 saved
```

不得降低门槛。

## 7. 后端与时间记录

启动/运行日志必须确认：

```text
backend contains int8_tensorwise+convrot
force_cast_weights=False
no dense fallback evidence
```

每条记录：

```text
Generation CUDA
Path
Total
QC time
```

本轮性能为候选描述性证据，不设置新的任意绝对失败门槛；关键是得到每个脆弱 seed 的 `MINIMUM_PASSING_STEP` 与真实稳态时间。后续系统 ROI 由 GPT 基于这些数据计算。

## 8. 通过条件

全部成立：

```text
930103 QC PASS by step<=3
920108 QC PASS by step<=3
same seed preserved
Star7 source unchanged
backend int8_tensorwise+convrot preserved
force_cast_weights=False
no dense fallback
no crash
no policy-external retry
```

则：

```text
ADAPTIVE_STEP_PROOF=PASS
READY_FOR_SYSTEM_TIME_ROI_RECALC=YES
FINAL_QUALITY_STABILITY_99=NO
```

任一 seed 到 3-step 仍 FAIL：

```text
ADAPTIVE_STEP_PROOF=FAIL_QUALITY
READY_FOR_SYSTEM_TIME_ROI_RECALC=NO
STOP_RETURN_TO_GPT
```

## 9. 输出

生成：

```text
H3-P0-QUALITY-STABILITY-ADAPTIVE-STEP-PROOF-RESULT-v1.md
H3-P0-QUALITY-STABILITY-ADAPTIVE-STEP-PROOF-STATE-v1.json
```

至少包含：

- 2 条预热；
- 实际正式 GPU 账本；
- 930103 2/3-step QC 与最小通过步数；
- 920108 2/3-step QC 与最小通过步数；
- Generation / Path / Total；
- backend / force_cast 证明；
- 源码前后 SHA256；
- ADAPTIVE_STEP_PROOF；
- GPU_RUNS_EXECUTED；
- Git commit / remote verify。

完成后：

```text
commit → push → remote verify → STOP → RETURN TO GPT
```

```text
one candidate
one proof
one verdict
```
