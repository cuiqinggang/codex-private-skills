# H3-P0 第一性原理极限收敛：完整方法复盘 v1

## 1. 目的

这份复盘不再记录单个参数或某次跑分，而是回答：

> H3-P0 从“慢、复杂、反复试错”走到“质量稳定、时间收敛、最终冻结”的过程中，哪些方法应该永久写进通用技能包，哪些只属于视频生成案例。

## 2. 最终结果

最终主路径：

```text
MiniMax H3 / Star7 / INT8+ConvRot / 1 step
-> deterministic QC
-> FAIL: reject invalid output
-> draw a new OS-random seed
-> rerun same fast path
-> accept first QC PASS
```

20 个正式独立交付任务：

```text
FINAL_ACCEPTED_QC=20/20
FIRST_ATTEMPT_PASS_RATE=90%
MEAN_ATTEMPTS_PER_TASK=1.10
DELIVERY_TOTAL_MEAN=6.804s
DELIVERY_TOTAL_P50=6.076s
DELIVERY_TOTAL_P95=11.974s
DELIVERY_TOTAL_MAX=12.862s
INVALID_OUTPUT_DELIVERED=0
```

## 3. 真正有效的方法论

### 3.1 物理极限与现实区间必须分开

物理极限是终极参照；现实最优区间是本机在当前成熟方法下可以逼近的目标带。不能因为当前实现慢，就把物理极限抬高；也不能因为理论很快，就否定现实软件/驻留/精度约束。

### 3.2 成熟方案先于自由探索

H3-P0 早期 V1-V11 证明：让执行器不断 profile、改变参数、安装候选、再根据结果继续发明下一轮，成本高、路径长、信息增益低。

真正的大幅收益来自成熟 Star7 路线的复制与验证，而不是继续微调旧路径。

### 3.3 GPT 循环，Codex 不循环

有效结构：

```text
GPT: 物理分析 + 外部成熟方案 + Virtual-99
-> 冻结命令包
-> Codex: 确定性执行
-> 证据回远端
-> GPT: 只在命令包外异常时重新裁决
```

执行器只能灵活决定“如何完成同一个已授权动作”，不能决定“下一步研究什么”。

### 3.4 失败要分层，不要一律当方案失败

H3-P0 至少出现过这些不同层级：

```text
Windows executor failure
Codex remote model capacity
source identity mismatch
single-seed content QC failure
Star7-specific precision quality failure
same-seed reference quality failure
system delivery failure
```

它们不能用同一种处理方式。

原则：

```text
先判失败属于控制面、执行面、随机样本、算法、质量还是系统交付层
再决定是否返回 GPT、重试、换种、回滚或冻结
```

### 3.5 随机系统必须优化“交付”，不是强迫每次 proposal 都成功

这是本案例最重要的新结论。

对于本质随机的生成系统：

```text
proposal attempt != user delivery
```

如果 seed 不是用户任务语义，而只是随机初始条件，则不应要求每一个 seed 都一次成功。

正确系统：

```text
fast stochastic proposal
-> deterministic verifier
-> invalid proposal rejected
-> resample
-> first valid result delivered
```

因此正式时间指标应使用：

```text
T_TFVR = Time To First Valid Result
```

而不是只看某个固定 seed 的单次 runtime。

### 3.6 “100%质量”要定义在 accepted output 层

有限测试不能证明未来随机过程数学上绝对不会持续失败。

工程上可以严格保证：

```text
INVALID_OUTPUT_DELIVERED=0
```

即：任何 QC FAIL 都不允许交付。

H3-P0 最终正式认证 20/20 accepted outputs 全部 PASS，但 first-attempt pass rate 为 90%。这不是矛盾，而是两层不同指标。

### 3.7 概率策略要用真实分布，而不是凭感觉

恢复证明阶段：两个已知坏起点均在一次新随机 seed 后恢复。

最终 20-task 阶段：

```text
18 task first-attempt PASS
2 task need second attempt
mean attempts=1.10
```

所以本项目不再需要假设“失败率约10%”；真实认证已经给出当前 task/hardware/runtime 下的经验分布。

长期生产仍要监测 drift。

### 3.8 快速兜底优先于全局降速

