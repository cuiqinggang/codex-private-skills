[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$EvidenceDirectory
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$comfyRoot = 'C:\AI\ComfyUI_Aaki_v3'
$pythonExe = Join-Path $comfyRoot 'python\python.exe'
$mainScript = Join-Path $comfyRoot 'ComfyUI\main.py'
$outputDirectory = Join-Path $comfyRoot 'data\output'
$inputDirectory = Join-Path $comfyRoot 'data\input'
$tempDirectory = Join-Path $comfyRoot 'data\temp'
$resolvedEvidence = [System.IO.Path]::GetFullPath($EvidenceDirectory)

if (Test-Path -LiteralPath $resolvedEvidence) {
    throw "Evidence directory already exists: $resolvedEvidence"
}
foreach ($required in @($pythonExe, $mainScript, $outputDirectory, $inputDirectory, $tempDirectory)) {
    if (-not (Test-Path -LiteralPath $required)) {
        throw "Required ComfyUI path missing: $required"
    }
}

if (Get-NetTCPConnection -LocalPort 8188 -State Listen -ErrorAction SilentlyContinue) {
    throw 'Port 8188 already has a TCP listener; refusing to claim, replace, or stop it.'
}

$null = New-Item -ItemType Directory -Path $resolvedEvidence
$stdoutPath = Join-Path $resolvedEvidence 'stdout.log'
$stderrPath = Join-Path $resolvedEvidence 'stderr.log'
$arguments = @(
    '-s',
    'ComfyUI\main.py',
    '--windows-standalone-build',
    '--listen', '127.0.0.1',
    '--port', '8188',
    '--output-directory', $outputDirectory,
    '--input-directory', $inputDirectory,
    '--temp-directory', $tempDirectory
)
$process = Start-Process -FilePath $pythonExe -ArgumentList $arguments -WorkingDirectory $comfyRoot -RedirectStandardOutput $stdoutPath -RedirectStandardError $stderrPath -WindowStyle Hidden -PassThru
$launch = [ordered]@{
    owned = $true
    pid = $process.Id
    started_at = [DateTimeOffset]::UtcNow.ToString('o')
    executable = $pythonExe
    working_directory = $comfyRoot
    arguments = $arguments
    powershell_version = $PSVersionTable.PSVersion.ToString()
    powershell_home = $PSHOME
    powershell_process = (Get-Process -Id $PID).Path
    requested_listen_address = '127.0.0.1'
    readiness = 'PENDING'
}
$launch | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $resolvedEvidence 'launch.json') -Encoding utf8NoBOM

$ready = $false
try {
    for ($attempt = 1; $attempt -le 60; $attempt++) {
        if ($process.HasExited) {
            throw "Owned ComfyUI process exited early with code $($process.ExitCode)."
        }
        try {
            $response = Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:8188/object_info' -TimeoutSec 2
            if ($response.StatusCode -eq 200) {
                $ready = $true
                break
            }
        } catch {
        }
        Start-Sleep -Seconds 1
    }
    if (-not $ready) {
        throw 'Owned ComfyUI did not become ready within 60 checks.'
    }
    $listener = Get-NetTCPConnection -LocalPort 8188 -State Listen -ErrorAction Stop |
        Where-Object { $_.OwningProcess -eq $process.Id -and $_.LocalAddress -eq '127.0.0.1' }
    if (-not $listener) {
        throw 'Readiness succeeded but the owned PID was not verified on 127.0.0.1:8188.'
    }
    $launch.readiness = 'PASS'
    $launch.listener = @($listener | Select-Object LocalAddress, LocalPort, OwningProcess, State)
    $launch | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $resolvedEvidence 'launch.json') -Encoding utf8NoBOM
} catch {
    if (-not $process.HasExited) {
        Stop-Process -Id $process.Id -Force
    }
    throw
}

[pscustomobject]@{
    status = 'COMFYUI_READY'
    owned_pid = $process.Id
    endpoint = 'http://127.0.0.1:8188'
    evidence_directory = $resolvedEvidence
} | ConvertTo-Json -Depth 4
