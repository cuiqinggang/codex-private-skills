# Rule Patch: C Layer Official Prompt Is Mandatory

Date: 2026-07-06
Route: `UF_V7_SEMI_AUTO_ABCD`
Status: active

## Trigger

Use this rule whenever generating or validating an UltraFusion V7.0 C-layer copy package.

## Rule

For V7.0 full ABCD benchmark runs, C layer must use the official C prompt source:

```text
30-TEMPLATES/C_LAYER_OFFICIAL_FUSION_PROMPT_v20260706.md
```

Do not replace it with a short C_PROMPT summary, a generic "strategy integration" instruction, or a rewritten compact version.

## Required C Prompt Signals

A valid C-layer package must contain all of these signals:

- `复检陌生稿规则`
- `四维稠密融合`
- evidence / data hard rules
- multi-channel comprehensive review
- logic closure / reverse consistency checking
- output section `【最终答案：C_Fusion】`
- output section `【评审报告】`
- output section `【版本说明】`

## Failure Codes

If any required signal is missing, mark the layer invalid:

```text
UF_PROMPT_ASSEMBLY_FAIL: C_LAYER_OFFICIAL_PROMPT_MISSING
UF_PROMPT_ASSEMBLY_FAIL: C_LAYER_SIMPLIFIED_PROMPT_USED
UF_PROMPT_ASSEMBLY_FAIL: C_FUSION_OUTPUT_SCHEMA_MISSING
```

The resulting C output must not enter D layer until the C package is regenerated with the official prompt.

## Acceptance Gate

Before C-layer copy/paste:

- [ ] canonical V15 full text injected
- [ ] official C prompt source loaded verbatim
- [ ] B1/B2/B3 input materials present
- [ ] no `<<<V15_FULL>>>` placeholder remains
- [ ] one outer `[COPY_START]` and one outer `[COPY_END]`
- [ ] package validation records the official prompt signals above
