param(
  [string]$Path = "."
)

$mdPath = Join-Path $Path "final-acceptance.md"
$jsonPath = Join-Path $Path "final-acceptance.json"
$errors = @()

if (-not (Test-Path -LiteralPath $mdPath)) { $errors += "missing final-acceptance.md" }
if (-not (Test-Path -LiteralPath $jsonPath)) { $errors += "missing final-acceptance.json" }

if (Test-Path -LiteralPath $mdPath) {
  $md = Get-Content -LiteralPath $mdPath -Raw -Encoding UTF8
  foreach ($heading in @("## Task ID", "## Final Decision", "## Evidence Summary", "## Verification Summary", "## Safety Boundary Check", "## Final Verdict")) {
    if ($md -notmatch [regex]::Escape($heading)) { $errors += "missing heading $heading" }
  }
}

if (Test-Path -LiteralPath $jsonPath) {
  try {
    $json = Get-Content -LiteralPath $jsonPath -Raw -Encoding UTF8 | ConvertFrom-Json
    foreach ($field in @("task_id", "final_decision", "evidence", "verification", "safety_boundary_check", "final_verdict")) {
      if (-not ($json.PSObject.Properties.Name -contains $field)) { $errors += "missing json field $field" }
    }
  } catch {
    $errors += "invalid json: $($_.Exception.Message)"
  }
}

$result = [ordered]@{
  check = "final-acceptance"
  path = (Resolve-Path -LiteralPath $Path -ErrorAction SilentlyContinue).Path
  status = if ($errors.Count -eq 0) { "PASS" } else { "FAIL" }
  errors = $errors
}

$result | ConvertTo-Json -Depth 6
if ($errors.Count -gt 0) { exit 1 }
