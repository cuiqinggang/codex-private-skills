# JEV Probability Engine P0 — 广域成熟方案池 v1

归属：first-principles-physical-limit-convergence v3.1.6
日期：2026-09-21
现实基线：T_P0=840.6046999999962 ms；COMMERCIAL_GATE=PASS；30/30。

## 唯一目标
min T_VALID subject to COMMERCIAL_GATE=PASS。质量、安全、正确性、成本、资源与反作弊只定义 VALID，不成为第二优化目标。

## KEEP / FROZEN
- Jev 1.13 Choice；当前同任务 30/30 现实通过。
- speculative fan-out：21–24 的 SUCCESS/FAIL_TEMP/FAIL_PERM 策略提前求值，MODEL_BARRIER_DEPTH=1。
- 32 个原子 Choice；确定性规则继续留在 code。
- state projection：每 shard 只携带真正被该 shard 引用的 request/evidence/constraints。
- short questions + state-path criteria。
- 固定 2 shards：当前唯一同环境现实最快拓扑证据。
- dependency-affinity semantic units + T0 后通用 LPT byte-balance。
- per-shard early release：任何 shard 返回即开始自己的动作，禁止全局 model join。
- predecessor receipt → O(1) precomputed-policy lookup → dependent action。
- 两条预热 persistent connections。
- Undici Pool/request，connections=2，pipelining=1。
- build-time standalone schema validation。
- in-memory immutable reducer + single append-only JSONL receipt log。
- incremental deterministic verifier + exactly one final global commercial gate。
- timed fast path retry=0；失败只返回 GPT。

## REJECT / RESERVE
- response cache：REJECT，benchmark 反作弊禁止答案缓存。
- 4/8 shards：REJECT，已有现实负证据且增加 request/duplicate-state/straggler。
- 1 shard：REJECT CURRENT；成熟但没有新证据推翻现实 s2 胜出。
- receipt 后第二轮 Jev：REJECT，增加 model barrier。
- prompt 改写/majority vote：REJECT，30/30 已过门槛且增加调用。
- XState/Temporal/DB/remote queue：REJECT P0，增加热路径。
- Rust/Go rewrite：REJECT CURRENT，本地开销不是 840 ms 主瓶颈。
- immediate full duplicate hedge：REJECT fast path；不改变单请求物理下界并放大资源。
- p95 delayed hedge：RESERVE reliability only，不进入 min-T fast path。
- OpenRouter response/provider routing：REJECT CURRENT；当前 Jev 1.13 只有 TypeSafe provider。
- TypeSafe direct API：FUTURE CANDIDATE；当前现实边界没有 TypeSafe key，不能进入唯一冻结方案。
- 64-option conditional-policy Choice：REJECT；增加选项/indirection，与原子问题成熟规则冲突。
- LLM verifier：REJECT；Reality Verifier 必须确定性独立。

## 成熟来源（2026-09-21）
- https://docs.typesafe.ai/concepts/how-to-build-with-system-one
- https://docs.typesafe.ai/patterns/fan-out
- https://docs.typesafe.ai/model-jaggedness/jev-1.13
- https://docs.typesafe.ai/models
- https://docs.typesafe.ai/primitives/choice
- https://openrouter.ai/typesafe/jev-1.13/
- https://undici.nodejs.org/
- https://ajv.js.org/standalone.html
- https://research.google/pubs/the-tail-at-scale/
