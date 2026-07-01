# Command: 30min Light Check

```text
Run AIOS skill self-purification 30min light check.

Rules:
- Do not modify formal business skills.
- Do not auto-merge patches.
- Scan recent and high-risk skills for duplicate rules, stale rules, missing acceptance gates, missing runtime evidence, and unsafe auto-optimization.
- Produce detected-problems, risk-control-report, do-not-auto-optimize findings, patch buffer summary, runtime-evidence.json, checkpoint timeline, and clickable index.html.
- Use minimum_runtime_minutes = 30.
- Run verify-runtime-gate.mjs before declaring PASS.
```

