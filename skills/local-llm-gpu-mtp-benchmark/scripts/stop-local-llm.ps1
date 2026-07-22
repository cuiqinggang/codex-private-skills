$ErrorActionPreference = "Stop"

$procs = Get-CimInstance Win32_Process | Where-Object { $_.Name -eq "llama-server.exe" }
if (-not $procs) {
    Write-Output "NO_LOCAL_LLM_PROCESS"
    exit 0
}

foreach ($p in $procs) {
    Stop-Process -Id $p.ProcessId -Force
    Write-Output "STOPPED PID=$($p.ProcessId)"
}
