[CmdletBinding()]
param(
    [string]$WorkspaceRoot = 'C:\AI\Bonsai2-27B-256K'
)

Set-StrictMode -Version 3.0
$ErrorActionPreference = 'Stop'

function Invoke-NativeCapture {
    param(
        [Parameter(Mandatory = $true)]
        [string]$FilePath,
        [string[]]$ArgumentList = @()
    )
    $output = & $FilePath @ArgumentList 2>&1 | Out-String
    $exitCode = $LASTEXITCODE
    [pscustomobject]@{
        command = $FilePath
        arguments = $ArgumentList
        exit_code = $exitCode
        output = $output.Trim()
    }
}

function Convert-NullableDouble {
    param([AllowNull()]$Value)
    if ($null -eq $Value -or [string]::IsNullOrWhiteSpace([string]$Value)) {
        return $null
    }
    return [double]$Value
}

function Protect-ProxyValue {
    param([AllowNull()][string]$Value)
    if ([string]::IsNullOrWhiteSpace($Value)) { return $Value }
    return ($Value -replace '(?i)(://)[^/@:\s]+:[^/@\s]+@', '$1***:***@')
}

$timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$workspaceExisted = Test-Path -LiteralPath $WorkspaceRoot -PathType Container
$workspaceEntriesBefore = @()
if ($workspaceExisted) {
    $workspaceEntriesBefore = @(Get-ChildItem -LiteralPath $WorkspaceRoot -Force |
        Select-Object Name, FullName, PSIsContainer, Length, LastWriteTimeUtc)
}

$bonsaiDemoPath = Join-Path $WorkspaceRoot 'Bonsai-demo'
$stagingPath = Join-Path $WorkspaceRoot 'downloads\staging'
$evidenceRoot = Join-Path $WorkspaceRoot 'evidence'
$evidencePath = Join-Path $evidenceRoot $timestamp
foreach ($directory in @($WorkspaceRoot, $stagingPath, $evidenceRoot, $evidencePath)) {
    if (-not (Test-Path -LiteralPath $directory -PathType Container)) {
        [void][System.IO.Directory]::CreateDirectory($directory)
    }
}

$gitCommand = Get-Command git.exe -ErrorAction SilentlyContinue
$curlCommand = Get-Command curl.exe -ErrorAction SilentlyContinue
$ariaCommand = Get-Command aria2c.exe -ErrorAction SilentlyContinue
$nvidiaCommand = Get-Command nvidia-smi.exe -ErrorAction SilentlyContinue

$gitVersion = if ($null -ne $gitCommand) {
    Invoke-NativeCapture -FilePath $gitCommand.Source -ArgumentList @('--version')
} else { $null }
$curlVersion = if ($null -ne $curlCommand) {
    Invoke-NativeCapture -FilePath $curlCommand.Source -ArgumentList @('--version')
} else { $null }
$ariaVersion = if ($null -ne $ariaCommand) {
    Invoke-NativeCapture -FilePath $ariaCommand.Source -ArgumentList @('--version')
} else { $null }
$nvidiaSummary = if ($null -ne $nvidiaCommand) {
    Invoke-NativeCapture -FilePath $nvidiaCommand.Source
} else { $null }

$gpuRows = @()
if ($null -ne $nvidiaCommand) {
    $queryArgs = @(
        '--query-gpu=index,name,memory.total,memory.used,driver_version'
        '--format=csv,noheader,nounits'
    )
    $queryOutput = & $nvidiaCommand.Source @queryArgs 2>&1
    $queryExit = $LASTEXITCODE
    if ($queryExit -eq 0) {
        foreach ($line in @($queryOutput)) {
            $parts = ([string]$line).Split(',') | ForEach-Object { $_.Trim() }
            if ($parts.Count -eq 5) {
                $gpuRows += [pscustomobject]@{
                    index = [int]$parts[0]
                    name = $parts[1]
                    memory_total_mib = Convert-NullableDouble $parts[2]
                    memory_used_mib = Convert-NullableDouble $parts[3]
                    driver_version = $parts[4]
                }
            }
        }
    }
}

$cudaReportedVersion = $null
if ($null -ne $nvidiaSummary -and $nvidiaSummary.output -match 'CUDA Version:\s*([0-9.]+)') {
    $cudaReportedVersion = $Matches[1]
}

$operatingSystem = Get-CimInstance -ClassName Win32_OperatingSystem
$systemDrive = Get-CimInstance -ClassName Win32_LogicalDisk -Filter "DeviceID='C:'"
$proxyNames = @(
    'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'NO_PROXY',
    'http_proxy', 'https_proxy', 'all_proxy', 'no_proxy'
)
$proxyEnvironment = [ordered]@{}
foreach ($name in $proxyNames) {
    $proxyEnvironment[$name] = Protect-ProxyValue ([Environment]::GetEnvironmentVariable($name, 'Process'))
}

$ramTotalBytes = [double]$operatingSystem.TotalVisibleMemorySize * 1KB
$ramFreeBytes = [double]$operatingSystem.FreePhysicalMemory * 1KB
$cFreeBytes = [double]$systemDrive.FreeSpace
$nvidiaPresent = $null -ne $nvidiaCommand -and $gpuRows.Count -gt 0
$targetGpuPresent = @($gpuRows | Where-Object { $_.name -match '(?i)2080\s*Ti' }).Count -gt 0
$diskGatePass = $cFreeBytes -ge 20GB
$status = if ($nvidiaPresent -and $targetGpuPresent -and $diskGatePass) { 'PASS' } else { 'BLOCKED' }

