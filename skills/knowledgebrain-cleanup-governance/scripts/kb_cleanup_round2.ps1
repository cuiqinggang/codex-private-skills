param(
  [switch]$PlanOnly,
  [switch]$Execute
)

$ErrorActionPreference = "Continue"
if (-not $PlanOnly -and -not $Execute) {
  Write-Error "Use -PlanOnly or -Execute"
  exit 2
}
if ($PlanOnly -and $Execute) {
  Write-Error "Use only one mode: -PlanOnly or -Execute"
  exit 2
}

$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$ColdRoot = "K:\AI\_COLD_ARCHIVE\knowledgebrain-cleanup-20260702"
$QuarantineRoot = "K:\AI\_QUARANTINE_REBUILDABLE\knowledgebrain-cleanup-20260702"
${REDACTED_SECRET}
${REDACTED_SECRET}
$RecentCutoff = (Get-Date).AddHours(-24)

$Rows = New-Object System.Collections.Generic.List[object]
$MovedRows = New-Object System.Collections.Generic.List[object]
$SkippedRows = New-Object System.Collections.Generic.List[object]

function Convert-ToArchiveRelativePath([string]$Path) {
  $full = [System.IO.Path]::GetFullPath($Path)
  if ($full.StartsWith("K:\AI\", [System.StringComparison]::OrdinalIgnoreCase)) {
    return Join-Path "K_AI" $full.Substring(6).TrimStart("\")
  }
${REDACTED_SECRET}
    return Join-Path "C_Users_A" $full.Substring(11).TrimStart("\")
  }
  $drive = $full.Substring(0, 1).ToUpperInvariant()
  $rest = $full.Substring(3).TrimStart("\")
  if ($drive -eq "K") { return Join-Path "K_DRIVE" $rest }
  if ($drive -eq "C") { return Join-Path "C_DRIVE" $rest }
  return ($full -replace "[:\\]", "_")
}

function Test-CorePath([string]$Path) {
  $leaf = Split-Path -Leaf $Path
  $coreNames = @("SKILL.md", "README.md", "INDEX.md", "ROUTING_MAP.md", "sync_policy.json", "sync_manifest.json")
  if ($coreNames -contains $leaf) { return $true }
  if ($leaf -like "*.ps1") { return $true }
  if ($Path -match "\\\.git($|\\)") { return $true }
  return $false
}

function Get-PathStats([string]$Path) {
  if (-not (Test-Path -LiteralPath $Path)) {
    return [pscustomobject]@{ Bytes = 0L; FileCount = 0; Latest = $null }
  }
  $item = Get-Item -LiteralPath $Path -Force -ErrorAction SilentlyContinue
  if ($null -eq $item) {
    return [pscustomobject]@{ Bytes = 0L; FileCount = 0; Latest = $null }
  }
  if (-not $item.PSIsContainer) {
    return [pscustomobject]@{ Bytes = [int64]$item.Length; FileCount = 1; Latest = $item.LastWriteTime }
  }
  $bytes = [int64]0
  $count = 0
  $latest = $item.LastWriteTime
  Get-ChildItem -LiteralPath $Path -Force -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object {
    $bytes += [int64]$_.Length
    $count++
    if ($_.LastWriteTime -gt $latest) { $latest = $_.LastWriteTime }
  }
  return [pscustomobject]@{ Bytes = $bytes; FileCount = $count; Latest = $latest }
}

function Add-PlanRow(
  [string]$Classification,
  [string]$SourcePath,
  [string]$ArchiveRoot,
  [string]$Reason
) {
  $moveId = "KB2-{0:D5}" -f ($Rows.Count + 1)
  if (-not (Test-Path -LiteralPath $SourcePath)) {
    $Rows.Add([pscustomobject]@{
      move_id=$moveId; classification=$Classification; source_path=$SourcePath; target_path="";
      bytes=0; file_count=0; latest_write_time=""; reason=$Reason; status="SKIPPED_NOT_FOUND";
      rollback_command=""
    })
    return
  }
  if (Test-CorePath $SourcePath) {
    $Rows.Add([pscustomobject]@{
      move_id=$moveId; classification=$Classification; source_path=$SourcePath; target_path="";
      bytes=0; file_count=0; latest_write_time=""; reason=$Reason; status="SKIPPED_CORE_FILE";
      rollback_command=""
    })
    return
  }

  $stats = Get-PathStats $SourcePath
  if ($stats.Latest -ne $null -and $stats.Latest -gt $RecentCutoff) {
    $Rows.Add([pscustomobject]@{
      move_id=$moveId; classification=$Classification; source_path=$SourcePath; target_path="";
      bytes=$stats.Bytes; file_count=$stats.FileCount; latest_write_time=$stats.Latest.ToString("yyyy-MM-dd HH:mm:ss");
      reason=$Reason; status="SKIPPED_ACTIVE_RECENT"; rollback_command=""
    })
    return
  }

  $relative = Convert-ToArchiveRelativePath $SourcePath
  $target = Join-Path $ArchiveRoot $relative
  $rollback = "Move-Item -LiteralPath '$target' -Destination '$SourcePath'"
  $Rows.Add([pscustomobject]@{
    move_id=$moveId; classification=$Classification; source_path=$SourcePath; target_path=$target;
    bytes=$stats.Bytes; file_count=$stats.FileCount; latest_write_time=if ($stats.Latest) { $stats.Latest.ToString("yyyy-MM-dd HH:mm:ss") } else { "" };
    reason=$Reason; status="PLANNED"; rollback_command=$rollback
  })
}

function Move-PlannedRow($row) {
  if ($row.status -ne "PLANNED") { return $row }
  try {
    $targetParent = Split-Path -Parent $row.target_path
    New-Item -ItemType Directory -Force -Path $targetParent | Out-Null
    if (Test-Path -LiteralPath $row.target_path) {
      $row.status = "SKIPPED_TARGET_EXISTS"
      return $row
    }
    Move-Item -LiteralPath $row.source_path -Destination $row.target_path -Force
    $row.status = "MOVED"
    return $row
  } catch {
    $row.status = "ERROR_MOVE_FAILED: $($_.Exception.Message)"
    return $row
  }
}

function Add-RebuildableDirs([string[]]$Roots) {
  $names = @("node_modules", "dist", "build", ".cache", "__pycache__", "tmp", "temp", "logs")
  foreach ($root in $Roots) {
    if (-not (Test-Path -LiteralPath $root)) { continue }
    foreach ($name in $names) {
      Get-ChildItem -LiteralPath $root -Directory -Force -Recurse -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -eq $name -and $_.FullName -notmatch "\\\.git($|\\)" } |
        ForEach-Object {
          Add-PlanRow "ISOLATE_REBUILDABLE" $_.FullName $QuarantineRoot "rebuildable runtime/cache/build directory"
        }
    }
  }
}

function Remove-ChildDuplicatePlans {
  $kept = New-Object System.Collections.Generic.List[object]
  foreach ($row in ($Rows | Sort-Object { $_.source_path.Length })) {
    if ($row.status -ne "PLANNED") {
      $kept.Add($row)
      continue
    }
    $isCovered = $false
    foreach ($parent in ($kept | Where-Object { $_.status -eq "PLANNED" })) {
      $parentPath = $parent.source_path.TrimEnd("\")
      if ($row.source_path.Length -gt $parentPath.Length -and $row.source_path.StartsWith($parentPath + "\", [System.StringComparison]::OrdinalIgnoreCase)) {
        $isCovered = $true
        break
      }
    }
    if ($isCovered) {
      $row.status = "SKIPPED_PARENT_PLANNED"
    }
    $kept.Add($row)
  }
  $Rows.Clear()
  foreach ($r in $kept) { $Rows.Add($r) }
}

function Add-CodexDateColdArchive([string[]]$DateRoots) {
  $dirNames = @("assets", "evidence", "screenshots", "reports", "runs", "outputs", "media", "captures")
  $mediaExts = @(".zip", ".7z", ".rar", ".mp4", ".mov", ".avi", ".mkv", ".png", ".jpg", ".jpeg", ".webp", ".gif")
  foreach ($dateRoot in $DateRoots) {
    if (-not (Test-Path -LiteralPath $dateRoot)) { Add-PlanRow "COLD_ARCHIVE" $dateRoot $ColdRoot "date root missing"; continue }
    foreach ($name in $dirNames) {
      Get-ChildItem -LiteralPath $dateRoot -Directory -Force -Recurse -ErrorAction SilentlyContinue |
        Where-Object { $dirNames -contains $_.Name -and $_.FullName -notmatch "\\\.git($|\\)" } |
        ForEach-Object {
          Add-PlanRow "COLD_ARCHIVE" $_.FullName $ColdRoot "old Codex run artifact directory"
        }
    }
    Get-ChildItem -LiteralPath $dateRoot -File -Force -Recurse -ErrorAction SilentlyContinue |
      Where-Object { $mediaExts -contains $_.Extension.ToLowerInvariant() -and $_.FullName -notmatch "\\\.git($|\\)" } |
      ForEach-Object {
        Add-PlanRow "COLD_ARCHIVE" $_.FullName $ColdRoot "old Codex media/binary delivery file"
      }
  }
}

function Add-SkillAssetTargets([string[]]$SkillRoots) {
  $directNames = @("assets", "evidence", "screenshots", "visual-evidence", "original-video", "original-package", "video_keyframes", "90-ARCHIVE", "backups")
  foreach ($skill in $SkillRoots) {
    if (-not (Test-Path -LiteralPath $skill)) { Add-PlanRow "COLD_ARCHIVE" $skill $ColdRoot "skill root missing"; continue }
    foreach ($name in $directNames) {
      $p = Join-Path $skill $name
      if (Test-Path -LiteralPath $p) {
        Add-PlanRow "COLD_ARCHIVE" $p $ColdRoot "skill bulky asset/evidence directory"
      }
    }
    $reports = Join-Path $skill "reports"
    if (Test-Path -LiteralPath $reports) {
      Get-ChildItem -LiteralPath $reports -Directory -Force -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -like "creation-*" } |
        ForEach-Object { Add-PlanRow "COLD_ARCHIVE" $_.FullName $ColdRoot "old skill creation report directory" }
    }
  }
}

function Write-SkillPointers {
  param([object[]]$RowsForPointers)
  $skillRoots = @(
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
    "K:\AI\skills\digital-product-indie-site",
    "K:\AI\skills\hermes-windows-native-screen-capture",
    "K:\AI\skills\ai-company-evolving-revenue-portfolio"
  )
  foreach ($skill in $skillRoots) {
    if (-not (Test-Path -LiteralPath $skill)) { continue }
    $moved = @($RowsForPointers | Where-Object { $_.status -eq "MOVED" -and $_.source_path.StartsWith($skill, [System.StringComparison]::OrdinalIgnoreCase) })
    if ($moved.Count -eq 0) { continue }
    $pointer = Join-Path $skill "ARCHIVED_ASSETS_POINTER.md"
    $lines = New-Object System.Collections.Generic.List[string]
    $lines.Add("# Archived Assets Pointer")
    $lines.Add("")
    $lines.Add("Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')")
    $lines.Add("")
    $lines.Add("Some bulky assets/evidence for this skill were moved to cold archive during Knowledge Brain cleanup round 2.")
    $lines.Add("")
    $lines.Add("Manifest:")
    $lines.Add("")
    $lines.Add($ManifestPath)
    $lines.Add("")
    $lines.Add("Moved items:")
    foreach ($r in $moved) { $lines.Add("- $($r.source_path) -> $($r.target_path)") }
    $lines.Add("")
    $lines.Add("Rollback: use the rollback_command column in the manifest.")
    $lines -join "`r`n" | Set-Content -LiteralPath $pointer -Encoding UTF8
  }
}

function Write-ObsidianPointer {
  param([object[]]$RowsForPointer)
  $pointer = "K:\AI\obsidian-vaults\AI-COMPANY-KNOWLEDGE-OS\01_META\Archived-Assets-Pointer-20260702.md"
  $moved = @($RowsForPointer | Where-Object { $_.status -eq "MOVED" -and $_.source_path.StartsWith("K:\AI\obsidian-vaults\AI-COMPANY-KNOWLEDGE-OS", [System.StringComparison]::OrdinalIgnoreCase) })
  $lines = New-Object System.Collections.Generic.List[string]
  $lines.Add("# Archived Assets Pointer 20260702")
  $lines.Add("")
  $lines.Add("Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')")
  $lines.Add("")
  $lines.Add("Knowledge Brain cleanup round 2 moved only bulky attachments/evidence/backups. Obsidian note bodies were kept in place.")
  $lines.Add("")
  $lines.Add("Manifest:")
  $lines.Add("")
  $lines.Add($ManifestPath)
  $lines.Add("")
  $lines.Add("Moved items:")
  if ($moved.Count -eq 0) { $lines.Add("- None") } else { foreach ($r in $moved) { $lines.Add("- $($r.source_path) -> $($r.target_path)") } }
  $lines.Add("")
  $lines.Add("Rollback: use the rollback_command column in the manifest.")
  $lines -join "`r`n" | Set-Content -LiteralPath $pointer -Encoding UTF8
}

$mediaWorkspaceDirs = @(
  "K:\AI\workspaces\AI-VIDEO-REPLICA-BLENDER-CODEX-15S-P3-SHOT-STRUCTURE-20260529",
  "K:\AI\workspaces\AI-VIDEO-REPLICA-R1-MOTHER-PLATE-20260529",
  "K:\AI\workspaces\AI-VIDEO-REPLICA-BLENDER-CODEX-5S-P2-QUALITY-ENHANCE-20260529",
  "K:\AI\workspaces\AI-VIDEO-REPLICA-BLENDER-CODEX-5S-VERIFY-20260529",
  "K:\AI\workspaces\AI-SPACE-CURTAIN-A0-5-RESCREEN-20260530",
  "K:\AI\workspaces\AI-SPACE-CURTAIN-A0-6-TARGETED-RESCREEN-20260531",
  "K:\AI\workspaces\AI-SPACE-CURTAIN-A0-7-MICRO-RESCREEN-20260531",
  "K:\AI\workspaces\AI-PROMO-PPT-STYLE-VIDEO-20260531",
  "K:\AI\workspaces\AI-SPACE-CURTAIN-A0-ASSET-SCOUT-20260530"
)
foreach ($p in $mediaWorkspaceDirs) {
  Add-PlanRow "COLD_ARCHIVE" $p $ColdRoot "explicit old media/video workspace candidate"
}

Add-RebuildableDirs @(
  "K:\AI\workspaces",
${REDACTED_SECRET}
  "K:\AI\tools\agent-skills-hotlist"
)

Add-CodexDateColdArchive @(
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
)

Add-SkillAssetTargets @(
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
  "K:\AI\skills\digital-product-indie-site",
  "K:\AI\skills\hermes-windows-native-screen-capture",
  "K:\AI\skills\ai-company-evolving-revenue-portfolio"
)

Add-PlanRow "COLD_ARCHIVE" "K:\AI\obsidian-vaults\AI-COMPANY-KNOWLEDGE-OS\05_EVIDENCE_REPORTS" $ColdRoot "Obsidian bulky evidence reports"
foreach ($p in @(
  "K:\AI\obsidian-vaults\AI-COMPANY-KNOWLEDGE-OS\assets",
  "K:\AI\obsidian-vaults\AI-COMPANY-KNOWLEDGE-OS\screenshots",
  "K:\AI\obsidian-vaults\AI-COMPANY-KNOWLEDGE-OS\backups"
)) {
  if (Test-Path -LiteralPath $p) { Add-PlanRow "COLD_ARCHIVE" $p $ColdRoot "Obsidian bulky attachment directory" }
}

Remove-ChildDuplicatePlans
$Rows | Export-Csv -LiteralPath $ManifestPath -NoTypeInformation -Encoding UTF8

if ($Execute) {
  New-Item -ItemType Directory -Force -Path $ColdRoot | Out-Null
  New-Item -ItemType Directory -Force -Path $QuarantineRoot | Out-Null
  for ($i = 0; $i -lt $Rows.Count; $i++) {
    $Rows[$i] = Move-PlannedRow $Rows[$i]
  }
  $Rows | Export-Csv -LiteralPath $ManifestPath -NoTypeInformation -Encoding UTF8
  Write-SkillPointers -RowsForPointers $Rows
  Write-ObsidianPointer -RowsForPointer $Rows
}

$movedCount = @($Rows | Where-Object { $_.status -eq "MOVED" }).Count
$plannedCount = @($Rows | Where-Object { $_.status -eq "PLANNED" }).Count
$skippedCount = @($Rows | Where-Object { $_.status -like "SKIPPED*" }).Count
$errorCount = @($Rows | Where-Object { $_.status -like "ERROR*" }).Count
$movedBytes = [int64]0
($Rows | Where-Object { $_.status -eq "MOVED" }) | ForEach-Object { $movedBytes += [int64]$_.bytes }
$movedFiles = 0
($Rows | Where-Object { $_.status -eq "MOVED" }) | ForEach-Object { $movedFiles += [int]$_.file_count }

$md = New-Object System.Collections.Generic.List[string]
$md.Add("# Knowledge Brain Cleanup Round 2 Report")
$md.Add("")
$md.Add("Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')")
$md.Add("Mode: $(if ($Execute) { 'EXECUTE' } else { 'PLAN_ONLY' })")
$md.Add("")
$md.Add("## Result")
$md.Add("")
if ($Execute) {
  if ($errorCount -gt 0 -or $skippedCount -gt 0) { $md.Add("RESULT=PASS_CLEANED_WITH_SKIPS") } else { $md.Add("RESULT=PASS_CLEANED") }
} else {
  $md.Add("RESULT=PLAN_READY")
}
$md.Add("")
$md.Add("## Counts")
$md.Add("")
$md.Add("- Total manifest rows: $($Rows.Count)")
$md.Add("- Planned rows: $plannedCount")
$md.Add("- Moved rows: $movedCount")
$md.Add("- Skipped rows: $skippedCount")
$md.Add("- Error rows: $errorCount")
$md.Add("- Moved files: $movedFiles")
$md.Add("- Moved bytes: $movedBytes")
$md.Add("- Moved GB: $([math]::Round($movedBytes / 1GB, 3))")
$md.Add("")
$md.Add("## Locations")
$md.Add("")
$md.Add("- Cold archive: $ColdRoot")
$md.Add("- Rebuildable quarantine: $QuarantineRoot")
$md.Add("- Manifest: $ManifestPath")
$md.Add("")
$md.Add("## Rules Applied")
$md.Add("")
$md.Add("- No permanent deletion.")
$md.Add("- Original relative paths preserved under archive/quarantine roots.")
$md.Add("- Git metadata skipped.")
$md.Add("- Core skill files, docs, policy files, and scripts skipped.")
$md.Add("- Items modified in the last 24 hours skipped as active/recent.")
$md.Add("")
$md.Add("## Status Breakdown")
$md.Add("")
$Rows | Group-Object status | Sort-Object Count -Descending | ForEach-Object {
  $md.Add("- $($_.Name): $($_.Count)")
}
$md.Add("")
$md.Add("## Skipped Items")
$md.Add("")
foreach ($r in ($Rows | Where-Object { $_.status -like "SKIPPED*" -or $_.status -like "ERROR*" } | Select-Object -First 200)) {
  $md.Add("- $($r.status): $($r.source_path) | $($r.reason)")
}
$md.Add("")
$md.Add("## Rollback")
$md.Add("")
$md.Add("Use the rollback_command column in the manifest. Each moved path can be restored to its source path without flattening.")
$md.Add("")
$md.Add("## Verification Still Required")
$md.Add("")
$md.Add("After execute mode, run:")
$md.Add("")
$md.Add("- K:\AI\knowledge-brain\tools\kb_audit_all_sources.ps1")
$md.Add("- K:\AI\knowledge-brain\tools\kb_health_check.ps1")
$md.Add("- K:\AI\knowledge-brain\tools\kb_light_sync_v2.ps1 twice")
$md -join "`r`n" | Set-Content -LiteralPath $ReportPath -Encoding UTF8

"MODE=$(if ($Execute) { 'EXECUTE' } else { 'PLAN_ONLY' })"
"MANIFEST=$ManifestPath"
"REPORT=$ReportPath"
"ROWS=$($Rows.Count)"
"MOVED=$movedCount"
"PLANNED=$plannedCount"
"SKIPPED=$skippedCount"
"ERROR=$errorCount"
"MOVED_FILES=$movedFiles"
"MOVED_GB=$([math]::Round($movedBytes / 1GB, 3))"
