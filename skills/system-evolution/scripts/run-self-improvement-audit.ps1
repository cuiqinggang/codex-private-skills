param(
  [ValidateSet("ReportOnly", "Approval")]
  [string]$Mode = "ReportOnly",
${REDACTED_SECRET}
)

$ErrorActionPreference = "SilentlyContinue"
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$runRoot = Join-Path $OutputRoot $stamp
$dirs = @($runRoot, "$runRoot\evidence", "$runRoot\reports")
foreach ($dir in $dirs) {
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

function Redact-Line {
  param([string]$Text)
  if ($null -eq $Text) { return "" }
  return ($Text -replace "(?i)(api[_-]?key|token|secret|password|cookie|authorization)\s*[:=]\s*\S+", '$1=[REDACTED]' -replace "(?i)sk-[A-Za-z0-9_-]{10,}", "sk-[REDACTED]")
}

function Get-SkillSummary {
  param([string]$Path)
  if (-not (Test-Path -LiteralPath $Path)) {
    return [ordered]@{ path = $Path; status = "NOT_FOUND" }
  }
  $text = Get-Content -LiteralPath $Path -Raw
  $name = ([regex]::Match($text, "(?m)^name:\s*(.+)$")).Groups[1].Value
  $description = ([regex]::Match($text, "(?m)^description:\s*""?(.+?)""?\s*$")).Groups[1].Value
  $headings = @()
  foreach ($m in [regex]::Matches($text, "(?m)^#{1,3}\s+(.+)$")) {
    if ($headings.Count -lt 10) { $headings += $m.Groups[1].Value }
  }
  return [ordered]@{
    path = $Path
    status = "FOUND"
    name = (Redact-Line $name)
    description = (Redact-Line $description)
    headings = $headings
  }
}

$evidence = [ordered]@{
  created_at = (Get-Date).ToString("s")
  mode = $Mode
  roots = [ordered]@{
${REDACTED_SECRET}
${REDACTED_SECRET}
    hSkills = "H:\AI\skills"
    hWorkspaces = "H:\AI\workspaces"
  }
}

${REDACTED_SECRET}
$keywords = @("Hermes","OpenClaw","ComfyUI","ECC","DeepSeek","skill","Xiaolongxia","New API","Open WebUI","AI Company","Gateway","Watchdog","Codex")
$sessionHits = @()
if (Test-Path -LiteralPath $sessionIndex) {
  Get-Content -LiteralPath $sessionIndex | ForEach-Object {
    try { $o = $_ | ConvertFrom-Json } catch { return }
    $name = [string]$o.thread_name
    foreach ($kw in $keywords) {
      if ($name -like "*$kw*") {
        $sessionHits += [ordered]@{ updated_at = $o.updated_at; keyword = $kw; id = $o.id; thread_name = (Redact-Line $name) }
        break
      }
    }
  }
}
$evidence.session_hits = $sessionHits

${REDACTED_SECRET}
$topicCounts = @{}
$examples = @{}
if (Test-Path -LiteralPath $outputRoot) {
  Get-ChildItem -LiteralPath $outputRoot -Directory | ForEach-Object {
    $n = $_.Name
    $topic = "Other"
    if ($n -match "ECC|ecc-") { $topic = "ECC" }
    elseif ($n -match "HERMES|OPEN-DESIGN|OPENWEBUI|NEWAPI|New API") { $topic = "Hermes/NewAPI/OpenDesign" }
    elseif ($n -match "XIAOLONGXIA|OPENCLAW|telegram-xiaolongxia|QWEN27") { $topic = "Xiaolongxia/OpenClaw" }
    elseif ($n -match "comfyui|COMFYUI") { $topic = "ComfyUI" }
    elseif ($n -match "AI-COMPANY|POLSIA") { $topic = "AI Company/Design" }
    elseif ($n -match "CODEX|yesterday-replay|screenshot-browser|screenshot-recognize|rule-auth") { $topic = "Codex Skills/Controls" }
    if (-not $topicCounts.ContainsKey($topic)) { $topicCounts[$topic] = 0; $examples[$topic] = @() }
    $topicCounts[$topic] = $topicCounts[$topic] + 1
    if ($examples[$topic].Count -lt 5) { $examples[$topic] += $n }
  }
}
$evidence.output_topics = @()
foreach ($k in $topicCounts.Keys) {
  $evidence.output_topics += [ordered]@{ topic = $k; count = $topicCounts[$k]; examples = $examples[$k] }
}

$skillFiles = @(
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
  "H:\AI\skills\ecc-endurance-ladder-unified\SKILL.md",
  "H:\AI\skills\comfyui-aaki-v3-video-baseline\SKILL.md",
  "H:\AI\skills\ai-company-design-systems\SKILL.md"
)
$evidence.skills = @()
foreach ($f in $skillFiles) {
  $evidence.skills += Get-SkillSummary -Path $f
}

${REDACTED_SECRET}
$automationTomlCount = 0
if (Test-Path -LiteralPath $automations) {
  $automationTomlCount = (Get-ChildItem -LiteralPath $automations -Recurse -File -Filter "automation.toml").Count
}
$evidence.automation_toml_count = $automationTomlCount

$taskName = "Codex_SelfImprovement_Audit_Biweekly"
$taskInfo = schtasks /query /TN $taskName /FO LIST /V 2>$null
$evidence.scheduled_task = [ordered]@{
  name = $taskName
  exists = [bool]$taskInfo
  summary = (($taskInfo | Select-String -Pattern "TaskName:|Next Run Time:|Status:|Last Run Time:|Last Result:|Task To Run:|Schedule:") | ForEach-Object { Redact-Line $_.Line })
}

$jsonPath = Join-Path $runRoot "evidence\self-improvement-audit-evidence.json"
$evidence | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $jsonPath -Encoding UTF8

$candidates = @(
${REDACTED_SECRET}
  [ordered]@{ name = "Windows Hermes quick healthcheck"; evidence = "windows-hermes-operations quick healthcheck script"; asset = "Runbook+Script"; priority = "A"; status = "implemented-readonly-check" },
  [ordered]@{ name = "Xiaolongxia route acceptance matrix"; evidence = "xiaolongxia-openclaw-gateway-safety-recovery route matrix"; asset = "Checklist+Script"; priority = "A"; status = "implemented-readonly-check" },
  [ordered]@{ name = "Open Design Codex reconnect check"; evidence = "codex-lite-power-upgrade connectivity reference"; asset = "Runbook+Script"; priority = "A"; status = "implemented-readonly-check" },
  [ordered]@{ name = "Periodic self-improvement audit"; evidence = $jsonPath; asset = "Automation+Checklist"; priority = "A"; status = "implemented-script" }
)

$reportPath = Join-Path $runRoot "CODEX_SELF_IMPROVEMENT_AUDIT_REPORT.md"
$lines = @()
$lines += "# CODEX_SELF_IMPROVEMENT_AUDIT_REPORT"
$lines += ""
$lines += "- Created: $(Get-Date -Format s)"
$lines += "- Mode: $Mode"
$lines += "- Evidence JSON: $jsonPath"
$lines += "- Boundary: read-only audit and report generation; no production services changed."
$lines += ""
$lines += "## Evidence Summary"
$lines += ""
$lines += "- Session hits: $($sessionHits.Count)"
$lines += "- Output topic groups: $($topicCounts.Count)"
$lines += "- Skill summaries checked: $($skillFiles.Count)"
$lines += "- Codex app automation TOML count: $automationTomlCount"
$lines += ""
$lines += "## Candidates"
$lines += ""
foreach ($c in $candidates) {
  $lines += "### $($c.name)"
  $lines += "- Asset type: $($c.asset)"
  $lines += "- Priority: $($c.priority)"
  $lines += "- Status: $($c.status)"
  $lines += "- Evidence: $($c.evidence)"
  $lines += ""
}
$lines += "## Prompt Improvement Slot"
$lines += ""
$lines += "Periodic runs should look for better public self-improvement audit prompts only when a Codex/browser research path is available. A better prompt must improve evidence quality, candidate scoring, verification, or rollback clarity. Popularity alone is not enough."
$lines += ""
$lines += "## Skip Rules"
$lines += ""
$lines += "- Skip broad duplicate all-in-one skills."
$lines += "- Skip full `H:\AI\skills` scans."
$lines += "- Skip secret/token/cookie inspection."
$lines += "- Skip production service starts/stops unless separately approved."
$lines += ""
$lines += "## Final Status"
$lines += ""
$lines += "CODEX_SELF_IMPROVEMENT_PERIODIC_AUDIT_PASS"
$lines | Set-Content -LiteralPath $reportPath -Encoding UTF8

Write-Output "CODEX_SELF_IMPROVEMENT_PERIODIC_AUDIT_PASS"
Write-Output $reportPath
