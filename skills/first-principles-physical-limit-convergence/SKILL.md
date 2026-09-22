---
name: first-principles-physical-limit-convergence
description: 极限短时间引擎 v4.2.0。机器 Skill ID 保留以兼容历史，但正式中文名改为“极限短时间引擎”。当前只有一虚一实。唯一锚定物不是提醒，而是所有实质判断的强制决策律：先过 VALID 硬门，再只比较 T_VALID；不能说明与 T_VALID 的关系，就不能冻结。实际验证没有现实 T_VALID，不得宣称完成。Foundation、成熟方案、JEV、Twin、缓存、GPU、自动化全部只能服务 T*=min(T_VALID)。
metadata:
  version: "4.2.0"
  display_name: "极限短时间引擎"
  legacy_machine_id: "first-principles-physical-limit-convergence"
  lineage: first-principles-physical-limit-convergence@4.2.0 <- @4.1.0 <- @4.0.0 <- @3.1.9
---

# 极限短时间引擎 v4.2.0

## 0. 正式名称与唯一锚定物

正式中文名：极限短时间引擎。
机器 Skill ID 暂不改名，以保持旧版本、旧分支、旧索引和 Codex 引用连续。
“第一性原理”保留为内部推导方法，不再占据主名称；主名称直接暴露唯一核心，避免长期工作后忘记真正目标。

唯一锚定物：

VALID = 正确性、质量、安全、权限、成本、资源等硬门全部通过
T_VALID = 从任务开始到第一个现实 VALID 结果出现的端到端时间
T* = min(T_VALID)

极限效率就是极限短时间的物理含义，不建立第二优化指标。

## 1. 锚定物是强制决策律，不是提醒

所有有实质影响的判断都必须遵守：先过 VALID，再只比较 T_VALID。

KEEP(x) 当且仅当：
1. VALID(x)=PASS；
2. x 有助于得到更小的 T_VALID。

如果一个动作既不影响 VALID，也不能降低 T_VALID，只是让系统更完整、更漂亮或更复杂，默认删除。

如果 TIME_RELATION=UNKNOWN，则不得把该候选冻结为当前最优；先测量、模拟、推导或缩小不确定性。
这不是第三步，只是虚和实共同遵守的唯一判定规则。

## 2. 一虚一实

流程只有：虚 -> 实；现实失败时 Reality Delta -> STOP -> 回虚。
正式标签第四字段仍只允许：虚、实。

### 虚 = 虚拟成熟

职责：在现实执行前，把候选方案竞争到唯一最小预测 T_VALID，并冻结。

虚内部可使用 Reality Foundation、Exact Reality Twin、动态成熟方案池、GPT/DeepSeek、JEV、确定性代码、verifier 攻击、Virtual-99、故障注入。
这些能力都没有独立目标。

每个实质候选至少必须有：
VALID_GATE=PASS|FAIL
PREDICTED_T_VALID=value|range|unknown
KEEP=YES|NO

冻结必须有：
SOLUTION_FROZEN=YES
VALID_GATE=PASS
PREDICTED_T_VALID_PRESENT=YES
FROZEN_SOLUTION=S*
EXECUTION_CONTRACT=deterministic
VERIFIER_CONTRACT=deterministic
EXPECTED_REALITY=minimum sufficient assumptions

没有可信时间值或区间的候选只能是研究材料，不能叫当前最优。

### 实 = 实际验证

职责：把冻结 S* 放进物理现实，得到真正的 VALID 和真正的 T_VALID。

必须明确计时起点、VALID 判定条件、第一个 VALID 结果时刻、T_VALID_REAL。

实际验证完成硬门：
VALID=PASS
T_VALID_REAL_PRESENT=YES

否则 REAL_VERIFY_COMPLETE=NO。
即使功能正确，如果没有现实时间，也不得宣称实际验证完成或现实最优。

INVALID run 的时间可以作为 Reality evidence，但不得进入 min(T_VALID)。

现实失败只允许：REALITY_DELTA=minimal sufficient delta；ACTION=STOP；RETURN_TO=虚。
执行器不得现场改方案。

## 3. 防漂移收口门

虚收口必须同时回答：
WHY_THIS_SOLUTION = 在 HARD_GATES=PASS 的候选中，它具有当前最小预测 T_VALID
PREDICTED_T_VALID=value|range

缺任一项：VIRTUAL_MATURITY=INCOMPLETE。

实收口必须同时有 VALID=PASS 和 T_VALID_REAL=value。
缺 T_VALID_REAL：REAL_VERIFY=INCOMPLETE。

任务总收口至少必须回答：当前现实最短有效时间是多少？
如果回答不了：TASK_EXTREME_TIME_STATUS=NOT_CLOSED。

## 4. 动态成熟方案池

旧赢家只是候选，不是永久权威。
是否继续搜索只看：继续搜索是否有现实可能进一步降低最终 T_VALID。
若没有：STOP_SEARCH。
防止成熟方案池反过来变成宏大工程。

## 5. Reality Foundation

local-ai-reality-foundation@1.1.0 继续作为虚的现实底座。
每个任务结束做吸收检查，但判据只有：新现实知识未来能否减少 T_VALID，或避免重复现实采集、重复踩坑。
不能则 ABSORB=NO；能则只吸收最小必要信息并形成新 Foundation 版本。

## 6. JEV 的成熟地位

JEV 不是第三步，也不是独立目标。
但 v4.x 要宣称成熟版之前，JEV 概率判断能力必须完成自己的极限适用度与极限时间成熟，并接入虚作为可选加速路径。

JEV_MATURITY_GATE=REQUIRED_BEFORE_V4_MATURE_FREEZE

具体节点只按：
T_WITH_JEV < T_WITHOUT_JEV 且 HARD_GATES=PASS -> USE_JEV
否则 -> NO_JEV

所以 JEV 接入是成熟能力要求，但是否实际调用仍由唯一锚定物决定。

## 7. 自动化一步化继续延后

gpt-codex-convergence-orchestrator@1.5.2 继续登记为未来一步化承载层。
当前 AUTOMATION_ATTACH=DEFERRED，LOCAL_DEPLOYMENT=DEFERRED。
先把 v4.x 两步本身跑成熟、把锚定物钉牢、完成 JEV 成熟接入，再讨论下一大版本的一步闭环。

## 8. 最终一句话

极限短时间引擎只有一个判定世界的方向：所有硬门通过以后，哪条现实路径能更早产生第一个 VALID 结果。虚负责把最短方案算出来并冻结，实负责把它在物理世界量出来；没有时间，就没有收口。