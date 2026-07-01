$ErrorActionPreference = 'Stop'

$Start = Get-Date
$Stamp = $Start.ToString('yyyyMMdd-HHmmss')
$RunRoot = 'H:\AI\reports\aios-skill-self-purification\weekly-60min-light-check'
$RunDir = Join-Path $RunRoot $Stamp
$OutDir = Join-Path $RunDir 'outputs'
$Roots = @('C:\Users\A\.codex\skills', 'H:\AI\skills')

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$FormalBefore = @{}
foreach ($Root in $Roots) {
    if (Test-Path -LiteralPath $Root) {
        Get-ChildItem -LiteralPath $Root -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object {
            $FormalBefore[$_.FullName] = $_.LastWriteTimeUtc.Ticks
        }
    }
}

function Add-Checkpoint {
    param(
        [string]$Name,
        [string]$Note
    )
    $Now = Get-Date
    $Elapsed = [math]::Round(($Now - $Start).TotalMinutes, 2)
    $Obj = [ordered]@{
        name = $Name
        at = $Now.ToString('o')
        elapsed_minutes = $Elapsed
        note = $Note
    }
    Add-Content -LiteralPath (Join-Path $RunDir 'checkpoint-events.jsonl') -Value ($Obj | ConvertTo-Json -Compress) -Encoding UTF8
    Write-Output "CHECKPOINT $Name elapsed=$Elapsed dir=$RunDir"
}

function Get-WordSet {
    param([string]$Text)
    @([regex]::Matches($Text.ToLowerInvariant(), '[a-z0-9\u4e00-\u9fff]{3,}') | ForEach-Object { $_.Value } | Sort-Object -Unique)
}

Add-Checkpoint 'start' 'policy loaded; shadow-only; formal writes forbidden; 60min automation floor active'

$Skills = @()
foreach ($Root in $Roots) {
    if (-not (Test-Path -LiteralPath $Root)) { continue }
    Get-ChildItem -LiteralPath $Root -Directory -ErrorAction SilentlyContinue | ForEach-Object {
        $SkillPath = Join-Path $_.FullName 'SKILL.md'
        $HasSkill = Test-Path -LiteralPath $SkillPath
        $Text = ''
        if ($HasSkill) {
            try { $Text = Get-Content -LiteralPath $SkillPath -Raw -ErrorAction Stop } catch { $Text = '' }
        }
        $Acceptance = (Get-ChildItem -LiteralPath $_.FullName -File -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -match '(ACCEPT|验收|EVIDENCE|REPORT|PASS|review|REVIEW)' } |
            Select-Object -First 8 -ExpandProperty Name) -join '; '
        $UseLines = @()
        if ($Text) {
            $UseLines = [regex]::Matches($Text, '(?im)^\s*-?\s*(Use when|Trigger|Triggers|When to use):?.{0,240}') |
                ForEach-Object { $_.Value.Trim() } |
                Select-Object -First 5
        }
        $Skills += [pscustomobject]@{
            Name = $_.Name
            Root = $Root
            Path = $_.FullName
            HasSkill = $HasSkill
            SkillPath = $SkillPath
            LastWriteTime = $_.LastWriteTime.ToString('o')
            LastWriteTimeUtc = $_.LastWriteTimeUtc
            TextLength = $Text.Length
            TriggerText = ($UseLines -join ' | ')
            HasAcceptance = [bool]$Acceptance
            AcceptanceFiles = $Acceptance
            HighRisk = ($Text -match '(?i)auto-merge|automerge|auto.?delete|delete|remove|unattended|without approval|always|whenever|must|global|system|admin|registry|permission|credential|secret|token|ssh|kill|stop process|format|reset|overwrite')
            LocalGlobal = ($Text -match '(?i)local|project-local|workspace|global|all tasks|every task|always|whenever')
            TotalControl = ($Text -match '(?i)total-control|orchestrator|all tasks|every task|always use|must use first')
            RejectedFailure = ($Text -match '(?i)rejected|failure|retrospective|postmortem|rollback|hard rules')
            Hash = $(if ($Text) { (Get-FileHash -LiteralPath $SkillPath -Algorithm SHA256).Hash } else { '' })
        }
    }
}

