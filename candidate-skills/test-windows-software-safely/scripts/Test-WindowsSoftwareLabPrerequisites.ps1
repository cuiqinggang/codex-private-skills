[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$VmName,
    [ValidateRange(2, 100)]
    [int]$MinimumFreeGB = 20
)

$ErrorActionPreference = 'Stop'
if ($env:OS -ne 'Windows_NT') {
    [pscustomobject]@{status='UNSUPPORTED';reason='Native Windows with Hyper-V is required.'}
    exit 2
}
if (-not (Get-Module -ListAvailable -Name Hyper-V)) { throw 'Hyper-V PowerShell module is unavailable.' }
$identity = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = [Security.Principal.WindowsPrincipal]::new($identity)
if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) { throw 'Administrator is required.' }

$vm = Get-VM -Name $VmName -ErrorAction Stop
$external = @()
foreach ($adapter in @(Get-VMNetworkAdapter -VMName $VmName -ErrorAction SilentlyContinue)) {
    if ($adapter.SwitchName) {
        $switch = Get-VMSwitch -Name $adapter.SwitchName -ErrorAction Stop
        if ([string]$switch.SwitchType -eq 'External') { $external += $switch.Name }
    }
}
$drive = Get-PSDrive -Name ([IO.Path]::GetPathRoot((Get-VMHardDiskDrive -VMName $VmName | Select-Object -First 1).Path).TrimEnd(':\'))
$freeGB = [math]::Round($drive.Free / (1024 * 1024 * 1024), 2)
[pscustomobject]@{
    status=$(if ($external.Count -or $freeGB -lt $MinimumFreeGB) {'BLOCKED'} else {'PASS'})
    vmName=$vm.Name;vmId=[string]$vm.Id;vmState=[string]$vm.State;externalSwitches=$external
    freeGB=$freeGB;minimumFreeGB=$MinimumFreeGB;powerShellDirect='VERIFY_WITH_GUEST_CREDENTIAL_AT_RUNTIME'
}
