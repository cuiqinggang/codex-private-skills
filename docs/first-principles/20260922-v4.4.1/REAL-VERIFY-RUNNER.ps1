param(
  [string]$Repo = 'C:\Users\A\Documents\Codex\codex-private-skills',
  [string]$Ref = 'codex/first-principles-physical-limit-convergence-v4.4.1'
)

# 【极限短时间引擎 v4.3.0｜v4.4.1完整现实验证｜1｜实】
# 只执行冻结现实验证；禁止现场修复、改方案、改代理或启动 GPU 重任务。

$ErrorActionPreference = 'Stop'
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$delta = [System.Collections.Generic.List[string]]::new()

function Add-Delta([string]$s) {
  if (-not [string]::IsNullOrWhiteSpace($s)) { [void]$delta.Add($s) }
}

try {
  if (-not (Test-Path -LiteralPath $Repo)) {
    Add-Delta "SHARED_REPO_MISSING=$Repo"
  } else {
    git -C $Repo fetch origin ("refs/heads/" + $Ref + ":refs/remotes/origin/" + $Ref) --quiet
    if ($LASTEXITCODE -ne 0) { Add-Delta "GIT_FETCH_FAIL=$Ref" }
  }

  if ($delta.Count -eq 0) {
    $methodSpec = "origin/" + $Ref + ":skills/first-principles-physical-limit-convergence/SKILL.md"
    $foundationSpec = "origin/" + $Ref + ":skills/local-ai-reality-foundation/SKILL.md"
    $versionSpec = "origin/" + $Ref + ":skills/local-ai-reality-foundation/VERSION"

    $method = git -C $Repo show $methodSpec
    $foundation = git -C $Repo show $foundationSpec
    $foundationVersion = (git -C $Repo show $versionSpec).Trim()

    if (($method -join [Environment]::NewLine) -notmatch 'local-ai-reality-foundation') { Add-Delta "METHOD_ROOT_FOUNDATION_MISSING" }
    if (($method -join [Environment]::NewLine) -notmatch '共同的现实根基') { Add-Delta "METHOD_ROOT_RELATION_MISSING" }
    if ($foundationVersion -ne '1.1.0') { Add-Delta "FOUNDATION_VERSION_EXPECTED_1.1.0_ACTUAL_$foundationVersion" }
    if (($foundation -join [Environment]::NewLine) -notmatch '本地 AI 现实底座永久资产 v1\.1\.0') { Add-Delta "FOUNDATION_IDENTITY_MISMATCH" }
  }

  if ($delta.Count -eq 0) {
    $gpuLine = & nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits 2>$null | Select-Object -First 1
    if (-not $gpuLine) {
      Add-Delta "NVIDIA_SMI_NO_RESULT"
    } else {
      $parts = $gpuLine -split ','
      $gpuName = $parts[0].Trim()
      $gpuMem = [int](($parts[1] -replace '[^0-9]','').Trim())
      if ($gpuName -ne 'NVIDIA GeForce RTX 2080 Ti') { Add-Delta "GPU_NAME_EXPECTED_RTX2080TI_ACTUAL_$gpuName" }
      if ([math]::Abs($gpuMem - 22528) -gt 32) { Add-Delta "GPU_MEMORY_EXPECTED_22528_ACTUAL_$gpuMem" }
    }
  }

  $paths = @(
    'C:\AI\Playwright-Native-AI-Browser',
    'C:\AI\OpenHands-Canvas',
    'C:\AI\Bonsai2-27B-256K'
  )
  foreach ($p in $paths) {
    if (-not (Test-Path -LiteralPath $p)) { Add-Delta "PATH_MISSING=$p" }
  }

  $sw.Stop()
  Write-Host "【极限短时间引擎 v4.3.0｜v4.4.1完整现实验证｜1｜实】"

  if ($delta.Count -gt 0) {
    Write-Host "VALID_REAL=FAIL"
    Write-Host ("T_ATTEMPT_REAL_MS={0:N3}" -f $sw.Elapsed.TotalMilliseconds)
    Write-Host ("REALITY_DELTA=" + ($delta -join ';'))
    Write-Host "FOUNDATION_ABSORB_CHECK=RETURN_TO_VIRTUAL"
    Write-Host "ACTION=STOP"
    Write-Host "RETURN_TO_GPT=YES"
    exit 2
  }

  Write-Host "VALID_REAL=PASS"
  Write-Host ("T_VALID_REAL_MS={0:N3}" -f $sw.Elapsed.TotalMilliseconds)
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
  $sw.Stop()
  Write-Host "【极限短时间引擎 v4.3.0｜v4.4.1完整现实验证｜1｜实】"
  Write-Host "VALID_REAL=FAIL"
  Write-Host ("T_ATTEMPT_REAL_MS={0:N3}" -f $sw.Elapsed.TotalMilliseconds)
  Write-Host ("REALITY_DELTA=UNEXPECTED_ERROR:" + $_.Exception.Message)
  Write-Host "FOUNDATION_ABSORB_CHECK=RETURN_TO_VIRTUAL"
  Write-Host "ACTION=STOP"
  Write-Host "RETURN_TO_GPT=YES"
  exit 3
}
