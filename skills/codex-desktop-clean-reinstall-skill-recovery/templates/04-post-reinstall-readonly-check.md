# Post-Reinstall Read-Only Check

Goal: inspect the fresh official Codex state without changing it.

## Checks

- H-drive backup exists.
- `codex-skills` and `agents-skills` counts.
- Current `C:\Users\A\.codex` exists.
- Current `C:\Users\A\.codex\skills` exists.
- Current `.system` exists and is preserved.
- Current `C:\Users\A\.agents\skills` exists.
- Agents `learned` skill is identified if present.
- Codex++ residue paths and shortcuts are listed.
- Same-name skill conflicts are listed.
- Non-conflicting Codex restore candidates are listed.

## Output

Write a Markdown report to:

`C:\Users\A\Desktop\1\output\codex-official-reinstall-recovery-check-report.md`

No delete, overwrite, or move actions are allowed in this stage.
