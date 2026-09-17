# H3-P0 Post-E1 Residual Virtual Convergence v1

状态：`RESIDUAL_VIRTUAL_CONVERGENCE_COMPLETE=YES / NEXT_GPU_STAGE_NOT_YET_UNLOCKED`

方法：`first-principles-physical-limit-convergence v1.8.0`

## 1. E1 完整性裁决

E1 `Star7 Native FP16 Exact` 本身完整通过冻结合同：

- E0 control + E1 candidate 各 1 warmup + 3 formal，共 8 GPU runs；
- fixed task / seeds / timing / QC 不变；
- 唯一性能变量为 diffusion loader；
- Star7 sm75 protected FP16、quantized checkpoint、`force-cast=False`、INT8/ConvRot preserved 均有日志证明；
- 8/8 MP4/QC PASS；
- source/workflow restore proof 完整；
- remote push + remote verify PASS；
- E2 未自动执行。

因此：

```text
E1_VALIDATION_COMPLETE=YES
E1_DECISION=KEEP
REPEAT_E1_REQUIRED=NO
```

## 2. E1 真实新状态

同窗口 P50/P95：

```text
CONTROL
Generation = 20.102 / 23.707 s
Path       = 18.654 / 18.905 s
Total      = 38.816 / 41.993 s

STAR7
Generation = 3.102 / 10.677 s
Path       = 3.430 / 7.626 s
Total      = 10.562 / 14.510 s
```

P50：

```text
TOTAL_GAIN = 28.254 s = 72.79%
GEN_GAIN   = 17.000 s = 84.57%
PATH_GAIN  = 15.224 s = 81.61%
```

Formal seed decomposition：

```text
910100: G=11.519, P=3.430, T=14.949 s
910102: G= 3.102, P=3.382, T= 6.484 s
910103: G= 2.470, P=8.092, T=10.562 s
```

含义：同一个 KEEP 栈已经真实展示 `6.484 s` fast path，但慢尾分别可能落在 Generation 或 Path，不再是原 38 s 基线中的单一巨大固定块。

## 3. 对 STEP 1 / STEP 2 的影响

```text
T_PHY_TOTAL_REFERENCE = 0.23–0.57 s
```

不变。

原 `REAL_STATE_OPTIMUM_RANGE = 4–14 s Total P50` 没有被推翻：E1 P50=10.562 s 已真实进入该带；E1 fast sample=6.484 s 进一步证明该带不是纯纸面假设。

当前只升级 REAL_STATE_MODEL：

```text
CURRENT_KEEP_WINNER = STAR7
CURRENT_TOTAL_P50   = 10.562 s
CURRENT_TOTAL_P95   = 14.510 s
CURRENT_FAST_VALID  = 6.484 s
CURRENT_PROBLEM     = TAIL_VARIANCE / RESIDENCY-SCHEDULING ATTRIBUTION
```

现在不宜仅凭 3 formal samples把 4–14 s 再缩成更窄的正式现实极限带；最终稳定区间要等下一轮候选与 Final Certification。

## 4. 原 Virtual-99 哪些假设已失效

旧 Step3 对 A1 Star7 规划只有约 `2–6 s` Total 收益，真实为 `28.254 s`。这说明 Star7 不只降低 Generation dtype/manual-cast，还显著改变了模型生命周期/驻留/路径行为。

因此旧的后续增量不能继续机械使用：

```text
A2 W4A8 old expected +6–12s    = INVALIDATED
A3 cache old expected +4–10s   = INVALIDATED
A4 INT8 VAE old expected +2–6s = INVALIDATED
R1/R2 old projected bands      = MUST_REBASE
```

所有剩余候选必须从 `10.562 s P50 / 14.510 s P95` 新赢家重新计算。

## 5. 外部成熟方案重新筛选

### 5.1 W4A8 diffusion — 从 HIGH_VALUE 降级为 BLOCKED_CURRENT_IMPLEMENTATION

文件候选 `minimax_h3_fl2va_pruned_w4a8_mixed.safetensors` 约 12.5GB 确实存在；但当前公开成熟实现存在关键硬件/平台边界：

