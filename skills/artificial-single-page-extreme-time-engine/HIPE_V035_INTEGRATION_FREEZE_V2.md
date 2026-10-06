# HIPE v0.3.5 × 极限短时间引擎：集成冻结 第2版

状态：FROZEN_INTEGRATION_CONTRACT  
集成版本：第2版  
上游 HIPE：v0.3.5 FULLY_SEALED  
目的：把 HIPE 从“可选元决策层”升级为“全局递归编译层”，同时保持 JEV 仅按条件调用。

## 1. 上游冻结不变

```text
REPO=cuiqinggang/codex-private-skills
PATH=skills/hybrid-intelligence-probability-engine-v0-3-5/
FREEZE_COMMIT=c6fe2878fd237e7a8120b3af8e75f93e3cd6a4d9
FREEZE_ID=HIPE-v0.3.5-FULLY-SEALED-20261006-R1
STATE=FULLY_SEALED
```

本集成第2版不修改 HIPE v0.3.5 任一冻结字节。

## 2. 第2版核心：Recursive Compile

```text
TASK
→ Solvability Gate
→ Mature Solution Cluster
→ Forward Compiler
→ CODE / JEV / GPT residual
→ residual 产生新候选/事实
→ 再次 Forward Compiler
→ 直到无法继续降级
→ DAG / parallel
→ Freeze
→ Reality
→ verifier
```

因此 HIPE 不只在任务开头运行一次；它是贯穿虚拟成熟阶段的**递归编译器**。

## 3. 性能最大化不是最大化 JEV 调用数

```text
MAX_HIPE_VALUE
=
MAX_COMPILED_FAST_PATH
-
UNNECESSARY_MODEL_BARRIERS
```

优先级固定：
```text
CODE > JEV > GPT
```

如果一项判断能 0–数毫秒由 CODE 精确完成，调用 100–500ms 网络决策模型是性能倒退。

## 4. 最适合 JEV 的转换

将常规现实问题尽量转换成：

```text
STATE
+ finite OPTIONS
+ typed QUESTION
+ deterministic verifier
```

典型转换：
- “接下来怎么办？” → 候选路线 Choice；
- “这是哪类失败？” → Failure Class Choice；
- “是否值得继续？” → Noul / Score；
- “浏览器下一步点哪一个？” → Action Choice；
- “哪个工具最适合？” → Tool Choice；
- “哪个成熟方案优先？” → Route Choice。

## 5. 批量判断

同一 state 下的独立判断默认一个 Decisions API 请求：

```text
questions = {
  route,
  risk,
  next_action,
  stop_or_continue,
  ...
}
```

不要拆成多个网络往返，除非存在真实数据依赖。

## 6. Browser / Web

```text
CODE observe
→ CODE action table
→ JEV bounded choice（仅在需要时）
→ CODE execute
→ incremental observe
→ verifier
```

目标不是让 JEV “控制浏览器”，而是让它替代昂贵的开放式 LLM 决策屏障。

## 7. Douyin / 下载类任务的特殊结论

这类任务成熟度高。

最优路线通常应首先尝试：
1. 成熟直接 API / CLI / 已验证 downloader；
2. 成熟组件组合；
3. 必要时 browser fallback；
4. 最后才自己从零实现平台协议。

一旦成熟 route 已确定，生产 hot path 应尽量是 CODE / HTTP / ffmpeg / verifier。
JEV 的最大价值更多在：
- 路线选择；
- fallback 分类；
- 多候选媒体/工具的语义决策；
- 浏览器 fallback 的有限动作选择。

禁止为了“使用 JEV”而把确定性下载 hot path 人为模型化。

## 8. OpenRouter Jev 已验证接入合同

```text
ENDPOINT=https://openrouter.ai/api/alpha/decisions
MODEL=typesafe/jev-1.13
KEY_ENV=OPENROUTER_API_KEY
```

2026-10-06 本机实测：
- Windows User scope OPENROUTER_API_KEY=SET；
- 最小 Decisions API 请求成功；
- 返回模型：typesafe/jev-1.13-20260917；
- provider=TypeSafe；
- 测试 Noul=0.99；
- exit code=0。

密钥值不进入仓库、命令参数、日志或冻结记录。

## 9. 外部性能证据边界

公开 benchmark 支持：
- 浏览器决策密集型流程可出现约 4× 级端到端加速；
- 决策本身可比通用 LLM 快得更多；
- 但整体收益由“智能判断占关键路径比例”限制。

因此我们的目标不是宣告固定倍数，而是通过第8版结构尽量：
- 删除 GPT barrier；
- batch JEV；
- CODE 化；
- 并行化；
- 减少 Reality 数量。

## 10. 集成冻结

```text
HIPE_ROLE=RECURSIVE_GLOBAL_COMPILER
GATE_ROLE=REALITY_SOLVABILITY_CLASSIFIER
FORWARD_COMPILER_ROLE=NODE_ROUTER
CODE_ROLE=FIRST_PRIORITY
JEV_ROLE=BOUNDED_TYPED_DECISION
GPT_ROLE=IRREDUCIBLE_RESIDUAL
REALITY_ROLE=FROZEN_PLAN_CERTIFICATION
```

一句话：

**所有非平凡任务都先编译；不是所有任务都调用 JEV。**
