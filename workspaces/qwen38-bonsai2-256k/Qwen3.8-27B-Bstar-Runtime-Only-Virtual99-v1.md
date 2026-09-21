# Qwen3.8 / Bonsai 2 B* — Runtime-only Virtual-99 v1

## 0. Scope

```text
CURRENT_STEP=2
SCOPE=RUNTIME_ONLY
METHOD=first-principles-physical-limit-convergence v3.1.7
B_STAR_MODEL_SELECTION=FROZEN
TARGET_CONTEXT=262144
JEV_SUITE=FROZEN
EXECUTOR_SUITE=FROZEN
RECOVERY=FROZEN
```

只重开已被 Reality 证伪的 Runtime 实现层。不得重新选择模型、不得降 128K、不得边现实测试边重新设计。

## 1. Reality contradiction

已知现实结果：

```text
PREBUILT_RUNTIME=prism-b10709-9a9394a / Windows CUDA 12.4 x64
ARCHIVE_HASH=PASS
EXTRACTION=PASS
llama-server --version=FAIL
EXIT=0xC000001D
CLASS=ILLEGAL_INSTRUCTION
```

现实锚：

```text
CPU=Intel Core i5-3570 / 4C4T / Ivy Bridge
GPU=RTX 2080 Ti
COMPUTE_CAPABILITY=7.5
VRAM=22528 MiB
NVCC=13.2
CMAKE=4.3.2
NINJA=1.13.2
VS2022_CPP_BUILD_TOOLS=PASS
SOURCE_BUILD_PREREQ_GATE=PASS
```

## 2. Upstream facts

Pinned source:

```text
REPO=PrismML-Eng/llama.cpp
COMMIT=9a9394a895b96003ca842a6041cb28ac49a108f7
RELEASE=prism-b10709-9a9394a
```

上游 CMake 支持：

- `GGML_NATIVE`
- `GGML_SSE42`
- `GGML_AVX`
- `GGML_AVX2`
- `GGML_BMI2`
- `CMAKE_CUDA_ARCHITECTURES`
- `LLAMA_BUILD_SERVER`
- `LLAMA_BUILD_TESTS`
- `LLAMA_BUILD_EXAMPLES`
- `LLAMA_BUILD_APP`
- `LLAMA_BUILD_UI`

上游明确标注 CUDA architecture 75 = Turing。Runtime `--list-devices` 路径会加载 backend 并列举非 CPU 设备。

同 commit Release CI 的 Windows CUDA 12.4 完整 Build step：

```text
START=2026-09-18T22:26:50Z
END=2026-09-18T22:30:34Z
T_CI_FULL_BUILD=224s
```

该 CI 构建比本方案更宽：包含多个 CUDA architectures、完整默认目标；本机 CPU 较旧，因此 Virtual-99 不直接拿 224s 当现实预测。

## 3. Candidate attack

### R0 — 原预编译 CUDA 包

```text
STATUS=REALITY_INVALID
REASON=0xC000001D
T_VALID=INVALID
```

永久淘汰，不重试。

### R1 — CPU x64 package + existing CUDA package 直接混合

CPU package 使用：

```text
GGML_BACKEND_DL=ON
GGML_CPU_ALL_VARIANTS=ON
```

但 CUDA release build 未使用 `GGML_BACKEND_DL=ON`。

动态 loader 要求 CUDA DLL 导出：

```text
ggml_backend_init
```

而该导出只由 `GGML_BACKEND_DL_IMPL` 在 `GGML_BACKEND_DL=ON` 时生成。

```text
STATUS=VIRTUAL_REJECTED
REASON=BACKEND_PLUGIN_ABI_CONTRACT_NOT_MET
```

### R2 — CPU x64 package + 本机单独编译 CUDA plugin

理论可行，但引入：

- 预编译 CPU package 与本机构建 CUDA plugin 的编译器/CRT ABI 边界；
- 额外 package 下载；
- 与 R3 相同的主要 CUDA 编译成本。

```text
STATUS=VIRTUAL_REJECTED
REASON=NO_POSITIVE_TIME_GAIN_AFTER_ABI_RISK
```

### R3* — 同 commit、同工具链、最小本机 source build

唯一赢家。

冻结：

