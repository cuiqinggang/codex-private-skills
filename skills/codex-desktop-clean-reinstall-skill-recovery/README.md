# Codex Desktop Clean Reinstall Skill Recovery

This skill package preserves and restores Codex skills around a clean official Codex Desktop reinstall on Windows, especially after Codex++ / CodexPlusPlus residue or Microsoft Store install problems.

Before using it, run the backup stage and confirm the report. The package is designed around this order:

1. Preserve `.codex\skills` and `.agents\skills`.
2. Clean old Codex / Codex++ only after confirmation.
3. Reinstall official Codex through Microsoft Store or `winget`.
4. Run a read-only check of the new environment.
5. Restore only non-conflicting Codex skills and diff Agents skills.

Dangerous actions are intentionally not one-click: deleting `.codex`, deleting Codex++ install folders, deleting registry entries, overwriting skills, copying `auth.json`, and changing Store/proxy/account/environment state all require explicit confirmation.
