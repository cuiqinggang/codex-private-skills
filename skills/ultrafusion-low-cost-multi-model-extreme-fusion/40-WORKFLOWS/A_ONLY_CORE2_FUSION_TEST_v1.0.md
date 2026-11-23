# A_ONLY_CORE2_FUSION_TEST v1.0

Date: 2026-06-23
Status: temporary test route

## Purpose

Use this route only for quick intermediate testing of:

- GPT official subscription browser capture.
- DeepSeek browser/API capture.
- Coordinate/screenshot bridge reliability.
- Whether two V15 extreme A drafts can produce a useful provisional answer.

## Hard Labels

Allowed label:

`A_ONLY_CORE2_FUSION_TEST`

Forbidden labels for this route:

- full UltraFusion
- full ABCD
- B layer
- C layer
- D layer
- D_Final
- Ultra_Answer_Final

## Required Inputs

- Original user question.
- V15 guard and A-layer prompt template.
- GPT A-layer response, if available.
- DeepSeek A-layer response, if available.
- Source/capture notes for each model.

## Steps

1. Route check: confirm the user has not explicitly requested or approved full ABCD execution.
2. Launch GPT and DeepSeek A-layer prompts in parallel where possible.
3. Require each model to produce a V15-style extreme A answer, not a casual answer.
4. Collect both A drafts with timestamps and model/source labels.
5. Fuse the two A drafts into a provisional answer.
6. Mark missing or failed models honestly. Do not fabricate missing A drafts.
7. Add the label `A_ONLY_CORE2_FUSION_TEST` in the output.
8. State that the result is not full UltraFusion acceptance evidence.

## Acceptance Criteria

- Output includes the exact route label.
- Output does not claim B/C/D execution.
- Output preserves model provenance.
- Output names missing models instead of inventing content.
- Output is treated as provisional, not final ABCD proof.

## Promotion Criteria

Only promote to full ABCD after the full UltraFusion pipeline is explicitly ready and the user asks for it or accepts it as the route.

## 2026-06-28 Status Update

This route is no longer the default for actual UltraFusion-style testing.

Current default has moved to full A/B/C/D workflow testing with:

`45-RUNTIME/ABCD_Temperature_And_Token_Strategy_v1.0.md`

Use this A-only route only if the user explicitly asks to return to it.

## 2026-06-28 Status Update

This route is no longer the default for actual UltraFusion-style testing.

Current default has moved to full A/B/C/D workflow testing with:

`45-RUNTIME/ABCD_Temperature_And_Token_Strategy_v1.0.md`

Use this A-only route only if the user explicitly asks to return to it.