如果失败只占少数任务，则不应该为了少量失败把 100% task 都切到慢路径。

H3-P0 中：

- 原始 Loader fallback 对 920108 也 FAIL；
- 且 fallback 链路耗时 90-100s 级；
- reseed 的成功 attempt 可回到约 5-8s 级。

所以正确策略是只让失败样本支付额外一次快路径成本。

### 3.9 不能把局部数值差异误判成因果根因

两轮定向诊断证明：误差拓扑更符合 `DISTRIBUTED_ACCUMULATION`，没有找到单一持续致病算子。

ACT32 真实测试保持 INT8/ConvRot、甚至让 930103 更快，但质量仍 FAIL。

结论：

> 找到“差异”不等于找到“可修复因果点”。

虚拟方案必须通过真实 A/B 才能升级为成熟方案。

### 3.10 控制面可靠性必须独立建设

H3 优化过程中还暴露：

- Windows `TokenDefaultDacl` 1344；
- Codex 模型 capacity；
- 会话/模型切换；
- 手工复制 GPT/Codex 结果。

这些不属于 H3 数学算法，但会破坏长流程效率。

因此控制面必须独立包含：

```text
checkpoint/resume
capacity-aware model routing
remote shared truth workspace
browser transport
idempotent execution
DO_NOT_REPEAT ledger
```

## 4. 被否定的工作方式

### 4.1 Codex 自由探索

否定原因：分支太多、状态难控、重复测试、成本高。

### 4.2 每个小测试后回 GPT 重新规划

否定原因：人为把一次 Virtual-99 可解决的问题变成真实执行循环。

### 4.3 强迫每个随机 seed 单次 100% PASS

否定原因：把随机 proposal 与最终 delivery 混为一谈，导致不必要的精度修复和慢路径兜底。

### 4.4 看到质量失败就全量切慢 Loader

否定原因：慢、且不能保证 same-seed reference 必然成功。

### 4.5 看到数值差异就修改对应层

否定原因：差异可能是无害路径差异，必须证明 failure-specific、持续、方向一致的因果链。

## 5. 通用技能应该吸收什么

写入 `first-principles-physical-limit-convergence`：

1. 随机系统的 attempt/delivery 双层合同；
2. `T_TFVR` 作为随机任务的正式时间指标；
3. deterministic verifier + stochastic resampling 模式；
4. accepted quality 100% 与 first-attempt success rate 分离；
5. 条件循环可以预授权，不等于 Codex 自由探索；
6. 控制面错误与业务失败分层；
7. GitHub 远端共同事实源；
8. checkpoint + DO_NOT_REPEAT；
9. capacity router；
10. GPT planner / Codex executor 自动闭环。

## 6. 视觉/视频引擎应该吸收什么

写入 `visual-art-engine-performance-ladder`：

1. 视觉生成天然允许 stochastic proposals；
2. 最终作品质量门禁必须独立于生成器；
3. 无效候选立即拒绝；
4. 失败优先 re-seed，而不是整体降级；
5. 统计 `first-attempt pass rate / attempts-to-success / T_TFVR`；
6. 如果用户要求 exact seed reproducibility，则重新切换为固定 seed 合同，不能自动换种；
7. 参考复刻、编辑任务如果语义依赖输入一致性，也不能默认 re-seed 代替算法修复。

## 7. 自动化方向

当前人工动作主要是：

```text
GPT 生成命令
-> 人复制到 Codex
-> Codex 执行
-> 人复制结果回 GPT
```

这不是高价值人工判断，只是 transport。

自动化目标：

```text
GitHub shared workspace = common truth
GPT = planner/judge
Codex = deterministic executor
AI Browser = ChatGPT transport
Capacity Router = model failover
Workflow Orchestrator = state machine + checkpoint + event routing
```

自动化必须保留用户作为最高中断/授权层，但不再要求用户搬运文本。

## 8. 最终经验一句话

> 固定任务后，先求物理边界，再用成熟方案做 Virtual-99；真实执行只验证被冻结的方案。对于随机生成系统，不强迫每个随机 proposal 一次成功，而用严格验证器拒绝坏样本，以最快路径重采样，优化首个有效交付结果的端到端时间。