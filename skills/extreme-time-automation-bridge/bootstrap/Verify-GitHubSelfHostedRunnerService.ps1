param(
  [string]$InstallDir = 'C:\actions-runner-etal',
  [string]$RepoFullName = 'cuiqinggang/codex-private-skills',
  [string]$RunnerName = ([Environment]::MachineName + '-etal')
)

$ErrorActionPreference='Stop'

$services=@(Get-CimInstance Win32_Service | Where-Object {
  ($_.Name -like 'actions.runner.*' -or $_.DisplayName -like 'GitHub Actions Runner*') -and
  ($_.PathName -like "*$InstallDir*" -or $_.Name -like "*$RunnerName*" -or $_.DisplayName -like "*$RunnerName*")
})
if ($services.Count -ne 1) {
  throw "RUNNER_SERVICE_NOT_UNIQUE count=$($services.Count)"
}

$api=& gh api "repos/$RepoFullName/actions/runners?per_page=100"
if ($LASTEXITCODE -ne 0) { throw 'RUNNER_API_READ_FAILED' }
$r=($api | ConvertFrom-Json).runners | Where-Object { $_.name -eq $RunnerName } | Select-Object -First 1
if (-not $r) { throw 'RUNNER_NOT_REGISTERED' }

[ordered]@{
  service_name=$services[0].Name
  service_state=$services[0].State
  service_start_mode=$services[0].StartMode
  runner_name=$r.name
  runner_status=$r.status
  runner_busy=$r.busy
  labels=@($r.labels | ForEach-Object { $_.name })
  ready=($services[0].State -eq 'Running' -and $r.status -eq 'online')
} | ConvertTo-Json -Depth 5
