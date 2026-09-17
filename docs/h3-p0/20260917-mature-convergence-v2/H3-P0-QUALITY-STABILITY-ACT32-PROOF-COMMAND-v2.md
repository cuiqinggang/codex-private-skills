# H3-P0 质量稳定性 ACT32 候选实证命令 v2

状态：`READY_TO_EXECUTE / SOURCE_IDENTITY_FIXED / ONE_CANDIDATE_ONLY / MAX_GPU_RUNS=6`

依据：

- `H3-P0-QUALITY-STABILITY-VIRTUAL-99-v1.md`
- `H3-P0-QUALITY-STABILITY-FINAL-LOCALIZATION-RESULT-v1.md`
- `H3-P0-QUALITY-STABILITY-ACT32-SOURCE-IDENTITY-CORRECTION-v1.md`
- `H3-P0-QUALITY-STABILITY-ACT32-PROOF-COMMAND-v1.md`（除源码身份笔误外，其候选定义、阈值与执行规则继续有效）
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

只验证 ACT32。不得自行设计第二候选、缩小保护范围、改 seed、改次数、改阈值或追加 GPU。

## 2. 正确源码身份门禁

GPU 前必须核对：

```text
STAR7_NODES_PATH=C:\AI\MiniMax-H3\ComfyUI\custom_nodes\minimax-h3-fp16-exact-star7\nodes.py
STAR7_NODES_SHA256=8F6D3EB42D5123A36A814F3EFE6910D499CDF618E190DE74F3BCA0D5935E232B

COMFY_ROOT_NODES_PATH=C:\AI\MiniMax-H3\ComfyUI\nodes.py
COMFY_ROOT_NODES_SHA256=5AB70A74109118256934B63675ED620A47BECB54343A77DAA66B4FE20A4D0EE7

MINIMAX_MODEL_PATH=C:\AI\MiniMax-H3\ComfyUI\comfy\ldm\minimax\model.py
MINIMAX_MODEL_SHA256=3267343A034C6DA91234D20FB63F74A0A439EFC4E468F473C9477D436B3BFC8A
```

本轮只允许临时修改 `STAR7_NODES_PATH`。

`COMFY_ROOT_NODES_PATH` 与 `MINIMAX_MODEL_PATH` 均禁止修改。

若上述任一真实 SHA 与这里不一致：保存证据、`ACT32_PROOF=NOT_RUN_SOURCE_IDENTITY_MISMATCH_V2`、GPU=0、STOP、RETURN TO GPT。

核验通过后，对 Star7 `nodes.py` 做字节级备份。

## 3. ACT32 定义

ACT32 的目标是：保留 INT8/ConvRot 权重快速核，只取消 50 个 DiT block 中反复的额外 FP16 激活截断。

必须保持：

```text
set_model_compute_dtype(torch.float16) unchanged
force_cast_weights=False
quant_format=int8_tensorwise
convrot=True
K_OUT_PROJ=64.0
K_FC2=256.0
residual stream=FP32
condition_proj protection unchanged
model / sampler / scheduler / seed / step unchanged
```

仅允许实现：

```text
norm/mod -> attention qkv_proj : FP32 activation into existing INT8/ConvRot linear
attention core                 : 不主动改算法；现有 attention 路径允许保持 FP16
attention out -> out_proj      : FP32 scale/divide -> existing INT8/ConvRot linear -> FP32 output
norm/mod -> fc1                : FP32 activation into existing INT8/ConvRot linear
SwiGLU                         : FP32
scaled activation -> fc2       : FP32 into existing INT8/ConvRot linear -> FP32 output
residual add                   : FP32
```

不得把 INT8 权重反量化为 dense FP32/FP16。

若当前 attention 路径因 dtype 不兼容不能运行：`ACT32_PROOF=FAIL_RUNTIME`，恢复源码并停止；不得发明第二实现。

## 4. 静态与后端门禁

GPU 前必须同时通过：

1. Star7 修改后的 `nodes.py` 语法检查；
2. 启动日志明确 ACT32 临时候选激活；
3. 运行时证明：

