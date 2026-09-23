# 千问3.8 27B1 — 本地智能体能力边界 + 极限时间 v4.6 虚拟成熟冻结

## 1. 项目唯一目标

本项目不再把“256K、执行器、JEV、Thinking”拆成互相独立的目标。

唯一目标：

```text
建立 Bonsai 2 27B 本地智能体的能力边界图；
对每一个现实可用能力区间，在全部质量硬门 PASS 的前提下求：
T* = min(T_VALID)
```

最终生产结构：

```text
本地 27B 智能体
+ JEV 概率判断加速器（可选、非单点依赖）
+ 按需 Thinking（思考模式）
+ 独立确定性验证器
```

## 2. 冻结路由

```text
明确/确定性任务
-> 本地 27B，Thinking OFF（关闭思考）

有限、结构化、可验证判断
-> JEV 优先候选
-> 只有预计整体 T_VALID 更短才采用
-> JEV 不可用/失败/低置信立即回本地 27B

轻微歧义
-> LOW_512（低思考，最多 512 token）

局部失败
-> MEDIUM_2048（中思考，最多 2048 token）

多回执冲突/高风险恢复
-> HIGH_8192（高思考，最多 8192 token）

仍不能安全收敛或需要重新设计
-> STOP
-> GPT
```

JEV 不成为本地智能体启动的硬依赖。

## 3. 旧 1018 测试资产完整继承

```text
Atomic Executor（原子执行器） = 592
JEV structured decision（结构化概率判断） = 240
Adaptive Thinking（自适应思考） = 96
Long workflows（长流程） = 18
Long workflow steps（长流程步骤） = 1800
Injected failures（故障注入） = 86
Prompt-cache trials（提示词缓存） = 48
Memory/batch trials（内存/批处理） = 24
--------------------------------
Virtual scenario units（虚拟场景单元） = 1018
```

原 v3 的 15 组两两组合覆盖全部保留，不删除原题库。

## 4. 16 个 token 预算冲突已闭环

旧错误：

```text
252-255K prompt
+ HIGH_8192 reasoning
> 262144 总窗口
```

新统一规则：

```text
prompt
+ reasoning
+ tool schema（工具定义）
+ output reserve（输出预留）
+ guard（保护余量）
<= 262144
```

仅 16 个旧 `252-255K + HIGH_8192` 案例需要改成：

```text
NEAR_BOUNDARY_TOTAL_ENVELOPE
= 接近总窗口上限的总预算测试
```

其 prompt 自动缩到安全上限；`252-255K` 的真实大 prompt 能力仍由同档 OFF / LOW / MEDIUM 案例保留，因此没有降低 256K 能力门。

修正案例数：

```text
16/16
```

## 5. 统一测试运行器已物化

唯一运行器：

```text
BSTAR-CAPABILITY-HARNESS-v46.py
```

唯一覆盖层：

```text
Qwen3.8-27B-Agent-Capability-Overlay-v46.json
```

运行器支持：

```text
self-test       = 零 GPU 全套结构自检
materialize     = 物化全部测试夹具
frontier-plan   = 生成最短现实能力边界首轮
probe           = 单案例现实探针
reality-frontier= 现实能力边界首轮
```

六类测试均已有唯一处理器：

```text
ATOMIC_AGENT_DECISION
= 原子执行判断

JEV_OR_LOCAL_STRUCTURED_DECISION
= JEV / 本地结构化判断

THINKING_ROUTE_DECISION
= 思考档位路由

LONG_WORKFLOW_CONTROLLER
= 长流程控制

CACHE_RUNTIME_PROBE
= 缓存运行探针

MEMORY_RUNTIME_PROBE
= 内存/批处理运行探针
```

## 6. 1018/1018 零 GPU 自检结果

实际执行结果：

```text
GPU_RUNS=0
NETWORK_CALLS=0
MODEL_CALLS=0

SUITE_UNITS=1018/1018
TOKEN_CORRECTIONS=16/16
EXECUTION_CHAIN_CLOSED=PASS
RUNNER_BINDING_CLOSED=PASS
SELFTEST=PASS
```

