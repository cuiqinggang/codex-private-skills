param(
  [string]$Repo = 'C:\Users\A\Documents\Codex\codex-private-skills',
  [string]$Ref = 'codex/first-principles-physical-limit-convergence-v4.4.1',
  [long]$StartTimestamp = 0
)

# REAL VERIFY RUNNER R2
# Read-only. No proxy/system changes. No GPU workload. No live redesign.

$ErrorActionPreference = 'Stop'
if ($StartTimestamp -le 0) {
  $StartTimestamp = [System.Diagnostics.Stopwatch]::GetTimestamp()
}
$delta = [System.Collections.Generic.List[string]]::new()

function Add-Delta([string]$Value) {
  if (-not [string]::IsNullOrWhiteSpace($Value)) {
    [void]$delta.Add($Value)
  }
}

function Get-ElapsedMs {
  $now = [System.Diagnostics.Stopwatch]::GetTimestamp()
  return (($now - $StartTimestamp) * 1000.0 / [System.Diagnostics.Stopwatch]::Frequency)
}

try {
  if (-not (Test-Path -LiteralPath $Repo)) {
    Add-Delta "SHARED_REPO_MISSING=$Repo"
  }

  if ($delta.Count -eq 0) {
    $methodManifestSpec = "origin/" + $Ref + ":skills/first-principles-physical-limit-convergence/manifest.json"
    $foundationVersionSpec = "origin/" + $Ref + ":skills/local-ai-reality-foundation/VERSION"

    $methodManifest = (git -C $Repo show $methodManifestSpec) -join [Environment]::NewLine
    if ($LASTEXITCODE -ne 0) {
      Add-Delta "METHOD_MANIFEST_READ_FAIL"
    }

    $foundationVersion = ((git -C $Repo show $foundationVersionSpec) -join "").Trim()
    if ($LASTEXITCODE -ne 0) {
      Add-Delta "FOUNDATION_VERSION_READ_FAIL"
    }

    if ($methodManifest -notmatch '"version"\s*:\s*"4\.4\.1"') {
      Add-Delta "METHOD_VERSION_NOT_4.4.1"
    }
    if ($methodManifest -notmatch '"skill_id"\s*:\s*"local-ai-reality-foundation"') {
      Add-Delta "FOUNDATION_ROOT_ID_MISSING"
    }
    if ($methodManifest -notmatch '"role"\s*:\s*"REQUIRED_ROOT_NOT_METHOD_STEP"') {
      Add-Delta "FOUNDATION_ROOT_ROLE_MISSING"
    }
    if ($foundationVersion -ne '1.1.0') {
      Add-Delta "FOUNDATION_VERSION_EXPECTED_1.1.0_ACTUAL_$foundationVersion"
    }
  }

  if ($delta.Count -eq 0) {
    $gpuLine = & nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits 2>$null | Select-Object -First 1
    if (-not $gpuLine) {
      Add-Delta "NVIDIA_SMI_NO_RESULT"
    } else {
      $parts = $gpuLine -split ','
      if ($parts.Count -lt 2) {
        Add-Delta "NVIDIA_SMI_PARSE_FAIL"
      } else {
        $gpuName = $parts[0].Trim()
        $gpuMem = [int](($parts[1] -replace '[^0-9]', '').Trim())
        if ($gpuName -ne 'NVIDIA GeForce RTX 2080 Ti') {
          Add-Delta "GPU_NAME_EXPECTED_RTX2080TI_ACTUAL_$gpuName"
        }
        if ([math]::Abs($gpuMem - 22528) -gt 32) {
          Add-Delta "GPU_MEMORY_EXPECTED_22528_ACTUAL_$gpuMem"
        }
      }
    }
  }

  $paths = @(
    'C:\AI\Playwright-Native-AI-Browser',
    'C:\AI\OpenHands-Canvas',
    'C:\AI\Bonsai2-27B-256K'
  )
  foreach ($p in $paths) {
    if (-not (Test-Path -LiteralPath $p)) {
      Add-Delta "PATH_MISSING=$p"
    }
  }

  $elapsedMs = Get-ElapsedMs

  Write-Host "METHOD=extreme-short-time-engine-v4.4.1"
  Write-Host "RUNNER=REAL-VERIFY-RUNNER-R2"

  if ($delta.Count -gt 0) {
    Write-Host "VALID_REAL=FAIL"
    Write-Host ("T_ATTEMPT_REAL_MS={0:N3}" -f $elapsedMs)
    Write-Host ("REALITY_DELTA=" + ($delta -join ';'))
    Write-Host "FOUNDATION_ABSORB_CHECK=RETURN_TO_VIRTUAL"
    Write-Host "ACTION=STOP"
    Write-Host "RETURN_TO_GPT=YES"
    exit 2
  }

  Write-Host "VALID_REAL=PASS"
  Write-Host ("T_VALID_REAL_MS={0:N3}" -f $elapsedMs)
  Write-Host "REALITY_FOUNDATION=local-ai-reality-foundation@1.1.0"
  Write-Host "FOUNDATION_ROOT=PASS"
  Write-Host "GPU_REALITY=PASS"
  Write-Host "ASSET_PATHS=PASS"
  Write-Host "FOUNDATION_ABSORB_CHECK=PASS"
  Write-Host "ABSORB=NO"
  Write-Host "VERSION_CHANGE=NO"
  Write-Host "REALITY_DELTA=NONE"
  Write-Host "ACTION=STOP"
  Write-Host "RETURN_TO_GPT=NO"
}
catch {
  $elapsedMs = Get-ElapsedMs
  Write-Host "METHOD=extreme-short-time-engine-v4.4.1"
  Write-Host "RUNNER=REAL-VERIFY-RUNNER-R2"
  Write-Host "VALID_REAL=FAIL"
  Write-Host ("T_ATTEMPT_REAL_MS={0:N3}" -f $elapsedMs)
  Write-Host ("REALITY_DELTA=UNEXPECTED_ERROR:" + $_.Exception.Message)
  Write-Host "FOUNDATION_ABSORB_CHECK=RETURN_TO_VIRTUAL"
  Write-Host "ACTION=STOP"
  Write-Host "RETURN_TO_GPT=YES"
  exit 3
}
