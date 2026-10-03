param([string]$BridgeWorkDir,[string]$TaskFile)
$ErrorActionPreference='Stop'
$names=@('Hermes8642SilentHealthCheck','HermesGatewayWatchdog_Logon','HermesNewApiAutoRecover_Logon','Hermes_Gateway','Hermes_OpenWebUI_AutoStart')
$rows=@(foreach($n in $names){$t=Get-ScheduledTask -TaskName $n -ErrorAction SilentlyContinue;if($t){[pscustomobject]@{name=$n;enabled=$t.Settings.Enabled;state=[string]$t.State}}})
$ports=@(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object {$_.LocalPort -in 8642,3000} | Select-Object LocalAddress,LocalPort,OwningProcess)
$e=[ordered]@{time=(Get-Date).ToString('o');tasks=$rows;ports=$ports;startup_exists=(Test-Path -LiteralPath 'C:\Users\A\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\HermesOpenWebUIAutoOpen.vbs')}
$e | ConvertTo-Json -Depth 6 -Compress | Write-Output
