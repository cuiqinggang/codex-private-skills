# G01：启动调试版 Chrome，并登录 GPT Plus
# 从 WSL 通过 /init 桥接执行

$ErrorActionPreference = 'Stop'

$chromeCandidates = @(
  "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
  "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
  "$env:LocalAppData\Google\Chrome\Application\chrome.exe"
)

$chrome = $chromeCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1

if (-not $chrome) {
  Write-Host "G01_FAIL_CHROME_NOT_FOUND"
  return
}

$profile = Join-Path $env:USERPROFILE "Desktop\Hermes_CDP_Chrome_Profile"
New-Item -ItemType Directory -Force -Path $profile | Out-Null

Start-Process -FilePath $chrome -ArgumentList @(
  "--remote-debugging-address=127.0.0.1",
  "--remote-debugging-port=9333",
  "--user-data-dir=$profile",
  "--no-first-run",
  "--new-window",
  "https://chatgpt.com/"
)

Start-Sleep -Seconds 3

try {
  $r = Invoke-RestMethod "http://127.0.0.1:9333/json/version"
  Write-Host "G01_PASS"
  Write-Host "BROWSER=$($r.Browser)"
  Write-Host "WIN_WS=$($r.webSocketDebuggerUrl)"
  Write-Host "PROFILE=$profile"
}
catch {
  Write-Host "G01_FAIL_9333_NOT_READY"
  Write-Host $_.Exception.Message
}
