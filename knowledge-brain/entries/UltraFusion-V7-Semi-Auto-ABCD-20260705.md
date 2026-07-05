# UltraFusion V7.0 Semi-Automatic ABCD Skill Upgrade

Date: 2026-07-05
Skill path: `C:\Users\A\.codex\skills\ultrafusion-low-cost-multi-model-extreme-fusion`
Route label: `UF_V7_SEMI_AUTO_ABCD`
GitHub target: `cuiqinggang/codex-private-skills`

## Summary

UltraFusion V7.0 is a semi-automatic ABCD reasoning workflow:

- Codex generates question packages.
- The human only copies and pastes.
- External models answer.
- Codex fuses, converges, scores, and judges whether the answer improved enough.

## Retrieval Keywords

`UltraFusion V7.0`, `半自动ABCD`, `ABCD问题包`, `复制粘贴多层推理`, `外部模型回答`, `Score_0 vs Score_FINAL`, `Gain < 2`, `UF_V7_SEMI_AUTO_ABCD`, `多模型融合`, `V15`, `最终收敛`.

## Core Flow

1. Baseline: score the ordinary answer as `Score_0`.
2. A layer: generate three extreme external answers `A1/A2/A3`.
3. B layer: generate three enhanced fusion answers `B1/B2/B3`.
4. C layer: generate one strategy answer `C_FINAL`.
5. D layer: generate `FINAL_ANSWER`, `SCORE_FINAL`, and risk analysis.
6. Compare: `Gain = SCORE_FINAL - Score_0`.

## Hard Gate

If `Gain < 2.0`, the run is `INVALID_CHAIN`.

## Main Files

- `40-WORKFLOWS/Semi_Automatic_ABCD_CopyPaste_Workflow_v7.0.md`
- `30-TEMPLATES/V7_Semi_Auto_Question_Package_Template.md`
- `37-SCORING/V7_Baseline_Gain_Scoring_Rule.md`
- `45-RUNTIME/V7_Semi_Auto_Run_State_Schema.md`
- `65-RULE-PATCHES/RULE-PATCH-20260705-ultrafusion-v7-semi-auto-abcd.md`
- `70-NOTES/FAILURE-REVIEW-ENTRY-v7-semi-auto-abcd.md`

## Next-Run Rule

When a future task mentions UltraFusion V7.0 or 半自动ABCD, first load the skill package above, then use the V7 question package template. Do not ask the user to design prompts or make fusion decisions; their role is copy/paste only.

