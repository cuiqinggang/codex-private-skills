param(
  [Parameter(Mandatory = $true)]
  [string]$OutputDir,
  [string]$Symptom = "",
  [string[]]$Hosts = @("chatgpt.com", "ab.chatgpt.com", "openai.com", "api.openai.com", "www.google.com", "cloudflare.com"),
  [string[]]$LocalProxyPorts = @("7890", "7891", "7892", "1080", "10808", "10809", "20171", "2080", "8080", "9090")
)

$ErrorActionPreference = "Continue"
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

$Hosts = @(
  foreach ($item in $Hosts) {
    foreach ($part in ($item -split ",")) {
      $trimmed = $part.Trim()
      if ($trimmed) { $trimmed }
    }
  }
) | Select-Object -Unique

$LocalProxyPorts = @(
  foreach ($item in $LocalProxyPorts) {
    foreach ($part in ("$item" -split ",")) {
      $trimmed = $part.Trim()
      if ($trimmed -match "^\d+$") { [int]$trimmed }
    }
  }
) | Select-Object -Unique

function Write-Text($Name, $Value) {
  $path = Join-Path $OutputDir $Name
  $Value | Out-File -LiteralPath $path -Encoding utf8
}

function Add-Line($Name, $Value) {
  $path = Join-Path $OutputDir $Name
  $Value | Add-Content -LiteralPath $path -Encoding utf8
}

function Invoke-Safe($Name, [scriptblock]$Block) {
  try {
    & $Block | Out-File -LiteralPath (Join-Path $OutputDir $Name) -Encoding utf8
  } catch {
    "ERROR: $($_.Exception.Message)" | Out-File -LiteralPath (Join-Path $OutputDir $Name) -Encoding utf8
  }
}

function Test-TcpQuick($HostName, $Port, $TimeoutMs = 5000) {
  $client = New-Object Net.Sockets.TcpClient
  $sw = [Diagnostics.Stopwatch]::StartNew()
  try {
    $iar = $client.BeginConnect($HostName, $Port, $null, $null)
    $ok = $iar.AsyncWaitHandle.WaitOne($TimeoutMs, $false)
    if ($ok -and $client.Connected) {
      $client.EndConnect($iar)
      $sw.Stop()
      return "True`t$($sw.ElapsedMilliseconds)ms"
    }
    $sw.Stop()
    return "False`tTIMEOUT_$($sw.ElapsedMilliseconds)ms"
  } catch {
    $sw.Stop()
    return "ERROR`t$($_.Exception.Message)"
  } finally {
    $client.Close()
  }
}

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
Write-Text "00-readme.txt" @(
  "Proxy/network diagnostic snapshot",
  "Timestamp: $timestamp",
  "Scope: read-only; no proxy/config changes",
  "Symptom: $Symptom"
)

Invoke-Safe "01-ipconfig-all.txt" { ipconfig /all }
Invoke-Safe "02-route-print.txt" { route print }
Invoke-Safe "03-dns-client.txt" { Get-DnsClientServerAddress | Format-List * }
Invoke-Safe "04-winhttp-proxy.txt" { netsh winhttp show proxy }
Invoke-Safe "05-user-internet-proxy.txt" {
  Get-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings" |
    Select-Object ProxyEnable, ProxyServer, ProxyOverride, AutoConfigURL, AutoDetect |
    Format-List
}
Invoke-Safe "06-env-proxy.txt" {
  Get-ChildItem Env: |
    Where-Object { $_.Name -match "proxy|http|https|all_proxy" } |
    Sort-Object Name |
    Format-Table -AutoSize
}
Invoke-Safe "07-related-processes.txt" {
  Get-Process |
    Where-Object { $_.ProcessName -match "paoluz|clash|flclash|v2ray|sing|mihomo|nekoray|hysteria|trojan|xray|chrome|edge|wechat|codex" } |
    Select-Object ProcessName, Id, Path, StartTime -ErrorAction SilentlyContinue |
    Sort-Object ProcessName |
    Format-Table -AutoSize
}
Invoke-Safe "08-netstat-keyports.txt" { netstat -ano }
Invoke-Safe "09-netsh-interfaces.txt" { netsh interface show interface }
Invoke-Safe "10-netsh-ip-config.txt" { netsh interface ip show config }

