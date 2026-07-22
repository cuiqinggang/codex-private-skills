# Benchmark Status: UltraFusion V7.0 Full Pipeline Final Gate Open

Date: 2026-07-06
Route: `UF_V7_SEMI_AUTO_ABCD`

## Current Status

The benchmark is not complete. The final D-layer external answer has not yet passed strict acceptance.

Do not rerun A/B/C unless the user explicitly asks. The next task should focus only on the D-layer final gate.

## Passed

- canonical V15 source recovered and locked
- full V15 injection required for A/B/C/D
- official C-layer prompt locked
- simplified C prompt failure captured
- D-layer refusal-prone wording removed
- D-layer `FINAL_ANSWER FIRST` wrapper added
- D-layer full-package rule added: wrapper + full V15 + official D_PROMPT + Q + A_Initial + C_Fusion
- D-layer production-depth rule added
- GitHub PR updated through commit `85e7b43`
- Knowledge Brain health check and hot sync passed

## Captured Failure Modes

1. `V15_FULL_MISSING`: shortened or summarized V15 invalidates a layer.
2. `C_LAYER_SIMPLIFIED_PROMPT_USED`: C layer must use the official C prompt.
3. `D_HARD_COMMAND_TRIGGERED_REFUSAL`: hard protocol wording can cause refusal.
4. `D_META_EVALUATION_WITHOUT_FINAL_ANSWER`: D output can become only a benchmark report.
5. `D_LAYER_V15_FULL_MISSING`: final-answer-first wrapper does not replace V15.
6. `FINAL_ANSWER_TOO_THIN`: correct order is not enough; the final answer must be production-depth.

## Latest Ready D Package

Use:

```text
${REDACTED_SECRET}
```

This package has passed assembly checks:

- one `[COPY_START]`
- one `[COPY_END]`
- `FINAL_ANSWER FIRST`
- full canonical V15
- official D prompt
- original Q
- A_Initial / Score_0
- C_Fusion
- 12-module production-depth requirement
- no unresolved placeholder

## Last External D Result

Status: failed strict gate.

Reason: external model output `Ultra_Answer_Final` first but gave a thin summary. It missed copyable prompt templates, full run schema, privacy SOP, structure-break/human-error fields, and detailed failure attribution.

Independent Codex scoring:

```text
Score_0 = 6.3 / 10
SCORE_FINAL = 8.1 / 10
Gain = +1.8
Verdict = INVALID_CHAIN_BY_STRICT_GATE
```

## Next-Run Acceptance Checklist

Accept the next D answer only if it contains:

- `# 1. Ultra_Answer_Final` first
- copyable 0/A/B/C/D prompt templates
- complete run record schema
- `Score_0`, `SCORE_FINAL`, `Gain`, `t_A`, `t_B`, `t_C`, `t_D`, `Total_Time`
- `BreakType`, `Human_Error`, `PII_Status`
- privacy redaction SOP
- scoring rubric and calibration method
- `Gain < 2` failure attribution tree
- 30-day validation plan
- Go / Internal Tool / No-Go thresholds
- D appendix with score, Gain, risk analysis, and benchmark verdict

If any core artifact is missing:

```text
UF_D_OUTPUT_FAIL: FINAL_ANSWER_TOO_THIN
```

