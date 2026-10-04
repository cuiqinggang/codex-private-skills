param(
  [string]$BridgeWorkDir,
  [string]$TaskFile
)
$ErrorActionPreference='Stop'
$e='C:\actions-runner-etal\_local-tools\ltmvh-v070-r1\LTMVH-V070-R1-REALITY-20261004.json'
$deadline=(Get-Date).AddMinutes(5)
while((Get-Date)-lt $deadline -and -not (Test-Path -LiteralPath $e)){
  Start-Sleep -Seconds 2
}
if(Test-Path -LiteralPath $e){
  Write-Output 'R1_EVIDENCE_FOUND=YES'
  Get-Content -LiteralPath $e -Raw
  exit 0
}
Write-Output 'R1_EVIDENCE_FOUND=NO'
Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'node.exe' -and $_.CommandLine -like '*ltmvh-v070-r1-raw-benchmark.js*' } | Select-Object ProcessId,ParentProcessId,CommandLine | ConvertTo-Json -Depth 4
exit 2
