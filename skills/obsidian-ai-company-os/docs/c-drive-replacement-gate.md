# C Drive Replacement Gate

This file defines the minimum gate before replacing:

${REDACTED_SECRET}

## Must Be True

- User explicitly approves replacement in a separate task.
- The old C-drive package is backed up first.
- The backup path is recorded.
- The old C-drive directory is not deleted directly.
- The clean candidate is copied only after backup.
- `SKILL.md`, `README.md`, and `MANIFEST.json` are checked after copy.
- Codex skill loading is verified after replacement.
- Rollback is tested as a plan before any replacement command runs.

## Must Not Happen

- Do not run `replacement-commands-preview.ps1` during review.
- Do not copy old `assets/project_snapshot` into the clean candidate.
- Do not treat this review as replacement approval.

