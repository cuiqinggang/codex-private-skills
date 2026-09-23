# 千问3.8 27B1 — v4.6 当前唯一入口

```text
PAGE=千问3.8 27B1
PROJECT=qwen38-bonsai2-agent-capability-envelope
METHOD=极限短时间引擎 v4.6.0
TASK_TIME_ID=BONSAI2-256K-V46-CLOSEOUT-V2-20260923
CURRENT_PHASE=实
VIRTUAL_COMPLETE=YES
REAL_ENTRY=READY
MODEL=Ternary Bonsai 2 27B PQ2_0
TARGET_CONTEXT=262144
DOWNLOAD=COMPLETE
RUNTIME_BUILD=COMPLETE
COLD_242K_REALITY_ANCHOR=PASS
```

## 当前目标

只做一件事：测清本地 27B 智能体的能力边界，并在每个有效能力区间内求最短有效时间 `min(T_VALID)`。

生产组合：
- 本地 27B 智能体；
- JEV 概率判断加速器（可选、非单点依赖）；
- 按需 Thinking（思考模式）；
- 独立确定性验证器。

## 虚阶段已完成

```text
SUITE_UNITS=1018/1018
TOKEN_BUDGET_CONFLICTS_FIXED=16/16
ZERO_GPU_SELFTEST=PASS
EXECUTION_CHAIN_CLOSED=PASS
RUNNER_BINDING_CLOSED=PASS
FRONTIER_INITIAL_UNITS=144
ATOMIC_PAIRWISE=800/800
JEV_PAIRWISE=57/57
THINKING_PAIRWISE=12/12
LONG_PAIRWISE=31/31
CACHE_PAIRWISE=69/69
MEMORY_PAIRWISE=28/28
MISSING_PAIR=0
```

首轮现实只跑 144 个能力边界锚点；PASS 且稳定不扩展，FAIL/不稳定/边界不清时按冻结规则扩展邻域；完整 1018 池保留用于最终全认证。

## 当前权威资产

- `Qwen3.8-27B-Agent-Capability-VIRTUAL-FREEZE-v46.md` — 虚拟成熟冻结。
- `Qwen3.8-27B-Agent-Capability-SELFTEST-v46.json` — 1018/1018 零 GPU 自检证据。
- `TIME-LEDGER-v46.json` — v4.6 连续时间账本。
- `Qwen3.8-27B-Agent-Capability-SOURCE-v46.tar.gz` — 完整运行器 + 覆盖层源包。
- `Qwen3.8-27B-Bstar-Executor-Cert-Suite-v3.json` — 原 1018 全量题库。

源包 SHA256：
`fa601064245f588bd89bb78f7241a9d74130f2f67ab91e3b378623be77d924ee`

## 现实阶段固定规则

```text
清晰确定任务 -> 本地 27B / Thinking OFF
有限结构化判断 -> JEV 仅在预计整体 T_VALID 更短时采用
JEV 不可用/失败/低置信 -> 本地 27B
轻微歧义 -> LOW_512
局部失败 -> MEDIUM_2048
多回执冲突/高风险恢复 -> HIGH_8192
仍无法安全收敛/需要重新设计 -> STOP -> GPT
```

现实只允许执行冻结运行器、采集现实证据和时间。
任何需要改题、改路由、改参数或改验证器的情况：

```text
Reality Delta（现实差异）
-> STOP
-> RETURN_TO_VIRTUAL
```

禁止现实现场修复。

## 时间连续性

同一 `TASK_TIME_ID` 跨以下状态永久连续：

```text
虚 -> 实
实 FAIL -> 虚
版本升级
重新发布
```

不得清零。历史未精确计时部分标记为 `NONZERO_UNINSTRUMENTED`；后续使用高精度主动工作时间接力。