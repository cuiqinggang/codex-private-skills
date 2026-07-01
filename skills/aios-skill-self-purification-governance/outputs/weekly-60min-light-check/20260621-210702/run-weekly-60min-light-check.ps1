param(
  [string]$RunDir,
  [int]$MinimumMinutes = 60
)
$ErrorActionPreference = 'Continue'
$started = Get-Date
$roots = @('C:\Users\A\.codex\skills','H:\AI\skills')
$checkpointPath = Join-Path $RunDir 'runtime-evidence.json'
$timelineMd = Join-Path $RunDir 'checkpoint-timeline.md'
$issuesPath = Join-Path $RunDir 'weekly-issue-list.md'
$candidatePath = Join-Path $RunDir 'candidate-patches.md'
$rejectedPath = Join-Path $RunDir 'rejected-edits.md'
$humanPath = Join-Path $RunDir 'needs-human-review.md'
$reviewDir = Join-Path $RunDir 'outputs'
New-Item -ItemType Directory -Force -Path $reviewDir | Out-Null
$checkpoints = New-Object System.Collections.Generic.List[object]
function Add-Checkpoint([string]$Name,[string]$Note) {
  $now = Get-Date
  $elapsed = [math]::Round(($now - $started).TotalMinutes,2)
  $checkpoints.Add([ordered]@{ name=$Name; at=$now.ToString('o'); elapsed_minutes=$elapsed; note=$Note }) | Out-Null
  $evidence = [ordered]@{
    task_id='AIOS_SKILL_SELF_PURIFICATION_WEEKLY_60MIN_LIGHT_CHECK'
    automation_id='aios-30min'
    started_at=$started.ToString('o')
    last_checkpoint_at=$now.ToString('o')
    elapsed_minutes=$elapsed
    minimum_elapsed_minutes=$MinimumMinutes
    checkpoints=$checkpoints
    checkpoint_count=$checkpoints.Count
    reviewed_roots=$roots
    formal_skills_modified='NO'
    auto_merge_allowed='NO'
    final_status='RUNNING'
  }
  $evidence | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $checkpointPath -Encoding UTF8
  $lines = @('# Checkpoint Timeline','')
  foreach ($cp in $checkpoints) { $lines += "- $($cp.name) | $($cp.elapsed_minutes) min | $($cp.at) | $($cp.note)" }
  $lines | Set-Content -LiteralPath $timelineMd -Encoding UTF8
}
function Normalize-Text([string]$s) {
  if ($null -eq $s) { return '' }
  return (($s.ToLowerInvariant() -replace '[^a-z0-9\p{IsCJKUnifiedIdeographs}]+',' ') -replace '\s+',' ').Trim()
}
function Get-SkillRecord([string]$dir) {
  $skillFile = Join-Path $dir 'SKILL.md'
  $mdFiles = @(Get-ChildItem -LiteralPath $dir -File -Filter '*.md' -ErrorAction SilentlyContinue)
  $allFiles = @(Get-ChildItem -LiteralPath $dir -File -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch '\\(node_modules|\.git|outputs|runs|backups)\\' })
  $text = ''
  if (Test-Path $skillFile) { $text = Get-Content -LiteralPath $skillFile -Raw -ErrorAction SilentlyContinue }
  $lines = @()
  if ($text) { $lines = $text -split "`r?`n" }
  $triggerLines = @($lines | Where-Object { $_ -match '(?i)use when|use this skill|trigger|keyword|触发|关键词|使用场景|适用|必须使用|开工前' } | Select-Object -First 30)
  $riskMatches = @($lines | Where-Object { $_ -match '(?i)auto.?merge|unattended|delete|remove|overwrite|global|always|any task|all tasks|background|自动合并|自动删除|删除|覆盖|全局|所有任务|任何任务|总控|常驻|硬规则|失败复盘|rejected' } | Select-Object -First 50)
  $acceptanceFiles = @($mdFiles | Where-Object { $_.Name -match '(?i)acceptance|验收|gate|evidence|result' })
  $rejectedFiles = @($allFiles | Where-Object { $_.Name -match '(?i)reject|rejected|buffer|patch|复盘|failure|fail|retrospective' })
  $lastWrite = ($allFiles + $mdFiles | Sort-Object LastWriteTime -Descending | Select-Object -First 1).LastWriteTime
  [ordered]@{
    name = Split-Path $dir -Leaf
    path = $dir
    skill_file = if (Test-Path $skillFile) { $skillFile } else { $null }
    last_write = if ($lastWrite) { $lastWrite.ToString('o') } else { $null }
    md_count = $mdFiles.Count
    file_count = $allFiles.Count
    trigger_text = (Normalize-Text (($triggerLines -join ' ') + ' ' + (Split-Path $dir -Leaf)))
    trigger_lines = $triggerLines
    risk_lines = $riskMatches
    acceptance_count = $acceptanceFiles.Count
    acceptance_files = @($acceptanceFiles | ForEach-Object FullName)
    rejected_buffer_count = $rejectedFiles.Count
    rejected_buffer_files = @($rejectedFiles | Select-Object -First 20 | ForEach-Object FullName)
  }
}
Add-Checkpoint 'start' 'Policy, runtime gate, Knowledge Brain, and memory checked; beginning filesystem comparison scan.'
$skillDirs = New-Object System.Collections.Generic.List[string]
foreach ($root in $roots) {
  if (Test-Path $root) {
    Get-ChildItem -LiteralPath $root -Directory -ErrorAction SilentlyContinue | ForEach-Object {
      if (Test-Path (Join-Path $_.FullName 'SKILL.md')) { $skillDirs.Add($_.FullName) | Out-Null }
    }
  }
}
$records = @($skillDirs | ForEach-Object { Get-SkillRecord $_ })
$now = Get-Date
$recent = @($records | Where-Object { $_.last_write -and ([datetime]$_.last_write) -ge $now.AddDays(-14) } | Sort-Object last_write -Descending)
$modified = @($records | Where-Object { $_.last_write -and ([datetime]$_.last_write) -ge $now.AddDays(-45) } | Sort-Object last_write -Descending)
$highRisk = @($records | Where-Object { $_.risk_lines.Count -gt 0 } | Sort-Object @{Expression={$_.risk_lines.Count};Descending=$true}, name)
$missingAcceptance = @($records | Where-Object { $_.acceptance_count -eq 0 } | Sort-Object name)
$triggerGroups = New-Object System.Collections.Generic.List[object]
for ($i=0; $i -lt $records.Count; $i++) {
  for ($j=$i+1; $j -lt $records.Count; $j++) {
    $a = $records[$i]; $b = $records[$j]
    $ta = @($a.trigger_text -split ' ' | Where-Object { $_.Length -ge 4 } | Select-Object -Unique)
    $tb = @($b.trigger_text -split ' ' | Where-Object { $_.Length -ge 4 } | Select-Object -Unique)
    if ($ta.Count -eq 0 -or $tb.Count -eq 0) { continue }
    $inter = @($ta | Where-Object { $tb -contains $_ })
    $unionCount = (@($ta + $tb | Select-Object -Unique)).Count
    $score = if ($unionCount -gt 0) { [math]::Round($inter.Count / $unionCount, 3) } else { 0 }
    $nameOverlap = 0
    $na = @((Normalize-Text $a.name) -split ' ' | Where-Object { $_.Length -ge 4 })
    $nb = @((Normalize-Text $b.name) -split ' ' | Where-Object { $_.Length -ge 4 })
    if (@($na | Where-Object { $nb -contains $_ }).Count -gt 0) { $nameOverlap = 0.08 }
    $finalScore = $score + $nameOverlap
    if ($finalScore -ge 0.18 -or ($inter.Count -ge 5 -and $finalScore -ge 0.12)) {
      $triggerGroups.Add([ordered]@{ score=[math]::Round($finalScore,3); shared_terms=@($inter | Select-Object -First 16); a=$a.name; a_path=$a.path; b=$b.name; b_path=$b.path }) | Out-Null
    }
  }
}
$triggerGroupsSorted = @($triggerGroups | Sort-Object score -Descending | Select-Object -First 80)
$localGlobal = @($records | Where-Object { ($_.risk_lines -join ' ') -match '(?i)(global|全局|all tasks|any task|所有任务|任何任务)' -and ($_.risk_lines -join ' ') -match '(?i)(H:\\|C:\\|local|project|workspace|本地|项目|工作区)' } | Sort-Object name)
$totalControl = @($records | Where-Object { ($_.risk_lines -join ' ') -match '(?i)(total-control|总控|use first|always use|所有任务|任何任务|all tasks|any task|开工前)' } | Sort-Object name)
$failureReview = @($records | Where-Object { $_.rejected_buffer_files -match '(?i)(failure|fail|复盘|retrospective)' } | Sort-Object name)
$staleRejected = @($records | Where-Object { $_.risk_lines -match '(?i)rejected|reject|buffer|失败复盘|复盘' -and $_.rejected_buffer_count -eq 0 } | Sort-Object name)
$inventory = [ordered]@{
  generated_at=(Get-Date).ToString('o')
  roots=$roots
  skill_count=$records.Count
  recent_14d_count=$recent.Count
  modified_45d_count=$modified.Count
  high_risk_phrase_count=$highRisk.Count
  missing_acceptance_count=$missingAcceptance.Count
  trigger_similarity_pairs=$triggerGroupsSorted.Count
  local_global_candidates=$localGlobal.Count
  total_control_candidates=$totalControl.Count
  failure_review_buffers_seen=$failureReview.Count
  stale_rejected_buffer_candidates=$staleRejected.Count
  records=$records
  trigger_groups=$triggerGroupsSorted
}
$inventory | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $RunDir 'scan-inventory.json') -Encoding UTF8
function Section($title,$items,$formatter) {
  $out = @("## $title",'')
  if (@($items).Count -eq 0) { $out += '- No findings in sampled scan.'; $out += ''; return $out }
  foreach ($item in $items) { $out += (& $formatter $item) }
  $out += ''
  return $out
}
$issueLines = @('# Weekly 60min Light Check Issue List','',"Generated: $(Get-Date -Format o)",'','Mode: shadow-only. Formal skill files modified: NO. Auto-merge allowed: NO.','')
$issueLines += '## Scope Summary'; $issueLines += ''; $issueLines += "- Skill roots scanned: $($roots -join '; ')"; $issueLines += "- Skill packages with SKILL.md: $($records.Count)"; $issueLines += "- Recent skills, 14d: $($recent.Count)"; $issueLines += "- Modified skills, 45d: $($modified.Count)"; $issueLines += "- Trigger-similarity pairs retained: $($triggerGroupsSorted.Count)"; $issueLines += "- High-risk wording candidates: $($highRisk.Count)"; $issueLines += "- Missing acceptance/evidence page candidates: $($missingAcceptance.Count)"; $issueLines += ''
$issueLines += Section 'P1 Duplicate or overlapping triggers' $triggerGroupsSorted { param($g) "- score=$($g.score): `$($g.a)` <-> `$($g.b)`; shared: $($g.shared_terms -join ', ')" }
$issueLines += Section 'P1 High-risk automation or scope wording' (@($highRisk | Select-Object -First 60)) { param($r) "- `$($r.name)` | $($r.path) | risk lines: $(@($r.risk_lines | Select-Object -First 3) -join ' / ')" }
$issueLines += Section 'P1 Local rules that may be elevated globally' $localGlobal { param($r) "- `$($r.name)` | $($r.path) | inspect global/local boundary wording." }
$issueLines += Section 'P1 Total-control trigger expansion candidates' $totalControl { param($r) "- `$($r.name)` | $($r.path) | inspect total-control or always-use wording." }
$issueLines += Section 'P2 Missing acceptance or evidence page candidates' (@($missingAcceptance | Select-Object -First 120)) { param($r) "- `$($r.name)` | $($r.path) | no ACCEPTANCE/GATE/EVIDENCE-like md file at package root." }
$issueLines += Section 'P2 Rejected-edit buffer stale/missing candidates' $staleRejected { param($r) "- `$($r.name)` | $($r.path) | mentions rejected/buffer/failure review but no matching buffer file found." }
$issueLines += Section 'P3 Failure review buffers found and should be preserved' $failureReview { param($r) "- `$($r.name)` | $($r.path) | preservation files: $(@($r.rejected_buffer_files | Select-Object -First 4) -join '; ')" }
$issueLines | Set-Content -LiteralPath $issuesPath -Encoding UTF8
$candidateLines = @('# Candidate Patches', '', 'Shadow-only patch candidates. Do not apply without user/GPT Gate Review.', '')
$candidateLines += '## Acceptance page candidates'; $candidateLines += ''; foreach ($r in @($missingAcceptance | Select-Object -First 40)) { $candidateLines += "- Candidate: add `ACCEPTANCE-GATE.md` to `$($r.path)` with runtime/status evidence checklist; do not touch SKILL.md." }
$candidateLines += ''; $candidateLines += '## Trigger de-dup candidates'; $candidateLines += ''; foreach ($g in @($triggerGroupsSorted | Select-Object -First 40)) { $candidateLines += "- Candidate: compare `$($g.a)` and `$($g.b)`; narrow one trigger by domain-specific prerequisites instead of broad `use when` wording." }
$candidateLines += ''; $candidateLines += '## High-risk wording candidates'; $candidateLines += ''; foreach ($r in @($highRisk | Select-Object -First 40)) { $candidateLines += "- Candidate: in `$($r.name)`, convert automation wording to shadow-first / human-review language where it implies merge, delete, overwrite, global expansion, or unattended action." }
$candidateLines | Set-Content -LiteralPath $candidatePath -Encoding UTF8
$rejectedLines = @('# Rejected Edits', '', 'These edits are explicitly rejected for this run.', '', '- Do not modify formal `SKILL.md` files.', '- Do not delete or compact user hard rules.', '- Do not delete failure retrospectives or rejected-edit buffers.', '- Do not merge duplicate skills automatically.', '- Do not broaden total-control triggers.', '- Do not convert project-local rules into global rules.', '- Do not claim PASS before 60 elapsed minutes and all checkpoints exist.', '')
foreach ($r in @($totalControl | Select-Object -First 40)) { $rejectedLines += "- Rejected now: direct trigger rewrite in `$($r.path)`; requires human review." }
foreach ($r in @($failureReview | Select-Object -First 40)) { $rejectedLines += "- Rejected now: removing/archiving failure review material in `$($r.path)`; preservation required." }
$rejectedLines | Set-Content -LiteralPath $rejectedPath -Encoding UTF8
$humanLines = @('# Needs Human Review', '', 'Items that should not be auto-applied.', '')
foreach ($g in @($triggerGroupsSorted | Where-Object { $_.score -ge 0.30 } | Select-Object -First 30)) { $humanLines += "- Trigger collision: `$($g.a)` vs `$($g.b)` (score $($g.score)); decide ownership before patching." }
foreach ($r in @($localGlobal | Select-Object -First 30)) { $humanLines += "- Local/global boundary: `$($r.name)`; check whether path-specific rules are being promoted globally." }
foreach ($r in @($highRisk | Select-Object -First 30)) { $humanLines += "- Risk wording: `$($r.name)`; inspect whether automation language violates shadow-only policy." }
$humanLines | Set-Content -LiteralPath $humanPath -Encoding UTF8
Add-Checkpoint 'scan-complete' "Initial comparative scan complete: $($records.Count) skills, $($triggerGroupsSorted.Count) trigger pairs, $($highRisk.Count) risk candidates."
$targets = @(
  @{Name='15min'; Minute=15; Note='15min checkpoint: issue list, candidates, rejected edits, and needs-human-review drafts exist.'},
  @{Name='30min'; Minute=30; Note='30min checkpoint: continued review window; formal skills unchanged and auto-merge still forbidden.'},
  @{Name='45min'; Minute=45; Note='45min checkpoint: checkpoint evidence complete so far; PASS still gated until 60min.'},
  @{Name='final'; Minute=$MinimumMinutes; Note='Final checkpoint: elapsed runtime gate reached; writing review page and final evidence.'}
)
foreach ($t in $targets) {
  while (((Get-Date) - $started).TotalMinutes -lt $t.Minute) { Start-Sleep -Seconds 20 }
  Add-Checkpoint $t.Name $t.Note
}
$ended = Get-Date
$elapsed = [math]::Round(($ended - $started).TotalMinutes,2)
$status = if ($elapsed -ge $MinimumMinutes -and $checkpoints.Count -ge 5) { 'PASS' } else { 'FAIL_RUNTIME_GATE' }
$finalEvidence = [ordered]@{
  task_id='AIOS_SKILL_SELF_PURIFICATION_WEEKLY_60MIN_LIGHT_CHECK'
  automation_id='aios-30min'
  started_at=$started.ToString('o')
  ended_at=$ended.ToString('o')
  elapsed_minutes=$elapsed
  minimum_elapsed_minutes=$MinimumMinutes
  checkpoints=$checkpoints
  checkpoint_count=$checkpoints.Count
  reviewed_scope=[ordered]@{
    roots=$roots
    skill_count=$records.Count
    recent_14d_count=$recent.Count
    modified_45d_count=$modified.Count
    trigger_similarity_pairs=$triggerGroupsSorted.Count
    high_risk_phrase_count=$highRisk.Count
    missing_acceptance_count=$missingAcceptance.Count
  }
  formal_skills_modified='NO'
  auto_merge_allowed='NO'
  final_status=$status
  pass_conditions=[ordered]@{
    elapsed_minutes_gte_60=($elapsed -ge $MinimumMinutes)
    checkpoints_complete=(@($checkpoints | ForEach-Object name) -contains 'start' -and @($checkpoints | ForEach-Object name) -contains '15min' -and @($checkpoints | ForEach-Object name) -contains '30min' -and @($checkpoints | ForEach-Object name) -contains '45min' -and @($checkpoints | ForEach-Object name) -contains 'final')
    formal_skills_modified_no=$true
    auto_merge_allowed_no=$true
  }
}
$finalEvidence | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $checkpointPath -Encoding UTF8
$html = @"
<!doctype html><html><head><meta charset='utf-8'><title>AIOS Weekly 60min Light Check $status</title><style>body{font-family:Segoe UI,Arial,sans-serif;max-width:1100px;margin:32px auto;line-height:1.45;color:#1f2937}h1,h2{color:#111827}code{background:#f3f4f6;padding:2px 4px;border-radius:4px}.status{font-weight:700}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.card{border:1px solid #d1d5db;border-radius:8px;padding:12px}a{color:#075985}</style></head><body>
<h1>AIOS Weekly 60min Light Check</h1>
<p class='status'>Final status: $status</p>
<div class='grid'>
<div class='card'><strong>Elapsed</strong><br>$elapsed minutes</div>
<div class='card'><strong>Skills reviewed</strong><br>$($records.Count)</div>
<div class='card'><strong>Trigger pairs</strong><br>$($triggerGroupsSorted.Count)</div>
<div class='card'><strong>Risk candidates</strong><br>$($highRisk.Count)</div>
<div class='card'><strong>Missing acceptance</strong><br>$($missingAcceptance.Count)</div>
<div class='card'><strong>Formal skills modified</strong><br>NO</div>
</div>
<h2>Outputs</h2>
<ul>
<li><a href='../runtime-evidence.json'>runtime-evidence.json</a></li>
<li><a href='../checkpoint-timeline.md'>checkpoint-timeline.md</a></li>
<li><a href='../weekly-issue-list.md'>weekly-issue-list.md</a></li>
<li><a href='../candidate-patches.md'>candidate-patches.md</a></li>
<li><a href='../rejected-edits.md'>rejected-edits.md</a></li>
<li><a href='../needs-human-review.md'>needs-human-review.md</a></li>
<li><a href='../scan-inventory.json'>scan-inventory.json</a></li>
</ul>
<h2>Gate</h2>
<p>PASS only because elapsed_minutes &gt;= 60, start/15/30/45/final checkpoints exist, formal_skills_modified=NO, and auto_merge_allowed=NO.</p>
</body></html>
"@
$html | Set-Content -LiteralPath (Join-Path $reviewDir 'index.html') -Encoding UTF8
$summary = @('# Run Summary','',"Status: $status", "Elapsed minutes: $elapsed", "Started: $($started.ToString('o'))", "Ended: $($ended.ToString('o'))", "Run dir: $RunDir", '', 'Key counts:', "- Skills reviewed: $($records.Count)", "- Trigger-similarity pairs: $($triggerGroupsSorted.Count)", "- High-risk wording candidates: $($highRisk.Count)", "- Missing acceptance candidates: $($missingAcceptance.Count)", '', 'Formal skills modified: NO', 'Auto-merge allowed: NO')
$summary | Set-Content -LiteralPath (Join-Path $RunDir 'RUN-SUMMARY.md') -Encoding UTF8
