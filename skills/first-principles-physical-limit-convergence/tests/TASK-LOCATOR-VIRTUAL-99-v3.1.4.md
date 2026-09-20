# Task Locator Virtual-99 — v3.1.4

```text
STEP=2_VIRTUAL_99
REAL_EXECUTION=NO
FORMAT=【实际页面名｜具体任务名｜序号】
```

本轮用户已明确页面名：

```text
playwright浏览器自动化3
```

页面名来源规则：

```text
USER_PROVIDED -> EXACT_USE
ELSE SYSTEM_UI_TITLE -> USE
ELSE -> NO_GUESS
```

冻结案例：

| Case | 条件 | 预期 | 实际 |
|---|---|---|---|
| L01 | 用户给 `playwright浏览器自动化3`，标签原样使用 | PASS | PASS |
| L02 | 用户给页面名但模型改写/缩写 | BLOCK | BLOCK |
| L03 | 用户没给、系统可读真实标题 | PASS | PASS |
| L04 | 两者都没有却用任务名猜页面 | BLOCK | BLOCK |
| L05 | GPT 命令首行有标签、末行缺标签 | BLOCK | BLOCK |
| L06 | GPT 命令首尾同一标签 | PASS | PASS |
| L07 | Codex 最后一行原样回传三字段标签 | PASS | PASS |
| L08 | Codex 最后一行缺标签 | BLOCK | BLOCK |
| L09 | Codex 回传页面名不同 | BLOCK | BLOCK |
| L10 | Codex 回传任务名不同 | BLOCK | BLOCK |
| L11 | Codex 回传序号不同 | BLOCK | BLOCK |
| L12 | 上次命令无定位标签却宣告 REAL PASS | BLOCK | BLOCK |

```text
EXPECTED_CASES=12
ACTUAL_CORRECT=12
VIRTUAL_PASS=12/12
VIRTUAL_ACCURACY=100%
USER_PAGE_NAME_EXACT=PASS
GPT_COMMAND_LOCATOR_GATE=PASS
CODEX_RETURN_LOCATOR_GATE=PASS
FALSE_REAL_PASS_PREVENTED=PASS
```

STOP
