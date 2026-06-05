param(
    [string]$BaseUrl = "http://localhost:13000",
    [string]$CcxEnvPath = "C:\Users\A\Desktop\1\output\TASK-20260514-CODEX-DEEPSEEK-V4PRO-VIDEO-REPLAY\tools\ccx\.env",
    [switch]$RunCodexExec
)

$ErrorActionPreference = "Continue"
$marker = "DEEPSEEK_V4PRO_CODEX_BACKUP_OK"

function Fail-Layer {
    param([string]$Layer, [string]$Message)
    Write-Output ("FAIL_LAYER: {0}" -f $Layer)
    Write-Output ("DETAIL: {0}" -f $Message)
    Write-Output "SKILL_VERIFY_FAIL"
    exit 1
}

try {
    $health = Invoke-RestMethod -Uri ($BaseUrl.TrimEnd("/") + "/health") -TimeoutSec 8
} catch {
    Fail-Layer -Layer "CCX_HEALTH" -Message $_.Exception.Message
}

if (-not $health -or ($health.status -notin @("healthy", $true))) {
    Fail-Layer -Layer "CCX_HEALTH" -Message "CCX health did not report healthy."
}

$proxyKey = $env:CCX_PROXY_ACCESS_KEY
if (-not $proxyKey -and (Test-Path -LiteralPath $CcxEnvPath)) {
    $proxyKey = ((Get-Content -LiteralPath $CcxEnvPath) | Where-Object { $_ -like "PROXY_ACCESS_KEY=*" }) -replace "^PROXY_ACCESS_KEY=", ""
}

if (-not $proxyKey) {
    Fail-Layer -Layer "CCX_PROXY_KEY" -Message "Missing CCX proxy access key. Set CCX_PROXY_ACCESS_KEY or provide a CCX .env path."
}

$body = @{
    model = "deepseek-v4-pro"
    input = "Reply exactly: $marker"
    stream = $false
} | ConvertTo-Json -Compress

try {
    $response = Invoke-RestMethod `
        -Uri ($BaseUrl.TrimEnd("/") + "/v1/responses") `
        -Method Post `
        -Headers @{ Authorization = "Bearer $proxyKey"; "Content-Type" = "application/json" } `
        -Body $body `
        -TimeoutSec 120
} catch {
    $detail = if ($_.ErrorDetails.Message) { $_.ErrorDetails.Message } else { $_.Exception.Message }
    Fail-Layer -Layer "CCX_RESPONSES" -Message $detail
}

$json = $response | ConvertTo-Json -Depth 12 -Compress
if ($json -notmatch [regex]::Escape($marker)) {
    Fail-Layer -Layer "DEEPSEEK_RESPONSE" -Message "Responses call did not include the exact marker."
}

Write-Output $marker

if ($RunCodexExec) {
    $oldKey = $env:OPENAI_API_KEY
    $env:OPENAI_API_KEY = $proxyKey
    try {
        $out = & codex exec `
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
            -C "C:\Users\A\Desktop\1" `
            "Reply exactly: $marker" 2>&1
        if ($LASTEXITCODE -ne 0 -or (($out -join "`n") -notmatch [regex]::Escape($marker))) {
            Fail-Layer -Layer "CODEX_EXEC" -Message "codex exec did not return the exact marker."
        }
    } finally {
        if ($null -ne $oldKey) { $env:OPENAI_API_KEY = $oldKey } else { Remove-Item Env:\OPENAI_API_KEY -ErrorAction SilentlyContinue }
    }
}

Write-Output "SKILL_VERIFY_PASS"
exit 0
