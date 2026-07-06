# UltraFusion V8 Failure Review Entry

Use this file when a V8 run fails, feels shallow, or produces unclear gain.

## Failure Template

```text
Date:
Question_ID:
Route:

Observed failure:
- B became comments:
- C became stitching:
- D became polishing:
- SelfScore inflated:
- Missing model fabricated:
- Facts not checked:
- Gain low or unknown:

Root cause:

Repair rule for next run:

Should this task have used V7.0 instead:
```

## Standing Repairs

- If B does not produce `B_ENHANCED_ANSWER`, invalidate B and rerun.
- If C lacks conflict handling, weak-evidence marking, and duplicate compression, invalidate C and rerun.
- If D does not attack before finalizing, invalidate D and rerun.
- If a current fact, price, model status, law, policy, or product detail matters, browse/check primary sources before scoring.
- If `Gain < 0.5`, admit low gain and prefer GPT direct for similar future tasks.
