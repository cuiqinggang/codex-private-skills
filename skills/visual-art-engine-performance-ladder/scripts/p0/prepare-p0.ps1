#Requires -Version 7.0
[CmdletBinding()]
param(
    [string]$ComfyUIRoot,
    [uri]$ApiEndpoint = 'http://127.0.0.1:8188',
    [string]$PackageRoot,
    [string]$OutputPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Test-CDrivePath {
    param([Parameter(Mandatory)][string]$Path)
    $full = [System.IO.Path]::GetFullPath($Path)
    if (-not $full.StartsWith('C:\', [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "BLOCKED_C_SOURCE_MISSING: only C-drive paths are allowed: $full"
    }
    return $full
}

function Invoke-ReadOnlyJson {
    param([Parameter(Mandatory)][string]$Uri)
    try {
        return Invoke-RestMethod -Method Get -Uri $Uri -TimeoutSec 3
    }
    catch {
        return $null
    }
}

$skillRoot = if ($PackageRoot) { Test-CDrivePath -Path $PackageRoot } else { Split-Path -Parent (Split-Path -Parent $PSScriptRoot) }
if (-not (Test-Path -LiteralPath (Join-Path $skillRoot 'SKILL.md') -PathType Leaf)) {
    throw "PackageRoot does not identify this skill package: $skillRoot"
}
$candidates = [System.Collections.Generic.List[string]]::new()
if ($ComfyUIRoot) {
    $candidates.Add((Test-CDrivePath -Path $ComfyUIRoot))
}
foreach ($candidate in @(
    'C:\AI\ComfyUI_Aaki_v3\ComfyUI',
    'C:\AI\ComfyUI\ComfyUI',
    'C:\AI\ComfyUI'
)) {
    if (-not $candidates.Contains($candidate)) {
        $candidates.Add($candidate)
    }
}

$resolvedRoot = $null
foreach ($candidate in $candidates) {
    if ((Test-Path -LiteralPath $candidate -PathType Container) -and
        (Test-Path -LiteralPath (Join-Path $candidate 'main.py') -PathType Leaf)) {
        $resolvedRoot = [System.IO.Path]::GetFullPath($candidate)
        break
    }
}

$pythonPath = $null
$inputPath = $null
$comfyOutputPath = $null
if ($resolvedRoot) {
    $parent = Split-Path -Parent $resolvedRoot
    foreach ($candidate in @(
        (Join-Path $resolvedRoot 'python.exe'),
        (Join-Path $resolvedRoot '.venv\Scripts\python.exe'),
        (Join-Path $parent 'python_embeded\python.exe'),
        (Join-Path $parent 'python\python.exe')
    )) {
        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            $pythonPath = [System.IO.Path]::GetFullPath($candidate)
            break
        }
    }
    $inputPath = Join-Path $resolvedRoot 'input'
    $comfyOutputPath = Join-Path $resolvedRoot 'output'
}

$baseUri = $ApiEndpoint.AbsoluteUri.TrimEnd('/')
$systemStats = Invoke-ReadOnlyJson -Uri "$baseUri/system_stats"
$queue = Invoke-ReadOnlyJson -Uri "$baseUri/queue"
$objectInfo = Invoke-ReadOnlyJson -Uri "$baseUri/object_info"
$nodeClasses = if ($objectInfo) { @($objectInfo.PSObject.Properties.Name) } else { @() }
$requiredNodes = @('LoadImage', 'SaveImage')
$missingNodes = $null
$nodesReady = $false
if ($null -ne $objectInfo) {
    $missingNodes = @($requiredNodes | Where-Object { $_ -notin $nodeClasses })
    $nodesReady = $missingNodes.Count -eq 0
}
$apiReady = $null -ne $systemStats -and $null -ne $queue

$result = [ordered]@{
    schema_version = 1
    generated_at = [DateTimeOffset]::UtcNow.ToString('o')
    mode = 'READ_ONLY_READINESS'
    c_drive_only = $true
    comfyui_root = $resolvedRoot
    python = $pythonPath
    api_endpoint = $baseUri
    api_ready = $apiReady
    input_path = $inputPath
    input_exists = [bool]($inputPath -and (Test-Path -LiteralPath $inputPath -PathType Container))
    output_path = $comfyOutputPath
    output_exists = [bool]($comfyOutputPath -and (Test-Path -LiteralPath $comfyOutputPath -PathType Container))
    queue_readable = $null -ne $queue
    object_info_readable = $null -ne $objectInfo
    node_discovery_status = if ($null -eq $objectInfo) { 'UNKNOWN_API_NOT_READY' } elseif ($nodesReady) { 'PASS' } else { 'MISSING_REQUIRED_NODES' }
    required_node_classes = $requiredNodes
    missing_node_classes = $missingNodes
    frozen_workflow_ready = $nodesReady
    benchmark_submitted = $false
    p0_current = 'PENDING'
    status = if (-not $resolvedRoot) {
        'BLOCKED_C_SOURCE_MISSING'
    } elseif (-not $apiReady) {
        'ENVIRONMENT_DISCOVERED_API_NOT_READY'
    } elseif (-not $nodesReady) {
        'P0_BLOCKED_NODE_UNAVAILABLE'
    } else {
        'P0_READINESS_PASS'
    }
}

$json = $result | ConvertTo-Json -Depth 8
if ($OutputPath) {
    $fullOutput = [System.IO.Path]::GetFullPath($OutputPath)
    if (-not $fullOutput.StartsWith($skillRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "OutputPath must remain inside the skill package: $skillRoot"
    }
    $parent = Split-Path -Parent $fullOutput
    if (-not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Force -Path $parent | Out-Null
    }
    [System.IO.File]::WriteAllText($fullOutput, $json + [Environment]::NewLine, [System.Text.UTF8Encoding]::new($false))
}
$json
