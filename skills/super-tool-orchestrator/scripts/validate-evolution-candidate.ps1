param(
  [Parameter(Mandatory = $true)]
  [string]$Path
)

$requiredHeadings = @(
  "## Source Task",
  "## Trigger",
  "## Candidate Type",
  "## Problem Solved",
  "## Proposed Change",
  "## Target Skill",
  "## Risk",
  "## Conflict Check",
  "## Validation Required",
  "## Approval Required"
)

$text = Get-Content -LiteralPath $Path -Raw -Encoding UTF8
$missing = @()
foreach ($heading in $requiredHeadings) {
  if ($text -notmatch [regex]::Escape($heading)) { $missing += $heading }
}

$result = [ordered]@{
  check = "evolution-candidate"
  path = $Path
  status = if ($missing.Count -eq 0) { "PASS" } else { "FAIL" }
  missing = $missing
}

$result | ConvertTo-Json -Depth 5
if ($missing.Count -gt 0) { exit 1 }
