# v0.1.1 Virtual Tests

## Goal

验证最短路由，不测试成熟下载器内部算法。

| Case | Input | Expected | Result |
|---|---|---|---|
| V01 | HF public single file | hf | PASS |
| V02 | HF multiple files | one hf invocation / native batch | PASS |
| V03 | GitHub Release + gh available | gh | PASS |
| V04 | GitHub Release + gh unavailable + asset URL available | aria2 | PASS |
| V05 | direct HTTPS | aria2 | PASS |
| V06 | browser-session-only | Playwright | PASS |
| V07 | mixed HF + direct URL | hf + aria2; no custom queue | PASS |
| V08 | workspace-write launched from user Home and returns 1344 | restart reality task from task-scoped narrow workdir; do not classify tool missing | PASS |
| V08b | scoped workdir still returns 1344 | retry once on pre-existing authorized proven execution channel; otherwise STOP | PASS |
| V09 | aria2 missing | bootstrap task required; router does not invent downloader | PASS |
| V10 | hf missing | bootstrap task required; router does not invent downloader | PASS |

## Attack

```text
AMBIGUOUS_ROUTE=0
CUSTOM_DOWNLOADER=0
CUSTOM_ADAPTER=0
CUSTOM_QUEUE=0
CUSTOM_STATUS_UI=0
JEV_REQUIRED=0
GH_HARD_DEPENDENCY=0
SPAWN_1344_MISCLASSIFIED_AS_TOOL_MISSING=0
```

## Time

```text
v0.1.0:
executor-entry failure could stop before tool verification

v0.1.1:
executor-entry classified first
-> source classification
-> mature tool
```

不伪造毫秒值：

```text
NUMERIC_T_VALID=REAL_TEST_REQUIRED
```

## Freeze

```text
RULE_SET_CLOSED=PASS
LOCAL_REALITY_INPUT_SUFFICIENT=PASS
TOOL_BOOTSTRAP_INFO_SUFFICIENT=PASS
SINGLE_TASK_ROUTING=PASS
MULTI_TASK_ROUTING=PASS
EXECUTOR_1344_CLASSIFICATION=PASS
NO_REDUNDANT_LAYER=PASS
VIRTUAL_MATURE=PASS
REAL_CERTIFIED=NO
```
