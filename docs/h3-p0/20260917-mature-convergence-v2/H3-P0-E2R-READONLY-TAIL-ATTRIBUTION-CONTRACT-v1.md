# H3-P0 E2R — E1 Tail Attribution Read-Only Contract v1

状态：`READY / ZERO_GPU / READ_ONLY`

目的：只使用已经存在的 E0/E1 证据，解释 Star7 KEEP 后三条 formal 中 Generation/Path 尾部的来源，为下一次 GPU 候选选择提供事实；不做新的优化测试。

## Identity / gates

```text
SKILL_ID=first-principles-physical-limit-convergence
REQUIRED_VERSION=1.8.0
NO_FREE_EXPLORATION=YES
CODEX_ROLE=DETERMINISTIC_VALIDATOR_EXECUTOR
GPU_RUNS_ALLOWED=0
NEW_INSTRUMENTATION=NO
NEW_PROFILER=NO
SOURCE_MODIFICATION=NO
NETWORK_PROXY_CHANGE=NO
```

## OBJECTIVE

对以下三个 E1 formal 样本做已有日志归因：

```text
910100: G=11.5185, P=3.4304, T=14.9489
910102: G= 3.1019, P=3.3823, T= 6.4843
910103: G= 2.4698, P=8.0919, T=10.5618
```

回答：

1. 910100 的 Generation tail 是否伴随 H3 load/offload/residency/reload/event；
2. 910103 的 Path tail 是否伴随 Qwen3-VL conditioning、VAE load/decode、H3→VAE transition 或其他已有可识别事件；
3. 910102 为什么形成当前 fast path；
4. formal seed changes 是否重复运行 text encoder，还是已有 node cache HIT；
5. 是否存在一个在现有证据中占 Total >=10% 的明确残余块。

## CURRENT_STATE

权威结果：`H3-P0-E1-RESULT.md/json`，E1=KEEP。

本机已有证据根：

`C:\AI\H3-P0-Acceptance\mature-convergence-v2\20260917-e0-e1-01`

只允许读取该阶段已经存在的：server logs、run json、summary、workflow、controller/state、已有标准输出/错误输出、已有时间标记。

## ALLOWED_CHANGE

无。

## ALLOWED_FILES_OR_COMPONENTS

只读：E1 evidence root、项目远端当前报告、已有 Star7 日志。

允许新写：

- `H3-P0-E2R-RESULT.md`
- `H3-P0-E2R-RESULT.json`

禁止修改模型、workflow、ComfyUI、Star7、samplers.py、Python 环境。

## BASELINE

E1 current winner 本身；这是归因任务，不做 A/B。

## SEEDS_AND_RUN_COUNT

```text
GPU_RUNS=0
TARGET_EXISTING_SEEDS=910100,910102,910103
```

## TIMING_BOUNDARY

不得创造新 timing。只能使用 E1 已记录的 authoritative Generation/Path/Total，以及已有日志中原本就存在的事件时间/顺序。

## QC_GATE

```text
NO_NEW_GPU_PROMPT=PASS
NO_FILE_MODIFICATION=PASS
NO_NEW_INSTRUMENTATION=PASS
ALL_CLAIMS_TRACEABLE_TO_EXISTING_EVIDENCE=PASS
```

无法从现有证据证明的内容必须写 `UNKNOWN`，不得推断成事实。

## EXPECTED_BOUNDED_OUTCOME

输出 attribution matrix：

| seed | Generation tail | Path tail | conditioning rerun/cache | H3 residency/load | VAE/transition | confidence |

并给每个残余候选以下裁决之一：

```text
MATERIAL
NOT_MATERIAL
ALREADY_CACHED
UNSUPPORTED_ON_CURRENT_HW
HIGH_RISK_DEFER
UNKNOWN_NEEDS_FUTURE_BOUNDED_TEST
```

## SUCCESS_RULE

成功不要求找到唯一根因；只要求把现有证据能证明/排除的部分完整分类，并明确下一 GPU 候选是否成熟。

## FAILURE / INCONCLUSIVE

若日志缺少足够事件：

```text
ATTRIBUTION_INCONCLUSIVE=YES
```

仍然写报告并 STOP；不得因此启动 profiler 或 GPU 重跑。

## ROLLBACK

无修改，所以无需 rollback；结束检查项目工作树无非预期修改。

## STOP_POINT

```text
WRITE RESULT
→ COMMIT/PUSH
→ REMOTE VERIFY
→ STOP
→ RETURN TO GPT
```

## TIME / CODEX BUDGET

```text
MAX_GPU_RUNS=0
WALL_BUDGET<=20min
CODEX_BUDGET=READ_ONLY_ONE_STAGE
```

## NEXT_ACTION_AFTER_EACH_OUTCOME

无论 MATERIAL / UNKNOWN / ALREADY_CACHED：都返回 GPT。Codex不得自行测试 INT8 text encoder、reserve-vram、host-sync、VAE 或 W4A8。
