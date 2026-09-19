[CmdletBinding()]
param(
    [string]$EvidencePath = 'C:\AI\Bonsai2-27B-256K\evidence\20260919-233425',
    [string]$WorkspaceRoot = 'C:\AI\Bonsai2-27B-256K'
)

Set-StrictMode -Version 3.0
$ErrorActionPreference = 'Stop'

$demoRoot = Join-Path $WorkspaceRoot 'Bonsai-demo'
$stagingRoot = Join-Path $WorkspaceRoot 'downloads\staging\runtime'
$targetDir = Join-Path $demoRoot 'bin\cuda'
$backupRoot = Join-Path $WorkspaceRoot 'backup'
$expectedStamp = 'prism-b10709-9a9394a cuda-12.4'
$aria = Get-Command aria2c.exe -ErrorAction Stop
$utf8 = [Text.UTF8Encoding]::new($false)

foreach ($directory in @($EvidencePath, $stagingRoot)) {
    if (-not (Test-Path -LiteralPath $directory -PathType Container)) {
        [void][IO.Directory]::CreateDirectory($directory)
    }
}

function Write-JsonFile {
    param([string]$Path, [object]$Value)
    [IO.File]::WriteAllText($Path, ($Value | ConvertTo-Json -Depth 12) + [Environment]::NewLine, $utf8)
}

function Get-Length {
    param([string]$Path)
    if (Test-Path -LiteralPath $Path -PathType Leaf) {
        return [int64](Get-Item -LiteralPath $Path).Length
    }
    return [int64]0
}

function Get-LogCounts {
    param([string[]]$Paths)
    $retryCount = 0
    $errorCount = 0
    foreach ($path in $Paths) {
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { continue }
        $content = [IO.File]::ReadAllText($path)
        $retryCount += [regex]::Matches($content, '(?im)\bretry(?:ing)?\b').Count
        $errorCount += [regex]::Matches($content, '(?im)\b(error|failed|exception)\b').Count
    }
    [pscustomobject]@{ retry_count = $retryCount; error_count = $errorCount }
}

$monitorRows = [Collections.Generic.List[object]]::new()
$probeRecords = [Collections.Generic.List[object]]::new()

function New-AriaArguments {
    param(
        [pscustomobject]$Asset,
        [int]$Connections,
        [int]$Splits,
        [string]$LogPath
    )
    return @(
        '--continue=true'
        '--auto-file-renaming=false'
        '--allow-overwrite=false'
        '--file-allocation=none'
        '--max-tries=5'
        '--retry-wait=2'
        '--timeout=30'
        '--connect-timeout=30'
        '--summary-interval=5'
        '--console-log-level=notice'
        '--log-level=notice'
        "--log=$LogPath"
        "--dir=$stagingRoot"
        "--out=$($Asset.name)"
        "--max-connection-per-server=$Connections"
        "--split=$Splits"
        '--min-split-size=1M'
        $Asset.url
    )
}

function Start-AriaProcess {
    param(
        [pscustomobject]$Asset,
        [int]$Connections,
        [int]$Splits,
        [string]$StdoutPath,
        [string]$StderrPath,
        [string]$LogPath
    )
    $arguments = New-AriaArguments -Asset $Asset -Connections $Connections -Splits $Splits -LogPath $LogPath
    $startParameters = @{
        FilePath = $aria.Source
        ArgumentList = $arguments
        PassThru = $true
        WindowStyle = 'Hidden'
        RedirectStandardOutput = $StdoutPath
        RedirectStandardError = $StderrPath
    }
    return Start-Process @startParameters
}

