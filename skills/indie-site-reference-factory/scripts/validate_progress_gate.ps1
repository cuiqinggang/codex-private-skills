param(
  [Parameter(Mandatory=$true)]
  [string]$WorkRoot
)

$ErrorActionPreference = "Stop"

$required = @(
  "outputs\progress\00_TARGET_BASELINE.md",
  "outputs\progress\01_GEOMETRY_SPEC.md",
  "outputs\progress\02_COMPONENT_SPECS_INDEX.md",
  "outputs\progress\03_BUILD_PLAN.md",
  "outputs\progress\FINAL_SIMILARITY_GATE.md",
  "outputs\progress\stage-gates\G00_TARGET_CAPTURE.md",
  "outputs\progress\stage-gates\G01_GEOMETRY_SPEC.md",
  "outputs\progress\stage-gates\G02_COMPONENT_SPECS.md",
  "outputs\progress\stage-gates\G03_BUILD_PLAN.md",
  "outputs\progress\stage-gates\G10_NAVBAR.md",
  "outputs\progress\stage-gates\G20_HERO_TEXT.md",
  "outputs\progress\stage-gates\G30_PRIMARY_VISUAL.md",
  "outputs\progress\stage-gates\G40_CTA_SCROLL.md",
  "outputs\progress\stage-gates\G50_FIRST_SECTION.md",
  "outputs\progress\stage-gates\G60_MOBILE.md",
  "evidence\screenshots\target_desktop.png",
  "evidence\screenshots\target_mobile.png",
  "evidence\screenshots\generated_desktop.png",
  "evidence\screenshots\generated_mobile.png"
)

$missing = @()
$invalid = @()

foreach ($rel in $required) {
  $path = Join-Path $WorkRoot $rel
  if (-not (Test-Path -LiteralPath $path)) {
    $missing += $rel
  }
}

$rounds = @()
$progressDir = Join-Path $WorkRoot "outputs\progress"
if (Test-Path -LiteralPath $progressDir) {
  $rounds = Get-ChildItem -LiteralPath $progressDir -Filter "ROUND_*_COMPARE.md" -ErrorAction SilentlyContinue
}

if ($rounds.Count -lt 1) {
  $missing += "outputs\progress\ROUND_N_COMPARE.md"
}

if ($missing.Count -gt 0) {
  Write-Host "PROGRESS_GATE=INVALID_TEST"
  Write-Host "Missing:"
  $missing | ForEach-Object { Write-Host "- $_" }
  exit 2
}

function Test-PngFile {
  param([Parameter(Mandatory=$true)][string]$Path)
  if (-not (Test-Path -LiteralPath $Path)) { return $false }
  $item = Get-Item -LiteralPath $Path
  if ($item.Length -lt 1024) { return $false }
  $fs = [System.IO.File]::OpenRead($Path)
  try {
    $buffer = New-Object byte[] 8
    $read = $fs.Read($buffer, 0, 8)
    if ($read -ne 8) { return $false }
    $signature = @(0x89,0x50,0x4E,0x47,0x0D,0x0A,0x1A,0x0A)
    for ($i = 0; $i -lt 8; $i++) {
      if ($buffer[$i] -ne $signature[$i]) { return $false }
    }
    return $true
  } finally {
    $fs.Close()
  }
}

function Read-Text {
  param([Parameter(Mandatory=$true)][string]$Path)
  return Get-Content -LiteralPath $Path -Encoding UTF8 -Raw
}

function Get-PercentAfterKeyword {
  param(
    [Parameter(Mandatory=$true)][string]$Text,
    [Parameter(Mandatory=$true)][string[]]$Keywords
  )
  foreach ($keyword in $Keywords) {
    $escaped = [regex]::Escape($keyword)
    $match = [regex]::Match($Text, "(?is)$escaped[^0-9]{0,80}([0-9]{1,3})(?:\s*)%")
    if ($match.Success) {
      return [int]$match.Groups[1].Value
    }
  }
  return $null
}

$screenshots = @(
  "evidence\screenshots\target_desktop.png",
  "evidence\screenshots\target_mobile.png",
  "evidence\screenshots\generated_desktop.png",
  "evidence\screenshots\generated_mobile.png"
)

foreach ($rel in $screenshots) {
  $path = Join-Path $WorkRoot $rel
  if (-not (Test-PngFile -Path $path)) {
    $invalid += "invalid_or_fake_png:$rel"
  }
}

$baselinePath = Join-Path $WorkRoot "outputs\progress\00_TARGET_BASELINE.md"
$baseline = Read-Text -Path $baselinePath
if ($baseline -notmatch "https?://") {
  $invalid += "missing_real_url:outputs\progress\00_TARGET_BASELINE.md"
}

$stageGates = @(
  "G00_TARGET_CAPTURE",
  "G01_GEOMETRY_SPEC",
  "G02_COMPONENT_SPECS",
  "G03_BUILD_PLAN",
  "G10_NAVBAR",
  "G20_HERO_TEXT",
  "G30_PRIMARY_VISUAL",
  "G40_CTA_SCROLL",
  "G50_FIRST_SECTION",
  "G60_MOBILE"
)

$visualStageGates = @(
  "G10_NAVBAR",
  "G20_HERO_TEXT",
  "G30_PRIMARY_VISUAL",
  "G40_CTA_SCROLL",
  "G50_FIRST_SECTION",
  "G60_MOBILE"
)

