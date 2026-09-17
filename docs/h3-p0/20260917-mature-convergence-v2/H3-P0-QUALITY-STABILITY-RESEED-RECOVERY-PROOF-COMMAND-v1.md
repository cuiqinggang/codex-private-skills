# H3-P0 质量稳定性 Re-seed Recovery Proof 命令 v1

状态：`READY_TO_EXECUTE / ONE_SYSTEM_CANDIDATE_ONLY`

依据：

- `H3-P0-QUALITY-STABILITY-RESEED-UNTIL-PASS-VIRTUAL-99-v1.md`
- `first-principles-physical-limit-convergence v1.9.0`

唯一候选：

```text
STAR7_RESEED_UNTIL_PASS_V1
```

## 1. 最高规则

```text
NO_FREE_EXPLORATION=YES
CODEX_ROLE=DETERMINISTIC_EXECUTOR
```

本轮不验证 Adaptive-Step、不验证 ACT32、不验证原始 Loader fallback。

生产候选的质量重试次数**没有固定上限**。停止条件是：

```text
QC PASS
```

但本轮只是机制证明，必须保留技术断路器处理基础设施故障。

## 2. 固定环境与任务

保持冻结栈：

```text
GPU = RTX 2080 Ti 22GB / sm75
Loader = MiniMaxH3FP16LoaderStar7
Diffusion = minimax_h3_fl2va_pruned_int8_convrot.safetensors
Text Encoder = qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors
VAE = minimax_h3_video_vae_fp16.safetensors
Flags = --fast-disk --reserve-vram 1.0 --disable-pinned-memory
```

固定任务：

```text
T2VA
32x32
5 frames
1 step
prompt=static frame
sampler=res_multistep
scheduler=beta
no input audio
real MP4
```

不得改 step、sampler、scheduler、模型或源码。

## 3. 两个恢复任务

### Task A

初始固定 seed：

```text
930103
```

先运行一次 Star7 1-step 并 QC。

该 seed 已知应 FAIL；若意外 PASS，记录 `FAILURE_NOT_REPRODUCED_TASK_A=YES`，该任务直接 ACCEPT，不进行随机重采样。

若 FAIL：

```text
reject output
→ draw a new random seed
→ Star7 1-step
→ QC
→ if FAIL: draw another fresh random seed and repeat
→ if PASS: ACCEPT and stop Task A
```

### Task B

初始固定 seed：

```text
920108
```

规则与 Task A 相同。

已知该 seed 在 Star7 与原始 Loader 的 1-step 下均失败，因此本任务特别用于证明换随机初始状态是否可以恢复，而不是改变精度路径。

## 4. 随机 seed 规则

每次 retry 必须使用新的随机 seed。

必须记录：

- retry index；
- seed；
- seed 生成方式；
- 是否与当前任务之前 seed 重复；
- QC 结果。

如果新生成 seed 与该任务任何已用 seed 重复，立即重新抽取，不提交重复 seed。

禁止：

- 手动挑“看起来容易成功”的 seed；
- 使用历史已知 PASS seed；
- 按顺序写死 930104/930105 等；
- 因失败而改模型/step/sampler/scheduler。

要求使用正常随机源生成新 seed，并把实际 seed 记入证据。

## 5. 质量重试没有固定次数上限

不要写：

```text
MAX_RETRIES=3
```

或任何其他固定质量重试上限。

只要：

- ComfyUI 正常；
- GPU 正常；
- 能生成新 seed；
- 能提交新任务；

就继续随机重采样直到 QC PASS。

### 技术断路器

只有系统性技术故障才允许停止任务，例如：

- ComfyUI/GPU crash；
- 连续无法提交 prompt；
- 随机 seed 生成器异常；
- 重复 seed 无法避免；
- 输出链损坏，无法执行 QC；
- 用户/系统外部中止。

技术断路器不得用来代替质量重试次数上限。

若技术故障：

```text
RECOVERY_PROOF=BLOCKED_TECHNICAL
保存证据
STOP
RETURN TO GPT
```

## 6. QC

每个尝试都必须执行同一冻结 QC：

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

FAIL 输出绝不 ACCEPT。

## 7. 计时

每次 attempt 记录：

- Generation CUDA；
- Path；
- Total；
- QC time。

每个 task 记录：

```text
DELIVERY_TOTAL
```

定义：从该 task 第一次 Star7 `POST /prompt` 前，到第一个 QC PASS 的结果被 ACCEPT。

DELIVERY_TOTAL 包括所有失败 attempts + QC + 重新随机 + 最终成功 attempt。

## 8. Proof 通过条件

Task A 与 Task B 都最终得到：

```text
FINAL_ACCEPTED_QC=PASS
```

同时：

```text
INVALID_OUTPUT_DELIVERED=NO
EVERY_RETRY_USED_NEW_RANDOM_SEED=YES
MODEL_AND_RUNTIME_UNCHANGED=YES
STEP_REMAINS_1=YES
STAR7_ONLY=YES
NO_MANUAL_SEED_SELECTION=YES
```

则：

```text
RESEED_RECOVERY_PROOF=PASS
READY_FOR_FINAL_RESEED_SYSTEM_CERTIFICATION=YES
FINAL_QUALITY_STABILITY_99=NO
```

若发生技术断路器：

```text
RESEED_RECOVERY_PROOF=BLOCKED_TECHNICAL
```

注意：本轮没有“因为质量失败次数太多而 FAIL”的固定次数裁决；质量失败只会触发下一次全新随机采样。

## 9. 证据文件

生成：

```text
H3-P0-QUALITY-STABILITY-RESEED-RECOVERY-PROOF-RESULT-v1.md
H3-P0-QUALITY-STABILITY-RESEED-RECOVERY-PROOF-STATE-v1.json
```

至少包含：

- Task A 全部 attempts；
- Task B 全部 attempts；
- 每条 seed；
- 每条 QC；
- 每条 Total / Generation / Path / QC time；
- 两个 DELIVERY_TOTAL；
- 每个 task 的 attempts-to-success；
- accepted MP4 SHA256；
- invalid outputs rejected 数量；
- backend / force_cast 证明；
- RESEED_RECOVERY_PROOF；
- Git commit；
- remote verify。

提交、推送、远端回读后 STOP RETURN TO GPT。

## 10. 禁止事项

```text
no fixed quality retry cap
no adaptive step
no reference loader
no ACT32
no source patch
no parameter sweep
no version sweep
no profiler
no kernel trace
no free exploration
```
