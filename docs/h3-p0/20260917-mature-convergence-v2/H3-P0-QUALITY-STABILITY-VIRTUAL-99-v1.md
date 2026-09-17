# H3-P0 质量稳定性 Virtual-99 v1

状态：`VIRTUAL_99_COMPLETE / ONE_REAL_CANDIDATE_SELECTED`

方法：`first-principles-physical-limit-convergence v1.9.0（第一性原理物理极限收敛引擎）`

## 1. 目标函数

硬约束：最终 MP4 必须通过既有 QC；不允许为了速度降低 `range>=8 / std>=1.5 / finite / 可解码 / 非黑 / 非平坦`。

唯一优化目标：在质量稳定约束成立时，最小化端到端时间。

```text
QUALITY_STABILITY = HARD_CONSTRAINT
TIME = ONLY_OPTIMIZATION_TARGET
```

本阶段先证明一个最小修复候选能够同时：

1. 修复已知 Star7 质量失败 seed；
2. 不破坏已知通过 seed；
3. 保留 INT8/ConvRot 快速权重路径；
4. 时间增量尽量 <=15% 且 <=1.0 s（以可配对稳态样本为准）。

## 2. 已冻结现实证据

最终定位结果：

```text
ERROR_TOPOLOGY=DISTRIBUTED_ACCUMULATION
FIRST_DIVERGENCE=NO_SINGLE_LOCAL_DIVERGENCE
CONFIDENCE=MEDIUM
```

已知事实：

- `930103`：Star7 FAIL，原始 UNETLoader PASS；
- `930100`：两条路径均 PASS；
- block 14 MLP 有局部峰值，但未持续到最终 residual，不能作为单点根因；
- 50 层 residual 误差呈跨层传播/累积，而非唯一单点跳变；
- FinalLayer / Pre-VAE 的相对误差大小本身不能区分 FAIL/PASS seed；
- Star7 残差流已为 FP32；主要分支计算仍反复把激活压到 FP16；
- `int8_tensorwise + ConvRot` 的 comfy-kitchen fast path 在 SM75/Turing 可用，线性算子允许 FP32 input/output dtype，同时权重保持 INT8。

因此，当前问题不是“某一层溢出”，而是：

```text
50层内多个 FP32 -> FP16 激活截断
+ INT8 动态激活量化
+ Attention / MLP 分支传播
=> 有限误差跨层累积
=> 对接近白色阈值的脆弱 seed，最终跨过 QC 平坦阈值
```

## 3. Virtual-99 候选裁决

### A. ACT32：FP32 激活边界 + INT8/ConvRot 权重快核

裁决：`SELECTED / REAL_PROOF_REQUIRED`

原则：

- 不改模型；
- 不改 INT8/ConvRot 权重；
- 不关闭量化；
- 不改 sampler / scheduler / seed / step；
- residual 继续 FP32；
- 保留 power-of-two overflow scaling；
- 只消除 Star7 在每个 block 分支入口和量化线性投影入口处的额外 FP16 截断；
- INT8 linear 从 FP32 激活值开始做动态 row-wise activation quantization，并输出 FP32；
- optimized attention 主体仍允许在 FP16 执行，避免把整个 attention 退回 FP32。

目标边界：

```text
norm/mod -> qkv_proj          : FP32 activation into INT8 linear
attention core                : FP16 allowed
attention out -> out_proj     : scale in FP32, FP32 into INT8 linear, FP32 out
norm/mod -> fc1               : FP32 activation into INT8 linear
SwiGLU                        : FP32（原本已是）
scaled activation -> fc2      : FP32 into INT8 linear, FP32 out
residual add                  : FP32（原本已是）
```

第一性原理理由：这同时作用于 50 层的分布式误差源，但不改变占主要权重体积和矩阵乘路径的 INT8/ConvRot 权重快核，是“质量约束下最小时间损失”的最高 ROI 候选。

### B. 仅 block14 高精度

裁决：`REJECTED_AS_PRIMARY`

原因：block14 局部误差峰值未持续到最终 residual；无法解释全部分布式误差。

### C. 仅后半段 blocks 15–49 高精度

裁决：`DEFERRED`

原因：可能降低成本，但当前误差源不是严格从 block15 才产生；在质量100%硬约束下，先验证全局激活边界修复更合理。只有 ACT32 质量成功但时间成本过高时，才允许未来独立研究缩小保护范围。

### D. 全量原始精度 / 原始 UNETLoader

裁决：`SAFETY_BASELINE_ONLY`

质量参考有效，但约 20 s Generation / 38–40 s Total 级别，不符合当前质量约束下最短时间目标。

### E. Star7 + QC + 原始 Loader fallback

裁决：`SECONDARY_SAFETY_PATH`

保留为保障方案。如果 ACT32 不能以低成本稳定修复，再启用此系统级兜底；不在当前首选实测中执行。

## 4. 虚拟时间预估

ACT32 不改变 INT8/ConvRot 权重与 W8A8 主矩阵乘，只增加激活 FP32 保存/转换与部分 FP32 前后处理。固定 P0 任务的 activation 规模很小，权重/量化线性仍是主路径。

因此 Virtual 规划区间（不是实测认证）：

```text
ACT32 Generation steady-state ≈ 当前 Star7 × 1.05–1.20
ACT32 Total steady-state      ≈ 6–10 s
```

高价值通过目标：

```text
paired median Total regression <= 15%
and paired median absolute regression <= 1.0 s
```

若质量完全修复但性能回退超过该门槛，则不直接冻结；返回 GPT 评估是否值得做保护范围缩减。

## 5. 唯一实测候选

当前只允许实测：

```text
CANDIDATE = STAR7_ACT32_INT8_CONVROT
```

不允许同期测试：

- block14-only；
- late-block-only；
- BF16；
- W4A8；
- INT8 VAE；
- cache；
- host-sync；
- 新模型；
- 参数 sweep；
- 版本 sweep。

## 6. 成功定义

候选证明阶段必须同时满足：

```text
known fragile seeds repaired = YES
known pass seeds remain PASS = YES
backend remains int8_tensorwise+convrot = YES
force_cast_weights = FALSE
no weight dequantization fallback = YES
paired median Total regression <= 15%
paired median absolute regression <= 1.0 s
```

若通过：`ACT32_PROOF=PASS`，随后再进入最终 10-run 质量稳定性认证。

若失败：`ACT32_PROOF=FAIL`，恢复源码并 STOP，返回 GPT；不得自行测试 B/C/D/E。

## 7. Virtual-99 裁决

```text
VIRTUAL_99_COMPLETE=YES
PRIMARY_REAL_CANDIDATE=STAR7_ACT32_INT8_CONVROT
SECONDARY_SAFETY_PATH=STAR7_QC_THEN_REFERENCE_FALLBACK
NO_FREE_EXPLORATION=YES
READY_FOR_BOUNDED_REAL_PROOF=YES
FINAL_QUALITY_STABILITY_99=NO
```
