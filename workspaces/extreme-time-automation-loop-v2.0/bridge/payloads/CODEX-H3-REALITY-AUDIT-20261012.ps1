param([string]$BridgeWorkDir,[string]$TaskFile)
$ErrorActionPreference='Stop'
$root='C:\AI\MiniMax-H3\projects\CODEX_H3_REALITY_TEST_01_20261012'
Write-Output ('AUDIT_UTC='+[DateTimeOffset]::UtcNow.ToString('o'))
Write-Output ('AUDIT_MACHINE='+$env:COMPUTERNAME+' USER='+[Environment]::UserName)
Write-Output ('PROJECT_EXISTS='+(Test-Path -LiteralPath $root))
if(-not (Test-Path -LiteralPath $root)){exit 0}
$files=@(Get-ChildItem -LiteralPath $root -Recurse -File -ErrorAction SilentlyContinue)
Write-Output ('FILE_COUNT='+$files.Count)
foreach($f in $files | Sort-Object FullName){
 $relative=$f.FullName.Substring($root.Length).TrimStart('\')
 if($f.Length -gt 0 -and $f.Length -lt 50000000 -and $f.Extension -in '.png','.mp4'){
   $hash=(Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256).Hash
 }else{$hash='SKIP'}
 Write-Output ('FILE='+$relative+' | BYTES='+$f.Length+' | SHA256='+$hash)
}
$pics=@(Get-ChildItem -LiteralPath (Join-Path $root 'images') -Filter '*.png' -File -ErrorAction SilentlyContinue)
Write-Output ('IMAGES_PRESENT='+$pics.Count)
$video=Join-Path $root 'final_video.mp4'
Write-Output ('H3_VIDEO_PRESENT='+(Test-Path -LiteralPath $video))
foreach($port in @(8188,8193)){
 try{$r=Invoke-WebRequest -UseBasicParsing -TimeoutSec 4 -Uri ('http://127.0.0.1:'+$port+'/system_stats');Write-Output ('PORT_'+$port+'_HTTP='+$r.StatusCode)}
 catch{Write-Output ('PORT_'+$port+'_OFFLINE='+$_.Exception.GetType().Name)}
}
Get-CimInstance Win32_Process -Filter "Name='codex.exe'" -ErrorAction SilentlyContinue |
 Where-Object { $_.CommandLine -match 'CODEX_H3_REALITY_TEST_01_20261012' } |
 ForEach-Object {Write-Output ('CODEX_PROCESS='+$_.ProcessId+' START='+$_.CreationDate)}
Write-Output 'AUDIT_COMPLETED_READ_ONLY'
exit 0