function Invoke-Probe {
    param(
        [pscustomobject]$Asset,
        [int]$Connections,
        [int]$Splits,
        [int]$DurationSeconds,
        [string]$StageName
    )
    $filePath = Join-Path $stagingRoot $Asset.name
    $safeStage = '{0}-{1}' -f $Asset.id, $StageName
    $stdoutPath = Join-Path $EvidencePath "$safeStage.stdout.txt"
    $stderrPath = Join-Path $EvidencePath "$safeStage.stderr.txt"
    $logPath = Join-Path $EvidencePath "$safeStage.aria2.log"
    $before = Get-Length -Path $filePath
    $started = Get-Date
    $process = Start-AriaProcess -Asset $Asset -Connections $Connections -Splits $Splits -StdoutPath $stdoutPath -StderrPath $stderrPath -LogPath $logPath
    $lastBytes = $before
    while (-not $process.HasExited -and ((Get-Date) - $started).TotalSeconds -lt $DurationSeconds) {
        Start-Sleep -Seconds 5
        $currentBytes = Get-Length -Path $filePath
        $now = Get-Date
        $monitorRows.Add([pscustomobject]@{
            timestamp = $now.ToString('o')
            asset = $Asset.name
            stage = $StageName
            downloaded_bytes = $currentBytes
            delta_bytes = $currentBytes - $lastBytes
            interval_mib_s = [math]::Round(($currentBytes - $lastBytes) / 1MB / 5, 4)
            process_alive = -not $process.HasExited
        })
        $lastBytes = $currentBytes
    }
    $stoppedForProbe = $false
    if (-not $process.HasExited) {
        Stop-Process -Id $process.Id -Force
        $stoppedForProbe = $true
    }
    $process.WaitForExit()
    $ended = Get-Date
    $after = Get-Length -Path $filePath
    $elapsed = [math]::Max(($ended - $started).TotalSeconds, 0.001)
    $counts = Get-LogCounts -Paths @($logPath, $stderrPath)
    $record = [pscustomobject]@{
        asset = $Asset.name
        stage = $StageName
        connections = $Connections
        splits = $Splits
        elapsed_s = [math]::Round($elapsed, 3)
        bytes_before = $before
        bytes_after = $after
        delta_bytes = $after - $before
        mib_per_s = [math]::Round(($after - $before) / 1MB / $elapsed, 4)
        retry_count = $counts.retry_count
        error_count = $counts.error_count
        completed = $after -eq [int64]$Asset.bytes
        stopped_for_probe = $stoppedForProbe
        exit_code = $process.ExitCode
        stdout_path = [IO.Path]::GetRelativePath($EvidencePath, $stdoutPath)
        stderr_path = [IO.Path]::GetRelativePath($EvidencePath, $stderrPath)
        aria2_log_path = [IO.Path]::GetRelativePath($EvidencePath, $logPath)
    }
    $probeRecords.Add($record)
    return $record
}

function Invoke-FinalDownload {
    param(
        [pscustomobject]$Asset,
        [int]$Connections,
        [int]$Splits,
        [double]$BestProbeMibS,
        [string]$StageName
    )
    $filePath = Join-Path $stagingRoot $Asset.name
    $safeStage = '{0}-{1}' -f $Asset.id, $StageName
    $stdoutPath = Join-Path $EvidencePath "$safeStage.stdout.txt"
    $stderrPath = Join-Path $EvidencePath "$safeStage.stderr.txt"
    $logPath = Join-Path $EvidencePath "$safeStage.aria2.log"
    $started = Get-Date
    $lastBytes = Get-Length -Path $filePath
    $process = Start-AriaProcess -Asset $Asset -Connections $Connections -Splits $Splits -StdoutPath $stdoutPath -StderrPath $stderrPath -LogPath $logPath
    $zeroGrowthIntervals = 0
    $lowSpeedIntervals = 0
    $trigger = $null
    while (-not $process.HasExited) {
        Start-Sleep -Seconds 30
        $currentBytes = Get-Length -Path $filePath
        $delta = $currentBytes - $lastBytes
        $speed = $delta / 1MB / 30
        $monitorRows.Add([pscustomobject]@{
            timestamp = (Get-Date).ToString('o')
            asset = $Asset.name
            stage = $StageName
            downloaded_bytes = $currentBytes
            delta_bytes = $delta
            interval_mib_s = [math]::Round($speed, 4)
            process_alive = -not $process.HasExited
        })
        if ($delta -le 0) { $zeroGrowthIntervals++ } else { $zeroGrowthIntervals = 0 }
        if ($BestProbeMibS -gt 0 -and $speed -lt ($BestProbeMibS * 0.5)) {
            $lowSpeedIntervals++
        } else {
            $lowSpeedIntervals = 0
        }
        $lastBytes = $currentBytes
        if ($zeroGrowthIntervals -ge 2) { $trigger = 'NO_GROWTH_60S'; break }
        if ($lowSpeedIntervals -ge 4) { $trigger = 'BELOW_50_PERCENT_120S'; break }
    }
    if ($trigger -and -not $process.HasExited) {
        Stop-Process -Id $process.Id -Force
    }
    $process.WaitForExit()
    $ended = Get-Date
    $finalBytes = Get-Length -Path $filePath
    $counts = Get-LogCounts -Paths @($logPath, $stderrPath)
    return [pscustomobject]@{
        completed = $finalBytes -eq [int64]$Asset.bytes
        final_bytes = $finalBytes
        elapsed_s = [math]::Round(($ended - $started).TotalSeconds, 3)
        exit_code = $process.ExitCode
        retry_count = $counts.retry_count
        error_count = $counts.error_count
        recovery_trigger = $trigger
        stdout_path = [IO.Path]::GetRelativePath($EvidencePath, $stdoutPath)
        stderr_path = [IO.Path]::GetRelativePath($EvidencePath, $stderrPath)
        aria2_log_path = [IO.Path]::GetRelativePath($EvidencePath, $logPath)
    }
}

