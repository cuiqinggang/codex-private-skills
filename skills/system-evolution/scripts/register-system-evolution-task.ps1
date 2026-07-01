param(
  [ValidateSet('Approval','Auto','ReportOnly')]
  [string]$Mode = 'Approval',
  [int]$MinHoursBetweenRuns = 24,
  [int]$RandomDelayHours = 8,
  [string]$DailyAt = '10:00'
)

$ErrorActionPreference = 'Stop'
$TaskName = 'Codex_SystemEvolution_2h'
$Runner = 'C:\Users\A\.codex\skills\system-evolution\scripts\run-system-evolution.ps1'
if (-not (Test-Path $Runner)) { throw "Runner missing: $Runner" }

$user = [System.Security.Principal.WindowsIdentity]::GetCurrent()
$sid = $user.User.Value
$startBoundary = (Get-Date -Date $DailyAt).ToString("yyyy-MM-dd'T'HH:mm:sszzz")
$randomDelay = [System.Xml.XmlConvert]::ToString((New-TimeSpan -Hours $RandomDelayHours))
$arguments = "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$Runner`" -Mode $Mode -MinHoursBetweenRuns $MinHoursBetweenRuns"

$xml = @"
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.3" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>System evolution report runner. Historical task name kept; daily randomized trigger plus logon catch-up; runner enforces a 24-hour cooldown.</Description>
    <URI>\$TaskName</URI>
  </RegistrationInfo>
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>$startBoundary</StartBoundary>
      <Enabled>true</Enabled>
      <RandomDelay>$randomDelay</RandomDelay>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
    <LogonTrigger>
      <Enabled>true</Enabled>
      <Delay>PT2M</Delay>
    </LogonTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>$sid</UserId>
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT72H</ExecutionTimeLimit>
    <Priority>7</Priority>
    <UseUnifiedSchedulingEngine>true</UseUnifiedSchedulingEngine>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>powershell.exe</Command>
      <Arguments>$([System.Security.SecurityElement]::Escape($arguments))</Arguments>
    </Exec>
  </Actions>
</Task>
"@

$taskXmlPath = Join-Path $env:TEMP "$TaskName.xml"
[System.IO.File]::WriteAllText($taskXmlPath, $xml, [System.Text.Encoding]::Unicode)

$oldErrorActionPreference = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
$output = & schtasks.exe /Create /TN $TaskName /XML $taskXmlPath /F 2>&1
$exit = $LASTEXITCODE
$ErrorActionPreference = $oldErrorActionPreference
Remove-Item -LiteralPath $taskXmlPath -Force -ErrorAction SilentlyContinue
if ($exit -ne 0) {
  $startupDir = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\Startup'
  $startupScript = Join-Path $startupDir 'Codex_SystemEvolution_24h.vbs'
  New-Item -ItemType Directory -Force -Path $startupDir | Out-Null
  $startupContent = 'Set shell = CreateObject("WScript.Shell")' + "`r`n" +
    'shell.Run "powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File ""C:\Users\A\.codex\skills\system-evolution\scripts\run-system-evolution.ps1"" -Mode Approval -MinHoursBetweenRuns 24", 0, False' + "`r`n"
  [System.IO.File]::WriteAllText($startupScript, $startupContent, [System.Text.Encoding]::ASCII)
  Write-Output "SCHEDULED_TASK_UPDATE_SKIPPED $TaskName Reason=$($output | Out-String)"
  Write-Output "STARTUP_FALLBACK_REGISTERED $startupScript"
  exit 0
}

Write-Output "REGISTERED $TaskName Mode=$Mode MinHoursBetweenRuns=$MinHoursBetweenRuns DailyAt=$DailyAt RandomDelayHours=$RandomDelayHours LogonTrigger=True"
