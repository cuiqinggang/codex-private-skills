---
name: knowledgebrain-cleanup-governance
description: Safely audit, clean, cold-archive, quarantine, and verify Knowledge Brain, Codex Documents, Obsidian, workspace, skill package, agent reference directories, and Windows Desktop task clutter. Use for desktop cleanup/organization, screenshot or step/check-number cleanup, one-off task scripts, Knowledge Brain cleanup, light-sync timeout prevention, rollback manifests, or reusable no-delete governance.
---

# Knowledge Brain Cleanup Governance

Use this skill for large-directory cleanup where the goal is to keep Knowledge Brain, skills, Obsidian, and Codex history usable without deleting valuable material.

## First Moves

${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
4. Read `references/cleanup-sop.md` before moving anything.
5. Prefer the bundled script `scripts/kb_cleanup_round2.ps1` as a starting point for manifest-backed moves.
6. For Desktop task clutter, read `references/desktop-task-artifact-cleanup-sop.md` and use `scripts/desktop_task_artifact_cleanup.ps1`.

## Hard Rules

- Never permanently delete original material.
- Move only to cold archive or rebuildable quarantine.
- Preserve relative paths unless Windows path length forces a documented `LONGPATH_RESIDUAL` fallback.
- Write a manifest before execution and update it after execution.
- Keep rollback commands in the manifest.
- Do not move `SKILL.md`, `README.md`, core indexes, sync policy files, tool scripts, `.git`, active repo roots, active skill roots, or Obsidian note bodies.
- Skip files or directories modified in the last 24 hours unless the user explicitly says they are inactive.
- If a directory is ambiguous, mark it for human review instead of moving it.
- For Desktop cleanup, preserve shortcuts, installers, user source images, active project directories, and ambiguous files by default.
- A file being recent is not sufficient reason to move it. Recent files may be included only when the user explicitly identifies the just-finished task as inactive clutter and the candidate matches the task-artifact rules.

## Workflow

1. Inventory explicit roots only. Do not do a blind full-disk scan.
2. Classify candidates:
   - `COLD_ARCHIVE`: old media, screenshots, reports, evidence, outputs, old backups, delivery packages.
   - `ISOLATE_REBUILDABLE`: `node_modules`, `dist`, `build`, `.cache`, `__pycache__`, `tmp`, `temp`, `logs`.
   - `KEEP_ACTIVE`: runtime skill bodies, Obsidian notes, current project state, policy and index files.
   - `HUMAN_REVIEW_REQUIRED`: repo roots, `.git`, ambiguous user data, active/recent material.
3. Run plan mode first and inspect the manifest for core-file mistakes.
4. Execute only low-risk planned rows.
5. Verify moved rows by checking that source paths are gone and target paths exist.
6. Run post-cleanup audit, health check, and two light sync passes.
7. Write a final report and an Obsidian pointer note.

## Required Verification

After execution, run:

```powershell
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
```

Acceptance target:

- `PARTIAL_TIMEOUTS=0` in all-source audit, or every remaining partial source has a specific listed reason.
- Health check `RESULT=PASS`.
- Light sync `RESULT=PASS`, `TIMEOUT=0`, `ERROR=0` twice.
- Final result is `PASS_CLEANED` or `PASS_CLEANED_WITH_SKIPS`.

## Script Use

Use the bundled script as a template:

```powershell
${REDACTED_SECRET}
${REDACTED_SECRET}
```

Before reuse, edit candidate lists and roots to match the current task. Keep the safety gates.

## Desktop Task Artifact Route

Trigger phrases include: `整理桌面`, `桌面清理`, `截图太多`, `step编号`, `check编号`, `检查编号`, `中间过程文件`, `一次性脚本`, `任务结束清场`.

Required order:

1. Inventory Desktop top-level items and compare recent additions with the last known cleanup report.
2. Confirm durable outputs already exist in the relevant skill, project output, or acceptance evidence.
3. Generate a CSV manifest in plan mode. Default candidates are task-named `.png` screenshots and `.py` one-off helpers only.
4. Preserve unrelated `.jpg/.jpeg`, shortcuts, installers, directories, archives, documents, and unknown files unless explicitly reviewed.
5. Execute from the saved manifest, verify every source/target pair, and retain rollback commands.
6. Update `RECENT_USE_LOG.md`, the relevant Obsidian skill note, and Knowledge Brain hot indexes.

Desktop cleanup is considered successful when the selected task artifacts are absent from Desktop, present in the cold archive, all manifest rows verify, and protected/ambiguous items remain untouched.
