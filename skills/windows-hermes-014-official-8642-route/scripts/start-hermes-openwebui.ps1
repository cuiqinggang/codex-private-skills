param(
    [switch]$NoOpen,
    [int]$HermesTimeoutSeconds = 120,
    [int]$DockerTimeoutSeconds = 300,
    [int]$OpenWebUITimeoutSeconds = 180
)

$ErrorActionPreference = 'Stop'

$InstallRoot = 'H:\Hermes_Windows_Native_014'
$HermesExe = Join-Path $InstallRoot 'venv\Scripts\hermes.exe'
$DataPath = 'C:\Users\A\.hermes'
$LogsDir = Join-Path $DataPath 'logs'
$ReportsDir = Join-Path $InstallRoot 'reports'
$HermesHealthUrl = 'http://127.0.0.1:8642/health'
$ModelsUrl = 'http://127.0.0.1:8642/v1/models'
$OpenWebUIUrl = 'http://127.0.0.1:3000'
$DockerDesktopExe = 'C:\Program Files\Docker\Docker\Docker Desktop.exe'
$OpenWebUIContainers = @('open-webui-clean', 'open-webui')

New-Item -ItemType Directory -Force -Path $LogsDir, $ReportsDir | Out-Null
$RunStamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$RunLog = Join-Path $ReportsDir "daily-start-$RunStamp.log"

function Write-Log {
    param([string]$Message)
    $line = "[{0}] {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Message
    Write-Host $line
    Add-Content -LiteralPath $RunLog -Encoding UTF8 -Value $line
}

function Test-HttpOk {
    param(
        [string]$Uri,
        [int]$TimeoutSec = 5,
        [string]$ExpectedText = ''
    )
    try {
        $resp = Invoke-WebRequest -Uri $Uri -UseBasicParsing -TimeoutSec $TimeoutSec
        if ([int]$resp.StatusCode -lt 200 -or [int]$resp.StatusCode -ge 500) {
            return $false
        }
        if ($ExpectedText -and $resp.Content -notmatch [regex]::Escape($ExpectedText)) {
            return $false
        }
        return $true
    } catch {
        return $false
    }
}

function Wait-Until {
    param(
        [scriptblock]$Condition,
        [int]$TimeoutSeconds,
        [int]$IntervalSeconds = 2,
        [string]$Label
    )
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        if (& $Condition) {
            Write-Log "PASS $Label"
            return $true
        }
        Start-Sleep -Seconds $IntervalSeconds
    }
    Write-Log "FAIL $Label timeout=${TimeoutSeconds}s"
    return $false
}

function Get-PortOwner {
    param([int]$Port)
    $conn = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $conn) {
        return $null
    }
    $proc = Get-CimInstance Win32_Process -Filter "ProcessId=$($conn.OwningProcess)" -ErrorAction SilentlyContinue
    [pscustomobject]@{
        Port = $Port
        PID = $conn.OwningProcess
        Name = $proc.Name
        Path = $proc.ExecutablePath
        CommandLine = $proc.CommandLine
    }
}

function Ensure-Hermes {
    Write-Log 'G01_BEGIN Windows native Hermes 8642'
    if (-not (Test-Path -LiteralPath $HermesExe)) {
        Write-Log "G01_FAIL hermes.exe missing: $HermesExe"
        exit 1
    }
    if (-not (Test-Path -LiteralPath $DataPath)) {
        Write-Log "G01_FAIL data path missing: $DataPath"
        exit 1
    }

    if (Test-HttpOk -Uri $HermesHealthUrl -ExpectedText 'ok') {
        Write-Log 'G01_PASS Hermes 8642 already healthy'
    } else {
        $owner = Get-PortOwner -Port 8642
        if ($owner) {
            $isHermes = ($owner.CommandLine -match [regex]::Escape($InstallRoot) -and $owner.CommandLine -match 'hermes')
            if (-not $isHermes) {
                Write-Log "G01_FAIL port 8642 occupied by non-Hermes process pid=$($owner.PID) name=$($owner.Name)"
                exit 1
            }
            Write-Log "G01_FAIL port 8642 occupied by Hermes-like process but health is not OK; not killing pid=$($owner.PID)"
            exit 1
        }

        $stdout = Join-Path $LogsDir 'gateway-8642-stdout.log'
        $stderr = Join-Path $LogsDir 'gateway-8642-stderr.log'
        Write-Log 'G01_START Hermes gateway run --replace'
        Start-Process -FilePath $HermesExe -ArgumentList @('gateway', 'run', '--replace') -WorkingDirectory $InstallRoot -WindowStyle Hidden -RedirectStandardOutput $stdout -RedirectStandardError $stderr | Out-Null

        $ok = Wait-Until -TimeoutSeconds $HermesTimeoutSeconds -Label 'Hermes health 8642' -Condition {
            Test-HttpOk -Uri $HermesHealthUrl -ExpectedText 'ok'
        }
        if (-not $ok) {
            Write-Log "G01_FAIL Hermes did not become healthy; logs: $stdout ; $stderr"
            exit 1
        }
    }

    $modelsOk = Test-HttpOk -Uri $ModelsUrl -ExpectedText 'hermes-agent'
    if (-not $modelsOk) {
        Write-Log 'G01_FAIL /v1/models did not return hermes-agent'
        exit 1
    }
    Write-Log 'G01_PASS /v1/models has hermes-agent'
}

