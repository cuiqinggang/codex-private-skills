[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateScript({ Test-Path -LiteralPath $_ -PathType Leaf })]
    [string]$Path,

    [ValidateSet('WindowsPowerShell51', 'PowerShell7', 'Current')]
    [string]$Target = 'WindowsPowerShell51',

    [ValidateSet('Optional', 'Required', 'Skip')]
    [string]$Analyzer = 'Optional',

    [string[]]$ScriptArguments = @(),

    [string]$IncidentLogPath = (Join-Path ([Environment]::GetFolderPath('LocalApplicationData')) 'PowerShellReliabilityGuard\incidents.jsonl'),

    [string]$LearnedCatalogPath = (Join-Path (Split-Path $PSScriptRoot -Parent) 'references\learned-errors.jsonl'),

    [string]$ResolveIncidentId,
    [string]$RootCause,
    [string]$Fix,
    [string]$Prevention
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

function Get-FileSha256([string]$LiteralPath) {
    $stream = [System.IO.File]::OpenRead($LiteralPath)
    $algorithm = [System.Security.Cryptography.SHA256]::Create()
    try {
        return ([BitConverter]::ToString($algorithm.ComputeHash($stream))).Replace('-', '').ToLowerInvariant()
    }
    finally {
        $algorithm.Dispose()
        $stream.Dispose()
    }
}

function Write-Utf8JsonLine([string]$LiteralPath, [object]$Value) {
    $directory = Split-Path $LiteralPath -Parent
    if (-not (Test-Path -LiteralPath $directory)) {
        [void](New-Item -ItemType Directory -Path $directory)
    }
    $line = $Value | ConvertTo-Json -Compress -Depth 8
    [System.IO.File]::AppendAllText(
        $LiteralPath,
        $line + [Environment]::NewLine,
        (New-Object System.Text.UTF8Encoding($false))
    )
}

