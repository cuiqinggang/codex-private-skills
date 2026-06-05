param(
    [string]$Version = "2.92.0",
    [string]$Proxy = ""
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

$base = Join-Path $env:LOCALAPPDATA "Programs\GitHub CLI"
$versionDir = Join-Path $base $Version
$zip = Join-Path $env:TEMP "gh_$Version`_windows_amd64.zip"
$url = "https://github.com/cli/cli/releases/download/v$Version/gh_$Version`_windows_amd64.zip"

New-Item -ItemType Directory -Force -Path $versionDir | Out-Null

$webArgs = @{
    Uri = $url
    OutFile = $zip
}
if ($Proxy) {
    $webArgs.Proxy = $Proxy
}

Invoke-WebRequest @webArgs
Expand-Archive -LiteralPath $zip -DestinationPath $versionDir -Force

$ghExe = Get-ChildItem -Path $versionDir -Recurse -Filter gh.exe | Select-Object -First 1
if (-not $ghExe) {
    throw "gh.exe was not found after extracting $zip"
}

$ghBin = Split-Path -Parent $ghExe.FullName
$currentUserPath = [Environment]::GetEnvironmentVariable("Path", "User")
$parts = @()
if ($currentUserPath) {
    $parts = $currentUserPath -split ";" | Where-Object { $_ }
}

if ($parts -notcontains $ghBin) {
    $newUserPath = (($parts + $ghBin) -join ";")
    [Environment]::SetEnvironmentVariable("Path", $newUserPath, "User")
}

if (($env:Path -split ";") -notcontains $ghBin) {
    $env:Path = $env:Path + ";" + $ghBin
}

& $ghExe.FullName --version
Write-Host "Installed gh.exe at: $($ghExe.FullName)"
Write-Host "Added to user PATH: $ghBin"
