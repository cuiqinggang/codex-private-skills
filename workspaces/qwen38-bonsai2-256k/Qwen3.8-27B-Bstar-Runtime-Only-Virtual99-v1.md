# B* Runtime-only Virtual-99 冻结 v1.0

## 状态

```text
PROJECT=qwen38-27b-bstar-256k-local-executor-jev
METHOD=first-principles-physical-limit-convergence v3.1.7
CURRENT_STEP=2
SCOPE=RUNTIME_ONLY
B_STAR_REOPENED=NO
TARGET_CONTEXT=262144
RUNTIME_ONLY_VIRTUAL_99=MATURE
```

## 现实矛盾输入

已知 Reality 证据：

```text
FAILED_RUNTIME=prism-b10709-9a9394a / win-cuda-12.4-x64
TRANSPORT=PASS
ARCHIVE_SHA256=PASS
EXTRACTION=PASS
llama-server --version=0xC000001D ILLEGAL_INSTRUCTION
MODEL_DOWNLOAD=NOT_STARTED
```

2026-09-21 只读 Reality Preflight：

```text
CPU=Intel Core i5-3570
CPU_CORES=4
GPU=RTX 2080 Ti
GPU_COMPUTE_CAP=7.5
GPU_TOTAL_MIB=22528
NVCC=13.2
CMAKE=4.3.2
NINJA=1.13.2
VS2022_CPP_BUILD_TOOLS=PRESENT
SOURCE_BUILD_PREREQ_GATE=PASS
```

## 根因闭合

Prism commit 9a9394a 的 Windows CUDA release 配置使用 `GGML_NATIVE=OFF`，但未使用 CPU 多变体动态选择。
在该源码配置中，native-default 为 ON 而 GGML_NATIVE 被显式关闭时，`INS_ENB=ON`，进而默认启用 SSE4.2 / AVX / AVX2 / BMI2。

MSVC x86 CPU backend 在 AVX2=ON 时使用 `/arch:AVX2`；Intel i5-3570 官方能力为 SSE4.1 / SSE4.2 / AVX，不包含 AVX2。
因此已有 `0xC000001D` 与 CPU backend ISA 不兼容形成闭合因果链。

## 候选竞争

### R0 — 原预编译 CUDA 12.4 包

```text
STATUS=REALITY_DISPROVED
T_VALID=INVALID
```

### R1 — 同 release 兼容 CPU backend graft

保持现有已下载、已 SHA 验证的 CUDA Runtime 全部不动，仅替换 CPU backend：

```text
SOURCE_RELEASE=prism-b10709-9a9394a
SOURCE_COMMIT=9a9394a895b96003ca842a6041cb28ac49a108f7
ASSET=llama-prism-b10709-9a9394a-bin-win-cpu-x64.zip
ASSET_BYTES=18785841
ASSET_SHA256=92cd4d1cee11107593ff87d77eb57b02d804c86dd4b13224e18ba963a4271ad8
CPU_BACKEND=ggml-cpu-sandybridge.dll
OPENMP_RUNTIME=libomp140.x86_64.dll
TARGET_NAME=ggml-cpu.dll
```

选择 sandybridge variant 的原因：

```text
sandybridge variant = SSE4.2 + AVX
i5-3570 verified product capability = SSE4.2 + AVX
AVX2/BMI2 not required
```

同一 commit 的 CPU dynamic backend 仍导出 `GGML_BACKEND_API` CPU 公共函数；dynamic-build 只额外增加 `ggml_backend_init`。因此以同 commit sandybridge DLL 替换静态命名的 `ggml-cpu.dll`，ABI contract 在 Virtual 阶段闭合。

PQ2_0 / CUDA 路径不变：现有 Prism `llama-server.exe`、`ggml.dll`、`ggml-base.dll`、`ggml-cuda.dll` 与 CUDA runtime DLL 均保留。

```text
R1=VIRTUAL_MATURE
```

### R2 — 本机仅重建 ggml-cpu

同 commit，关闭 AVX2/BMI2，仅 build `ggml-cpu` target。

```text
QUALITY_PATH=VALID
TIME=R1_SLOWER
ROLE=FALLBACK_AFTER_R1_REALITY_FAIL
```

### R3 — CPU compatible host + dynamic ggml-cuda backend

采用成熟 `GGML_BACKEND_DL=ON / GGML_CPU=OFF / GGML_CUDA=ON / --target ggml-cuda` 架构，CUDA arch 固定 75。

```text
QUALITY_PATH=VALID
TIME=R1_SLOWER
ROLE=FALLBACK_AFTER_R2_FAIL
```

### Vulkan

Prism 9a9394a 的 Vulkan backend 没有 PQ2_0 专用路径；不能满足 B* PQ2_0 GPU Runtime 硬门。

```text
VULKAN=ELIMINATED
```

## 时间唯一标准

Runtime-only `T_VALID` 定义：

```text
START = Reality repair command starts
END   = both gates PASS:
        1. llama-server --version exit=0
        2. llama-server --list-devices exit=0 and RTX 2080 Ti / CUDA device present
```

不包括模型下载，不包括完整 B* Certification。

现实锚：
- 既有 FlClash explicit-reuse path 已现实证明 PASS；
- 1 MiB Range probe = 3637.314 ms；
- 历史 253,442,371-byte runtime Asset 1 在 x1/s1 第一阶段已完整取得；
- R1 新增传输仅 18,785,841 bytes（约 17.92 MiB）；
- 无源码编译、无 CUDA 编译、无 runtime 大包重下。

冻结：

```text
RUNTIME_WINNER=R1_SAME_RELEASE_CPU_BACKEND_GRAFT
MIN_T_VALID_VIRTUAL_TARGET_MS=60000
MIN_T_VALID_VIRTUAL_TARGET=60s
TIME_GATE_POLICY=HARD
```

60 秒是 Virtual-99 冻结目标，不冒充现实实测值。

Reality 判定：

```text
QUALITY_PASS && T_VALID_REAL_MS <= 60000
=> RUNTIME_R1_REALITY_CERTIFIED

QUALITY_PASS && T_VALID_REAL_MS > 60000
=> RUNTIME_R1_FAIL_TIME_MODEL
=> RETURN_TO_STEP_2

ANY_QUALITY_GATE_FAIL
=> RESTORE_ORIGINAL_CPU_DLL
=> SAVE_EVIDENCE
=> STOP
=> RETURN_TO_STEP_2
```

禁止在同一次 Reality 中自动转 R2/R3。

## 冻结硬门

```text
ASSET_SIZE_EXACT=PASS
ASSET_SHA256_EXACT=PASS
SOURCE_RELEASE_EXACT=PASS
CPU_VARIANT_PRESENT=PASS
OPENMP_RUNTIME_PRESENT=PASS
BACKUP_ORIGINAL_CPU_DLL=PASS
llama-server --version EXIT=0
llama-server --list-devices EXIT=0
CUDA_DEVICE_PRESENT=PASS
RTX_2080_TI_PRESENT=PASS
NO_ILLEGAL_INSTRUCTION=PASS
SYSTEM_PROXY_MODIFIED=false
GIT_PROXY_MODIFIED=false
FLCLASH_MODIFIED=false
NETWORK_MODIFIED=false
REGISTRY_MODIFIED=false
MODEL_DOWNLOADS=0
```

## Step 3 唯一允许动作

只验证 R1。R1 Reality FAIL 后不得现场编译，不得切 R2/R3；必须 RETURN_TO_STEP_2。
