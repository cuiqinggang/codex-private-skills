# PE-P0-GENERAL-01 TASK CONTRACT — v1.1 clarification

业务语义、24 项 fixture、hidden oracle、COMMERCIAL_GATE 与 T0/T1 均未改题。

## 固定依赖

01–20 读取输入后互相无现实依赖。
21–24 分别依赖 17–20 的真实动作结果。
动作集合固定为 EXECUTE / HOLD / ROUTE / REJECT。

## v1.1 对“依赖”的精确定义

21–24 的最终动作提交时间必须晚于对应真实 predecessor receipt。

允许在 receipt 出现前做 speculative policy compilation：对有限的可能 receipt 状态预先计算“若该状态发生，应采取什么动作”。这不是提前执行，也不是 oracle 泄露。

Verifier 必须检查：

`dependent_action_commit_time > predecessor_receipt_time`

而不是强制：

`dependent_model_query_time > predecessor_receipt_time`

后者不是业务要求，会制造伪串行。

## 状态转移

EXECUTE: SUCCESS→DONE；FAIL_TEMP→FAILED_RETRYABLE；FAIL_PERM→FAILED_FINAL。
HOLD→ON_HOLD。
ROUTE→ROUTED。
REJECT→REJECTED。
真实 action 必须产生不可变 receipt。

## COMMERCIAL_GATE

24/24 动作与最终状态必须匹配 hidden oracle；EXECUTE 必须读取真实 receipt；21–24 最终动作必须在自己的真实依赖 receipt 后提交；非法动作/转移/漏项/重复项为 0；独立 verifier 校验 private oracle、action log、最终状态与 manifest hashes；anti-cheat 必须 PASS。

任何一项失败，COMMERCIAL_GATE=FAIL，该次时间不参与最快比较。

## Anti-cheat

Engine 不得读取 private oracle / hidden executor outcomes；不得按 item_id 或 benchmark 名写死答案；T0 前不得读取当前输入或缓存本 benchmark 答案；不得把 hypothetical receipt 冒充真实 receipt；不得在真实 receipt 前提交 21–24 最终动作。
