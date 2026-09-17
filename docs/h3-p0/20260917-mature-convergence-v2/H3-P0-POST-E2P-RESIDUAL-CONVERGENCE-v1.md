# H3-P0 Post-E2P Residual Convergence v1

状态：`POST_E2P_REBASE_COMPLETE=YES / NEXT_ACTION=E2M_REMOTE_METADATA_PREFLIGHT / GPU_UNLOCK=NO`

方法：`first-principles-physical-limit-convergence v1.8.0`

## 1. 当前真实赢家

E1 Star7 Native FP16 Exact 继续 KEEP：

```text
Total P50/P95 = 10.562 / 14.510 s
Generation P50/P95 = 3.102 / 10.677 s
Path P50/P95 = 3.430 / 7.626 s
Fast valid sample = 6.484 s
```

E2R 只读归因：`ATTRIBUTION_INCONCLUSIVE=YES`。它只证明慢尾分别存在于 Generation 和 pre-Generation Path 区间，不能把慢尾唯一归因到 residency/Qwen/VAE/host-sync。

E2P W4A8 预检：

```text
SM75_BEHAVIOR=FALLBACK_SUPPORTED
W4A8_CANDIDATE_MATURE=NO
STATUS=COMPATIBILITY_INCONCLUSIVE
```

本机 `comfy-kitchen 0.2.31` 源码可识别 W4A8 layout；SM75 不选择 SM80+ CUDA/Triton fast path，但可到达 eager backend。Star7 可保留 W4A8 metadata/dispatch，但不提供 W4A8 kernel；Star7+W4A8 端到端兼容尚未验证。

## 2. 外部成熟证据重新核对

同卡成熟项目 `IvenKooLab/minimax-h3-turing` 明确报告：

- RTX 2080 Ti 22GB / Turing sm75；
- PyTorch 2.9.1+cu130；
- W4A8 mixed diffusion；
- ComfyUI v0.33.1 baseline；
- 标准 UNETLoader workflow；
- W4A8 是其 Turing 主量化路线，并有真实生产运行。

Kijai 当前公开文件：

```text
minimax_h3_fl2va_pruned_w4a8_mixed.safetensors
size ≈ 12.5 GB
```

模型卡仍说明 W4A8 是 experimental 4-bit weights + INT8 ConvRot activations，Requires ComfyUI >=0.31.0；本机 ComfyUI 0.34 已满足最低版本。

这证明：`SM75 + W4A8` 端到端可行路径真实存在；但不能证明本机 `comfy-kitchen 0.2.31 + Star7 2.0.14` 与该外部环境完全等价。

## 3. 为什么现在不直接下载 12.5GB

当前缺口只剩两个：

1. 目标 Kijai 文件的实际 safetensors metadata / quantization layout 是否与本机 parser 的 W4A8 路径精确一致；
2. Star7 loader 对这个具体 metadata 是否能无冲突保留 `force_cast_weights=false` / quantized dispatch。

这两个问题都可在**不下载完整权重、不启动 GPU**的前提下通过 safetensors header/远端元数据完成高价值预检。

因此生命周期 ROI：

```text
E2M tiny metadata preflight cost << 12.5GB full download + A/B cost
```

先 E2M 是当前最短工程路径。

## 4. E2M 成熟门禁

只有 E2M 同时证明：

```text
TARGET_FILE_IDENTITY=PASS
QUANTIZATION_METADATA_PRESENT=PASS
LAYOUT_TYPE_COMPATIBLE_WITH_LOCAL_PARSER=PASS
REQUIRED_TENSOR_KEYS_COMPATIBLE=PASS
STAR7_STATIC_PARSE_PATH_COMPATIBLE=PASS
NO_FULL_STACK_UPGRADE_REQUIRED=PASS
```

才允许：

```text
W4A8_MATURE_FOR_BOUNDED_AB=YES
→ GPT may issue E2W download + paired A/B contract
```

任何关键 metadata 无法获得或解析冲突：

```text
W4A8_MATURE_FOR_BOUNDED_AB=NO
→ STOP / RETURN GPT
```

## 5. 当前排序

```text
1. E2M remote W4A8 metadata/header preflight — ZERO GPU / NO FULL DOWNLOAD
2. If PASS: E2W W4A8 + Star7 bounded paired A/B
3. If FAIL/INCONCLUSIVE: remove W4A8 from current queue
4. Then reconsider only remaining bounded candidates using E1/E2R facts
```

INT8 VAE 继续 `FALLBACK_ONLY`；host-sync/residency/TE candidates 继续 `NOT_MATURE`，因为 E2R 未提供机制归因。

## 6. 状态

```text
T_PHY_TOTAL_REFERENCE=0.23–0.57 s
REAL_STATE_OPTIMUM_RANGE=4–14 s
CURRENT_KEEP=STAR7
CURRENT_P50=10.562 s
E1_REPEAT=NO
E2R_ATTRIBUTION=INCONCLUSIVE
E2P_SM75_BEHAVIOR=FALLBACK_SUPPORTED
W4A8_CANDIDATE_MATURE=NO
NEXT=E2M_REMOTE_METADATA_PREFLIGHT
GPU_RUNS_ALLOWED_NEXT=0
FULL_MODEL_DOWNLOAD_ALLOWED_NEXT=NO
FINAL_99=NO
```
