param(
  [Parameter(Mandatory=$true)]
  [string]$WorkRoot,

  [Parameter(Mandatory=$true)]
  [string]$Gate
)

$ErrorActionPreference = "Stop"

$visualThreshold = 95
$gateOrder = @(
  "G00_TARGET_CAPTURE",
  "G01_GEOMETRY_SPEC",
  "G02_COMPONENT_SPECS",
  "G03_BUILD_PLAN",
  "G10_NAVBAR",
  "G20_HERO_TEXT",
  "G30_PRIMARY_VISUAL",
  "G40_CTA_SCROLL",
  "G50_FIRST_SECTION",
  "G60_MOBILE",
  "G90_FINAL"
)

function Add-Issue {
  param(
    [Parameter(Mandatory=$true)][string]$Kind,
    [Parameter(Mandatory=$true)][string]$Message
  )
  if ($Kind -eq "missing") { $script:missing += $Message; return }
  $script:invalid += $Message
}

function Test-RequiredFile {
  param([Parameter(Mandatory=$true)][string]$RelativePath)
  $path = Join-Path $WorkRoot $RelativePath
  if (-not (Test-Path -LiteralPath $path)) {
    Add-Issue missing $RelativePath
    return $false
  }
  return $true
}

function Read-RequiredText {
  param([Parameter(Mandatory=$true)][string]$RelativePath)
  $path = Join-Path $WorkRoot $RelativePath
  if (-not (Test-RequiredFile $RelativePath)) { return "" }
  return Get-Content -LiteralPath $path -Encoding UTF8 -Raw
}

function Test-PngFile {
  param([Parameter(Mandatory=$true)][string]$RelativePath)
  $path = Join-Path $WorkRoot $RelativePath
  if (-not (Test-Path -LiteralPath $path)) {
    Add-Issue missing $RelativePath
    return $false
  }
  $item = Get-Item -LiteralPath $path
  if ($item.Length -lt 1024) {
    Add-Issue invalid "invalid_or_too_small_png:$RelativePath"
    return $false
  }
  $fs = [System.IO.File]::OpenRead($path)
  try {
    $buffer = New-Object byte[] 8
    $read = $fs.Read($buffer, 0, 8)
    $signature = @(0x89,0x50,0x4E,0x47,0x0D,0x0A,0x1A,0x0A)
    if ($read -ne 8) {
      Add-Issue invalid "invalid_png_header:$RelativePath"
      return $false
    }
    for ($i = 0; $i -lt 8; $i++) {
      if ($buffer[$i] -ne $signature[$i]) {
        Add-Issue invalid "invalid_png_header:$RelativePath"
        return $false
      }
    }
    return $true
  } finally {
    $fs.Close()
  }
}

