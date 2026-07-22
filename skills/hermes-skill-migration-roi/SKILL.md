---
name: hermes-skill-migration-roi
description: Sanitized private mirror entry; sensitive source details were removed.
---

# Hermes Skill Migration ROI Windows Studio

Use this skill before moving legacy H-drive skills into the current Windows Codex studio. The goal is to convert useful procedures into safe Windows skills, not blindly copy old runtimes.

## Core Rule

Treat legacy skills as an investment portfolio:

1. Preserve backups first.
${REDACTED_SECRET}
3. Classify each candidate by Windows value, duplicate status, rewrite cost, safety risk, and verification path.
4. Import only small high-value batches.
5. Convert commands to Windows PowerShell and current local paths.
6. Stop before deletes, broad overwrites, installs, account actions, secrets, or cloud spend.

## Workflow

1. Inventory candidate `SKILL.md` files and active local skills.
2. Classify each candidate as active duplicate, ready to adapt, reference only, archive, or reject.
${REDACTED_SECRET}
4. Keep source H-drive backups unchanged unless the user explicitly asks to modify them.
5. Rewrite body instructions for Windows Studio: PowerShell, Windows paths, current ports, backup, rollback, smoke tests.
6. Verify frontmatter, discoverability, and relevant bundled resources.

## Gates

- `G01 inventory`: confirm candidate scope and active skill conflicts.
- `G02 adapt`: write Windows-safe skill files under the active skill directory.
- `G03 verify`: check `SKILL.md` frontmatter, counts, paths, and trigger descriptions.
- `G04 operational test`: run only safe local smoke checks relevant to the skill.
- `G05 destructive`: stop before deleting or overwriting preserved copies.

## References

- `references/status-20260519.md`: historical migration state.
- `references/roi-rules.md`: scoring ideas.
- `references/commands.md`: old command snippets to adapt, not blindly execute.

## Verification

- PASS: adapted skills exist in active directory, have valid frontmatter, and include Windows-safe workflow and stop gates.
- FAIL: missing source, duplicate conflict, old WSL/OpenClaw commands remain executable by default, or no verification route exists.

