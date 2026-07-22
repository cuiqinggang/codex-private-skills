param(
  [int]$Days = 30,
${REDACTED_SECRET}
)

$ErrorActionPreference = "Stop"

$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$runDir = Join-Path $OutputDir "codex-self-improvement-audit-$stamp"
New-Item -ItemType Directory -Force -Path $runDir | Out-Null

$roots = @(
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
)

$since = (Get-Date).AddDays(-1 * $Days)
$evidence = @()

foreach ($root in $roots) {
  if (-not (Test-Path -LiteralPath $root)) { continue }

  Get-ChildItem -LiteralPath $root -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object {
      $_.LastWriteTime -ge $since -and
      $_.Length -le 5MB -and
      $_.FullName -notmatch '\\(\.git|node_modules|__pycache__|dist|build|\.cache)\\' -and
      $_.Extension -match '^\.(md|txt|toml|json|html|ps1|py)$'
    } |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 300 |
    ForEach-Object {
      $evidence += [pscustomobject]@{
        LastWriteTime = $_.LastWriteTime.ToString("s")
        Length = $_.Length
        Path = $_.FullName
      }
    }
}

$csvPath = Join-Path $runDir "recent-evidence.csv"
$evidence | Export-Csv -NoTypeInformation -Encoding UTF8 -LiteralPath $csvPath

$promptPath = Join-Path $runDir "audit-prompt.md"
$reportPath = Join-Path $runDir "audit-report-template.md"

$prompt = @"
# Codex Self-Improvement Audit Prompt

Review the evidence list in:

$csvPath

Use:

${REDACTED_SECRET}

Task:

1. Review the last $Days days of evidence.
2. Identify repeated, time-consuming, error-prone, or context-heavy workflows.
3. Decide the smallest useful form for each candidate: skill, subagent,
   automation, extend existing, or skip.
4. Produce a shortlist with evidence dates, confidence, and recommendation.
5. Create or update only high-confidence, narrow assets.
6. Leave ambiguous items in the report instead of packaging them.

Boundary:

- C-drive hot paths are primary.
- K/H drives are backup/reference only unless explicitly requested.
- Do not store secrets.
- Do not create active automations without explicit user approval.
"@

Set-Content -LiteralPath $promptPath -Encoding UTF8 -Value $prompt

$template = @"
# Codex Self-Improvement Audit Report

Status: DRAFT
Window: last $Days days
Generated: $(Get-Date -Format s)

## Shortlist

| Candidate | Evidence | Frequency | Recommendation | Confidence | Decision |
|---|---|---:|---|---:|---|

## Created Or Extended

- None yet.

## Deliberately Skipped

- None yet.

## Needs More Evidence

- None yet.

## Next Run

Use the prompt in `audit-prompt.md` and update this report with decisions.
"@

Set-Content -LiteralPath $reportPath -Encoding UTF8 -Value $template

Write-Host "CODEX_SELF_IMPROVEMENT_AUDIT_PACK_READY"
Write-Host "RunDir: $runDir"
Write-Host "Evidence: $csvPath"
Write-Host "Prompt: $promptPath"
Write-Host "Report: $reportPath"