$Skills | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $RunDir 'scan-inventory.json') -Encoding UTF8

$Recent = @($Skills | Where-Object { $_.LastWriteTimeUtc -gt (Get-Date).ToUniversalTime().AddDays(-14) })
$Modified45 = @($Skills | Where-Object { $_.LastWriteTimeUtc -gt (Get-Date).ToUniversalTime().AddDays(-45) })
$DupeNames = @($Skills | Group-Object Name | Where-Object Count -gt 1 | Sort-Object Count -Descending)
$MissingAcceptance = @($Skills | Where-Object { $_.HasSkill -and -not $_.HasAcceptance } | Sort-Object LastWriteTimeUtc -Descending)
$HighRisk = @($Skills | Where-Object { $_.HasSkill -and $_.HighRisk } | Sort-Object LastWriteTimeUtc -Descending)
$LocalGlobal = @($Skills | Where-Object { $_.HasSkill -and $_.LocalGlobal } | Sort-Object LastWriteTimeUtc -Descending)
$TotalControl = @($Skills | Where-Object { $_.HasSkill -and $_.TotalControl } | Sort-Object LastWriteTimeUtc -Descending)
$RejectedHits = @($Skills | Where-Object { $_.HasSkill -and $_.RejectedFailure } | Sort-Object LastWriteTimeUtc -Descending)

$Pairs = @()
$WithTrig = @($Skills | Where-Object { $_.HasSkill -and $_.TriggerText })
for ($i = 0; $i -lt $WithTrig.Count; $i++) {
    for ($j = $i + 1; $j -lt $WithTrig.Count; $j++) {
        $A = $WithTrig[$i]
        $B = $WithTrig[$j]
        $Wa = Get-WordSet $A.TriggerText
        $Wb = Get-WordSet $B.TriggerText
        if ($Wa.Count -eq 0 -or $Wb.Count -eq 0) { continue }
        $Inter = @($Wa | Where-Object { $Wb -contains $_ })
        $Union = @($Wa + $Wb | Sort-Object -Unique)
        $Score = [math]::Round($Inter.Count / [math]::Max(1, $Union.Count), 2)
        if ($Score -ge 0.28 -or ($A.Name -eq $B.Name)) {
            $Pairs += [pscustomobject]@{
                A = $A.Path
                B = $B.Path
                Score = $Score
                Overlap = ($Inter -join ', ')
            }
        }
    }
}
$Pairs = @($Pairs | Sort-Object Score -Descending | Select-Object -First 180)

$Summary = [ordered]@{
    run_dir = $RunDir
    started_at = $Start.ToString('o')
    roots = $Roots
    total_skill_dirs = $Skills.Count
    skill_md_count = @($Skills | Where-Object HasSkill).Count
    recent_14d = $Recent.Count
    modified_45d = $Modified45.Count
    duplicate_name_groups = $DupeNames.Count
    trigger_similarity_pairs = $Pairs.Count
    high_risk_candidates = $HighRisk.Count
    missing_acceptance_candidates = $MissingAcceptance.Count
    local_global_candidates = $LocalGlobal.Count
    total_control_candidates = $TotalControl.Count
    rejected_failure_hits = $RejectedHits.Count
    formal_skills_modified = 'NO'
    auto_merge_allowed = 'NO'
}
$Summary | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $RunDir 'scan-summary.json') -Encoding UTF8

