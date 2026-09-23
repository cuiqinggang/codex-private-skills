# 历史 48 节点执行层收益审计

本文件只审计旧 v0.1.x “已经预先完成路由后的执行平面”，不得作为 v0.2.0 完整端到端收益。

## 路由结构

```text
TOTAL_NODES=48
CODE=16
JEV=24
GPT_RESIDUAL=8
```

结构上：
- 不再直接交给 GPT 的节点 = 40/48 = 83.3333%
- GPT-routed 节点数 = 8/48 = 16.6667%
- 节点数量层面的 GPT route shrink = 6x

这不是时间加速倍数。

## 请求体静态字节审计

按旧 v0.1.1 runner 的精确 JSON 序列化方式：

```text
FULL_GPT_REQUEST_BYTES=17722
HYBRID_GPT_REQUEST_BYTES=1489
JEV_SHARD_1_REQUEST_BYTES=8252
JEV_SHARD_2_REQUEST_BYTES=8396
HYBRID_TOTAL_REQUEST_BYTES=18137
```

得到：

- GPT 请求体字节减少 = 91.5980%
- Hybrid 全部模型请求体字节总和相对 Full-GPT = +2.3417%

因此旧结构的真正收益不是“网络字节更少”，而是把大量高价/高延迟 GPT 语义工作移动到 CODE/JEV，并让 JEV/GPT residual 合法并行。

## GPT 预期输出静态字节审计

按隐藏 oracle 的最短合法 JSON 表达：

```text
FULL_GPT_EXPECTED_OUTPUT_BYTES=790
HYBRID_GPT_EXPECTED_OUTPUT_BYTES=230
```

GPT 输出负载静态字节减少约：
70.8861%

## 输入成本的字节权重代理

仅用静态 request bytes 乘冻结挂牌 input price：
- GPT = 2.00 美元 / 1M input tokens
- JEV = 0.042 美元 / 1M input tokens

得到 input-only byte-weighted proxy：
```text
FULL_GPT / HYBRID ≈ 9.6388x
```

重要：
这不是实际 token 账单，也没有加入 GPT 输出 token 成本，因此只能作为虚拟结构成本代理，禁止写成现实成本收益。

## 当前不能给出的数字

由于旧 runner 没有计入“原始任务 → 正向拆解/编译”的时间：

```text
COMPLETE_TASK_T_VIRTUAL_STAR=NOT_ESTABLISHED
COMPLETE_TASK_T_REAL_STAR=NOT_MEASURED
COMPLETE_TASK_TIME_SPEEDUP=NOT_CERTIFIED
COMPLETE_TASK_COST_SPEEDUP=NOT_CERTIFIED
```

JEV v0.4.0 的 560.9819 ms 是历史概率核心现实锚点，不是本轮新增收益。
