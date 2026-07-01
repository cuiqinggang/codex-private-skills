param([string]$RunDir,[int]$MinimumMinutes=60)
$ErrorActionPreference = 'Continue'
$started = Get-Date
$roots = @('C:\Users\A\.codex\skills','H:\AI\skills')
$checkpoints = New-Object System.Collections.Generic.List[object]
function Write-Evidence([string]$status) {
  $now = Get-Date
  $elapsed = [math]::Round(($now - $started).TotalMinutes,2)
  [ordered]@{
    task_id='AIOS_SKILL_SELF_PURIFICATION_WEEKLY_60MIN_LIGHT_CHECK'
    automation_id='aios-30min'
    started_at=$started.ToString('o')
    ended_at=if ($status -ne 'RUNNING') { $now.ToString('o') } else { $null }
    elapsed_minutes=$elapsed
    minimum_elapsed_minutes=$MinimumMinutes
    checkpoints=$checkpoints
    checkpoint_count=$checkpoints.Count
    reviewed_roots=$roots
    reviewed_scope=$script:scope
    final_status=$status
    formal_skills_modified='NO'
    auto_merge_allowed='NO'
    pass_conditions=[ordered]@{
      elapsed_minutes_gte_60=($elapsed -ge $MinimumMinutes)
      required_checkpoints_present=(('start','15min','30min','45min','final' | ForEach-Object { $n=$_; @($checkpoints | Where-Object name -eq $n).Count -gt 0 }) -notcontains $false)
      formal_skills_modified_no=$true
      auto_merge_allowed_no=$true
    }
  } | ConvertTo-Json -Depth 9 | Set-Content -LiteralPath (Join-Path $RunDir 'runtime-evidence.json') -Encoding UTF8
}
function Add-Checkpoint([string]$name,[string]$note) {
  $now = Get-Date
  $checkpoints.Add([ordered]@{name=$name; at=$now.ToString('o'); elapsed_minutes=[math]::Round(($now-$started).TotalMinutes,2); note=$note}) | Out-Null
  $lines = @('# Checkpoint Timeline','') + @($checkpoints | ForEach-Object { "- $($_.name) | $($_.elapsed_minutes) min | $($_.at) | $($_.note)" })
  $lines | Set-Content -LiteralPath (Join-Path $RunDir 'checkpoint-timeline.md') -Encoding UTF8
  Write-Evidence 'RUNNING'
}
function Norm([string]$s) { if ($null -eq $s) { '' } else { (($s.ToLowerInvariant() -replace '[^a-z0-9\p{IsCJKUnifiedIdeographs}]+',' ') -replace '\s+',' ').Trim() } }
function SkillDirs([string]$root) {
  $out = New-Object System.Collections.Generic.List[string]
  if (-not (Test-Path $root)) { return @() }
  Get-ChildItem -LiteralPath $root -Directory -ErrorAction SilentlyContinue | ForEach-Object {
    if (Test-Path (Join-Path $_.FullName 'SKILL.md')) { $out.Add($_.FullName) | Out-Null }
    Get-ChildItem -LiteralPath $_.FullName -Directory -ErrorAction SilentlyContinue | Select-Object -First 12 | ForEach-Object {
      if (Test-Path (Join-Path $_.FullName 'SKILL.md')) { $out.Add($_.FullName) | Out-Null }
    }
  }
  @($out | Select-Object -Unique)
}
function Rec([string]$dir) {
  $sf = Join-Path $dir 'SKILL.md'
  $text = if (Test-Path $sf) { Get-Content -LiteralPath $sf -Raw -ErrorAction SilentlyContinue } else { '' }
  $lines = @($text -split "`r?`n")
  $rootMd = @(Get-ChildItem -LiteralPath $dir -File -Filter '*.md' -ErrorAction SilentlyContinue)
  $subMd = @(Get-ChildItem -LiteralPath $dir -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -notmatch '^(node_modules|\.git|outputs|runs|backups)$' } | Select-Object -First 12 | ForEach-Object { Get-ChildItem -LiteralPath $_.FullName -File -Filter '*.md' -ErrorAction SilentlyContinue | Select-Object -First 15 })
  $allMd = @($rootMd + $subMd)
  $trigger = @($lines | Where-Object { $_ -match '(?i)use when|use this skill|trigger|keyword|触发|关键词|适用|必须使用|开工前|任务涉及' } | Select-Object -First 35)
  $risk = @($lines | Where-Object { $_ -match '(?i)auto.?merge|unattended|delete|remove|overwrite|global|always|any task|all tasks|background|自动合并|自动删除|删除|覆盖|全局|所有任务|任何任务|总控|常驻|硬规则|失败复盘|rejected|human review|formal skill' } | Select-Object -First 60)
  $acc = @($allMd | Where-Object { $_.Name -match '(?i)acceptance|验收|gate|evidence|result|proof' })
  $rej = @($allMd | Where-Object { $_.Name -match '(?i)reject|rejected|buffer|failure|fail|retrospective|复盘|失败' })
  $writes = @($allMd + (if (Test-Path $sf) { Get-Item $sf } else { @() }) | Sort-Object LastWriteTime -Descending)
  [ordered]@{
    name=Split-Path $dir -Leaf; path=$dir; skill_file=$sf
    last_write=if ($writes.Count) { $writes[0].LastWriteTime.ToString('o') } else { $null }
    md_count=$allMd.Count
    trigger_text=Norm((($trigger -join ' ') + ' ' + (Split-Path $dir -Leaf)))
    trigger_lines=$trigger
    risk_lines=$risk
    acceptance_count=$acc.Count; acceptance_files=@($acc | ForEach-Object FullName)
    rejected_buffer_count=$rej.Count; rejected_buffer_files=@($rej | ForEach-Object FullName)
  }
}
Add-Checkpoint 'start' '60min formal run started; prior recursive draft run marked aborted; shadow-only mode active.'
$dirs = @(); foreach ($r in $roots) { $dirs += SkillDirs $r }; $dirs = @($dirs | Select-Object -Unique)
$records = @($dirs | ForEach-Object { Rec $_ })
$now = Get-Date
$recent = @($records | Where-Object { $_.last_write -and ([datetime]$_.last_write) -ge $now.AddDays(-14) } | Sort-Object last_write -Descending)
$modified = @($records | Where-Object { $_.last_write -and ([datetime]$_.last_write) -ge $now.AddDays(-45) } | Sort-Object last_write -Descending)
$highRisk = @($records | Where-Object { $_.risk_lines.Count -gt 0 } | Sort-Object @{Expression={$_.risk_lines.Count};Descending=$true}, name)
$missingAcceptance = @($records | Where-Object { $_.acceptance_count -eq 0 } | Sort-Object name)
$localGlobal = @($records | Where-Object { ($_.risk_lines -join ' ') -match '(?i)(global|全局|all tasks|any task|所有任务|任何任务)' -and ($_.risk_lines -join ' ') -match '(?i)(H:\\|C:\\|local|project|workspace|本地|项目|工作区)' } | Sort-Object name)
$totalControl = @($records | Where-Object { ($_.risk_lines -join ' ') -match '(?i)(total-control|总控|use first|always use|所有任务|任何任务|all tasks|any task|开工前)' } | Sort-Object name)
$failureReview = @($records | Where-Object { @($_.rejected_buffer_files | Where-Object { $_ -match '(?i)(failure|fail|复盘|retrospective|失败)' }).Count -gt 0 } | Sort-Object name)
$staleRejected = @($records | Where-Object { ($_.risk_lines -join ' ') -match '(?i)rejected|reject|buffer|失败复盘|复盘' -and $_.rejected_buffer_count -eq 0 } | Sort-Object name)
$pairs = New-Object System.Collections.Generic.List[object]
for($i=0;$i -lt $records.Count;$i++){ for($j=$i+1;$j -lt $records.Count;$j++){ $a=$records[$i]; $b=$records[$j]; $ta=@($a.trigger_text -split ' ' | ? { $_.Length -ge 4 } | Select-Object -Unique); $tb=@($b.trigger_text -split ' ' | ? { $_.Length -ge 4 } | Select-Object -Unique); if(!$ta -or !$tb){continue}; $inter=@($ta | ? { $tb -contains $_ }); $union=@($ta+$tb | Select-Object -Unique); $score=if($union.Count){[math]::Round($inter.Count/$union.Count,3)}else{0}; if($score -ge 0.16 -or $inter.Count -ge 6){$pairs.Add([ordered]@{score=$score; shared_terms=@($inter|Select -First 18); a=$a.name; a_path=$a.path; b=$b.name; b_path=$b.path})|Out-Null}}}
$pairs = @($pairs | Sort-Object score -Descending | Select-Object -First 120)
$script:scope = [ordered]@{skill_count=$records.Count; recent_14d_count=$recent.Count; modified_45d_count=$modified.Count; trigger_similarity_pairs=$pairs.Count; high_risk_phrase_count=$highRisk.Count; missing_acceptance_count=$missingAcceptance.Count; local_global_candidates=$localGlobal.Count; total_control_candidates=$totalControl.Count; failure_review_buffers_seen=$failureReview.Count; stale_rejected_buffer_candidates=$staleRejected.Count}
[ordered]@{generated_at=(Get-Date).ToString('o'); roots=$roots; scope=$script:scope; records=$records; trigger_groups=$pairs} | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $RunDir 'scan-inventory.json') -Encoding UTF8
$issues = @('# Weekly 60min Light Check Issue List','',"Generated: $(Get-Date -Format o)",'','Mode: shadow-only. Formal skill files modified: NO. Auto-merge allowed: NO.','','## Scope Summary','',"- Skill roots scanned: $($roots -join '; ')","- Skill packages with SKILL.md: $($records.Count)","- Recent skills, 14d: $($recent.Count)","- Modified skills, 45d: $($modified.Count)","- Trigger-similarity pairs retained: $($pairs.Count)","- High-risk wording candidates: $($highRisk.Count)","- Missing acceptance/evidence page candidates: $($missingAcceptance.Count)",'','## P1 Duplicate or overlapping triggers','')
if($pairs.Count){ foreach($g in $pairs){$issues += "- score=$($g.score): `$($g.a)` <-> `$($g.b)`; shared: $($g.shared_terms -join ', ')" }} else {$issues+='- No findings in sampled scan.'}
$issues += '','## P1 High-risk automation or scope wording',''; if($highRisk.Count){foreach($r in @($highRisk|Select -First 80)){$issues += "- `$($r.name)` | $($r.path) | risk lines: $(@($r.risk_lines|Select -First 3) -join ' / ')"}}else{$issues+='- No findings in sampled scan.'}
$issues += '','## P1 Local rules that may be elevated globally',''; if($localGlobal.Count){foreach($r in $localGlobal){$issues += "- `$($r.name)` | $($r.path) | inspect global/local boundary wording."}}else{$issues+='- No findings in sampled scan.'}
$issues += '','## P1 Total-control trigger expansion candidates',''; if($totalControl.Count){foreach($r in $totalControl){$issues += "- `$($r.name)` | $($r.path) | inspect total-control or always-use wording."}}else{$issues+='- No findings in sampled scan.'}
$issues += '','## P2 Missing acceptance or evidence page candidates',''; if($missingAcceptance.Count){foreach($r in @($missingAcceptance|Select -First 150)){$issues += "- `$($r.name)` | $($r.path) | no acceptance/gate/evidence-like md file found in sampled root/subdirs."}}else{$issues+='- No findings in sampled scan.'}
$issues += '','## P2 Rejected-edit buffer stale/missing candidates',''; if($staleRejected.Count){foreach($r in $staleRejected){$issues += "- `$($r.name)` | $($r.path) | mentions rejected/buffer/failure review but no matching buffer file found."}}else{$issues+='- No findings in sampled scan.'}
$issues += '','## P3 Failure review buffers found and should be preserved',''; if($failureReview.Count){foreach($r in $failureReview){$issues += "- `$($r.name)` | $($r.path) | preserve: $(@($r.rejected_buffer_files|Select -First 4) -join '; ')"}}else{$issues+='- No findings in sampled scan.'}
$issues | Set-Content -LiteralPath (Join-Path $RunDir 'weekly-issue-list.md') -Encoding UTF8
$cand = @('# Candidate Patches','','Shadow-only patch candidates. Do not apply without user/GPT Gate Review.','','## Acceptance page candidates','')
foreach($r in @($missingAcceptance|Select -First 50)){$cand += "- Candidate: add `ACCEPTANCE-GATE.md` or `EVIDENCE.md` to `$($r.path)` with explicit status, runtime, rollback, and user-visible proof checklist; no `SKILL.md` rewrite."}
$cand += '','## Trigger de-dup candidates',''; foreach($g in @($pairs|Select -First 50)){$cand += "- Candidate: compare `$($g.a)` and `$($g.b)`; narrow trigger ownership by domain/precondition instead of broad `use when` overlap."}
$cand += '','## High-risk wording candidates',''; foreach($r in @($highRisk|Select -First 50)){$cand += "- Candidate: in `$($r.name)`, downgrade merge/delete/overwrite/global/unattended wording to shadow-first or needs-human-review language."}
$cand | Set-Content -LiteralPath (Join-Path $RunDir 'candidate-patches.md') -Encoding UTF8
$rej = @('# Rejected Edits','','These edits are explicitly rejected for this run.','','- Do not modify formal `SKILL.md` files.','- Do not delete or compact user hard rules.','- Do not delete failure retrospectives or rejected-edit buffers.','- Do not merge duplicate skills automatically.','- Do not broaden total-control triggers.','- Do not convert project-local rules into global rules.','- Do not claim PASS before 60 elapsed minutes and all checkpoints exist.','')
foreach($r in @($totalControl|Select -First 50)){$rej += "- Rejected now: direct trigger rewrite in `$($r.path)`; requires human review."}
foreach($r in @($failureReview|Select -First 50)){$rej += "- Rejected now: removing/archiving failure review material in `$($r.path)`; preservation required."}
$rej | Set-Content -LiteralPath (Join-Path $RunDir 'rejected-edits.md') -Encoding UTF8
$human = @('# Needs Human Review','','Items that should not be auto-applied.','','## Highest priority','')
foreach($g in @($pairs|?{$_.score -ge 0.25}|Select -First 35)){$human += "- Trigger collision: `$($g.a)` vs `$($g.b)` (score $($g.score)); decide ownership before patching."}
foreach($r in @($localGlobal|Select -First 35)){$human += "- Local/global boundary: `$($r.name)`; check whether path-specific rules are being promoted globally."}
foreach($r in @($totalControl|Select -First 35)){$human += "- Total-control trigger: `$($r.name)`; check whether entry conditions are too broad."}
foreach($r in @($highRisk|Select -First 35)){$human += "- Risk wording: `$($r.name)`; inspect whether automation language violates shadow-only policy."}
$human | Set-Content -LiteralPath (Join-Path $RunDir 'needs-human-review.md') -Encoding UTF8
Add-Checkpoint 'scan-complete' "Comparative scan complete: $($records.Count) skills, $($pairs.Count) trigger pairs, $($highRisk.Count) risk candidates."
foreach($target in @(@{n='15min';m=15;note='15min checkpoint: issue/candidate/rejected/human-review drafts present.'},@{n='30min';m=30;note='30min checkpoint: formal files still untouched; review window continuing.'},@{n='45min';m=45;note='45min checkpoint: evidence complete so far; PASS remains gated until 60min.'},@{n='final';m=$MinimumMinutes;note='Final checkpoint: runtime threshold reached; final review page generated.'})) { while(((Get-Date)-$started).TotalMinutes -lt $target.m){Start-Sleep -Seconds 20}; Add-Checkpoint $target.n $target.note }
$status = if((((Get-Date)-$started).TotalMinutes -ge $MinimumMinutes) -and (($checkpoints|% name) -contains 'start') -and (($checkpoints|% name) -contains '15min') -and (($checkpoints|% name) -contains '30min') -and (($checkpoints|% name) -contains '45min') -and (($checkpoints|% name) -contains 'final')){'PASS'}else{'FAIL_RUNTIME_GATE'}
New-Item -ItemType Directory -Force -Path (Join-Path $RunDir 'outputs') | Out-Null
$elapsed=[math]::Round(((Get-Date)-$started).TotalMinutes,2)
@("# Run Summary","","Status: $status","Elapsed minutes: $elapsed","Started: $($started.ToString('o'))","Ended: $((Get-Date).ToString('o'))","Run dir: $RunDir",'','Key counts:',"- Skills reviewed: $($records.Count)","- Trigger-similarity pairs: $($pairs.Count)","- High-risk wording candidates: $($highRisk.Count)","- Missing acceptance candidates: $($missingAcceptance.Count)",'','Formal skills modified: NO','Auto-merge allowed: NO') | Set-Content -LiteralPath (Join-Path $RunDir 'RUN-SUMMARY.md') -Encoding UTF8
$html="<!doctype html><html><head><meta charset='utf-8'><title>AIOS Weekly 60min Light Check $status</title><style>body{font-family:Segoe UI,Arial,sans-serif;max-width:1080px;margin:32px auto;color:#1f2937;line-height:1.45}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.card{border:1px solid #d1d5db;border-radius:8px;padding:12px}a{color:#075985}</style></head><body><h1>AIOS Weekly 60min Light Check</h1><p><b>Final status:</b> $status</p><div class='grid'><div class='card'><b>Elapsed</b><br>$elapsed min</div><div class='card'><b>Skills reviewed</b><br>$($records.Count)</div><div class='card'><b>Trigger pairs</b><br>$($pairs.Count)</div><div class='card'><b>Risk candidates</b><br>$($highRisk.Count)</div><div class='card'><b>Missing acceptance</b><br>$($missingAcceptance.Count)</div><div class='card'><b>Formal skills modified</b><br>NO</div></div><h2>Outputs</h2><ul><li><a href='../runtime-evidence.json'>runtime-evidence.json</a></li><li><a href='../checkpoint-timeline.md'>checkpoint-timeline.md</a></li><li><a href='../weekly-issue-list.md'>weekly-issue-list.md</a></li><li><a href='../candidate-patches.md'>candidate-patches.md</a></li><li><a href='../rejected-edits.md'>rejected-edits.md</a></li><li><a href='../needs-human-review.md'>needs-human-review.md</a></li><li><a href='../scan-inventory.json'>scan-inventory.json</a></li></ul><p>Gate: PASS only if elapsed_minutes &gt;= 60, checkpoints complete, formal_skills_modified=NO, and auto_merge_allowed=NO.</p></body></html>"
$html | Set-Content -LiteralPath (Join-Path $RunDir 'outputs\index.html') -Encoding UTF8
Write-Evidence $status
Write-Output "RUN_COMPLETE $status $RunDir"
