# JEV Probability Engine P0 — v0.4.0 攻击：成熟方案融合

## 定位

- 母技能：`first-principles-physical-limit-convergence v3.1.7`
- 当前现实冠军：`jev-probability-engine-p0 v0.4.0`
- 当前现实 P0：`560.9819 ms`
- 当前现实门槛：`30/30 PASS`，`COMMERCIAL_GATE_SERIES=PASS`
- 本轮归属：`高智能虚拟成熟`
- Codex 权限：只允许最终现实验证，不允许设计、探索、改方案。

## 已成熟并直接复用的能力

### A. v0.4.0 现实已证明
- `typesafe/jev-1.13`
- 1 个 JEV decision wave
- 2 个并发 HTTP request
- 2 个 local execution wave
- 进程级单例 `SocketsHttpHandler`
- 进程级单例 `HttpClient`
- connection pooling / keep-alive
- 计时边界：T0 在正式 public input read 前；T1 在 Reality verifier 与 manifest 写盘后
- 现实认证：30/30 PASS，`T_P0=560.9819 ms`

### B. v3.1.6 已完成但未与 v0.4.0 C# 冠军完全合并的成熟结构
来自既有 `JEV-PROBABILITY-ENGINE-P0-PAYLOAD-PROOF-v1.json` 与 `FROZEN-RUNTIME-SPEC.md`：
- dependency-affinity semantic units
- runtime 2-way LPT byte balance
- per-shard projected state
- per-shard early release
- one append-only JSONL receipt log
- 1 final deterministic commercial gate
- 旧固定 fixture payload：`24482/24482 -> 7310/7310`
- 总 payload 与最大 shard payload 均减少 `70.141%`
- 12/12 failure injection PASS

## v0.4.0 现实实现中仍存在的可删除结构

认证 C# 实现当前仍：
1. 对两个 HTTP 请求复制完整 24-item state；
2. 仅按 question 顺序 round-robin 分 shard；
3. 等两个 HTTP request 都返回后，才开始所有本地动作；
4. 24 个 receipt 分别落盘并再次逐个读取。

这些不是商业语义要求，也不是物理必要屏障。

## 唯一融合候选

`JPE-P0-S2-PROJECTED-EARLY-RELEASE-V3`

固定：

```text
MODEL=typesafe/jev-1.13
MODEL_BARRIER_DEPTH=1
HTTP_REQUESTS_PER_RUN=2
HTTP_CONCURRENCY=2
ACTION_DEPENDENCY_DEPTH=2
FINAL_VERIFY_BARRIERS=1
QUESTION_COUNT=32
RESPONSE_CACHE=FORBIDDEN
TIMED_RETRY_COUNT=0
```

融合：
- 保留 v0.4.0 C# persistent transport；
- 使用已证明的 20 个 semantic unit；
- 17→21、18→22、19→23、20→24 四个 bundle 不可拆；
- T0 后按 public bytes 做 2-way LPT；
- 每 shard 仅携带自己引用 item 的 request/evidence/constraints；
- 两 shard 并发请求；
- 任一 shard 返回即执行该 shard 的 first-wave 与 dependent action，不等另一个 shard；
- receipt 使用单 append-only JSONL；
- 最后一次独立 deterministic verifier；
- T0/T1、oracle、benchmark、模型、商业门槛不变。

## 本轮明确不加入

- s1 单请求：旧现实 sweep 中 s2 已胜出；在没有新现实证据前不替代 s2。
- s4/s8：旧现实负证据。
- 第二轮 JEV：增加 model barrier。
- retry / hedge / majority vote / 多模型：增加关键路径或资源，且不解决当前 P0。
- TypeSafe direct API：缺少当前现实 credential，保留为未来独立候选。
- System.Text.Json source-generation / ResponseHeadersRead：成熟但预计属于次级本地微优化，不在本轮第一攻击中叠加，避免一次改变过多因素。

## 结论

本轮不是 Codex 探索任务。唯一候选已在 GPT 侧冻结；Codex 只负责之后按该候选做一次现实认证。
