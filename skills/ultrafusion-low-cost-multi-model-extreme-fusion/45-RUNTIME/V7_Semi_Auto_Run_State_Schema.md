# UltraFusion V7.0 Semi-Auto Run State Schema

Date: 2026-07-05
Status: active

Use this schema when Codex runs `UF_V7_SEMI_AUTO_ABCD`.

```yaml
run_id:
route_label: UF_V7_SEMI_AUTO_ABCD
original_question:
baseline:
  baseline_answer_source:
  score_0:
  quality_analysis:
  enter_abcd: true
layers:
  A:
    package_generated: false
    external_answers:
      A1:
      A2:
      A3:
    accepted_answers:
    rejected_answers:
  B:
    package_generated: false
    external_answers:
      B1:
      B2:
      B3:
    accepted_answers:
    rejected_answers:
  C:
    package_generated: false
    c_final:
  D:
    package_generated: false
    final_answer:
    score_final:
    risk_analysis:
comparison:
  score_0:
  score_final:
  gain:
  verdict: EFFECTIVE_CHAIN | INVALID_CHAIN
notes:
  missing_inputs:
  model_failures:
  human_copy_paste_issues:
  next_run_adjustments:
```

