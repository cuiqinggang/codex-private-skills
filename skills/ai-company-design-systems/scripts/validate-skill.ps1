$ErrorActionPreference = 'Stop'

$Root = Split-Path -Parent $PSScriptRoot
$RequiredFiles = @(
    'SKILL.md',
    'agents\openai.yaml',
    'references\github-research-20260526.md',
    'references\design-system-rules-20260526.md',
    'templates\design-system-manifest.json'
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
if ($Skill -notmatch '(?ms)^---\s*name:\s*ai-company-design-systems\s*description:\s*".+?"\s*---') {
    Write-Error 'SKILL.md frontmatter is invalid.'
    exit 1
}

$RequiredPhrases = @(
    'skills visualization',
    'approval inbox',
    'revenue path',
    'shadcn-ui/ui',
    'xyflow/xyflow',
    'human approval'
)

foreach ($phrase in $RequiredPhrases) {
    if ($Skill -notlike "*$phrase*") {
        Write-Error "SKILL.md missing required phrase: $phrase"
        exit 1
    }
}

$TemplateRaw = Get-Content -Raw -LiteralPath (Join-Path $Root 'templates\design-system-manifest.json')
$Template = $TemplateRaw | ConvertFrom-Json
foreach ($section in @('tokens', 'components', 'data_objects', 'views', 'governance', 'references', 'validation')) {
    if (-not ($Template.PSObject.Properties.Name -contains $section)) {
        Write-Error "Template missing section: $section"
        exit 1
    }
}

Write-Host 'AI_COMPANY_DESIGN_SYSTEMS_SKILL_VALIDATE_PASS'
Write-Host 'AI_COMPANY_DESIGN_SYSTEMS_SKILL_READY'
