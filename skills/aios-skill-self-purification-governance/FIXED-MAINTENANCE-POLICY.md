# Fixed Maintenance Policy

Task ID: `AIOS_SKILL_SELF_PURIFICATION_FIXED_MAINTENANCE_POLICY_INSTALL_V1`

This policy fixes the maintenance rhythm for AIOS skill self-purification. It installs governance rules only. It does not run weekly, monthly, quarterly, or post-project maintenance.

## Fixed Cycles

| Cycle | Runtime | Suggested Timing | Purpose | Formal skill writes |
| --- | ---: | --- | --- | --- |
| Weekly light check | 30 min minimum | Sunday night | Scan recent, new, modified, and frequently-used skills for issues | Forbidden |
| Monthly sample optimization | 120 min minimum | First Sunday night | Score and shadow-test 10-15 high-value or high-risk skills | Forbidden |
| Quarterly graph governance | 240 min minimum | First Sunday night of the first month of each quarter | Build a relation graph and find duplication, conflicts, stale files, orphan skills, and trigger risk | Forbidden |
| Post-project retrospective | 30 min minimum | After major project PASS or ACCEPTED | Extract lessons, failures, and skill update candidates | Forbidden |

## Time Sufficiency Verdict

- Weekly 30 min is enough because it is a light scan and issue-list task, not deep rewriting, merge work, deletion, or global restructuring.
- Monthly 2h is enough because V3 verified 12 samples in 120.02 minutes with 9 checkpoints and produced before/after scores, accepted candidates, rejected edits, and human-review items.
- Quarterly 4h is enough for medium-scale global scan and graph governance because it produces relation maps and merge suggestions only, with no direct merge.
- 8h is not routine. Reserve 8h only for semiannual or annual large reorganization, major migration, or multi-package governance repair.

## Red Lines

1. Never unattended auto-merge formal skills.
2. Never auto-delete user hard rules.
3. Never auto-delete failure reviews.
4. Never auto-modify high-risk system operation rules.
5. Never auto-expand total-control trigger scope.
6. Never generalize project-local rules into global rules.
7. Never overwrite formal files just because a score improved.
8. Formal merges require user or GPT Gate Review.
9. All 30min, 2h, 4h, and 8h tasks must pass runtime gate.
10. Insufficient `elapsed_minutes` forbids PASS.

## Operating Mode

All maintenance outputs must be shadow-first:

- create issue lists,
- create candidate patches,
- classify accepted, rejected, and needs-human-review items,
- write runtime evidence,
- write an offline review page,
- leave formal skill packages untouched unless a separate explicit merge approval is granted.

