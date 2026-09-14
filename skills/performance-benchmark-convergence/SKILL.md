---
name: performance-benchmark-convergence
description: 将毫秒级性能优化的测量、A/A 校准、paired A/B、MDE、顺序效应、环境漂移、确认批次与 99 分收敛固化成可复用流程。适用于替换 workload/runner/output validator 后快速建立可信 benchmark；不保证性能达到 99，也不允许为 PASS 事后修改统计规则。
metadata:
  version: "0.1.0"
  short-description: 性能测试与99分收敛经验库
---

# 性能测试与 99 分收敛经验库

这是一个通用 benchmark 方法技能。目标不是替某个具体项目优化，而是把一次完整的毫秒级性能测试经验固化成可重复使用的认证流程，让后续项目只替换少量 profile 数据即可执行相同门禁。

## 核心原则

1. **先证明尺子可靠，再比较候选。** A/A 未通过前禁止候选裁决。
2. **固定 TASK/contract。** workload、输出语义、计时边界、validator 与环境变化都必须显式版本化。
3. **历史 baseline 不作为毫秒级候选唯一参照。** 使用同期 interleaved paired A/B。
4. **标签只能是 metadata。** A/B label 不得进入 workflow、filename、HTTP、session/client id 或计时内 evidence path。
5. **统计规则先冻结。** 不得看到结果后修改 alpha、CI、MDE、equivalence bound 或 KEEP 规则让旧批转 PASS。
6. **三门串行。** `STATISTICAL_SELFTEST`、`NULL_CALIBRATION`、`AA_CALIBRATION` 相互独立；前两门 PASS 不能覆盖第三门 FAIL/INCONCLUSIVE。
7. **99 是现实收敛状态，不是预设结果。** 本技能只保证测试路径严谨、可审计、可复用，不保证任何实现必然达到 99。

## 快速入口

新项目先复制并填写 [Benchmark Profile Template](templates/BENCHMARK-PROFILE.md)，然后严格执行 [Reusable Benchmark Playbook](references/PLAYBOOK.md)。

典型流程：

`PROFILE -> PREFLIGHT -> HARNESS FINGERPRINT -> LABEL-BLIND SELFTEST -> NULL CALIBRATION -> AUTHORITATIVE A/A -> PAIRED A/B -> CONFIRMATION -> 99/FREEZE or CONTINUE`

## 最小替换项

新任务通常只需要替换：

- `TASK_ID / CONTRACT_ID`
- workload/workflow/fixture
- runner 启动入口
- endpoint/runtime readiness
- `T_START/T_END` 计时边界
- output validator 与唯一正确结果定义
- evidence root
- 当前实现 A 与候选实现 B
- 环境指纹

统计逻辑、label-blind 规则、A/A 门禁、paired A/B 设计、失败证据保留原则默认复用，不要因项目不同随意重写。

## 结果状态

必须使用明确状态：

- `PASS`
- `FAIL`
- `INCONCLUSIVE`
- `INVALID_ENVIRONMENT_DRIFT`
- `INCONCLUSIVE_BELOW_MEASUREMENT_RESOLUTION`
- `BLOCKED_RUNTIME_PERMISSION`

不能把所有非 PASS 都写成 ROLLBACK。

## 99 分使用方式

99 分不是一个统计阈值，而是项目层收敛结论。只有在：

- benchmark 已校准；
- 当前 best implementation 有重复 confirmation；
- 高价值候选已被测试或有证据说明不适用；
- external frontier 已检查；
- 当前实现稳定；
- 剩余现实可行、低风险优化难以带来显著新增收益；

时，项目才能按自身方法论评估是否进入 99/FREEZE。

本技能禁止把“AA PASS”或“候选 KEEP”直接等同于“99”。

## 来源经验

首个成熟案例来自 `visual-art-engine-performance-ladder` P0 Measurement Protocol V2。该案例暴露并固化了：historical baseline drift、null false-positive、shared-A cluster、order equivalence、label leakage、harness fingerprint、Windows 长路径以及 runtime permission 等关键经验。

详细失败经验见 [FAILURE-LESSONS.md](references/FAILURE-LESSONS.md)。
