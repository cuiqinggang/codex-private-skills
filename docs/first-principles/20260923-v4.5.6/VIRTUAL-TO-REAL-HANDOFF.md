# v4.5.6 Virtual -> Real Handoff

Role: VIRTUAL exit condition, not a third method step.

## Reality constraints applied

- Codex remains the REAL executor.
- No executable .ps1 staging in AppData\\Local\\Temp.
- No `w32tm /query /source` hard dependency.
- Full `codex exec` duration is measured by `System.Diagnostics.Stopwatch`.
- The Codex prompt is carried by a PowerShell single-quoted here-string, so embedded `$variables` are not expanded by the caller shell.
- The frozen script is streamed from the immutable Git object directly into PowerShell 7.

## Frozen artifact

```text
COMMIT=00f277aee824c324f52c6b7678f724c541da63c7
PATH=docs/first-principles/20260923-v4.5.6/REAL-ENTRY-FROZEN.ps1
```

## Exact handoff command

```powershell
$repo = 'C:\Users\A\Documents\Codex\codex-private-skills'
$taskId = 'ESTE-20260922-001'

$codexStart = [DateTimeOffset]::Now
$sw = [System.Diagnostics.Stopwatch]::StartNew()

Write-Host "TASK_TIME_ID=$taskId"
Write-Host "CODEX_HANDOFF_START_TIMESTAMP=$($codexStart.ToString('o'))"
Write-Host "TIME_SOURCE=LOCAL_SYSTEM_CLOCK_AUDIT_ONLY"
Write-Host "DURATION_CLOCK=SYSTEM_DIAGNOSTICS_STOPWATCH"

$prompt = @'
【ESTE-20260922-001｜极限短时间引擎 v4.5.6｜实】

禁止读取任何 Skill 文件。本冻结合同自包含。
只执行冻结合同，不分析、不重新设计、不现场修复。

你是 REAL 执行器。严格按顺序执行以下动作：

1. 检查冻结 commit 是否已存在于本地：
   git cat-file -e "00f277aee824c324f52c6b7678f724c541da63c7^{commit}"

2. 若不存在，只允许执行：
   git fetch origin codex/first-principles-physical-limit-convergence-v4.5.6
   若且仅若第一次是网络传输类错误，可原样重试一次。
   禁止修改代理或系统设置。

3. 再次确认冻结 commit 存在。

4. 不写 Temp/AppData，不创建中间脚本。直接执行：
   git show "00f277aee824c324f52c6b7678f724c541da63c7:docs/first-principles/20260923-v4.5.6/REAL-ENTRY-FROZEN.ps1" | & 'C:\Program Files\PowerShell\7\pwsh.exe' -NoProfile -NonInteractive -Command -

5. 完整原样返回现实输出。不得修改冻结文件，不得现场修复。

若获取失败或 commit 仍不存在，只返回最小 HANDOFF_DELTA、ACTION=STOP、RETURN_TO_GPT=YES。
'@

codex exec --ephemeral --skip-git-repo-check --sandbox workspace-write -C $repo --color never $prompt

$codexExit = $LASTEXITCODE
$sw.Stop()
$codexEnd = [DateTimeOffset]::Now

Write-Host ""
Write-Host "CODEX_PROCESS_END_TIMESTAMP=$($codexEnd.ToString('o'))"
Write-Host ("CODEX_PROCESS_ACTIVE_MS={0:N3}" -f $sw.Elapsed.TotalMilliseconds)
Write-Host "CODEX_EXIT_CODE=$codexExit"
```

## Freeze preflight

The literal payload must contain the following unchanged tokens before freeze:

```text
$ErrorActionPreference
$commit
$LASTEXITCODE
$null
```

For this v4.5.6 handoff, the outer PowerShell prompt itself contains no embedded execution variables that require expansion. The frozen real script carries its own variables only after it is streamed into its own PowerShell process.
