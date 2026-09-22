# 极限短时间引擎 v4.4.0｜极简审计｜虚冻结

## 任务

在不降低有效性的前提下，把当前方法压到最短、最不易漂移的永久核心。

## 唯一标准

```text
T_VALID = 从审计任务开始到得到第一个有效、可冻结的方法结果的端到端时间
T* = min(T_VALID)
```

本任务的虚阶段不把“字数”冒充完整现实时间；字数只用于预测运行时读取/判断负担。冻结依据仍是：有效门先过，再预测总 T_VALID 更短。

## 有效硬门

```text
唯一锚定物直接位于 SKILL.md
只有虚/实两步
虚必须有预测时间与冻结方案
实必须有现实时间
现实失败=最小现实差异+停止+回虚
执行器不得现场改冻结方案
删除律直接服从 T_VALID
```

## 冻结方案

```text
VERSION=4.4.0
BRANCH=codex/first-principles-physical-limit-convergence-v4.4.0
FROZEN_SOLUTION=PASS
VALID_GATE=PASS
PREDICTED_T_VALID=LOWER_THAN_V4.3_FOR_METHOD_LOAD_AND_DECISION_PATH
```

预测依据：删除 JEV、自动化、具体工具等非永久方法规则；减少读取内容和判断分支，同时保留全部闭环硬门。

下一步只允许“实”：按冻结版本做现实读取回验、结构攻击和实际时间测量；不得在实阶段现场改方案。
