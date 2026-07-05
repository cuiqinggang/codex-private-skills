# D Layer Final-Answer-First Command Wrapper

Status: active
Route: `UF_V7_SEMI_AUTO_ABCD`
Purpose: ensure D layer generates the final answer to the original question before any scoring, benchmark, or meta-evaluation appendix.

## Required Placement

Place this command immediately after `[COPY_START]` and before source materials / long D rubric.

## Wrapper Text

```text
【D层执行命令：FINAL_ANSWER FIRST】

请基于下面的原始问题 Q、C_Fusion 候选稿、A_Initial/Score_0，生成 UltraFusion V7.0 D 层最终交付结果。

最重要：你的主任务不是评价 UltraFusion 系统本身，而是回答原始问题 Q，产出一份可以直接交付给用户使用的最终方案。

输出必须按以下顺序：

# 1. Ultra_Answer_Final（必须第一部分输出）

这一部分必须是对【原始问题 Q】的完整最终答案，而不是评测摘要。必须覆盖：

1. 系统流程
2. 角色分工
3. A/B/C/D 复制粘贴执行方式
4. 提示词/记录模板
5. 质量评分办法
6. 成本与时间控制
7. 隐私脱敏与安全规则
8. 风险清单与失败归因
9. 30 天验证计划
10. Go / Internal Tool / No-Go 决策标准

# 2. D层验收附录（第二部分输出）

在最终答案之后，再输出简短验收附录：关键事实表、四维评分、SCORE_FINAL、Gain、反例测试、推理链闭合性、风险分析、Benchmark 结论。

硬性禁止：
- 禁止只输出评估报告而没有 Ultra_Answer_Final。
- 禁止把 Ultra_Answer_Final 写成“对系统是否成立的判断”。
- 禁止只分析 Gain、统计学问题、SaaS 可行性，而不回答原始问题 Q。
- 禁止用“我可以继续帮你做 Python pipeline / SaaS 架构”作为结尾替代答案。

现在开始。第一行必须是：
# 1. Ultra_Answer_Final
```
