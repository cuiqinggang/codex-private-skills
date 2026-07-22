$ErrorActionPreference = "Stop"

$task = "FIX_Codex_LongText_Attachment"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$codexHome = Join-Path $env:USERPROFILE ".codex"
$backupRoot = Join-Path $codexHome "patches\backups\$timestamp"
$reportRoot = Join-Path $codexHome "patches\reports"
$fallbackRoot = Join-Path $codexHome "manual-paste-attachments"
$reportPath = Join-Path $reportRoot "$task-$timestamp.json"
$notes = New-Object System.Collections.Generic.List[string]

New-Item -ItemType Directory -Force -Path $backupRoot, $reportRoot, $fallbackRoot | Out-Null

$candidatePaths = @(
    (Join-Path $env:LOCALAPPDATA "Programs\Codex\resources\app.asar"),
    (Join-Path $env:LOCALAPPDATA "Codex\resources\app.asar")
)

$storeCandidates = Get-ChildItem -LiteralPath "C:\Program Files\WindowsApps" -Directory -Filter "OpenAI.Codex_*" -ErrorAction SilentlyContinue |
    ForEach-Object { Join-Path $_.FullName "app\resources\app.asar" } |
    Where-Object { Test-Path -LiteralPath $_ }

$appxCandidates = @()
try {
    $appxCandidates = Get-AppxPackage -Name "OpenAI.Codex" -ErrorAction Stop |
        ForEach-Object { Join-Path $_.InstallLocation "app\resources\app.asar" } |
        Where-Object { Test-Path -LiteralPath $_ }
} catch {
    $notes.Add("Get-AppxPackage OpenAI.Codex failed: $($_.Exception.Message)")
}

$allCandidates = @($candidatePaths + $storeCandidates + $appxCandidates) | Select-Object -Unique
$existing = $allCandidates | Where-Object { Test-Path -LiteralPath $_ }

$selected = $null
$backupPath = $null
$status = "PATCH_FALLBACK"

foreach ($path in $existing) {
    if ($path -like "C:\Program Files\WindowsApps\*") {
        $notes.Add("Found Windows Store/MSIX app.asar: $path; skipped direct WindowsApps modification.")
        continue
    }

    try {
        $stream = [System.IO.File]::Open($path, [System.IO.FileMode]::Open, [System.IO.FileAccess]::ReadWrite, [System.IO.FileShare]::None)
        $stream.Close()
        $selected = $path
        break
    } catch {
        $notes.Add("Candidate app.asar is not writable: $path; $($_.Exception.Message)")
    }
}

if ($selected -ne $null) {
    $backupPath = Join-Path $backupRoot "app.asar.backup"
    Copy-Item -LiteralPath $selected -Destination $backupPath -Force

    $bytes = [System.IO.File]::ReadAllBytes($selected)
    $latin1 = [System.Text.Encoding]::GetEncoding("ISO-8859-1")
    $content = $latin1.GetString($bytes)
    $needle = "oo&&X.addPastedTextHandler(Qc)"
    $replacement = "!1&&X.addPastedTextHandler(Qc)"
    $matchCount = ([regex]::Matches($content, [regex]::Escape($needle))).Count

    if ($matchCount -eq 1) {
        $content = $content.Replace($needle, $replacement)
        [System.IO.File]::WriteAllBytes($selected, $latin1.GetBytes($content))
        $status = "PATCH_APPLIED"
        $notes.Add("Unique target snippet found and replaced.")
    } elseif ($matchCount -eq 0) {
        $status = "PATCH_FALLBACK"
        $notes.Add("Target snippet not found: $needle; app.asar was not modified.")
    } else {
        $status = "PATCH_FALLBACK"
        $notes.Add("Target snippet matched $matchCount times; unsafe to patch, app.asar was not modified.")
    }
} else {
    $notes.Add("No safely writable non-WindowsApps app.asar found; enabled clipboard-to-txt fallback.")
}

$fallbackScript = Join-Path $fallbackRoot "clipboard-to-txt.ps1"

$report = [pscustomobject]@{
    task = $task
    status = $status
    timestamp = $timestamp
    asar_path = $selected
    existing_asar_paths = @($existing)
    backup_path = $backupPath
    fallback_script = $fallbackScript
    fallback_directory = $fallbackRoot
    notes = @($notes)
    suggested_next_step = if ($status -eq "PATCH_APPLIED") {
        "Fully quit and restart Codex Desktop, then test long text paste."
    } else {
        "Copy long text, run install-auto-longtext-fileclip.ps1 -Start, then paste in Codex."
    }
}

$report | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $reportPath -Encoding UTF8
$report | ConvertTo-Json -Depth 6
