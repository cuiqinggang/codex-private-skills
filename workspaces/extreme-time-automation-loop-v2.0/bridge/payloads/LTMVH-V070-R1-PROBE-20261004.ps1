param(
  [string]$BridgeWorkDir,
  [string]$TaskFile
)
$ErrorActionPreference='Continue'
Write-Output ('IDENTITY=' + [Security.Principal.WindowsIdentity]::GetCurrent().Name)
Write-Output ('NOW=' + (Get-Date).ToString('o'))
Write-Output '---CDP---'
try {
  $v=Invoke-RestMethod -Uri 'http://127.0.0.1:9223/json/version' -TimeoutSec 5
  $v | ConvertTo-Json -Depth 8
  $list=Invoke-RestMethod -Uri 'http://127.0.0.1:9223/json/list' -TimeoutSec 5
  $list | Select-Object id,type,title,url,webSocketDebuggerUrl | ConvertTo-Json -Depth 8
} catch { Write-Output ('CDP_ERROR=' + $_.Exception.Message) }
Write-Output '---NODE---'
try { node --version } catch { Write-Output ('NODE_ERROR=' + $_.Exception.Message) }
Write-Output '---PLAYWRIGHT_CANDIDATES---'
$roots=@('C:\AI','C:\actions-runner-etal')
foreach($root in $roots){
  if(Test-Path -LiteralPath $root){
    Get-ChildItem -LiteralPath $root -Recurse -File -ErrorAction SilentlyContinue |
      Where-Object { $_.Name -in @('package.json','chatgpt-existing-cdp.js','chatgpt-continuity-runtime.js') } |
      Select-Object -First 80 FullName | ForEach-Object { $_.FullName }
  }
}
Write-Output '---CHROME_PROCS---'
Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |
  Where-Object { $_.Name -match 'chrome|msedge' -and $_.CommandLine -match '9223|shared-mcp' } |
  Select-Object ProcessId,ParentProcessId,Name,CommandLine |
  ConvertTo-Json -Depth 4
exit 0
