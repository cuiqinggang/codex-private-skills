param([string]$BridgeWorkDir,[string]$TaskFile)
$ErrorActionPreference='Stop'
Write-Output 'REAL_WINDOWS_PROBE_START'
$root='C:\AI\GPT-Windows-Bridge-B'
$entry=Join-Path $root 'mcp\node_modules\@wonderwhy-er\desktop-commander\dist\index.js'
$tunnelDir=Join-Path $root 'tunnel\v0.0.16'
$exe=Get-ChildItem -LiteralPath $tunnelDir -Recurse -File -Filter 'tunnel-client.exe' -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName
$node=Get-Command node.exe -ErrorAction SilentlyContinue
$desktop=Join-Path ([Environment]::GetFolderPath('Desktop')) 'tunnel-client-v0.0.16-windows-amd64\tunnel-client.exe'
$procs=@(Get-CimInstance Win32_Process -ErrorAction SilentlyContinue | Where-Object { $_.Name -in @('tunnel-client.exe','tunnel-client-runtime.exe','node.exe','Runner.Listener.exe','pwsh.exe','powershell.exe') } | Select-Object Name,ProcessId,SessionId,ExecutablePath)
$tcp=@(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object { $_.LocalPort -in @(55999,56000,7890) } | Select-Object LocalAddress,LocalPort,OwningProcess)
$ready=$null
try { $w=Invoke-WebRequest -Uri 'http://127.0.0.1:56000/readyz' -UseBasicParsing -TimeoutSec 4; $ready=[ordered]@{code=[int]$w.StatusCode;body=([string]$w.Content).Trim()} }
catch { $ready=[ordered]@{code=0;reason=$_.Exception.GetType().Name} }
$version=''
if($exe){$version=((& $exe --version 2>&1) | Out-String).Trim()}
$profileExample=''
if($exe){$profileExample=((& $exe profiles samples show sample_mcp_stdio_local 2>&1) | Out-String);if($profileExample.Length -gt 2800){$profileExample=$profileExample.Substring(0,2800)}}
$report=[ordered]@{
 task='OPENAI-TUNNEL-WIN32-REAL-INSPECT-20261012'
 timestamp_utc=(Get-Date).ToUniversalTime().ToString('o')
 device=$env:COMPUTERNAME
 runner=$env:RUNNER_NAME
 current_user=[Security.Principal.WindowsIdentity]::GetCurrent().Name
 node_path=$node.Source
 mcp_entry_path=$entry
 mcp_entry_exists=(Test-Path -LiteralPath $entry)
 official_tunnel_exe_path=$exe
 desktop_exe_exists=(Test-Path -LiteralPath $desktop)
 official_cli_version=$version
 observed_processes=$procs
 current_listeners=$tcp
 existing_demo_ready=$ready
 stdio_profile_sample=$profileExample
 secrets_read=$false
 existing_processes_modified=$false
 flclash_modified=$false
 github_runner_modified=$false
}
$json=$report|ConvertTo-Json -Depth 7
Write-Output $json
Write-Output 'REAL_WINDOWS_PROBE_COMPLETE'
if(-not $report.mcp_entry_exists -or -not $exe -or -not $node){throw 'LOCAL_STAGE_MISSING'}
