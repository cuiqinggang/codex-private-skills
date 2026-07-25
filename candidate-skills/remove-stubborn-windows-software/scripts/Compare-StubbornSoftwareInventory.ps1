[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$BaselineInventoryPath,
    [Parameter(Mandatory)]
    [string]$CurrentInventoryPath,
    [string]$KnownResidueManifestPath,
    [string]$OutputPath
)

$ErrorActionPreference = 'Stop'
function Is-Exact([string]$Value, [string[]]$Allowed) {
    foreach ($candidate in $Allowed) {
        if ([string]::Equals($Value, $candidate, [StringComparison]::OrdinalIgnoreCase)) { return $true }
    }
    return $false
}

$baseline = Get-Content -LiteralPath $BaselineInventoryPath -Raw -Encoding UTF8 | ConvertFrom-Json
$current = Get-Content -LiteralPath $CurrentInventoryPath -Raw -Encoding UTF8 | ConvertFrom-Json
foreach ($inventory in @($baseline,$current)) {
    if ([int]$inventory.schemaVersion -ne 1 -or [string]$inventory.kind -ne 'stubborn-software-inventory') { throw 'Unsupported inventory.' }
}
if ([string]$baseline.computer -ne [string]$current.computer) { throw 'Inventories belong to different computers.' }
$baselineHash = (Get-FileHash -LiteralPath $BaselineInventoryPath -Algorithm SHA256).Hash.ToLowerInvariant()
if ([string]$current.baselineInventorySha256 -ne $baselineHash) { throw 'Current inventory was not captured from this exact baseline.' }

$knownIds = @()
if ($KnownResidueManifestPath) {
    $known = Get-Content -LiteralPath $KnownResidueManifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
    if ([int]$known.schemaVersion -ne 1) { throw 'Unsupported known-residue manifest.' }
    $knownIds = @($known.evidenceIds | ForEach-Object { [string]$_ })
}

$active = @()
$residual = @()
foreach ($product in @($current.products)) { $active += "product:$($product.displayName)" }
foreach ($process in @($current.processes)) { $active += [string]$process.evidenceId }
foreach ($component in @($current.servicesAndDrivers)) {
    if ([string]$component.state -match '^(Running|Start Pending|Continue Pending)$') { $active += [string]$component.evidenceId }
    else { $residual += [string]$component.evidenceId }
}
foreach ($task in @($current.scheduledTasks)) {
    if ([string]$task.state -eq 'Running') { $active += [string]$task.evidenceId } else { $residual += [string]$task.evidenceId }
}
foreach ($startup in @($current.startupEntries)) { $residual += [string]$startup.evidenceId }
foreach ($root in @($current.installRoots | Where-Object { [bool]$_.exists })) { $residual += [string]$root.evidenceId }
$active = @($active | Sort-Object -Unique)
$residual = @($residual | Sort-Object -Unique)
$unknown = @($residual | Where-Object { -not (Is-Exact $_ $knownIds) })

$classification = if ($active.Count) {
    'ACTIVE_PRODUCT'
} elseif ($unknown.Count) {
    'UNKNOWN_BLOCKER'
} elseif ($residual.Count) {
    'KNOWN_VENDOR_RESIDUE'
} else {
    'ABSENT'
}
$result = [ordered]@{
    schemaVersion=1;kind='stubborn-software-comparison';computer=[string]$current.computer
    baselineCapturedAt=[string]$baseline.capturedAt;currentCapturedAt=[string]$current.capturedAt
    classification=$classification;activeEvidence=$active;knownResidualEvidence=@($residual | Where-Object { Is-Exact $_ $knownIds })
    unknownEvidence=$unknown
}
if ($OutputPath) {
    $parent = Split-Path -Parent $OutputPath
    if ($parent) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
    $result | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $OutputPath -Encoding UTF8
}
[pscustomobject]$result
