# UltraFusion V8.2 Failure Review Entry

Use this file when a V8.2 run fails, feels shallow, produces unclear gain, or trips a gate.

## Failure Template

```text
Date:
Question_ID:
Route:

Before_A_Route_Gate:
- Matched_Count:
- Route_Decision:
- Should route have been different:

Observed failure:
- B became comments:
- C became stitching:
- D became polishing:
- SelfScore inflated:
- Deduction empty/generic:
- Missing model fabricated:
- Facts not checked:
- Gain low or unknown:
- EARLY_WARNING high after repair:
- D_Final_Insurance_Check failed:

Gate code:
- B_DEGRADATION_FAIL:
- C_STITCHING_FAIL:
- D_POLISHING_FAIL:
- V8_QUALITY_FAIL:

Root cause:

Repair rule for next run:

Should this task have used V7.0 instead:
```

## Standing Repairs

- If Before-A matches fewer than 2 criteria, prefer `GPT_DIRECT`.
- If B does not produce `B_ENHANCED_ANSWER`, invalidate B and rerun once.
- If B is not standalone or is only a review, mark `B_DEGRADATION_FAIL` after one failed rerun.
- If C lacks conflict handling, weak-evidence marking, duplicate compression, or D judgement points, invalidate C and rerun once.
- If C still fails, mark `C_STITCHING_FAIL`.
- If D does not attack C before finalizing, invalidate D and rerun once.
- If D only polishes language without attack, judgement, and repair, mark `D_POLISHING_FAIL`.
- If `D_Final_Insurance_Check` has 0-1 YES after repair, mark `V8_QUALITY_FAIL` and recommend V7.
- If a current fact, price, model status, law, policy, or product detail matters, browse/check primary sources before scoring.
- If Deduction is empty or generic while SelfScore is high, lower the score or rewrite the scoring block.
- If `Gain < 0.5`, admit low gain and prefer GPT direct for similar future tasks.

## Balance Failure Template

```text
Quality:
- Did the answer become shallow or brittle:
- Did B/C/D actually improve the answer:
- Did Verdict = TOO_THIN require a warning:

Architecture:
- Which added gate was necessary:
- Which added field was ceremony:
- Did anything drift toward V7/V15:

Speed:
- Did the chain feel too slow for the task:
- Could ceremony be reduced while keeping B/C/D duties:

Decision:
- Keep V8.2:
- Simplify V8.2:
- Upgrade to V7:
```
