# Preserve Before Uninstall

Goal: protect skills before any Codex cleanup.

## Inputs

- Current Codex skills: `C:\Users\A\.codex\skills`
- Current Agents skills: `C:\Users\A\.agents\skills`
- Backup root: `H:\Codex_Reinstall_Skill_Backup_YYYYMMDD`

## Steps

1. Check whether `.codex\skills`, `.agents\skills`, `config.toml`, `auth.json`, `sessions`, and `session_index.jsonl` exist.
2. Create the H-drive backup root.
3. Copy `.codex\skills` to `codex-skills`.
4. Copy `.agents\skills` to `agents-skills`.
5. Generate `copy-log.tsv`.
6. Generate `codex-reinstall-machine-readable-index.md`.
7. Generate `codex-desktop-reinstall-preservation-notes.md`.
8. Compare source and backup skill counts.

Sensitive files such as `auth.json` are existence-checked only unless the user explicitly asks for a separate secure copy.

## Acceptance

- Backup directories exist.
- Skill counts match or mismatches are explained.
- Report lists executed and skipped actions.
- Deletion has not started.
