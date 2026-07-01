# Command: Monthly 2H Sample Optimization

```text
Run AIOS monthly SkillOpt 2H sample optimization.

Rules:
- Use a shadow workspace.
- Select 10-15 high-value, high-reuse, high-risk skills.
- Include accepted, rejected, and needs-human patch buffers.
- Do not modify formal business skills.
- Do not auto-merge accepted candidates.
- Preserve do-not-auto-optimize list.
- Use minimum_runtime_minutes = 120.
- Create at least 8 checkpoints plus final checkpoint.
- Produce runtime-evidence.json, runtime-proof.html, checkpoint-timeline.html, skill-score-before-after.json, accepted-candidates.md, rejected-edits.md, needs-human-review.md, simplification-report.md, risk-control-report.md, final-verdict.md, and index.html.
- Run verify-runtime-gate.mjs before declaring PASS.
```

