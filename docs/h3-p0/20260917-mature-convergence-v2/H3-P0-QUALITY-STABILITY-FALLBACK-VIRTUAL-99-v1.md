# H3-P0 质量稳定性 Verified Fast Path Virtual-99 v1

状态：`VIRTUAL_99_COMPLETE / SYSTEM_CANDIDATE_SELECTED / REAL_PROOF_REQUIRED`

方法：`first-principles-physical-limit-convergence v1.9.0（第一性原理物理极限收敛引擎）`

## 1. 进入本阶段的事实

ACT32 已真实验证失败：

```text
ACT32_PROOF=FAIL_QUALITY
930103_REPAIRED=NO
backend=int8_tensorwise+convrot:200
force_cast_weights=False
```

这说明“全局 FP32 激活边界 + 保留 INT8/ConvRot”不是当前质量稳定性的有效修复杠杆。

最终定位已冻结：

```text
ERROR_TOPOLOGY=DISTRIBUTED_ACCUMULATION
FIRST_DIVERGENCE=NO_SINGLE_LOCAL_DIVERGENCE
CONFIDENCE=MEDIUM
```

因此不再派生 ACT32-v3、block14-only、late-block-only 或其他精度组合。

## 2. 第一性原理重新定义

最终目标不是要求某一个近似计算路径对所有 seed 永远一次成功；有限测试也无法证明数学意义的“所有未来 seed 100%”。

工程目标改为：

```text
FINAL_DELIVERED_OUTPUT_QC_PASS = HARD_CONSTRAINT
INVALID_OUTPUT_MUST_NEVER_BE_DELIVERED
EXPECTED_DELIVERY_TIME = MINIMIZE
```

也就是把“质量稳定性”定义在完整生产系统上，而不是定义在单个 Star7 内核上。

## 3. 当前系统候选

唯一候选：

```text
VERIFIED_FAST_PATH_V1
```

流程：

```text
requested seed
→ Star7 fast path
→ QC
   ├─ PASS → ACCEPT / DELIVER
   └─ FAIL → same-seed original UNETLoader reference path
              → QC
              ├─ PASS → ACCEPT / DELIVER
              └─ FAIL → CONTROLLED_FAIL / DO NOT DELIVER
```

当前 v1 不允许自动换 seed；如果将来 reference 同 seed 也出现失败，再由 GPT 单独决定是否需要第三层 deterministic seed rollover（确定性换 seed）路径。当前不提前增加复杂度。

## 4. 为什么这是当前最高 ROI 路线

已知 Star7 稳态正常样本约 5.4–8.7 秒；已知两个质量失败 seed 为 `920108` 与 `930103`。

独立 seed 粗样本中，Star7 已观察到约 14 PASS / 2 FAIL（16 个不同 seed，观察失败率约 12.5%；仅作 Virtual 规划，不当作长期真实概率）。

若快路径约 6.5 秒、reference fallback 约 39 秒，则虚拟长期平均：

```text
E[T] ≈ 6.5 + 0.125 × 39 ≈ 11.4 s
```

仍落在此前本机现实总时间目标 `4–14 s` 内。真实系统时间必须由下一步完整链路实测替换。

## 5. 仍缺的关键证据

- `930103`: Star7 FAIL、同 seed reference PASS 已多次实证。
- `920108`: Star7 FAIL 已实证，但同 seed reference 尚未正式验证。
- 生产系统的真实 `DELIVERY_TOTAL`（含 Star7、QC、必要的 reference fallback、第二次 QC）尚未实测。

因此下一步只做一个 bounded fallback proof（有限兜底证明），不做最终10次认证。

## 6. Fallback Proof 通过条件

使用两个已知 Star7 失败 seed：

```text
930103
920108
```

每个 seed 执行完整生产链：

```text
Star7 → QC → 若 FAIL → same-seed original UNETLoader → QC
```

通过必须：

```text
FINAL_ACCEPTED_QC=2/2
930103_FALLBACK_PASS=YES
920108_FALLBACK_PASS=YES
INVALID_OUTPUT_DELIVERED=NO
NO_SEED_CHANGE=YES
NO_MANUAL_INTERVENTION=YES
```

并记录：

```text
FAST_TOTAL
FAST_QC_TIME
REFERENCE_TOTAL (if triggered)
REFERENCE_QC_TIME (if triggered)
DELIVERY_TOTAL = 从首次 Star7 POST 前到最终被 QC 接受
```

## 7. 后续裁决

若 fallback proof PASS：

```text
VERIFIED_FAST_PATH_PROOF=PASS
READY_FOR_SYSTEM_TIME_ROI_RECALC=YES
```

返回 GPT，依据真实 fallback 时间和既有 Star7 失败率证据重新计算质量约束下的现实最优时间，再决定是否进入最终 10-run 系统认证。

若任一 same-seed reference 仍 FAIL：

```text
VERIFIED_FAST_PATH_PROOF=FAIL_REFERENCE_QUALITY
```

停止并返回 GPT；不得自行换 seed 或增加第三层策略。

## 8. 禁止事项

本阶段禁止：

- ACT32-v3 或其他精度 patch；
- block14-only / late-block-only；
- W4A8 / BF16 / VAE / cache / host-sync；
- 参数 sweep / 版本 sweep；
- profiler / kernel trace；
- 自动换 seed；
- 为通过而降低 QC。

```text
one system candidate
one bounded proof
one verdict
```