function Get-GateReportPath {
  param([Parameter(Mandatory=$true)][string]$GateId)
  return "outputs\progress\stage-gates\$GateId.md"
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

function Assert-Contains {
  param(
    [Parameter(Mandatory=$true)][AllowEmptyString()][string]$Text,
    [Parameter(Mandatory=$true)][string]$Pattern,
    [Parameter(Mandatory=$true)][string]$Issue
  )
  if ($Text -notmatch $Pattern) {
    Add-Issue invalid $Issue
  }
}

function Assert-PreviousGatesPassed {
  param([Parameter(Mandatory=$true)][string]$CurrentGate)
  $idx = [array]::IndexOf($gateOrder, $CurrentGate)
  if ($idx -lt 0) {
    Add-Issue invalid "unknown_gate:$CurrentGate"
    return
  }
  for ($i = 0; $i -lt $idx; $i++) {
    $prev = $gateOrder[$i]
    if ($prev -eq "G90_FINAL") { continue }
    $prevRel = Get-GateReportPath $prev
    $prevText = Read-RequiredText $prevRel
    if ($prevText -and $prevText -notmatch "(?is)Proceed allowed\s*:\s*YES") {
      Add-Issue invalid "previous_gate_not_passed:$prev"
    }
  }
}

function Assert-BasicGateReport {
  param([Parameter(Mandatory=$true)][string]$GateId)
  $rel = Get-GateReportPath $GateId
  $text = Read-RequiredText $rel
  if (-not $text) { return "" }
  Assert-Contains $text ([regex]::Escape($GateId)) "gate_report_missing_gate_id:$GateId"
  Assert-Contains $text "(?is)Proceed allowed\s*:\s*(YES|NO)" "gate_report_missing_proceed_decision:$GateId"
  return $text
}

function Validate-FoundationGate {
  param([Parameter(Mandatory=$true)][string]$GateId)
  Assert-PreviousGatesPassed $GateId
  $reportText = Assert-BasicGateReport $GateId

  if ($GateId -eq "G00_TARGET_CAPTURE") {
    $baseline = Read-RequiredText "outputs\progress\00_TARGET_BASELINE.md"
    Test-PngFile "evidence\screenshots\target_desktop.png" | Out-Null
    Test-PngFile "evidence\screenshots\target_mobile.png" | Out-Null
    Test-PngFile "evidence\screenshots\target_fullpage.png" | Out-Null
    Assert-Contains $baseline "https?://" "baseline_missing_real_url"
    Assert-Contains $baseline "target_desktop\.png" "baseline_missing_target_desktop_reference"
    Assert-Contains $baseline "target_mobile\.png" "baseline_missing_target_mobile_reference"
    Assert-Contains $baseline "(allowed rewrite|允许替换)" "baseline_missing_allowed_rewrite"
    Assert-Contains $baseline "(must preserve|必须保留)" "baseline_missing_must_preserve"
  }

  if ($GateId -eq "G01_GEOMETRY_SPEC") {
    $spec = Read-RequiredText "outputs\progress\01_GEOMETRY_SPEC.md"
    foreach ($token in @("Header","Hero","Mobile")) {
      Assert-Contains $spec $token "geometry_missing_token:$token"
    }
    foreach ($token in @("x","y","width","height")) {
      Assert-Contains $spec $token "geometry_missing_measure:$token"
    }
  }

  if ($GateId -eq "G02_COMPONENT_SPECS") {
    $index = Read-RequiredText "outputs\progress\02_COMPONENT_SPECS_INDEX.md"
    foreach ($token in @("Navbar","HeroTitle","HeroSubtitle","PrimaryVisual","MobileHero")) {
      Assert-Contains $index $token "component_index_missing:$token"
    }
    Assert-Contains $index "(desktop geometry|desktop)" "component_index_missing_desktop_geometry"
    Assert-Contains $index "(mobile geometry|mobile)" "component_index_missing_mobile_geometry"
    Assert-Contains $index "(forbidden drift|不得)" "component_index_missing_forbidden_drift"
  }

  if ($GateId -eq "G03_BUILD_PLAN") {
    $plan = Read-RequiredText "outputs\progress\03_BUILD_PLAN.md"
    foreach ($token in @("G10_NAVBAR","G20_HERO_TEXT","G30_PRIMARY_VISUAL","G40_CTA_SCROLL","G50_FIRST_SECTION","G60_MOBILE")) {
      Assert-Contains $plan $token "build_plan_missing_gate:$token"
    }
    Assert-Contains $plan "validate_stage_gate\.ps1" "build_plan_missing_gate_command"
  }

  if ($reportText -and $reportText -notmatch "(?is)Proceed allowed\s*:\s*YES") {
    Add-Issue invalid "foundation_gate_report_does_not_allow_proceed:$GateId"
  }
}

function Validate-VisualGate {
  param([Parameter(Mandatory=$true)][string]$GateId)
  Assert-PreviousGatesPassed $GateId
  $reportText = Assert-BasicGateReport $GateId

  $shots = @(
    "evidence\screenshots\stage-gates\${GateId}_target_desktop.png",
    "evidence\screenshots\stage-gates\${GateId}_generated_desktop.png",
    "evidence\screenshots\stage-gates\${GateId}_target_mobile.png",
    "evidence\screenshots\stage-gates\${GateId}_generated_mobile.png",
    "evidence\screenshots\stage-gates\${GateId}_comparison.png"
  )

  foreach ($shot in $shots) {
    Test-PngFile $shot | Out-Null
    if ($reportText -and $reportText -notmatch [regex]::Escape((Split-Path -Leaf $shot))) {
      Add-Issue invalid "gate_report_missing_screenshot_reference:$shot"
    }
  }

  if (-not $reportText) { return }

  Assert-Contains $reportText "(扣分|Deductions|deduction)" "visual_gate_missing_deductions:$GateId"
  Assert-Contains $reportText "(Formula|公式)" "visual_gate_missing_formula:$GateId"

  $desktop = Get-PercentAfterKeyword $reportText @("Desktop similarity","桌面相似度","桌面")
  $mobile = Get-PercentAfterKeyword $reportText @("Mobile similarity","移动端相似度","移动相似度","移动")
  $overall = Get-PercentAfterKeyword $reportText @("Overall similarity","综合相似度","综合")

  if ($null -eq $desktop) { Add-Issue invalid "missing_desktop_similarity_percent:$GateId" }
  if ($null -eq $mobile) { Add-Issue invalid "missing_mobile_similarity_percent:$GateId" }
  if ($null -eq $overall) { Add-Issue invalid "missing_overall_similarity_percent:$GateId" }

  foreach ($pair in @(@("desktop",$desktop),@("mobile",$mobile),@("overall",$overall))) {
    if ($null -ne $pair[1] -and ($pair[1] -lt 0 -or $pair[1] -gt 100)) {
      Add-Issue invalid "invalid_percent_range:$($pair[0])=$($pair[1])"
    }
  }

  if ($null -ne $desktop -and $null -ne $mobile -and $null -ne $overall) {
    $expected = [int][Math]::Round(($desktop * 0.6) + ($mobile * 0.4), 0, [MidpointRounding]::AwayFromZero)
    if ($overall -ne $expected) {
      Add-Issue invalid "overall_formula_mismatch:expected=$expected actual=$overall"
    }
    $script:desktopScore = $desktop
    $script:mobileScore = $mobile
    $script:overallScore = $overall
  }

  if ($reportText -match "(?is)Proceed allowed\s*:\s*YES") {
    $script:proceedDeclared = $true
  } else {
    $script:proceedDeclared = $false
  }
}

function Validate-FinalGate {
  Assert-PreviousGatesPassed "G90_FINAL"
  $finalText = Read-RequiredText "outputs\progress\FINAL_SIMILARITY_GATE.md"
  Test-PngFile "evidence\screenshots\target_desktop.png" | Out-Null
  Test-PngFile "evidence\screenshots\target_mobile.png" | Out-Null
  Test-PngFile "evidence\screenshots\generated_desktop.png" | Out-Null
  Test-PngFile "evidence\screenshots\generated_mobile.png" | Out-Null

  Assert-Contains $finalText "(扣分|Deductions|deduction)" "final_missing_deductions"
  Assert-Contains $finalText "(build|构建).{0,80}(pass|passed|通过|success|successful)" "final_missing_build_pass_evidence"

  $desktop = Get-PercentAfterKeyword $finalText @("Desktop similarity","桌面相似度","桌面")
  $mobile = Get-PercentAfterKeyword $finalText @("Mobile similarity","移动端相似度","移动相似度","移动")
  $overall = Get-PercentAfterKeyword $finalText @("Overall similarity","综合相似度","综合")
  if ($null -eq $desktop) { Add-Issue invalid "missing_desktop_similarity_percent:G90_FINAL" }
  if ($null -eq $mobile) { Add-Issue invalid "missing_mobile_similarity_percent:G90_FINAL" }
  if ($null -eq $overall) { Add-Issue invalid "missing_overall_similarity_percent:G90_FINAL" }
  if ($null -ne $desktop -and $null -ne $mobile -and $null -ne $overall) {
    $expected = [int][Math]::Round(($desktop * 0.6) + ($mobile * 0.4), 0, [MidpointRounding]::AwayFromZero)
    if ($overall -ne $expected) {
      Add-Issue invalid "overall_formula_mismatch:expected=$expected actual=$overall"
    }
    $script:desktopScore = $desktop
    $script:mobileScore = $mobile
    $script:overallScore = $overall
  }
}

$missing = @()
$invalid = @()
$desktopScore = $null
$mobileScore = $null
$overallScore = $null
$proceedDeclared = $false

if ([array]::IndexOf($gateOrder, $Gate) -lt 0) {
  Add-Issue invalid "unknown_gate:$Gate"
} elseif ($Gate -in @("G00_TARGET_CAPTURE","G01_GEOMETRY_SPEC","G02_COMPONENT_SPECS","G03_BUILD_PLAN")) {
  Validate-FoundationGate $Gate
} elseif ($Gate -eq "G90_FINAL") {
  Validate-FinalGate
} else {
  Validate-VisualGate $Gate
}

Write-Host "STAGE_GATE=$Gate"

if ($missing.Count -gt 0 -or $invalid.Count -gt 0) {
  Write-Host "STATUS=INVALID_TEST"
  if ($missing.Count -gt 0) {
    Write-Host "Missing:"
    $missing | ForEach-Object { Write-Host "- $_" }
  }
  if ($invalid.Count -gt 0) {
    Write-Host "Invalid:"
    $invalid | ForEach-Object { Write-Host "- $_" }
  }
  exit 2
}

if ($null -ne $desktopScore) { Write-Host "DesktopSimilarity=$desktopScore%" }
if ($null -ne $mobileScore) { Write-Host "MobileSimilarity=$mobileScore%" }
if ($null -ne $overallScore) { Write-Host "OverallSimilarity=$overallScore%" }

if ($Gate -notin @("G00_TARGET_CAPTURE","G01_GEOMETRY_SPEC","G02_COMPONENT_SPECS","G03_BUILD_PLAN")) {
  if ($desktopScore -lt $visualThreshold -or $mobileScore -lt $visualThreshold -or $overallScore -lt $visualThreshold) {
    Write-Host "STATUS=GATE_BLOCKED"
    Write-Host "ProceedAllowed=false"
    exit 4
  }
  if (-not $proceedDeclared -and $Gate -ne "G90_FINAL") {
    Write-Host "STATUS=INVALID_TEST"
    Write-Host "Invalid:"
    Write-Host "- report_scores_pass_but_proceed_not_declared_yes"
    exit 2
  }
}

Write-Host "STATUS=PASS"
Write-Host "ProceedAllowed=true"
exit 0
