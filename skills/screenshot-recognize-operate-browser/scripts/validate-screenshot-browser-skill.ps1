param(
    [string]$SkillRoot = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = "Stop"

$skill = Join-Path $SkillRoot "SKILL.md"
$method = Join-Path $SkillRoot "references\method.md"
$agent = Join-Path $SkillRoot "agents\openai.yaml"

foreach ($path in @($skill, $method, $agent)) {
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Missing required file: $path"
    }
}

$skillText = Get-Content -LiteralPath $skill -Encoding UTF8 -Raw
$methodText = Get-Content -LiteralPath $method -Encoding UTF8 -Raw

$requiredSkillPatterns = @(
    'name:\s*screenshot-recognize-operate-browser',
    'screenshot -> locate UI -> guarded browser action -> screenshot recheck -> result verification',
    'Mature Defaults',
    'Self Check'
)

$requiredMethodPatterns = @(
    'Yesterday-Replay Defaults',
    'Gate G01: Scope And Permission',
    'Gate G02: First Screenshot',
    'Gate G03: Target Recognition',
    'Gate G04: Pre-Action Safety Check',
    'Gate G05: One Small Action',
    'Gate G06: Screenshot Recheck',
    'Gate G07: Result Verification',
    'Cross-Site Test Matrix',
    'Static page',
    'Form',
    'Modal/menu',
    'Long page',
    'Dynamic UI',
    'Copy/download',
    'ChatGPT-like',
    'Safety page',
    'clipboard sentinel',
    'Do not report success because an action was attempted'
)

$failures = New-Object System.Collections.Generic.List[string]

foreach ($pattern in $requiredSkillPatterns) {
    if ($skillText -notmatch $pattern) {
        $failures.Add("SKILL.md missing pattern: $pattern")
    }
}

foreach ($pattern in $requiredMethodPatterns) {
    if ($methodText -notmatch $pattern) {
        $failures.Add("method.md missing pattern: $pattern")
    }
}

if ($methodText -match 'click.*paste.*send.*copy.*without observation') {
    $failures.Add("method.md appears to allow chained opaque actions")
}

if ($failures.Count -gt 0) {
    Write-Host "FAIL screenshot browser skill validation"
    $failures | ForEach-Object { Write-Host "- $_" }
    exit 1
}

Write-Host "PASS screenshot browser skill validation"
Write-Host "Skill root: $SkillRoot"
