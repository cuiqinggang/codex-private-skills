# Qwen3.8 / Bonsai 2 B* — Runtime-only Virtual-99 v2

## 0. 唯一定位

```text
PROJECT=qwen38-27b-bstar-256k-local-executor-jev
METHOD=first-principles-physical-limit-convergence v3.1.7
CURRENT_STEP=2
STEP_NAME=高智能虚拟成熟
SCOPE=RUNTIME_ONLY_REOPEN
REALITY_REDESIGN=FORBIDDEN
B_STAR_MODEL_SELECTION=FROZEN
TARGET_CONTEXT=262144
JEV_SUITE=FROZEN
EXECUTOR_SUITE=FROZEN
VERIFIER=FROZEN
RECOVERY=FROZEN
FINAL_REALITY_CERT_V3=FROZEN
```

本 v2 是 Runtime-only 唯一新 Authority。旧 Runtime-only v1 同时存在 “source build / 600s” 与 “CPU backend graft / 60s” 两套冲突 Authority，现全部 supersede：

```text
RUNTIME_ONLY_V1=SUPERSEDED
OLD_60S=INVALID_FULL_T_VALID_SCOPE
OLD_600S=RUNTIME_LOCAL_BUDGET_ONLY
```

本轮只允许重新求 Runtime*。但是最终时间必须按“从当前现实状态到完整有效 B* 生产系统”的总墙钟定义，而不是只算编译。

## 1. Reality contradiction

已证伪：

```text
R0=prism-b10709-9a9394a / Windows CUDA 12.4 x64 prebuilt
ARCHIVE_HASH=PASS
EXTRACTION=PASS
LLAMA_SERVER_VERSION=FAIL
EXIT=0xC000001D
CLASS=ILLEGAL_INSTRUCTION
T_VALID(R0)=INVALID
RETRY_R0=FORBIDDEN
```

当前 Reality Anchor：

```text
CPU=Intel Core i5-3570 / Ivy Bridge / 4C4T / SSE4.2 + AVX / no AVX2 contract
GPU=RTX 2080 Ti / Turing / Compute Capability 7.5
VRAM=22528 MiB
NVCC=CUDA 13.2
CMAKE=4.3.2
NINJA=1.13.2
VS2022_CPP_BUILD_TOOLS=PASS
SOURCE_BUILD_PREREQ_GATE=PASS
MODEL_DOWNLOAD=NOT_STARTED
```

## 2. 固定源与兼容性事实

```text
SOURCE_REPO=PrismML-Eng/llama.cpp
SOURCE_COMMIT=9a9394a895b96003ca842a6041cb28ac49a108f7
SOURCE_RELEASE=prism-b10709-9a9394a
```

Bonsai 2 PQ2_0/PTQ1_0 依赖 Prism fork 的 ternary packing / runtime transform，stock llama.cpp 不进入候选。

外部 RTX 2080 Ti Bonsai 2 实测使用的 Prism commit 为 `01041db99dae68529db58c6fc692a9ca623b30a2`。Git ancestry 已核对：冻结 commit `9a9394a...` 仅领先该 commit 1 个提交；差异只触及 release workflow 与 speculative 代码，而本 B* 已冻结 `SPECULATIVE=OFF`。因此无需回退 commit。

CUDA 13.2 仍支持 Turing `sm_75`；无需为本轮另装 CUDA 12.4。Vendor Windows CUDA build helper 的 CUDA>=13 默认 arch list 从 80 起，不覆盖 RTX 2080 Ti，因此本轮必须显式指定 75。

## 3. Runtime 成熟候选集与淘汰

### R0 — 原预编译包

```text
STATUS=REALITY_INVALID
REASON=0xC000001D
T_VALID=INVALID
```

### R1* — 同 release / deterministic AVX / sm_75 / server-only source build

