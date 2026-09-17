# 随机系统的验证式交付（Stochastic Verified Delivery）

## 适用范围

用于生成模型、随机搜索、采样器、启发式算法、Monte Carlo 等“单次候选有随机性”的任务。

## 核心区分

```text
ATTEMPT != DELIVERY
```

ATTEMPT 是一次随机候选；DELIVERY 是最终允许交付的有效结果。

如果随机变量不是用户语义，而只是内部初始条件，则一次 attempt 失败不等于任务失败。

## 冻结前必须回答

```text
随机变量是否属于 TASK？
```

- 用户明确要求 exact seed / exact reproduction：属于 TASK，禁止自动换种；
- 用户只要求得到一个有效结果：seed 通常不属于交付语义，可作为内部随机变量。

## 推荐状态机

```text
DRAW_RANDOM_STATE
-> FAST_PROPOSAL
-> DETERMINISTIC_VERIFY
-> PASS: ACCEPT
-> FAIL: REJECT + DRAW_NEW_RANDOM_STATE
```

该循环必须由 GPT 在命令包中预授权，Codex 只执行。

## 时间指标

随机系统正式优化：

```text
T_TFVR = Time To First Valid Result
```

从任务首次提交到首个通过 verifier 并被 ACCEPT 的结果出现。

同时记录：

```text
FIRST_ATTEMPT_PASS_RATE
ATTEMPT_PASS_RATE
MEAN_ATTEMPTS_PER_TASK
ATTEMPTS_P50/P95/MAX
T_TFVR Mean/P50/P95/Max
INVALID_OUTPUTS_REJECTED
INVALID_OUTPUT_DELIVERED
```

## 质量定义

不要把：

```text
20/20 accepted outputs PASS
```

写成：

```text
future random process mathematically guaranteed to terminate 100%
```

有限认证能证明的是当前样本上的系统行为。

工程硬约束应写：

```text
INVALID_OUTPUT_DELIVERED = 0
```

即 verifier 失败的候选绝不交付。

## 概率解释

若每次 attempt 的成功率近似为 `p`，独立近似下平均尝试次数约为：

```text
E[N] = 1/p
```

连续 n 次失败概率约为：

```text
(1-p)^n
```

这些公式只用于 Virtual-99 粗算；真实冻结必须使用实测分布，不应默认独立同分布。

## 优先级原则

如果：

- 快路径单次成功率较高；
- verifier 可靠且便宜；
- 重采样成本小；
- 慢路径会让所有任务整体降速；

则优先比较：

```text
fast proposal + verify + resample
```

而不是：

```text
make every attempt slower to avoid rare failures
```

## 不适用

以下情况不能自动换随机状态：

- 用户要求 exact seed；
- 安全/金融/医疗等不能靠随机重试掩盖错误的任务；
- retry 改变了用户语义；
- verifier 无法可靠判断结果有效性；
- 失败具有系统性而不是随机性。

## H3-P0 真实例

```text
20 delivery tasks
22 attempts
first-attempt pass 90%
mean attempts 1.10
T_TFVR mean 6.804s
P50 6.076s
P95 11.974s
max 12.862s
accepted QC 20/20
invalid delivered 0
```

该案例证明：单次 attempt 不必 100% 成功，系统仍可在严格质量门禁下实现高成功交付与低平均完成时间。