# UltraFusion V8.2 五项 P0 轻量测试报告

生成日期：2026-07-07
${REDACTED_SECRET}

## 测试 1：GPT_ONLY_V8_2

模拟条件：
- 只提供 GPT 答案。
- DeepSeek A/B 与千问 A/B 均无真实返回文本。

预期：
- 运行状态应标记为 `GPT_ONLY_V8_2`。
- 不得声称 DeepSeek / 千问参与。
- 不得称为完整三模型 V8.2。
- Gain 可信度可以为低或未知。

结果：
- `RUN_SUMMARY_TEMPLATE.md` 包含 `GPT_ONLY_V8_2` 状态。
- `SKILL.md` 明确规定 GPT_ONLY_V8_2 不能声称完成多模型验证。
- 通过。

## 测试 2：LIMITED_V8_2

模拟条件：
- GPT A/B 与 DeepSeek A/B 存在。
- 千问 B 缺失。

预期：
- 运行状态应标记为 `LIMITED_V8_2`。
- 必须明确缺失模型和缺失层级。
- 不得称为完整三模型 V8.2。

结果：
- `RUN_SUMMARY_TEMPLATE.md` 包含缺失模型与缺失层级字段。
- `SKILL.md` 明确规定 LIMITED_V8_2 不能称为完整三模型 V8.2。
- 通过。

## 测试 3：FULL_V8_2

模拟条件：
- GPT、DeepSeek、千问的 A/B 答案都存在。
- C/D 由 GPT 执行。

预期：
- 允许标记为 `FULL_V8_2`。
- D 层必须区分 `最终答案质量分（SCORE_FINAL）` 与 `D 层执行自评分`。
- D 层必须包含 Score_0 污染风险与 Gain 可信度。

结果：
- `SKILL.md` 包含 FULL_V8_2 定义。
- `D_PROMPT.md` 包含最终答案质量分（SCORE_FINAL）、D 层执行自评分、基线污染风险、Gain 可信度。
- 通过。

## 总结

- 三轮轻量测试结果：通过。
- 结论：SMOKE_PASS
