#Requires -Version 7.0
$skillRoot = Split-Path -Parent $PSScriptRoot
$target = Join-Path $skillRoot 'scripts\p0\prepare-p0.ps1'
$guard = 'C:\Users\A\.codex\skills\powershell-reliability-guard\scripts\Invoke-GuardedPowerShell.ps1'
$evidence = Join-Path $skillRoot 'evidence\validation\pester-readiness.json'

Describe 'prepare-p0 readiness' {
    It 'keeps the evidence OutputPath separate from the discovered ComfyUI output path' {
        & $guard -Path $target -Target PowerShell7 -ScriptArguments @('-PackageRoot', $skillRoot, '-ApiEndpoint', 'http://127.0.0.1:1', '-OutputPath', $evidence)
        $LASTEXITCODE | Should Be 0
        $record = Get-Content -LiteralPath $evidence -Raw | ConvertFrom-Json
        $record.mode | Should Be 'READ_ONLY_READINESS'
        $record.benchmark_submitted | Should Be $false
        $record.p0_current | Should Be 'PENDING'
        $record.api_ready | Should Be $false
        $record.node_discovery_status | Should Be 'UNKNOWN_API_NOT_READY'
        $record.missing_node_classes | Should Be $null
        $record.output_path | Should Match 'ComfyUI.+output$'
    }
}