function ConvertTo-NativeArgument([AllowEmptyString()][string]$Value) {
    if ($Value.Length -gt 0 -and $Value -notmatch '[\s"]') { return $Value }

    $builder = New-Object System.Text.StringBuilder
    [void]$builder.Append('"')
    $backslashes = 0
    foreach ($character in $Value.ToCharArray()) {
        if ($character -eq '\') {
            $backslashes++
            continue
        }
        if ($character -eq '"') {
            [void]$builder.Append((('\' * (($backslashes * 2) + 1)) -join ''))
            [void]$builder.Append('"')
            $backslashes = 0
            continue
        }
        if ($backslashes -gt 0) {
            [void]$builder.Append((('\' * $backslashes) -join ''))
            $backslashes = 0
        }
        [void]$builder.Append($character)
    }
    if ($backslashes -gt 0) {
        [void]$builder.Append((('\' * ($backslashes * 2)) -join ''))
    }
    [void]$builder.Append('"')
    return $builder.ToString()
}

function New-Incident(
    [string]$Phase,
    [string]$Summary,
    [int]$ExitCode,
    [string]$StandardOutput,
    [string]$StandardError,
    [object[]]$Issues
) {
    $incident = [ordered]@{
        schema_version = 1
        event = 'FAILURE_OPENED'
        incident_id = [guid]::NewGuid().ToString('N')
        recorded_utc = [DateTime]::UtcNow.ToString('o')
        phase = $Phase
        summary = $Summary
        script_path = $resolvedPath
        script_sha256 = $scriptHash
        target = $Target
        host_edition = $PSVersionTable.PSEdition
        host_version = $PSVersionTable.PSVersion.ToString()
        exit_code = $ExitCode
        stdout = $StandardOutput
        stderr = $StandardError
        issues = @($Issues)
    }
    Write-Utf8JsonLine -LiteralPath $resolvedIncidentLog -Value $incident
    return [pscustomobject]$incident
}

function Stop-WithIncident([object]$Incident) {
    [pscustomobject]@{
        Status = 'BLOCKED'
        IncidentId = $Incident.incident_id
        Phase = $Incident.phase
        Summary = $Incident.summary
        IncidentLog = $resolvedIncidentLog
    } | ConvertTo-Json -Depth 6
    exit 1
}

$resolvedPath = (Resolve-Path -LiteralPath $Path).ProviderPath
$resolvedIncidentLog = [System.IO.Path]::GetFullPath($IncidentLogPath)
$scriptHash = Get-FileSha256 -LiteralPath $resolvedPath

$hostMatchesTarget = switch ($Target) {
    'WindowsPowerShell51' { $PSVersionTable.PSEdition -eq 'Desktop' -and $PSVersionTable.PSVersion.Major -eq 5 }
    'PowerShell7' { $PSVersionTable.PSEdition -eq 'Core' -and $PSVersionTable.PSVersion.Major -ge 7 }
    'Current' { $true }
}
if (-not $hostMatchesTarget) {
    $incident = New-Incident -Phase 'HOST' `
        -Summary ('Runner host does not match target {0}.' -f $Target) `
        -ExitCode 1 -StandardOutput '' -StandardError '' -Issues @()
    Stop-WithIncident -Incident $incident
}

$checkerPath = Join-Path $PSScriptRoot 'Test-PowerShellArtifact.ps1'
try {
    $preflight = & $checkerPath -Path $resolvedPath -Target $Target -Analyzer $Analyzer -PassThru
}
catch {
    $incident = New-Incident -Phase 'PREFLIGHT_INTERNAL' -Summary $_.Exception.Message `
        -ExitCode 1 -StandardOutput '' -StandardError ($_ | Out-String) -Issues @()
    Stop-WithIncident -Incident $incident
}

if ($preflight.Status -ne 'PASS') {
    $incident = New-Incident -Phase 'PREFLIGHT' `
        -Summary ('Preflight rejected the script with {0} error(s).' -f $preflight.ErrorCount) `
        -ExitCode 1 -StandardOutput '' -StandardError '' -Issues @($preflight.Issues)
    Stop-WithIncident -Incident $incident
}

if (-not [string]::IsNullOrWhiteSpace($ResolveIncidentId)) {
    if ([string]::IsNullOrWhiteSpace($RootCause) -or
        [string]::IsNullOrWhiteSpace($Fix) -or
        [string]::IsNullOrWhiteSpace($Prevention)) {
        throw 'ResolveIncidentId requires RootCause, Fix, and Prevention. Guesses are not accepted.'
    }
}

$hostExecutable = [System.Diagnostics.Process]::GetCurrentProcess().MainModule.FileName
$nativeArguments = @('-NoLogo', '-NoProfile', '-NonInteractive')
if ($PSVersionTable.PSVersion.Major -le 5) {
    $nativeArguments += @('-ExecutionPolicy', 'Bypass')
}
$nativeArguments += @('-File', $resolvedPath)
$nativeArguments += $ScriptArguments
$argumentLine = (($nativeArguments | ForEach-Object { ConvertTo-NativeArgument -Value ([string]$_) }) -join ' ')

$startInfo = New-Object System.Diagnostics.ProcessStartInfo
$startInfo.FileName = $hostExecutable
$startInfo.Arguments = $argumentLine
$startInfo.UseShellExecute = $false
$startInfo.CreateNoWindow = $true
$startInfo.RedirectStandardOutput = $true
$startInfo.RedirectStandardError = $true
$process = New-Object System.Diagnostics.Process
$process.StartInfo = $startInfo

try {
    if (-not $process.Start()) { throw 'PowerShell child process did not start.' }
    $stdoutTask = $process.StandardOutput.ReadToEndAsync()
    $stderrTask = $process.StandardError.ReadToEndAsync()
    $process.WaitForExit()
    $standardOutput = $stdoutTask.Result
    $standardError = $stderrTask.Result
    $exitCode = $process.ExitCode
}
finally {
    $process.Dispose()
}

if ($exitCode -ne 0) {
    $summaryText = 'Target script returned non-zero exit code {0}.' -f $exitCode
    $incident = New-Incident -Phase 'EXECUTION' -Summary $summaryText -ExitCode $exitCode `
        -StandardOutput $standardOutput -StandardError $standardError -Issues @()
    Stop-WithIncident -Incident $incident
}

$archiveStatus = 'NOT_REQUESTED'
if (-not [string]::IsNullOrWhiteSpace($ResolveIncidentId)) {
    $sourceIncident = $null
    $alreadyResolved = $false
    if (Test-Path -LiteralPath $resolvedIncidentLog) {
        foreach ($line in [System.IO.File]::ReadAllLines($resolvedIncidentLog, [Text.Encoding]::UTF8)) {
            if ([string]::IsNullOrWhiteSpace($line)) { continue }
            $candidate = $line | ConvertFrom-Json
            if ($candidate.event -eq 'FAILURE_OPENED' -and $candidate.incident_id -eq $ResolveIncidentId) {
                $sourceIncident = $candidate
            }
            if ($candidate.event -eq 'FAILURE_VERIFIED_RESOLVED' -and $candidate.incident_id -eq $ResolveIncidentId) {
                $alreadyResolved = $true
            }
        }
    }
    if ($null -eq $sourceIncident) {
        throw ('Incident {0} was not found; verified experience was not archived.' -f $ResolveIncidentId)
    }
    if ($alreadyResolved) {
        throw ('Incident {0} was already resolved; duplicate archival was blocked.' -f $ResolveIncidentId)
    }
    if (-not [string]::Equals([string]$sourceIncident.script_path, $resolvedPath, [StringComparison]::OrdinalIgnoreCase)) {
        throw ('Incident {0} belongs to a different script path; verified experience was not archived.' -f $ResolveIncidentId)
    }

    $evidence = 'Incident {0}; failed hash {1}; passing hash {2}; passing exit code 0 at {3}.' -f `
        $ResolveIncidentId, $sourceIncident.script_sha256, $scriptHash, [DateTime]::UtcNow.ToString('o')
    $environment = '{0} {1}; target {2}' -f $PSVersionTable.PSEdition, $PSVersionTable.PSVersion, $Target
    $archiveScript = Join-Path $PSScriptRoot 'Add-PowerShellFailure.ps1'
    $archiveJson = & $archiveScript -Symptom $sourceIncident.summary -RootCause $RootCause `
        -Fix $Fix -Prevention $Prevention -Environment $environment -Evidence $evidence `
        -IncidentId $ResolveIncidentId -CatalogPath $LearnedCatalogPath
    $archiveResult = $archiveJson | ConvertFrom-Json
    $archiveStatus = $archiveResult.Status
    Write-Utf8JsonLine -LiteralPath $resolvedIncidentLog -Value ([ordered]@{
        schema_version = 1
        event = 'FAILURE_VERIFIED_RESOLVED'
        incident_id = $ResolveIncidentId
        recorded_utc = [DateTime]::UtcNow.ToString('o')
        passing_script_sha256 = $scriptHash
        learned_error_status = $archiveStatus
    })
}

[pscustomobject]@{
    Status = 'PASS'
    Path = $resolvedPath
    Sha256 = $scriptHash
    Target = $Target
    Analyzer = $preflight.Analyzer
    ExitCode = $exitCode
    StandardOutput = $standardOutput
    StandardError = $standardError
    VerifiedArchive = $archiveStatus
    IncidentLog = $resolvedIncidentLog
} | ConvertTo-Json -Depth 6
exit 0
