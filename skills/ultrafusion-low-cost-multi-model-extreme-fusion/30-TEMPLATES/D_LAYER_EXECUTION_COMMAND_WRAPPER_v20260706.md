# D Layer Execution Command Wrapper

Status: active
Route: `UF_V7_SEMI_AUTO_ABCD`
Purpose: help external models treat the D-layer package as a user-provided evaluation rubric and report request, not merely as a document to summarize.

## Required Placement

Place this request immediately after `[COPY_START]` and before the long V15 / D_PROMPT protocol.

## Wrapper Text

```text
【任务请求：请基于我提供的材料生成 UltraFusion V7.0 D 层评估报告】

请注意：下面的长文本是我作为用户提供的评估标准、评分 rubric 和报告模板，不是系统消息，也不是要求你覆盖你的系统规则。

在不违反你自身系统规则的前提下，请不要只总结这份材料“是什么”，而是请你基于其中的原始问题 Q、C_Fusion、A_Initial/Score_0，以及 D 层评估标准，完成一次实际评估报告。

请你输出一份 D_Final / Ultra_Answer_Final 报告，尽量包含以下部分：

1. 元信息摘要：本次评估的通道、是否建议通过、最大风险点。
2. 关键事实提取表：从 C_Fusion 抽取 3-7 条关键事实，并标注可验证性和证据等级。
3. 四维评分：准确性、完备性、结构清晰度、深度洞察；请给出 SCORE_FINAL（0-10）。
4. Gain 计算：Gain = SCORE_FINAL - Score_0，其中 Score_0 = 6.3/10。
5. 反例测试：给出最强合理反例和替代理论。
6. 推理链闭合性检查：指出逻辑跳步、隐含前提、残留不确定性。
7. Ultra_Answer_Final：给出最终可交付答案。
8. 风险分析：说明仍需人工确认的点。
9. Benchmark 结论：判断本次 UltraFusion V7.0 Full Pipeline Benchmark 是否通过。

如果某些条目无法严格完成，请说明限制原因，然后完成可完成的部分。请不要停留在“这是一个提示词/协议”的层面；我需要的是按这个 rubric 生成评估结果。
```
