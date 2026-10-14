param(
    [switch]$NoOpen,
    [switch]$StartBackendOnly,
    [switch]$WaitAndOpen,
    [int]$HermesTimeoutSeconds = 120,
    [int]$HermesModelsTimeoutSeconds = 180,
    [int]$DockerTimeoutSeconds = 300,
    [int]$OpenWebUITimeoutSeconds = 180,
    [int]$StageDelaySeconds = 90
)

$ErrorActionPreference = 'Stop'

$InstallRoot = Split-Path -Parent $PSScriptRoot
$HermesExe = "C:\Users\A\.hermes\hermes-agent\venv\Scripts\hermes.exe"
$DataPath = 'C:\Users\A\.hermes'
$env:HERMES_HOME = $DataPath
$LogsDir = Join-Path $DataPath 'logs'
$ReportsDir = Join-Path $InstallRoot 'reports'
$HermesHealthUrl = 'http://127.0.0.1:8642/health'
$ModelsUrl = 'http://127.0.0.1:8642/v1/models'
$HermesModelId = 'DeepSeek-V4-Pro'
$OpenWebUIUrl = 'http://127.0.0.1:3000'
$DockerDesktopExe = 'C:\Program Files\Docker\Docker\Docker Desktop.exe'
$OpenWebUIContainers = @('open-webui-clean', 'open-webui')
$GatewayProxyUrl = 'http://127.0.0.1:7890'

New-Item -ItemType Directory -Force -Path $LogsDir, $ReportsDir | Out-Null
$RunStamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$RunLog = Join-Path $ReportsDir "daily-start-$RunStamp.log"
$script:BackendStartRequested = $false

function Get-ApiServerHeaders {
    $envPath = Join-Path $DataPath '.env'
    if (-not (Test-Path -LiteralPath $envPath)) {
        return @{}
    }
    $line = Get-Content -LiteralPath $envPath -ErrorAction SilentlyContinue |
        Where-Object { $_ -match '^API_SERVER_KEY=' } |
        Select-Object -First 1
    if (-not $line) {
        return @{}
    }
    $key = ($line -replace '^API_SERVER_KEY=', '').Trim().Trim('"').Trim("'")
    if (-not $key) {
        return @{}
    }
    return @{ Authorization = "Bearer $key" }
}

$script:ApiServerHeaders = Get-ApiServerHeaders

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
        $requestArgs = @{
            Uri = $Uri
            UseBasicParsing = $true
            TimeoutSec = $TimeoutSec
        }
        if ($script:ApiServerHeaders.Count -gt 0) {
            $requestArgs.Headers = $script:ApiServerHeaders
        }
        $resp = Invoke-WebRequest @requestArgs
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

function Test-WindowsHermesOwner {
    param([pscustomobject]$Owner)
    if (-not $Owner) {
        return $false
    }
    $lineage = @($Owner.CommandLine)
    $currentPid = $Owner.PID
    for ($i = 0; $i -lt 4; $i++) {
        $proc = Get-CimInstance Win32_Process -Filter "ProcessId=$currentPid" -ErrorAction SilentlyContinue
        if (-not $proc -or -not $proc.ParentProcessId) {
            break
        }
        $parent = Get-CimInstance Win32_Process -Filter "ProcessId=$($proc.ParentProcessId)" -ErrorAction SilentlyContinue
        if (-not $parent) {
            break
        }
        $lineage += $parent.CommandLine
        $currentPid = $parent.ProcessId
    }
    $combined = ($lineage -join "`n")
    $legacyGateway = (
        (
            $combined -match [regex]::Escape($InstallRoot) -or
            $combined -match [regex]::Escape('C:\Users\A\.hermes\gateway-service\Hermes_Gateway.cmd') -or
            $combined -match 'hermes_cli\.main'
        ) -and
        $combined -match 'gateway run'
    )
    $hiddenGatewayService = $combined -match [regex]::Escape('C:\Users\A\.hermes\gateway-service\run-hermes-gateway-hidden.py')
    return ($legacyGateway -or $hiddenGatewayService)
}

