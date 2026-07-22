$ErrorActionPreference = 'Stop'

${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

function Normalize-Key {
    param([string]$Value)
    if ([string]::IsNullOrWhiteSpace($Value)) { return '' }
    $text = $Value.Trim()
    $text = $text.Trim('"')
    $text = $text.Trim("'")
    return $text.ToLowerInvariant()
}

function Get-FrontmatterName {
    param([string]$SkillMdPath)
    if (-not (Test-Path -LiteralPath $SkillMdPath)) { return '' }
    $lines = Get-Content -LiteralPath $SkillMdPath -TotalCount 80 -ErrorAction Stop
    $inside = $false
    foreach ($line in $lines) {
        if ($line -match '^\s*---\s*$') {
            if (-not $inside) { $inside = $true; continue }
            break
        }
        if ($inside -and $line -match '^\s*name\s*:\s*(.+?)\s*$') {
            $name = $Matches[1].Trim()
            $name = $name.Trim('"')
            $name = $name.Trim("'")
            return $name
        }
    }
    foreach ($line in $lines) {
        if ($line -match '^\s*name\s*:\s*(.+?)\s*$') {
            $name = $Matches[1].Trim()
            $name = $name.Trim('"')
            $name = $name.Trim("'")
            return $name
        }
    }
    return ''
}

function Get-SkillTextSample {
    param([string]$PreservePath, [string]$SkillPath)
    $chunks = New-Object System.Collections.Generic.List[string]
    foreach ($p in @($PreservePath, $SkillPath)) {
        if (-not [string]::IsNullOrWhiteSpace($p)) { $chunks.Add($p) }
    }
    if (Test-Path -LiteralPath $PreservePath) {
        $files = Get-ChildItem -LiteralPath $PreservePath -Recurse -File -ErrorAction SilentlyContinue |
            Where-Object { $_.Extension -in @('.md', '.txt', '.ps1', '.py', '.sh', '.json', '.yaml', '.yml') } |
            Sort-Object FullName
        foreach ($file in $files) {
            $chunks.Add($file.FullName)
            try {
                if ($file.Length -lt 262144) {
                    $chunks.Add((Get-Content -LiteralPath $file.FullName -Raw -ErrorAction Stop))
                } else {
                    $chunks.Add(((Get-Content -LiteralPath $file.FullName -TotalCount 220 -ErrorAction Stop) -join "`n"))
                }
            } catch {
                $chunks.Add("READ_ERROR: $($_.Exception.Message)")
            }
        }
    }
    return ($chunks -join "`n")
}

function Add-Tag {
    param(
        [System.Collections.Generic.List[string]]$Tags,
        [string]$Tag,
        [bool]$Condition
    )
    if ($Condition -and -not $Tags.Contains($Tag)) { $Tags.Add($Tag) }
}

function Get-TopFolderPriority {
    param([string]$TopFolder)
    switch -Regex ($TopFolder) {
        '^AI_REPLAY_VAULT' { return 10 }
        '^Hermes_Skills$' { return 15 }
        '^Codex技能包$' { return 20 }
        '^Hermes_CleanBaseline' { return 30 }
        '^Codex_Skill_Backups$' { return 40 }
        '^Qwen36_27B_Skill_Backups$' { return 45 }
        '^OpenClaw_Skill_Backups$' { return 50 }
        '^OpenClaw_Full_Backups$' { return 60 }
        '^OpenClaw_Dynamic_Reset_Backups$' { return 70 }
        '^Hermes_Backup$' { return 80 }
        default { return 99 }
    }
}

function Resolve-EquivalentActive {
    param(
        [string]$SkillName,
        [string]$FrontmatterName,
        [hashtable]$ActiveByKey
    )
    $keys = New-Object System.Collections.Generic.List[string]
    foreach ($name in @($SkillName, $FrontmatterName)) {
        $key = Normalize-Key $name
        if ($key) { $keys.Add($key) }
    }

    $completeBodyCn = -join ([char[]](0x5B8C,0x6574,0x4F53,0x5EFA,0x8BBE,0x89C4,0x8303))
    $modelRoutingCn = -join ([char[]](0x7231,0x9A6C,0x4ED5,0x5927,0x6A21,0x578B,0x63A5,0x5165,0x8C03,0x8BD5,0x6628,0x65E5,0x91CD,0x73B0,0x6280,0x80FD,0x5305))
    $aliasMap = @{}
    $aliasMap['gpt-plus-superbrain-v0.1'] = 'gpt-plus-superbrain'
    $aliasMap['gpt-plus-superbrain-v0.2'] = 'gpt-plus-superbrain'
    $aliasMap[(Normalize-Key $completeBodyCn)] = 'complete-body-building-rules'
    $aliasMap[(Normalize-Key $modelRoutingCn)] = 'hermes-model-routing-windows-014'
    $aliasMap['qwen36-27b-connector-v0.2-20260430'] = 'qwen36-27b-local-connector'
    $aliasMap['qwen36-27b-connector-v0.3-20260430'] = 'qwen36-27b-local-connector'
    $aliasMap['openclaw-recovery-20260427'] = 'openclaw-recovery'
    foreach ($key in @($keys)) {
        if ($aliasMap.ContainsKey($key)) { $keys.Add($aliasMap[$key]) }
    }

    $matches = New-Object System.Collections.Generic.List[object]
    foreach ($key in $keys) {
        if ($ActiveByKey.ContainsKey($key)) {
            foreach ($item in $ActiveByKey[$key]) { $matches.Add($item) }
        }
    }
    return @($matches | Sort-Object Path -Unique)
}

$activeSkillFiles = Get-ChildItem -LiteralPath $ActiveRoot -Recurse -Filter 'SKILL.md' -File -ErrorAction SilentlyContinue
$activeItems = foreach ($file in $activeSkillFiles) {
    $dir = Split-Path -Parent $file.FullName
    $frontmatterName = Get-FrontmatterName -SkillMdPath $file.FullName
    [pscustomobject]@{
        DirName = Split-Path -Leaf $dir
        FrontmatterName = $frontmatterName
        Path = $file.FullName
        Scope = if ($file.FullName -match '\\\.archive\\') { 'archive' } else { 'active' }
    }
}

$activeByKey = @{}
foreach ($item in $activeItems) {
    foreach ($name in @($item.DirName, $item.FrontmatterName)) {
        $key = Normalize-Key $name
        if (-not $key) { continue }
        if (-not $activeByKey.ContainsKey($key)) {
            $activeByKey[$key] = New-Object System.Collections.Generic.List[object]
        }
        $activeByKey[$key].Add($item)
    }
}

$rows = Import-Csv -LiteralPath $InputCsv | Where-Object { $_.Category -eq 'C_NEEDS_REDESIGN_OR_ARCHIVE' }
if (@($rows).Count -ne 111) {
    throw "Expected 111 C_NEEDS_REDESIGN_OR_ARCHIVE rows, found $(@($rows).Count)."
}

$preserveToSource = @{}
if (Test-Path -LiteralPath $DestManifestCsv) {
    foreach ($item in (Import-Csv -LiteralPath $DestManifestCsv)) {
        if (-not [string]::IsNullOrWhiteSpace($item.PreservePath)) {
            $preserveToSource[$item.PreservePath] = $item
        }
    }
}

$annotated = foreach ($row in $rows) {
    $groupKey = Normalize-Key $(if (-not [string]::IsNullOrWhiteSpace($row.FrontmatterName)) { $row.FrontmatterName } else { $row.SkillName })
    [pscustomobject]@{
        Row = $row
        GroupKey = $groupKey
        TopPriority = Get-TopFolderPriority -TopFolder $row.TopFolder
    }
}

$canonicalByGroup = @{}
foreach ($group in ($annotated | Group-Object GroupKey)) {
    $winner = $group.Group | Sort-Object TopPriority, @{Expression = { [double]$_.Row.SizeMB }; Descending = $true }, @{Expression = { $_.Row.PreservePath }} | Select-Object -First 1
    $canonicalByGroup[$group.Name] = $winner.Row.PreservePath
}

$results = foreach ($entry in $annotated) {
    $row = $entry.Row
    $sourcePath = ''
    if ($row.PSObject.Properties.Name -contains 'SourcePath') { $sourcePath = [string]$row.SourcePath }
    if ([string]::IsNullOrWhiteSpace($sourcePath) -and $preserveToSource.ContainsKey($row.PreservePath)) {
        $sourcePath = [string]$preserveToSource[$row.PreservePath].SourcePath
    }
    $text = Get-SkillTextSample -PreservePath $row.PreservePath -SkillPath $row.SkillPath
    $lower = $text.ToLowerInvariant()
    $nameBlob = "$($row.SkillName) $($row.FrontmatterName) $($row.Description) $($row.TopFolder)".ToLowerInvariant()
    $allBlob = "$nameBlob`n$lower"

    $tags = New-Object System.Collections.Generic.List[string]
    Add-Tag $tags 'OpenClaw' ($allBlob -match 'openclaw|\.openclaw')
    Add-Tag $tags 'WSL-UnixPath' ($allBlob -match '/mnt/|/home/|~/|wsl|ubuntu|bash|\.sh\b')
    Add-Tag $tags 'RecoveryBackupBaseline' ($allBlob -match 'recover|recovery|backup|baseline|snapshot|reset')
    Add-Tag $tags 'OldChromeProfile' ($allBlob -match 'hermes_cdp_chrome_profile')
    Add-Tag $tags 'QwenLocal' ($allBlob -match 'qwen36|qwen')
    Add-Tag $tags 'GPTCodexBridge' ($allBlob -match 'chatgpt|gpt|codex|bridge|clipboard|cdp')
    Add-Tag $tags 'BrowserDesktopAutomation' ($allBlob -match 'browser|chrome|playwright|desktop-computer|device-automation|android|ios|harmonyos')
    Add-Tag $tags 'ModelOrGPUWorkflow' ($allBlob -match 'model|llm|stable-diffusion|whisper|lambda|modal|gpu|inference|bioinformatics')
    Add-Tag $tags 'ExternalService' ($allBlob -match 'tavily|qqbot|telegram|api key|token')

    $activeMatches = Resolve-EquivalentActive -SkillName $row.SkillName -FrontmatterName $row.FrontmatterName -ActiveByKey $activeByKey
    $activeExists = @($activeMatches | Where-Object { $_.Scope -eq 'active' }).Count -gt 0
    $archiveExists = @($activeMatches | Where-Object { $_.Scope -eq 'archive' }).Count -gt 0
    $activePaths = ($activeMatches | Select-Object -ExpandProperty Path -Unique) -join '; '
    $activeScopes = ($activeMatches | Select-Object -ExpandProperty Scope -Unique) -join ';'

    $groupCount = @($annotated | Where-Object { $_.GroupKey -eq $entry.GroupKey }).Count
    $isCanonical = ($canonicalByGroup[$entry.GroupKey] -eq $row.PreservePath)
    $sourceExists = if ([string]::IsNullOrWhiteSpace($sourcePath)) { $false } else { Test-Path -LiteralPath $sourcePath }
    $preserveExists = Test-Path -LiteralPath $row.PreservePath

    $windowsValue = 0
    if ($tags.Contains('GPTCodexBridge')) { $windowsValue += 4 }
    if ($tags.Contains('BrowserDesktopAutomation')) { $windowsValue += 3 }
    if ($tags.Contains('ModelOrGPUWorkflow')) { $windowsValue += 2 }
    if ($tags.Contains('ExternalService')) { $windowsValue += 1 }
    if ($tags.Contains('OpenClaw')) { $windowsValue -= 1 }
    if ($tags.Contains('RecoveryBackupBaseline')) { $windowsValue -= 1 }
    if ($windowsValue -lt 0) { $windowsValue = 0 }
    if ($windowsValue -gt 5) { $windowsValue = 5 }

    $legacyValue = 0
    if ($tags.Contains('OpenClaw')) { $legacyValue += 3 }
    if ($tags.Contains('RecoveryBackupBaseline')) { $legacyValue += 3 }
    if ($tags.Contains('QwenLocal')) { $legacyValue += 2 }
    if ($tags.Contains('GPTCodexBridge')) { $legacyValue += 2 }
    if ($tags.Contains('BrowserDesktopAutomation')) { $legacyValue += 1 }
    if ($legacyValue -gt 5) { $legacyValue = 5 }

    $rewriteCost = 1
    if ($tags.Contains('WSL-UnixPath')) { $rewriteCost += 1 }
    if ($tags.Contains('OpenClaw')) { $rewriteCost += 1 }
    if ($tags.Contains('OldChromeProfile')) { $rewriteCost += 1 }
    if ($tags.Contains('BrowserDesktopAutomation')) { $rewriteCost += 1 }
    if ($tags.Contains('QwenLocal')) { $rewriteCost += 1 }
    if ($rewriteCost -gt 5) { $rewriteCost = 5 }

    $roiClass = ''
    $recommendedAction = ''
    $reason = ''
    $priority = 'P3'

    if ($activeExists) {
        $roiClass = 'A_ALREADY_ACTIVE'
        $recommendedAction = 'No migration. Active Windows Hermes equivalent exists; keep only if a reference copy is desired.'
${REDACTED_SECRET}
        $priority = 'P4'
    } elseif ($archiveExists) {
        $roiClass = 'B_ALREADY_ARCHIVED'
        $recommendedAction = 'No daily migration. Keep as archive unless the user explicitly reopens this old route.'
        $reason = 'Equivalent skill already exists under active .archive.'
        $priority = 'P4'
    } elseif ($groupCount -gt 1 -and -not $isCanonical) {
        $roiClass = 'E_DELETE_CANDIDATE_DUPLICATE'
        $recommendedAction = 'Delete only after explicit approval; canonical preserved copy remains available.'
        $reason = "Duplicate preserved copy. Canonical preserve path: $($canonicalByGroup[$entry.GroupKey])"
        $priority = 'P5'
    } elseif ($windowsValue -ge 4 -and $rewriteCost -le 4) {
        $roiClass = 'C_REWRITE_SHORTLIST'
        $recommendedAction = 'Review and Windowsize in a later focused batch if this workflow is still needed.'
        $reason = 'High Windows workflow value and not already active.'
        $priority = 'P1'
    } elseif ($windowsValue -ge 2 -and $rewriteCost -le 3 -and -not $tags.Contains('OpenClaw')) {
        $roiClass = 'C_REWRITE_SHORTLIST'
        $recommendedAction = 'Review and Windowsize only if this domain is still used on the Windows Hermes system.'
        $reason = 'Moderate Windows value with manageable rewrite cost.'
        $priority = 'P2'
    } elseif ($legacyValue -ge 3 -or $isCanonical) {
        $roiClass = 'D_ARCHIVE_REFERENCE'
        $recommendedAction = 'Keep in H-drive archive/reference package; do not import into daily Windows Hermes.'
        $reason = 'Useful mainly as legacy evidence, recovery notes, or one canonical old-system reference.'
        $priority = 'P3'
    } else {
        $roiClass = 'E_DELETE_CANDIDATE_LOW_VALUE'
        $recommendedAction = 'Delete only after explicit approval; low Windows value and no unique legacy reason found.'
        $reason = 'Low current value and not selected as a canonical reference.'
        $priority = 'P5'
    }

    [pscustomobject]@{
        SkillName = $row.SkillName
        FrontmatterName = $row.FrontmatterName
        TopFolder = $row.TopFolder
        Category = $row.Category
        RiskHits = $row.RiskHits
        EvidenceTags = ($tags -join ';')
        FileCount = $row.FileCount
        SizeMB = $row.SizeMB
        SourceExists = $sourceExists
        PreserveExists = $preserveExists
        GroupKey = $entry.GroupKey
        GroupCount = $groupCount
        IsCanonicalPreservedCopy = $isCanonical
        ActiveEquivalentExists = $activeExists
        ArchiveEquivalentExists = $archiveExists
        ActiveEquivalentScope = $activeScopes
        ActiveEquivalentPath = $activePaths
        WindowsValueScore = $windowsValue
        LegacyValueScore = $legacyValue
        RewriteCostScore = $rewriteCost
        Priority = $priority
        ROIClass = $roiClass
        RecommendedAction = $recommendedAction
        Reason = $reason
        SourcePath = $sourcePath
        PreservePath = $row.PreservePath
        SkillPath = $row.SkillPath
    }
}

$classificationPath = Join-Path $OutDir 'roi-111-classification.csv'
$results | Sort-Object ROIClass, Priority, GroupKey, TopFolder, PreservePath | Export-Csv -LiteralPath $classificationPath -NoTypeInformation -Encoding UTF8

$splitMap = @{
    'already-active.csv' = { param($r) $r.ROIClass -eq 'A_ALREADY_ACTIVE' }
    'already-archived.csv' = { param($r) $r.ROIClass -eq 'B_ALREADY_ARCHIVED' }
    'rewrite-shortlist.csv' = { param($r) $r.ROIClass -eq 'C_REWRITE_SHORTLIST' }
    'archive-reference.csv' = { param($r) $r.ROIClass -eq 'D_ARCHIVE_REFERENCE' }
    'delete-candidates-review-first.csv' = { param($r) $r.ROIClass -like 'E_DELETE_CANDIDATE*' }
}
foreach ($fileName in $splitMap.Keys) {
    $predicate = $splitMap[$fileName]
    $results | Where-Object { & $predicate $_ } | Sort-Object Priority, GroupKey, TopFolder, PreservePath |
        Export-Csv -LiteralPath (Join-Path $OutDir $fileName) -NoTypeInformation -Encoding UTF8
}

$summary = New-Object System.Collections.Generic.List[string]
$summary.Add('# Hermes WSL/OpenClaw Skill ROI Summary')
$summary.Add('')
$summary.Add('Date: 2026-05-19')
$summary.Add('')
$summary.Add('Scope: 111 preserved skills previously classified as C_NEEDS_REDESIGN_OR_ARCHIVE from the H-drive unmatched skill package.')
$summary.Add('')
$summary.Add('No source or preserved skill was deleted by this run. Delete candidates require explicit user approval.')
$summary.Add('')
$summary.Add('## Counts by ROI class')
$summary.Add('')
$summary.Add('| ROI class | Count | Meaning |')
$summary.Add('|---|---:|---|')
foreach ($g in ($results | Group-Object ROIClass | Sort-Object Name)) {
    $meaning = switch ($g.Name) {
        'A_ALREADY_ACTIVE' { 'Equivalent Windows Hermes skill is already active.' }
        'B_ALREADY_ARCHIVED' { 'Equivalent legacy route already exists under .archive.' }
        'C_REWRITE_SHORTLIST' { 'Worth later Windows rewrite if the workflow is still needed.' }
        'D_ARCHIVE_REFERENCE' { 'Keep as reference; do not import into daily Windows Hermes.' }
        default { 'Delete only after approval; duplicate or low current value.' }
    }
    $summary.Add("| $($g.Name) | $($g.Count) | $meaning |")
}
$summary.Add('')
$summary.Add('## Counts by top folder')
$summary.Add('')
$summary.Add('| Top folder | Count |')
$summary.Add('|---|---:|')
foreach ($g in ($results | Group-Object TopFolder | Sort-Object @{Expression = 'Count'; Descending = $true }, @{Expression = 'Name'; Descending = $false })) {
    $summary.Add("| $($g.Name) | $($g.Count) |")
}
$summary.Add('')
$summary.Add('## Rewrite shortlist')
$summary.Add('')
$rewrite = @($results | Where-Object { $_.ROIClass -eq 'C_REWRITE_SHORTLIST' } | Sort-Object Priority, @{Expression = 'WindowsValueScore'; Descending = $true }, RewriteCostScore, SkillName)
if ($rewrite.Count -eq 0) {
    $summary.Add('No rewrite shortlist items were selected by the current rules.')
} else {
    $summary.Add('| Priority | Skill | Frontmatter | Windows value | Rewrite cost | Reason |')
    $summary.Add('|---|---|---|---:|---:|---|')
    foreach ($r in $rewrite) {
        $summary.Add("| $($r.Priority) | $($r.SkillName) | $($r.FrontmatterName) | $($r.WindowsValueScore) | $($r.RewriteCostScore) | $($r.Reason) |")
    }
}
$summary.Add('')
$summary.Add('## Practical decision')
$summary.Add('')
$summary.Add('- Do not hard-migrate all 111. Most are old WSL/OpenClaw/recovery evidence or repeated backup copies.')
$summary.Add('- Keep canonical archive references for old-system recovery logic and historical bridge/device automation patterns.')
$summary.Add('- Migrate only the rewrite shortlist, one small batch at a time, after confirming current Windows Hermes demand.')
$summary.Add('- Treat delete candidates as review-first. The safe deletion target is the preserved duplicate copy, not the active Windows Hermes skill.')
$summary.Add('')
$summary.Add('## Output files')
$summary.Add('')
$summary.Add("- Full classification: $classificationPath")
$summary.Add("- Rewrite shortlist: $(Join-Path $OutDir 'rewrite-shortlist.csv')")
$summary.Add("- Archive references: $(Join-Path $OutDir 'archive-reference.csv')")
$summary.Add("- Delete candidates: $(Join-Path $OutDir 'delete-candidates-review-first.csv')")

$summaryPath = Join-Path $OutDir 'roi-summary.md'
$summary | Set-Content -LiteralPath $summaryPath -Encoding UTF8

[pscustomobject]@{
    Classification = $classificationPath
    Summary = $summaryPath
    Total = @($results).Count
    RewriteShortlist = @($rewrite).Count
    DeleteCandidates = @($results | Where-Object { $_.ROIClass -like 'E_DELETE_CANDIDATE*' }).Count
} | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $OutDir 'roi-run-result.json') -Encoding UTF8

Write-Host "ROI_CLASSIFICATION_PASS"
Write-Host "Classification=$classificationPath"
Write-Host "Summary=$summaryPath"
Write-Host "Total=$(@($results).Count)"
