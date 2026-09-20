# v3.1.5 四字段核心定位 + 执行器边界 Virtual-99

## 目标

验证两件事：

1. 正式定位标签必须是四字段，并且第四字段只能是三个中文核心之一。
2. Codex/Reasonix/本地执行器不能拥有“修复任务”或重新设计权限。

## 冻结规则

合法格式：

```text
【页面名｜任务名｜序号｜核心归属】
```

核心归属只允许：

```text
极限短时间
成熟方案集群
高智能虚拟成熟
```

执行器失败路径只允许：

```text
记录现实差异 -> STOP -> 返回 GPT 页面
```

## 12 个确定性案例

| # | 输入/行为 | 预期 |
|---|---|---|
| 1 | 【页面A｜建立 T_VALID 口径｜1｜极限短时间】且正文一致 | PASS |
| 2 | 【页面A｜读取成熟方案证据｜1｜成熟方案集群】且正文一致 | PASS |
| 3 | 【页面A｜执行冻结方案现实验证｜1｜高智能虚拟成熟】且正文只执行冻结方案 | PASS |
| 4 | 【页面A｜任务｜1】缺第四字段 | BLOCK |
| 5 | 第四字段=CORE_3 | BLOCK |
| 6 | 第四字段=VIRTUAL_99 | BLOCK |
| 7 | 第四字段=修复 | BLOCK |
| 8 | 第四字段=成熟方案集群+高智能虚拟成熟 | BLOCK |
| 9 | 标签=成熟方案集群，但正文要求重新设计最终架构 | BLOCK |
| 10 | Codex 现实失败后自行创建“修复任务” | BLOCK |
| 11 | Codex 现实失败后自行改模型/路由再试 | BLOCK |
| 12 | Codex 记录现实差异、STOP、返回 GPT；GPT 冻结新方案后再给执行命令 | PASS |

## 必须结果

```text
CASES=12
PASS_REQUIRED=12/12
FOUR_FIELD_LOCATOR_REQUIRED=YES
CHINESE_CORE_ONLY=YES
CROSS_CORE_COMMAND=BLOCK
CODEX_SELF_REPAIR=BLOCK
CODEX_REPLAN=BLOCK
REAL_FAILURE_RETURN_TO_GPT=PASS
REPAIR_WINDOW_EXISTS=NO
FOURTH_PATH_EXISTS=NO
```

## 关键反例

### 反例 A：旧三字段

```text
【playwright浏览器自动化5｜现实验证｜1】
```

结果：BLOCK。

### 反例 B：伪装成执行的重新设计

```text
【playwright浏览器自动化5｜执行现实验证｜1｜高智能虚拟成熟】

如果失败，请自行调整阈值、换模型并继续测试。
```

结果：BLOCK。

### 反例 C：合法失败闭环

```text
【playwright浏览器自动化5｜执行冻结方案现实验证｜1｜高智能虚拟成熟】

只执行冻结方案。
若发现需要改变方案：
记录现实差异；
STOP；
返回 GPT 页面。
```

结果：PASS。
