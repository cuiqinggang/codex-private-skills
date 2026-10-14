# UltraFusion V7.5 半自动 ABCD 运行状态记录 Schema

状态：active

本文件中文化 `UF_V7_SEMI_AUTO_ABCD` 的运行记录字段。字段名保留英文，中文解释用于用户审校。

```yaml
run_id: 本次运行编号。
route_label: UF_V7_SEMI_AUTO_ABCD，半自动 ABCD 路线标签。
original_question: 用户原始问题。
baseline:
  baseline_answer_source: 普通直答答案来源。
  score_0: 普通答案初始评分，即 Score_0。
  quality_analysis: 普通答案质量分析。
  enter_abcd: 是否进入 ABCD。
layers:
  A:
    package_generated: 是否已生成 A 层问题包。
    external_answers:
      A1: 第一个外部模型的 A 层输出。
      A2: 第二个外部模型的 A 层输出。
      A3: 第三个外部模型的 A 层输出。
    accepted_answers: 被接受进入下一层的 A 输出。
    rejected_answers: 被拒绝的 A 输出及原因。
  B:
    package_generated: 是否已生成 B 层问题包。
    external_answers:
      B1: 第一个外部模型的 B 层增强答案。
      B2: 第二个外部模型的 B 层增强答案。
      B3: 第三个外部模型的 B 层增强答案。
    accepted_answers: 被接受进入 C 层的 B 输出。
    rejected_answers: 被拒绝的 B 输出及原因。
  C:
    package_generated: 是否已生成 C 层官方融合问题包。
    c_final: C 层高密度融合结果。
  D:
    package_generated: 是否已生成 D 层最终答案优先问题包。
    final_answer: D 层最终答案。
    score_final: D 层最终评分，即 SCORE_FINAL。
    risk_analysis: 风险、缺口、过度自信和人工确认点。
comparison:
  score_0: 普通答案初始评分。
  score_final: D 层最终评分。
  gain: Gain = SCORE_FINAL - Score_0。
  verdict: EFFECTIVE_CHAIN | INVALID_CHAIN。
notes:
  missing_inputs: 缺失输入。
  model_failures: 外部模型失败记录。
  human_copy_paste_issues: 复制粘贴边界或错贴问题。
  next_run_adjustments: 下次运行的修复建议。
```

## 状态码说明

- `EFFECTIVE_CHAIN`：有效链路，Gain 至少 2.0。
- `INVALID_CHAIN`：无效链路，Gain 小于 2.0 或关键门禁失败。