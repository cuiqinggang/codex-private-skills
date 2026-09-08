[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Symptom,
    [Parameter(Mandatory = $true)][string]$RootCause,
    [Parameter(Mandatory = $true)][string]$Fix,
    [Parameter(Mandatory = $true)][string]$Prevention,
    [Parameter(Mandatory = $true)][string]$Environment,
    [Parameter(Mandatory = $true)][string]$Evidence,
    [string]$IncidentId,
    [string]$CatalogPath = (Join-Path (Split-Path $PSScriptRoot -Parent) 'references\learned-errors.jsonl')
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

function Normalize-Text([string]$Value) {
    return (($Value.Trim().ToLowerInvariant()) -replace '\s+', ' ')
}

$fingerprintSource = '{0}|{1}|{2}' -f (Normalize-Text $Symptom), (Normalize-Text $RootCause), (Normalize-Text $Prevention)
$sha256 = [System.Security.Cryptography.SHA256]::Create()
try {
    $fingerprint = ([BitConverter]::ToString($sha256.ComputeHash([Text.Encoding]::UTF8.GetBytes($fingerprintSource)))).Replace('-', '').ToLowerInvariant()
}
finally {
    $sha256.Dispose()
}

$resolvedCatalog = [System.IO.Path]::GetFullPath($CatalogPath)
$matchingOccurrences = 0
if (Test-Path -LiteralPath $resolvedCatalog) {
    foreach ($line in [System.IO.File]::ReadAllLines($resolvedCatalog, [Text.Encoding]::UTF8)) {
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        $existing = $line | ConvertFrom-Json
        if ($existing.fingerprint -eq $fingerprint) {
            $matchingOccurrences++
        }
    }
}

if ($matchingOccurrences -gt 0) {
    $nextOccurrence = $matchingOccurrences + 1
    $repeatEntry = [ordered]@{
        schema_version = 1
        event = 'REPEATED_OCCURRENCE'
        recorded_utc = [DateTime]::UtcNow.ToString('o')
        fingerprint = $fingerprint
        incident_id = $IncidentId
        occurrence_count = $nextOccurrence
        promotion_required = ($nextOccurrence -ge 2)
    }
    $repeatLine = $repeatEntry | ConvertTo-Json -Compress
    [System.IO.File]::AppendAllText($resolvedCatalog, $repeatLine + [Environment]::NewLine, (New-Object Text.UTF8Encoding($false)))
    [pscustomobject]@{
        Status = if ($nextOccurrence -ge 2) { 'PROMOTION_REQUIRED' } else { 'DUPLICATE' }
        Fingerprint = $fingerprint
        OccurrenceCount = $nextOccurrence
        Catalog = $resolvedCatalog
    } | ConvertTo-Json -Compress
    return
}

$entry = [ordered]@{
    schema_version = 1
    event = 'LEARNED_ERROR'
    recorded_utc = [DateTime]::UtcNow.ToString('o')
    fingerprint = $fingerprint
    incident_id = $IncidentId
    symptom = $Symptom
    root_cause = $RootCause
    fix = $Fix
    prevention = $Prevention
    environment = $Environment
    evidence = $Evidence
    occurrence_count = 1
    promotion_required = $false
}

$directory = Split-Path $resolvedCatalog -Parent
if (-not (Test-Path -LiteralPath $directory)) {
    [void](New-Item -ItemType Directory -Path $directory)
}
$jsonLine = ($entry | ConvertTo-Json -Compress)
[System.IO.File]::AppendAllText($resolvedCatalog, $jsonLine + [Environment]::NewLine, (New-Object Text.UTF8Encoding($false)))
[pscustomobject]@{ Status = 'ADDED'; Fingerprint = $fingerprint; Catalog = $resolvedCatalog } |
    ConvertTo-Json -Compress
