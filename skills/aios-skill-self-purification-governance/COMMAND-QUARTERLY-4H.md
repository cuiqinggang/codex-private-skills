# Command Package: Quarterly 4h Graph Governance

Copy this command package into GPT or a long-task runner when the quarterly graph governance run is actually needed.

```text
TASK_ID:
AIOS_SKILL_SELF_PURIFICATION_QUARTERLY_4H_GRAPH_GOVERNANCE

RUNTIME:
Minimum 240 minutes. Do not finish early. At least 16 checkpoints and a final checkpoint are required.

MODE:
Shadow-only graph governance. No formal merge. No automatic deletion. No hard-rule rewrite.

SCOPE:
${REDACTED_SECRET}

CHECK:
1. duplicate skills
2. trigger conflicts
3. stale skills
4. orphan skills
5. total-control trigger expansion risk
6. local project rules incorrectly promoted to global rules
7. merge candidates
8. do-not-merge list

OUTPUTS:
runtime-evidence.json
checkpoint-timeline.html
skill-relation-graph.json
duplicate-skill-report.md
trigger-conflict-report.md
stale-or-orphan-report.md
merge-suggestions.md
do-not-merge-list.md
needs-human-review.md
outputs/index.html

PASS RULE:
PASS only if elapsed_minutes >= 240, at least 16 checkpoints exist, formal_skills_modified is NO, and merge suggestions remain suggestions.
```

