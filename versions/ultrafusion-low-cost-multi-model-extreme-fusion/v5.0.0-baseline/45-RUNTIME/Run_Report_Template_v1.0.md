# 运行报告模板 v1.0

```
# UltraFusion Run Report

## Run ID: {run_id}
## Question: {question_summary}
## Timestamp: {timestamp}

## Model Status
| Model | A | B | C | D | Final Status |
|-------|---|---|---|---|--------------|
| GPT | ✓ | ✓ | ✓ | ✓ | PASS |
| DeepSeek | ✓ | ✓ | ✓ | ✓ | PASS |
| MiniMax | ✓ | ✓ | ✓ | ✓ | PASS |

## V15 Injection Gate
- A: ✓ | B: ✓ | C: ✓ | D: ✓
- V15_SHA256: {hash}

## D_Final Score: {score}/100

## Deductions: {count}, Total: -{points}
## Unique Contributions: {hero_model} (+{bonus})

## Final Verdict: {A+/A/B+/B/C/D}
```

## 2026-06-28 Runtime Parameter Log

Temperature profile: `ABCD_TEMP_v1`

| Stage | Temperature | Range | Notes |
|-------|------------:|-------|-------|
| A | 0.70 | 0.65-0.75 | independent extreme drafts |
| B | 0.60 | 0.50-0.65 | absorb all A extreme drafts and generate B extreme drafts |
| C | 0.35 | 0.25-0.40 | dense extreme fusion |
| D | 0.20 | 0.10-0.25 | final extreme review |

max_tokens policy: `RECORD_ONLY_UNTIL_CALIBRATED`

| Stage | Configured max_tokens | Actual output length | Truncated | Too verbose | V15 impact |
|-------|----------------------:|---------------------:|-----------|-------------|------------|
| A | {A_max_tokens_configured} | {A_actual_length} | {A_truncated} | {A_verbosity} | {A_v15_impact} |
| B | {B_max_tokens_configured} | {B_actual_length} | {B_truncated} | {B_verbosity} | {B_v15_impact} |
| C | {C_max_tokens_configured} | {C_actual_length} | {C_truncated} | {C_verbosity} | {C_v15_impact} |
| D | {D_max_tokens_configured} | {D_actual_length} | {D_truncated} | {D_verbosity} | {D_v15_impact} |
