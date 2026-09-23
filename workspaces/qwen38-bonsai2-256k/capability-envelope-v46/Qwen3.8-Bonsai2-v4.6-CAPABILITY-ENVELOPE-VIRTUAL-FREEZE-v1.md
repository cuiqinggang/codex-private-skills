# 千问3.8 27B1 — Bonsai 2 27B 本地智能体能力边界｜v4.6 虚拟成熟最终冻结 v1

## 0. 任务身份与连续时间

```text
PAGE=千问3.8 27B1
TASK=本地智能体能力边界 + 概率判断加速 + 自适应Thinking极限时间
TASK_TIME_ID=QWEN38-27B1-20260923T182700+0800
METHOD=极限短时间引擎 v4.6.0
PHASE=虚
TIME_RESET=FORBIDDEN
```

版本发布、虚→实、现实失败→返虚都继续同一个 `TASK_TIME_ID`；不得因新版本、新 runner 或 Reality Delta 清零。

历史 2026-09-23 18:27+08:00 起到精确计时器建立之前的主动工作已经真实发生，但没有 Stopwatch 分段证据，所以标记为 `HISTORICAL_UNINSTRUMENTED_ACTIVE=UNKNOWN_NOT_ZERO`，禁止伪造为 0，也禁止拿墙钟跨度冒充主动工作时间。

## 1. 简化后的唯一产品目标

不是证明“27B 什么都能做”，而是建立：

```text
CAPABILITY_ENVELOPE=能力边界图
+
ROUTE_TABLE=最短有效路由表
```

对每个任务区域记录：

- 能否稳定完成；
- 最大可用上下文；
- 最佳路由；
- 最佳 Thinking 档位；
- 是否适合概率引擎；
- `T_VALID` / P50 / P95；
- 首个稳定 FAIL 边界。

在所有质量硬门 PASS 的能力区内唯一优化：

```text
T*=min(T_VALID)
```

## 2. 冻结生产结构

```text
主智能体 = Bonsai 2 27B 本地模型
确定性明确任务 = Thinking OFF
有限结构化概率判断 = 优先评估 JEV/概率引擎
JEV 不适合/失败/低置信 = 本地 27B
轻微歧义 = LOW_512
局部失败 = MEDIUM_2048
多现实回执冲突 = HIGH_8192
HIGH 后仍不能安全收敛/需要重设计 = STOP -> GPT
```

外部 JEV 只作为可选加速器，不是硬依赖。只有同任务 A/B 满足全部质量门且 `T_VALID_JEV < T_VALID_LOCAL`，该任务类才正式路由到 JEV；否则使用本地 27B。

## 3. 工程闭环 A：token 总预算

旧 v3 的硬规则是：

```text
prompt + tool schema + reasoning + output <= 262144
```

旧 contradiction 已明确发现 16 个 `252-255K + HIGH_8192` 案例即使不计工具/输出也必然越界。

v4 修正为“总请求包络”：

```text
WINDOW=262144
SAFETY_MARGIN=512
FORMAL_CEILING=261632
TOOL_SCHEMA_RESERVE=2048
OUTPUT_RESERVE=1024
```

Thinking 保留：

```text
OFF=0
LOW=512
MEDIUM=2048
HIGH=8192
```

`252-255K` 档不再表示“无条件给 prompt 252-255K”，而表示“总请求接近窗口上限”。

结果：

- 原 16 个 HIGH 硬冲突：全部修复；
- 显式加入 tool/output reserve 后，额外发现 16 个 MEDIUM 也需要 prompt 缩短；
- 共 32 个 case 做 prompt payload clamp；
- case 数、域、Thinking 档位、能力要求均未删除；
- OFF/LOW 仍保留真正约 252K prompt 的近窗口压力测试；
- `TOKEN_ENVELOPE_OVERFLOW=0`。

## 4. 工程闭环 B：统一可执行 runner

冻结：

```text
BASE_SUITE=Qwen3.8-27B-Bstar-Executor-Cert-Suite-v3.json
PATCH=CAPABILITY-ENVELOPE-PATCH-v4.json
EFFECTIVE_SUITE=bstar-capability-envelope-v4（运行时由 v3 + patch 确定性生成）
RUNNER=BONSAI2-CAPABILITY-ENVELOPE-RUNNER-v2.py
```

runner 三个模式：

1. `self-test`：0 GPU / 0 模型调用，实例化全部 1018；
2. `emit-plan`：输出最短现实能力边界计划；
3. `reality`：调用已启动 llama-server；任何矛盾只写 Reality Delta + STOP。

现实 runner：
- 不下载模型；
- 不编译 runtime；
- 不修改代理/FlClash/系统设置；
- 使用 `/apply-template` + `/tokenize` 精确校准 prompt；
- 使用 `/completion`；
- `cache_prompt=true`；
- 所有 context band 使用嵌套共享前缀；
- 同一 band 不同 Thinking 路线复用公共 prefix；
- 失败不现场改题/改参数。

## 5. 1018/1018 零 GPU 自检 — 已真实执行

