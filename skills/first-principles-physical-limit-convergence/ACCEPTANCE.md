# Acceptance — first-principles-physical-limit-convergence v3.1.1

## 唯一验收

当前方法只允许三个核心：

```text
CORE_1 = 极限短时间
CORE_2 = 成熟方案集群
CORE_3 = 高智能虚拟成熟
```

必须满足：

```text
CORE_COUNT=3
CORE_4_EXISTS=NO
THREE_CORE_WHITELIST=PASS
```

## 下一步白名单

任何下一步必须明确标注 CORE=1 / CORE=2 / CORE=3。

不能直接映射：

```text
BLACKLIST=YES
EXECUTE=NO
```

## 历史规则

旧版本、旧 command pack、L0/L1/L2/L3/L4、Shadow Pilot、Assisted Pilot 等：

```text
HISTORICAL_REFERENCE=ALLOWED
CURRENT_METHOD_AUTHORITY=NO
```

## 顺序

```text
1 极限短时间
-> 2 成熟方案集群
-> 3 高智能虚拟成熟
```

现实实现与案例验证属于第 3 核心冻结方案的验证动作，不建立第四层。

## 完成即交接

如果已经生成冻结方案/执行入口/命令包，且下一步需要外部执行器：

```text
HANDOFF_COMMAND_REQUIRED=YES
HANDOFF_SAME_REPLY=YES
HANDOFF_FIELDS=READ+DO+RETURN
HANDOFF_EXTRA_USER_TURN=0
```

只报告“完成”但没有给出可复制执行命令：

```text
DELIVERY_COMPLETE=NO
```

## 失败

现实验证失败：

```text
REALITY_DELTA
-> RETURN_TO CORE_3
-> RE-MATURE
-> RE-FREEZE
-> RE-VERIFY
```

## 最终验收

```text
TIME_ONLY_OBJECTIVE=PASS
MATURE_SOLUTION_CLUSTER_FIRST=PASS
HIGH_INTELLIGENCE_VIRTUAL_MATURITY=PASS
ALL_CURRENT_ACTIONS_MAP_TO_1_2_3=PASS
UNMAPPED_CURRENT_ACTIONS=0
HANDOFF_EXTRA_USER_TURN=0
FINAL_99_ALLOWED=YES
```