fixture manifest（测试夹兛清单）：

```text
SHA256=f686fa72d40c4726f31d7bea52a4e0428d8176cbfcfde651a417bdba2419e365
```

## 7. 为极限时间做的现实测试压缩

不再一上来逐个现实执行 1018 单元。

使用数学最小两两覆盖首轮：

```text
Atomic（原子执行）       64 / 592
JEV（概率判断）          24 / 240
Thinking（思考路由）      4 / 96
Long workflow（长流程）  16 / 18
Cache（缓存）            24 / 48
Memory（内存）           12 / 24
--------------------------------
首轮现实锚点             144
```

覆盖结果：

```text
Atomic pairwise（两两组合）      800/800
JEV pairwise                     57/57
Thinking pairwise                12/12
Long workflow pairwise           31/31
Cache pairwise                   69/69
Memory pairwise                  28/28
MISSING=0
```

现实扩展规则：

```text
PASS 且稳定
-> 不扩大

FAIL
-> 扩展所有与失败点共享两个因素的邻域案例

不稳定
-> 5 次复测
-> 仍不确定再扩到 20 次

能力边界
-> 邻近上下文 / Thinking 档位二分定位

需要最终全认证
-> 1018 全量池仍可直接运行
```

因此测试压缩不会删除能力维度，只删除无信息增益的重复现实执行。

## 8. 长上下文运行绑定

现实运行器在真正调用本地模型前会：

```text
调用 /tokenize
-> 按冻结 token envelope（token 总预算）构造 prompt
-> 确保实际 prompt tokens <= 冻结上限
```

128K 及以上模型案例同时加入首/中/尾三处分散 `CTX_MARKER`（上下文标记），要求模型在最终 JSON 中准确返回，避免“只是塞满上下文但没有真正读取”的假通过。

## 9. 时间规则

```text
TASK_TIME_ID=BONSAI2-256K-V46-CLOSEOUT-V2-20260923
```

同一个 `TASK_TIME_ID` 必须跨：

```text
虚 -> 实
实 FAIL -> 虚
版本升级
重新发布
```

连续继承，不允许清零。

v4.6 正式口径：

```text
T_VALID_RUN
= 所有必要主动智能体工作区间的并集
```

用户离开/纯等待不计入主动时间，但时间身份与累计值不能重置。

历史 2026-09-23 18:27 之后已有一段主动工作未用 Stopwatch 精确采集：

```text
HISTORICAL_ACTIVE_TIME=NONZERO_UNINSTRUMENTED
```

不得伪造为 0，也不得用墙钟差冒充。

本次恢复后已开始精确连续计时：

```text
EXACT_CONTINUATION_START=2026-09-23T21:22:24.614753+08:00
ACTIVE_CHECKPOINT_MS=700815.591
```

后续 Reality handoff（现实交接）继续使用同一 TASK_TIME_ID 和累计值。

## 10. 虚阶段门禁

```text
REALITY_FOUNDATION_SUFFICIENT=PASS
FINAL_VALID_CONDITION_DEFINED=PASS
SUITE_EXECUTABILITY=PASS
TOKEN_BUDGET_GATE=PASS
EXECUTION_CHAIN_CLOSED=PASS
RUNNER_BINDING_CLOSED=PASS
EXTERNAL_DEPENDENCIES_CLOSED=PASS
CODEX_POLICY_COMPATIBILITY=PASS
KNOWN_FAILURE_GATES=PASS
TIMING_CONTRACT_READY=PASS
FROZEN_SOLUTION=PASS
HANDOFF_READY=PASS

VIRTUAL_COMPLETE=YES
```

## 11. 下一状态

```text
CURRENT_PHASE=实
```

现实阶段只能执行冻结运行器、记录时间和现实证据。

任何需要改题、改路由、改参数、改验证器的情况：

```text
Reality Delta（现实差异）
-> STOP
-> RETURN_TO_VIRTUAL
```

禁止现实现场修复。
