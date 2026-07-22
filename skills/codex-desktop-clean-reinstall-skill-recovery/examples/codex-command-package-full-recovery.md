# Copy-Paste Command Package For Future Recovery

Use this prompt in a future Codex session when the same class of problem returns.

```text
Use the skill `codex-desktop-clean-reinstall-skill-recovery`.

Goal:
Safely preserve Codex skills, clean old Codex/Codex++ state, reinstall official Codex, run a read-only post-reinstall check, then restore only non-conflicting skills.

Rules:
${REDACTED_SECRET}
- Do not copy `auth.json` unless I explicitly ask.
- Do not overwrite the new official `.codex`.
- Never overwrite `.system`.
- Agents skills must be diffed before overwrite.
- Do not delete `.codex`, `.agents`, Codex++ folders, registry entries, or shortcuts until you show the list and I explicitly confirm.
- Use official Store/winget install only: `winget install Codex -s msstore`.
- If Store stalls, repair Store first; do not use third-party installers.

Execute:
1. Run the preserve-before-uninstall script and write a report.
2. Give me the deletion/cleanup plan and wait for confirmation.
3. After I confirm, clean old state and verify.
4. Reinstall official Codex through the official channel.
5. Run read-only post-reinstall check.
6. Give me the restore plan and wait for confirmation.
7. Restore non-conflicting Codex skills only.
8. Diff Agents skills only.
9. Write final acceptance report.
```
