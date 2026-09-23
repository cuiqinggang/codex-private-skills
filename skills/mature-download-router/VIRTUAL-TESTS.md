# v0.1.2 Virtual Tests

## 结论先行

v0.1.1 的“路由逻辑 PASS”是真的，但把它标成完整 VIRTUAL_MATURE=PASS 过早，因为没有把 Reality Foundation 已知的本机网络出口加入调用合同。

v0.1.2 只补这一条，不增加下载器逻辑。

## Cases

| Case | 条件 | 冻结行为 | 结果 |
|---|---|---|---|
| V01 | HF public file + network context available | hf + inherited process proxy | PASS |
| V02 | Direct HTTPS + network context available | aria2c + inherited/explicit proxy | PASS |
| V03 | HF + Direct URL mixed | hf + aria2c; no custom queue | PASS |
| V04 | route correct but network context omitted | BLOCK before freeze | PASS |
| V05 | existing verified proxy endpoint currently reachable | use it process-locally; no persistent change | PASS |
| V06 | existing endpoint unavailable | STOP with minimal Reality Delta | PASS |
| V07 | gh missing | GitHub asset URL -> aria2c | PASS |
| V08 | scoped workdir | PROCESS_SPAWN path preserved | PASS |

## Attack checks

```text
ROUTE_AMBIGUITY=0
CUSTOM_DOWNLOADER=0
CUSTOM_ADAPTER=0
CUSTOM_QUEUE=0
CUSTOM_STATUS_UI=0
JEV_REQUIRED=0
NETWORK_CONTEXT_OMISSION_ALLOWED=0
PERSISTENT_PROXY_MUTATION=0
```

## Reality consistency

Known real evidence included in the twin:

```text
REAL_01:
  explicit existing proxy -> HF official/mirror reachable

REAL_04:
  WORKDIR scoped -> PROCESS_SPAWN=PASS
  aria2c=1.37.0
  hf=1.19.0
  gh=2.92.0
  route match=2/2
  both download tools failed at network stage with connection refused
```

Therefore the virtual correction is:

```text
source classification
-> inherit current verified network context
-> mature tool
```

not:

```text
source classification
-> mature tool
```

## Freeze

```text
ROUTE_LOGIC=PASS
NETWORK_CONTEXT_CLOSED=PASS
LOCAL_REALITY_INPUT_SUFFICIENT=PASS
SINGLE_TASK_ROUTING=PASS
MULTI_TASK_ROUTING=PASS
NO_REDUNDANT_LAYER=PASS
VIRTUAL_MATURE=PASS
REAL_CERTIFIED=NO
NUMERIC_T_VALID=REAL_TEST_REQUIRED
```
