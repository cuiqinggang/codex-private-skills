# HIPE v0.3.5 × 极限短时间引擎：集成冻结

状态：FROZEN_INTEGRATION_CONTRACT  
日期：2026-10-06  
目的：冻结 HIPE v0.3.5 在极限短时间任务流程中的正确定位，不修改 HIPE v0.3.5 冻结资产。

## 1. HIPE v0.3.5 权威冻结

```text
REPO=cuiqinggang/codex-private-skills
PATH=skills/hybrid-intelligence-probability-engine-v0-3-5/
FREEZE_COMMIT=c6fe2878fd237e7a8120b3af8e75f93e3cd6a4d9
FREEZE_ID=HIPE-v0.3.5-FULLY-SEALED-20261006-R1
STATE=FULLY_SEALED
POLICY=IMMUTABLE; NEEDS_VERSIONED_UPGRADE
```

正式组件：
- Reality Solvability Gate v0.2.0
- Comfort-Zone Forward Compiler v0.2.0
- CODE / JEV / GPT residual 路由
- 合法并行
- deterministic verifier

HIPE v0.3.5 原冻结字节不在本集成文档中改动。

## 2. 从任务第一步开始的固定集成点

```text
TASK_ACCEPTED
↓
[Gate] Reality Solvability Gate v0.2.0
↓
成熟直接解 / 成熟组合解 / 成熟探索协议 / 未知前沿
↓
[Compiler] Comfort-Zone Forward Compiler v0.2.0
↓
┌──────────────┬──────────────┬───────────────┐
│ CODE         │ JEV          │ GPT residual  │
│ 精确确定性   │ 有限Choice   │ 开放生成/未知 │
└──────────────┴──────────────┴───────────────┘
↓
按真实依赖图最大合法并行
↓
冻结整包方案
↓
Reality Executor
↓
deterministic verifier
↓
FINAL_VALID
```

## 3. “全流程都能用”的正确解释

HIPE 可以挂在几乎所有关键判断点前面，但不是所有步骤都做远端模型调用。

### 适合 CODE
- 精确整数/阈值；
- 文件、hash、schema、ffprobe；
- 有明确算法的状态判断；
- 原子提交；
- exactly-once gate；
- 已冻结动作执行。

### 适合 JEV
必须同时满足：
- 语义保持；
- 状态明确/可提取；
- 选择有限或可枚举；
- action ontology 已认证；
- 有 deterministic verifier；
- 不需要开放生成；
- 没有 unresolved hidden information；
- 不依赖 timed retry。

典型：
- 下一浏览器动作从可见控件表中选择；
- 工具路由；
- 多候选优先级；
- failure class；
- allow / block / review；
- continue / stop；
- 多个独立 typed decisions 一次并行回答。

### 适合 GPT residual
- 目标/规格还不完整；
- 需要第一性原理重构；
- 开放式设计或写作；
- 页面未暴露必要动作；
- 隐藏信息未解决；
- 需要动态创造新候选；
- timed retry 或复杂长程恢复。

## 4. Browser / Web 集成模型

推荐结构：

```text
GPT：首次目标理解 / 必要自由文本
CODE：页面观测→真实控件表、状态快照、执行、freshness、verifier
JEV：有限 operation + target Choice
CODE：执行
JEV/CODE：下一有限选择
...
deterministic verifier：确认任务完成
```

不要让通用 LLM 每一步重新：
- 读完整页面；
- 生成 selector；
- 解释所有可能动作；
- 再决定一个点击。

这类反复生成会形成 model barrier。

## 5. 公开现实证据（仅作外部方法证据，不冒充本地 Reality）

Ora 2026-09 的 240-run 对照：
- browser median：1.9s（JEV） vs 8.2s（LLM decider），约 4.3x，加速约 76.8%；
- browser 单步 decision：159ms vs 1211ms，约 7.6x，decision latency 减少约 86.9%；
- WebMCP：1.4s vs 3.7s，约 2.6x，时间减少约 62.2%；
- NLWeb：2.0s vs 7.8s，约 3.9x，时间减少约 74.4%；
- browser success：78% vs 71%，但存在 JEV 因页面未暴露 search box 而 0/5 的任务。

独立 jev-browser 项目单次公开 demo：
- 2.13s / 2 decisions vs LLM tool-calling 8.20s / 4 decisions；
- 约 3.85x，时间减少约 74%。

TypeSafe 官方说明：
- Jev 面向 typed decisions，而非 strings；
- 多问题可并行采样；
- 官方给出的端到端范围约 70–500ms；
- 官方工作流高倍数结果属于 System-One-shaped workflow，不应直接外推为所有任务。

来源：
- https://ora.ai/blog/evaluating-jev
- https://github.com/dennisonbertram/jev-browser
- https://typesafe.ai/blog/introducing-system-one-models-and-jev
- https://openrouter.ai/blog/tutorials/how-to-use-jev/

## 6. 对我们的预期收益边界

外部证据支持：当“决策”占任务关键路径很大时，JEV/HIPE 能显著缩短时间。

但整体任务加速受 Amdahl 定律约束：
- 决策只占约30%：即使决策快7.6x，整体约只快1.35x；
- 决策约50%：整体约快1.77x；
- 决策约70%：整体约快2.55x；
- 类似公开 browser benchmark 决策约83%：整体可能接近3.6x，实际公开对照约4.3x。

因此不能宣称“任何任务都提高4–5倍”。

对当前极限短时间方法，更可靠的目标是同时减少：
1. 模型判断屏障；
2. 不必要串行；
3. Reality 次数；
4. 页面切换与人工胶水；
5. LLM 在有限选择上的重复大推理。

## 7. 新方法验证预算

旧 Greenfield：11 次 Reality 实例。

新版方法目标：
- 3–4轮内验证收敛；
- 硬上限5轮。

若任务同等复杂，Reality 次数目标相对旧11次：
- 3轮：减少约72.7%；
- 4轮：减少约63.6%；
- 5轮上限：仍减少约54.5%。

这只是结构预算，不是已认证速度成绩。

## 8. 安全与正确性边界

- JEV 只能从提供给它的候选中选，页面没暴露必要动作时不能靠它猜。
- consequential action 仍必须有确定性权限/业务 gate。
- DONE 不能由模型自报替代 verifier。
- 无 verifier 的开放回答不得提升为 FINAL_VALID。
- 本集成合同不改变 HIPE v0.3.5 原认证范围。

## 9. 冻结结论

```text
HIPE_ROLE=GLOBAL_META_DECISION_LAYER
JEV_ROLE=BOUNDED_TYPED_DECIDER
CODE_ROLE=DETERMINISTIC_STATE_ACTION_VERIFY
GPT_ROLE=OPEN_REASONING_AND_RESIDUAL
REALITY_ROLE=FROZEN_PLAN_CERTIFICATION
```

核心原则：

**处处可路由，不等于处处用 JEV；先把问题编译成最便宜、最快、可验证的执行形态。**