$failureReasons = @()
if (-not $nvidiaPresent) { $failureReasons += 'NVIDIA_GPU_NOT_DETECTED' }
if ($nvidiaPresent -and -not $targetGpuPresent) { $failureReasons += 'TARGET_2080_TI_CLASS_DEVICE_NOT_DETECTED' }
if (-not $diskGatePass) { $failureReasons += 'C_DRIVE_FREE_SPACE_BELOW_20_GIB' }

$preflight = [ordered]@{
    schema_version = 1
    task = 'qwen38-bonsai2-pq2-256k-baseline-v1'
    captured_local = (Get-Date).ToString('o')
    status = $status
    failure_reasons = $failureReasons
    workspace = [ordered]@{
        root = $WorkspaceRoot
        existed_before = $workspaceExisted
        entries_before = $workspaceEntriesBefore
        bonsai_demo_path = $bonsaiDemoPath
        staging_path = $stagingPath
        evidence_path = $evidencePath
    }
    powershell = [ordered]@{
        edition = $PSVersionTable.PSEdition
        version = $PSVersionTable.PSVersion.ToString()
        process_path = [System.Diagnostics.Process]::GetCurrentProcess().MainModule.FileName
        pshome = $PSHOME
    }
    tools = [ordered]@{
        git = $gitVersion
        curl = $curlVersion
        aria2c_present = $null -ne $ariaCommand
        aria2c = $ariaVersion
        nvidia_smi_present = $null -ne $nvidiaCommand
        nvidia_smi = $nvidiaSummary
    }
    gpu = $gpuRows
    cuda_driver_reported_version = $cudaReportedVersion
    ram = [ordered]@{
        total_bytes = [int64]$ramTotalBytes
        available_bytes = [int64]$ramFreeBytes
        total_gib = [math]::Round($ramTotalBytes / 1GB, 3)
        available_gib = [math]::Round($ramFreeBytes / 1GB, 3)
    }
    c_drive = [ordered]@{
        free_bytes = [int64]$cFreeBytes
        free_gib = [math]::Round($cFreeBytes / 1GB, 3)
        gate_minimum_gib = 20
        gate_pass = $diskGatePass
    }
    proxy_environment_read_only = $proxyEnvironment
    gates = [ordered]@{
        nvidia_gpu_present = $nvidiaPresent
        target_2080_ti_class_present = $targetGpuPresent
        c_drive_20_gib_free = $diskGatePass
        phase_b_authorized = $status -eq 'PASS'
    }
    prohibited_actions_confirmed = [ordered]@{
        proxy_changed = $false
        network_changed = $false
        system_settings_changed = $false
        model_download_started = $false
    }
}

$jsonPath = Join-Path $evidencePath 'preflight.json'
$textPath = Join-Path $evidencePath 'preflight.txt'
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
$json = $preflight | ConvertTo-Json -Depth 10
[System.IO.File]::WriteAllText($jsonPath, $json + [Environment]::NewLine, $utf8NoBom)

$textLines = @(
    'TASK=qwen38-bonsai2-pq2-256k-baseline-v1'
    "STATUS=$status"
    "TIMESTAMP=$timestamp"
    "EVIDENCE_PATH=$evidencePath"
    "POWERSHELL_VERSION=$($PSVersionTable.PSVersion)"
    "POWERSHELL_PATH=$([System.Diagnostics.Process]::GetCurrentProcess().MainModule.FileName)"
    "GIT_VERSION=$($gitVersion.output)"
    "CURL_VERSION=$($curlVersion.output -split [Environment]::NewLine | Select-Object -First 1)"
    "ARIA2C_PRESENT=$($null -ne $ariaCommand)"
    "NVIDIA_GPU_PRESENT=$nvidiaPresent"
    "TARGET_2080_TI_CLASS_PRESENT=$targetGpuPresent"
    "GPU_NAMES=$(($gpuRows.name) -join '; ')"
    "GPU_MEMORY_TOTAL_MIB=$(($gpuRows.memory_total_mib) -join '; ')"
    "GPU_MEMORY_USED_MIB=$(($gpuRows.memory_used_mib) -join '; ')"
    "CUDA_DRIVER_REPORTED_VERSION=$cudaReportedVersion"
    "RAM_TOTAL_GIB=$($preflight.ram.total_gib)"
    "RAM_AVAILABLE_GIB=$($preflight.ram.available_gib)"
    "C_DRIVE_FREE_GIB=$($preflight.c_drive.free_gib)"
    "C_DRIVE_GATE_PASS=$diskGatePass"
    "PROXY_ENV_READ_ONLY=$(($proxyEnvironment | ConvertTo-Json -Compress))"
    "FAILURE_REASONS=$($failureReasons -join ',')"
    'PROXY_CHANGED=NO'
    'NETWORK_CHANGED=NO'
    'SYSTEM_SETTINGS_CHANGED=NO'
    'MODEL_DOWNLOAD_STARTED=NO'
    "PHASE_B_AUTHORIZED=$($status -eq 'PASS')"
)
[System.IO.File]::WriteAllLines($textPath, $textLines, $utf8NoBom)

[pscustomobject]@{
    status = $status
    timestamp = $timestamp
    evidence_path = $evidencePath
    preflight_json = $jsonPath
    preflight_txt = $textPath
    failure_reasons = $failureReasons
} | ConvertTo-Json -Depth 5

if ($status -ne 'PASS') { exit 2 }
exit 0
