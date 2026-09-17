# H3-P0 质量稳定性 ACT32 候选实证命令 v1

状态：`READY_TO_EXECUTE / ONE_CANDIDATE_ONLY / MAX_GPU_RUNS=6`

依据：

- `H3-P0-QUALITY-STABILITY-VIRTUAL-99-v1.md`
- `H3-P0-QUALITY-STABILITY-FINAL-LOCALIZATION-RESULT-v1.md`
- `first-principles-physical-limit-convergence v1.9.0`

唯一候选：

```text
STAR7_ACT32_INT8_CONVROT
```

## 1. 最高规则

```text
NO_FREE_EXPLORATION=YES
CODEX_ROLE=DETERMINISTIC_EXECUTOR
```

本轮只验证 ACT32；不得自行测试任何第二候选。

允许有限执行灵活性：等价 PowerShell / `.ps1`、绝对路径、日志、备份、恢复同一中断任务。

禁止：

- W4A8；
- BF16 候选；
- block14-only；
- late-block-only；
- 原始 Loader fallback 系统；
- 新模型；
- 参数/版本 sweep；
- profiler；
- kernel trace；
- 改 seed / 次数 / 顺序 / 阈值；
- 自动设计第二版补丁。

若候选失败：保存证据、恢复源码、STOP、RETURN TO GPT。

## 2. 固定环境和任务

保持现有冻结栈：

