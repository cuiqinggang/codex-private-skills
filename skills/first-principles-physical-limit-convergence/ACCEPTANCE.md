# Acceptance — first-principles-physical-limit-convergence v3.1.6

## 1. 三核心唯一白名单

必须满足：

```text
核心数量=3
第四核心存在=否
核心1=极限短时间
核心2=成熟方案集群
核心3=高智能虚拟成熟
```

任何当前动作必须真实、唯一地映射到三个核心之一。

不能唯一映射：

```text
发布命令=否
执行=否
动作=停止
```

## 2. 四字段任务定位

正式命令第一行和最后一行必须完全一致：

```text
【实际页面名｜具体任务名｜序号｜核心归属】
```

验收：

```text
VISIBLE_FIELDS=4
FIELD_1=ACTUAL_PAGE_NAME
FIELD_2=TASK_NAME
FIELD_3=SEQ
FIELD_4=EXACT_CHINESE_CORE_NAME
```

第四字段只允许：

```text
极限短时间
成熟方案集群
高智能虚拟成熟
```

以下均必须 BLOCK：

- 只有原三字段；
- 第四字段为空；
- 第四字段使用 CORE_1 / CORE_2 / CORE_3；
- 第四字段使用 STEP 1 / STEP 2 / STEP 3；
- 第四字段使用英文别名；
- 第四字段写“修复/补丁/优化/验收”等自造类别；
- 第四字段同时写两个或三个核心；
- 标签核心与命令正文实际工作不一致；
- 页面名由执行器猜测；
- 首尾标签不一致。

机器定位键：

```text
LOCATOR_KEY=PAGE_NAME+TASK_NAME+SEQ+EXACT_CHINESE_CORE_NAME
```

## 3. 序号验收

```text
SEQ_SCOPE=PER_TASK
SEQ_FORMAT=PLAIN_INTEGER
SEQ_IS_COUNT_ONLY=YES
REPAIR_WINDOW_EXISTS=NO
```

v3.1.4 的“4..6 修复窗口”语义必须不存在。

执行器失败后不得把下一序号解释成修复权限。

## 4. Codex / Reasonix / 本地执行器权限

必须满足：

```text
EXECUTOR_ROLE=FROZEN_COMMAND_EXECUTOR_ONLY
CODEX_REPAIR_TASK_ALLOWED=NO
CODEX_REPLAN_ALLOWED=NO
CODEX_VIRTUAL_MATURITY_ALLOWED=NO
CODEX_NEW_ROUTE_ALLOWED=NO
GPT_PAGE_OWNS_REPAIR_DESIGN=YES
GPT_PAGE_OWNS_VIRTUAL_MATURITY=YES
```

执行器允许：

- 执行 GPT 已冻结命令；
- 做命令明确要求的确定性读写/运行/测试/部署/现实验证；
- 收集事实；
- 记录现实差异；
- 回传；
- 停止。

执行器不允许：

- 自己建立“修复任务”；
- 自己决定修复办法；
- 自己重新设计；
- 自己增加候选路线；
- 自己更换模型、阈值、路由、fallback、验证合同；
- 失败后继续自由探索。

如果现实失败：

```text
记录现实差异
-> 停止
-> 返回 GPT 页面
```

之后只能由 GPT 页面重新进入三个核心之一。

## 5. 已冻结修正方案的执行

如果 GPT 已经完成：

```text
问题分析
-> 高智能虚拟成熟
-> 方案冻结
```

Codex 可以执行该冻结方案。

但正式任务不得定义为“Codex 修复”。

其语义必须是：

```text
执行冻结方案
或
执行冻结方案现实验证
```

并用第四字段标明真实核心归属。

## 6. 三核心失败闭环

唯一合法闭环：

```text
现实失败
-> 执行器记录现实差异并停止
-> GPT 页面
-> 极限短时间 / 成熟方案集群 / 高智能虚拟成熟（三选一）
-> GPT 冻结新的执行命令
-> 执行器再次执行
```

禁止：

```text
现实失败
-> Codex 自己修
-> Codex 再试
```

## 7. 完成即交接

虚拟成熟已经 PASS 且存在冻结执行源时：

```text
SAME_REPLY_HANDOFF_REQUIRED=YES
HANDOFF_EXTRA_USER_TURN=0
ONE_EXECUTION_SOURCE_OF_TRUTH=YES
```

交接命令也必须使用四字段中文核心定位标签。

## 8. 全局接收端兜底

`~/.codex/AGENTS.md` 的全局门禁必须最终升级为：

```text
【页面名｜任务名｜序号｜核心归属】
```

并检查第四字段只能是三个中文核心之一。

缺失、错误、正文不匹配：

```text
BLOCK
STOP
```

即使当前 Skill 没有加载，接收端也不得允许 Codex 自行修复或重新设计。

## 9. v3.1.6 虚拟验收要求

必须至少覆盖：

```text
有效核心1标签
有效核心2标签
有效核心3标签
缺第四字段
英文核心字段
非法第四字段
多个核心同时出现
正文/标签核心冲突
Codex 自行修复
Codex 自行重新设计
失败后 Reality Delta + STOP
GPT 冻结方案后 Codex 仅执行
```

要求：

```text
PASS_REQUIRED=12/12
FOUR_FIELD_LOCATOR=PASS
CHINESE_CORE_ONLY=PASS
EXECUTOR_ONLY_GATE=PASS
NO_REPAIR_WINDOW=PASS
NO_FOURTH_PATH=PASS
```

## 10. 最终验收

```text
TIME_ONLY_OBJECTIVE=PASS
MATURE_SOLUTION_CLUSTER_FIRST=PASS
HIGH_INTELLIGENCE_VIRTUAL_MATURITY=PASS
THREE_CORE_ONLY=PASS
VISIBLE_LOCATOR_FIELDS=4
CHINESE_CORE_FIELD_REQUIRED=PASS
CODEX_EXECUTOR_ONLY=PASS
CODEX_SELF_REPAIR=FORBIDDEN
REAL_FAILURE_RETURNS_TO_GPT=PASS
UNMAPPED_CURRENT_ACTIONS=0
FINAL_99_ALLOWED=YES
```


## 11. v3.1.6 现实锚定与精确数字孪生验收

```text
REALITY_ANCHOR_SKILL_VERSION=1.1.0
REALITY_FINGERPRINT_V3_PRESENT=PASS
CRITICAL_UNKNOWN_COUNT=0
CRITICAL_EXECUTION_STATE_COVERAGE_PERCENT=100.00
EXACT_TWIN_VERSION=1.0.0
EXACT_TWIN_CHINESE_NAME=现实执行环境精确数字孪生唯一版
TWIN_CONTRACT_SELFTEST=24/24 PASS
TWIN_REALITY_MODE_MUTATION=FORBIDDEN
SHADOW_RELABEL_AS_REALITY=FORBIDDEN
REALITY_SHADOW_RUN=NOT_YET
ENVIRONMENT_99=NOT_YET
FOURTH_CORE_CREATED=NO
```

Twin 必须先复现 SetTokenInformation/1344 的 3/3 现实边界，之后才允许研究 Shadow 硬化方案。
