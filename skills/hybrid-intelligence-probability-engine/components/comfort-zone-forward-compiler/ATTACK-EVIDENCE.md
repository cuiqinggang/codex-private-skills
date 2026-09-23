# 正向拆解器攻击验证证据

## 1. 形式规则穷举

10 个布尔硬门全部组合：

```text
TOTAL=1024
PASS=1024
FAIL=0
```

## 2. JEV 舒适区单条件破坏攻击

从 32 个标准 JEV 案例出发，分别破坏以下 8 个关键条件：

1. 语义保持；
2. 状态可显式化；
3. 动作空间有限；
4. 动作本体已认证；
5. 有确定性 verifier；
6. 不需要开放生成；
7. 不依赖隐藏信息；
8. 不需要 timed retry。

共：

```text
32 × 8 = 256 attacks
SAFE_FALLBACK_TO_GPT=256/256
UNSAFE_JEV_OVERRROUTE=0
```

## 3. 历史 48 节点回归

```text
CODE=16
JEV=24
GPT=8
PASS=48/48
```

## 4. 本地确定性路由门耗时

在当前 GPT 页面本地 Python 环境，对 48 节点路由门重复 5000 次：

```text
MIN_MS=0.004517
P50_MS=0.004867
P95_MS=0.005158
MAX_MS=0.314124
```

该数据只证明确定性路由门本身极轻，不代表完整语义编译器耗时。

## 5. 128 案例 GPT 页面语义审查

本页对 128 个公开自然语言任务与隐藏构造 oracle 进行了同模型语义复核：

```text
SEMANTIC_CASES=128
CODE=32
JEV=32
GPT=64
GPT_PAGE_ROUTE_REVIEW=128/128
UNSAFE_JEV_OVERRROUTE=0
MISSED_CERTIFIED_JEV=0
```

限制：
这是 GPT 页面同模型虚拟审查，不是独立 API 重复试验，也不是 Reality Certification。
因此它可以进入 Virtual-99 证据，但不能替代现实 compiler 认证。
