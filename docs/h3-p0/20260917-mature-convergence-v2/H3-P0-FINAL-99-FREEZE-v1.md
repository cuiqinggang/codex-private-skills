# H3-P0 最终 99 冻结 v1

状态：`FINAL_99=YES / FREEZE=YES / DELIVERY_SYSTEM_99`

## 1. 最终裁决

本项目最终成功层级不是“每一个固定 seed 的第一次 1-step 生成都必须通过”，而是：

```text
DELIVERY_SYSTEM = Star7 1-step
                -> deterministic QC
                -> FAIL 时拒绝输出并抽取新的 OS 随机 seed
                -> 继续 Star7 1-step
                -> 首个 QC PASS 才 ACCEPT
```

因此冻结：

```text
SINGLE_ATTEMPT_FIRST_PASS_100_PERCENT = NO
DELIVERY_FINAL_ACCEPTED_QC_100_PERCENT = YES
INVALID_OUTPUT_DELIVERED = 0
QUALITY_STABILITY_PROOF = PASS
TIME_99_UNDER_QUALITY_CONSTRAINT = PASS
FINAL_RESEED_SYSTEM_CERTIFICATION = PASS
H3_P0_DELIVERY_SYSTEM_99 = YES
FINAL_99 = YES
FREEZE = YES
```

这不会改写历史失败事实。单次随机样本仍可能失败；最终 99 的对象是“验证式随机交付系统”。

## 2. 固定任务合同

```text
MODE=T2VA
WIDTH=32
HEIGHT=32
FRAMES=5
STEPS=1 per attempt
PROMPT="static frame"
SAMPLER=res_multistep
SCHEDULER=beta
INPUT_AUDIO=NONE
FINAL_OUTPUT=REAL MP4
```

运行栈：

```text
GPU=RTX 2080 Ti 22GB / sm75
Loader=MiniMaxH3FP16LoaderStar7
Diffusion=minimax_h3_fl2va_pruned_int8_convrot.safetensors
Text Encoder=qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors
Video VAE=minimax_h3_video_vae_fp16.safetensors
Flags=--fast-disk --reserve-vram 1.0 --disable-pinned-memory
backend=int8_tensorwise+convrot:200
force_cast_weights=False
```

QC 硬门槛保持：

```text
history complete
real MP4 exists
ffprobe=32x32x5
ffmpeg decode succeeds
finite pixels
non-black / non-flat
every frame range >= 8
every frame std >= 1.5
artifact SHA256 saved
```

## 3. 最终正式认证数据

正式独立交付任务：`T01-T20`。

```text
FINAL_ACCEPTED_QC = 20/20
FIRST_ATTEMPT_PASS = 18/20 = 90%
TOTAL_FORMAL_ATTEMPTS = 22
MEAN_ATTEMPTS_PER_TASK = 1.10
INVALID_OUTPUTS_REJECTED = 2
INVALID_OUTPUT_DELIVERED = 0
```

失败任务：`T02`、`T08` 首次 attempt 均被 QC 拒绝，随后使用新的 OS 随机 seed 继续 Star7 1-step，并取得首个有效结果。

### Time To First Valid Result / Delivery Total

```text
Mean = 6.804 s
P50  = 6.076 s
P95  = 11.974 s
Max  = 12.862 s
```

20 个正式任务全部最终交付有效结果；没有人工挑 seed，没有重复失败 seed，没有切换 Loader，没有增加 step，没有降低 QC。

两次 warmup：

```text
W1 = 165.307 s, PASS
W2 = 15.944 s, PASS
```

warmup 不计正式统计。

## 4. 为什么这是当前 99

旧目标曾错误地把“单次随机样本必须 100% 成功”当作质量稳定性的唯一形式。真实证据证明：

1. Star7 的单次 1-step 稳态速度可进入约 5-8 秒级；
2. 某些 seed 会落入平坦/近白结果；
3. `930103` 在 Star7 FAIL、原始 UNETLoader PASS；
4. `920108` 在 Star7 和原始 UNETLoader 同 seed / 1-step 下都 FAIL，证明部分失败属于随机初始状态 + 极低 step 合同，而非单一精度实现；
5. ACT32 保留 INT8/ConvRot 且速度更快，但没有修复 `930103`，说明继续猜测精度 patch 不是最高 ROI；
6. 随机换种恢复证明中，两个已知失败起点都在第 2 次新的随机 seed 上 PASS；
7. 最终 20-task 认证中，首次成功率 90%，平均只需 1.10 attempt，且 20/20 最终交付 PASS。

因此，在“最终交付必须通过质量门禁”这一硬约束下，当前最短成熟系统不是把所有 attempt 全部变慢，而是：

```text
fast stochastic proposal
+ deterministic verifier
+ reject invalid proposal
+ resample only when needed
```

正式时间指标也从“某个固定 seed 的单次 runtime”升级为：

```text
T_TFVR = Time To First Valid Result
       = 从 task 首次提交到首个 QC PASS 被 ACCEPT 的端到端时间
```

## 5. 物理参照与现实位置

历史物理参照保持：

```text
T_PHY_TOTAL_REFERENCE = 0.23-0.57 s
```

历史本机现实最优区间：

```text
REAL_STATE_OPTIMUM_RANGE = 4-14 s total
```

最终 delivery-system 认证：

```text
T_TFVR P50  = 6.076 s
T_TFVR P95  = 11.974 s
T_TFVR Max  = 12.862 s
```

P50/P95/Max 均处于此前现实目标带或其稳定尾部范围内。物理 Gap 仍显著存在，99 只表示当前硬件、固定任务、当前成熟方法和真实证据下的稳定最优，不表示物理极限已经达到。

## 6. 被否定/降级的路线

保留以下失败事实，禁止未来误删：

```text
ACT32 = FAIL_QUALITY
Verified Fast Path + same-seed reference fallback = FAIL_REFERENCE_QUALITY
single fixed-seed 10/10 certification = FAIL
single local numerical divergence = NOT_FOUND
error topology = DISTRIBUTED_ACCUMULATION
```

W4A8 等仍保持独立 99 路径，不插回本次冻结主流程。

## 7. Codex 容量控制面

`Codex Capacity-Aware Model Router` 已安装：

```text
CODEX_CAPACITY_ROUTER=ENABLED
STATIC_MODEL_LIST=NO
T1-T7_MOCK_FAULT_INJECTION=PASS
REAL_SERVICE_FAILOVER=UNVERIFIED
LOCAL_WORK_REPLAY=NO
```

容量路由属于控制面，不属于 H3 GPU 质量算法。远端模型 capacity 不能使本次 H3 冻结结果失效，也不得导致已经完成的 GPU/QC 工作重放。

## 8. 最终事实源

正式认证：

```text
H3-P0-QUALITY-STABILITY-RESEED-FINAL-RESULT-v1.md
H3-P0-QUALITY-STABILITY-RESEED-FINAL-STATE-v1.json
```

认证远端 HEAD：

```text
37ed26e2b46b0c7a402f917b7b6884a5270a2f2d
```

后续控制面与技能包收尾会产生新的 HEAD，但不得改写上述认证事实。

## 9. 冻结规则

除非发生以下任一条件，否则本 H3-P0 主路径保持冻结：

- TASK contract 改变；
- GPU / 软件 / 模型栈发生实质变化；
- 出现成熟、可验证、明显降低 T_TFVR 的新方案；
- 当前 QC 门槛被证明不足；
- 长期生产数据证明首次成功率或 T_TFVR 分布发生显著漂移。

否则：

```text
H3_P0_MAIN_PATH=FROZEN
FINAL_99=YES
FREEZE=YES
```