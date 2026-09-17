# H3-P0 随机重采样直到通过：最终系统认证 v1

状态：`READY_TO_EXECUTE / FINAL_SYSTEM_CERTIFICATION`

方法：`first-principles-physical-limit-convergence v1.9.0`

系统候选：`STAR7_RESEED_UNTIL_PASS_V1`

## 1. 已冻结前提

已真实证明：

```text
RESEED_RECOVERY_PROOF=PASS
FINAL_ACCEPTED_QC=2/2
QUALITY_RETRY_LIMIT=NONE
STEP_REMAINS_1=YES
STAR7_ONLY=YES
```

两个已知失败起点 `930103`、`920108` 均在自动换用新的 OS 随机 seed 后，第 2 次 attempt 得到 QC PASS；失败输出未交付。

因此最终认证不再要求“任意固定 seed 第一次必须 PASS”，而认证完整生产语义：

```text
随机 seed
→ Star7 / 1-step
→ QC
→ PASS: ACCEPT
→ FAIL: reject + new random seed + retry
→ 直到首次 PASS
```

质量 retry **没有固定次数上限**。系统停止条件是 `QC PASS`，技术故障另行断路。

## 2. 质量硬约束

每个 ACCEPT 输出必须：

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

任何 FAIL 输出必须拒绝，禁止交付。

## 3. 最终认证样本

先做 2 个 warmup delivery task，不计正式统计；warmup 也必须使用随机 seed 和同一生产逻辑。

然后连续执行 **20 个独立正式 delivery task**。

每个正式任务：

1. 用 `secrets.randbits(63)` 或等价 CSPRNG 生成新的 seed；
2. 运行冻结 Star7 / 1-step；
3. 做完整 QC；
4. FAIL 时生成新的、全局未使用过的随机 seed 并重试；
5. 首次 PASS 时 ACCEPT 并结束该 task；
6. 下一个 task 再从新的随机 seed 开始。

不得人工选择历史 PASS seed，不得重复失败 seed，不得换 Loader、step、模型或 QC。

## 4. 技术断路器不是质量 retry 上限

生产质量 retry 不设次数上限。

仅以下系统性故障允许暂停认证并 checkpoint：

```text
GPU/ComfyUI crash
无法生成新的随机 seed
seed collision / RNG anomaly
磁盘/MP4输出链故障
Codex 控制面全模型 capacity 且路由器无法恢复
```

发生技术阻断：

```text
TASK_STATE=CHECKPOINTED
LOCAL_WORK_REPLAY=NO
```

恢复后从未完成 task 继续，不重复已完成 task。

## 5. Codex 容量路由器

本轮开始前只核验：

```text
CODEX_CAPACITY_ROUTER=ENABLED
STATIC_MODEL_LIST=NO
```

当前安装验收范围为 controlled mock；不得把 mock 写成真实服务 failover 已验证。

若真实 capacity 在本轮自然发生：允许按已安装路由器处理，并记录真实 route event；不得因此重跑已完成 H3 工作。

## 6. 统计

每个 attempt 保存：

```text
task_id
attempt_index
seed
Total
QC_time
frame range/std
MP4 SHA256
PASS/FAIL
```

每个 delivery task 保存：

```text
ATTEMPTS_TO_SUCCESS
DELIVERY_TOTAL
ACCEPTED_SEED
FINAL_ACCEPTED_QC
```

最终计算：

```text
TOTAL_TASKS=20
TOTAL_ATTEMPTS
FIRST_ATTEMPT_PASS_COUNT
FIRST_ATTEMPT_PASS_RATE
ATTEMPT_PASS_RATE = 20 / TOTAL_ATTEMPTS
MEAN_ATTEMPTS_PER_TASK
ATTEMPTS_P50/P95/MAX
DELIVERY_TOTAL_MEAN/P50/P95/MAX
SINGLE_ATTEMPT_TOTAL_P50/P95
INVALID_OUTPUTS_REJECTED
INVALID_OUTPUT_DELIVERED
```

说明：有限样本只提供工程认证和经验概率，不宣称数学上证明未来所有随机任务绝对 100% 终止。

## 7. 最终通过门槛

质量门槛：

```text
FINAL_ACCEPTED_QC = 20/20
INVALID_OUTPUT_DELIVERED = 0
EVERY_RETRY_USED_NEW_RANDOM_SEED = YES
NO_MANUAL_SEED_SELECTION = YES
STAR7_ONLY = YES
STEP_REMAINS_1 = YES
MODEL_AND_RUNTIME_UNCHANGED = YES
```

时间/效率门槛（稳态，warmup 排除）：

```text
MEAN_ATTEMPTS_PER_TASK <= 1.25
DELIVERY_TOTAL_P50 <= 10 s
DELIVERY_TOTAL_MEAN <= 12 s
DELIVERY_TOTAL_P95 <= 20 s
SINGLE_ATTEMPT_TOTAL_P50 <= 10 s
```

这些门槛对应质量约束下的最短时间目标：若单次成功率约 >=80%，理论平均 attempts <=1.25；当前历史观察成功率更高，但不把历史比例硬编码为 90%。

如果质量 20/20 PASS 但时间门槛失败：

```text
QUALITY_STABILITY_PROOF=PASS
TIME_99_UNDER_QUALITY_CONSTRAINT=FAIL
FINAL_QUALITY_STABILITY_99=NO
```

如果全部通过：

```text
QUALITY_STABILITY_PROOF=PASS
TIME_99_UNDER_QUALITY_CONSTRAINT=PASS
FINAL_RESEED_SYSTEM_CERTIFICATION=PASS
READY_TO_FREEZE_FINAL_99=YES
```

最终冻结仍需 Git push + remote verify。

## 8. 禁止事项

最终认证期间不得：

- 固定质量重试次数上限；
- 人工挑选 seed；
- 修改 Star7；
- Adaptive-Step；
- 原始 Loader fallback；
- ACT32；
- W4A8；
- 参数/版本搜索；
- profiler / kernel trace；
- 降低 QC。

本轮只认证一个系统：

```text
Star7 1-step + random reseed until QC PASS
```