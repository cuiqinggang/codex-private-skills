# Verification

Do not report success until the exact marker is observed:

```text
DEEPSEEK_V4PRO_CODEX_BACKUP_OK
```

## 1. Default Model

```powershell
${REDACTED_SECRET}
[regex]::Match($c, '(?m)^\s*model\s*=\s*"([^"]+)"').Groups[1].Value
```

Expected: `gpt-5.5`.

## 2. Superpowers

```powershell
${REDACTED_SECRET}
```

Expected: match exists.

## 3. No Flash In Default Config

```powershell
${REDACTED_SECRET}
```

Expected: no match.

## 4. CCX Health

```powershell
Invoke-RestMethod -Uri "http://localhost:13000/health"
```

Expected: status is healthy.

## 5. CCX Responses

Run:

```powershell
${REDACTED_SECRET}
```

Expected: `DEEPSEEK_V4PRO_CODEX_BACKUP_OK`.

## 6. Codex Temporary Provider

Use a temporary provider override, not default config. Set the proxy key only in the current process:

```powershell
$env:OPENAI_API_KEY = "<CCX_PROXY_ACCESS_KEY>"
codex exec `
  -c 'model_provider="ccx-deepseek-v4pro-backup"' `
  -c 'model="deepseek-v4-pro"' `
  -c 'model_reasoning_effort="high"' `
  -c 'disable_response_storage=true' `
  -c 'model_providers.ccx-deepseek-v4pro-backup.name="DeepSeek-V4Pro-Backup-via-CCX"' `
  -c 'model_providers.ccx-deepseek-v4pro-backup.base_url="http://localhost:13000/v1"' `
  -c 'model_providers.ccx-deepseek-v4pro-backup.wire_api="responses"' `
  -c 'model_providers.ccx-deepseek-v4pro-backup.env_key="OPENAI_API_KEY"' `
  -c 'model_providers.ccx-deepseek-v4pro-backup.requires_openai_auth=false' `
  --ephemeral `
  --ignore-rules `
  -s read-only `
${REDACTED_SECRET}
  "Reply exactly: DEEPSEEK_V4PRO_CODEX_BACKUP_OK"
Remove-Item Env:\OPENAI_API_KEY -ErrorAction SilentlyContinue
```

Expected: exit code `0` and exact marker.

