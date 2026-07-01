# Live Smoke And Recovery

Use this reference when model/provider verification must be real, not only config-based.

## Confirmed Live Route

The mature route uses OpenRouter through Cursor/Kilo:

| Role | Exact OpenRouter id | Status |
|---|---|---|
| Main executor | `deepseek/deepseek-v4-pro` | live-call verified |
| Light executor | `deepseek/deepseek-v4-flash` | live-call verified |
| Strong controller | `z-ai/glm-5.2` | live-call verified |
| Vision primary | `qwen/qwen3-vl-235b-a22b-instruct` | live-call verified |

Latest known evidence package:

- `C:\Users\A\Desktop\391.zip`
- `C:\Users\A\Desktop\ClaudeCode_Outputs\Mature_AI_Coding_SuperTool_Ecosystem_Station_Full_Deploy_Run\evidence\openrouter_live_model_smoke_verification.json`
- `C:\Users\A\Desktop\ClaudeCode_Outputs\Mature_AI_Coding_SuperTool_Ecosystem_Station_Full_Deploy_Run\reports\OpenRouter_Live_Model_Smoke_Verification_Report.md`

## Run Live Smoke

Use the bundled script:

```powershell
$env:OPENROUTER_API_KEY='<process-only key>'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Users\A\.codex\skills\cursor-kilo-supertool-mature-stack\scripts\run_openrouter_live_model_smoke.ps1"
Remove-Item Env:\OPENROUTER_API_KEY -ErrorAction SilentlyContinue
```

Safety rules:

- Never print the key.
- Do not write the key to User or Machine environment variables.
- Do not include the key in reports, ZIPs, logs, command transcripts, or screenshots.
- Run a key-pattern scan after the live call.

## Acceptance

Only set `live_call_verified=true` when the provider returns a non-empty assistant text response. A provider response id alone is useful evidence but is not a completed live call.

Use these evidence flags:

- `active_config_confirmed`
- `local_report_confirmed`
- `user_decision_confirmed`
- `provider_catalog_confirmed`
- `live_call_verified`

Do not set `live_call_verified=true` from config, local reports, user decision, or provider catalog alone.

## Retry Pattern

Some reasoning or controller models may return an empty `content` field for one prompt while still returning a provider response id. Retry with small plain-text prompts:

1. `Say OK.`
2. `Return exactly LIVE_OK for <model>.`
3. `Reply with one short plain-text confirmation for <model>.`

If all retries return empty content or an error, record `PARTIAL`, not PASS.
