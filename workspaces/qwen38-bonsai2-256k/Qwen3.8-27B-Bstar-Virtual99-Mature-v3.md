# Qwen3.8-27B / Bonsai 2 B* 256K Virtual-99 成熟冻结报告 v3.0

## 0. 状态

```text
PROJECT=qwen38-27b-bstar-256k-local-executor-jev
METHOD=first-principles-physical-limit-convergence v3.1.7
STAGE=VIRTUAL_99_MATURE_FREEZE_V3
MODEL_DOWNLOADS=0
GPU_MODEL_RUNS=0
CODEX_SOLVER_USED=0
B_STAR_BASE=Ternary Bonsai 2 27B PQ2_0
REAL_EXECUTOR_CERTIFIED=NO
```

**v1 的 23-probe 仅是外部 smoke evidence；v2 虽扩大到 1018 个单元，但重新审计发现：如果只检查“数量”，仍不足以证明组合状态覆盖完整。v3 的修正不是继续盲目加题，而是增加系统化组合覆盖、可执行 case contract、确定性 oracle 和结构覆盖审计。**

## 1. 唯一目标

```text
先要求：
JEV_GATE=PASS
EXECUTOR_GATE=PASS
LONG_CONTEXT_GATE=PASS
RECOVERY_GATE=PASS
STABILITY_GATE=PASS
SCOPE_DISCIPLINE_GATE=PASS
TIME_ACCOUNTING_GATE=PASS

全部 PASS 后唯一优化：
min T_SUITE_TOTAL
```

不能用速度抵消错误，也不能用一个综合分掩盖硬失败。

## 2. B* 角色

B* 不是高层规划大脑，而是执行 GPT / 第一性原理 / Virtual-99 已冻结成熟计划的具体执行层：

```text
冻结 PLAN
→ 当前 STEP
→ 允许工具
→ 真实 RECEIPT
→ 确定性 VERIFIER
→ STATE 哈希链
→ 有限恢复 / Adaptive Thinking
→ Evidence
→ STOP
```

开放式重新规划仍回 GPT。

## 3. 成熟系统栈

```text
MODEL=Ternary Bonsai 2 27B
PACKING=PQ2_0 (~7.21GB)
CTX=262144
RUNTIME=PrismML llama.cpp fork / pinned CUDA 12.4
N_GPU_LAYERS=99
PARALLEL=1
FLASH_ATTENTION=ON
TEXT_ONLY=YES
MMPROJ=OFF
SPECULATIVE=OFF
PRIMARY_KV=q8_0/q8_0
FALLBACK_KV=q4_0/q4_0 only on hard memory failure
PROMPT_CACHE=request cache_prompt:true
CTX_CHECKPOINTS=32
CACHE_RAM_START=4096 MiB
CACHE_IDLE_SLOTS=ON
EXTERNAL_STATE_LEDGER=YES
JEV_FIRST=YES
DETERMINISTIC_VERIFIER=YES
THINKING=ADAPTIVE
GPT_FINAL_ESCALATION=YES
```

### 外部确定性状态账本

```text
PLAN.json                  immutable
STATE.json                 current step / retries / blockers
RECEIPTS/                  raw tool receipts
EVIDENCE/                  readback/hash/test/browser evidence
ARTIFACT_MANIFEST.json     final expected artifacts + hashes
```

生产请求只携带当前工作集，不强迫每轮重新 Prefill 全部 256K；262144 仍是硬能力上限与压力门。

## 4. Thinking 冻结

```text
OFF          明确、确定性、正常路径
LOW_512      轻微歧义
MEDIUM_2048  局部失败/需要有限推理
HIGH_8192    多回执冲突/高风险恢复
GPT          HIGH 后仍无法安全收敛
```

Max/unlimited 不进入正常生产认证，因为无界时延与“极限短时间”目标冲突。

## 5. Codex 替代能力：8 个完整域

| 域 | 数量 | 重点 |
|---|---:|---|
| E1 Plan Fidelity | 64 | 顺序、DAG、分支、checkpoint、rollback、禁止项、计划哈希不变 |
| E2 State Continuity | 64 | 10/25/50/100/200 步、重试计数、版本、恢复一致性 |
| E3 File/Code Mutation | 96 | 精确写入、多文件、配置、代码修复、TDD、编码、幂等、部分写恢复 |
| E4 Tool Invocation | 80 | file/PowerShell/Git/HTTP/browser/local service/hash/multi-tool |
| E5 Failure Recovery | 96 | 非零退出、超时、缺文件、端口、checksum、JSON、网络、DOM、权限等 |
| E6 Verification/Evidence | 64 | readback、SHA256、测试码、schema、manifest、health、false-pass trap |
| E7 Long Context/Resource | 64 | 8K→252–255K，分散约束、working-set、cache controls、输出余量 |
| E8 STOP/Scope Discipline | 64 | STOP、blocker、禁止越权、代理/系统不可改、注入、重复动作 |

