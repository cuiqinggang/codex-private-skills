param(
    [string]$WebDriverUrl = "http://127.0.0.1:4444",
    [string]$OutputDir = "output/isolated-browser"
)

$ErrorActionPreference = "Stop"

function Invoke-WebDriver {
    param(
        [string]$Method,
        [string]$Path,
        [object]$Body = $null
    )

    $uri = "$WebDriverUrl$Path"
    if ($null -eq $Body) {
        return Invoke-RestMethod -Method $Method -Uri $uri -TimeoutSec 20
    }

    $json = $Body | ConvertTo-Json -Depth 20 -Compress
    return Invoke-RestMethod -Method $Method -Uri $uri -Body $json -ContentType "application/json" -TimeoutSec 20
}

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

$status = Invoke-WebDriver -Method Get -Path "/status"
if ($status.value.ready -ne $true) {
    throw "Selenium WebDriver is not ready."
}

$session = Invoke-WebDriver -Method Post -Path "/session" -Body @{
    capabilities = @{
        alwaysMatch = @{
            browserName = "chrome"
            "goog:chromeOptions" = @{
                args = @("--no-sandbox", "--disable-dev-shm-usage")
            }
        }
    }
}

$sessionId = $session.value.sessionId
if (-not $sessionId) {
    throw "Could not create WebDriver session."
}

try {
    $html = @"
<!doctype html>
<html>
<head><meta charset="utf-8"><title>Codex isolated browser test</title></head>
<body style="font-family: Arial, sans-serif; padding: 40px;">
  <h1>Codex isolated browser test</h1>
  <input id="name" aria-label="test input" style="font-size: 20px; padding: 8px;" />
  <button id="apply" style="font-size: 20px; padding: 8px 12px;">Apply</button>
  <p id="result" style="font-size: 22px;">waiting</p>
  <script>
    document.getElementById('apply').addEventListener('click', () => {
      document.getElementById('result').textContent =
        'container browser OK: ' + document.getElementById('name').value;
    });
  </script>
</body>
</html>
"@

    $encoded = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($html))
    Invoke-WebDriver -Method Post -Path "/session/$sessionId/url" -Body @{ url = "data:text/html;base64,$encoded" } | Out-Null

    $inputElement = Invoke-WebDriver -Method Post -Path "/session/$sessionId/element" -Body @{
        using = "css selector"
        value = "#name"
    }
    $inputId = $inputElement.value.'element-6066-11e4-a52e-4f735466cecf'
    Invoke-WebDriver -Method Post -Path "/session/$sessionId/element/$inputId/value" -Body @{
        text = "virtual mouse and keyboard"
        value = @("v","i","r","t","u","a","l"," ","m","o","u","s","e"," ","a","n","d"," ","k","e","y","b","o","a","r","d")
    } | Out-Null

    $buttonElement = Invoke-WebDriver -Method Post -Path "/session/$sessionId/element" -Body @{
        using = "css selector"
        value = "#apply"
    }
    $buttonId = $buttonElement.value.'element-6066-11e4-a52e-4f735466cecf'
    Invoke-WebDriver -Method Post -Path "/session/$sessionId/element/$buttonId/click" -Body @{} | Out-Null

    $result = Invoke-WebDriver -Method Post -Path "/session/$sessionId/execute/sync" -Body @{
        script = "return document.getElementById('result').textContent;"
        args = @()
    }

    $screenshot = Invoke-WebDriver -Method Get -Path "/session/$sessionId/screenshot"
    $screenshotPath = Join-Path $OutputDir "isolated-browser-proof.png"
    [IO.File]::WriteAllBytes((Resolve-Path -LiteralPath $OutputDir).Path + "\isolated-browser-proof.png", [Convert]::FromBase64String($screenshot.value))

    [pscustomobject]@{
        ok = ($result.value -eq "container browser OK: virtual mouse and keyboard")
        result = $result.value
        screenshot = (Resolve-Path -LiteralPath $screenshotPath).Path
        webdriver = $WebDriverUrl
        noVnc = "http://127.0.0.1:7900/?autoconnect=1&resize=scale&password=secret"
    } | ConvertTo-Json -Depth 4
} finally {
    Invoke-WebDriver -Method Delete -Path "/session/$sessionId" | Out-Null
}
