# 第一性原理物理极限收敛引擎 v2.0.0

正式技能：`first-principles-physical-limit-convergence`

核心仍然只有四步：

```text
1. 物理极限
2. 本机现实最优区间
3. GPT Virtual-99
4. Codex 完整实测命令包
```

v2.0 新增两项横向能力，不增加主流程层级：

- **随机系统的验证式交付**：区分 attempt 与 delivery，优化 `T_TFVR = Time To First Valid Result`，用严格 verifier 拒绝坏候选并按冻结规则重采样；
- **GPT-Codex 自动控制面**：GitHub 共同事实源 + ChatGPT 浏览器桥接 + Codex 确定性执行 + checkpoint/idempotency + capacity router，去除人工复制粘贴。

关键原则：

```text
NO_FREE_EXPLORATION=YES
CODEX_ROLE=DETERMINISTIC_EXECUTOR
GPT_ROLE=PLANNER/JUDGE
```

随机系统中：

```text
single attempt failure != delivery failure
```

如果随机变量不是用户任务语义，可采用：

```text
fast proposal -> QC -> reject invalid -> resample -> first valid result
```

正式时间指标：

```text
T_TFVR
```

H3-P0 实证：20 个交付任务最终 20/20 QC PASS；首次成功率 90%；平均 1.10 次尝试；T_TFVR P50 6.076s、P95 11.974s；无效输出交付 0。

详细规则：

- `SKILL.md`
- `references/STOCHASTIC-VERIFIED-DELIVERY.md`
- `references/AUTOMATED-GPT-CODEX-CONTROL-PLANE.md`

正式分支：

`codex/first-principles-physical-limit-convergence-v2.0.0`
