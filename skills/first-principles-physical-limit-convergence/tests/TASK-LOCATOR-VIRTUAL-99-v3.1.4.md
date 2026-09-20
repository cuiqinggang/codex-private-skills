# Task Locator Virtual-99 — v3.1.4

```text
STEP=2_VIRTUAL_99
REAL_EXECUTION=NO
VISIBLE_FIELDS=2
FORMAT=【页面名｜序号】
```

唯一基准：

```text
【第一性原理极限短时间引擎v3.1.4｜1】
```

机器解析只认：

```text
PAGE_NAME = 第一段完整字符串
SEQ = 第二段普通整数
LOCATOR_KEY = PAGE_NAME + "|" + SEQ
```

冻结案例：

| Case | 输入/条件 | 预期 |
|---|---|---|
| T01 | `【第一性原理极限短时间引擎v3.1.4｜1】` | PASS |
| T02 | `【Bonsai 27B 256K｜6】` | PASS |
| T03 | 序号为 0 | BLOCK |
| T04 | 序号为 7 | BLOCK |
| T05 | 序号写成 001 | BLOCK |
| T06 | 增加 CORE/STEP/ROLE/STATUS 等可见字段 | BLOCK |
| T07 | 同页面按 1→2→3 单调递增 | PASS |
| T08 | 3 未闭环，记录原因后进入 4→5→6 | PASS |
| T09 | 6 后仍试图继续 7 | BLOCK |
| T10 | 页面首次编号后，定位名称沿用首次冻结名称 | PASS |

确定性重放：

```text
EXPECTED_CASES=10
ACTUAL_CORRECT=10
VIRTUAL_PASS=10/10
VIRTUAL_ACCURACY=100%
VISIBLE_FIELDS=2
HUMAN_READABLE=PASS
MACHINE_PARSEABLE=PASS
PAGE_SEQUENCE_UNIQUE_WITHIN_FROZEN_PAGE_NAME=PASS
CORE_GATE_DUPLICATION=0
FOURTH_CORE_CREATED=NO
FOURTH_STEP_CREATED=NO
```

说明：100% 仅指上述 10 个冻结规则案例全部符合预期。

STOP
