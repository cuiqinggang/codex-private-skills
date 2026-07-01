---
name: ecc-endurance-ladder-unified
description: Use when the user asks about ECC, endurance ladder, Claude-style 12-layer workflow, mature replay, completion closure, independent verification, final acceptance, or packaging ECC governance assets. This local skill is a lightweight entrypoint that points to the unified H-drive source of truth instead of duplicating it.
---

# ECC Endurance Ladder Unified

Use this as the short Codex entrypoint for ECC work.

The source package is:

```text
H:\AI\skills\ecc-endurance-ladder-unified
```

Start there, in this order:

1. `README.md`
2. `SKILL.md`
3. `MANIFEST.md`
4. `reports\index.md`

Do not load the old baseline and governance packages in parallel unless a task
explicitly asks for historical comparison. The unified package already merged
the endurance ladder baseline with skill-package governance evolution.

For complex ECC runs, final PASS requires a final acceptance artifact, not just
execution claims, report text, or model self-report. Prefer the unified package
scripts under `H:\AI\skills\ecc-endurance-ladder-unified\scripts`.

This shim intentionally contains no copied templates, reports, or scripts. It
exists to make the current `.codex\skills` registry route future ECC work to the
single H-drive source of truth.
