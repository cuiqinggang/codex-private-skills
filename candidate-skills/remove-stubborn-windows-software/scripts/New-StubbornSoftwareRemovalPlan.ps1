[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$InventoryPath,
    [Parameter(Mandatory)]
    [string]$OutputPath,
    [Parameter(Mandatory)]
    [string]$ApprovedPublisherThumbprintsPath,
    [ValidateRange(1, 72)]
    [int]$ValidHours = 24
)

$ErrorActionPreference = 'Stop'
$inventory = Get-Content -LiteralPath $InventoryPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ([int]$inventory.schemaVersion -ne 1 -or [string]$inventory.kind -ne 'stubborn-software-inventory') {
    throw 'Unsupported inventory.'
}
$approval = Get-Content -LiteralPath $ApprovedPublisherThumbprintsPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ([int]$approval.schemaVersion -ne 1) { throw 'Unsupported publisher thumbprint approval map.' }
$lolBins = @('powershell.exe','pwsh.exe','cmd.exe','wscript.exe','cscript.exe','mshta.exe','rundll32.exe','regsvr32.exe')

$actions = @()
$humanGates = @()
foreach ($product in @($inventory.products)) {
    if ([bool]$product.windowsInstaller -and [string]$product.productCode -match '^\{[0-9A-Fa-f-]{36}\}$') {
        $actions += [ordered]@{
            type='MSI';displayName=[string]$product.displayName;productCode=[string]$product.productCode
        }
    } elseif ($product.uninstall -and [string]$product.signatureStatus -eq 'Valid' -and [string]$product.sha256 -match '^[a-f0-9]{64}$') {
        $leaf = [IO.Path]::GetFileName(([string]$product.uninstall.executable)).ToLowerInvariant()
        $publisherApproval = @($approval.publishers | Where-Object {
            [string]::Equals([string]$_.publisher,[string]$product.publisher,[StringComparison]::OrdinalIgnoreCase)
        })
        $thumbprintApproved = $publisherApproval.Count -eq 1 -and @($publisherApproval[0].thumbprints | Where-Object {
            [string]::Equals(([string]$_).Replace(' ',''),([string]$product.signerThumbprint).Replace(' ',''),[StringComparison]::OrdinalIgnoreCase)
        }).Count -eq 1
        if ($lolBins -contains $leaf) {
            $humanGates += [ordered]@{displayName=[string]$product.displayName;reason='LOLBin cannot be a vendor uninstaller.'}
            continue
        }
        if (-not $thumbprintApproved) {
            $humanGates += [ordered]@{displayName=[string]$product.displayName;reason='Publisher and signer thumbprint are not in the human-approved map.'}
            continue
        }
        $actions += [ordered]@{
            type='VendorUninstaller';displayName=[string]$product.displayName
            executablePath=[string]$product.uninstall.executable;arguments=[string]$product.uninstall.arguments
            sha256=[string]$product.sha256;publisher=[string]$product.publisher
            signer=[string]$product.signer;signerThumbprint=([string]$product.signerThumbprint).Replace(' ','').ToUpperInvariant()
        }
    } else {
        $humanGates += [ordered]@{
            displayName=[string]$product.displayName;reason='No verified MSI or validly signed vendor uninstaller.'
        }
    }
}

$planCore = [ordered]@{
    schemaVersion=1;kind='stubborn-software-removal-plan';computer=[string]$inventory.computer
    userSid=[string]$inventory.userSid;createdAt=[DateTime]::UtcNow.ToString('o')
    expiresAt=[DateTime]::UtcNow.AddHours($ValidHours).ToString('o')
    requestedDisplayNames=@($inventory.requestedDisplayNames);requestedPublishers=@($inventory.requestedPublishers)
    actions=$actions;humanGates=$humanGates;requiresReboot=($actions.Count -gt 0)
    nextStep='reinventory-and-verify'
    publisherThumbprintApprovalSha256=(Get-FileHash -LiteralPath $ApprovedPublisherThumbprintsPath -Algorithm SHA256).Hash.ToLowerInvariant()
}
$canonical = $planCore | ConvertTo-Json -Depth 8 -Compress
$bytes = [Text.UTF8Encoding]::new($false).GetBytes($canonical)
$sha = [Security.Cryptography.SHA256]::Create()
try { $planHash = ([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-','').ToLowerInvariant() }
finally { $sha.Dispose() }
$plan = $planCore
$plan['planHash'] = $planHash
$parent = Split-Path -Parent $OutputPath
if ($parent) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
$plan | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $OutputPath -Encoding UTF8
$planHash