$assets = @(
    [pscustomobject]@{
        id = 'llama'
        name = 'llama-prism-b10709-9a9394a-bin-win-cuda-12.4-x64.zip'
        url = 'https://github.com/PrismML-Eng/llama.cpp/releases/download/prism-b10709-9a9394a/llama-prism-b10709-9a9394a-bin-win-cuda-12.4-x64.zip'
        bytes = [int64]253442371
        sha256 = 'f565c8428c1f108311f65ed97f02425188b3aa3c745c2bc597521bbd24bcbbc9'
    },
    [pscustomobject]@{
        id = 'cudart'
        name = 'cudart-llama-bin-win-cuda-12.4-x64.zip'
        url = 'https://github.com/PrismML-Eng/llama.cpp/releases/download/prism-b10709-9a9394a/cudart-llama-bin-win-cuda-12.4-x64.zip'
        bytes = [int64]391443627
        sha256 = '8c79a9b226de4b3cacfd1f83d24f962d0773be79f1e7b75c6af4ded7e32ae1d6'
    }
)

$modelBefore = @(Get-ChildItem -LiteralPath $demoRoot -Recurse -File -Filter '*.gguf' -ErrorAction SilentlyContinue)
$existingTarget = @()
if (Test-Path -LiteralPath $targetDir -PathType Container) {
    $existingTarget = @(Get-ChildItem -LiteralPath $targetDir -Recurse -File | ForEach-Object {
        [pscustomobject]@{
            path = [IO.Path]::GetRelativePath($targetDir, $_.FullName)
            size_bytes = $_.Length
            sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
        }
    })
}
Write-JsonFile -Path (Join-Path $EvidencePath 'runtime-existing-before.json') -Value $existingTarget

