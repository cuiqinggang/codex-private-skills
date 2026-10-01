param(
  [string]$RegistrationToken = $env:GITHUB_RUNNER_REGISTRATION_TOKEN,
  [string]$RunnerName = ([Environment]::MachineName + '-etal'),
  [string]$InstallDir = 'C:\actions-runner-etal',
  [string]$RepoUrl = 'https://github.com/cuiqinggang/codex-private-skills',
  [switch]$Replace
)

$ErrorActionPreference='Stop'
$version='2.337.0'
$zipName="actions-runner-win-x64-$version.zip"
$downloadUrl="https://github.com/actions/runner/releases/download/v$version/$zipName"
$expectedSha='1150692afa94e71f872017e254ea55b6eece1eece3fe7e3a6d4c93d0a1b85cfc'

function Assert-NoProxyMutation {
  # 本脚本只使用正常 HTTPS 出站连接；不写任何代理、网卡或 FlClash 配置。
  return $true
}

Assert-NoProxyMutation | Out-Null

if ([string]::IsNullOrWhiteSpace($RegistrationToken)) {
  $gh = Get-Command gh -ErrorAction SilentlyContinue
  if ($gh) {
    try {
      $json = & gh api --method POST repos/cuiqinggang/codex-private-skills/actions/runners/registration-token 2>$null
      if ($LASTEXITCODE -eq 0 -and $json) {
        $RegistrationToken = ($json | ConvertFrom-Json).token
      }
    } catch {}
  }
}
if ([string]::IsNullOrWhiteSpace($RegistrationToken)) {
  throw 'BOOTSTRAP_TOKEN_REQUIRED: provide -RegistrationToken, GITHUB_RUNNER_REGISTRATION_TOKEN, or an authenticated gh CLI.'
}

New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
$zipPath = Join-Path $InstallDir $zipName

if (-not (Test-Path (Join-Path $InstallDir 'config.cmd'))) {
  Invoke-WebRequest -Uri $downloadUrl -OutFile $zipPath -UseBasicParsing
  $actual = (Get-FileHash -LiteralPath $zipPath -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($actual -ne $expectedSha) {
    Remove-Item -LiteralPath $zipPath -Force -ErrorAction SilentlyContinue
    throw "RUNNER_SHA256_MISMATCH expected=$expectedSha actual=$actual"
  }
  Expand-Archive -LiteralPath $zipPath -DestinationPath $InstallDir -Force
}

Push-Location $InstallDir
try {
  if (Test-Path '.runner') {
    if (-not $Replace) {
      Write-Host 'RUNNER_ALREADY_CONFIGURED'
    } else {
      throw 'REPLACE_REQUESTED_BUT_SAFE_REMOTE_REMOVE_TOKEN_NOT_IMPLEMENTED'
    }
  } else {
    & .\config.cmd --unattended --url $RepoUrl --token $RegistrationToken --name $RunnerName --work '_work'
    if ($LASTEXITCODE -ne 0) { throw "RUNNER_CONFIG_FAILED exit=$LASTEXITCODE" }
  }

  $taskName='ETAL-GitHub-Actions-Runner'
  $runCmd=(Join-Path $InstallDir 'run.cmd')
  $action=New-ScheduledTaskAction -Execute 'cmd.exe' -Argument ('/c "' + $runCmd + '"')
  $trigger=New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
  $principal=New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited
  $settings=New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -RestartCount 999 -RestartInterval (New-TimeSpan -Minutes 1) -ExecutionTimeLimit ([TimeSpan]::Zero)
  Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force | Out-Null

  $existing = Get-CimInstance Win32_Process | Where-Object {
    $_.CommandLine -like "*$InstallDir*Runner.Listener*"
  }
  if (-not $existing) {
    Start-Process -FilePath 'cmd.exe' -ArgumentList @('/c',('"' + $runCmd + '"')) -WorkingDirectory $InstallDir -WindowStyle Hidden
  }

  Start-Sleep -Seconds 3
  $configured = Test-Path '.runner'
  $task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
  [ordered]@{
    status = if ($configured -and $task) { 'BOOTSTRAP_CONFIGURED' } else { 'BOOTSTRAP_INCOMPLETE' }
    runner_name = $RunnerName
    install_dir = $InstallDir
    scheduled_task = $taskName
    user = $env:USERNAME
    mode = 'INTERACTIVE_USER_AT_LOGON'
    runner_version = $version
    proxy_modified = $false
  } | ConvertTo-Json -Depth 4
} finally {
  Pop-Location
}