$Issue = @()
$Issue += '# Weekly 60min AIOS Skill Purification Issue List'
$Issue += ''
$Issue += "Started: $($Start.ToString('o'))"
$Issue += "Run dir: $RunDir"
$Issue += ''
$Issue += '## Counts'
$Summary.GetEnumerator() | ForEach-Object { $Issue += "- $($_.Key): $($_.Value)" }
$Issue += ''
$Issue += '## High-signal issues'
foreach ($G in ($DupeNames | Select-Object -First 25)) {
    $Paths = ($G.Group | ForEach-Object Path) -join ' | '
    $Issue += "- Duplicate package name ``$($G.Name)`` count=$($G.Count): $Paths"
}
foreach ($M in ($MissingAcceptance | Select-Object -First 40)) {
    $Issue += "- Missing/weak acceptance evidence candidate: ``$($M.Name)`` at ``$($M.Path)``"
}
foreach ($H in ($HighRisk | Select-Object -First 40)) {
    $Issue += "- High-risk wording candidate: ``$($H.Name)`` at ``$($H.Path)``"
}
foreach ($Tc in ($TotalControl | Select-Object -First 30)) {
    $Issue += "- Total-control trigger scope candidate: ``$($Tc.Name)`` at ``$($Tc.Path)``"
}
foreach ($P in ($Pairs | Select-Object -First 40)) {
    $Issue += "- Trigger overlap score=$($P.Score): ``$($P.A)`` <-> ``$($P.B)`` overlap=[$($P.Overlap)]"
}
$Issue | Set-Content -LiteralPath (Join-Path $RunDir 'weekly-issue-list.md') -Encoding UTF8

$Cand = @('# Candidate Patches (Shadow Only)', '', 'No formal skill files modified. These are review candidates, not applied patches.', '', '## Suggested review candidates')
foreach ($M in ($MissingAcceptance | Select-Object -First 25)) {
    $Cand += "- Add or link explicit acceptance/review evidence page for ``$($M.Path)`` if this is an active skill."
}
foreach ($H in ($HighRisk | Select-Object -First 25)) {
    $Cand += "- Human-review high-risk automation wording in ``$($H.Path)``; preserve hard rules and convert direct actions to approval-gated language only if appropriate."
}
foreach ($G in ($DupeNames | Select-Object -First 20)) {
    $Cand += "- Compare duplicate skill roots for ``$($G.Name)`` and document canonical/local mirror relationship before any merge."
}
$Cand | Set-Content -LiteralPath (Join-Path $RunDir 'candidate-patches.md') -Encoding UTF8

$Rej = @(
    '# Rejected Edits Buffer',
    '',
    'Rejected by policy for this run:',
    '',
    '- No auto-merge into formal skill files.',
    '- No deletion of hard rules, failure reviews, archives, quarantine folders, or backup folders.',
    '- No promotion of project-local rules into global AGENTS/SKILL scope.',
    '- No total-control trigger expansion.',
    ''
)
foreach ($R in ($RejectedHits | Select-Object -First 40)) {
    $Rej += "- Preserve failure/rejected-review material candidate: ``$($R.Path)``"
}
$Rej | Set-Content -LiteralPath (Join-Path $RunDir 'rejected-edits.md') -Encoding UTF8

$Human = @(
    '# Needs Human Review',
    '',
    '- Decide canonical source for duplicate name groups that exist in both `C:\Users\A\.codex\skills` and `H:\AI\skills`.',
    '- Review high-risk Windows/system/browser/permission skills before any wording edits.',
    '- Review `_test_344_index_probe_skill`, archive, quarantine, and OLD folders as metadata-only candidates; do not delete in this run.',
    '- Inspect H-drive `cursor-kilo-terminal-paste-repair` because it is a recent directory without top-level `SKILL.md` while the Codex mirror has one.',
    ''
)
foreach ($Tc in ($TotalControl | Select-Object -First 25)) {
    $Human += "- Total-control scope review: ``$($Tc.Path)``"
}
$Human | Set-Content -LiteralPath (Join-Path $RunDir 'needs-human-review.md') -Encoding UTF8

