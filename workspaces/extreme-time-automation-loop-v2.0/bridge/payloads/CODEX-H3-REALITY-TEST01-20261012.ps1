param(
  [string]$BridgeWorkDir,
  [string]$TaskFile
)
$ErrorActionPreference='Stop'
$ProgressPreference='SilentlyContinue'
$project='C:\AI\MiniMax-H3\projects\CODEX_H3_REALITY_TEST_01_20261012'
$prompt=Join-Path $project 'TASK_PROMPT.md'
$artifactRoot=Join-Path $env:RUNNER_TEMP 'etal-bridge-result'
$proof=Join-Path $artifactRoot 'reality-evidence'
New-Item -ItemType Directory -Force -Path $proof | Out-Null
Write-Output ('BRIDGE_REALITY_START='+[DateTimeOffset]::UtcNow.ToString('o'))
Write-Output ('HOST='+$env:COMPUTERNAME)
Write-Output ('RUNNER_USER='+[Environment]::UserName)
Write-Output ('PROJECT='+$project)
$utf8=New-Object System.Text.UTF8Encoding($false)
[Console]::OutputEncoding=$utf8
$OutputEncoding=$utf8
if(-not (Test-Path -LiteralPath $prompt)){
  throw ('TASK_PROMPT_MISSING='+$prompt)
}
if(-not (Test-Path -LiteralPath 'C:\AI\MiniMax-H3\ComfyUI\main.py')){
  throw 'LOCAL_H3_MAIN_MISSING'
}
if(-not (Test-Path -LiteralPath 'C:\AI\MiniMax-H3\.venv\Scripts\python.exe')){
  throw 'LOCAL_H3_PYTHON_MISSING'
}
$codex=(Get-Command codex.cmd -ErrorAction SilentlyContinue)
if(-not $codex){$codex=(Get-Command codex -ErrorAction SilentlyContinue)}
if(-not $codex){
  $absolute='C:\Users\A\AppData\Roaming\npm\codex.cmd'
  if(Test-Path -LiteralPath $absolute){ $codex=[pscustomobject]@{Source=$absolute} }
}
if(-not $codex){throw 'CODEX_COMMAND_NOT_FOUND: PATH and verified absolute path missing'}
Write-Output ('CODEX_PATH='+$codex.Source)
Write-Output ('CODEX_VERSION='+((& $codex.Source --version) -join ' '))
try{
  $r=Invoke-WebRequest -Uri 'http://127.0.0.1:8188/system_stats' -UseBasicParsing -TimeoutSec 5
  Write-Output ('COMFYUI_8188_HTTP='+$r.StatusCode)
}catch{
  Write-Output ('COMFYUI_8188_FAIL='+$_.Exception.Message)
}
try{
  $r=Invoke-WebRequest -Uri 'http://127.0.0.1:8193/system_stats' -UseBasicParsing -TimeoutSec 5
  Write-Output ('H3_8193_HTTP='+$r.StatusCode)
}catch{
  Write-Output ('H3_8193_OFFLINE='+$_.Exception.Message)
}
if(-not (Test-Path 'C:\Users\A\.codex')){throw 'CODEX_HOME_NOT_FOUND'}
$env:CODEX_HOME='C:\Users\A\.codex'
Set-Location $project
Write-Output 'CODEX_EXEC_BEGIN'
$exitCode=50
try {
  Get-Content -LiteralPath $prompt -Encoding UTF8 -Raw | & $codex.Source exec -s workspace-write --skip-git-repo-check -c model_reasoning_effort=medium -c sandbox_workspace_write.network_access=true -C $project - 2>&1 | Tee-Object -FilePath (Join-Path $project 'CODEX_ACTIONS_BRIDGE.log')
  $exitCode=$LASTEXITCODE
  Write-Output ('CODEX_EXEC_EXIT='+$exitCode)
}catch{
  Write-Output ('CODEX_EXEC_EXCEPTION='+$_.Exception.ToString())
  $exitCode=51
}finally{
  $files=Get-ChildItem -LiteralPath $project -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Extension -in '.md','.json','.txt','.log','.png','.mp4' -and $_.Length -lt 50000000 }
  foreach($f in $files){
    $relative=$f.FullName.Substring($project.Length).TrimStart('\')
    $dest=Join-Path $proof $relative
    New-Item -ItemType Directory -Force -Path (Split-Path $dest) | Out-Null
    Copy-Item -LiteralPath $f.FullName -Destination $dest -Force -ErrorAction SilentlyContinue
    Write-Output ('EVIDENCE_FILE='+$relative+';BYTES='+$f.Length)
  }
  Write-Output ('BRIDGE_REALITY_END='+[DateTimeOffset]::UtcNow.ToString('o'))
}
if($exitCode -ne 0){exit 51}
$images=@(Get-ChildItem -LiteralPath (Join-Path $project 'images') -Filter '*.png' -File -ErrorAction SilentlyContinue)
$video=Join-Path $project 'final_video.mp4'
if($images.Count -ne 8 -or -not (Test-Path -LiteralPath $video)){
  Write-Output ('NOT_FULL_DELIVERY: IMAGES='+$images.Count+' VIDEO='+[int](Test-Path -LiteralPath $video))
  exit 52
}
Write-Output 'DELIVERABLES_PRESENT_NEED_QUALITY_VERIFICATION'
exit 0