Atomic Executor = **592**。

## 6. v3 的关键升级：组合覆盖不是“题数堆积”

v3 把 6 个核心状态因子纳入系统化覆盖：

```text
Domain(8)
Context band(8)
Tool family(8)
Failure mode(8)
Plan shape(8)
Reasoning route(4)
```

592 个 Atomic cases 经覆盖数组构造后，**上述任意两个因子之间的全部合法取值组合均有至少一个 case 覆盖**。覆盖审计文件逐对记录 observed/possible/missing，要求 missing=0。

此外 E3/E4/E5 额外增加高风险三元组合压力，不把 pairwise 当成全部质量保证。

## 7. 长流程而不是“小题”

```text
8 × LONG-50  = 400 steps
6 × LONG-100 = 600 steps
4 × LONG-200 = 800 steps
TOTAL        = 1800 steps
Injected failures = 86
```

18 条长流程混合：多文件修改、本地服务、Git 分支收口、浏览器 deterministic fixture、HTTP 数据链、多工具故障恢复。

硬门：

```text
1800/1800 expected step outcomes
86/86 injected failures handled according to oracle
PLAN_DRIFT=0
FORBIDDEN_ACTIONS=0
FALSE_PASS=0
FINAL_MANIFEST_EXACT=18/18
STOP_DISCIPLINE=18/18
```

## 8. 256K 不再用 3 个 marker 糊弄

8 个 context bands：

```text
8K / 32K / 64K / 128K / 192K / 224K / 240-245K / 252-255K
```

最高两个 band 使用分散状态事实、依赖与禁止约束（32 needles/constraints 级），同时验证：

```text
首/中/尾远距离依赖
跨工具回执引用
约束保持
STATE 重建
token budget guard
no truncation
正确 STOP
```

任何 request 必须由 server tokenizer 实测，并满足：

```text
prompt_tokens + tool_schema_tokens + reserved_output_tokens <= 262144
```

## 9. JEV / Thinking / Cache / Memory

```text
JEV cases                240
Thinking routing cases    96
Prompt-cache trials       48
Memory/batch trials       24
Long workflows            18
Atomic executor          592
--------------------------------
Virtual scenario units  1018
Long workflow steps     1800
```

Prompt-cache 试验显式比较 cold/no-cache、warm `cache_prompt:true`、prefix-mutated control；必须读取 `timings.prompt_n`、`prompt_ms` 与 checkpoint restore 日志。

跨进程重启不把 `/slots save/restore` 当作可靠 prefix-cache 方案；重启后由外部 PLAN/STATE/RECEIPTS 重建工作集。

## 10. Virtual-99 的真实含义

```text
VIRTUAL_CONTROL_PLANE_COVERAGE=PASS
PAIRWISE_STATE_COVERAGE=100%
TEST_ORACLE_CLOSED=YES
REAL_MODEL_BEHAVIOR=UNKNOWN
REAL_EXECUTOR_CERTIFIED=NO
```

**这 1018 个单元在虚拟阶段验证的是：测试覆盖、状态机、oracle、权限边界、恢复路径和时间记账是否闭合。没有下载模型，就不能诚实宣称 B* 已经把 1018 个模型行为题全部答对。**

最终模型能力必须由现实认证包运行同一套 suite 得出。

## 11. 最终报告格式

只有所有质量硬门 PASS 才报告性能冠军指标：

```text
T_SUITE_TOTAL
T_SETUP
T_EXECUTOR_TOTAL
T_JEV_TOTAL
T_THINKING_TOTAL
T_LONG_WORKFLOW_TOTAL
T_LONG_CONTEXT_TOTAL
T_CACHE_TOTAL
T_MEMORY_TOTAL
P50_CASE
P95_CASE
T_PREFILL_TOTAL
T_REASONING_TOTAL
T_DECODE_TOTAL
T_TOOL_TOTAL
T_VERIFY_TOTAL
T_RECOVERY_TOTAL
```

最终状态只能是明确 PASS/FAIL 类状态，不输出模糊综合分。