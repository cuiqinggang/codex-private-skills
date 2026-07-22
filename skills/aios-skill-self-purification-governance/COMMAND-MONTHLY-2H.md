# Command Package: Monthly 2h Sample Optimization

Copy this command package into GPT or a long-task runner when the monthly sample optimization run is actually needed.

```text
TASK_ID:
AIOS_SKILL_SELF_PURIFICATION_MONTHLY_2H_SAMPLE_OPTIMIZATION

RUNTIME:
Minimum 120 minutes. Do not finish early. Required checkpoints: 0, 15, 30, 45, 60, 75, 90, 105, 120 final.

MODE:
Shadow-only. Do not modify formal skill files. Do not auto-merge. Candidate patches only.

SCOPE:
${REDACTED_SECRET}

PROCESS:
1. collect skill inventory and recent-use evidence
2. select 10-15 samples
3. score before state
4. generate candidate improvements
5. reject over-broad, risky, or local-only changes
6. score after state in shadow
7. split accepted, rejected, and needs-human-review
8. produce review dashboard

OUTPUTS:
runtime-evidence.json
checkpoint-timeline.html
skill-score-before-after.json
accepted-candidates.md
rejected-edits.md
needs-human-review.md
simplification-report.md
risk-control-report.md
outputs/index.html

PASS RULE:
PASS only if elapsed_minutes >= 120, checkpoint evidence exists, formal_skills_modified is NO, and no auto-merge occurred.
```