```text
SOURCE_COMMIT=9a9394a895b96003ca842a6041cb28ac49a108f7
GENERATOR=Visual Studio 17 2022
ARCH=x64
CUDA_TOOLKIT=existing 13.2
CUDA_ARCH=75-real

GGML_CUDA=ON
GGML_NATIVE=OFF
GGML_SSE42=ON
GGML_AVX=ON
GGML_AVX2=OFF
GGML_AVX_VNNI=OFF
GGML_BMI2=OFF
GGML_AVX512=OFF
GGML_AVX512_VBMI=OFF
GGML_AVX512_VNNI=OFF
GGML_AVX512_BF16=OFF
GGML_OPENMP=OFF
GGML_LLAMAFILE=OFF

LLAMA_BUILD_TESTS=OFF
LLAMA_BUILD_EXAMPLES=OFF
LLAMA_BUILD_APP=OFF
LLAMA_BUILD_UI=OFF
LLAMA_OPENSSL=OFF

BUILD_TARGETS=llama-server;llama-cli
PARALLEL_BUILD=4
```

注：不使用官方 `build_cuda_windows.ps1` 的默认 architecture 列表，因为其默认示例从 80 起，不包含本机 RTX 2080 Ti 的 sm_75。

## 4. Runtime validity gates

Reality 中 Runtime 只有同时满足以下条件才算 VALID：

```text
G1_SOURCE_COMMIT_EXACT=PASS
G2_CONFIGURE_EXIT=0
G3_BUILD_EXIT=0
G4_LLAMA_SERVER_PRESENT=PASS
G5_LLAMA_CLI_PRESENT=PASS
G6_LLAMA_SERVER_VERSION_EXIT=0
G7_LLAMA_CLI_VERSION_EXIT=0
G8_LIST_DEVICES_EXIT=0
G9_RTX_2080_TI_VISIBLE=PASS
G10_ILLEGAL_INSTRUCTION=0
G11_FILES_INSTALLED_TO_STAGING_ONLY=PASS
```

任何一门 FAIL：

```text
SAVE_EVIDENCE
STOP
RETURN_TO_STEP_2
```

禁止现场修参数。

## 5. Time model

定义：

```text
T_VALID_RUNTIME =
T_SOURCE
+ T_CONFIGURE
+ T_BUILD
+ T_VERSION_VERIFY
+ T_DEVICE_VERIFY
```

不计用户复制命令时间；从 deterministic harness 开始计时，到 G1-G11 全 PASS 为止。

Virtual-99 时间预算：

```text
T_SOURCE       <= 120 s
T_CONFIGURE    <=  60 s
T_BUILD        <= 360 s
T_VERIFY       <=  60 s
----------------------
min T_VALID    = 600 s
```

因此冻结：

```text
T_PHY_RUNTIME_MODEL_LOWER_BOUND ~= 300 s
MIN_T_VALID_VIRTUAL99 = 600 s
MIN_T_VALID_VIRTUAL99_HMS = 00:10:00
```

解释：

- 224s 是上游现代 GitHub Windows runner 对“更宽完整 CUDA build”的真实 Build step；
- 本机 i5-3570 较慢；
- 但本方案只构建 `sm_75-real`，只构建 `llama-server + llama-cli`，关闭 tests/examples/app/UI/OpenMP/llamafile；
- 600s 是从当前现实状态出发、包含源码获取和两层 Runtime 验证的 Virtual-99 冻结上限，而不是宣称现实已经跑到 600s。

Reality 判定：

```text
QUALITY_GATES_FAIL
=> RUNTIME_REALITY_FAIL
=> STOP / RETURN_TO_STEP_2

ALL_GATES_PASS AND T_VALID_REAL <= 600s
=> RUNTIME_REALITY_CERTIFIED

ALL_GATES_PASS AND T_VALID_REAL > 600s
=> RUNTIME_TIME_MODEL_FAIL
=> 保存时间分解
=> STOP / RETURN_TO_STEP_2
```

## 6. Frozen winner

```text
RUNTIME_WINNER=R3_MINIMAL_NATIVE_SOURCE_BUILD
VIRTUAL_99=PASS
MIN_T_VALID=600s
REALITY_CERTIFIED=NO
NEXT_STEP=3_REALITY_CERTIFICATION
```
