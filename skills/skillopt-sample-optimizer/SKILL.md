---
name: skillopt-sample-optimizer
description: Use when the user asks to run SkillOpt, skill self-cleaning, skill package optimization, 2h sample optimization, skill governance sample tests, candidate patches, before/after scoring, rejected edits, or safe optimization of Codex/H-drive skills without modifying formal skill packages.
---

# SkillOpt Sample Optimizer

Use this skill to run safe, evidence-backed optimization on a small set of skill packages. The goal is to improve future skill quality by producing candidate patches, rejected edits, before/after scores, and a clickable acceptance dashboard.

## Hard Rules

1. Treat formal skill directories as read-only unless the user separately approves a specific patch.
2. Copy selected samples into a `shadow-skills` workspace before any simulated edits.
3. Generate candidate patches only; do not auto-merge into `H:\AI\skills` or `C:\Users\A\.codex\skills`.
4. Preserve user hard rules, safety stop points, final acceptance rules, failure histories, visual proof rules, and rollback rules.
5. Require at least one rejected edit. If every proposed edit is accepted, re-run the risk review.
6. Prefer smaller, clearer edits over broad rewrites.
7. Never optimize by turning multiple skills into one giant prompt.
8. Always produce a clickable local HTML acceptance page.

## Workflow

1. Run a preflight reuse check for related skills, workspaces, failure reviews, and governance rules.
2. Select representative samples. Use 3 to 5 samples for quick validation and 10 to 15 samples for the 2h reusable workflow. Prefer diversity across long-task orchestration, dashboards, recovery/safety, visual/media work, skill sedimentation, automation, and meta-orchestration.
3. Copy each selected sample into `shadow-skills`.
4. Score each sample before optimization using the rubric in `references/rubric.md`.
5. Detect duplicated, stale, vague, risky, missing, or conflicting rules.
6. Generate candidate patches with `ADD`, `DELETE`, or `REPLACE`.
7. Split candidates into `accepted`, `needs human`, and `rejected`.
8. Simulate the effect on shadow copies only.
9. Score after optimization and explain which gains are real.
10. Write all required outputs and the acceptance dashboard.

## 2h Sample Optimization

For the current 2h reusable workflow, use `scripts/run_skillopt_v2.py`. Keep `scripts/run_skillopt_2h.py` only as the older 5-sample compatibility runner.

Default command:

```powershell
python C:\Users\A\.codex\skills\skillopt-sample-optimizer\scripts\run_skillopt_v2.py --workspace H:\AI\workspaces\AIOS-SKILLOPT-2H-SAMPLE-OPTIMIZATION-YYYYMMDD
```

The script must:

- read real skill files,
- copy samples into the workspace,
- produce candidate patches and rejected edits,
- produce needs-human-review items,
- create before/after scoring,
- identify skills and rule types that must not be auto-optimized,
- write next-run command packages for 30min and monthly-2h modes,
- write `index.html`,
- mark `formal_skills_modified` as `false`.

## Required Outputs

- `outputs/index.html`
- `outputs/skill-health-dashboard.html`
- `outputs/before-after-comparison.html`
- `outputs/selected-samples-expanded.md`
- `outputs/detected-problems.md`
- `outputs/candidate-patches.md`
- `outputs/candidate-patches-all.md`
- `outputs/accepted-candidates.md`
- `outputs/rejected-edits.md`
- `outputs/needs-human-review.md`
- `outputs/skill-score-before-after.json`
- `outputs/simplification-report.md`
- `outputs/risk-control-report.md`
- `outputs/do-not-auto-optimize-list.md`
- `outputs/long-term-run-policy.md`
- `outputs/next-run-command-30min.md`
- `outputs/next-run-command-monthly-2h.md`
- `outputs/final-verdict.md`
- `outputs/manifest.json`

## Final Verdict Rules

Use `USEFUL` only when the run:

- analyzes at least 3 real samples,
- produces accepted, rejected, and needs-human-review edits,
- keeps formal skills unmodified,
- creates HTML acceptance evidence,
- gives a concrete next-run frequency,
- records risks and human-review boundaries.

Use `PARTIAL_USEFUL` when outputs are present but sample count, evidence, or review depth is incomplete.

Use `NOT_USEFUL` when the process creates noisy suggestions, deletes hard rules, or cannot separate useful and risky edits.