- comfy-kitchen `AsymW4A8Int8Layout` 当前原生实现声明 `MIN_SM_VERSION=(8,0)`；
- 独立 `ComfyUI-W4A8-Loader` 当前兼容表要求 NVIDIA SM80+，测试 RTX4090，并明确 Windows installer 不支持；
- 本机是 Windows + RTX 2080 Ti / sm75；
- Star7 可保留 `asym_w4a8_int8` 调度，不能替代底层 SM75 W4A8 kernel 缺口。

因此：

```text
A2_W4A8_CURRENT_STATUS=NOT_APPLICABLE_WITH_VERIFIED_MATURE_IMPLEMENTATION
UNLOCK_OLD_E2=NO
```

只有未来找到并核验 `Windows + sm75` 的成熟 W4A8 implementation 后才重新入队。

### 5.2 INT8 ConvRot Video VAE — 降级

公开仍有 `RTX 2080 Ti 22GB` 上 INT8 ConvRot VAE black/NaN/Inf 的未解决报告；与此同时 E1 后 Path P50 已仅 3.430 s。

因此：

```text
A4_INT8_VAE=HIGH_RISK_LOW_REMAINING_HEADROOM
STATUS=FALLBACK_ONLY
```

当前不值得立即用一轮 GPU 冒险。

### 5.3 Conditioning / Text Encoder — 先归因再决定

本机仍用 `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors`。公开硬件指南指出 NVFP4-AWQ 原生主要面向 Blackwell；旧 NVIDIA/Turing 应优先 INT8 ConvRot text encoder，因为 NVFP4 在旧卡上是 emulated path。

但 P0 prompt 固定，ComfyUI node cache 可能已经完全跳过重复 conditioning。

所以先判断 E1 formal runs 是否真正重复执行 Qwen conditioning：

```text
IF CONDITIONING_CACHED:
    CACHE / TE FORMAT gain≈0 for steady P0
    DO NOT GPU TEST
ELSE:
    TE_INT8_CONVROT becomes a mature hardware-matched candidate
```

### 5.4 Host-sync targeted patch

当前 Generation P50=3.102 s 已进入 STEP2 的 2–5 s 规划带，但 P95=10.677 s。

上游 H3 `_forward` 的 scalar D2H / `tolist()` sync 机制仍真实存在，但本任务仅 1 step；因此它从“大头”改为**尾部条件候选**：只有只读归因排除 residency/loading 后才进入。

## 6. 新的 residual priority

```text
R0 = E1 KEEP winner

NEXT = E2R READ-ONLY TAIL ATTRIBUTION
  - ZERO GPU RUNS
  - NO NEW INSTRUMENTATION
  - inspect existing E1 logs/evidence only

THEN conditional:
  B1 = INT8 ConvRot text encoder, only if conditioning actually reruns / contributes material Path
  B2 = one predefined Star7-era residency policy, only if existing evidence attributes tail to residency
  B3 = minimal H3 host-sync patch, only if Generation tail remains after residency attribution
  B4 = INT8 VAE fallback only if a verified sm75-safe fix appears and Path remains material

W4A8 = blocked until verified sm75/Windows implementation exists
```

## 7. Post-E1 Virtual-99 projection

因为 E1 已出现 `6.484 s` 有效样本，后续目标从“砍大头”变成“让更多样本稳定靠近 fast path”。

不再伪造 6–12 秒额外收益。新的保守规划：

```text
CURRENT_P50 = 10.562 s
CURRENT_P95 = 14.510 s
CURRENT_FAST_VALID = 6.484 s

POST_E1_RESIDUAL_CENTRAL_TARGET = 6–9 s P50
POST_E1_RESIDUAL_WIDE_TARGET    = 5–11 s P50
PRIMARY_RESIDUAL_OBJECTIVE      = reduce tail / stabilize residency and scheduling
```

这些仍是 Virtual planning bands，不是 PASS threshold。

## 8. 当前停止/继续裁决

```text
FINAL_99=NO
E1_REPEAT=NO
OLD_E2_W4A8_UNLOCK=NO
RESIDUAL_VIRTUAL_CONVERGENCE_COMPLETE=YES
NEXT_GPU_CANDIDATE=NOT_YET_SELECTED
NEXT_ACTION=E2R_READ_ONLY_ATTRIBUTION
```

原因：E1 已经达到极高收益并进入现实目标带，但三条样本的瓶颈位置不同。直接再跑一个模型候选会把归因和候选收益混在一起；先用已有日志做零成本归因，符合最短工程时间和 NO_FREE_EXPLORATION。
