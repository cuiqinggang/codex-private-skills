param([switch]$Once, [switch]$AudioTest, [int]$RefreshSeconds=60)
$ErrorActionPreference='Continue'
$root='C:\AI\Polsia-Unified-V4'
$lastAlarm=''
try { $Host.UI.RawUI.WindowTitle='极简故障监控｜仅查看' } catch {}
try {
  $raw=$Host.UI.RawUI
  $sz=New-Object Management.Automation.Host.Size(91,13)
  if($raw.BufferSize.Width -lt 91){$raw.BufferSize=New-Object Management.Automation.Host.Size(91,[Math]::Max(100,$raw.BufferSize.Height))}
  $raw.WindowSize=$sz
} catch {}
function Alert-Sound([string]$message) {
  $beep='NOT_VERIFIED'; $speech='NOT_VERIFIED'
  try { [Console]::Beep(970,180); [Threading.Thread]::Sleep(120); [Console]::Beep(680,280); $beep='API_INVOKED' } catch { $beep='UNAVAILABLE' }
  try {
    $text=$message.Replace("'","")
    $cmd="Add-Type -AssemblyName System.Speech; "+'$v=New-Object System.Speech.Synthesis.SpeechSynthesizer; '+ '$cn=@($v.GetInstalledVoices()|Where-Object {$_.Enabled -and $_.VoiceInfo.Culture.Name -eq "zh-CN"}); if($cn.Count -gt 0){$v.SelectVoice($cn[0].VoiceInfo.Name)}; $v.Speak('+"'"+$text+"'"+'); $v.Dispose()'
    $enc=[Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($cmd))
    $exe=Join-Path $env:WINDIR 'System32\WindowsPowerShell\v1.0\powershell.exe'
    $p=Start-Process -FilePath $exe -ArgumentList @('-NoLogo','-NoProfile','-NonInteractive','-EncodedCommand',$enc) -WindowStyle Hidden -PassThru
    if($p.WaitForExit(12000)) { if($p.ExitCode -eq 0){$speech='ENGINE_EXIT_0'}else{$speech='ENGINE_ERROR_'+$p.ExitCode} }
    else { try{$p.Kill()}catch{}; $speech='ENGINE_TIMEOUT' }
  } catch { $speech='ENGINE_UNAVAILABLE' }
  return [pscustomobject]@{beep=$beep;speech=$speech}
}
function State-CN([string]$state) {
  switch ($state) {
    'WAITING_CEO' {'等待总控审批'}
    'RUNNING' {'正在执行'}
    'ALERT' {'发现故障'}
    'READY' {'待派发'}
    'FROZEN' {'业务已冻结'}
    default {'状态待核实'}
  }
}
function Fault-CN([string]$key) {
  switch -Wildcard ($key) {
    'TEST_ONLY_INJECTED_MONITOR_FAULT' {'隔离测试故障'}
    'BRANCH_*_STALE' {'某任务长期未更新'}
    'BRANCH_*_ERROR' {'执行分支出现错误'}
    'BRANCH_*_INVALID_STATE' {'执行分支状态文件损坏'}
    'INFLIGHT_WITHOUT_ACTIVE_CODEX' {'业务标记正在执行，但未发现执行器'}
    'MOTHER_STATE_UNREADABLE' {'母任务状态文件无法读取'}
    'V008_FREEZE_HASH_MISMATCH' {'业务冻结校验失败'}
    'V008_MANIFEST_HASH_MISMATCH' {'文件清单校验失败'}
    'MONITOR_SAMPLING_STALE' {'监控采样停止更新'}
    'MONITOR_SNAPSHOT_UNREADABLE' {'监控状态不可读取'}
    default {'未知类型故障，请查看故障记录'}
  }
}
if($AudioTest) {
  $result=Alert-Sound '监控声音测试。只有出现新故障才会自动提醒。'
  $beepCN=if($result.beep -eq 'API_INVOKED'){'已发出'}else{'未成功'}
  $voiceCN=if($result.speech -eq 'ENGINE_EXIT_0'){'已完成'}else{'未成功'}
  Write-Output ('声音测试：提示音'+$beepCN+'；中文语音播报'+$voiceCN)
  return
}
while($true){
  $faults=@();$state=$null;$age=-1
  try{
    $state=Get-Content -LiteralPath (Join-Path $root 'snapshot.json') -Encoding utf8 -Raw -ErrorAction Stop | ConvertFrom-Json -ErrorAction Stop
    $age=[math]::Round(([DateTime]::UtcNow-([DateTime]$state.utc).ToUniversalTime()).TotalSeconds)
    foreach($key in @($state.alert_keys)) { if(-not [string]::IsNullOrWhiteSpace([string]$key)){$faults+= [string]$key} }
    if($age -lt 0 -or $age -gt 150){$faults+='MONITOR_SAMPLING_STALE'}
  }catch{ $faults=@('MONITOR_SNAPSHOT_UNREADABLE') }
  $faults=@($faults|Sort-Object -Unique)
  try { Clear-Host } catch {}
  Write-Host '  极简故障监控' -ForegroundColor Cyan
  Write-Host '  ------------------------------------------------------------' -ForegroundColor DarkGray
  if($null -ne $state){
    $wait=@($state.branches|Where-Object {$_.status -eq 'READY'}).Count
    $run=@($state.branches|Where-Object {$_.status -eq 'RUNNING'}).Count
    $blocked=@($state.branches|Where-Object {$_.status -eq 'BLOCKED'}).Count
    Write-Host ('  母任务：'+(State-CN ([string]$state.root_status))+'   |   保存点：'+$(if($state.freeze){'已登记'}else{'待核实'}))
    Write-Host ('  执行中：'+$run+'    待派发：'+$wait+'    已知阻塞：'+$blocked)
    Write-Host ('  最近采样：'+([DateTime]$state.utc).ToLocalTime().ToString('HH:mm:ss')+'   |   '+$age+' 秒前')
  } else { Write-Host '  监控数据读取失败。' -ForegroundColor Red }
  Write-Host ''
  if($faults.Count -gt 0){
    Write-Host ('  !!! 当前故障 '+$faults.Count+' 项') -ForegroundColor Red
    foreach($key in $faults|Select-Object -First 3){Write-Host ('      '+(Fault-CN $key)) -ForegroundColor Red}
    $fingerprint=$faults -join '|'
    if($fingerprint -ne $lastAlarm){
      $testOnly=$faults.Count -eq 1 -and $faults[0] -eq 'TEST_ONLY_INJECTED_MONITOR_FAULT'
      $msg=if($testOnly){'监控测试：发现模拟故障。'}else{'故障警报：检测到新的异常，请查看屏幕。'}
      $audio=Alert-Sound $msg
      $beepCN=if($audio.beep -eq 'API_INVOKED'){'已发出'}else{'未成功'}
      $voiceCN=if($audio.speech -eq 'ENGINE_EXIT_0'){'已完成'}else{'未成功'}
      Write-Host ('  提醒：提示音'+$beepCN+'，中文语音播报'+$voiceCN) -ForegroundColor Yellow
    }
    $lastAlarm=$fingerprint
  } else {
    Write-Host '  √ 当前没有新的异常，后台监控正常。' -ForegroundColor Green
    $lastAlarm=''
  }
  Write-Host ''
  Write-Host '  每60秒刷新｜关闭本窗口不影响任务、冻结及后台采集' -ForegroundColor DarkGray
  if($Once){break}
  Start-Sleep -Seconds ([math]::Max(10,$RefreshSeconds))
}
