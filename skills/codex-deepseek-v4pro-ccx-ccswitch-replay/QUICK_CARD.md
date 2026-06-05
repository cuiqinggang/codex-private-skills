# Quick Card

## Normal Use

Use Codex normally with GPT-5.5. Do not change the default `model = "gpt-5.5"`.

## When To Use DeepSeek V4 Pro

Use DeepSeek V4 Pro only when GPT/Codex quota is insufficient and the user explicitly wants the manual backup route.

## Preflight

Check:

- CCX is running.
- `http://localhost:13000/v1` is reachable.
- CC Switch provider exists.
- Provider name is `DeepSeek-V4Pro-Backup-via-CCX`.
- Only `deepseek-v4-pro` is configured for the backup provider.
- No DeepSeek Flash provider is configured.

## Stop Spending

- Stop CCX.
- Or disable/remove the CC Switch backup provider.
- Stop using Codex `Enter API key` backup route.

## Do Not

- Do not change `model = "gpt-5.5"`.
- Do not occupy or stop anything on port `3000`.
- Do not configure DeepSeek Flash.
- Do not put the DeepSeek key in reports, logs, docs, or skill files.
