Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$stageRoot = Split-Path -Path $PSScriptRoot -Parent
$target = Join-Path $PSScriptRoot 'start-label-blind-aa-comfyui.ps1'
$evidence = Join-Path $stageRoot 'comfyui-runtime-label-blind-aa-c43875c3'
$guard = 'C:\Users\A\.codex\skills\powershell-reliability-guard\scripts\Invoke-GuardedPowerShell.ps1'
$incidentLog = Join-Path $stageRoot 'powershell-guard-incidents.jsonl'

& $guard -Path $target -Target PowerShell7 -Analyzer Optional -ScriptArguments @('-EvidenceDirectory', $evidence) -IncidentLogPath $incidentLog
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