$assetResults = [Collections.Generic.List[object]]::new()
foreach ($asset in $assets) {
    $filePath = Join-Path $stagingRoot $asset.name
    $assetStarted = Get-Date
    $existingBytes = Get-Length -Path $filePath
    if ($existingBytes -gt $asset.bytes) {
        throw "Existing partial is larger than expected for $($asset.name)."
    }

    $p1 = $null
    $p4 = $null
    $p8 = $null
    if ($existingBytes -lt $asset.bytes) {
        $p1 = Invoke-Probe -Asset $asset -Connections 1 -Splits 1 -DurationSeconds 30 -StageName 'probe-x1'
    }
    if ((Get-Length -Path $filePath) -lt $asset.bytes) {
        $p4 = Invoke-Probe -Asset $asset -Connections 4 -Splits 4 -DurationSeconds 30 -StageName 'probe-x4'
    }

    $x8Decision = 'NOT_NEEDED'
    if ((Get-Length -Path $filePath) -lt $asset.bytes -and $null -ne $p4) {
        $p1Speed = if ($null -ne $p1) { [double]$p1.mib_per_s } else { 0.0 }
        $remaining = $asset.bytes - (Get-Length -Path $filePath)
        if ($p4.error_count -eq 0 -and $p4.mib_per_s -gt ($p1Speed * 1.15) -and $remaining -gt 64MB) {
            $x8Decision = 'TESTED_X4_GAIN_AND_REMAINING_GT_64MIB'
            $p8 = Invoke-Probe -Asset $asset -Connections 8 -Splits 8 -DurationSeconds 30 -StageName 'probe-x8'
        } else {
            $x8Decision = 'SKIPPED_NO_CLEAR_HEADROOM'
        }
    }

    $assetProbes = @($probeRecords.ToArray() | Where-Object asset -eq $asset.name)
    $stable = @($assetProbes | Where-Object { $_.delta_bytes -gt 0 -and $_.error_count -eq 0 } | Sort-Object mib_per_s -Descending)
    if ((Get-Length -Path $filePath) -lt $asset.bytes -and $stable.Count -eq 0) {
        throw "No stable download probe for $($asset.name)."
    }

    $selected = if ($stable.Count -gt 0) {
        $stable[0]
    } else {
        [pscustomobject]@{ connections = 1; splits = 1; mib_per_s = 0.0; stage = 'already-complete' }
    }
    $finalRun = $null
    $reprobePerformed = $false
    if ((Get-Length -Path $filePath) -lt $asset.bytes) {
        $finalRun = Invoke-FinalDownload -Asset $asset -Connections $selected.connections -Splits $selected.splits -BestProbeMibS $selected.mib_per_s -StageName 'final'
        if (-not $finalRun.completed -and $finalRun.recovery_trigger) {
            $reprobePerformed = $true
            [void](Invoke-Probe -Asset $asset -Connections 1 -Splits 1 -DurationSeconds 30 -StageName 'reprobe-x1')
            if ((Get-Length -Path $filePath) -lt $asset.bytes) {
                [void](Invoke-Probe -Asset $asset -Connections 4 -Splits 4 -DurationSeconds 30 -StageName 'reprobe-x4')
            }
            $assetProbes = @($probeRecords.ToArray() | Where-Object asset -eq $asset.name)
            $stable = @($assetProbes | Where-Object { $_.delta_bytes -gt 0 -and $_.error_count -eq 0 } | Sort-Object mib_per_s -Descending)
            if ((Get-Length -Path $filePath) -lt $asset.bytes -and $stable.Count -eq 0) {
                throw "Re-probe found no stable download mode for $($asset.name)."
            }
            if ($stable.Count -gt 0) { $selected = $stable[0] }
            if ((Get-Length -Path $filePath) -lt $asset.bytes) {
                $finalRun = Invoke-FinalDownload -Asset $asset -Connections $selected.connections -Splits $selected.splits -BestProbeMibS $selected.mib_per_s -StageName 'final-after-reprobe'
            }
        }
    }

    $actualBytes = Get-Length -Path $filePath
    if ($actualBytes -ne $asset.bytes) {
        throw "Size mismatch for $($asset.name): $actualBytes != $($asset.bytes)."
    }
    $actualHash = (Get-FileHash -LiteralPath $filePath -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actualHash -ne $asset.sha256) {
        throw "SHA256 mismatch for $($asset.name)."
    }
    $assetEnded = Get-Date
    $assetResults.Add([pscustomobject]@{
        name = $asset.name
        url = $asset.url
        expected_bytes = $asset.bytes
        actual_bytes = $actualBytes
        expected_sha256 = $asset.sha256
        actual_sha256 = $actualHash
        hash_verified = $true
        selected_connections = $selected.connections
        selected_splits = $selected.splits
        selected_probe_stage = $selected.stage
        selected_probe_mib_s = $selected.mib_per_s
        x8_decision = $x8Decision
        reprobe_performed = $reprobePerformed
        total_seconds = [math]::Round(($assetEnded - $assetStarted).TotalSeconds, 3)
        final_run = $finalRun
    })
}