```text
STATUS=VIRTUAL_WINNER
ID=R1_SAME_RELEASE_DETERMINISTIC_AVX_SM75_SERVER_ONLY

SOURCE_COMMIT=9a9394a895b96003ca842a6041cb28ac49a108f7
GENERATOR=Visual Studio 17 2022
ARCH=x64
CUDA_TOOLKIT=existing 13.2
CMAKE_CUDA_ARCHITECTURES=75-real
PARALLEL_BUILD=4

GGML_CUDA=ON
GGML_BACKEND_DL=OFF
GGML_CPU_ALL_VARIANTS=OFF
GGML_NATIVE=OFF
GGML_SSE42=ON
GGML_AVX=ON
GGML_AVX2=OFF
GGML_AVX_VNNI=OFF
GGML_FMA=OFF
GGML_BMI2=OFF
GGML_AVX512=OFF
GGML_AVX512_VBMI=OFF
GGML_AVX512_VNNI=OFF
GGML_AVX512_BF16=OFF
GGML_OPENMP=OFF
GGML_LLAMAFILE=OFF

LLAMA_BUILD_TESTS=OFF
LLAMA_BUILD_TOOLS=ON
LLAMA_BUILD_EXAMPLES=OFF
LLAMA_BUILD_SERVER=ON
LLAMA_BUILD_APP=OFF
LLAMA_BUILD_UI=OFF
LLAMA_OPENSSL=OFF
LLAMA_DSPARK_MARKOV_CUDA=OFF

BUILD_TARGET=llama-server
```

选择理由：宿主 CPU 明确只有 AVX 而非 AVX2；关闭 native detection 和 all-variants，把 CPU ISA 从“运行时选择”变成“构建时确定”；CUDA 只生成 `sm_75`；只构建生产必需 server target；不编译 frozen-off 的 speculative CUDA head。

### R2 — 同源 native CPU auto-detect + sm_75

```text
STATUS=VIRTUAL_DOMINATED
REASON=NO_RUNTIME_GAIN_AND_REINTRODUCES_HOST_ISA_DETECTION_UNCERTAINTY
```

### R3 — 同源 CPU all-variants / backend-dl + sm_75

```text
STATUS=VIRTUAL_DOMINATED
REASON=LONGER_BUILD_AND_REINTRODUCES_CPU_VARIANT_SELECTION_FAMILY
```

### R4 — 回退外部 benchmark commit + CUDA 12.4

```text
STATUS=RESERVE_ONLY
REASON=EXACT_RELEASE_IS_DIRECT_DESCENDANT_AND_SPECULATIVE_DELTA_IS_FROZEN_OFF; EXTRA_TOOLKIT_INSTALL_ADDS_TIME
```

### Stock llama.cpp

```text
STATUS=FORMAT_GATE_FAIL
REASON=PQ2_0_BONSAI_RUNTIME_CONTRACT_NOT_MET
```

## 4. R1* Virtual validity gates

R1* 进入 Reality 前必须在 Twin 中保持：

```text
SOURCE_COMMIT_EXACT=PASS
CPU_ISA_CONTRACT=PASS
CUDA_SM75_CONTRACT=PASS
MODEL_FORMAT_CONTRACT=PASS
NO_PREBUILT_CPU_VARIANT_SELECTION=PASS
NO_STOCK_LLAMA_SUBSTITUTION=PASS
NO_MODEL_CHANGE=PASS
NO_CONTEXT_DOWNGRADE=PASS
NO_SUITE_CHANGE=PASS
NO_VERIFIER_CHANGE=PASS
```

注意：这些是 Virtual/Twin 兼容性门，不伪装成 Reality model capability PASS。原 v3 Authority 仍明确：

```text
REAL_MODEL_BEHAVIOR=UNKNOWN
REAL_EXECUTOR_CERTIFIED=NO
```

## 5. 总 T_VALID 的唯一口径

```text
T_VALID =
T_PREPARE
+ T_RUNTIME_READY
+ T_MODEL_READY
+ T_SERVER_READY
+ T_CERTIFICATION
+ T_VERIFY
```

起点：Step 3 deterministic runner 开始执行当前冻结 Authority 的第一个动作。

终点：B* 完整 v3 Reality Certification 的所有质量硬门 PASS，最终 RESULT + evidence readback 完成，出现第一个可验证的完整生产有效状态。

当前现实中已经完成的 Authority persist / Suite Integrity / Reality Anchor 证据不得重复收费；尚未完成的模型下载不得记 0。

## 6. 时间锚与 Virtual-99 时间模型

### 6.1 Runtime

上游同系列 Windows CI full CUDA build 曾有约 224s build-step 真实锚；本机 i5-3570 更慢，但 R1* 只编译 sm_75 + llama-server，并关闭 tests/examples/app/UI/speculative CUDA。

冻结 Runtime 局部目标：

