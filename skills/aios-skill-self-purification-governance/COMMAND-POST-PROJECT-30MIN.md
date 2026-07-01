# Command Package: Post-Project 30min Retrospective

Copy this command package into GPT or a long-task runner after a major project reaches PASS or ACCEPTED.

```text
TASK_ID:
AIOS_SKILL_SELF_PURIFICATION_POST_PROJECT_30MIN_RETROSPECTIVE

RUNTIME:
Minimum 30 minutes. Required checkpoints: start, 15min, final.

MODE:
Retrospective and candidate-patch mode only. Do not modify formal skill files.

SCOPE:
Review the just-completed project, its final outputs, failures, repairs, acceptance evidence, and reusable lessons.

PROCESS:
1. identify what worked
2. identify what failed or nearly failed
3. extract reusable SOP/checklist/template candidates
4. decide whether a skill update is needed
5. write candidate patches only
6. classify rejected and needs-human-review items

OUTPUTS:
runtime-evidence.json
checkpoint-timeline.html
project-lessons.md
candidate-skill-updates.md
rejected-edits.md
needs-human-review.md
outputs/index.html

PASS RULE:
PASS only if elapsed_minutes >= 30, checkpoints exist, no formal skill files were modified, and all formal changes remain candidates.
```

