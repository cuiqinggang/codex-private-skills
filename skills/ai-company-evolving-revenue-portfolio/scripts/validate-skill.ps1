$ErrorActionPreference = 'Stop'

$Root = Split-Path -Parent $PSScriptRoot
$RequiredFiles = @(
    'SKILL.md',
    'README.md',
    'UPDATE-SOP.md',
    'CHANGELOG.md',
    'agents\openai.yaml',
    'reports\video-analysis-report.md',
    'reports\integration-analysis.md',
    'sources\source-index.md',
    'sources\extracted-rules.md',
    'templates\revenue-path-card.md',
    'templates\context-asset-card.md',
    'templates\replay-review-template.md',
    'prompts\gpt-update-skill-pack.md',
    'prompts\codex-execute-revenue-cycle.md',
    'prompts\hermes-agent-system-prompt.md',
    'use-cases\ai-teaching-group-qa-assistant.md',
    'evidence\frames\README.md'
)

$Missing = @()
foreach ($file in $RequiredFiles) {
    $path = Join-Path $Root $file
    if (-not (Test-Path -LiteralPath $path)) {
        $Missing += $file
    }
}

if ($Missing.Count -gt 0) {
    Write-Error ("Missing required files: " + ($Missing -join ', '))
    exit 1
}

$Skill = Get-Content -Raw -LiteralPath (Join-Path $Root 'SKILL.md')
if ($Skill -notmatch '(?ms)^---\s*name:\s*ai-company-evolving-revenue-portfolio\s*description:\s*".+?"\s*---') {
    Write-Error 'SKILL.md frontmatter is invalid.'
    exit 1
}

Write-Host 'AI_COMPANY_SKILL_VALIDATE_PASS'
Write-Host 'AI_COMPANY_EVOLVING_SKILL_PACK_V0_1_READY'
