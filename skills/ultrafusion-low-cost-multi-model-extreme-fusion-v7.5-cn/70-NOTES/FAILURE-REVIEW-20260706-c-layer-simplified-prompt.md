# Failure Review: Simplified C Prompt Used In V7 Benchmark

Date: 2026-07-06
Route: `UF_V7_SEMI_AUTO_ABCD`
Status: fixed

## What Happened

During the UltraFusion V7.0 full pipeline benchmark, the first C-layer package used a simplified internal C prompt instead of the user-supplied official C-layer prompt.

The simplified version described C layer as generic strategy integration and did not include the full stranger recheck, dense fusion, evidence alignment, reverse consistency, and `C_Fusion` output requirements.

## Why This Was Wrong

C layer is not a light merge step. In V7.0 full ABCD it is the official multi-draft fusion layer and must run with:

- stranger recheck
- dense four-dimensional fusion
- evidence and data hard rules
- logic closure checks
- reverse consistency checks
- `【最终答案：C_Fusion】`, `【评审报告】`, and `【版本说明】`

## Corrective Action

The simplified C package was invalidated. The official prompt was preserved at:

```text
30-TEMPLATES/C_LAYER_OFFICIAL_FUSION_PROMPT_v20260706.md
```

A new C-layer package must be generated from that source before entering D layer.

## Future Prevention

Before any C-layer package is handed to the user, validate:

- contains `复检陌生稿规则`
- contains `四维稠密融合`
- contains evidence / data hard rules
- contains `【最终答案：C_Fusion】`
- contains `【评审报告】`
- contains `【版本说明】`

If validation fails, stop immediately and regenerate the C package.
