param(
    [string]$ExpectedUser = "",
    [string]$Proxy = ""
)

$ErrorActionPreference = "Continue"

$defaultGhBin = Join-Path $env:LOCALAPPDATA "Programs\GitHub CLI\2.92.0\bin"
if (Test-Path -LiteralPath $defaultGhBin) {
    if (($env:Path -split ";") -notcontains $defaultGhBin) {
        $env:Path = $env:Path + ";" + $defaultGhBin
    }
}

if ($Proxy) {
    $env:HTTP_PROXY = $Proxy
    $env:HTTPS_PROXY = $Proxy
}

Write-Host "== gh command =="
Get-Command gh -All -ErrorAction SilentlyContinue | Format-List Source,Version,CommandType

Write-Host "== gh version =="
gh --version 2>&1

Write-Host "== auth status =="
gh auth status 2>&1

if ($ExpectedUser) {
    Write-Host "== repo list =="
    gh repo list $ExpectedUser --limit 5 2>&1
}

Write-Host "== git credential setup =="
gh auth setup-git 2>&1
