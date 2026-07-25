[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [Parameter(Mandatory)]
    [string]$PlanPath,
    [Parameter(Mandatory)]
    [ValidatePattern('^[a-fA-F0-9]{64}$')]
    [string]$ApprovePlanHash,
    [switch]$Execute,
    [string]$ResultPath
)

$ErrorActionPreference = 'Stop'
if ($env:OS -ne 'Windows_NT') { throw 'Removal requires native Windows.' }
$plan = Get-Content -LiteralPath $PlanPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ([int]$plan.schemaVersion -ne 1 -or [string]$plan.kind -ne 'stubborn-software-removal-plan') { throw 'Unsupported plan.' }
if ([string]$plan.computer -ne $env:COMPUTERNAME) { throw 'Plan belongs to another computer.' }
$sid = [Security.Principal.WindowsIdentity]::GetCurrent().User.Value
if ([string]$plan.userSid -ne $sid) { throw 'Plan belongs to another user.' }
if ([DateTime]::Parse([string]$plan.expiresAt).ToUniversalTime() -lt [DateTime]::UtcNow) { throw 'Plan expired.' }

$copy = [ordered]@{}
foreach ($property in $plan.PSObject.Properties) {
    if ($property.Name -ne 'planHash') { $copy[$property.Name] = $property.Value }
}
$canonical = $copy | ConvertTo-Json -Depth 8 -Compress
$bytes = [Text.UTF8Encoding]::new($false).GetBytes($canonical)
$sha = [Security.Cryptography.SHA256]::Create()
try { $actualPlanHash = ([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-','').ToLowerInvariant() }
finally { $sha.Dispose() }
if ($actualPlanHash -ne ([string]$plan.planHash).ToLowerInvariant() -or $actualPlanHash -ne $ApprovePlanHash.ToLowerInvariant()) {
    throw 'Plan hash mismatch.'
}

$results = @()
foreach ($action in @($plan.actions)) {
    if ([string]$action.type -eq 'MSI') {
        if ([string]$action.productCode -notmatch '^\{[0-9A-Fa-f-]{36}\}$') { throw 'Invalid MSI ProductCode.' }
        $preview = "msiexec.exe /x $($action.productCode)"
        if ($Execute -and $PSCmdlet.ShouldProcess([string]$action.displayName, 'Run exact MSI uninstaller')) {
            $process = Start-Process -FilePath "$env:SystemRoot\System32\msiexec.exe" -ArgumentList @('/x',[string]$action.productCode) -Wait -PassThru
            $results += [ordered]@{displayName=[string]$action.displayName;mode='Execute';exitCode=$process.ExitCode;entry=$preview}
        } else { $results += [ordered]@{displayName=[string]$action.displayName;mode='Preview';entry=$preview} }
    } elseif ([string]$action.type -eq 'VendorUninstaller') {
        $lolBins = @('powershell.exe','pwsh.exe','cmd.exe','wscript.exe','cscript.exe','mshta.exe','rundll32.exe','regsvr32.exe')
        if ($lolBins -contains [IO.Path]::GetFileName(([string]$action.executablePath)).ToLowerInvariant()) { throw 'LOLBin cannot be a vendor uninstaller.' }
        if (-not (Test-Path -LiteralPath ([string]$action.executablePath) -PathType Leaf)) { throw 'Vendor uninstaller is missing.' }
        $hash = (Get-FileHash -LiteralPath ([string]$action.executablePath) -Algorithm SHA256).Hash.ToLowerInvariant()
        $signature = Get-AuthenticodeSignature -LiteralPath ([string]$action.executablePath)
        $thumbprint = ([string]$signature.SignerCertificate.Thumbprint).Replace(' ','').ToUpperInvariant()
        if ($hash -ne ([string]$action.sha256).ToLowerInvariant() -or [string]$signature.Status -ne 'Valid' -or
            $thumbprint -ne ([string]$action.signerThumbprint).Replace(' ','').ToUpperInvariant()) {
            throw 'Vendor uninstaller identity changed.'
        }
        if ($Execute -and $PSCmdlet.ShouldProcess([string]$action.displayName, 'Run verified vendor uninstaller')) {
            $process = Start-Process -FilePath ([string]$action.executablePath) -ArgumentList ([string]$action.arguments) -Wait -PassThru
            $results += [ordered]@{displayName=[string]$action.displayName;mode='Execute';exitCode=$process.ExitCode;entry=[string]$action.executablePath}
        } else { $results += [ordered]@{displayName=[string]$action.displayName;mode='Preview';entry=[string]$action.executablePath} }
    } else { throw "Unsupported action type: $($action.type)" }
}

$output = [ordered]@{
    schemaVersion=1;kind='stubborn-software-removal-result'
    mode=$(if ($Execute) {'Execute'} else {'Preview'});planHash=$actualPlanHash;actions=$results
    humanGates=@($plan.humanGates)
    rebootRequest=$(if ($Execute -and [bool]$plan.requiresReboot) {
        [ordered]@{type='rebootRequest';reason='vendor-uninstaller-requested';resumeStep=[string]$plan.nextStep;evidencePath=$ResultPath}
    } else {$null})
    completion='NOT_VERIFIED_REINVENTORY_REQUIRED'
}
if ($ResultPath) {
    $parent = Split-Path -Parent $ResultPath
    if ($parent) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
    $output | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $ResultPath -Encoding UTF8
}
[pscustomobject]$output
