# Global Locator Dual Gate Virtual-99 v3.1.5

定位任务：

```text
页面=playwright浏览器自动化5
任务=四字段中文核心双门禁
核心归属=高智能虚拟成熟
现实执行=否
```

## 冻结规则

发送端与接收端都必须要求：

```text
【页面名｜任务名｜序号｜核心归属】
```

第四字段只允许：

```text
极限短时间
成熟方案集群
高智能虚拟成熟
```

Codex 只执行冻结命令，不得自行修复、重新设计或虚拟成熟。

## Virtual-99 cases

| Case | 条件 | 预期 | 虚拟结果 |
|---|---|---|---|
| G01 | GPT 命令四字段完整且正文核心一致 | PASS | PASS |
| G02 | 仍使用旧三字段标签 | BLOCK | BLOCK |
| G03 | 第四字段为空 | BLOCK | BLOCK |
| G04 | 第四字段为 CORE_3 / STEP 2 / VIRTUAL_99 | BLOCK | BLOCK |
| G05 | 第四字段为“修复” | BLOCK | BLOCK |
| G06 | 第四字段同时包含两个核心 | BLOCK | BLOCK |
| G07 | 标签核心=成熟方案集群，正文要求重新设计 | BLOCK | BLOCK |
| G08 | Skill 未加载，但全局 AGENTS 四字段门禁存在；收到旧三字段 | BLOCK | BLOCK |
| G09 | Codex 执行后最后一行原样回显四字段标签 | PASS | PASS |
| G10 | Codex 最后一行核心字段变化 | BLOCK | BLOCK |
| G11 | 现实失败后 Codex 自行修/换路线继续 | BLOCK | BLOCK |
| G12 | 现实失败后只记录差异、STOP、返回 GPT | PASS | PASS |

```text
EXPECTED_CASES=12
ACTUAL_CORRECT=12
VIRTUAL_PASS=12/12
VIRTUAL_ACCURACY=100%
FOUR_FIELD_LOCATOR=PASS
CHINESE_CORE_ONLY=PASS
CORE_BODY_CONSISTENCY=PASS
CODEX_EXECUTOR_ONLY=PASS
CODEX_SELF_REPAIR=BLOCKED
REALITY_DELTA_RETURN_TO_GPT=PASS
NO_FOURTH_PATH=PASS
```

STOP
