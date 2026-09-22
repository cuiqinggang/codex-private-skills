# v4.5.5 Virtual -> Real Handoff

This handoff is part of VIRTUAL completion. It preserves Codex as the REAL executor.

## Whole-loop principle

```text
GPT -> Codex -> deterministic tools -> local evidence -> Codex result -> GPT final judgment
```

PowerShell is an internal deterministic tool. It does not replace Codex in the default closed loop.

## Frozen real artifact

- repository: cuiqinggang/codex-private-skills
- branch: codex/first-principles-physical-limit-convergence-v4.5.5
- frozen commit: ba4b82004102fa8e833f45b3f88404b10a576a3e
- frozen path: docs/first-principles/20260923-v4.5.5/REAL-ENTRY-FROZEN.ps1
- git blob sha: 901b8ee53237f11e5a8d9f643d0341cea4f88cf4
- no Temp/AppData script write
- Codex streams the frozen script directly from git object to PowerShell

## Timing relay

The outer PowerShell wrapper surrounds the entire `codex exec` process:

```text
CODEX_HANDOFF_START_TIMESTAMP
CODEX_PROCESS_ACTIVE_MS
CODEX_PROCESS_END_TIMESTAMP
```

The wrapper also records the Windows time source using `w32tm /query /source`.

## Frozen Codex contract

1. Do not read Skill files; this contract is self-contained.
2. Check whether frozen commit exists locally.
3. If missing, fetch only branch codex/first-principles-physical-limit-convergence-v4.5.5; retry once only for transport failure; never change proxy/system settings.
4. Confirm the frozen commit exists.
5. Do not write the frozen script to Temp/AppData or another staging path.
6. Stream the exact frozen git object directly into PowerShell 7:
   `git show <commit>:<path> | pwsh -NoProfile -Command -`
7. Return the reality output verbatim. Do not redesign, repair, or alter the frozen artifact.
8. On functional failure, stop and return the minimum Reality Delta to GPT.

## Exact manual-mode handoff command

The current manual bridge uses one PowerShell block. PowerShell only wraps and times the full Codex executor process; Codex remains the REAL executor.

```powershell
$repo = 'C:\\Users\\A\\Documents\\Codex\\codex-private-skills'
$taskId = 'ESTE-20260922-001'
$timeSource = (& w32tm /query /source 2>$null | Out-String).Trim()
if ([string]::IsNullOrWhiteSpace($timeSource)) { $timeSource = 'UNKNOWN' }

$codexStart = [DateTimeOffset]::Now
$sw = [System.Diagnostics.Stopwatch]::StartNew()

Write-Host "TASK_TIME_ID=$taskId"
Write-Host "CODEX_HANDOFF_START_TIMESTAMP=$($codexStart.ToString('o'))"
Write-Host "TIME_SOURCE=$timeSource"

codex exec --ephemeral --skip-git-repo-check --sandbox workspace-write -C $repo --color never @"
【ESTE-20260922-001｜极限短时间引擎 v4.5.5｜实】
禁止读取任何 Skill 文件。本冻结合同自包含。
只执行冻结合同，不分析、不重新设计、不现场修复。

你是 REAL 执行器。唯一高价值动作：运行下面这一条 PowerShell 命令，并原样返回输出。

& 'C:\\Program Files\\PowerShell\\7\\pwsh.exe' -NoProfile -NonInteractive -Command '
  $ErrorActionPreference = "Stop"
  $commit = "ba4b82004102fa8e833f45b3f88404b10a576a3e"
  $branch = "codex/first-principles-physical-limit-convergence-v4.5.5"
  $path = "docs/first-principles/20260923-v4.5.5/REAL-ENTRY-FROZEN.ps1"

  git cat-file -e ($commit + "^{commit}") 2>$null
  if ($LASTEXITCODE -ne 0) {
    $first = & git fetch origin $branch 2>&1
    $firstExit = $LASTEXITCODE
    if ($firstExit -ne 0) {
      $txt = [string]::Join([Environment]::NewLine, $first)
      $transport = $txt -match "(?i)unable to access|empty reply|could not resolve|failed to connect|timed out|connection.*(reset|closed)"
      if (-not $transport) {
        Write-Host "HANDOFF_DELTA=GIT_FETCH_NONTRANSPORT_FAIL"
        Write-Host "ACTION=STOP"
        Write-Host "RETURN_TO_GPT=YES"
        exit 10
      }
      $second = & git fetch origin $branch 2>&1
      if ($LASTEXITCODE -ne 0) {
        Write-Host "HANDOFF_DELTA=GIT_TRANSPORT_FAIL"
        Write-Host "ACTION=STOP"
        Write-Host "RETURN_TO_GPT=YES"
        exit 11
      }
    }
  }

  git cat-file -e ($commit + "^{commit}") 2>$null
  if ($LASTEXITCODE -ne 0) {
    Write-Host "HANDOFF_DELTA=FROZEN_COMMIT_MISSING"
    Write-Host "ACTION=STOP"
    Write-Host "RETURN_TO_GPT=YES"
    exit 12
  }

  git show ($commit + ":" + $path) | & "C:\\Program Files\\PowerShell\\7\\pwsh.exe" -NoProfile -NonInteractive -Command -
  exit $LASTEXITCODE
'

不要写入 Temp/AppData。
不要修改代理或系统设置。
不要读取额外技能。
不要修复冻结方案。
只返回上面命令产生的现实输出。
"@

$codexExit = $LASTEXITCODE
$sw.Stop()
$codexEnd = [DateTimeOffset]::Now

Write-Host "CODEX_PROCESS_END_TIMESTAMP=$($codexEnd.ToString('o'))"
Write-Host ("CODEX_PROCESS_ACTIVE_MS={0:N3}" -f $sw.Elapsed.TotalMilliseconds)
Write-Host "CODEX_EXIT_CODE=$codexExit"
```
