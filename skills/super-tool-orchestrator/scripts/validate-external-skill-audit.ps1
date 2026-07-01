param(
  [Parameter(Mandatory = $true)]
  [string]$Path
)

$requiredHeadings = @(
  "## External Source",
  "## External Skill",
  "## Local Skill Conflict",
  "## Local Skill Summary",
  "## External Skill Summary",
  "## Overlap",
  "## Useful Parts",
  "## Risks",
  "## Recommendation",
  "## Approval Required"
)

$text = Get-Content -LiteralPath $Path -Raw -Encoding UTF8
$missing = @()
foreach ($heading in $requiredHeadings) {
  if ($text -notmatch [regex]::Escape($heading)) { $missing += $heading }
}

$result = [ordered]@{
  check = "external-skill-audit"
  path = $Path
  status = if ($missing.Count -eq 0) { "PASS" } else { "FAIL" }
  missing = $missing
}

$result | ConvertTo-Json -Depth 5
if ($missing.Count -gt 0) { exit 1 }
