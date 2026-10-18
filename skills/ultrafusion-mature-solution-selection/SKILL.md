---
name: ultrafusion-mature-solution-selection
description: 复杂任务成熟方案选择；不预设用户方案或多模型方案最优，以合格质量下最短完整交付时间选择最简单有效路径。
version: 1.0.0
status: VIRTUAL_MATURED_PENDING_REALITY
---
# UltraFusion：成熟方案优选与极限短时间

## 原则
用户提出的方案、三模型九候选、单模型多视角、Fusion、MoA 都只是候选，不预设任何一种为主方案。先复用该领域成熟最佳实践，再选择证据最强、结构最简单、质量合格且端到端时间最短的路径。目标不是拼接所有方案，而是找到净收益最高的最小方案。

## 优化目标
先定义任务完成条件与最低可接受质量 Q_min。仅比较满足 Q_min 的可行路线，以完整交付墙钟时间 T_valid 最短为首要目标，预算作为约束、成本作为次级指标。完整时间包含模型调用、并行等待、检索、融合、验证、重试、启动和交付。未经实测的时间只能标记 VIRTUAL_ONLY，不得宣称已测得物理极限。

## 七步极简流程
1. DEFINE：定义任务、Q_min、交付物、时间/预算/权限约束。
2. REUSE_GATE：优先搜索并复用官方成熟流程、成熟开源方案和已有技能包，建立最快可信 BASELINE。
3. COMPARE：最多保留 3 条真正不同的端到端候选（不是强制三条），比较质量证据、完整时间、成本、依赖、失败风险与集成开销。
4. SELECT：选择预期净收益最高的最简单方案。额外模型或步骤只有在能补足明确缺口/提供独立核验，且收益超过延迟、成本与协调开销时才加入。
5. FUSE/ATTACK：必要时仅融合兼容且有证据的优势；攻击一个最大瓶颈，检查最强反例。不得为全面而全面，也不得拼成未经验证的新系统。
6. STOP_GATE：没有可说明的净收益、需要自造调度器/状态机/锁/浏览器控制器，或融合成本抵消收益时，退回成熟 BASELINE。通常最多一次定向修复，不做无止境迭代。
7. VERIFY：输出最优路线、备选、质量 PASS/FAIL/UNKNOWN、实测或虚拟时间、失败回退条件与下一次 Reality 条件。

## 模型组合按需选择，不固定三模型
- 单模型直答：默认，适用于模型本身已能合格回答、额外调用预期收益低的任务。
- 单模型多视角/多次采样：适用于需要思路多样性、成本和调用复杂度仍低的任务；不得称为独立模型交叉验证。
- 两模型加裁判：适用于模型互补明显、第三个模型只需统一判断的任务。
- 三模型并行融合：仅当模型差异、任务价值与并行收益足以覆盖额外开销时使用。
- 多层 MoA/长轮辩论：非默认；只有实证收益超过增加的延迟才采用。
模型选择根据当前可用性、能力、工具、成本与时延决定，不预设某一品牌恒优。渠道不可用时降级，不虚构调用。

## 证据纪律
研究分数只对相应数据集、评审器与任务成立；不能直接证明一般推理、编码或现实速度。统一裁判不能替代来源核查、计算验证和真实测试；共识不等于正确。不得编造来源、执行日志、时间或验收状态。九路候选只在搜索空间确实广且任务价值足够高时作为可选探索方式，不是默认流程。

## BOT 与既有系统
BOT 是执行器，不是能力提升证据。优先复用既有《三人行》与 Windows 执行桥 C→A→B；C 未证实故障不得切 A。不修改代理，不另建协调基础设施。自动执行需真实权限和可用性；未执行方案标记 VIRTUAL_ONLY。

## 最小报告
任务/Q_min；复用的成熟方案及来源；最多三条有意义的端到端候选；所选方案及净收益；T_valid 实测或虚拟区间；成本；关键反例/失败条件；PASS/FAIL/UNKNOWN；是否值得增加模型或步骤；STOP_GATE/Reality 条件。

## 现实验收
比较单模型基线与候选方案时，使用同题、相同工具权限和 Q_min，记录质量通过率、端到端墙钟时间（样本足够时 p50/p90）、费用、重试与失败。未实测前状态为 VIRTUAL_MATURED_PENDING_REALITY，不得声称 FINAL PASS。

## 研究参考（仅用于提出候选）
- OpenRouter Fusion: https://openrouter.ai/blog/announcements/fusion-beats-frontier/
- Together AI Mixture-of-Agents: https://www.together.ai/blog/together-moa
- ICML 2024, “Should we be going MAD?”: https://proceedings.mlr.press/v235/smit24a.html
这些研究支持探索多模型/多视角组合，但不支持无条件固定三模型、九候选或多层辩论。

## 历史依据（保留，不覆盖）
- skills/ultrafusion-low-cost-multi-model-extreme-fusion/UltraFusion-6.1-官网三模型极限答案工作台.md
- skills/ultrafusion-v8-minimal-pressure-chain/SKILL.md
- skills/ultrafusion-nine-path-minimum-time/SKILL.md
本 Skill 负责统一选择原则，不宣称历史版本已全部通过现实验收。
