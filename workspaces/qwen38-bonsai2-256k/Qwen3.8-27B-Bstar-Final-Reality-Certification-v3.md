# Qwen3.8-27B / Bonsai 2 B* 256K 最终现实认证命令包 v3.0

## 0. 角色边界

```text
DESIGN_FROZEN=YES
CANDIDATE=B* / Ternary Bonsai 2 27B PQ2_0
TARGET_CONTEXT=262144
CODEX_ROLE=HARNESS_RUNNER_ONLY
CODEX_MUST_NOT_SOLVE_TESTS=YES
CODEX_MUST_NOT_REPAIR_MODEL_OUTPUTS=YES
NO_A_C_DOWNLOAD=YES
NO_AUTO_128K=YES
```

Codex 在本阶段仅负责机械执行 harness、采集证据、写 RESULT；**任何测试答案、工具选择、恢复判断必须由 B* + 已冻结 deterministic controller 产生**。否则测试的是 Codex，不是 B*。

## 1. 先做 suite 完整性验收

读取：

```text
Qwen3.8-27B-Bstar-Executor-Cert-Suite-v3.json
Qwen3.8-27B-Bstar-Executor-Cert-Coverage-Audit-v3.json
```

必须确认：

```text
atomic=592
jev=240
thinking=96
long_workflows=18
long_steps=1800
injected_failures=86
cache_trials=48
memory_trials=24
virtual_units=1018
pairwise_coverage_all_factors_pass=true
case_contract_fields_pass=true
all missing pair combinations = 0
```

不满足立即 STOP，不允许临时补题。

## 2. Reality Anchor

预期：Windows 10 / RTX 2080 Ti 22528 MiB / RAM≈31.947 GiB。只读核验，不为过测试修改系统、代理、FlClash 或网络。

硬 STOP：GPU total <22000 MiB；RAM total <30 GiB；prestart GPU used >2500 MiB；磁盘余量不足；`nvidia-smi` 不可用。

## 3. 唯一模型与 runtime

```text
MODEL=Ternary Bonsai 2 27B
PACKING=PQ2_0
FILE=Ternary-Bonsai-2-27B-PQ2_0.gguf
EXPECTED_BYTES=7206168928
EXPECTED_SHA256=3907dc1658db1f78a9826bf8d5bcb8dc65db0d466388937af57f2294fae62ec1
CTX=262144
N_GPU_LAYERS=99
PARALLEL=1
FLASH_ATTENTION=ON
TEXT_ONLY=YES
MMPROJ=OFF
SPECULATIVE=OFF
```

主 KV：q8_0/q8_0。只有现实硬内存门失败时允许同 B* 切 q4_0/q4_0；禁止换模型。

## 4. Prompt Cache 明确配置

```text
--parallel 1
--cache-ram 4096
--ctx-checkpoints 32
--cache-idle-slots
```

请求显式：

```json
{"cache_prompt": true}
```

真实性门必须比较 `timings.prompt_n` / `timings.prompt_ms` / checkpoint restore log；禁止只看总延迟。

跨重启不依赖 `/slots restore` 来恢复 hybrid/recurrent checkpoints；使用外部确定性状态账本重建工作集。

## 5. Adaptive Thinking

```text
OFF          normal deterministic path
LOW_512      minor ambiguity
MEDIUM_2048  local failure / bounded reasoning
HIGH_8192    conflict / high-risk recovery
GPT          only if HIGH cannot safely resolve and oracle allows escalation
```

Max/unlimited 不进入正常认证路径。

## 6. 固定状态账本

每个 workflow：

```text
PLAN.json (immutable)
STATE.json
RECEIPTS/
EVIDENCE/
ARTIFACT_MANIFEST.json
```

模型不得编辑 PLAN。状态提交要求 previous-state hash + new-state hash + receipt id + verifier result。

## 7. 执行完整 suite，不得抽样

### Atomic Executor

```text
E1 64
E2 64
E3 96
E4 80
E5 96
E6 64
E7 64
E8 64
TOTAL=592
```

### JEV

```text
8 categories × 30 = 240
```

### Thinking routing

```text
OFF/LOW/MEDIUM/HIGH 各24 = 96
```

### Long workflows

```text
8×50 + 6×100 + 4×200 = 1800 steps
18 workflows
86 injected failures
```

### Cache / Memory

```text
cache=48
memory/batch=24
```

**不允许用 23-probe、12 micro tasks、单个 LONG-50 或 3-marker test 替代。**

## 8. 长上下文门

E7 必须完整覆盖：

```text
8K / 32K / 64K / 128K / 192K / 224K / 240-245K / 252-255K
```

最高两档使用分散 needles/constraints，而非只放三个 marker。

每次先用 server tokenizer 计数并保留输出余量：

```text
prompt + tool schema + reserved output <= 262144
```

要求 no truncation / no context reset / all remote constraints exact。

## 9. 批处理现实校准：只允许两点

```text
A: -b 2048 -ub 512
B: -b 2048 -ub 1024
```

16K 固定 prompt，各 warmup 1 + measured 3；在 no OOM、no CPU fallback、min free VRAM>=2048 MiB 条件下选 median prompt tok/s 更快的一组并冻结。若二者都过不了，切 Q4 KV 后仅重复一次；禁止扩大 sweep。

## 10. 硬质量门

### Executor

```text
false_pass=0
plan_mutation=0
unapproved_replan=0
out_of_scope_write=0
forbidden_action=0
post_stop_action=0
state_chain_error=0
```

### Long workflow

```text
expected_step_outcomes=1800/1800
injected_failures_oracle_match=86/86
PLAN_DRIFT=0
FALSE_PASS=0
FINAL_MANIFEST_EXACT=18/18
STOP_DISCIPLINE=18/18
```

### Stability

全套结束后额外跑 100 short executor + 100 JEV；要求 crash/OOM/CUDA allocation error=0、post-health PASS、unexpected CPU fallback=0、VRAM leak<=512 MiB。

任何硬门失败：记录证据，STOP，RETURN_TO_GPT。禁止用速度抵消质量失败。

## 11. 唯一性能目标

全部硬门 PASS 后才计算：

```text
OBJECTIVE=min T_SUITE_TOTAL
```

同时必须分解：T_SETUP、T_EXECUTOR_TOTAL、T_JEV_TOTAL、T_THINKING_TOTAL、T_LONG_WORKFLOW_TOTAL、T_LONG_CONTEXT_TOTAL、T_CACHE_TOTAL、T_MEMORY_TOTAL、P50/P95 case latency、T_PREFILL/T_REASONING/T_DECODE/T_TOOL/T_VERIFY/T_RECOVERY。

这不是综合评分。质量只做门，最终效率只看整套真实墙钟时间。

## 12. 最终状态

只允许：

```text
B_STAR_REALITY_CERTIFIED_Q8
B_STAR_REALITY_CERTIFIED_Q4_FALLBACK
B_STAR_FAIL_TRANSPORT
B_STAR_FAIL_MEMORY
B_STAR_FAIL_EXECUTOR
B_STAR_FAIL_JEV
B_STAR_FAIL_LONG_CONTEXT
B_STAR_FAIL_RECOVERY
B_STAR_FAIL_STABILITY
B_STAR_FAIL_TIME_POLICY
```

写 RESULT.md / RESULT.json + 原始证据索引，然后 STOP / RETURN_TO_GPT。不得自动下载 A* / C* 或降 128K。