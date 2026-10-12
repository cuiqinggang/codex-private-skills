param([string]$BridgeWorkDir,[string]$TaskFile)
$ErrorActionPreference='Stop'
$clock=[Diagnostics.Stopwatch]::StartNew()
Write-Output 'POLSIA_GITHUB_WINDOWS_LINK_PASS'
Write-Output ('TEST_ID=POLSIA-GITHUB-WINDOWS-LINK-20261012-01')
Write-Output ('HOST='+$env:COMPUTERNAME)
Write-Output ('RUNNER='+$env:RUNNER_NAME)
Write-Output ('EXECUTION_UTC='+[DateTime]::UtcNow.ToString('o'))
Write-Output ('POLSIA_ROOT_EXISTS='+[bool](Test-Path 'C:\AI\Polsia-V5-Parallel-20261012'))
Write-Output ('CODEX_AVAILABLE='+[bool](Get-Command codex -ErrorAction SilentlyContinue))
$clock.Stop()
Write-Output ('LOCAL_PROBE_MS='+$clock.Elapsed.TotalMilliseconds.ToString('F3',[cultureinfo]::InvariantCulture))
exit 0