foreach ($hostName in $Hosts) {
  Invoke-Safe "dns-$hostName-default.txt" { nslookup $hostName }
  Invoke-Safe "dns-$hostName-1.1.1.1.txt" { nslookup $hostName 1.1.1.1 }
  Invoke-Safe "dns-$hostName-8.8.8.8.txt" { nslookup $hostName 8.8.8.8 }
}

foreach ($hostName in $Hosts) {
  Add-Line "tcp-443-socket-tests.txt" "$hostName`t443`t$(Test-TcpQuick $hostName 443 5000)"
}

foreach ($port in $LocalProxyPorts) {
  Add-Line "local-proxy-port-tests.txt" "127.0.0.1`t$port`t$(Test-TcpQuick "127.0.0.1" $port 3000)"
}

$proxyServer = ""
try {
  $settings = Get-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings"
  if ($settings.ProxyEnable -eq 1 -and $settings.ProxyServer) {
    $proxyServer = $settings.ProxyServer
  }
} catch {}

$urls = @(
  "https://chatgpt.com/",
  "https://ab.chatgpt.com/",
  "https://api.openai.com/",
  "https://www.google.com/generate_204",
  "https://cloudflare.com/cdn-cgi/trace"
)

foreach ($url in $urls) {
  Add-Line "curl-direct-vs-proxy.txt" "## DIRECT $url"
  curl.exe -I --max-time 12 --noproxy "*" $url 2>&1 | Add-Content -LiteralPath (Join-Path $OutputDir "curl-direct-vs-proxy.txt") -Encoding utf8
  if ($proxyServer) {
    $proxyUrl = if ($proxyServer -match "^\w+://") { $proxyServer } else { "http://$proxyServer" }
    Add-Line "curl-direct-vs-proxy.txt" "## PROXY $proxyUrl $url"
    curl.exe -I --max-time 12 --proxy $proxyUrl $url 2>&1 | Add-Content -LiteralPath (Join-Path $OutputDir "curl-direct-vs-proxy.txt") -Encoding utf8
  }
}

if ($proxyServer) {
  $proxyUrl = if ($proxyServer -match "^\w+://") { $proxyServer } else { "http://$proxyServer" }
  Add-Line "client-like-openai-checks.txt" "## ChatGPT browser-like HEAD"
  $chatgptClientCheck = curl.exe -I -L --max-time 15 --proxy $proxyUrl -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125 Safari/537.36" "https://chatgpt.com/" 2>&1 |
    Select-Object -First 60
  $chatgptClientCheck | Add-Content -LiteralPath (Join-Path $OutputDir "client-like-openai-checks.txt") -Encoding utf8
  Add-Line "client-like-openai-checks.txt" "## OpenAI API unauthenticated /v1/models"
  $apiClientCheck = curl.exe -i --max-time 15 --proxy $proxyUrl "https://api.openai.com/v1/models" 2>&1 |
    Select-Object -First 60
  $apiClientCheck | Add-Content -LiteralPath (Join-Path $OutputDir "client-like-openai-checks.txt") -Encoding utf8
}

$localProxyText = ""
$curlText = ""
$clientText = ""
if (Test-Path (Join-Path $OutputDir "local-proxy-port-tests.txt")) {
  $localProxyText = Get-Content -LiteralPath (Join-Path $OutputDir "local-proxy-port-tests.txt") -Raw
}
if (Test-Path (Join-Path $OutputDir "curl-direct-vs-proxy.txt")) {
  $curlText = Get-Content -LiteralPath (Join-Path $OutputDir "curl-direct-vs-proxy.txt") -Raw
}
if (Test-Path (Join-Path $OutputDir "client-like-openai-checks.txt")) {
  $clientText = Get-Content -LiteralPath (Join-Path $OutputDir "client-like-openai-checks.txt") -Raw
}

$proxyPortHealthy = $localProxyText -match "127\.0\.0\.1\s+7890\s+True"
$chatgptHealthy = $clientText -match "HTTP/1\.1 200 OK"
$apiHealthy = $clientText -match "HTTP/1\.1 401 Unauthorized" -and $clientText -match "Missing bearer authentication"
$bareCurlHasExpectedNoise = $curlText -match "HTTP/1\.1 403 Forbidden" -or $curlText -match "HTTP/1\.1 421 Misdirected Request"

