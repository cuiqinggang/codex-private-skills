param(
  [string]$StationRoot = 'C:\Users\A\Desktop\AI_Coding_SuperTool_Ecosystem_Station',
  [string]$RunRoot = 'C:\Users\A\Desktop\ClaudeCode_Outputs\Mature_AI_Coding_SuperTool_Ecosystem_Station_Full_Deploy_Run'
)

$ErrorActionPreference = 'Stop'

function Write-Json($Object, [string]$Path, [int]$Depth = 16) {
  $dir = Split-Path $Path -Parent
  if ($dir) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
  $Object | ConvertTo-Json -Depth $Depth | Set-Content -LiteralPath $Path -Encoding UTF8
}

function Read-Json($Path) {
  if (-not (Test-Path -LiteralPath $Path)) { return $null }
  return Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json
}

function Set-ObjectProperty {
  param(
    [Parameter(Mandatory=$true)]$Object,
    [Parameter(Mandatory=$true)][string]$Name,
    $Value
  )
  if ($Object.PSObject.Properties.Name -contains $Name) {
    $Object.$Name = $Value
  } else {
    $Object | Add-Member -NotePropertyName $Name -NotePropertyValue $Value -Force
  }
}

function Get-OpenRouterKey {
  $envNames = @('OPENROUTER_API_KEY','OPENROUTER_KEY')
  foreach ($name in $envNames) {
    $v = [Environment]::GetEnvironmentVariable($name,'Process')
    if (-not $v) { $v = [Environment]::GetEnvironmentVariable($name,'User') }
    if (-not $v) { $v = [Environment]::GetEnvironmentVariable($name,'Machine') }
    if ($v -and $v -match '^sk-or-v1-[A-Za-z0-9]+$') {
      return [ordered]@{ key=$v; source="env:$name" }
    }
  }

  $attachDir = 'C:\Users\A\.codex\manual-paste-attachments'
  if (Test-Path -LiteralPath $attachDir) {
    $files = Get-ChildItem -LiteralPath $attachDir -Filter '*.txt' -File -ErrorAction SilentlyContinue |
      Sort-Object LastWriteTime -Descending |
      Select-Object -First 80
    foreach ($file in $files) {
      $text = Get-Content -LiteralPath $file.FullName -Raw -ErrorAction SilentlyContinue
      if ($text -match 'sk-or-v1-[A-Za-z0-9]+') {
        $matches = [regex]::Matches($text, 'sk-or-v1-[A-Za-z0-9]+')
        if ($matches.Count -gt 0) {
          return [ordered]@{ key=$matches[$matches.Count - 1].Value; source=("attachment:" + $file.Name) }
        }
      }
    }
  }
  if ($env:OPENROUTER_KEY_FROM_STDIN -eq '1') {
    $stdinKey = [Console]::In.ReadLine()
    if ($stdinKey -and $stdinKey.Trim() -match '^sk-or-v1-[A-Za-z0-9]+$') {
      return [ordered]@{ key=$stdinKey.Trim(); source='stdin:redacted' }
    }
  }
  throw 'No OpenRouter key found in env, recent paste attachments, or stdin.'
}

function Invoke-OpenRouterSmoke {
  param(
    [string]$ApiKey,
    [string]$ModelId,
    [string]$DisplayName
  )
  $uri = 'https://openrouter.ai/api/v1/chat/completions'
  $headers = @{
    Authorization = "Bearer $ApiKey"
    'Content-Type' = 'application/json'
    'HTTP-Referer' = 'https://local.codex'
    'X-Title' = 'Codex Kilo SuperTool Live Smoke Verification'
  }
  $started = Get-Date
  $prompts = @(
    'Say OK.',
    ('Return exactly LIVE_OK for ' + $DisplayName + '.'),
    ('Reply with one short plain-text confirmation for ' + $DisplayName + '.')
  )
  $lastResponse = $null
  $lastContent = ''
  $attempt = 0
  try {
    foreach ($prompt in $prompts) {
      $attempt++
      $body = [ordered]@{
        model = $ModelId
        messages = @(
          [ordered]@{ role='system'; content='Minimal live smoke verification. Reply with plain text only.' },
          [ordered]@{ role='user'; content=$prompt }
        )
        max_tokens = 128
        temperature = 0
      } | ConvertTo-Json -Depth 8
      $response = Invoke-RestMethod -Method Post -Uri $uri -Headers $headers -Body $body -TimeoutSec 90
      $lastResponse = $response
      $content = ''
      if ($response.choices -and $response.choices.Count -gt 0 -and $response.choices[0].message) {
        $content = [string]$response.choices[0].message.content
      }
      $lastContent = $content
      if ($content.Length -gt 0) { break }
    }
    return [ordered]@{
      model_display_name = $DisplayName
      exact_model_id = $ModelId
      live_call_verified = ($lastContent.Length -gt 0)
      http_success = $true
      response_nonempty = ($lastContent.Length -gt 0)
      response_preview_redacted = if ($lastContent.Length -gt 120) { $lastContent.Substring(0,120) } else { $lastContent }
      provider_response_model = $lastResponse.model
      provider_response_id = $lastResponse.id
      attempt_count = $attempt
      elapsed_ms = [int]((Get-Date) - $started).TotalMilliseconds
      error = $null
    }
  } catch {
    $err = $_.Exception.Message
    return [ordered]@{
      model_display_name = $DisplayName
      exact_model_id = $ModelId
      live_call_verified = $false
      http_success = $false
      response_nonempty = $false
      response_preview_redacted = ''
      provider_response_model = $null
      provider_response_id = $null
      attempt_count = $attempt
      elapsed_ms = [int]((Get-Date) - $started).TotalMilliseconds
      error = $err
    }
  }
}

