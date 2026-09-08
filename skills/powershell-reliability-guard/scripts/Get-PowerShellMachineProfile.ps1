[CmdletBinding()]
param()

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

$operatingSystem = Get-CimInstance -ClassName Win32_OperatingSystem
$analyzer = Get-Module -ListAvailable -Name PSScriptAnalyzer |
    Sort-Object Version -Descending |
    Select-Object -First 1
$pester = Get-Module -ListAvailable -Name Pester |
    Sort-Object Version -Descending |
    Select-Object -First 1

$profile = [ordered]@{
    captured_utc = [DateTime]::UtcNow.ToString('o')
    computer_name = $env:COMPUTERNAME
    os_caption = $operatingSystem.Caption
    os_version = $operatingSystem.Version
    os_build = $operatingSystem.BuildNumber
    powershell_edition = $PSVersionTable.PSEdition
    powershell_version = $PSVersionTable.PSVersion.ToString()
    process_architecture = if ([Environment]::Is64BitProcess) { 'x64' } else { 'x86' }
    os_architecture = $operatingSystem.OSArchitecture
    is_elevated = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(
        [Security.Principal.WindowsBuiltInRole]::Administrator
    )
    current_directory = (Get-Location).ProviderPath
    execution_policy = [ordered]@{}
    psscriptanalyzer_version = if ($null -eq $analyzer) { $null } else { $analyzer.Version.ToString() }
    pester_version = if ($null -eq $pester) { $null } else { $pester.Version.ToString() }
    powershell_exe = [bool](Get-Command powershell.exe -ErrorAction SilentlyContinue)
    pwsh_exe = [bool](Get-Command pwsh.exe -ErrorAction SilentlyContinue)
    console_input_encoding = [Console]::InputEncoding.WebName
    console_output_encoding = [Console]::OutputEncoding.WebName
    active_code_page = (& cmd.exe /d /c chcp 2>$null)
}

foreach ($entry in Get-ExecutionPolicy -List) {
    $profile.execution_policy[[string]$entry.Scope] = [string]$entry.ExecutionPolicy
}

$profile | ConvertTo-Json -Depth 5
