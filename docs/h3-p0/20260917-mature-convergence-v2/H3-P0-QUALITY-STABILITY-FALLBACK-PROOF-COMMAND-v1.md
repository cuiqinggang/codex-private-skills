# H3-P0 质量稳定性 Verified Fast Path 兜底证明命令 v1

状态：`READY_TO_EXECUTE / ONE_SYSTEM_CANDIDATE_ONLY / MAX_GPU_RUNS=4`

依据：

- `H3-P0-QUALITY-STABILITY-FALLBACK-VIRTUAL-99-v1.md`
- `H3-P0-QUALITY-STABILITY-ACT32-PROOF-RESULT-v2.md`
- `first-principles-physical-limit-convergence v1.9.0`

唯一候选：

```text
VERIFIED_FAST_PATH_V1
```

## 1. 最高规则

```text
NO_FREE_EXPLORATION=YES
CODEX_ROLE=DETERMINISTIC_EXECUTOR
```

本轮不修改 Star7、ComfyUI、模型、采样参数或精度策略。

禁止：

- ACT32-v3；
- 任何新 patch；
- 改 seed；
- 降低 QC；
- 参数/版本搜索；
- profiler / kernel trace；
- 自动第三层重试。

## 2. 固定环境与任务

保持冻结任务：

```text
GPU = RTX 2080 Ti 22GB / sm75
ComfyUI = 8a33128f2f8c5585c57486c07de481241e70a39c
Diffusion = minimax_h3_fl2va_pruned_int8_convrot.safetensors
Text Encoder = qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors
VAE = minimax_h3_video_vae_fp16.safetensors
Flags = --fast-disk --reserve-vram 1.0 --disable-pinned-memory
T2VA / 32x32 / 5 frames / 1 step / prompt=static frame / res_multistep / beta / no input audio / real MP4
```

Star7 使用原始冻结文件：

```text
C:\AI\MiniMax-H3\ComfyUI\custom_nodes\minimax-h3-fp16-exact-star7\nodes.py
SHA256=8F6D3EB42D5123A36A814F3EFE6910D499CDF618E190DE74F3BCA0D5935E232B
```

如源码身份不符：保存证据并 STOP RETURN TO GPT。

## 3. 系统链路定义

每个测试 seed 必须按以下完整生产链执行：

```text
T0 = 首次 Star7 POST /prompt 前
Star7 same-seed run
→ RESULT_READY
→ QC
   ├─ PASS: ACCEPT
   └─ FAIL: 启动原始 UNETLoader same-seed reference run
             → RESULT_READY
             → QC
             ├─ PASS: ACCEPT
             └─ FAIL: CONTROLLED_FAIL
T1 = 最终 ACCEPT 或 CONTROLLED_FAIL 判定完成
```

定义：

```text
DELIVERY_TOTAL = T1 - T0
```

`DELIVERY_TOTAL` 必须包含：

- Star7 Total；
- 第一次 QC 时间；
- 若触发 fallback，则包含切换/加载/原始 Loader Total；
- 第二次 QC 时间。

不得用 `Star7 Total + 历史 reference Total` 拼接代替真实链路时间。

## 4. 固定测试 seed 与 GPU 上限

只测试两个已知 Star7 失败 seed：

```text
930103
920108
```

每个 seed 最多 2 次 GPU：

```text
1. Star7
2. 仅在 Star7 QC FAIL 时，同 seed 原始 UNETLoader
```

全任务：

```text
MAX_GPU_RUNS=4
```

如果 Star7 在某 seed 本轮意外 QC PASS：

- 该 seed 直接 ACCEPT；
- 不为“强行证明 fallback”额外运行 reference；
- 记录 `FALLBACK_NOT_TRIGGERED_THIS_RUN`。

## 5. QC 不变

每个最终 ACCEPT 输出必须全部满足：

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

禁止降低阈值。

## 6. Reference 路径

原始 reference 必须使用标准 `UNETLoader`，同模型、同 text encoder、同 VAE、同 flags、同 task、同 seed。

reference 只在对应 Star7 本轮 QC FAIL 时触发。

不得：

- 改 seed；
- 改 prompt；
- 改 sampler/scheduler；
- 改模型；
- 使用 ACT32 或其他 patch。

## 7. 通过条件

如果两个 seed 最终都 ACCEPT：

```text
FINAL_ACCEPTED_QC=2/2
INVALID_OUTPUT_DELIVERED=NO
NO_SEED_CHANGE=YES
NO_MANUAL_INTERVENTION=YES
VERIFIED_FAST_PATH_PROOF=PASS
READY_FOR_SYSTEM_TIME_ROI_RECALC=YES
```

对每个 seed 记录：

```text
FAST_QC
FAST_TOTAL
FAST_QC_TIME
FALLBACK_TRIGGERED
REFERENCE_QC
REFERENCE_TOTAL
REFERENCE_QC_TIME
DELIVERY_TOTAL
FINAL_ACCEPTED_LOADER
```

## 8. 失败条件

若 Star7 FAIL 且同 seed reference 也 FAIL：

```text
VERIFIED_FAST_PATH_PROOF=FAIL_REFERENCE_QUALITY
INVALID_OUTPUT_DELIVERED=NO
CONTROLLED_FAIL=YES
```

立即停止后续新策略；不得自动换 seed、追加 retry 或设计第三层。

如果 reference 无法启动/运行：

```text
VERIFIED_FAST_PATH_PROOF=FAIL_RUNTIME
```

保存证据后停止。

## 9. 证据与收口

生成新文件：

```text
H3-P0-QUALITY-STABILITY-FALLBACK-PROOF-RESULT-v1.md
H3-P0-QUALITY-STABILITY-FALLBACK-PROOF-STATE-v1.json
```

必须包含：

- 两个 seed 的完整链路；
- GPU 提交账本；
- Star7/reference QC；
- DELIVERY_TOTAL；
- 最终 ACCEPT/FAIL；
- Star7 源码 SHA256 前后核验；
- `VERIFIED_FAST_PATH_PROOF`；
- Git commit；
- remote verify。

完成后：

```text
commit → push → remote verify → STOP → RETURN TO GPT
```

本轮不是最终10次系统认证，不得宣告 FINAL_99。
