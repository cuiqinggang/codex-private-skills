param(
    [string]$Name = "codex-isolated-chrome",
    [switch]$Remove
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw "Docker is not available on PATH."
}

$existing = docker ps -a --filter "name=^/$Name$" --format "{{.Names}}"
if ($existing -ne $Name) {
    Write-Output "Container not found: $Name"
    exit 0
}

$running = docker ps --filter "name=^/$Name$" --format "{{.Names}}"
if ($running -eq $Name) {
    docker stop $Name | Out-Null
    Write-Output "Stopped container: $Name"
}

if ($Remove) {
    docker rm $Name | Out-Null
    Write-Output "Removed container: $Name"
}
