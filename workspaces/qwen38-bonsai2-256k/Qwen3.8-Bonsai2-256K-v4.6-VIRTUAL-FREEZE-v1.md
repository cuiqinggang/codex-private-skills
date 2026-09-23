# Qwen3.8 / Bonsai 2 27B 256K — v4.6 虚拟成熟冻结 v1

## 1. 唯一目标

本任务不是重新开发模型，也不是重新证明下载。

最终有效条件：

```text
MODEL_AND_RUNTIME_REUSED=PASS
CTX_262144=PASS
STRICT_LONG_CONTEXT_VALID=PASS
IN_PROCESS_PREFIX_REUSE_MEASURED=PASS
DECODE_MEASURED=PASS
RESOURCE_GATE=PASS
REAL_RESULT_COMPLETE=PASS
```

唯一优化：
```text
min T_VALID_RUN
```
其中当前 GPU 子任务只贡献现实物理时间；整体闭环仍由极限短时间引擎 v4.6.0 计时。

## 2. 保留的旧成熟资产

```text
MODEL=prism-ml/Ternary-Bonsai-2-27B-gguf
PACKING=PQ2_0
MODEL_BYTES=7206168928
MODEL_SHA256=3907dc1658db1f78a9826bf8d5bcb8dc65db0d466388937af57f2294fae62ec1

RUNTIME_REPO=PrismML-Eng/llama.cpp
RUNTIME_COMMIT=9a9394a895b96003ca842a6041cb28ac49a108f7
CPU=IvyBridge AVX / no AVX2
CUDA_ARCH=75
NGL=99
CTX=262144
PARALLEL=1
FLASH_ATTENTION=ON
REASONING=OFF
PRIMARY_KV=q8_0/q8_0
FALLBACK_KV=q4_0/q4_0 only if q8 hard-memory startup fails
TEXT_ONLY=YES
SPECULATIVE=OFF
```

## 3. 已经成立的 Reality

242054-token Reality Anchor：

```text
PROMPT_MS=1367320.567
E2E_MS=1378701.719
SEMANTIC_VALID=PASS
```

正确输出：

```json
{"begin":3817,"middle":6241,"end":9053,"sum":42}
```

原 validator false-negative 根因：
把数值 `3817/6241/9053` 与完整 marker 字符串 `BNS_BEGIN_3817/BNS_MIDDLE_6241/BNS_END_9053` 比较。

因此 cold 质量认证禁止重跑。

## 4. 2026-09-23 成熟方案增量

### 4.1 保留 PQ2_0

Bonsai 2 官方资料仍把 PQ2_0 作为 CUDA 快 Prompt 处理的重要 packing。242K 现实瓶颈主要是 Prefill，因此不切换 PTQ1_0。

### 4.2 Context checkpoints

冻结 runtime b10709 已确认自身支持：

```text
--ctx-checkpoints
--checkpoint-min-step
--cache-ram
--cache-idle-slots
--cache-reuse
```

本轮固定显式：

```text
--ctx-checkpoints 32
--checkpoint-min-step 8192
--cache-reuse 0
```

理由：
Bonsai 2 是 hybrid-attention；context checkpoint 是恢复 hybrid/recurrent prefix 状态的成熟机制。

### 4.3 Host RAM prompt cache 不进入本轮关键路径

本轮是：

```text
parallel=1
同一 server 生命周期
seed -> HOT100 -> HOT98 -> HOT95
```

因此不需要跨 slot 的 host-RAM prompt cache 才能完成目标。
为减少无关状态和近期 cross-slot cache 风险，冻结：

```text
--cache-ram 0
--no-cache-idle-slots
```

只测同 slot 的 `cache_prompt:true + context checkpoints`。

### 4.4 跨重启 slot save/restore 淘汰

虽然 llama-server 有 slot save/restore API，但 Bonsai 2 是约 75% linear attention 的 hybrid model。
2026-07~09 upstream 已有公开现实问题：hybrid/recurrent 模型 restore 不持久化 server context checkpoints，restore 可报告成功但下一请求仍 `cache_n=0` 并完整 Prefill。

因此：

```text
PERSISTENT_SLOT_RESTORE=REJECTED
```

不得把它计入未来节省 22 分钟的方案。

### 4.5 Speculative decode 淘汰

当前 Bonsai 2 27B 没有官方对应 DSpark drafter。
不把上一代 Bonsai/Ternary 的 speculative 收益外推到 Bonsai 2。