function Wait-PortFree {
    param(
        [int]$Port,
        [int]$TimeoutSeconds = 20
    )
    Wait-Until -TimeoutSeconds $TimeoutSeconds -IntervalSeconds 1 -Label "Port $Port free" -Condition {
        -not (Get-PortOwner -Port $Port)
    }
}

function Invoke-DockerBounded {
    param([string]$ArgumentLine, [int]$TimeoutSeconds = 10)
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = 'C:\Program Files\Docker\Docker\resources\bin\docker.exe'
    $psi.Arguments = $ArgumentLine
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $psi
    try {
        [void]$process.Start()
        $stdout = $process.StandardOutput.ReadToEndAsync()
        $stderr = $process.StandardError.ReadToEndAsync()
        if (-not $process.WaitForExit($TimeoutSeconds * 1000)) {
            $process.Kill()
            Write-Log "G02_WARN Docker CLI timed out: $ArgumentLine"
            return $false
        }
        return ($process.ExitCode -eq 0)
    } catch { return $false } finally { $process.Dispose() }
}

function Test-DockerReady {
    return (Invoke-DockerBounded -ArgumentLine 'version --format {{.Server.Version}}' -TimeoutSeconds 8)
}

function Stop-LauncherWindowsHermesProcesses {
    $procs = Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |
        Where-Object {
            $_.CommandLine -match [regex]::Escape($InstallRoot) -and
            $_.CommandLine -match 'hermes' -and
            $_.CommandLine -match 'gateway run'
        }
    foreach ($proc in $procs) {
        Write-Log "G01_WARN stopping stale Windows Hermes gateway pid=$($proc.ProcessId)"
        Stop-Process -Id $proc.ProcessId -Force -ErrorAction SilentlyContinue
    }
}

function Stop-KnownHermesPortConflict {
    param([pscustomobject]$Owner)

    if (-not $Owner) {
        return $true
    }

    $isWslRelay = $Owner.Name -eq 'wslrelay.exe'
    $isWindowsHermes = Test-WindowsHermesOwner -Owner $Owner

    if ($isWindowsHermes) {
        Write-Log "G01_WARN stale Windows Hermes on 8642 pid=$($Owner.PID); stopping targeted process"
        Stop-Process -Id $Owner.PID -Force -ErrorAction SilentlyContinue
        return (Wait-PortFree -Port 8642 -TimeoutSeconds 20)
    }

    if ($isWslRelay) {
        Write-Log "G01_WARN 8642 is owned by WSL relay pid=$($Owner.PID); stopping old WSL Hermes gateway only"
        & wsl.exe -d Ubuntu-24.04 -- sh -lc "pkill -f '/.local/bin/hermes gateway run --replace' || true" *> $null
        Start-Sleep -Seconds 2
        $stillOwner = Get-PortOwner -Port 8642
        if ($stillOwner -and $stillOwner.Name -eq 'wslrelay.exe') {
            Write-Log "G01_WARN forcing stale WSL relay off 8642 pid=$($stillOwner.PID)"
            Stop-Process -Id $stillOwner.PID -Force -ErrorAction SilentlyContinue
        }
        return (Wait-PortFree -Port 8642 -TimeoutSeconds 20)
    }

    Write-Log "G01_FAIL port 8642 occupied by unknown process pid=$($Owner.PID) name=$($Owner.Name); not stopping it"
    return $false
}

function Test-WindowsHermesHealthReady {
    $owner = Get-PortOwner -Port 8642
    if (-not $owner) {
        return $false
    }
    if (Test-WindowsHermesOwner -Owner $owner) {
        return (Test-HttpOk -Uri $HermesHealthUrl -ExpectedText 'ok')
    }
    if ($owner.Name -eq 'wslrelay.exe') {
        Write-Log "G01_WARN WSL relay reclaimed 8642 during Windows Hermes startup pid=$($owner.PID)"
        Stop-KnownHermesPortConflict -Owner $owner | Out-Null
        return $false
    }
    return $false
}