foreach ($gateId in $stageGates) {
  $gatePath = Join-Path $WorkRoot "outputs\progress\stage-gates\$gateId.md"
  if (Test-Path -LiteralPath $gatePath) {
    $gateText = Read-Text -Path $gatePath
    if ($gateText -notmatch [regex]::Escape($gateId)) {
      $invalid += "stage_gate_missing_gate_id:$gateId"
    }
    if ($gateText -notmatch "(?is)Proceed allowed\s*:\s*YES") {
      $invalid += "stage_gate_not_passed:$gateId"
    }
    if ($visualStageGates -contains $gateId) {
      $comparisonRel = "evidence\screenshots\stage-gates\${gateId}_comparison.png"
      $comparisonPath = Join-Path $WorkRoot $comparisonRel
      if (-not (Test-PngFile -Path $comparisonPath)) {
        $invalid += "stage_gate_missing_comparison_board:$gateId"
      }
      if ($gateText -notmatch [regex]::Escape("${gateId}_comparison.png")) {
        $invalid += "stage_gate_report_missing_comparison_board_reference:$gateId"
      }
      $gateDesktop = Get-PercentAfterKeyword -Text $gateText -Keywords @("桌面相似度","Desktop similarity","Desktop","桌面")
      $gateMobile = Get-PercentAfterKeyword -Text $gateText -Keywords @("移动端相似度","移动相似度","Mobile similarity","Mobile","移动")
      $gateOverall = Get-PercentAfterKeyword -Text $gateText -Keywords @("综合相似度","Overall similarity","Overall","综合")
      if ($null -eq $gateDesktop) { $invalid += "stage_gate_missing_desktop_percent:$gateId" }
      if ($null -eq $gateMobile) { $invalid += "stage_gate_missing_mobile_percent:$gateId" }
      if ($null -eq $gateOverall) { $invalid += "stage_gate_missing_overall_percent:$gateId" }
      if ($null -ne $gateDesktop -and $null -ne $gateMobile -and $null -ne $gateOverall) {
        $expectedGateOverall = [int][Math]::Round(($gateDesktop * 0.6) + ($gateMobile * 0.4), 0, [MidpointRounding]::AwayFromZero)
        if ($gateOverall -ne $expectedGateOverall) {
          $invalid += "stage_gate_formula_mismatch:$gateId expected=$expectedGateOverall actual=$gateOverall"
        }
        if ($gateDesktop -lt 95 -or $gateMobile -lt 95 -or $gateOverall -lt 95) {
          $invalid += "stage_gate_score_below_threshold:$gateId desktop=$gateDesktop mobile=$gateMobile overall=$gateOverall"
        }
      }
    }
  }
}

$roundText = ($rounds | Sort-Object Name | ForEach-Object { Read-Text -Path $_.FullName }) -join "`n`n"
$finalPath = Join-Path $WorkRoot "outputs\progress\FINAL_SIMILARITY_GATE.md"
$finalText = Read-Text -Path $finalPath
$allText = "$roundText`n`n$finalText"

foreach ($requiredRef in @("target_desktop.png","target_mobile.png","generated_desktop.png","generated_mobile.png")) {
  if ($allText -notmatch [regex]::Escape($requiredRef)) {
    $invalid += "missing_screenshot_reference:$requiredRef"
  }
}

if ($allText -notmatch "(扣分|deduction|deduct|penalty)") {
  $invalid += "missing_deduction_logic"
}

$desktopScore = Get-PercentAfterKeyword -Text $allText -Keywords @("桌面相似度","桌面","desktop similarity","desktop")
$mobileScore = Get-PercentAfterKeyword -Text $allText -Keywords @("移动端相似度","移动相似度","移动","mobile similarity","mobile")
$overallScore = Get-PercentAfterKeyword -Text $allText -Keywords @("综合相似度","综合","overall similarity","overall","composite")

if ($null -eq $desktopScore) { $invalid += "missing_desktop_similarity_percent" }
if ($null -eq $mobileScore) { $invalid += "missing_mobile_similarity_percent" }
if ($null -eq $overallScore) { $invalid += "missing_overall_similarity_percent" }

foreach ($scoreName in @("desktopScore","mobileScore","overallScore")) {
  $score = Get-Variable -Name $scoreName -ValueOnly
  if ($null -ne $score -and ($score -lt 0 -or $score -gt 100)) {
    $invalid += "invalid_percent_range:$scoreName=$score"
  }
}

if ($invalid.Count -gt 0) {
  Write-Host "PROGRESS_GATE=INVALID_TEST"
  Write-Host "Invalid:"
  $invalid | ForEach-Object { Write-Host "- $_" }
  Write-Host "RoundCompareCount=$($rounds.Count)"
  exit 2
}

$declaredPass = $allText -match "CLONE_SIMILARITY_PASS"
$buildPassed = $allText -match "(?is)(build|构建).{0,80}(pass|passed|通过|success|successful)"

Write-Host "RoundCompareCount=$($rounds.Count)"
Write-Host "DesktopSimilarity=$desktopScore%"
Write-Host "MobileSimilarity=$mobileScore%"
Write-Host "OverallSimilarity=$overallScore%"

if ($overallScore -lt 70) {
  Write-Host "PROGRESS_GATE=FAIL_SIMILARITY"
  if ($declaredPass) { Write-Host "DeclaredPassBlocked=true" }
  exit 3
}

if ($desktopScore -ge 95 -and $mobileScore -ge 95 -and $overallScore -ge 95) {
  if (-not $buildPassed) {
    Write-Host "PROGRESS_GATE=INVALID_TEST"
    Write-Host "Invalid:"
    Write-Host "- missing_build_pass_evidence_for_clone_pass"
    exit 2
  }
  Write-Host "PROGRESS_GATE=CLONE_SIMILARITY_PASS"
  exit 0
}

Write-Host "PROGRESS_GATE=PARTIAL_SIMILARITY"
if ($declaredPass) { Write-Host "DeclaredPassBlocked=true" }
exit 4
