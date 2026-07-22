# Codex DeepSeek V4 Pro Backup Skill

This skill packages the 2026-05-14 successful replay path for using DeepSeek V4 Pro as a manual backup model route for Windows Codex Desktop.

It does not replace the default GPT route. The default Codex config must continue to use:

```toml
model = "gpt-5.5"
```

## Proven Route

DeepSeek official API -> CCX/API Proxy -> `http://localhost:13000/v1` -> CC Switch provider -> Codex API-key provider -> `deepseek-v4-pro`.

## Key Files

- `SKILL.md`: trigger and core rules.
- `QUICK_CARD.md`: one-page operator card.
- `references/success-case-20260514.md`: known-good evidence.
- `references/replay-checklist.md`: gated replay steps.
- `references/rollback.md`: rollback path.
- `references/verification.md`: minimum checks.
- `references/no-secret-policy.md`: key handling rules.
- `references/troubleshooting.md`: known failures and fixes.
- `scripts/check-current-state.ps1`: read-only check.
- `scripts/verify-deepseek-v4pro-backup.ps1`: route verification.

## Non-Negotiables

- Do not set DeepSeek as default.
- Do not configure DeepSeek Flash.
- Do not occupy port `3000`.
- Do not print or store DeepSeek API keys in reports or docs.
- Do not claim success without `DEEPSEEK_V4PRO_CODEX_BACKUP_OK`.

