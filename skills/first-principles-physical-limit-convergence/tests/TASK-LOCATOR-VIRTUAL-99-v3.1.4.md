# Task Locator Virtual-99 — v3.1.4

```text
STEP=2_VIRTUAL_99
REAL_EXECUTION=NO
VISIBLE_FIELDS=3
FORMAT=【实际页面名｜具体任务名｜序号】
```

基准页面：

```text
Bonsai 2 27B / 256K 主项目
```

基准任务：

```text
准备现实运行材料
```

冻结案例：

| Case | 条件 | 预期 | 实际 |
|---|---|---|---|
| T01 | 正确页面 + 正确任务 + 1 | PASS | PASS |
| T02 | 同一页面的另一个任务从 1 开始 | PASS | PASS |
| T03 | 同一任务允许到 6 | PASS | PASS |
| T04 | 页面名与真实页面不一致 | BLOCK | BLOCK |
| T05 | 用任务名冒充页面名 | BLOCK | BLOCK |
| T06 | 任务名与当前任务不一致 | BLOCK | BLOCK |
| T07 | 序号为 0 | BLOCK | BLOCK |
| T08 | 序号为 7 | BLOCK | BLOCK |
| T09 | 序号写成 001 | BLOCK | BLOCK |
| T10 | ORDER/ANSWER 三字段完全一致 | PASS | PASS |
| T11 | ORDER/ANSWER 任务字段不一致 | BLOCK | BLOCK |
| T12 | 增加 CORE 等第四个可见字段 | BLOCK | BLOCK |

确定性虚拟重放：

```text
EXPECTED_CASES=12
ACTUAL_CORRECT=12
VIRTUAL_PASS=12/12
VIRTUAL_ACCURACY=100%
PAGE_IS_ACTUAL_UI_TITLE=PASS
MULTI_TASK_SAME_PAGE=PASS
PER_TASK_SEQUENCE=PASS
TASK_NAME_CANNOT_REPLACE_PAGE_NAME=PASS
THREE_FIELD_PAIRING=PASS
EXTRA_VISIBLE_FIELD_REJECTED=PASS
CORE_GATE_DUPLICATION=0
FOURTH_CORE_CREATED=NO
FOURTH_STEP_CREATED=NO
```

说明：100% 仅指上述 12 个冻结定位案例全部符合预期。

STOP
