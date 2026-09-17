# H3-P0 质量稳定性 Re-seed Until Pass Virtual-99 v1

状态：`VIRTUAL_99_COMPLETE / PRIMARY_SYSTEM_CANDIDATE_SELECTED`

方法：`first-principles-physical-limit-convergence v1.9.0（第一性原理物理极限收敛引擎）`

## 1. 目标函数

硬约束：任何最终交付 MP4 必须通过既有 QC；失败结果绝不交付。

唯一优化目标：在上述质量硬约束下，最小化获得第一个合格结果的端到端时间。

```text
QUALITY_STABILITY = HARD_CONSTRAINT
TIME_TO_FIRST_ACCEPTED_RESULT = ONLY_OPTIMIZATION_TARGET
```

## 2. 已冻结现实证据

- Star7 1-step 稳态快路径约 5–8 s 级；
- 已知部分 seed 会在 Star7 下产生白/平坦结果；
- `930103`：Star7 FAIL，原始 UNETLoader PASS；
- `920108`：Star7 FAIL，原始 UNETLoader 同 seed 也 FAIL；
- 因此部分失败属于随机初始状态 / 当前 1-step 合同下的坏采样区域，而不只是 Star7 精度路径问题；
- ACT32 已真实证明不能修复 `930103`；
- 原始 Loader fallback 对 `920108` 也失败，且成本约 90–100 s；
- seed 不是任务语义本身，而是随机采样初始条件；用户任务是获得一个合格视频，而不是必须复现某个固定 seed。

## 3. 第一性原理裁决

对于随机生成系统，如果一次独立随机采样成功概率为 `p`，则连续 `n` 次独立采样仍失败概率为：

```text
P(all fail after n tries) = (1-p)^n
```

达到第一个成功样本的期望尝试次数：

```text
E[tries] = 1 / p
```

因此当 `p` 较高时，最短质量稳定策略不是把每一次都变慢，而是保留最快单次路径并在 QC FAIL 后重新随机采样。

生产系统停止条件应是：

```text
QC PASS
```

而不是固定重试次数。

## 4. 选中系统候选

候选：

```text
STAR7_RESEED_UNTIL_PASS_V1
```

生产逻辑：

```text
new random seed
→ Star7 / 1-step
→ QC
→ PASS: ACCEPT and stop
→ FAIL: reject output, draw a new random seed, repeat
```

规则：

- 每次失败后必须生成新的随机 seed；
- 禁止重复使用已失败 seed；
- 不允许把无效输出交付给用户；
- 不降低 QC；
- 不改变模型、sampler、scheduler、step、分辨率、帧数；
- 不切换原始 Loader；
- 不增加 inference step；
- 质量重试次数不设固定上限；
- 只允许技术断路器处理系统性故障，例如 ComfyUI/GPU 崩溃、随机种子生成器异常、重复 seed、无法继续提交任务。

## 5. 为什么高于 Adaptive-Step 与慢 fallback

### Re-seed Until Pass

失败时只支付另一条约 5–8 s 级 Star7 快跑。

### Adaptive-Step

失败后增加 denoiser forward 次数，单次成本系统性上升；尚未证明是必要的。

### 原始 Loader fallback

已实测约 90–100 s，并且 `920108` 同 seed 仍失败，因此既慢又不能保证质量。

裁决：

```text
PRIMARY = STAR7_RESEED_UNTIL_PASS_V1
ADAPTIVE_STEP = DEFERRED
REFERENCE_FALLBACK = REJECTED_AS_PRIMARY
ACT32 = REJECTED
```

## 6. 概率与时间 Virtual 估算

现有样本不足以发布正式长期失败率，但若用于规划：

- 单次成功率 90%：期望尝试次数约 1.11；
- 单次成功率 87.5%：期望尝试次数约 1.14；
- 单次成功率 80%：期望尝试次数 1.25。

若稳态单次约 6.5 s，则对应期望生成时间约：

```text
p=0.90  → 约 7.2 s
p=0.875 → 约 7.4 s
p=0.80  → 约 8.1 s
```

以上为 Virtual 规划值，不是正式认证结果。

## 7. 实证策略

生产逻辑不设质量重试次数上限，但实证阶段必须是有限实验。

第一阶段只验证“自动从已知失败状态恢复”的机制：

- task A 初始 seed = 930103；
- task B 初始 seed = 920108；
- 初始 seed 失败后，不再使用原 seed；
- 自动生成全新随机 seed，并持续 Star7 1-step + QC，直到该任务首次 PASS；
- 记录完整 DELIVERY_TOTAL、尝试次数、全部 seed、每条 QC。

这不是给生产系统设置上限；只是有限证明自动随机重采样可以从已知坏样本恢复。

## 8. 后续最终认证

若恢复证明 PASS，再进入独立最终系统认证：多条独立 delivery task，每条都采用 `retry until QC PASS`；统计：

- first-try success rate；
- attempts per delivery；
- DELIVERY_TOTAL P50/P95/Max；
- accepted QC 100%；
- invalid output delivered = NO。

最终 99 看的是：

```text
FINAL_DELIVERY_QC = 100%
INVALID_OUTPUT_DELIVERED = NO
TIME_TO_FIRST_ACCEPTED_RESULT = 当前可实现稳定最优
```

而不是“每一个随机 seed 第一次必须成功”。

## 9. Virtual-99 裁决

```text
VIRTUAL_99_COMPLETE=YES
PRIMARY_REAL_CANDIDATE=STAR7_RESEED_UNTIL_PASS_V1
QUALITY_RETRY_LIMIT=NONE
STOP_CONDITION=QC_PASS
TECHNICAL_CIRCUIT_BREAKER=YES
NO_FREE_EXPLORATION=YES
READY_FOR_BOUNDED_RECOVERY_PROOF=YES
FINAL_QUALITY_STABILITY_99=NO
```
