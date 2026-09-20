# CORE② — MATURE SOLUTION CLUSTER

版本：0.2.0
日期：2026-09-21

目标不变：`min T_E2E subject to COMMERCIAL_GATE=PASS`。

## C — Compiler

采用 Node.js + TypeScript 普通确定性流程、JSON Schema、Ajv standalone build-time validator、dependency_ids 直接构图、speculative-policy compiler。
数学、日期、状态、掩码、依赖、hash 全留在代码。
不在 P0 热路径使用生成式 planner、Agent while-loop、运行时 schema compilation 或远程工作流编译服务。

## P — Probabilistic Kernel

固定 versioned model `jev-1.13.0`。
最终动作优先 Choice；同一 model barrier 最大 fan-out。
state/question 只携带该判断需要的信息，避免 context rot。
允许一个大 batch 或多个 concurrent shard；禁止把本可提前构造的问题拖到 receipt 后串行询问。

Transport 保留成熟现实候选：TypeSafe 官方 JS SDK；direct HTTP + Node/Undici；OpenRouter typesafe/jev-1.13。谁在当前机器最快必须 Step 3 同门槛实测，Virtual-99 不凭公开 latency 指定赢家。

## S — State Runtime

采用进程内 TypeScript finite-state reducer / transition table、immutable receipts、原生 Promise 并发、per-dependency unlock。
每个 dependent item 只等自己的 predecessor，不设置 17–20 全局 wait-all。
当前 P0 热路径不加入数据库、远程队列、Temporal 或 XState actor runtime。
XState v5 作为复杂动态状态任务的成熟扩展候选保留。

## V — Verifier

独立、T0 前预加载的 harness 持有 private oracle；Engine 不可读取。
Ajv standalone 校验结构；strict compare 校验动作/状态/receipt；Node crypto SHA-256 校验 manifest。
局部验证尽量与无关 action overlap；最终只保留一个 global commercial-gate barrier。
禁止 LLM 自评代替 reality verifier。

## 成熟证据

2026-09-21 检查：
- https://docs.typesafe.ai/concepts/how-to-build-with-system-one
- https://docs.typesafe.ai/patterns/fan-out
- https://docs.typesafe.ai/primitives
- https://docs.typesafe.ai/model-jaggedness/jev-1.13
- https://docs.typesafe.ai/models
- https://github.com/typesafe-ai/typesafe-sdk-js
- https://ajv.js.org/standalone.html
- https://stately.ai/docs
- https://undici.nodejs.org/
- https://openrouter.ai/typesafe/jev-1.13/

## Freeze

```text
C = TypeScript deterministic binder + Ajv standalone + speculative-policy compiler
P = pinned jev-1.13.0 + one serial model barrier + reality-tunable sharding
S = in-process finite-state reducer + immutable receipts + per-dependency unlock
V = independent preloaded harness + strict oracle compare + SHA-256
```