```text
backend contains int8_tensorwise+convrot
force_cast_weights=False
quantized backend/count unchanged
NO_DENSE_WEIGHT_FALLBACK=YES
```

若出现 dense fallback、forced cast 或模型身份变化：

```text
ACT32_PROOF=FAIL_BACKEND_MUTATION
restore
STOP
```

## 5. 固定环境与任务

保持冻结环境：

```text
GPU=RTX 2080 Ti 22GB / sm75
ComfyUI=8a33128f2f8c5585c57486c07de481241e70a39c
Diffusion=minimax_h3_fl2va_pruned_int8_convrot.safetensors
Text Encoder=qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors
VAE=minimax_h3_video_vae_fp16.safetensors
Flags=--fast-disk --reserve-vram 1.0 --disable-pinned-memory
```

固定任务：T2VA / 32x32 / 5 frames / 1 step / prompt=`static frame` / sampler=`res_multistep` / scheduler=`beta` / 无输入音频 / 真实 MP4。

计时定义沿用冻结标准。

## 6. GPU 上限和顺序

```text
MAX_GPU_RUNS=6
```

预热两次，不计性能证明：

```text
940098
940099
```

正式四条，严格顺序：

```text
1. 930103  # 已知 Star7 FAIL / reference PASS
2. 920108  # 已知 Star7 白/平坦 FAIL
3. 930100  # 已知 Star7 PASS
4. 930101  # 已知 Star7 PASS
```

全部只跑 ACT32，不重复原始 Loader；已有 reference 历史证据继续使用。

任一正式 QC FAIL：立即 `ACT32_PROOF=FAIL_QUALITY`，停止后续 GPU，恢复源码，不得换 seed 或补跑。

## 7. QC 硬门槛

每条正式运行必须全部满足：

```text
history complete
real MP4 exists
ffprobe=32x32x5
ffmpeg decode succeeds
all pixels finite
non-black / non-flat
every frame range>=8
every frame std>=1.5
artifact SHA256 saved
```

不得降低。

## 8. 性能配对门槛

历史 Star7 Total：

```text
930103 = 6.1379 s
930100 = 6.8896 s
930101 = 8.6514 s
```

`920108` 无冻结 Total，只参与质量证明。

计算 930103 / 930100 / 930101 的 ACT32 paired delta 和 ratio。

必须同时满足：

```text
paired median Total regression <=15%
paired median absolute Total regression <=1.0 s
all formal ACT32 Total <=14 s
```

质量4/4通过但性能失败：

```text
ACT32_QUALITY_PROOF=PASS
ACT32_PERFORMANCE_PROOF=FAIL
ACT32_PROOF=FAIL_PERFORMANCE
```

恢复、STOP，不得自行缩小保护范围。

## 9. PASS 条件

全部成立才允许：

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

然后：

```text
ACT32_PROOF=PASS
READY_FOR_FINAL_QUALITY_STABILITY_CERTIFICATION=YES
FINAL_QUALITY_STABILITY_99=NO
```

本轮仍不是最终99认证。

## 10. 恢复、证据和版本隔离

无论 PASS/FAIL，都恢复 Star7 `nodes.py` 到原字节版本，并核对 SHA256 必须回到：

```text
8F6D3EB42D5123A36A814F3EFE6910D499CDF618E190DE74F3BCA0D5935E232B
```

保存实际候选修改：

```text
H3-P0-QUALITY-STABILITY-ACT32-PATCH-v2.diff
```

生成新文件，不覆盖 v1 阻断证据：

```text
H3-P0-QUALITY-STABILITY-ACT32-PROOF-RESULT-v2.md
H3-P0-QUALITY-STABILITY-ACT32-PROOF-STATE-v2.json
```

必须记录：源码身份、ACT32 diff、后端证明、2次预热、正式运行、QC、paired timing、ACT32_PROOF、GPU_RUNS_EXECUTED、源码恢复、Git commit、remote verify。

提交、推送、远端回读后 STOP RETURN TO GPT。

## 11. 禁止事项

```text
one candidate
one proof
one verdict
```

禁止 W4A8、BF16、block14-only、late-block-only、fallback 系统、参数/版本 sweep、profiler、kernel trace、新模型、自动第二版候选。