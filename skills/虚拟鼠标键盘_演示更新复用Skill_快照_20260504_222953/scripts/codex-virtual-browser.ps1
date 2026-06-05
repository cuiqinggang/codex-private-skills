param(
    [string]$Url = "about:blank",
    [string]$Session = "codex-virtual",
    [switch]$Headed
)

$argsList = @("--yes", "--package", "@playwright/cli", "playwright-cli", "-s=$Session", "open", $Url)

if ($Headed) {
    $argsList += "--headed"
}

npx @argsList
