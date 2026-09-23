# 混合智能概率引擎 v0.3.1 — 现实认证合同

## 标签

【混合智能概率引擎｜完整任务现实认证｜3｜实】

## 现实只做认证

禁止在 Reality：
- 改模型；
- 改 benchmark；
- 改正向编译器；
- 改 JEV 语义；
- 改 verifier；
- 改 provider 策略；
- 失败后现场修复；
- 为追求更快而重新设计。

失败：
Reality Delta → STOP → 返回 GPT 的“虚”。

## 同任务 A/B

Full-GPT 与 Hybrid：
- 同一个原始任务族；
- 同一个 variant；
- 同一个最终 verifier；
- 同一会话/同一时间窗口；
- 测量顺序按 variant 奇偶交替 A→B / B→A，降低 provider 时间漂移。

## 次数

- 3 组 warmup pair，不进入 measured arrays；
- 30 组 measured pair；
- 无 timed retry；
- 任一有效性/成本硬门失败，停止。

## Full-GPT

原始任务
→ GPT-5.6 Sol
→ 严格 JSON Schema
→ 独立 verifier
→ 结果写入

## Hybrid

原始任务
→ 冻结确定性正向编译
→ 16 CODE
→ 24 JEV（32 Choice questions / 2 shards）
→ 8 GPT SQL residual
→ JEV 两 shard 与 GPT residual 并行
→ 独立 verifier
→ 结果写入

## 模型

GPT：
- openai/gpt-5.6-sol
- reasoning effort=low
- provider.sort=throughput
- provider.require_parameters=true
- strict JSON Schema

JEV：
- typesafe/jev-1.13
- OpenRouter Decisions API
- v0.4.0 认证语义合同

## Reality 必须回传

- Full-GPT 30/30 有效性
- Hybrid 30/30 有效性
- critical uncaught error
- T_FULL_GPT min / P50 / P95
- T_HYBRID min / P50 / P95
- 实际 usage.cost
- S_E2E_TIME
- S_E2E_COST
- 每次 model/provider/generation id
- JEV 两 shard / GPT residual component timings
- 最终 result SHA256
- 外层进程总时间

## 晋级门

必须全部满足：

1. Full-GPT 全部 measured 有效；
2. Hybrid 全部 measured 有效；
3. critical uncaught error = 0；
4. 每个 measured pair 的 Hybrid 实际成本 <= Full-GPT；
5. min(T_HYBRID) < min(T_FULL_GPT)。

只有这些全部 PASS，才允许把 v0.3.1 从“虚拟成熟”晋级为现实认证版本。

## 凭据边界

Codex 不读取、不寻找、不打印 OPENROUTER_API_KEY，也不替用户发起凭据化付费请求。

Reality 由冻结 GUI launcher 在用户明确确认后：
- 单次读取 inherited env 或 masked input；
- 不落盘密钥；
- 确认后才开始外层 Reality 计时；
- 执行冻结 runner；
- 输出 SHA256；
- STOP。
