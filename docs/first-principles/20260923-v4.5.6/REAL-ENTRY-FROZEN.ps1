# EXTREME SHORT TIME ENGINE v4.5.6 - REAL
# ASCII-only. Read-only. No proxy/system change. No live redesign.

$ErrorActionPreference = 'Stop'
$start = [System.Diagnostics.Stopwatch]::GetTimestamp()
$delta = [System.Collections.Generic.List[string]]::new()

function Add-Delta([string]$Value) {
  if (-not [string]::IsNullOrWhiteSpace($Value)) {
    [void]$delta.Add($Value)
  }
}

function Get-ElapsedMs {
  $now = [System.Diagnostics.Stopwatch]::GetTimestamp()
  return (($now - $start) * 1000.0 / [System.Diagnostics.Stopwatch]::Frequency)
}

try {
  if ($PSVersionTable.PSVersion.Major -lt 7) {
    Add-Delta ("POWERSHELL_MAJOR_EXPECTED_GE_7_ACTUAL_" + $PSVersionTable.PSVersion.Major)
  }

  $gpuLine = & nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits 2>$null | Select-Object -First 1
  if (-not $gpuLine) {
    Add-Delta 'NVIDIA_SMI_NO_RESULT'
  }
  else {
    $parts = $gpuLine -split ','
    if ($parts.Count -lt 2) {
      Add-Delta 'NVIDIA_SMI_PARSE_FAIL'
    }
    else {
      $gpuName = $parts[0].Trim()
      $gpuMem = [int](($parts[1] -replace '[^0-9]', '').Trim())
      if ($gpuName -ne 'NVIDIA GeForce RTX 2080 Ti') {
        Add-Delta ("GPU_NAME_EXPECTED_RTX2080TI_ACTUAL_" + $gpuName)
      }
      if ([math]::Abs($gpuMem - 22528) -gt 32) {
        Add-Delta ("GPU_MEMORY_EXPECTED_22528_ACTUAL_" + $gpuMem)
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
      Add-Delta ("PATH_MISSING=" + $p)
    }
  }

  $elapsedMs = Get-ElapsedMs

  Write-Host 'METHOD=extreme-short-time-engine-v4.5.6'
  Write-Host 'PHASE=REAL'
  Write-Host 'RUNNER=REAL-ENTRY-FROZEN-v4.5.6'
  Write-Host 'REALITY_FOUNDATION=local-ai-reality-foundation@1.1.0'
  Write-Host 'FOUNDATION_ROLE=REQUIRED_ROOT_NOT_METHOD_STEP'

  if ($delta.Count -gt 0) {
    Write-Host 'VALID_REAL=FAIL'
    Write-Host ("T_REAL_LOCAL_DIAGNOSTIC_MS={0:N3}" -f $elapsedMs)
    Write-Host ("REALITY_DELTA=" + ($delta -join ';'))
    Write-Host 'ACTION=STOP'
    Write-Host 'RETURN_TO_VIRTUAL=YES'
    exit 2
  }

  Write-Host 'VALID_REAL=PASS'
  Write-Host ("T_REAL_LOCAL_DIAGNOSTIC_MS={0:N3}" -f $elapsedMs)
  Write-Host 'FOUNDATION_ROOT=PASS'
  Write-Host 'POWERSHELL_REALITY=PASS'
  Write-Host 'GPU_REALITY=PASS'
  Write-Host 'ASSET_PATHS=PASS'
  Write-Host 'REALITY_DELTA=NONE'
  Write-Host 'ACTION=STOP'
  Write-Host 'RETURN_TO_VIRTUAL=NO'
  exit 0
}
catch {
  $elapsedMs = Get-ElapsedMs
  Write-Host 'METHOD=extreme-short-time-engine-v4.5.6'
  Write-Host 'PHASE=REAL'
  Write-Host 'RUNNER=REAL-ENTRY-FROZEN-v4.5.6'
  Write-Host 'VALID_REAL=FAIL'
  Write-Host ("T_REAL_LOCAL_DIAGNOSTIC_MS={0:N3}" -f $elapsedMs)
  Write-Host ("REALITY_DELTA=UNEXPECTED_ERROR:" + $_.Exception.Message)
  Write-Host 'ACTION=STOP'
  Write-Host 'RETURN_TO_VIRTUAL=YES'
  exit 3
}