```text
T_RUNTIME_READY*=00:10:00
```

旧 600s 仅保留为 Runtime 局部预算，不再叫 full T_VALID。

### 6.2 Model Ready

模型：

```text
FILE=Ternary-Bonsai-2-27B-PQ2_0.gguf
BYTES=7206168928
SHA256=3907dc1658db1f78a9826bf8d5bcb8dc65db0d466388937af57f2294fae62ec1
```

既有 Reality transport probe：

```text
1 MiB / 3637.314 ms
x1≈0.27493 MiB/s
```

既有成熟下载算法已经现实证明 x4 continuation 可完成 runtime asset；x8 未被证明为必要。Virtual-99 使用成熟的 x4 等效吞吐模型，不把未验证 x8 收益计入极限：

```text
T_RAW_MODEL_TRANSFER(x4 model)≈01:44:09
T_MODEL_READY* (含完整性/hash余量)=01:48:00
```

若 Step 3 开始时模型文件已经存在且 exact bytes + SHA256 PASS，则按当前状态规则 `T_MODEL_READY=0`，不得重复下载。

### 6.3 Certification

冻结 v3 suite：

```text
Atomic Executor=592
JEV=240
Thinking=96
Long Workflows=18
Long Workflow Steps=1800
Injected Failures=86
Cache Trials=48
Memory/Batch Trials=24
Stability=100 executor + 100 JEV
Context Bands=8K/32K/64K/128K/192K/224K/240-245K/252-255K
PARALLEL=1
```

外部同级 RTX 2080 Ti Bonsai 2 timing prior：
- PQ2_0 short pp512≈691 tok/s；
- long 150K no-spec prefill≈315.5 tok/s；
- short decode≈39.12 tok/s；
- 150K no-spec decode≈13.1 tok/s。

长上下文 150K 行来自相邻 Bonsai2 PQ2_0 变体，只作为 Twin timing prior，不作为本机 Reality PASS。

用短点 + 150K 点拟合一阶 context-degradation 模型后，冻结 suite 的不可省长上下文/Atomic/Cache/Memory 工作量给出：

```text
T_CERT_PREFILL_FLOOR_MODEL≈99:38:00
T_CERT_TOTAL_MODEL≈116:13:00
```

其中后者继续包含 decode、long-workflow、thinking/JEV、prefix-mutated cache、stability、tool/verifier/recovery 的冻结工作量模型。

## 7. 新的 min T_VALID

从当前现实状态出发：

```text
T_RUNTIME_READY*   ≈ 00:10:00
T_MODEL_READY*     ≈ 01:48:00
T_SERVER_READY*    ≈ 00:02:00
T_CERT+FINALVERIFY ≈116:13:00
--------------------------------
MIN_T_VALID_VIRTUAL99 = 118:13:00
MIN_T_VALID_SECONDS    = 425580
```

这里的 `118:13:00` 是新的 **full-system Virtual-99 可证伪极限目标**，不是 Reality 已实测值，也不是物理定律常数。

冻结判定：

```text
QUALITY_GATE_FAIL
=> REALITY_FAIL
=> SAVE_MINIMUM_CONTRADICTION_EVIDENCE
=> STOP
=> RETURN_TO_STEP_2

ALL_QUALITY_GATES_PASS AND T_VALID_REAL > 425580s
=> TIME_MODEL_FAIL
=> SAVE_FULL_TIME_DECOMPOSITION
=> STOP
=> RETURN_TO_STEP_2

ALL_QUALITY_GATES_PASS AND T_VALID_REAL <= 425580s
=> REALITY_CERTIFIED
```

Reality 若更快，允许 PASS；不得为了“贴近模型”故意等待。

## 8. 冻结结果

```text
RUNTIME_ONLY_VIRTUAL_99_V2=PASS
RUNTIME_WINNER=R1_SAME_RELEASE_DETERMINISTIC_AVX_SM75_SERVER_ONLY
FULL_SYSTEM_MIN_T_VALID*=118:13:00
FULL_SYSTEM_MIN_T_VALID_SECONDS=425580
RUNTIME_ONLY_V1=SUPERSEDED
REALITY_CERTIFIED=NO
NEXT_STEP=3_REALITY_CERTIFICATION
AUTO_FALLBACK=NO
```

Reality 禁止现场切 R2/R3/R4；任何矛盾必须带证据回 Step 2。
