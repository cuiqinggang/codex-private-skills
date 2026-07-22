# Skill Restore Execution Plan

Goal: restore usable skills without damaging official Codex state.

## Required Guardrails

- Back up current `.codex` and `.agents` first.
- Copy only missing Codex skill directories.
- Skip `.system`.
- Do not overwrite same-name directories.
- Do not copy `auth.json` or official SQLite/plugin/session state.
- Agents skills get diff/hash reports before any overwrite decision.

## Steps

1. Create a current-state backup under `K:\AI\backups\skills_backups` only after C validation and explicit approval for this exact backup; otherwise stop with `BACKUP_NOT_AUTHORIZED`.
${REDACTED_SECRET}
3. Write copied, skipped, and failed lists.
4. Count final target skills.
5. Run Agents diff.
6. Write restore report.

Stop if the user asks to overwrite anything; produce a diff first.