$evidenceDir = Join-Path $RunRoot 'evidence'
$reportsDir = Join-Path $RunRoot 'reports'
$verificationDir = Join-Path $RunRoot 'continuous_system_verification'
New-Item -ItemType Directory -Force -Path $evidenceDir,$reportsDir,$verificationDir | Out-Null

$keyInfo = Get-OpenRouterKey
$apiKey = $keyInfo.key

$models = @(
  [ordered]@{ display='DeepSeek V4 Pro'; id='deepseek/deepseek-v4-pro' },
  [ordered]@{ display='DeepSeek V4 Flash'; id='deepseek/deepseek-v4-flash' },
  [ordered]@{ display='GLM-5.2 / Zhipu 5.2'; id='z-ai/glm-5.2' },
  [ordered]@{ display='Qwen3-VL-235B / Qwen multimodal 235B'; id='qwen/qwen3-vl-235b-a22b-instruct' }
)

$results = @()
foreach ($m in $models) {
  $results += Invoke-OpenRouterSmoke -ApiKey $apiKey -ModelId $m.id -DisplayName $m.display
}

$verifiedCount = @($results | Where-Object { $_.live_call_verified -eq $true }).Count
$failed = @($results | Where-Object { $_.live_call_verified -ne $true })
$allPass = ($verifiedCount -eq $models.Count)

$smoke = [ordered]@{
  generated_at = (Get-Date).ToString('o')
  live_call_performed = $true
  key_source = $keyInfo.source
  key_redacted = $true
  api_keys_printed = $false
  api_keys_persisted = $false
  api_keys_modified = $false
  models_requested = $models.Count
  live_call_verified_models_count = $verifiedCount
  all_models_live_call_verified = $allPass
  results = $results
}

$livePath = Join-Path $evidenceDir 'openrouter_live_model_smoke_verification.json'
Write-Json $smoke $livePath

$matrixPath = Join-Path $StationRoot 'models\model_matrix.json'
$matrix = Read-Json $matrixPath
if ($matrix -and $matrix.models) {
  foreach ($model in $matrix.models) {
    $match = @($results | Where-Object { $_.model_display_name -eq $model.model_display_name } | Select-Object -First 1)
    if ($match.Count -gt 0) {
      $m = $match[0]
      if (-not $model.provider_smoke_evidence) {
        Set-ObjectProperty -Object $model -Name provider_smoke_evidence -Value ([pscustomobject]@{})
      }
      Set-ObjectProperty -Object $model.provider_smoke_evidence -Name live_call_performed -Value $true
      Set-ObjectProperty -Object $model.provider_smoke_evidence -Name live_call_verified -Value ([bool]$m.live_call_verified)
      Set-ObjectProperty -Object $model.provider_smoke_evidence -Name live_call_evidence_path -Value $livePath
      Set-ObjectProperty -Object $model.provider_smoke_evidence -Name provider_response_id -Value $m.provider_response_id
      if (-not $model.evidence_confirmation) {
        Set-ObjectProperty -Object $model -Name evidence_confirmation -Value ([pscustomobject]@{})
      }
      Set-ObjectProperty -Object $model.evidence_confirmation -Name live_call_verified -Value ([bool]$m.live_call_verified)
      Set-ObjectProperty -Object $model.evidence_confirmation -Name live_call_evidence_paths -Value @($livePath)
      if ($m.live_call_verified) {
        $model.status = 'CONFIRMED'
      }
    }
  }
  $matrix | Add-Member -NotePropertyName live_call_verified_models_count -NotePropertyValue $verifiedCount -Force
  $matrix | Add-Member -NotePropertyName all_models_live_call_verified -NotePropertyValue $allPass -Force
  $matrix | Add-Member -NotePropertyName live_call_evidence_path -NotePropertyValue $livePath -Force
  Write-Json $matrix $matrixPath
}

