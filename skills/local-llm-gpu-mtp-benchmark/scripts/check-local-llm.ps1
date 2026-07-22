$ErrorActionPreference = "Continue"

Write-Output "== llama-server processes =="
Get-CimInstance Win32_Process |
    Where-Object { $_.Name -eq "llama-server.exe" } |
    Select-Object ProcessId,Name,CommandLine

Write-Output "== models endpoint =="
try {
    Invoke-RestMethod -Uri "http://127.0.0.1:1234/v1/models" -TimeoutSec 5 |
        ConvertTo-Json -Depth 8
} catch {
    Write-Output "MODELS_ENDPOINT_FAILED: $($_.Exception.Message)"
}

Write-Output "== nvidia-smi =="
nvidia-smi --query-gpu=name,memory.total,memory.used,memory.free,utilization.gpu,power.draw,power.limit --format=csv,noheader
