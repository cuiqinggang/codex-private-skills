# 混合智能概率引擎 v0.3.0 — 虚拟成熟冻结

## 结论

本版本完成的是“已认证任务族范围内”的完整虚拟成熟，不声称任意自然语言任务都能自动进入 JEV。

```text
版本=0.3.0
虚拟成熟=通过
现实认证=待执行
现实成熟=否

冻结任务族=HIPE-E2E-V3-48
未知任务族策略=直接全GPT，不强行混合
```

## 完整端到端时间边界

混合路径从同一原始任务开始，完整计入：

原始任务读取
→ 已认证任务族识别
→ 确定性正向拆解/编译
→ CODE / JEV / GPT residual
→ 合法并行
→ 确定性执行
→ 独立验证器
→ 结果落盘

旧 v0.1.x “预先标好路由后才开始计时”的做法已废止为历史原型，不再用于完整引擎收益认证。

## 最终虚拟冠军

方案 D：

**已认证任务族确定性编译 + CODE/JEV/GPT residual 并行混合执行**

虚拟校准快照：2026-09-24。

```text
全GPT虚拟端到端时间=16178.873 ms
混合引擎虚拟端到端时间=10673.287 ms

虚拟时间加速=1.515829 倍
虚拟时间下降=34.0295%

全GPT成本代理=0.039168 美元
混合成本代理=0.014926054 美元

虚拟成本收益=2.624136 倍
虚拟成本下降=61.8922%
```

以上时间/成本属于数字孪生虚拟目标，不是现实认证成绩。

## 数字孪生校准

GPT-5.6 Sol：
- 模型固定：openai/gpt-5.6-sol
- 路由：provider.sort=throughput
- 推理强度：low
- 严格 JSON Schema 输出
- 2026-09-24 OpenRouter OpenAI Fast 快照：P50 首 token 延迟约 3.70 s，吞吐约 71 tok/s
- 当前 Fast 路径价格快照：4 美元/M 输入，20 美元/M 输出

JEV：
- 模型固定：typesafe/jev-1.13
- 历史现实认证核心仍为 v0.4.0
- 历史现实最短锚点：560.9819 ms
- 输入价格快照：0.042 美元/M，输出 0

JEV 的 560.9819 ms 只作为已认证概率核心现实锚点，不属于本轮新增收益。

## 当前临界路径

```text
JEV历史现实锚点≈560.982 ms
GPT residual虚拟路径≈10671.831 ms
本地编译+验证+写入P50≈1.456 ms
```

因此当前固定 benchmark 的临界路径是 GPT residual，不是 JEV。

这意味着：
- 再把 JEV 从 560 ms 优化到更低，当前完整任务时间几乎不变；
- 真正下一数量级的优化方向是缩短 GPT residual 或扩大“有现实证据的确定性/JEV舒适区”，但不能以牺牲语义/商业门为代价。

## 正向拆解成熟结果

独立组件：

**JEV 舒适区导向正向拆解器 v0.1.0（JEV Comfort-Zone-Guided Forward Compiler v0.1.0）**

已经完成：

```text
形式规则空间=1024/1024 PASS
已认证任务族128边界案例=128/128 PASS
48节点回归路由=48/48 PASS
Schema攻击=192/192 PASS
SQL residual验证/失败注入=64/64 PASS
```

当前任务族固定路由：

```text
总节点=48
CODE=16
JEV=24
GPT residual=8
JEV Choice问题=32
```

JEV 语义合同严格复用 v0.4.0：
- request
- current_state
- evidence
- constraints
- allowed_actions
- dependency_ids
- EXECUTE/HOLD/ROUTE/REJECT Choice criteria

不得再次复用 v0.5.0 那种删语义字段的优化，因为该路线现实 0/30 已证明失败。

## 两级运行入口

### 已认证任务族

直接：

原始任务
→ 确定性正向编译
→ CODE/JEV/GPT residual
→ 并行
→ Verifier

不再先调用一次 GPT 做在线拆解。

### 未知任务族

直接：

原始任务
→ Full-GPT
→ Verifier

不为了提高 JEV 占比强制拆解。

新的任务族只有在“虚”阶段完成舒适区发现、攻击、验证和冻结后，才加入确定性编译器。

## 成熟方案竞争

A. 全 GPT：基线，虚拟约 16178.873 ms。

B. 在线 GPT 编译器 → Hybrid：淘汰。已认证任务族上增加一个串行高智能模型屏障；即使只按当前最低公开首 token 延迟估计，下界也高于方案 D。

C. JEV 先路由 → Hybrid：淘汰。增加串行 JEV 屏障，虚拟下界约 11234.269 ms，高于 D。

D. 已认证任务族确定性编译 → 并行 Hybrid：**虚拟冠军，10673.287 ms**。

E. Full-GPT 与 Hybrid 同时赛跑：时间下界不优于 D，但付费工作叠加，商业成本门失败，淘汰。

F. 未知任务族直接 Full-GPT：作为安全兜底保留，不与已认证任务族冠军竞争。

## 敏感性攻击

### 时间

25 组：
- 5 个字符/token 比例：3.0 / 3.5 / 4.0 / 4.5 / 5.0
- 5 个当前 GPT-5.6 Sol provider 性能画像

结果：

```text
最差虚拟加速=1.264183 倍
最好虚拟加速=1.605502 倍
最差时间下降=20.8975%
最好时间下降=37.7142%
25/25均为正收益
```

### 成本

20 组不同 token 比例 / provider 价格画像：

```text
最差成本收益=2.358612 倍
最好成本收益=2.635126 倍
最差成本下降=57.6022%
最好成本下降=62.0511%
20/20均为正收益
```

## 本地确定性实际测试

不是模拟口头判断，而是在当前 GPT 工作环境实际执行了本地 Python / SQLite：

- 编译/解析 P50：0.092257 ms
- 独立 verifier P50：1.297560 ms
- 结果写入 P50：0.066288 ms
- 本地固定开销 P50 合计：1.456105 ms
- 原始 benchmark：12061 bytes

这些是本地实际计时，不是 OpenRouter 现实模型计时。

## 虚拟成熟门

本版本在固定范围内满足：

- 正向拆解独立组件：PASS
- 形式舒适区穷举：PASS
- 已认证任务族边界：PASS
- GPT residual 不可被旧“简单正则拼接”代码路径偷做：PASS
- 独立 SQL verifier：PASS
- 成熟方案竞争：PASS
- 结构攻击/失败注入：PASS
- 数字孪生数值 T*：已建立
- 时间收益数值：已建立
- 成本收益数值：已建立
- 敏感性攻击：PASS
- Reality runner：冻结并完成无付费 selftest
- GUI Reality launcher：冻结并完成语法自测
- Reality 失败合同：冻结

因此在 `HIPE-E2E-V3-48` 已认证任务族范围：

```text
VIRTUAL_MATURITY=PASS
```

但：

```text
REALITY_CERTIFIED=NO
```

## Reality 才能证明的剩余变量

虚阶段不伪造：

- 真实 OPENROUTER_API_KEY 可用性；
- 真实 provider 路由；
- GPT-5.6 Sol 真实首 token / 生成吞吐；
- GPT residual 真实 30/30 有效性；
- JEV 真实本轮延迟；
- 真实 usage.cost；
- Full-GPT 与 Hybrid 同会话真实 A/B；
- 真实 T_REAL_STAR；
- 真实成本收益；
- 真实 RESULT_SHA256。

这些是下一步“实”的唯一剩余主要变量。
