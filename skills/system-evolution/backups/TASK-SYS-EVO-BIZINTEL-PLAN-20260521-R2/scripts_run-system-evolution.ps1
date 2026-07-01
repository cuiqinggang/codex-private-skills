param(
  [ValidateSet('Approval','Auto','ReportOnly')]
  [string]$Mode = 'Approval',
  [switch]$NoSound
)

$ErrorActionPreference = 'Stop'
$Workspace = 'C:\Users\A\Desktop\1'
$Root = Join-Path $Workspace 'output\TASK-20260520-AI-SYSTEM-EVOLUTION-LOOP'
$Poc = Join-Path $Root 'prototype\evolution_loop_poc.py'
$SkillDir = 'C:\Users\A\.codex\skills\system-evolution'
$HRoot = 'H:\AI_System_Evolution'
$Now = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'

function Write-Utf8File {
  param([string]$Path, [string]$Content)
  $dir = Split-Path -Parent $Path
  if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
  [System.IO.File]::WriteAllText($Path, $Content, [System.Text.Encoding]::UTF8)
}

function Play-SystemEvolutionSound {
  param([bool]$Success)
  if ($NoSound) { return }
  try {
    Add-Type -AssemblyName System.Speech
    $voice = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $message = if ($Success) { '系统进化报告已生成，请查看待批准方案。' } else { '系统进化运行失败，请查看日志。' }
    [void]$voice.SpeakAsync($message)
    if ($Success) { [System.Media.SystemSounds]::Exclamation.Play() } else { [System.Media.SystemSounds]::Hand.Play() }
  } catch {
    $warn = "[$Now] Sound warning: $($_.Exception.Message)"
    Add-Content -LiteralPath (Join-Path $Root 'logs\system-evolution-runner.log') -Value $warn -Encoding UTF8
  }
}

function Sync-ToHDrive {
  if ($Mode -eq 'ReportOnly') { return }
  if (-not (Test-Path 'H:\')) { return }
  $destSkill = Join-Path $HRoot 'skills\system-evolution'
  New-Item -ItemType Directory -Force -Path $destSkill | Out-Null
  Copy-Item -Path (Join-Path $SkillDir '*') -Destination $destSkill -Recurse -Force

  foreach ($sub in @('reports','plans','actions','state','logs')) {
    $src = Join-Path $Root $sub
    $dst = Join-Path $HRoot $sub
    if (Test-Path $src) {
      New-Item -ItemType Directory -Force -Path $dst | Out-Null
      Copy-Item -Path (Join-Path $src '*') -Destination $dst -Recurse -Force -ErrorAction SilentlyContinue
    }
  }
}

try {
  if (-not (Test-Path $Poc)) { throw "PoC script missing: $Poc" }
  New-Item -ItemType Directory -Force -Path (Join-Path $Root 'logs') | Out-Null
  $logPath = Join-Path $Root 'logs\system-evolution-runner.log'
  Add-Content -LiteralPath $logPath -Value "[$Now] START Mode=$Mode" -Encoding UTF8

  Push-Location $Workspace
  $output = & python $Poc --root $Root 2>&1
  $exit = $LASTEXITCODE
  Pop-Location
  Add-Content -LiteralPath $logPath -Value ($output | Out-String) -Encoding UTF8
  if ($exit -ne 0) { throw "PoC failed with exit code $exit" }

  $summaryPath = Join-Path $Root 'evidence\run-summary.json'
  $summary = Get-Content -Raw -LiteralPath $summaryPath | ConvertFrom-Json
  $pass = [bool]$summary.pass

  $pending = @"
# 系统进化待批准执行方案

- 生成时间：$Now
- 模式：$Mode
- 建议触发名：系统进化
- 完整名称：情报支持系统进化方案
- PASS：$pass

## 可以自动做的低风险动作

见 actions\low-risk-auto-actions.md。

## 需要 Codex/Hermes 验证的动作

见 actions\codex-validation-tasks.md。

## 必须用户批准的生产升级

见 actions\manual-approval-required.md。

## 当前策略

当前处于 $Mode 模式。Approval 模式只提出方案和提醒，不修改生产系统。切换到 Auto 后也只执行低风险文件类动作，生产升级仍需批准。
"@
  Write-Utf8File -Path (Join-Path $Root 'actions\pending-approval.md') -Content $pending

  $notice = @"
# 系统进化最新提醒

- 时间：$Now
- 状态：$(if ($pass) { 'PASS' } else { 'PARTIAL/FAIL' })
- 采集来源：$($summary.fetched_source_count)
- 候选情报：$($summary.candidate_count)
- 有效情报：$($summary.selected_count)
- 升级建议：$($summary.upgrade_suggestions_count)
- Codex/Hermes 验证任务：$($summary.codex_validation_task_count)
- 待批准方案：actions\pending-approval.md
- 完整报告：reports\system-evolution-report.md
- 最终报告：reports\report.md

提示：这次运行没有自动修改生产系统。
"@
  Write-Utf8File -Path (Join-Path $Root 'reports\latest-system-evolution-notice.md') -Content $notice

  Sync-ToHDrive
  Play-SystemEvolutionSound -Success:$pass
  Add-Content -LiteralPath $logPath -Value "[$Now] END PASS=$pass" -Encoding UTF8
  Write-Output "SYSTEM_EVOLUTION_RUN_PASS Mode=$Mode Root=$Root"
  exit 0
} catch {
  $err = $_.Exception.Message
  $failNotice = "# 系统进化运行失败`r`n`r`n- 时间：$Now`r`n- 错误：$err`r`n"
  Write-Utf8File -Path (Join-Path $Root 'reports\latest-system-evolution-notice.md') -Content $failNotice
  Play-SystemEvolutionSound -Success:$false
  Write-Error $err
  exit 1
}
