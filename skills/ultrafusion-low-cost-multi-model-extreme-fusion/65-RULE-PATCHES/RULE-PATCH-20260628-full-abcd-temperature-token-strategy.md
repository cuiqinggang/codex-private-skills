# Rule Patch: Full ABCD Temperature and Token Strategy

Date: 2026-06-28
Source material: H:\AI\inbox\codex-learning-materials\01-new\20260628-ultrafusion-full-abcd-temperature-and-token-strategy.md
Value: HIGH_VALUE

## Rules

1. Do not modify V15 source text for temperature or token settings.
2. Temperature policy belongs in runtime/runbook/router/prompt-assembly execution rules.
3. A/B/C/D are all V15 extreme stages; temperature only controls divergence versus convergence.
4. Temperature descends from A to D: A/B maximize independent divergence; C/D maximize correctness and stability.
5. Default temperatures: A 0.70, B 0.60, C 0.35, D 0.20.
6. B is one layer: each participating model reads all valid A extreme drafts and directly generates `B_<model>_Extreme`.
7. Do not split B into sublayers or two-step variants unless the user explicitly asks for a separate experiment.
8. max_tokens is not fixed yet. It is a test record item until real full-flow runs provide evidence.
9. Current default actual test route is full ABCD workflow testing. `A_ONLY_CORE2_FUSION_TEST` is paused as default.

## Trigger Keywords

- UltraFusion temperature
- A/B/C/D temperature
- B layer temperature
- max_tokens
- full flow test
- full ABCD test
- A/B maximize independent divergence C/D maximize correctness
- A layer wide divergence
- 温度策略
- 全流程测试

## Preflight Action

Before running or planning a full UltraFusion test, read:

- `45-RUNTIME/ABCD_Temperature_And_Token_Strategy_v1.0.md`
- `40-WORKFLOWS/Automated_ABCD_Extreme_Workflow_v5.0.md`
- `20-RUNBOOK/Automated_Runbook_v1.0.md`
- `30-TEMPLATES/00_Router_Template_v1.0.md`

## Acceptance Criteria

- Temperature defaults appear in runtime state and run reports.
- max_tokens appears as recorded telemetry, not as a hardcoded final value.
- Full-flow tests use A/B/C/D, not A-only route.
- B is not split into sublayers or two-step variants.
- B outputs are B-layer extreme drafts, not summaries or peer-review notes.
