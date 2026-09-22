# 极限短时间引擎 v4.4.0｜极简审计｜实证

## 冻结对象

```text
VERSION=4.4.0
BRANCH=codex/first-principles-physical-limit-convergence-v4.4.0
FROZEN_SKILL=UNCHANGED_DURING_REAL_VERIFY
```

## 固定现实基准

从开始读取真实仓库 `SKILL.md`，到完成以下共同有效判定并得到 PASS：
1. 唯一锚定物存在；
2. 虚有预测 T_VALID；
3. 实有现实 T_VALID；
4. 失败回虚；
5. 独立锚定合同不存在。

同一口径各运行 5 次，取最短有效时间 `T*=min(T_VALID)`。

## 现实结果

```text
v4.3 samples_ms=730,820,988,886,679
v4.3 T_VALID_MIN_MS=679
v4.3 P50_MS=820
v4.3 SKILL_CHARS=967

v4.4 samples_ms=625,748,908,602,778
v4.4 T_VALID_MIN_MS=602
v4.4 P50_MS=748
v4.4 SKILL_CHARS=713

MIN_TIME_REDUCTION=11.3%
P50_REDUCTION=8.8%
SKILL_CHAR_REDUCTION=26.3%
```

首次完整真实回读还执行了 13 项结构检查：

```text
REAL_READBACK_PASS=true
FULL_CHECK_T_VALID_REAL_MS=2651
CHECKS=13/13 PASS
```

## 漂移攻击

```text
BASE_VALID=PASS
REMOVE_ANCHOR=BLOCKED
REMOVE_PREDICTED_TIME=BLOCKED
REMOVE_FROZEN_SOLUTION=BLOCKED
REMOVE_REAL_TIME=BLOCKED
REMOVE_FAIL_LOOP=BLOCKED
ALLOW_EXECUTOR_REDESIGN=BLOCKED
REMOVE_DELETE_LAW=BLOCKED
ADD_THIRD_STEP=BLOCKED
ADD_SPECIFIC_TOOL_RULE=BLOCKED

ATTACKS=10/10 PASS
```

## 收口

```text
VALID_REAL=PASS
T_VALID_REAL*=602 ms
REALITY_DELTA=NONE
AUDIT_REAL=PASS
ACTION=STOP
```

说明：602 ms 是本次“共同仓库读取 + 固定结构判定”现实基准的最短有效时间，不冒充未来本地 Codex fresh session 的绝对执行时间。本次任务是方法极简审计；本地部署与 fresh session 行为验证仍属于后续部署验收，不进入本次核心方法。