```text
SPECULATIVE=OFF
```

### 4.6 4-bit KV 只作内存 fallback

官方说明 q4 KV 是 memory tool，不是 speed tool，decode 可能略慢。
本机 q8 已现实证明 262144 可启动，因此：

```text
q8 PRIMARY
q4 FALLBACK_ON_HARD_MEMORY_ONLY
```

### 4.7 不做 batch 大 sweep

当前长 Prefill 约 22m47s，但短 PP sweep 不能可靠代表 242K。
扩大 sweep 会增加本轮整体 T_VALID_RUN，且没有足够证据保证净收益。

保持 runtime 当前成熟默认 batch/ubatch；本轮只记录实际值/启动参数，不扩大竞争。

### 4.8 JEV 从 GPU benchmark 删除

JEV 是极限短时间引擎“虚”内部的决策加速器，不是 Bonsai GPU Prefill/Decode 物理指标。
本轮 GPU runner：

```text
JEV_A_B=SKIP_NOT_CRITICAL_PATH
```

未来单独按整体 T_VALID_RUN 比较是否接入。

## 5. Strict verifier 冻结

模型输出必须：

1. trim 后整体就是一个 JSON object；
2. JSON parse PASS；
3. property count = 4；
4. exact keys = begin,middle,end,sum；
5. integer values：
   - begin=3817
   - middle=6241
   - end=9053
   - sum=42
6. JSON 外任何解释文字都 FAIL。

禁止 regex 从额外文字中“抠出一个正确 JSON”后判 PASS。

0-GPU self-test 必须：

```text
GOOD_JSON=PASS
WRONG_BEGIN=FAIL
WRONG_MIDDLE=FAIL
WRONG_END=FAIL
WRONG_SUM=FAIL
MISSING_KEY=FAIL
EXTRA_KEY=FAIL
EXTRA_OUTER_TEXT=FAIL
INVALID_JSON=FAIL
```

10/10 才允许启动 GPU。

## 6. Reality 执行链

```text
0-GPU verifier self-test
-> preflight：model/runtime/path/GPU/context flags
-> start q8 server
-> confirm CUDA/full offload/262144
-> tokenize existing v3 prompt-242k.txt
-> require token count = 242054
-> 242K cold_full_seed, n_predict=1, cache_prompt=true
-> HOT100 valid
-> HOT98 valid
-> HOT95 valid
-> 3 x isolated decode
-> collect resources/timings/cached_tokens
-> stop server
-> write RESULT.json + RESULT.md
-> STOP
-> GPT final judge
```

不做：
download/build/JEV/speculation/full certification suite。

## 7. Prefix reuse validity

HOT100：
- exact same token prompt；
- expected high cached token count；
- output strict verifier PASS。

HOT98：
- one token changes at intended 98% prefix boundary；
- record intended prefix, actual cached tokens, prompt_ms；
- strict verifier PASS。

HOT95 同理。

必须记录：
```text
actual_cached_tokens
actual_cached_ratio
prompt_ms
prompt_per_second
predicted_ms
predicted_per_second
e2e_ms
verify_ms
output
```

不能只看 E2E 猜 cache hit。

## 8. 冻结预测时间

不可避免主成本：
```text
242K cache seed ~= 已知 Reality prompt 1367s 量级
```

HOT100/HOT98/HOT95 目标是取得真实复用收益；在未现实测量前不伪造有限时间数字。

因此：
```text
PREDICTED_T_REAL_GPU
= one 242K seed
+ HOT100
+ HOT98
+ HOT95
+ decode x3
+ verifier/resource overhead
```

相比旧方案，已确定删除：
- 再一次 cold 质量认证；
- 1018-unit suite；
- JEV A/B；
- 下载/编译；
- 无收益参数 sweep。

所以本方案是当前完整有效候选中的最短 Reality 路线。

## 9. Frozen

```text
VIRTUAL_MATURITY=PASS
REALITY_FOUNDATION_SUFFICIENT=PASS
FINAL_VALID_CONDITION_DEFINED=PASS
EXECUTION_CHAIN_CLOSED=PASS
EXTERNAL_DEPENDENCIES_CLOSED=PASS
CODEX_POLICY_COMPATIBILITY=PASS
KNOWN_FAILURE_GATES=PASS
TIMING_CONTRACT_READY=PASS
FROZEN_SOLUTION=PASS
HANDOFF_READY=PASS
```
