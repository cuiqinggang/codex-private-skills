# H3-P0 质量稳定性 Adaptive-Step Virtual-99 v1

状态：`VIRTUAL_99_COMPLETE / ONE_REAL_CANDIDATE_SELECTED`

方法：`first-principles-physical-limit-convergence v1.9.0（第一性原理物理极限收敛引擎）`

## 1. 新事实

当前已冻结证据：

- Star7 1-step 在 `930103`、`920108` 上发生白/平坦 QC FAIL；
- ACT32 保留 INT8/ConvRot 且更快，但 `930103` 仍 FAIL，故精度边界修复不是主杠杆；
- `930103` 原始 UNETLoader 1-step PASS；
- `920108` 原始 UNETLoader 1-step 仍 FAIL，后四帧 `range=0 / std=0`；
- 因此 `920108` 证明：固定 1-step 合同本身对部分随机初始状态没有足够质量余量，失败不再能归因于 Star7/FP16。

正式结论：

```text
PRECISION_ONLY_ROOT_CAUSE = NO
ONE_STEP_QUALITY_FLOOR_EXISTS = YES
```

## 2. 第一性原理目标

质量仍是硬约束：

```text
final MP4 finite / decodable / non-black / non-flat
every frame range >= 8
every frame std >= 1.5
```

时间仍是唯一优化目标。

采样 step 是 denoising / trajectory correction 次数。1 step 是当前最短路径，但真实证据已证明它不是对所有 seed 都足够。最小时间策略因此不是把所有任务固定升到更多 step，而是：

```text
easy sample -> 1 step
fragile sample -> only after QC fail, increase to 2 steps
still fail -> only then increase to 3 steps
```

即 `MINIMUM_PASSING_STEP（最小通过步数）`。

## 3. Virtual-99 候选

唯一首选候选：

```text
CANDIDATE = STAR7_ADAPTIVE_MIN_STEP_V1
```

生产策略：

```text
Star7 / 1 step
→ QC
→ PASS: ACCEPT
→ FAIL: same seed Star7 / 2 steps
→ QC
→ PASS: ACCEPT
→ FAIL: same seed Star7 / 3 steps
→ QC
→ PASS: ACCEPT
→ FAIL: CONTROLLED_FAIL / RETURN POLICY LAYER
```

本候选：

- 保持 Star7 原始源码；
- 保持 INT8/ConvRot；
- 保持同 seed；
- 保持模型、prompt、sampler、scheduler、分辨率、帧数不变；
- 只在 QC 已证明 1-step 不足时增加 step；
- 不使用原始 UNETLoader；
- 不换 seed；
- 不降低 QC。

## 4. 为什么优先于重新 seed

重新 seed 可能更快，但改变随机初始条件。Adaptive-Step 首先尝试保持同 seed 与随机轨迹身份，因此信息保真更强。

只有若同 seed 3-step 仍不能通过，才允许 GPT 后续把 `re-seed fast retry` 作为下一独立系统候选。

## 5. 虚拟时间

已知 Star7 稳态 1-step 正常样本 Total 约 5.4–8.7 s，Generation 多数约 2–4.5 s。

step 增加主要增加 H3 denoiser forward 次数，Path/QC 不应线性翻倍。因此虚拟规划（不是认证数据）：

```text
2-step fallback Total ≈ 1-step Total + 1× additional Generation forward
3-step fallback Total ≈ 1-step Total + 2× additional Generation forward
```

预期同 seed 2-step 若能修复，困难样本总交付仍可能落在约 10–15 s 级，远低于当前 reference fallback 的约 90–105 s 单次运行和约 199–275 s DELIVERY_TOTAL。

## 6. 唯一真实证明

只使用两个已冻结的真实失败 seed：

```text
930103
920108
```

不重做它们的 1-step 失败；失败已经多次冻结。

对每个 seed：

1. Star7 2-step；
2. 若 QC PASS，记录 `MINIMUM_PASSING_STEP=2`，不跑 3-step；
3. 若 2-step QC FAIL，才运行同 seed Star7 3-step；
4. 若 3-step PASS，记录 `MINIMUM_PASSING_STEP=3`；
5. 若 3-step 仍 FAIL，则该候选失败。

质量 proof 最多 4 条正式 GPU；允许最多 2 条 2-step 预热，总 GPU 上限 6。

## 7. 候选通过条件

```text
930103 final QC PASS by step<=3
920108 final QC PASS by step<=3
same seed preserved = YES
Star7 source unchanged = YES
backend int8_tensorwise+convrot preserved = YES
force_cast_weights=False
no dense fallback
no crash
no auto retry outside frozen policy
```

若成立：

```text
ADAPTIVE_STEP_PROOF=PASS
READY_FOR_FULL_SYSTEM_CERTIFICATION=YES
FINAL_QUALITY_STABILITY_99=NO
```

若任一 seed 到 3-step 仍 FAIL：

```text
ADAPTIVE_STEP_PROOF=FAIL_QUALITY
STOP_RETURN_TO_GPT
```

不得现场增加 4/5/6 step，不得换 seed，不得引入第二候选。

## 8. Virtual-99 裁决

```text
VIRTUAL_99_COMPLETE=YES
PRIMARY_REAL_CANDIDATE=STAR7_ADAPTIVE_MIN_STEP_V1
ACT32=REJECTED_QUALITY
REFERENCE_FALLBACK=REJECTED_AS_PRIMARY_AND_NOT_QUALITY_COMPLETE
RESEED_FAST_RETRY=DEFERRED_NEXT_INDEPENDENT_CANDIDATE_IF_NEEDED
NO_FREE_EXPLORATION=YES
READY_FOR_BOUNDED_REAL_PROOF=YES
FINAL_QUALITY_STABILITY_99=NO
```
