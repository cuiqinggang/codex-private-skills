---
name: codex-deepseek-v4pro-ccx-ccswitch-replay
description: Use this skill to restore, repair, migrate, or verify the 2026-05-14 successful Windows Codex backup route: DeepSeek V4 Pro via CCX/API Proxy on localhost:13000/v1, CC Switch Codex provider, and Codex API-key provider. Trigger when the user says "恢复 Codex DeepSeek V4 Pro 备用路线", "重新配置 Codex DeepSeek", "Codex 额度不够，切 DeepSeek V4 Pro", "复现 CCX + CC Switch 接 DeepSeek", "Codex DeepSeek V4 Pro 备用模型修复", or "按 2026-05-14 成功案例恢复".
---

# Codex DeepSeek V4 Pro Backup via CCX and CC Switch

Use this skill only to replay the proven 2026-05-14 Windows path:

DeepSeek official API -> CCX/API Proxy -> `http://localhost:13000/v1` -> CC Switch Codex provider -> Codex API-key provider -> `deepseek-v4-pro` -> `DEEPSEEK_V4PRO_CODEX_BACKUP_OK`.

## Trigger Phrases

Load this skill when the user asks:

- "恢复 Codex DeepSeek V4 Pro 备用路线"
- "重新配置 Codex DeepSeek"
- "Codex 额度不够，切 DeepSeek V4 Pro"
- "复现 CCX + CC Switch 接 DeepSeek"
- "Codex DeepSeek V4 Pro 备用模型修复"
- "按 2026-05-14 成功案例恢复"

## When To Use

- GPT/Codex quota is insufficient and the user wants a manual backup route.
- CCX needs to be reinstalled, restarted, or repaired.
- CC Switch provider needs to be recreated or verified.
- A new Windows machine needs the same backup route.
- The old backup route stopped working and needs layered diagnosis.

## When Not To Use

- Do not use this as the default daily GPT route.
- Do not replace default `model = "gpt-5.5"`.
- Do not configure or select DeepSeek Flash.
- Do not change or stop Open WebUI on port `3000`.
- Do not save, print, or report DeepSeek API keys.
- Do not point Codex directly at `https://api.deepseek.com` as the final route.

## Fixed Rules

- Default GPT-5.5 stays unchanged.
- DeepSeek V4 Pro is manual backup only.
- Only use `deepseek-v4-pro`.
- CCX uses `13000`; Open WebUI keeps `3000`.
- Backup before any config write.
- Verify before reporting success.
- If a required key, component, or compatibility layer is missing, stop with `SAFE_STOP_PASS`.
- If DeepSeek API key is needed and unavailable, output `NEED_DEEPSEEK_API_KEY` and stop.

## One-Line Recovery Strategy

First confirm the GPT default path is untouched, then start or repair CCX on `13000`, confirm the CC Switch backup provider, and test Codex with a temporary provider override; do not directly modify the default `gpt-5.5` config.

## Required References

- Read `references/success-case-20260514.md` for the known-good case.
- Read `references/replay-checklist.md` before reinstalling or repairing.
- Read `references/verification.md` before claiming success.
- Read `references/rollback.md` before changing existing config.
- Read `references/no-secret-policy.md` before handling any key.
- Read `references/troubleshooting.md` when a layer fails.

## Scripts

- `scripts/check-current-state.ps1`: read-only status check.
- `scripts/verify-deepseek-v4pro-backup.ps1`: CCX and optional Codex backup route verification.
