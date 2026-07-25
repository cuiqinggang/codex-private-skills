[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$VmName,
    [Parameter(Mandatory)]
    [string]$ScenarioName,
    [Parameter(Mandatory)]
    [ValidateSet('None','Private')]
    [string]$NetworkMode,
    [string]$PrivateSwitchName,
    [Parameter(Mandatory)]
    [string]$GuestPayloadPath,
    [Parameter(Mandatory)]
    [string]$EvidenceRoot,
    [Parameter(Mandatory)]
    [string]$OutputPath,
    [Parameter(Mandatory)]
    [switch]$ConfirmDisposable,
    [ValidateRange(1, 10)]
    [int]$MaxGuestReboots = 2,
    [ValidateRange(1, 72)]
    [int]$ValidHours = 24
)

$ErrorActionPreference = 'Stop'
if ($env:OS -ne 'Windows_NT') { throw 'Planning requires native Windows with Hyper-V.' }
if (-not $ConfirmDisposable) { throw 'Explicit disposable-VM confirmation is required.' }
if (-not (Test-Path -LiteralPath $GuestPayloadPath -PathType Leaf)) { throw 'Guest payload must be one existing file.' }
if ($NetworkMode -eq 'Private') {
    if ([string]::IsNullOrWhiteSpace($PrivateSwitchName)) { throw 'PrivateSwitchName is required.' }
    $switch = Get-VMSwitch -Name $PrivateSwitchName -ErrorAction Stop
    if ([string]$switch.SwitchType -ne 'Private') { throw 'Only a Private switch is allowed.' }
}
$vm = Get-VM -Name $VmName -ErrorAction Stop
$adapters = @(Get-VMNetworkAdapter -VMName $VmName -ErrorAction Stop)
$privateSwitchId = $(if ($NetworkMode -eq 'Private') {[string]$switch.Id} else {$null})
$runId = [guid]::NewGuid().ToString('N')
$guestRunRoot = "C:\ProgramData\WindowsSoftwareTestLab\$runId"
$plan = [ordered]@{
    schemaVersion=1;kind='windows-software-test-plan';runId=$runId;host=$env:COMPUTERNAME
    vmName=$vm.Name;vmId=[string]$vm.Id;disposableConfirmed=$true;scenarioName=$ScenarioName;networkMode=$NetworkMode
    privateSwitchName=$PrivateSwitchName;privateSwitchId=$privateSwitchId
    initialAdapterIds=@($adapters | ForEach-Object {[string]$_.Id} | Sort-Object)
    guestPayloadPath=[IO.Path]::GetFullPath($GuestPayloadPath)
    guestPayloadSha256=(Get-FileHash -LiteralPath $GuestPayloadPath -Algorithm SHA256).Hash.ToLowerInvariant()
    guestPayloadDestination="$guestRunRoot\payload.ps1";testMarkerPath="$guestRunRoot\executed.marker"
    evidenceRoot=[IO.Path]::GetFullPath($EvidenceRoot);baselineCheckpointName="baseline-$runId"
    maxGuestReboots=$MaxGuestReboots;createdAt=[DateTime]::UtcNow.ToString('o')
    expiresAt=[DateTime]::UtcNow.AddHours($ValidHours).ToString('o')
}
$canonical = $plan | ConvertTo-Json -Depth 6 -Compress
$sha = [Security.Cryptography.SHA256]::Create()
try { $hash = ([BitConverter]::ToString($sha.ComputeHash([Text.UTF8Encoding]::new($false).GetBytes($canonical)))).Replace('-','').ToLowerInvariant() }
finally { $sha.Dispose() }
$plan['planHash'] = $hash
$parent = Split-Path -Parent $OutputPath
if ($parent) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
$plan | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $OutputPath -Encoding UTF8
$hash