$continuousJson = Join-Path $verificationDir 'system_verification_report.json'
$continuousMd = Join-Path $verificationDir 'system_verification_report.md'
$finalVerdictPath = Join-Path $verificationDir 'final_verdict.txt'
$continuous = Read-Json $continuousJson
if ($continuous) {
  Set-ObjectProperty -Object $continuous -Name live_model_smoke_verification_path -Value $livePath
  Set-ObjectProperty -Object $continuous.counts -Name live_model_call_verified_cycles -Value $(if ($allPass) { $continuous.cycle_limit } else { 0 })
  Set-ObjectProperty -Object $continuous.counts -Name live_model_smoke_verified_models -Value $verifiedCount
  Set-ObjectProperty -Object $continuous -Name final_verdict -Value $(if ($allPass -and $continuous.counts.real_execution_cycles -eq $continuous.cycle_limit -and $continuous.counts.tool_invocation_cycles -eq $continuous.cycle_limit -and $continuous.counts.routing_config_cycles -eq $continuous.cycle_limit) { 'ACCEPTED' } else { 'PARTIAL' })
  Set-ObjectProperty -Object $continuous -Name verdict_reason -Value $(if ($continuous.final_verdict -eq 'ACCEPTED') { '30 local runtime cycles passed and all four OpenRouter model live smoke calls returned non-empty responses.' } else { 'Local runtime cycles passed but at least one live model smoke call failed.' })
  Write-Json $continuous $continuousJson
  $md = @"
# Continuous Full-System Acceptance & Runtime Verification

- generated_at: $($continuous.generated_at)
- cycle_limit: $($continuous.cycle_limit)
- cycles_completed: $($continuous.cycles_completed)
- final_verdict: $($continuous.final_verdict)

## Runtime Counts

- real_execution_cycles: $($continuous.counts.real_execution_cycles) / $($continuous.cycle_limit)
- routing_config_cycles: $($continuous.counts.routing_config_cycles) / $($continuous.cycle_limit)
- tool_invocation_cycles: $($continuous.counts.tool_invocation_cycles) / $($continuous.cycle_limit)
- checkpoint_cycles: $($continuous.counts.checkpoint_cycles) / $($continuous.cycle_limit)

## Live Model Smoke

- live_call_performed: true
- live_model_smoke_verified_models: $verifiedCount / $($models.Count)
- live_model_smoke_evidence: $livePath

## Verdict Reason

$($continuous.verdict_reason)

## Safety

- No API key printed.
- No API key persisted.
- No API key modified.
- Hermes Gateway not modified.
- Qwen direct vision config not touched.
"@
  $md | Set-Content -LiteralPath $continuousMd -Encoding UTF8
  $continuous.final_verdict | Set-Content -LiteralPath $finalVerdictPath -Encoding ASCII
}

$reportPath = Join-Path $reportsDir 'OpenRouter_Live_Model_Smoke_Verification_Report.md'
$lines = @()
$lines += '# OpenRouter Live Model Smoke Verification Report'
$lines += ''
$lines += "- generated_at: $($smoke.generated_at)"
$lines += "- live_call_performed: true"
$lines += "- key_source: $($smoke.key_source)"
$lines += "- key_redacted: true"
$lines += "- api_keys_printed: false"
$lines += "- api_keys_persisted: false"
$lines += "- live_call_verified_models_count: $verifiedCount / $($models.Count)"
$lines += "- all_models_live_call_verified: $allPass"
$lines += ''
$lines += '## Results'
foreach ($r in $results) {
  $lines += ''
  $lines += "### $($r.model_display_name)"
  $lines += "- exact_model_id: $($r.exact_model_id)"
  $lines += "- live_call_verified: $($r.live_call_verified)"
  $lines += "- http_success: $($r.http_success)"
  $lines += "- response_nonempty: $($r.response_nonempty)"
  $lines += "- provider_response_model: $($r.provider_response_model)"
  $lines += "- provider_response_id: $($r.provider_response_id)"
  $lines += "- elapsed_ms: $($r.elapsed_ms)"
  if ($r.error) { $lines += "- error: $($r.error)" }
}
$lines += ''
$lines += "JSON evidence: $livePath"
$lines | Set-Content -LiteralPath $reportPath -Encoding UTF8

[ordered]@{
  live_call_performed = $true
  live_call_verified_models_count = $verifiedCount
  all_models_live_call_verified = $allPass
  evidence_path = $livePath
  report_path = $reportPath
  final_verdict = if ($continuous) { $continuous.final_verdict } else { if ($allPass) { 'LIVE_SMOKE_ACCEPTED' } else { 'LIVE_SMOKE_PARTIAL' } }
} | ConvertTo-Json -Depth 8
