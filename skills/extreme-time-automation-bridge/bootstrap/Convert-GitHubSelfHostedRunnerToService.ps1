param(
  [string]$InstallDir = 'C:\actions-runner-etal',
  [string]$RepoFullName = 'cuiqinggang/codex-private-skills',
  [string]$RepoUrl = 'https://github.com/cuiqinggang/codex-private-skills',
  [string]$RunnerName = ($env:COMPUTERNAME + '-etal'),
  [string]$ServiceAccount = 'NT AUTHORITY\NETWORK SERVICE'
)

$ErrorActionPreference='Stop'

function Assert-Administrator {
  $id=[Security.Principal.WindowsIdentity]::GetCurrent()
  $p=New-Object Security.Principal.WindowsPrincipal($id)
  if (-not $p.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    throw 'ADMIN_REQUIRED: GitHub documents that Windows service configuration requires an elevated shell.'
  }
}

function Get-GhToken([string]$Endpoint) {
  $gh=Get-Command gh -ErrorAction Stop
  $raw=& $gh.Source api --method POST $Endpoint
  if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($raw)) {
    throw "GH_TOKEN_REQUEST_FAILED: $Endpoint"
  }
  $token=($raw | ConvertFrom-Json).token
  if ([string]::IsNullOrWhiteSpace($token)) {
    throw "GH_TOKEN_EMPTY: $Endpoint"
  }
  return $token
}

function Stop-InteractiveRunner([string]$Root) {
  $escaped=[regex]::Escape($Root)
  $procs=Get-CimInstance Win32_Process -ErrorAction SilentlyContinue | Where-Object {
    $_.Name -in @('Runner.Listener.exe','Runner.Worker.exe') -and $_.ExecutablePath -match "^$escaped"
  }
  foreach($p in $procs) {
    Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue
  }
}

function Get-RunnerService([string]$Root,[string]$Name) {
  $services=Get-CimInstance Win32_Service | Where-Object {
    ($_.Name -like 'actions.runner.*' -or $_.DisplayName -like 'GitHub Actions Runner*') -and
    ($_.PathName -like "*$Root*" -or $_.Name -like "*$Name*" -or $_.DisplayName -like "*$Name*")
  }
  return @($services)
}

function Wait-RunnerOnline([string]$Repo,[string]$Name,[int]$Seconds=45) {
  $deadline=(Get-Date).AddSeconds($Seconds)
  do {
    $json=& gh api "repos/$Repo/actions/runners?per_page=100"
    if ($LASTEXITCODE -eq 0 -and $json) {
      $r=($json | ConvertFrom-Json).runners | Where-Object { $_.name -eq $Name } | Select-Object -First 1
      if ($r -and $r.status -eq 'online') { return $r }
    }
    Start-Sleep -Seconds 3
  } while((Get-Date) -lt $deadline)
  return $null
}

Assert-Administrator

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
  throw 'GH_CLI_REQUIRED'
}
& gh auth status 1>$null 2>$null
if ($LASTEXITCODE -ne 0) { throw 'GH_AUTH_REQUIRED' }

$config=Join-Path $InstallDir 'config.cmd'
if (-not (Test-Path -LiteralPath $config)) {
  throw "RUNNER_NOT_INSTALLED: $config"
}

Stop-InteractiveRunner -Root $InstallDir
Push-Location $InstallDir
try {
  if (Test-Path '.runner') {
    $removeToken=Get-GhToken -Endpoint "repos/$RepoFullName/actions/runners/remove-token"
    try {
      & .\config.cmd remove --token $removeToken
      if ($LASTEXITCODE -ne 0) { throw "RUNNER_REMOVE_FAILED exit=$LASTEXITCODE" }
    } finally {
      $removeToken=$null
    }
  }

  $registrationToken=Get-GhToken -Endpoint "repos/$RepoFullName/actions/runners/registration-token"
  try {
    & .\config.cmd --unattended --url $RepoUrl --token $registrationToken --name $RunnerName --work '_work' --runasservice --windowslogonaccount $ServiceAccount
    if ($LASTEXITCODE -ne 0) { throw "RUNNER_SERVICE_CONFIG_FAILED exit=$LASTEXITCODE" }
  } finally {
    $registrationToken=$null
  }
} finally {
  Pop-Location
}

$svc=Get-RunnerService -Root $InstallDir -Name $RunnerName
if ($svc.Count -ne 1) {
  throw "RUNNER_SERVICE_NOT_UNIQUE count=$($svc.Count)"
}
$serviceName=$svc[0].Name
$service=Get-Service -Name $serviceName -ErrorAction Stop
if ($service.Status -ne 'Running') {
  Start-Service -Name $serviceName
  $service.WaitForStatus('Running',[TimeSpan]::FromSeconds(30))
}

$online=Wait-RunnerOnline -Repo $RepoFullName -Name $RunnerName
if (-not $online) { throw 'RUNNER_NOT_ONLINE_AFTER_SERVICE_CONFIG' }

[ordered]@{
  status='SERVICE_REALITY_READY'
  runner_name=$RunnerName
  install_dir=$InstallDir
  service_name=$serviceName
  service_status=(Get-Service -Name $serviceName).Status.ToString()
  runner_status=$online.status
  runner_busy=$online.busy
  labels=@($online.labels | ForEach-Object { $_.name })
  persistence='WINDOWS_SERVICE'
  proxy_modified=$false
} | ConvertTo-Json -Depth 5