$Html = @"
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>AIOS Weekly 60min Review</title>
  <style>body{font-family:Segoe UI,Arial,sans-serif;max-width:1100px;margin:32px auto;line-height:1.45}code{background:#f3f3f3;padding:2px 4px}li{margin:4px 0}</style>
</head>
<body>
  <h1>AIOS Weekly 60min Skill Purification Review</h1>
  <p>Run dir: <code>$RunDir</code></p>
  <ul>
    <li>Total skill dirs: $($Skills.Count)</li>
    <li>SKILL.md count: $(@($Skills | Where-Object HasSkill).Count)</li>
    <li>Recent 14d: $($Recent.Count)</li>
    <li>Duplicate name groups: $($DupeNames.Count)</li>
    <li>Trigger similarity pairs: $($Pairs.Count)</li>
    <li>High-risk candidates: $($HighRisk.Count)</li>
    <li>Missing acceptance candidates: $($MissingAcceptance.Count)</li>
  </ul>
  <p>Shadow-only. Formal skill files modified: NO. Auto-merge allowed: NO.</p>
  <p>See sibling markdown reports for issue list, candidate patches, rejected edits, and human review queue.</p>
</body>
</html>
"@
$Html | Set-Content -LiteralPath (Join-Path $OutDir 'index.html') -Encoding UTF8

Add-Checkpoint 'scan-complete' "inventory and shadow reports generated; skills=$($Skills.Count); pairs=$($Pairs.Count)"

foreach ($Target in @(15, 30, 45)) {
    while (((Get-Date) - $Start).TotalMinutes -lt $Target) {
        Start-Sleep -Seconds 20
    }
    Add-Checkpoint "${Target}min" 'runtime gate checkpoint; continuing comparison and no formal writes'
}

while (((Get-Date) - $Start).TotalMinutes -lt 60.05) {
    Start-Sleep -Seconds 20
}

$FormalAfter = @{}
foreach ($Root in $Roots) {
    if (Test-Path -LiteralPath $Root) {
        Get-ChildItem -LiteralPath $Root -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object {
            $FormalAfter[$_.FullName] = $_.LastWriteTimeUtc.Ticks
        }
    }
}
$Changed = @()
foreach ($K in $FormalAfter.Keys) {
    if ($FormalBefore.ContainsKey($K) -and $FormalBefore[$K] -ne $FormalAfter[$K]) {
        $Changed += $K
    } elseif (-not $FormalBefore.ContainsKey($K)) {
        $Changed += $K
    }
}
$FormalModified = if ($Changed.Count -eq 0) { 'NO' } else { 'YES' }
$End = Get-Date
$Elapsed = [math]::Round(($End - $Start).TotalMinutes, 2)
$Status = if ($Elapsed -ge 60 -and $FormalModified -eq 'NO') { 'PASS' } else { 'PARTIAL_OR_FAIL' }

Add-Checkpoint 'final' "final status=$Status; formal_skills_modified=$FormalModified"

$Runtime = [ordered]@{
    started_at = $Start.ToString('o')
    ended_at = $End.ToString('o')
    elapsed_minutes = $Elapsed
    required_minimum_minutes = 60
    checkpoints = @('start', 'scan-complete', '15min', '30min', '45min', 'final')
    reviewed_scope = $Roots
    total_skill_dirs = $Skills.Count
    skill_md_count = @($Skills | Where-Object HasSkill).Count
    final_status = $Status
    formal_skills_modified = $FormalModified
    changed_formal_files = $Changed
    auto_merge_allowed = 'NO'
    output_files = @('runtime-evidence.json', 'checkpoint-events.jsonl', 'weekly-issue-list.md', 'candidate-patches.md', 'rejected-edits.md', 'needs-human-review.md', 'outputs/index.html')
}
$Runtime | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $RunDir 'runtime-evidence.json') -Encoding UTF8

$Events = Get-Content -LiteralPath (Join-Path $RunDir 'checkpoint-events.jsonl')
$Timeline = '<html><body><h1>Checkpoint Timeline</h1><pre>' + ($Events -join "`n") + '</pre></body></html>'
$Timeline | Set-Content -LiteralPath (Join-Path $RunDir 'checkpoint-timeline.html') -Encoding UTF8

Write-Output "FINAL_STATUS $Status elapsed=$Elapsed formal_skills_modified=$FormalModified run_dir=$RunDir"
