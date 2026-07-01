# Command Package: Weekly 30min Light Check

Copy this command package into GPT or a long-task runner when the weekly maintenance run is actually needed.

```text
TASK_ID:
AIOS_SKILL_SELF_PURIFICATION_WEEKLY_30MIN_LIGHT_CHECK

RUNTIME:
Minimum 30 minutes. Do not finish early. Required checkpoints: start, 15min, final.

MODE:
Shadow-only. Do not modify formal skill files. Do not auto-merge. Do not delete hard rules or failure reviews.

SCOPE:
Scan recent, new, modified, and frequently-used skills under C:\Users\A\.codex\skills and H:\AI\skills.

CHECK:
1. duplicate triggers
2. conflicting rules
3. missing acceptance pages
4. risky automation language
5. stale rejected-edit buffers
6. local rules that should not become global

OUTPUTS:
runtime-evidence.json
checkpoint-timeline.html
weekly-issue-list.md
candidate-patches.md
rejected-edits.md
needs-human-review.md
outputs/index.html

PASS RULE:
PASS only if elapsed_minutes >= 30, checkpoints exist, no formal skill files were modified, and auto-merge remains forbidden.
```

