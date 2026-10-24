[CmdletBinding()]
param([ValidateSet('Audit','Apply')][string]$Mode='Audit')
$ErrorActionPreference='Stop'
$root='C:\AI\Docker-Autostart-20261024'
$startup=[Environment]::GetFolderPath('Startup')
$guard='C:\Users\A\.codex\skills\powershell-reliability-guard\scripts\Invoke-GuardedPowerShell.ps1'
$target='C:\Users\A\.codex\skills\docker-management\scripts\Start-DockerQuiet.ps1'
$hostPath='C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
$entry=Join-Path $startup 'Docker-Quiet-Autostart.vbs'
$settings='C:\Users\A\AppData\Roaming\Docker\settings-store.json'
$auto=(ConvertFrom-Json ([IO.File]::ReadAllText($settings))).AutoStart
$old=@('Docker Desktop.lnk','HermesOpenWebUIAutoOpen.vbs')
$runPath='HKCU:\Software\Microsoft\Windows\CurrentVersion\Run'
$run=Get-ItemProperty -LiteralPath $runPath
$dockerRun=$run.PSObject.Properties | Where-Object {$_.Name -notmatch '^PS' -and [string]$_.Value -match 'Docker Desktop\.exe'}
if($Mode -eq 'Audit'){
 [pscustomobject]@{StartupEntry=$entry;NativeAutoStart=$auto;ExistingRun=@($dockerRun|Select-Object Name,Value);ExistingLegacyStartup=@($old|Where-Object {Test-Path -LiteralPath (Join-Path $startup $_)})}|ConvertTo-Json -Depth 4
 exit 0
}
if($auto -eq $true){throw 'Native Docker autostart is also enabled. Normalize it using Docker settings before adding a second path.'}
New-Item -ItemType Directory -Force -Path (Join-Path $root 'backup') | Out-Null
$enc=New-Object Text.UTF8Encoding($false)
foreach($name in $old){
 $p=Join-Path $startup $name
 if(Test-Path -LiteralPath $p){Move-Item -LiteralPath $p -Destination (Join-Path $root ('backup\'+$name))}
}
if(@($dockerRun).Count -gt 0){
 [IO.File]::WriteAllText((Join-Path $root 'backup\run-values.json'),(ConvertTo-Json -InputObject @($dockerRun|Select-Object Name,Value)),$enc)
 foreach($v in $dockerRun){Remove-ItemProperty -LiteralPath $runPath -Name $v.Name}
}
if(Test-Path -LiteralPath $entry){Copy-Item -LiteralPath $entry -Destination (Join-Path $root 'backup\Docker-Quiet-Autostart.vbs')}
$cmd='"'+$hostPath+'" -NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -WindowStyle Hidden -File "'+$guard+'" -Path "'+$target+'" -Target WindowsPowerShell51'
$body='Option Explicit'+[Environment]::NewLine+'WScript.Quit CreateObject("WScript.Shell").Run("'+$cmd.Replace('"','""')+'", 0, True)'
$candidate=Join-Path $root 'Docker-Quiet-Autostart.candidate.vbs'
[IO.File]::WriteAllText($candidate,$body,$enc)
Copy-Item -LiteralPath $candidate -Destination $entry -Force
if((Get-FileHash -LiteralPath $candidate).Hash -ne (Get-FileHash -LiteralPath $entry).Hash){throw 'Startup readback failed'}
[pscustomobject]@{Status='INSTALLED';StartupEntry=$entry;NativeAutoStart=$auto;Target=$target;RebootAcceptance='PENDING'}|ConvertTo-Json
exit 0
