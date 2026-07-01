param(
  [string]$Path = "."
)

$required = @(
  "00-goal.md",
  "01-context.md",
  "02-plan.md",
  "03-execution-log.md",
  "04-verification.md",
  "05-handoff.md",
  "06-next-actions.md",
  "07-loop-control.md",
  "08-rollback.md",
  "09-decisions.md"
)

$missing = @()
foreach ($file in $required) {
  if (-not (Test-Path -LiteralPath (Join-Path $Path $file))) {
    $missing += $file
  }
}

$result = [ordered]@{
  check = "task-package"
  path = (Resolve-Path -LiteralPath $Path -ErrorAction SilentlyContinue).Path
  status = if ($missing.Count -eq 0) { "PASS" } else { "FAIL" }
  missing = $missing
}

$result | ConvertTo-Json -Depth 5
if ($missing.Count -gt 0) { exit 1 }