Write-JsonFile -Path (Join-Path $EvidencePath 'runtime-download-probes.json') -Value $probeRecords.ToArray()
$monitorRows.ToArray() | Export-Csv -LiteralPath (Join-Path $EvidencePath 'runtime-download-monitor.csv') -NoTypeInformation -Encoding utf8

if (Test-Path -LiteralPath $targetDir -PathType Container) {
    $existingFiles = @(Get-ChildItem -LiteralPath $targetDir -Recurse -File)
    if ($existingFiles.Count -gt 0) {
        $stampPath = Join-Path $targetDir '.llama_release'
        $installedStamp = if (Test-Path -LiteralPath $stampPath) {
            [IO.File]::ReadAllText($stampPath).Trim()
        } else { '' }
        if ($installedStamp -ne $expectedStamp) {
            if (-not $installedStamp.StartsWith('prism-')) {
                throw 'Existing CUDA target is non-empty and cannot be confirmed as an older project runtime.'
            }
            [void][IO.Directory]::CreateDirectory($backupRoot)
            $backupPath = Join-Path $backupRoot ('runtime-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
            Move-Item -LiteralPath $targetDir -Destination $backupPath
        }
    }
}
if (-not (Test-Path -LiteralPath $targetDir -PathType Container)) {
    [void][IO.Directory]::CreateDirectory($targetDir)
}

foreach ($asset in $assets) {
    $zipPath = Join-Path $stagingRoot $asset.name
    Expand-Archive -LiteralPath $zipPath -DestinationPath $targetDir -Force
}
[IO.File]::WriteAllText((Join-Path $targetDir '.llama_release'), $expectedStamp, $utf8)

$serverPath = Join-Path $targetDir 'llama-server.exe'
$cliPath = Join-Path $targetDir 'llama-cli.exe'
if (-not (Test-Path -LiteralPath $serverPath -PathType Leaf)) { throw 'llama-server.exe missing after extraction.' }
if (-not (Test-Path -LiteralPath $cliPath -PathType Leaf)) { throw 'llama-cli.exe missing after extraction.' }

Push-Location $targetDir
try {
    $versionOutput = & $serverPath --version 2>&1 | Out-String
    $versionExit = $LASTEXITCODE
} finally {
    Pop-Location
}
[IO.File]::WriteAllText((Join-Path $EvidencePath 'llama-server-version.txt'), $versionOutput, $utf8)
Write-JsonFile -Path (Join-Path $EvidencePath 'llama-server-version.json') -Value ([ordered]@{
    command = "$serverPath --version"
    exit_code = $versionExit
    stdout_stderr = $versionOutput.Trim()
})
if ($versionExit -ne 0) { throw "llama-server --version failed with exit code $versionExit." }

$modelAfter = @(Get-ChildItem -LiteralPath $demoRoot -Recurse -File -Filter '*.gguf' -ErrorAction SilentlyContinue)
$modelDelta = $modelAfter.Count - $modelBefore.Count
if ($modelDelta -ne 0) { throw "Model file count changed during runtime phase: $modelDelta." }

$runtimeFiles = @(Get-ChildItem -LiteralPath $targetDir -Recurse -File | ForEach-Object {
    [pscustomobject]@{
        path = [IO.Path]::GetRelativePath($targetDir, $_.FullName).Replace('\','/')
        size_bytes = $_.Length
        sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    }
})

$final = [ordered]@{
    schema_version = 1
    status = 'PASS'
    runtime_source = 'PINNED_RELEASE'
    cuda_variant = '12.4'
    release = 'prism-b10709-9a9394a'
    runtime_hash_verified = $true
    cuda_binary_exists = $true
    setup_ps1_executed = $false
    model_files_downloaded_during_runtime_phase = $modelDelta
    model_file_count_before = $modelBefore.Count
    model_file_count_after = $modelAfter.Count
    llama_server_version_exit_code = $versionExit
    assets = $assetResults.ToArray()
    installed_files = $runtimeFiles
}
Write-JsonFile -Path (Join-Path $EvidencePath 'runtime-download-final.json') -Value $final
$final | ConvertTo-Json -Depth 6
exit 0
