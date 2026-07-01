param(
  [Parameter(Mandatory = $true)]
  [string]$Path
)

$requiredHeadings = @(
  "## Gate ID",
  "## Task ID",
  "## Current Level",
  "## What Codex Did",
  "## Evidence Produced",
  "## Verification Results",
  "## Codex Claim",
  "## Requested GPT Decision"
)

$text = Get-Content -LiteralPath $Path -Raw -Encoding UTF8
$missing = @()
foreach ($heading in $requiredHeadings) {
  if ($text -notmatch [regex]::Escape($heading)) {
    $missing += $heading
  }
}

$result = [ordered]@{
  check = "gate-report"
  path = $Path
  status = if ($missing.Count -eq 0) { "PASS" } else { "FAIL" }
  missing = $missing
}

$result | ConvertTo-Json -Depth 5
if ($missing.Count -gt 0) { exit 1 }