function Ensure-Docker {
    Write-Log 'G02_BEGIN Docker Desktop'
    $dockerReady = $false
    & docker version --format '{{.Server.Version}}' *> $null
    if ($LASTEXITCODE -eq 0) {
        $dockerReady = $true
    }
    if (-not $dockerReady) {
        if (-not (Test-Path -LiteralPath $DockerDesktopExe)) {
            Write-Log "G02_FAIL Docker Desktop missing: $DockerDesktopExe"
            exit 1
        }
        Write-Log 'G02_START Docker Desktop'
        Start-Process -FilePath $DockerDesktopExe -WindowStyle Hidden | Out-Null
        $dockerReady = Wait-Until -TimeoutSeconds $DockerTimeoutSeconds -IntervalSeconds 3 -Label 'Docker API ready' -Condition {
            & docker version --format '{{.Server.Version}}' *> $null
            $LASTEXITCODE -eq 0
        }
        if (-not $dockerReady) {
            Write-Log 'G02_FAIL Docker API not ready'
            exit 1
        }
    } else {
        Write-Log 'G02_PASS Docker API already ready'
    }
}

function Ensure-OpenWebUI {
    Write-Log 'G03_BEGIN Open WebUI 3000'
    if (Test-HttpOk -Uri $OpenWebUIUrl -ExpectedText 'Open WebUI') {
        Write-Log 'G03_PASS Open WebUI already healthy'
    } else {
        $chosen = $null
        $containers = & docker ps -a --format '{{.Names}}'
        foreach ($name in $OpenWebUIContainers) {
            if ($containers -contains $name) {
                $chosen = $name
                break
            }
        }
        if (-not $chosen) {
            Write-Log 'G03_FAIL no known Open WebUI container found'
            exit 1
        }

        Write-Log "G03_START docker start $chosen"
        & docker start $chosen *> $null
        if ($LASTEXITCODE -ne 0) {
            Write-Log "G03_WARN docker start $chosen returned exit code $LASTEXITCODE; will still wait for HTTP 3000 because Docker may already have another Open WebUI container bound"
        }

        $ok = Wait-Until -TimeoutSeconds $OpenWebUITimeoutSeconds -IntervalSeconds 3 -Label 'Open WebUI HTTP 3000' -Condition {
            Test-HttpOk -Uri $OpenWebUIUrl -ExpectedText 'Open WebUI'
        }
        if (-not $ok) {
            $owner = Get-PortOwner -Port 3000
            if ($owner) {
                Write-Log "G03_FAIL port 3000 owner pid=$($owner.PID) name=$($owner.Name)"
            } else {
                Write-Log 'G03_FAIL no listener on port 3000'
            }
            exit 1
        }
    }
}

function Open-Page {
    Write-Log 'G04_BEGIN Open browser page'
    if ($NoOpen) {
        Write-Log 'G04_SKIP NoOpen was specified'
    } else {
        Start-Process $OpenWebUIUrl | Out-Null
        Write-Log "G04_PASS opened $OpenWebUIUrl"
    }
}

Write-Log 'START Windows native Hermes daily launcher'
Write-Log "RunLog: $RunLog"
Write-Log 'Order: Hermes 8642 -> Docker Desktop -> Open WebUI 3000 -> browser'
Ensure-Hermes
Ensure-Docker
Ensure-OpenWebUI
Open-Page
Write-Log 'FINAL_PASS Windows native Hermes page is ready'