function Test-WindowsHermesModels {
    $owner = Get-PortOwner -Port 8642
    if (-not $owner) {
        return $false
    }
    if (Test-WindowsHermesOwner -Owner $owner) {
        return (Test-HttpOk -Uri $ModelsUrl -TimeoutSec 10 -ExpectedText $HermesModelId)
    }
    if ($owner.Name -eq 'wslrelay.exe') {
        Write-Log "G01_WARN WSL relay reclaimed 8642 while waiting for /v1/models pid=$($owner.PID)"
        Stop-KnownHermesPortConflict -Owner $owner | Out-Null
        return $false
    }
    return $false
}

function Start-WindowsHermesGateway {
    $stdout = Join-Path $LogsDir 'gateway-8642-stdout.log'
    $stderr = Join-Path $LogsDir 'gateway-8642-stderr.log'
    Stop-LauncherWindowsHermesProcesses
    $env:HTTPS_PROXY = $GatewayProxyUrl
    $env:HTTP_PROXY = $GatewayProxyUrl
    $env:ALL_PROXY = $GatewayProxyUrl
    if ($script:ApiServerHeaders.ContainsKey('Authorization')) {
        $env:API_SERVER_KEY = ($script:ApiServerHeaders.Authorization -replace '^Bearer\s+', '')
    }
    $env:HERMES_GATEWAY_PLATFORM_CONNECT_TIMEOUT = '45'
    $env:HERMES_TELEGRAM_HTTP_CONNECT_TIMEOUT = '30'
    $env:HERMES_TELEGRAM_HTTP_READ_TIMEOUT = '60'
    $env:HERMES_TELEGRAM_HTTP_WRITE_TIMEOUT = '60'
    $env:HERMES_TELEGRAM_HTTP_POOL_TIMEOUT = '20'
    Write-Log "G01_INFO Gateway proxy env set for child process: $GatewayProxyUrl"
    Write-Log 'G01_START Windows native Hermes gateway run --replace'
    $script:BackendStartRequested = $true
    Start-Process -FilePath $HermesExe -ArgumentList @('gateway', 'run', '--replace') -WorkingDirectory $InstallRoot -WindowStyle Hidden -RedirectStandardOutput $stdout -RedirectStandardError $stderr | Out-Null

    $ok = Wait-Until -TimeoutSeconds $HermesTimeoutSeconds -Label 'Windows Hermes owns 8642 and health is OK' -Condition {
        Test-WindowsHermesHealthReady
    }
    if (-not $ok) {
        Write-Log "G01_FAIL Hermes did not become healthy; logs: $stdout ; $stderr"
        exit 1
    }

    $modelsOk = Wait-Until -TimeoutSeconds $HermesModelsTimeoutSeconds -IntervalSeconds 3 -Label "/v1/models has $HermesModelId" -Condition {
        Test-WindowsHermesModels
    }
    if (-not $modelsOk) {
        Write-Log "G01_FAIL /v1/models did not return $HermesModelId after Windows Hermes start"
        exit 1
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

    $healthOk = Test-HttpOk -Uri $HermesHealthUrl -ExpectedText 'ok'
    $modelsOk = Test-WindowsHermesModels
    if ($healthOk -and $modelsOk) {
        Write-Log 'G01_PASS Windows native Hermes 8642 already healthy'
        return
    }

    $owner = Get-PortOwner -Port 8642
    if ($healthOk -and -not $modelsOk) {
        Write-Log 'G01_WARN 8642 health is OK but /v1/models is not Windows Hermes; treating as stale/conflicting gateway'
    }
    if ($owner -and -not (Stop-KnownHermesPortConflict -Owner $owner)) {
        exit 1
    }

    Start-WindowsHermesGateway
    Write-Log 'G01_PASS Windows native Hermes 8642 ready'
}

function Ensure-Docker {
    Write-Log 'G02_BEGIN Docker Desktop'
    $dockerReady = $false
    if (Test-DockerReady) {
        $dockerReady = $true
    }
    if (-not $dockerReady) {
        if (-not (Test-Path -LiteralPath $DockerDesktopExe)) {
            Write-Log "G02_FAIL Docker Desktop missing: $DockerDesktopExe"
            exit 1
        }
        Write-Log 'G02_START Docker Desktop'
        $script:BackendStartRequested = $true
        Start-Process -FilePath $DockerDesktopExe -WindowStyle Hidden | Out-Null
        $dockerReady = Wait-Until -TimeoutSeconds $DockerTimeoutSeconds -IntervalSeconds 3 -Label 'Docker API ready' -Condition {
            Test-DockerReady
        }
        if (-not $dockerReady) {
            Write-Log 'G02_RECOVER one official Docker Desktop restart'
            $restartOk = Invoke-DockerBounded -ArgumentLine 'desktop restart --timeout 60' -TimeoutSeconds 65
            if ($restartOk) {
                $dockerReady = Wait-Until -TimeoutSeconds 180 -IntervalSeconds 3 -Label 'Docker API after official restart' -Condition { Test-DockerReady }
            }
            if (-not $dockerReady) {
                Write-Log 'G02_FAIL Docker API not ready after bounded official recovery; data preserved'
                exit 1
            }
        }
    } else {
        Write-Log 'G02_PASS Docker API already ready'
    }
}

function Start-DockerDesktopIfNeeded {
    Write-Log 'G02_BEGIN Docker Desktop start request'
    if (Test-DockerReady) {
        Write-Log 'G02_PASS Docker API already ready'
        return
    }
    if (-not (Test-Path -LiteralPath $DockerDesktopExe)) {
        Write-Log "G02_FAIL Docker Desktop missing: $DockerDesktopExe"
        exit 1
    }
    Write-Log 'G02_START Docker Desktop'
    $script:BackendStartRequested = $true
    Start-Process -FilePath $DockerDesktopExe -WindowStyle Hidden | Out-Null
}

function Start-OpenWebUIContainerIfPossible {
    Write-Log 'G03_BEGIN Open WebUI start request'
    if (Test-HttpOk -Uri $OpenWebUIUrl -ExpectedText 'Open WebUI') {
        Write-Log 'G03_PASS Open WebUI already healthy'
        return
    }
    if (-not (Test-DockerReady)) {
        Write-Log 'G03_DEFER Docker API not ready yet; wait stage will start Open WebUI later'
        return
    }

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
    $script:BackendStartRequested = $true
    & docker start $chosen *> $null
    if ($LASTEXITCODE -ne 0) {
        Write-Log "G03_WARN docker start $chosen returned exit code $LASTEXITCODE; wait stage will still check HTTP 3000"
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
        $script:BackendStartRequested = $true
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

function Start-BackendStage {
    Write-Log 'STAGE1_BEGIN backend start'
    Ensure-Hermes
    Start-DockerDesktopIfNeeded
    Start-OpenWebUIContainerIfPossible
    Write-Log 'STAGE1_PASS backend start requested'
}

function Wait-And-OpenStage {
    Write-Log 'STAGE2_BEGIN wait and open page'
    Ensure-Hermes
    Ensure-Docker
    Ensure-OpenWebUI
    Open-Page
    Write-Log 'STAGE2_PASS wait and open finished'
}

Write-Log 'START Windows native Hermes daily launcher'
Write-Log "RunLog: $RunLog"
Write-Log 'Order: stage1 backend start -> staged wait -> stage2 status checks -> browser'
if ($StartBackendOnly) {
    Start-BackendStage
    Write-Log 'FINAL_PASS Windows native Hermes backend start requested'
    exit 0
}
if ($WaitAndOpen) {
    Wait-And-OpenStage
    Write-Log 'FINAL_PASS Windows native Hermes page is ready'
    exit 0
}

Start-BackendStage
$allReady = ((Test-WindowsHermesModels) -and (Test-DockerReady) -and (Test-HttpOk -Uri $OpenWebUIUrl -ExpectedText 'Open WebUI'))
if ($allReady -and -not $script:BackendStartRequested) {
    Write-Log 'STAGE_WAIT_SKIP all services already ready'
} else {
    Write-Log "STAGE_WAIT_BEGIN sleeping ${StageDelaySeconds}s before final checks"
    Start-Sleep -Seconds $StageDelaySeconds
    Write-Log 'STAGE_WAIT_DONE'
}
Wait-And-OpenStage
Write-Log 'FINAL_PASS Windows native Hermes page is ready'