```text
UNITS_EXPECTED=1018
UNITS_INSTANTIATED=1018
GPU_RUNS=0
MODEL_CALLS=0

ATOMIC=592/592
JEV=240/240
THINKING=96/96
LONG_WORKFLOWS=18/18
CACHE=48/48
MEMORY=24/24

LONG_STEPS=1800
INJECTED_FAILURES=86

ORIGINAL_16_HARD_CONFLICTS_REPAIRED=PASS
TOKEN_ENVELOPE_OVERFLOWS=0

ATOMIC_FULL_PAIRWISE_PAIRS=800
ATOMIC_REALITY_ANCHORS=64
ATOMIC_ANCHOR_PAIRWISE_PAIRS=800

JEV_FULL_PAIRWISE_PAIRS=57
JEV_REALITY_ANCHORS=24
JEV_ANCHOR_PAIRWISE_PAIRS=57

SELFTEST=PASS
```

有效 suite canonical SHA256（v3 + patch 生成后）：

```text
9b94215208f55d2ac07065249d72eff113043f9cc18f7e8b8c103271e6487ba4
```

fixture digest：

```text
e4c465e2c61cfb9aed58d53e936488a4c656d33e9cdc79ccf0e8a6ea6992fa87
```

## 6. 极限时间优化后的现实策略

完整 1018 是能力宇宙，不再要求现实从头到尾逐题冷跑。

### 原子执行器

592 cases 的全部 800 个合法 pairwise 组合，可由 64 个锚点 100% 覆盖：

```text
592 -> 64 Reality anchors
PAIRWISE_COVERAGE=800/800
```

64 个锚点进一步按：

```text
8 context bands × 4 Thinking routes × 2 cases
```

合并为：

```text
32 个模型请求组
```

context 从 8K → 32K → 64K → 128K → 192K → 224K → 240-245K → 252-255K 单调增长，使用嵌套共享 prefix；因此不需要为每个 case 重付完整长上下文 Prefill。

### 概率判断

240 cases 的 type/confidence/ambiguity 全部 57 个 pairwise 组合压缩为：

```text
24 Reality anchors
57/57 pairwise coverage
```

外部 JEV 只做同任务 A/B；不可用时本地 27B 路线继续，不阻断整体认证。

### 长流程

6 类 archetype 使用冻结 ladder：

```text
先最短 rung
PASS -> 向更长 rung
FAIL -> 在该类停止并记能力边界
```

禁止为了“全 PASS”盲跑更长任务。

### Adaptive Expansion

只有出现 FAIL / ambiguous / 边界不闭合时，才从 1018 全量 catalog 中自动扩展相邻因素案例。

这使 Reality 的工作量由“全量证明所有题”改为“最短时间定位能力边界”。

## 7. 256K 与 Runtime 保留事实

继续复用已经成立的现实事实：

```text
MODEL=Ternary-Bonsai-2-27B-PQ2_0.gguf
MODEL_BYTES=7206168928
MODEL_SHA256=3907dc1658db1f78a9826bf8d5bcb8dc65db0d466388937af57f2294fae62ec1
RUNTIME_COMMIT=9a9394a895b96003ca842a6041cb28ac49a108f7
CPU=IvyBridge compatible
CUDA_ARCH=sm_75
CTX=262144
PRIMARY_KV=q8_0
Q4=hard-memory fallback only
SPECULATIVE=OFF
```

242054-token Reality Anchor 保留，不重复做旧质量认证。

## 8. 时间规则

v4.6 唯一计时：

```text
T_VALID_RUN = UNION(所有必要主动智能体工作区间)
```

计入：
- GPT 读取/搜索/虚拟成熟；
- runner/suite 构建与自检；
- GPT→Codex 交接；
- Codex 执行；
- Reality 验证；
- Reality Delta 返工；
- GPT 最终收口。

不计：
- 用户离开；
- 休息；
- 与任务无关的现实空档。

局部 `T_GPT/T_CODEX/T_REAL/T_VERIFY/T_REWORK` 仅诊断，不是第二优化目标。

当前开发 run 继续同一 TASK_TIME_ID，历史未仪表化主动时间保留为未知非零；从本次 instrumentation 开始写入精确段。成熟后另开 CLEAN TASK_TIME_ID 测真正 `T*`，但当前开发 run 的时间不得清零或伪装成 clean run。

## 9. 冻结门

```text
REALITY_FOUNDATION_SUFFICIENT=PASS
FINAL_VALID_CONDITION_DEFINED=PASS
TOKEN_ENVELOPE_GATE=PASS
SUITE_EXECUTABILITY_GATE=PASS
RUNNER_BINDING_GATE=PASS
ZERO_GPU_SELFTEST=1018/1018 PASS
ATOMIC_PAIRWISE_REALITY_REDUCTION=PASS
JEV_PAIRWISE_REALITY_REDUCTION=PASS
EXTERNAL_DEPENDENCIES_CLOSED=PASS
CODEX_POLICY_COMPATIBILITY=PASS
KNOWN_FAILURE_GATES=PASS
POSITION_AND_SEQUENCE_GATE=PASS
TIMING_CONTRACT_READY=PASS
EXECUTION_CHAIN_CLOSED=PASS
FROZEN_SOLUTION=PASS
HANDOFF_READY=PASS

VIRTUAL_COMPLETE=YES
REAL_ENTRY=READY
```

## 10. 下一状态

```text
VIRTUAL -> REAL
```

Reality 禁止现场修复或重新设计；任何矛盾：

```text
最小 Reality Delta
-> STOP
-> 同一 TASK_TIME_ID 返回虚
-> 时间继续累计，不重置
```