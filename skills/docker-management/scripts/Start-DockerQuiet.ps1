[CmdletBinding()]
param([ValidateSet('Audit','Start')][string]$Mode='Start',[int]$ReadyTimeoutSeconds=180)
$ErrorActionPreference='Stop'
$root='C:\AI\Docker-Autostart-20261024'
[IO.Directory]::CreateDirectory($root) | Out-Null
$utf8=New-Object Text.UTF8Encoding($false)
$processEnvBefore=[string]$env:ProgramData
# Repair only this launcher and its children. Never change global networking or credentials.
$common=[Environment]::GetFolderPath('CommonApplicationData')
if($common -ne 'C:\ProgramData' -or !(Test-Path -LiteralPath $common)){throw 'Unexpected CommonApplicationData'}
$env:ProgramData=$common
$env:ALLUSERSPROFILE=$common
if(!$env:COMPUTERNAME){$env:COMPUTERNAME=[Environment]::MachineName}
if(!$env:SystemRoot){$env:SystemRoot=[Environment]::GetFolderPath('Windows')}
if(!$env:WINDIR){$env:WINDIR=$env:SystemRoot}
$docker='C:\Program Files\Docker\Docker\resources\bin\docker.exe'
$desktop='C:\Program Files\Docker\Docker\Docker Desktop.exe'
if(!(Test-Path -LiteralPath $docker) -or !(Test-Path -LiteralPath $desktop)){throw 'Docker installation missing'}
function Test-Engine {
 $si=New-Object Diagnostics.ProcessStartInfo
 $si.FileName=$docker
 $si.Arguments='info --format "{{.ServerVersion}}"'
 $si.UseShellExecute=$false
 $si.CreateNoWindow=$true
 $si.RedirectStandardOutput=$true
 $si.RedirectStandardError=$true
 $p=New-Object Diagnostics.Process
 $p.StartInfo=$si
 try{
  [void]$p.Start()
  $out=$p.StandardOutput.ReadToEndAsync()
  $err=$p.StandardError.ReadToEndAsync()
  if(!$p.WaitForExit(5000)){try{$p.Kill()}catch{};return $false}
  $ok=$p.ExitCode -eq 0 -and $out.Result.Trim() -match '^\d+\.\d+'
  return $ok
 }finally{$p.Dispose()}
}
function Save-Receipt([string]$status,[string]$action){
 $r=[ordered]@{time=(Get-Date).ToString('o');mode=$Mode;status=$status;action=$action;programDataBefore=$processEnvBefore;programData=$env:ProgramData;computerName=$env:COMPUTERNAME;pid=$PID}
 $json=$r|ConvertTo-Json
 $tmp=Join-Path $root ('status.'+$PID+'.tmp')
 [IO.File]::WriteAllText($tmp,$json,$utf8)
 Move-Item -LiteralPath $tmp -Destination (Join-Path $root 'status.json') -Force
 [IO.File]::AppendAllText((Join-Path $root 'startup.jsonl'),($r|ConvertTo-Json -Compress)+[Environment]::NewLine,$utf8)
 $json
}
if($Mode -eq 'Audit'){Save-Receipt 'AUDIT_PASS' 'NO_START';exit 0}
if(Test-Engine){Save-Receipt 'ENGINE_READY' 'ALREADY_READY_NO_RESTART';exit 0}
$running=@(Get-Process -Name 'com.docker.backend','Docker Desktop' -ErrorAction SilentlyContinue)
$action='WAIT_EXISTING_NO_DUPLICATE'
if($running.Count -eq 0){
 Start-Process -FilePath $desktop -ArgumentList '-AutoStart' -WindowStyle Hidden | Out-Null
 $action='OFFICIAL_AUTOSTART_REQUESTED'
}
$until=(Get-Date).AddSeconds($ReadyTimeoutSeconds)
while((Get-Date) -lt $until){
 if(Test-Engine){Save-Receipt 'ENGINE_READY' $action;exit 0}
 Start-Sleep -Seconds 3
}
Save-Receipt 'ENGINE_NOT_READY_REQUIRES_DIAGNOSIS' $action
# Never reset Docker, terminate WSL, kill business containers, or auto-relaunch a wedged backend.
exit 1
