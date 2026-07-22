param(
    [string]$Name = "codex-isolated-chrome",
    [string]$Image = "selenium/standalone-chrome:latest",
    [int]$WebDriverPort = 4444,
    [int]$NoVncPort = 7900
)

$ErrorActionPreference = "Stop"

function Test-PortFree {
    param([int]$Port)
    $listener = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    return -not $listener
}

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw "Docker is not available on PATH."
}

$existing = docker ps -a --filter "name=^/$Name$" --format "{{.Names}}"
if ($existing -eq $Name) {
    $running = docker ps --filter "name=^/$Name$" --format "{{.Names}}"
    if ($running -eq $Name) {
        Write-Output "Container already running: $Name"
        Write-Output "WebDriver: http://127.0.0.1:$WebDriverPort"
${REDACTED_SECRET}
        exit 0
    }

    docker start $Name | Out-Null
    Write-Output "Started existing container: $Name"
} else {
    if (-not (Test-PortFree -Port $WebDriverPort)) {
        throw "Port $WebDriverPort is already in use."
    }
    if (-not (Test-PortFree -Port $NoVncPort)) {
        throw "Port $NoVncPort is already in use."
    }

    docker run -d `
        --name $Name `
        --shm-size="2g" `
        -p "127.0.0.1:${WebDriverPort}:4444" `
        -p "127.0.0.1:${NoVncPort}:7900" `
        $Image | Out-Null
    Write-Output "Created and started container: $Name"
}

$deadline = (Get-Date).AddSeconds(60)
do {
    Start-Sleep -Seconds 2
    try {
        $status = Invoke-RestMethod -Uri "http://127.0.0.1:$WebDriverPort/status" -Method Get -TimeoutSec 3
        if ($status.value.ready -eq $true) {
            Write-Output "WebDriver is ready: http://127.0.0.1:$WebDriverPort"
${REDACTED_SECRET}
            exit 0
        }
    } catch {
        # Keep waiting until the deadline.
    }
} while ((Get-Date) -lt $deadline)

docker logs --tail 80 $Name
throw "Timed out waiting for Selenium WebDriver to become ready."
