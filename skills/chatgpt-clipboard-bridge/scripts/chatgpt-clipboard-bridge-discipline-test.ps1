param(
    [string]$AgentsPath = "AGENTS.md",
${REDACTED_SECRET}
    [string]$DisciplinePath = "docs/chatgpt-clipboard-bridge-execution-discipline.md"
)

$ErrorActionPreference = "Stop"

function Read-Utf8 {
    param([string]$Path)
    $resolved = Resolve-Path -LiteralPath $Path
    return [System.IO.File]::ReadAllText($resolved, [System.Text.Encoding]::UTF8)
}

$agents = Read-Utf8 $AgentsPath
$skill = Read-Utf8 $SkillPath
if (Test-Path -LiteralPath $DisciplinePath) {
    $discipline = Read-Utf8 $DisciplinePath
} else {
    $discipline = ""
}

$combined = $agents + "`n" + $skill + "`n" + $discipline

$required = @(
    "默认自动执行",
    "只有高风险才停",
    "Codex 不改写 GPT",
    "结构提取",
    "一一对应",
    "Level 0",
    "Level 1",
    "Level 2",
    "Level 3",
    "执行范围锁",
    "复制回复 / Copy response",
    "Never fall back to CDP",
    "page-body text",
    "OCR"
)

foreach ($needle in $required) {
    if (-not $combined.Contains($needle)) {
        throw "Execution discipline is missing required rule: $needle"
    }
}

Write-Host "[chatgpt-bridge-discipline-test] execution discipline checks passed"
