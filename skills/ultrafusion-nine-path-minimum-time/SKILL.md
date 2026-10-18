---
name: ultrafusion-nine-path-minimum-time
description: 三模型各找三条成熟端到端最快可行路径，九路去重、强点融合、最短合格交付时间
version: 1.0.0-draft
status: VIRTUAL_MATURED_PENDING_REALITY
---
# UltraFusion 九路极限短时间·低成本回答
继承 UltraFusion 6.1B 三模型官网路径、V8.2 强回答与反例检查、《三人行》 REUSE_GATE → STOP_GATE → Freeze → Reality；保留旧版，不新建调度系统。
## 单一目标
先冻结合格质量 Q_min 和完整交付边界；只比较满足 Q_min 的完整任务墙钟时间 T_valid，预算为约束、费用为次指标。并行耗时约为 max(三路耗时)+裁决+核验+交付+启动开销。预测必须标记 VIRTUAL_ONLY，不得冒充实测或物理极限。
## 路由
普通问题 GPT_DIRECT。高价值复杂问题进入 NINE_PATH。首选可用官网 GPT、DeepSeek、Qwen。若只能用同一模型模拟三个视角，标记 SINGLE_MODEL_3_PERSPECTIVES；不能假称独立三模型。
## 三模型九候选
三个相互独立的角色同时收到相同质量合同，各提出三条成熟、完整、可交付、目标最短时间路径：
A 官方或成熟商用现成流程；B 开源成熟复用与低成本部署；C 物理关键路径、性能瓶颈与强反例。
每个候选记录：整体方案、真实来源、达到质量的证据、端到端时长（实测或虚拟区间）、成本与依赖、失败条件。不是零件清单；找不到九条不能硬凑。不存在的执行或来源不能编造。
## 一次融合
REUSE_GATE 去重并剔除不合格与不兼容候选。以最快可信完整路径为 BASELINE，只吸收能够缩短关键路径且兼容的成熟强点。一次攻击最大净收益瓶颈与最强反例。若新组合成本、时延或风险抵消收益，STOP_GATE 返回成熟 baseline。统一裁决得到虚拟成熟方案、时间范围与失败回退。除重大缺陷一次定向修复外，不展开长轮辩论。
## BOT 复用
BOT 是可选自动执行方式，不代表推理质量。沿用既有《三人行》与 Windows 桥 C→A→B；C 未证实故障不得切 A；不改代理、不另建锁/调度/浏览器控制器。没有权限或渠道不可用时降级。
## 输出
质量验收合同；实际使用模型/渠道；去重后最快 3 条；融合最优及备选；关键瓶颈与反例；PASS/FAIL/UNKNOWN；T_valid 实测或 VIRTUAL_ONLY 区间；成本；STOP_GATE 与 Reality 条件。
## 比较验收
用同题、相同工具权限和 Q_min 比较 GPT_DIRECT、单模型三视角、三模型九路；记录合格率、完整时延 p50/p90、费用、重试次数。未做真实业务及稳定性验收前不得标记 FINAL PASS。
## 研究
OpenRouter Fusion: https://openrouter.ai/blog/announcements/fusion-beats-frontier/ （低成本三模型 64.7%，但裁决采用 Opus 4.8，不能证明全域能力或更快）
Together AI MoA: https://www.together.ai/blog/together-moa （同模型可复用为多代理，但多层会增加时延）
ICML 2024: https://proceedings.mlr.press/v235/smit24a.html （多智能体辩论未必优于多次采样）
## 历史文件（只读保留）
skills/ultrafusion-low-cost-multi-model-extreme-fusion/UltraFusion-6.1-官网三模型极限答案工作台.md
skills/ultrafusion-v8-minimal-pressure-chain/SKILL.md