```text
GPU = RTX 2080 Ti 22GB / sm75
ComfyUI = 8a33128f2f8c5585c57486c07de481241e70a39c
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

正式计时定义完全沿用此前冻结定义。

## 3. 源码身份与安全

操作前记录 SHA256：

- Star7 `nodes.py`；
- ComfyUI `comfy/ldm/minimax/model.py`。

已知最近冻结值可作交叉检查：

```text
nodes.py = 5AB70A74109118256934B63675ED620A47BECB54343A77DAA66B4FE20A4D0EE7
model.py = 3267343A034C6DA91234D20FB63F74A0A439EFC4E468F473C9477D436B3BFC8A
```

若真实本机值与已冻结值不一致：不要覆盖；记录差异并 STOP RETURN TO GPT。

先制作字节级备份。

本轮只允许临时修改 Star7 `nodes.py`；禁止修改 `model.py`。

## 4. ACT32 候选的精确定义

目标：保留 INT8/ConvRot 权重快核，只取消反复的额外 FP16 激活截断。

必须保持：

```text
set_model_compute_dtype(torch.float16) = unchanged
force_cast_weights = False
quant_format = int8_tensorwise
convrot = True
weight count / backend = unchanged
K_OUT_PROJ = 64.0
K_FC2 = 256.0
residual stream = FP32
condition_proj protection = unchanged
```

候选仅做以下逻辑变化：

### 4.1 DiT block 分支入口

现 Star7 中 `norm + modulation` 后进入 attention / MLP 的激活被显式 `.to(torch.float16)`。

ACT32：

```text
norm/mod result remains FP32 into attention branch
norm/mod result remains FP32 into MLP branch
```

不得改 modulation 数学，不得改 residual add。

### 4.2 Attention out_proj

保持 `/ K_OUT_PROJ` 与 `* K_OUT_PROJ` 的 power-of-two overflow protection，但：

```text
scale/divide in FP32
FP32 activation -> existing INT8/ConvRot out_proj
output -> FP32
```

不得把权重反量化成 dense FP32。

### 4.3 MLP

保持 Star7 的 FP32 SwiGLU 与 `/K_FC2`、`*K_FC2` overflow protection，但：

```text
FP32 activation -> existing INT8/ConvRot fc1
SwiGLU = FP32
scaled activation remains FP32 -> existing INT8/ConvRot fc2
fc2 output -> FP32
```

不得因输入 dtype 变为 FP32 而绕回未保护的原始 MLP forward。

### 4.4 Attention 主体

不为了本轮目标主动改 attention 算法、backend 或 attention override 规则。

如果当前 attention 路径自然接受 FP32 qkv 激活并运行，则按现有实现运行；不得为了追求速度另加新 attention patch。

若发生 dtype 不兼容而无法执行：候选直接 `ACT32_PROOF=FAIL_RUNTIME`，恢复并停止；不得临场发明第二实现。

## 5. 静态/启动门禁

GPU 前必须：

1. `python -m py_compile` 或等价语法检查 PASS；
2. 启动日志明确 Star7 ACT32 临时候选激活；
3. 日志/运行时核对：

```text
backend contains int8_tensorwise+convrot
force_cast_weights=False
quantized weight backend/count unchanged
```

如果发现 dense weight fallback、forced cast 或模型身份变化：

```text
ACT32_PROOF=FAIL_BACKEND_MUTATION
GPU formal runs = 0
restore
STOP
```

## 6. GPU 运行上限与顺序

总上限：`MAX_GPU_RUNS=6`。

### 6.1 两次预热，不计性能证明

```text
940098
940099
```

必须完成技术输出链；记录 QC，但不用于正式质量通过率或性能配对。

### 6.2 四条正式压力样本

严格顺序：

```text
1. 930103  # 已知 Star7 失败，原始 Loader PASS
2. 920108  # 已知 Star7 平坦/白帧失败
3. 930100  # 已知 Star7 PASS
4. 930101  # 已知 Star7 PASS
```

全部使用 ACT32 候选，不运行原始 Loader 对照；已有历史 reference 作为冻结证据。

任意一条正式 QC FAIL：

```text
ACT32_PROOF=FAIL_QUALITY
停止后续 GPU
restore
保存证据
RETURN TO GPT
```

禁止补 seed、换 seed 或追加运行。

## 7. QC

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

质量门槛不得降低。

## 8. 性能配对门禁

候选证明只使用可配对历史稳态 Star7 样本：

```text
930103 baseline Total = 6.1379 s
930100 baseline Total = 6.8896 s
930101 baseline Total = 8.6514 s
```

`920108` 因历史 QC 中断无冻结 Total，不参与配对性能门禁。

计算上述三 seed 的 ACT32 Total 与历史 Star7 Total 的 paired delta / ratio。

通过必须同时满足：

```text
paired median Total regression <= 15%
paired median absolute Total regression <= 1.0 s
all formal ACT32 Total <= 14 s
```

Generation / Path 同时记录，但 Total 是主裁决。

若质量4/4 PASS但性能门禁失败：

```text
ACT32_QUALITY_PROOF=PASS
ACT32_PERFORMANCE_PROOF=FAIL
ACT32_PROOF=FAIL_PERFORMANCE
```

恢复并 STOP，不得自行缩小保护范围。

## 9. 最终候选通过条件

全部同时成立：

```text
FORMAL_QC=4/4
930103_REPAIRED=YES
920108_REPAIRED=YES
930100_REMAINS_PASS=YES
930101_REMAINS_PASS=YES
BACKEND_INT8_CONVROT_PRESERVED=YES
FORCE_CAST_WEIGHTS_FALSE=YES
NO_DENSE_WEIGHT_FALLBACK=YES
NO_CRASH=YES
NO_AUTO_RETRY=YES
PAIRED_MEDIAN_TOTAL_REGRESSION<=15%
PAIRED_MEDIAN_ABS_REGRESSION<=1.0s
ALL_FORMAL_TOTAL<=14s
```

则：

```text
ACT32_PROOF=PASS
READY_FOR_FINAL_QUALITY_STABILITY_CERTIFICATION=YES
FINAL_QUALITY_STABILITY_99=NO
```

注意：本轮只是候选实证，不得直接宣告最终99。

## 10. 恢复与证据

无论 PASS/FAIL，测试完成后都必须恢复 Star7 `nodes.py` 到字节级原始版本，并核对 SHA256。

保存实际 ACT32 修改为独立 diff：

```text
H3-P0-QUALITY-STABILITY-ACT32-PATCH-v1.diff
```

生成：

```text
H3-P0-QUALITY-STABILITY-ACT32-PROOF-RESULT-v1.md
H3-P0-QUALITY-STABILITY-ACT32-PROOF-STATE-v1.json
```

内容至少包括：

- 源码前后 SHA256；
- ACT32 diff；
- backend / force_cast / quantization proof；
- 2 条预热；
- 实际正式运行表；
- 全部 QC；
- 三条 paired timing；
- ACT32_PROOF 裁决；
- GPU_RUNS_EXECUTED；
- Git commit；
- remote verify。

提交、推送、远端回读后 STOP RETURN TO GPT。

## 11. 禁止事项

本轮绝对禁止把失败结果转化为新的现场试验。

```text
one candidate
one proof
one verdict
```
