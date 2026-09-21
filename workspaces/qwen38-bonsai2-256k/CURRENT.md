# Qwen3.8 / Bonsai 2 27B 256K — 当前唯一执行入口

## 0. Current State

```text
PROJECT=qwen38-27b-bstar-256k-local-executor-jev
METHOD=first-principles-physical-limit-convergence v3.1.7
CURRENT_STEP=2
STEP_NAME=高智能虚拟成熟
SCOPE=Runtime candidate + certification executability binding
REALITY_ENTRY=FORBIDDEN
```

当前不是 Step 3。任何旧命令、旧 Runtime v1、旧 60s/600s 时间门都不得用于现实执行。

## 1. 冻结不重开的系统目标

```text
B_STAR_MODEL=Ternary Bonsai 2 27B PQ2_0
TARGET_CONTEXT=262144
JEV_ROLE=FROZEN
EXECUTOR_QUALITY_OBJECTIVE=FROZEN
VERIFIER_QUALITY_GATES=FROZEN
RECOVERY_POLICY=FROZEN
NO_AUTO_128K=YES
NO_A_C_AUTO_DOWNLOAD=YES
```

原 v3 Authority：

```text
Qwen3.8-27B-Bstar-Virtual99-Mature-v3.md
Qwen3.8-27B-Bstar-Final-Reality-Certification-v3.md
Qwen3.8-27B-Bstar-Executor-Cert-Suite-v3.json
Qwen3.8-27B-Bstar-Executor-Cert-Coverage-Audit-v3.json
```

精确 blob：

```text
FINAL_CERT_V3_SHA=18543d5de00f838233d9db6abcea0c4534720dd7
SUITE_V3_SHA=87847854af82771291124213d9518c981725d90b
COVERAGE_V3_SHA=b7beea02c87a349d7146beb94711c226db684df1
```

## 2. 已确认 Reality contradiction

```text
KNOWN_PREBUILT_RUNTIME=prism-b10709-9a9394a / Windows CUDA 12.4 x64
KNOWN_TRANSPORT_FOR_THIS_RUNTIME=PASS
KNOWN_RUNTIME_ARCHIVE_HASHES=PASS
KNOWN_RUNTIME_EXTRACTION=PASS
KNOWN_LLAMA_SERVER_VERSION_GATE=FAIL
KNOWN_RUNTIME_FAILURE=0xC000001D_ILLEGAL_INSTRUCTION

MODEL_DOWNLOAD=NOT_STARTED
B_STAR_MODEL_FAILURE=NO
LONG_CONTEXT_FAILURE=NO
PREBUILT_RUNTIME_RETRY=FORBIDDEN
```

Reality Anchor：

```text
CPU=Intel i5-3570 / 4C4T / Ivy Bridge
GPU=RTX 2080 Ti / sm_75
VRAM=22528 MiB
NVCC=CUDA 13.2
CMAKE=4.3.2
NINJA=1.13.2
VS_CPP_BUILD_TOOLS=PASS
SOURCE_BUILD_PREREQ_GATE=PASS
```

## 3. Runtime-only Virtual-99 v2 当前结论

Authority：

```text
Qwen3.8-27B-Bstar-Runtime-Only-Virtual99-v2.md
BLOB_SHA=5d25722743fd334d04df32269d5ab4108ebe2ccc
```

旧 Runtime-only v1：

```text
RUNTIME_ONLY_V1=SUPERSEDED
OLD_60S=INVALID_FULL_T_VALID_SCOPE
OLD_600S=RUNTIME_LOCAL_BUDGET_ONLY
```

Runtime candidate 已收敛：

```text
RUNTIME_WINNER=
R1_SAME_RELEASE_DETERMINISTIC_AVX_SM75_SERVER_ONLY

SOURCE_COMMIT=9a9394a895b96003ca842a6041cb28ac49a108f7
CPU_BASELINE=AVX / no AVX2
CUDA_ARCH=75-real
BUILD_TARGET=llama-server
T_RUNTIME_READY_MODEL≈00:10:00
```

模型传输现有 timing prior：

```text
MODEL_BYTES=7206168928
EXISTING_1MIB_PROBE=3637.314ms
MATURE_TRANSFER_MODE=x4
T_MODEL_READY_MODEL≈01:48:00
```

## 4. 新发现的 Virtual contradiction

详细 Authority：

```text
Qwen3.8-27B-Bstar-Suite-Executability-Contradiction-v1.md
```

### A. Context budget 数学冲突

v3 自己要求：

```text
prompt_tokens + tool_schema_tokens + reserved_output_tokens <= 262144
```

但 v3 Suite 的 `252-255K` band 中存在 16 个 `HIGH_8192` Atomic cases。

最低 252K 即：

```text
258048 + 8192 = 266240 > 262144
```

尚未计算 tool schema / final output，因此这些 case 必然不可执行。

### B. Fixture / runner binding 缺失

Suite case 写着：

```text
fixture.generator=bstar-fixture-v3
```

但当前 Authority workspace 没有该 generator 的实现，也没有完整 1018-unit deterministic Reality runner。

因此让 Codex 现在进入 Reality 会迫使它现场发明 fixture / prompt / oracle / runner，违反“Reality 只验证、不得重新设计”。

## 5. 时间状态

此前基于 Runtime + model transfer + 外部 RTX 2080 Ti timing prior + v3 workload 得到：

```text
PROVISIONAL_FULL_SYSTEM_TIME_MODEL≈118:13:00
```

但它不是当前合法 `min T_VALID`，因为 `T_CERTIFICATION` 尚没有可执行绑定。

正式状态：

```text
SUITE_EXECUTABILITY_GATE=FAIL
RUNNER_BINDING_GATE=FAIL
RUNTIME_CANDIDATE_VIRTUAL_MATURE=YES
FULL_VIRTUAL_99=NOT_MATURE
MIN_T_VALID=UNRESOLVED
REALITY_CERTIFIED=NO
STEP3_COMMAND=FORBIDDEN
```

## 6. 唯一下一步

继续 Step 2，只修 certification executability binding：

```text
context-envelope semantic repair
→ bstar-fixture-v3 deterministic generator
→ exact PLAN / prompt / fixture / oracle instantiation
→ unique Reality runner binding
→ 1018-unit no-model self-test
→ token-budget audit
→ recompute full-system min T_VALID
→ freeze
→ only then Step 3
```

禁止：

```text
现在运行旧 R1 60s script
现在运行旧 600s source-build gate
把 provisional 118:13:00 当成 PASS/FAIL 门
现场让 Codex 写测试 harness
现实边跑边改 suite
```