$verdict = @()
$verdict += "# Proxy Health Verdict"
$verdict += ""
$verdict += "Time: $timestamp"
$verdict += "Symptom: $Symptom"
$verdict += ""
if ($proxyPortHealthy -and $chatgptHealthy -and $apiHealthy) {
  $verdict += "Overall: HEALTHY for ChatGPT/OpenAI-style client traffic."
} elseif ($proxyPortHealthy -and ($chatgptHealthy -or $apiHealthy)) {
  $verdict += "Overall: PARTIAL/DEGRADED. The local proxy is alive and at least one OpenAI-family client check works."
} elseif (-not $proxyPortHealthy) {
  $verdict += "Overall: FAULT. The expected local proxy listener 127.0.0.1:7890 is not healthy."
} else {
  $verdict += "Overall: FAULT or UNKNOWN. Client-like OpenAI checks did not prove healthy reachability."
}
$verdict += ""
$verdict += "Signals:"
$verdict += "- Local proxy 127.0.0.1:7890 healthy: $proxyPortHealthy"
$verdict += "- Browser-like ChatGPT check returned 200 OK: $chatgptHealthy"
$verdict += "- OpenAI API /v1/models returned expected unauthenticated 401: $apiHealthy"
$verdict += "- Bare curl HEAD returned 403/421 noise: $bareCurlHasExpectedNoise"
$verdict += ""
$verdict += "Interpretation:"
if ($bareCurlHasExpectedNoise -and $chatgptHealthy -and $apiHealthy) {
  $verdict += "- Bare curl HEAD 403/421 is NOT a fault in this state. Treat it as an expected low-level probe artifact because browser-like ChatGPT and API endpoint checks are healthy."
} elseif ($bareCurlHasExpectedNoise) {
  $verdict += "- Bare curl HEAD 403/421 is a weak signal. Confirm with client-like checks before calling the network broken."
} else {
  $verdict += "- Bare curl did not show the known 403/421 noise in this run."
}
$verdict += "- Use this file as the first recovery verdict, then inspect detailed logs only if the verdict is not healthy."
$verdict | Out-File -LiteralPath (Join-Path $OutputDir "health-verdict.md") -Encoding utf8

$summary = @()
$summary += "# Proxy Diagnostic Summary"
$summary += ""
$summary += "Time: $timestamp"
$summary += "Symptom: $Symptom"
$summary += ""
$summary += "## Quick Reads"
$summary += ""
$summary += "- User proxy: see 05-user-internet-proxy.txt"
$summary += "- WinHTTP proxy: see 04-winhttp-proxy.txt"
$summary += "- Local proxy ports: see local-proxy-port-tests.txt"
$summary += "- DNS results: see dns-*.txt"
$summary += "- Direct/proxy HTTP comparison: see curl-direct-vs-proxy.txt"
$summary += "- Client-like OpenAI checks: see client-like-openai-checks.txt"
$summary += "- Health verdict: see health-verdict.md"
$summary += ""
$summary += "## Initial Interpretation Checklist"
$summary += ""
$summary += "- If user proxy points to 127.0.0.1 and that port is True, the local proxy listener is alive."
$summary += "- Do not call bare curl 403/421 a fault if health-verdict.md says browser-like ChatGPT and API checks are healthy."
$summary += "- If client-like ChatGPT/OpenAI checks return 403/421/timeouts, suspect node/export/DNS/rule mode."
$summary += "- For ChatGPT, browser-like checks are stronger than bare curl HEAD because bare requests can be blocked while real browser traffic works."
$summary += "- If DNS for ChatGPT/OpenAI contains unrelated or suspicious IPs, suspect DNS pollution/interception or DNS leakage."
$summary += "- Do not change WinHTTP just because it is direct unless the failing client uses WinHTTP."
$summary | Out-File -LiteralPath (Join-Path $OutputDir "summary.md") -Encoding utf8

Get-ChildItem -LiteralPath $OutputDir | Select-Object Name, Length | Format-Table -AutoSize
