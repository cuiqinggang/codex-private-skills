# 混合智能概率引擎 P0 v0.1.1 — Virtual Freeze

## 定位

- 母方法：整体闭环极限短时间引擎 v4.6
- 概率核心：JEV Probability Engine P0 v0.4.0
- Reality benchmark：保持 v0.1.0 的固定 48 节点，不改变 benchmark 语义
- 模型：GPT = openai/gpt-5.6-sol；JEV = typesafe/jev-1.13
- 网关：OpenRouter
- 唯一优化目标：COMMERCIAL_GATE=PASS 前提下 min T_VALID

本版本由 v0.1.0 Reality Delta 触发：
REAL_VALID=NOT_TESTED
REALITY_DELTA=FROZEN_RUNNER_DENIED_BY_AUTO_REVIEW_CREDENTIAL_AND_PAID_NETWORK_ACTION

该 Delta 不属于算法/性能失败；它证明凭据化、可能计费的外部网络调用不能继续放在 Codex 自动审查执行边界内。

## v0.1.1 核心修正

1. 虚/实职责继续严格分离。
2. Codex 不再承担任何 OPENROUTER_API_KEY 或付费 OpenRouter 请求。
3. Reality 的凭据化网络执行移动到用户明确确认的本地一键 GUI launcher。
4. GUI 只在单次运行内把 OPENROUTER_API_KEY 传给冻结 child runner；不写入磁盘、不打印。
5. 人工确认和密钥输入发生在 Reality 计时开始之前，不污染 T_VALID / outer process timing。
6. v0.1.0 的 48 节点 benchmark、模型、endpoint、价格常量、路由、runs=10、Verifier 不因本次 Delta 改变。
7. 现实 runner 新增：
   - 已知 HTTP / auth / payment / rate-limit / network / timeout / response-schema 的 Reality Delta 分类；
   - CRITICAL_UNCAUGHT_ERROR；
   - 原生 S_E2E_COST；
   - 失败也尽量写最小证据 JSON。
8. 不允许 Reality 现场修复、换模型、换 provider、换 benchmark 或二次设计。

## 四字段标签

统一：
【页面/项目名｜具体任务名｜步骤/序号｜虚/实】

本版本虚阶段：
【混合智能概率引擎｜v0.1.1虚拟成熟与冻结｜2｜虚】

Reality：
【混合智能概率引擎｜冻结方案现实验证｜3｜实】

第四字段不再使用“三核心名称”。

## 固定 runtime

TASK
→ Comfort-Zone-Guided Forward Compiler
→ CODE / evidence-bounded JEV Choice / GPT residual
→ independent legal parallelism
→ deterministic executor
→ independent verifier
→ COMMERCIAL GATE
→ T_VALID

JEV production comfort zone 继续限制为：
explicit state + finite Choice + fixed action ontology + deterministic verifier + zero timed retry。

## Reality benchmark

TOTAL=48
- deterministic=16
- JEV Choice=24
- GPT regex-synthesis residual=8

Choice ontology:
EXECUTE / HOLD / ROUTE / REJECT

Hybrid:
16 CODE + 24 JEV (2 shards) + 8 GPT residual

JEV 两 shard 与 GPT residual 在无依赖条件下并行。

## GPT-side prevalidation gate

冻结前必须尽量把 Reality 以外能验证的内容全部验证：

- source/static contract
- benchmark cardinality and oracle
- deterministic 16-node logic
- 24 JEV Choice semantic oracle
- 8 GPT regex tasks against deterministic verifier
- JSON / response parsing assumptions
- public model IDs
- public endpoint contract
- public pricing snapshot
- missing-auth failure
- local structural selftest
- outer timing boundary
- secret non-persistence rule
- failure taxonomy

这些 PASS 只提高 Reality 成功概率，不代替真实 API inference、真实费用或真实 T_VALID。

## Commercial gate

FULL_GPT_VALID=PASS
HYBRID_VALID=PASS
CRITICAL_UNCAUGHT_ERROR=0
NORMALIZED_COST_HYBRID <= NORMALIZED_COST_FULL_GPT
min(T_HYBRID) < min(T_FULL_GPT)

全部成立才允许 REAL_VALID=PASS。

## Remaining reality-only variables

虚阶段无法伪造：
- 用户授权后的真实 OPENROUTER_API_KEY 可用性；
- OpenRouter 真实网络路径；
- GPT-5.6 Sol 的真实返回与 token usage；
- Jev 1.13 的真实 Choice 返回与 usage.cost；
- 10 measured runs 的真实稳定性；
- 真实 Full-GPT / Hybrid cost；
- 真实 T_VALID；
- 真实 result SHA256。

因此：
VIRTUAL_MATURITY=PASS
REALITY_CERTIFICATION=PENDING

v0.1.0 历史永久保留，不覆盖。
