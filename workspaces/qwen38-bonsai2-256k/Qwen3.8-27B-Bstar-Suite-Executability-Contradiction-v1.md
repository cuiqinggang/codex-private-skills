# Qwen3.8 / Bonsai 2 B* — Suite Executability Contradiction v1

## 0. 定性

```text
CURRENT_STEP=2
CLASS=VIRTUAL_CONTRADICTION
SCOPE=FROZEN_CERTIFICATION_EXECUTABILITY
REALITY_EXECUTION=FORBIDDEN
```

Runtime-only Virtual-99 v2 在把 full-system `T_VALID` 绑定到最终 v3 认证时发现：现有 v3 Suite 只有结构化 case 元数据，没有与 `bstar-fixture-v3` 对应的可执行 fixture generator / runner binding；同时存在至少 16 个违反自身 context budget 硬门的 case。

因此：

```text
SUITE_EXECUTABILITY_GATE=FAIL
RUNNER_BINDING_GATE=FAIL
FULL_SYSTEM_MIN_T_VALID=UNRESOLVED
PROVISIONAL_TIME_MODEL=118:13:00
STEP3_ENTRY=FORBIDDEN
```

## 1. 数学不可执行矛盾

冻结 v3 规则：

```text
TARGET_CONTEXT=262144
request hard gate:
prompt_tokens + tool_schema_tokens + reserved_output_tokens <= 262144
```

冻结最高 context band：

```text
252-255K
```

冻结 reasoning route：

```text
HIGH_8192
```

即使取该 band 的最低 252 Ki tokens：

```text
252 * 1024 = 258048 prompt tokens
258048 + 8192 = 266240
266240 > 262144
```

此时还没有加入任何 tool schema 或 final output reserve，因此必然违反硬门。

经解析当前 `Qwen3.8-27B-Bstar-Executor-Cert-Suite-v3.json`，最高 band 中恰有 16 个 `HIGH_8192` Atomic cases：

```text
E1_PLAN_FIDELITY-059
E1_PLAN_FIDELITY-063
E2_STATE_CONTINUITY-059
E2_STATE_CONTINUITY-063
E3_FILE_CODE_MUTATION-059
E3_FILE_CODE_MUTATION-063
E4_TOOL_INVOCATION-059
E4_TOOL_INVOCATION-063
E5_FAILURE_RECOVERY-059
E5_FAILURE_RECOVERY-063
E6_VERIFICATION_EVIDENCE-059
E6_VERIFICATION_EVIDENCE-063
E7_LONG_CONTEXT_RESOURCE-059
E7_LONG_CONTEXT_RESOURCE-063
E8_STOP_SCOPE_DISCIPLINE-059
E8_STOP_SCOPE_DISCIPLINE-063
```

所以旧的：

```text
SUITE_INTEGRITY_GATE=PASS
PAIRWISE_COVERAGE=PASS
```

只能证明数量/组合覆盖完整，不能证明 case 在 262144 hard context 内可执行。

## 2. Runner / fixture 缺口

现有 Atomic case 只给出：

```text
fixture.generator=bstar-fixture-v3
seed
workspace_scope
context_band
tool_family
plan_shape
variant
injected_failure
distributed_needles
```

并给出抽象 oracle/invariant 名称。

但当前 Authority workspace 中没有 `bstar-fixture-v3` 的实现文件，也没有完整 Final Reality harness runner。现存的 `RUNTIME-R1-REALITY-VERIFY-v1.ps1` 只属于旧 60s CPU-backend-graft Runtime 测试，不能承担 v3 1018-unit certification。

因此 Codex 若现在进入 Reality，只能临场发明 fixture、prompt、expected output、tool semantics 或 runner；这属于 Step 3 现场重新设计，按固定闭环规则禁止。

## 3. 对 Runtime v2 时间模型的影响

Runtime candidate 本身已经收敛：

```text
RUNTIME_WINNER=
R1_SAME_RELEASE_DETERMINISTIC_AVX_SM75_SERVER_ONLY

T_RUNTIME_READY_MODEL=00:10:00
T_MODEL_READY_MODEL=01:48:00
PROVISIONAL_FULL_SYSTEM_TIME_MODEL=118:13:00
```

但由于 `T_CERTIFICATION` 尚没有可执行、确定性绑定的现实路径：

```text
MIN_T_VALID*=UNRESOLVED
```

`118:13:00` 只能保留为 provisional timing model，不得作为 Step 3 PASS/FAIL gate。

## 4. 唯一允许的 Step 2 修复方向

只重开认证的 **executability binding**，不重开 B* 模型选择、256K 目标、JEV 角色、Runtime winner 或质量门目标：

```text
1. 给 context band 定义可执行 token-envelope 语义；
2. 消除 252-255K × HIGH_8192 的硬冲突，同时保留真正接近 256K 的 OFF/低预算长上下文能力门；
3. 实现并冻结 bstar-fixture-v3 generator；
4. 每个 case 生成实际 PLAN / fixture / prompt / expected oracle / STOP；
5. 实现或绑定唯一 deterministic Reality runner；
6. runner self-test 必须在不调用 B* 的情况下证明所有 1018 units 可实例化、token budget 可满足、oracle 闭合；
7. 重新计算 full-system min T_VALID；
8. 只有上述全部 PASS 后才生成 Step 3 Reality command。
```

## 5. 当前状态

```text
RUNTIME_DESIGN=VIRTUAL_MATURE_CANDIDATE
RUNTIME_REALITY_CERTIFIED=NO
SUITE_EXECUTABILITY=FAIL
FULL_VIRTUAL_99=NOT_MATURE
MIN_T_VALID=UNRESOLVED
STEP3_COMMAND=WITHHELD_BY_GATE
NEXT_ACTION=CONTINUE_STEP_2_EXECUTABLE_SUITE_BINDING
```
