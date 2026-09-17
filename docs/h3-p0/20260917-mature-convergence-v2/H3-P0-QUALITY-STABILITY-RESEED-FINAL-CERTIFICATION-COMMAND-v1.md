# H3-P0 随机重采样系统最终认证命令 v1

状态：`READY_TO_EXECUTE`

## 0. 入口

先读取：

```text
docs/h3-p0/20260917-mature-convergence-v2/H3-P0-QUALITY-STABILITY-RESEED-FINAL-CERTIFICATION-v1.md
```

严格执行，不重新设计。

## 1. 控制面预检

核验：

```text
C:\AI\Codex-Capacity-Router\reports\ACCEPTANCE.json
```

必须至少满足：

```text
CODEX_CAPACITY_ROUTER=ENABLED
STATIC_MODEL_LIST=NO
```

真实服务 failover 当前可为未验证；只需准确记录，不得阻断 H3，除非本轮真实发生 capacity 且无法恢复。

## 2. H3 冻结身份

保持冻结环境：

```text
Star7 nodes.py SHA256 = 8F6D3EB42D5123A36A814F3EFE6910D499CDF618E190DE74F3BCA0D5935E232B
ComfyUI commit = 8a33128f2f8c5585c57486c07de481241e70a39c
Diffusion = minimax_h3_fl2va_pruned_int8_convrot.safetensors
Text Encoder = qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors
Video VAE = minimax_h3_video_vae_fp16.safetensors
Flags = --fast-disk --reserve-vram 1.0 --disable-pinned-memory
backend = int8_tensorwise+convrot
force_cast_weights = False
```

固定任务：

```text
T2VA
32x32
5 frames
1 step
prompt=static frame
sampler=res_multistep
scheduler=beta
no input audio
real MP4
```

不得修改源码、模型、step、sampler、scheduler、QC。

## 3. 随机种子账本

使用系统 CSPRNG：

```text
secrets.randbits(63)
```

或严格等价实现。

建立全局 `used_seeds`；所有 warmup、正式 task、retry seed 均不得重复。

不得人工挑历史已知 PASS seed。

## 4. 两个 warmup delivery task

先执行 W1/W2，不计正式统计。

每个 warmup 也严格运行完整系统：

```text
new random seed
→ Star7 1-step
→ QC
→ FAIL 则 new random seed 重试
→ 首次 PASS 停止
```

warmup 失败 attempt 也保存证据。

## 5. 20 个正式 delivery task

连续执行：

```text
T01 ... T20
```

每个 task：

```text
attempt=1
while True:
    生成一个未使用的新随机 seed
    Star7 1-step 运行
    完整 QC
    保存 attempt 证据
    if QC PASS:
        ACCEPT
        结束当前 task
        break
    else:
        REJECT
        attempt += 1
```

重要：**质量 retry 没有固定次数上限。**

只有技术故障才允许 checkpoint 暂停；技术恢复后继续未完成 task，不重复已完成 task。

## 6. QC

每个 attempt 都执行：

```text
history complete
MP4 exists
ffprobe=32x32x5
ffmpeg decode succeeds
finite
non-black/non-flat
every frame range >= 8
every frame std >= 1.5
SHA256
```

FAIL 输出必须留证据但不得交付。

## 7. 计时

每个 attempt：

```text
ATTEMPT_TOTAL = POST /prompt 前 → MP4存在且 QC裁决完成
```

每个 delivery task：

```text
DELIVERY_TOTAL = 当前 task 第一次 POST /prompt 前
                 → 首个 QC PASS 被 ACCEPT
```

DELIVERY_TOTAL 必须包含所有失败 attempt、QC、随机换种、成功 attempt。

若冻结源码无法提供 CUDA Event 分段，不得临时修改源码；可将 Generation CUDA / Path CUDA 记为 null，并保留 wall/log 代理值，但最终系统裁决以 ATTEMPT_TOTAL / DELIVERY_TOTAL 为准。

## 8. 最终统计

对 T01–T20 计算：

```text
TOTAL_TASKS
TOTAL_ATTEMPTS
FIRST_ATTEMPT_PASS_COUNT
FIRST_ATTEMPT_PASS_RATE
ATTEMPT_PASS_RATE
MEAN_ATTEMPTS_PER_TASK
ATTEMPTS_P50/P95/MAX
DELIVERY_TOTAL_MEAN/P50/P95/MAX
ATTEMPT_TOTAL_P50/P95
INVALID_OUTPUTS_REJECTED
INVALID_OUTPUT_DELIVERED
```

## 9. 裁决门槛

必须全部满足：

```text
FINAL_ACCEPTED_QC=20/20
INVALID_OUTPUT_DELIVERED=0
EVERY_RETRY_USED_NEW_RANDOM_SEED=YES
NO_MANUAL_SEED_SELECTION=YES
STAR7_ONLY=YES
STEP_REMAINS_1=YES
MODEL_AND_RUNTIME_UNCHANGED=YES
MEAN_ATTEMPTS_PER_TASK<=1.25
DELIVERY_TOTAL_P50<=10s
DELIVERY_TOTAL_MEAN<=12s
DELIVERY_TOTAL_P95<=20s
ATTEMPT_TOTAL_P50<=10s
```

通过：

```text
QUALITY_STABILITY_PROOF=PASS
TIME_99_UNDER_QUALITY_CONSTRAINT=PASS
FINAL_RESEED_SYSTEM_CERTIFICATION=PASS
READY_TO_FREEZE_FINAL_99=YES
```

否则准确记录失败维度，不自动发明新候选。

## 10. 产物

生成：

```text
H3-P0-QUALITY-STABILITY-RESEED-FINAL-RESULT-v1.md
H3-P0-QUALITY-STABILITY-RESEED-FINAL-STATE-v1.json
```

至少包含：

- 2 warmup 完整账本；
- 20 个 task 全部 attempts；
- 每个 seed / QC / SHA256；
- 统计；
- 容量路由器状态；
- 若真实 capacity 本轮发生，记录 route event；
- Git commit / remote verify。

完成后：

```text
commit
push
remote verify
STOP
RETURN TO GPT
```

禁止继续其他 H3 优化。