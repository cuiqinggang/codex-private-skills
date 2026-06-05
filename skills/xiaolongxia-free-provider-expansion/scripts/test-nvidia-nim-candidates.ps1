param(
  [string]$OutputDir = "C:\Users\A\Desktop\1\output\XIAOLONGXIA-NVIDIA-NIM-RETEST",
  [string]$SecretFile = "C:\Users\A\xiaolongxia-free-api-local\secrets\nvidia_api_key.txt",
  [int]$DelaySeconds = 3
)

$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

$key = $env:NVIDIA_API_KEY
if ([string]::IsNullOrWhiteSpace($key) -and (Test-Path -LiteralPath $SecretFile)) {
  $key = (Get-Content -LiteralPath $SecretFile -Raw).Trim()
}
if ([string]::IsNullOrWhiteSpace($key)) {
  throw "NVIDIA_API_KEY is required. Set it in the current process or provide the local secret file. Do not write a global environment variable."
}

$tests = @(
  @{ requested_model = "meta/llama-3.1-8b-instruct"; marker = "NVIDIA_LLAMA31_8B_OK"; class_hint = "A" },
  @{ requested_model = "nvidia/nemotron-3-super-120b-a12b"; marker = "NVIDIA_NEMOTRON_SUPER_OK"; class_hint = "A" },
  @{ requested_model = "meta/llama-3.1-70b-instruct"; marker = "NVIDIA_LLAMA31_70B_OK"; class_hint = "A" },
  @{ requested_model = "moonshotai/kimi-k2.5"; marker = "NVIDIA_KIMI_K25_OK"; class_hint = "C_previous_404" },
  @{ requested_model = "minimaxai/minimax-m2.5"; marker = "NVIDIA_MINIMAX_M25_OK"; class_hint = "C_previous_410" },
  @{ requested_model = "z-ai/glm5"; marker = "NVIDIA_GLM5_OK"; class_hint = "C_previous_410" }
)

$headers = @{
  Authorization = "Bearer $key"
  "Content-Type" = "application/json"
  Accept = "application/json"
}

$results = @()
foreach ($t in $tests) {
  $body = @{
    model = $t.requested_model
    messages = @(@{ role = "user"; content = "Return exactly this marker and nothing else: $($t.marker)" })
    temperature = 0
    max_tokens = 120
    stream = $false
  } | ConvertTo-Json -Depth 6

  $timestamp = (Get-Date).ToString("o")
  $sw = [System.Diagnostics.Stopwatch]::StartNew()
  $status = $null
  $success = $false
  $returned = ""
  $content = ""
  $errType = "none"
  $errSummary = ""

  try {
    $resp = Invoke-WebRequest -Method Post -Uri "https://integrate.api.nvidia.com/v1/chat/completions" -Headers $headers -Body $body -UseBasicParsing -TimeoutSec 90
    $status = [int]$resp.StatusCode
    $json = $resp.Content | ConvertFrom-Json
    $returned = [string]$json.model
    if ([string]::IsNullOrWhiteSpace($returned)) { $returned = $t.requested_model }
    $content = [string]$json.choices[0].message.content
    $success = $true
  } catch {
    if ($_.Exception.Response) { $status = [int]$_.Exception.Response.StatusCode }
    $errType = $_.Exception.GetType().Name
    $errSummary = $_.Exception.Message
    if ($_.ErrorDetails -and $_.ErrorDetails.Message) { $errSummary = $_.ErrorDetails.Message }
  } finally {
    $sw.Stop()
  }

  $contains = $content -match [regex]::Escape($t.marker)
  if ($success -and -not $contains) {
    $errType = "marker_mismatch"
    $errSummary = $content
  }
  $errSummary = ($errSummary -replace "nvapi-[A-Za-z0-9_-]+", "nvapi-***")

  $results += [pscustomobject]@{
    provider = "nvidia"
    requested_model = $t.requested_model
    returned_model = $returned
    marker = $t.marker
    http_status = $status
    success = $success
    response_contains_marker = $contains
    latency_ms = $sw.ElapsedMilliseconds
    error_type = $errType
    error_summary = $errSummary
    timestamp = $timestamp
    class_hint = $t.class_hint
    candidate_a_class = ($success -and $contains -and $sw.ElapsedMilliseconds -lt 60000)
  }

  Start-Sleep -Seconds $DelaySeconds
}

$jsonPath = Join-Path $OutputDir "nvidia-nim-candidate-retest.json"
$mdPath = Join-Path $OutputDir "nvidia-nim-candidate-retest.md"
$results | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $jsonPath -Encoding UTF8

$md = @()
$md += "# NVIDIA NIM Candidate Retest"
$md += ""
$md += "| Model | HTTP | Success | Marker | Latency ms | Error | A candidate |"
$md += "| --- | ---: | --- | --- | ---: | --- | --- |"
foreach ($r in $results) {
  $md += "| `$($r.requested_model)` | $($r.http_status) | $($r.success) | $($r.response_contains_marker) | $($r.latency_ms) | `$($r.error_type)` | $($r.candidate_a_class) |"
}
$md | Set-Content -LiteralPath $mdPath -Encoding UTF8

[pscustomobject]@{
  Json = $jsonPath
  Markdown = $mdPath
  Passed = @($results | Where-Object { $_.response_contains_marker }).Count
}
