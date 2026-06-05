param(
    [ValidateSet("temp", "default")]
    [string]$Mode = "temp",

    [switch]$ActiveWindow,

    [string]$Region,

    [string]$Path
)

$skillScript = Join-Path $env:USERPROFILE ".codex\skills\screenshot\scripts\take_screenshot.ps1"

if (-not (Test-Path -LiteralPath $skillScript)) {
    throw "Screenshot skill helper not found: $skillScript"
}

$forwardArgs = @{}

if ($Path) {
    $forwardArgs["Path"] = $Path
} else {
    $forwardArgs["Mode"] = $Mode
}

if ($ActiveWindow) {
    $forwardArgs["ActiveWindow"] = $true
}

if ($Region) {
    $forwardArgs["Region"] = $Region
}

& $skillScript @forwardArgs
