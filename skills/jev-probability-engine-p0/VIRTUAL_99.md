# CORE② — VIRTUAL-99 STRUCTURAL FREEZE

版本：0.2.0
日期：2026-09-21

## 关键发现

v0.1.0 的旧链路：
`P1 → A1/receipt → P2 → A2`

把“现实动作依赖”错误等同于“概率模型必须等 receipt 后再询问”。

TypeSafe 官方规则：只有第二请求在第一个答案前根本无法构造时，第二轮才是真依赖；否则应 speculative fan-out。

21–24 必须等待真实 receipt 才能提交最终动作，但它们的 receipt-status→action 语义可以对有限结果空间提前求值。

## Speculative policy compilation

17–20 EXECUTE 的真实 executor result 空间：
SUCCESS / FAIL_TEMP / FAIL_PERM。

21–24 每项提前形成三个直接条件 Choice，共 12 个 conditional-policy questions。
加上 01–20 的 20 个当前动作 Choice，Virtual-99 单大 batch 候选共 32 个问题；也允许同 barrier 并发分片。

receipt 返回后只做 O(1) deterministic lookup，再提交真实 dependent action。

## 深度

```text
MODEL_BARRIER_DEPTH_MIN=1
ACTION_DEPENDENCY_DEPTH_MIN=2
FINAL_VERIFY_BARRIERS_MIN=1
```

## 已删除的非必要结构

- 生成式 planner 重解释固定 structured task。
- runtime schema compilation。
- 每 item 串行 Jev。
- receipt 后固定第二轮 Jev。
- 17–20 全部完成才释放 21–24 的 global wait-all。
- 对数学、日期、allowed-action mask、状态转移、hash 使用 Jev。
- 无条件 majority vote / prompt 改写重采样。
- XState/Temporal/数据库/远程队列强行进入当前 P0 热路径。
- 中间反复落盘再读。
- LLM verifier 自评。
- 多个全局 verifier barriers。

## 尚须现实验证

- TypeSafe direct vs OpenRouter。
- 官方 SDK vs direct HTTP/Undici。
- 单 32-question batch vs concurrent shards。
- conditional-policy 对 Jev 1.13 的实际商业门槛通过率。
- 当前机器/网络/TLS/connection reuse。
- action executor 与 verifier 实际时间。

```text
MATURE_CLUSTER=FROZEN_V0.2
VIRTUAL_99_STRUCTURAL=PASS
MODEL_BARRIER_DEPTH_MIN=1
ACTION_DEPENDENCY_DEPTH_MIN=2
T_PHY_V2_FORMULA=DERIVED
T_REAL_STAR=NOT_MEASURED
T_P0=NOT_MEASURED
REAL_CERTIFIED=NO
```

现实若证明 speculative route 无法过同一 COMMERCIAL_GATE，不降低门槛；保留本版证据，标失败并产生新版本回退。
