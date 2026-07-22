param(
    [ValidateSet("Kilo", "Fast")]
    [string]$Mode = "Kilo"
)

$ErrorActionPreference = "Stop"

${REDACTED_SECRET}
${REDACTED_SECRET}

if (-not (Test-Path -LiteralPath $Exe)) {
    throw "llama-server.exe not found: $Exe"
}
if (-not (Test-Path -LiteralPath $Model)) {
    throw "model not found: $Model"
}

$existing = Get-CimInstance Win32_Process | Where-Object {
    $_.Name -eq "llama-server.exe" -and $_.CommandLine -like "*127.0.0.1*1234*"
}
if ($existing) {
    $existing | Select-Object ProcessId,Name,CommandLine
    Write-Output "LOCAL_LLM_ALREADY_RUNNING"
    exit 0
}

$ctxSize = if ($Mode -eq "Fast") { "4096" } else { "24576" }
$cacheType = if ($Mode -eq "Fast") { "f16" } else { "q4_0" }
$ub = if ($Mode -eq "Fast") { "1024" } else { "512" }

$args = @(
    "-m", $Model,
    "--host", "127.0.0.1",
    "--port", "1234",
    "--ctx-size", $ctxSize,
    "--gpu-layers", "all",
    "--main-gpu", "0",
    "--flash-attn", "on",
    "--cache-type-k", $cacheType,
    "--cache-type-v", $cacheType,
    "--jinja",
    "--reasoning", "off",
    "--no-warmup",
    "-np", "1",
    "-b", "2048",
    "-ub", $ub,
    "--alias", "qwen3.6-27b-iq4-xs-mtp",
    "--spec-type", "draft-mtp",
    "--spec-default",
    "--spec-draft-p-min", "0.5"
)

$proc = Start-Process -FilePath $Exe -ArgumentList $args -WindowStyle Hidden -PassThru
Write-Output "STARTED llama-server.exe PID=$($proc.Id)"

for ($i = 0; $i -lt 90; $i++) {
    try {
        $models = Invoke-RestMethod -Uri "http://127.0.0.1:1234/v1/models" -TimeoutSec 3
        $models | ConvertTo-Json -Depth 8
        Write-Output "LOCAL_LLM_READY"
        exit 0
    } catch {
        Start-Sleep -Seconds 2
    }
}

throw "LOCAL_LLM_NOT_READY_AFTER_TIMEOUT"
