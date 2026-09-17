# 验收 — v1.9.0

英文：`ACCEPTANCE（验收）`

```text
技能ID = first-principles-physical-limit-convergence
版本 = 1.9.0
母技能身份门禁 = PASS
禁止自由探索 = YES
Codex只做确定性执行 = YES
```

## 四步主干

```text
第1步 物理极限 = PASS
第2步 本机现实最优区间 = PASS
第3步 GPT虚拟99 = PASS
第4步 Codex完整命令包 = PASS
```

## 简洁执行规则

```text
虚拟层允许反复攻击迭代 = YES
真实执行层逐步回GPT重规划 = NO
完整命令包一次走完 = YES
命令包内正常PASS/FAIL/ROLLBACK继续执行 = YES
未覆盖异常才返回GPT = YES
```

## Codex有限灵活性

```text
有限执行灵活性 = PASS
执行形式允许等价调整 = PASS
方案内容由Codex自行调整 = NO
```

允许：等价命令写法、脚本封装、路径修正、既定任务恢复。

禁止：换模型、换候选、换版本、改参数、改运行次数、改顺序、改阈值、新增性能剖析或新研究路线。

## 独立新路线

```text
新研究方向不插回当前主流程 = PASS
新研究方向记录为独立99路径 = PASS
独立99路径以后单独再走四步法 = PASS
```

## 其他核心原则

```text
单一端到端物理极限 = PASS
MRE最小真实执行 = PASS
本机现实状态模型 = PASS
成熟方案矩阵 = PASS
最终认证 = PASS
远端核验 = PASS
```

## v1.9.0 改动范围

v1.9.0 不改变第一性原理、MRE、成熟方案、虚拟99、质量门禁或99定义。

只纠正两个执行解释：

1. 完整命令包既然已经由 GPT 根据虚拟99一次设计完成，Codex 就应完整执行到底，不应把正常中间结果拆成一次次返回 GPT 的循环；
2. Codex 可以灵活调整执行形式，但绝不能自行改变方案内容。

```text
METHOD_LOGIC_ACCEPTANCE=PASS
SIMPLICITY_AUDIT=PASS
BOUNDED_EXECUTION_FLEXIBILITY=PASS
PLAN_MUTATION_BY_CODEX=NO
RUNTIME_INSTALLATION_1_9_0=NOT_VERIFIED
H3_FINAL_99=NO
```