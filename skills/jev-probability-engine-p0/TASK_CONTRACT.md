# PE-P0-GENERAL-01 TASK CONTRACT

## 目的

测整台 Probability Engine，而不是测一个 Jev 分类调用。

固定执行链：
输入 → 编译/状态构造 → 第一层并行概率判断 → 第一批真实动作/回执 → 第二层依赖判断 → 第二批动作 → Reality Verify → DONE

## 固定规模

总项目：24。
第一层：20 项，01–20，读取输入后互相无依赖。
第二层：4 项，21–24，分别依赖 17–20 的真实动作回执。

动作集合：
EXECUTE
HOLD
ROUTE
REJECT

每项最少输入字段：
item_id
request
current_state
evidence[]
constraints[]
allowed_actions[]
dependency_ids[]

第二层在第一批动作完成后新增 dependency_receipts[]。

## 状态转移

初始均为 PENDING。

EXECUTE：通过动作执行器；SUCCESS → DONE；FAIL_TEMP → FAILED_RETRYABLE；FAIL_PERM → FAILED_FINAL。
HOLD → ON_HOLD。
ROUTE → ROUTED。
REJECT → REJECTED。

每个动作必须产生不可变 receipt。

## 商业门槛

只有以下全部满足才 PASS：
24/24 有且只有一个最终动作；
动作与隐藏 oracle 一致；
最终状态与隐藏 oracle 一致；
EXECUTE 项读取真实 receipt；
21–24 的最终决策发生在依赖 receipt 之后；
非法动作、非法转移、漏项、重复项均为 0；
最终 verifier 读取独立 oracle、动作日志和最终状态；
最终 manifest 的输入/输出/动作日志/verifier 结果 hash 一致；
反作弊规则通过。

任何一项失败，COMMERCIAL_GATE=FAIL，该次时间不参与最快比较。

## 基准完整性

Engine 不得读取 private oracle 或隐藏动作结果。
不得按 item_id 或 benchmark 名称写死答案。
T0 前不得读取当前 24 项、构造本次 DAG 或缓存本 benchmark 的 Jev 答案。
允许预加载通用 Runtime、通用 Compiler 规则、通用状态机、Jev client、认证与连接池。