# MULTI-AGENT PARALLELISM

```text
MORE_AGENTS != MONOTONICALLY_FASTER
```

## 两种时间

```text
T_EXEC = 固定任务真正运行的完成时间
T_CONVERGENCE = 研究、计算、审计、修改、测试、分析、决策收敛所需墙钟时间
```

研究型多智能体往往缩短 `T_CONVERGENCE`；不属于固定任务运行时的研究智能体不能计入 `T_EXEC`。

## 数量选择

理论并行上界可用 Amdahl 关系 sanity check：

```text
S(N) <= 1 / ((1-P) + P/N)
```

实际：

```text
T_AGENTS(N)
= T_RESOURCE_CRITICAL_PATH(N)
+ T_COORDINATION(N)
+ T_MERGE(N)
+ T_CONTENTION(N)

N_STAR = argmin_N T_AGENTS(N)
```

## Agent Spawn Gate

只有全部满足才增加智能体：

```text
INDEPENDENT_SUBTASKS >= 2
SUBTASK_TIME > ASSIGNMENT_OVERHEAD
NO_EXCLUSIVE_RESOURCE_CONFLICT = YES
OUTPUT_INDEPENDENTLY_VERIFIABLE = YES
EXPECTED_WALL_CLOCK_GAIN > 0
```

若 `MARGINAL_TIME_SAVED <= COORDINATION + MERGE + CONTENTION`，停止增加。

## 三种模式

- `OFF`：短任务、高串行、协调成本高。
- `SUPPORT_PARALLEL`：关键资源执行串行，辅助分析并行。
- `RESOURCE_PARTITIONED`：不同机器/GPU/独立资源可真实分区。

## STEP 1 推荐分工

复杂任务可并行：

```text
Agent A: PHYSICAL DAG / serial dependencies
Agent B: compute-bound lower bound
Agent C: memory / bandwidth / transfer lower bound
Agent D: machine sustainable-efficiency envelope
Agent E: external sanity references (optional)
Agent F: adversarial audit / assumption challenge
Integrator: unify contract, units and timing boundaries
```

Integrator 禁止简单平均互相矛盾结果。

## V1 命令包

复杂命令可采用 `AUTHOR_AGENT + AUDIT_AGENT`，审核合同漂移、不必要流程、计时、GPU async、可逆性、benchmark 污染、dirty worktree、repo closure、自动越权继续优化等。

## H3 类单 GPU 默认

```text
AGENT_MODE=SUPPORT_PARALLEL
GPU_RUN_SERIAL=YES
GPU_EXCLUSIVE=YES
CONCURRENT_GPU_HEAVY_AGENTS=0
```

研究、计算、审计可并行；避免多个智能体同时修改同一工作树。

正确原则：

```text
MAXIMIZE USEFUL_PARALLELISM
NOT MAXIMIZE AGENT_COUNT
```
