[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
if ($env:OS -ne 'Windows_NT') { throw 'Run the integration test in a disposable Windows VM.' }

$marker = Join-Path $env:ProgramData 'RebootResumeAdapterFixture'
New-Item -ItemType Directory -Path $marker -Force | Out-Null
$state = Join-Path $marker 'fixture-state.json'

if (-not (Test-Path -LiteralPath $state)) {
    [ordered]@{phase=0;firstBoot=$null;secondBoot=$null} | ConvertTo-Json | Set-Content -LiteralPath $state -Encoding UTF8
}

$fixture = Get-Content -LiteralPath $state -Raw -Encoding UTF8 | ConvertFrom-Json
$boot = (Get-CimInstance Win32_OperatingSystem).LastBootUpTime.ToUniversalTime().ToString('o')
switch ([int]$fixture.phase) {
    0 {
        $fixture.phase=1; $fixture.firstBoot=$boot
        $fixture | ConvertTo-Json | Set-Content -LiteralPath $state -Encoding UTF8
        Write-Output 'FIXTURE_ARMED_FOR_REBOOT_1'
    }
    1 {
        if ($fixture.firstBoot -eq $boot) { throw 'First guest reboot was not observed.' }
        $fixture.phase=2; $fixture.secondBoot=$boot
        $fixture | ConvertTo-Json | Set-Content -LiteralPath $state -Encoding UTF8
        Write-Output 'FIXTURE_ARMED_FOR_REBOOT_2'
    }
    2 {
        if ($fixture.secondBoot -eq $boot) { throw 'Second guest reboot was not observed.' }
        $fixture.phase=3
        $fixture | ConvertTo-Json | Set-Content -LiteralPath $state -Encoding UTF8
        Write-Output 'REBOOT_RESUME_VM_INTEGRATION_PASS'
    }
    default { Write-Output 'REBOOT_RESUME_VM_INTEGRATION_ALREADY_PASS' }
}

# This fixture never reboots the host or guest. The VM controller must reboot between phases.
