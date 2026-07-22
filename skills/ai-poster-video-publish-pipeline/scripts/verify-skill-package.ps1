param(
    [string]$SkillRoot,
    [string]$ReportPath
)

$ErrorActionPreference = 'Stop'

if (-not $SkillRoot -or $SkillRoot.Trim().Length -eq 0) {
    $SkillRoot = Split-Path -Parent $PSScriptRoot
}
$SkillRoot = [System.IO.Path]::GetFullPath($SkillRoot)
if (-not $ReportPath -or $ReportPath.Trim().Length -eq 0) {
    $ReportPath = Join-Path $SkillRoot 'reports\creation-20260528\verification.json'
}

$errors = New-Object System.Collections.Generic.List[string]
$warnings = New-Object System.Collections.Generic.List[string]

function Add-Error {
    param([string]$Message)
    $script:errors.Add($Message) | Out-Null
}

function Test-File {
    param([string]$RelativePath)
    $path = Join-Path $SkillRoot $RelativePath
    if (-not (Test-Path -LiteralPath $path)) {
        Add-Error "Missing required file: $RelativePath"
    }
}

$requiredFiles = @(
    'SKILL.md',
    'README.md',
    'RUNBOOK.md',
    'PLATFORM-RULES.md',
    'CONTENT-REVIEW-GATE.md',
    'AUTO-PUBLISH-GATE.md',
    'VIDEO-SPEC.md',
    'PROMPT-TEMPLATES.md',
    'CASE-STUDY-20260528.md',
    'templates\config.full.json',
    'templates\config.short.json',
    'templates\publish-approved.template.json',
    'templates\douyin-caption.txt',
    'templates\wechat-moments-caption.txt',
    'templates\group-whitelist.template.json',
    'scripts\build-slideshow.ps1',
    'scripts\validate-video.ps1',
    'scripts\check-platform-package.ps1',
    'scripts\prepare-publish-package.ps1',
    'scripts\verify-skill-package.ps1',
    'reports\creation-20260528\final-report.md'
)

foreach ($file in $requiredFiles) {
    Test-File $file
}

$hardRules = @(
    '宣传图和能力图必须分离',
    '宣传图必须有微信版和抖音版',
    '视频第一张必须是宣传图',
    'full版视频最后必须再次出现宣传图',
    '视频默认稳定静态展示',
    '如果任何动效导致文字发虚或画面不稳',
    '抖音包必须自动检查导流信息',
    '内容审核通过后，自动发布属于机械执行',
    '遇到验证码、人脸、短信、安全提示、违规提示、付费推广、删除文件、批量私信、批量群发陌生对象',
    '微信群只允许白名单群',
    '发布后必须截图留证',
    '任何最终 PASS 必须有验证脚本或确定性清单证据'
)

$ruleFiles = @(
    'SKILL.md',
    'RUNBOOK.md',
    'PLATFORM-RULES.md',
    'CONTENT-REVIEW-GATE.md',
    'AUTO-PUBLISH-GATE.md'
)

foreach ($file in $ruleFiles) {
    $path = Join-Path $SkillRoot $file
    if (Test-Path -LiteralPath $path) {
        $text = Get-Content -LiteralPath $path -Raw -Encoding UTF8
        foreach ($rule in $hardRules) {
            if ($text.IndexOf($rule, [System.StringComparison]::Ordinal) -lt 0) {
                Add-Error "Missing hard rule in ${file}: $rule"
            }
        }
    }
}

$jsonFiles = @(
    'templates\config.full.json',
    'templates\config.short.json',
    'templates\publish-approved.template.json',
    'templates\group-whitelist.template.json'
)
foreach ($file in $jsonFiles) {
    $path = Join-Path $SkillRoot $file
    if (Test-Path -LiteralPath $path) {
        try {
            Get-Content -LiteralPath $path -Raw -Encoding UTF8 | ConvertFrom-Json | Out-Null
        }
        catch {
            Add-Error "Invalid JSON ${file}: $($_.Exception.Message)"
        }
    }
}

$scriptFiles = @(
    'scripts\build-slideshow.ps1',
    'scripts\validate-video.ps1',
    'scripts\check-platform-package.ps1',
    'scripts\prepare-publish-package.ps1',
    'scripts\verify-skill-package.ps1'
)
foreach ($file in $scriptFiles) {
    $path = Join-Path $SkillRoot $file
    if (Test-Path -LiteralPath $path) {
        $tokens = $null
        $parseErrors = $null
        [System.Management.Automation.Language.Parser]::ParseFile($path, [ref]$tokens, [ref]$parseErrors) | Out-Null
        if ($parseErrors -and $parseErrors.Count -gt 0) {
            foreach ($err in $parseErrors) {
                Add-Error "PowerShell parse error ${file}: $($err.Message)"
            }
        }
    }
}

$skillPath = Join-Path $SkillRoot 'SKILL.md'
if (Test-Path -LiteralPath $skillPath) {
    $skillText = Get-Content -LiteralPath $skillPath -Raw -Encoding UTF8
    if ($skillText -notmatch '(?s)^---\s+name:\s*ai-poster-video-publish-pipeline\s+description:\s*.+?\s+---') {
        Add-Error 'SKILL.md frontmatter is missing required name/description.'
    }
}

$status = if ($errors.Count -eq 0) { 'PASS' } else { 'FAIL' }
$result = [pscustomobject]@{
    status = $status
    skill_root = $SkillRoot
    required_file_count = $requiredFiles.Count
    hard_rule_count = $hardRules.Count
    checked_rule_files = $ruleFiles
    checked_scripts = $scriptFiles
    errors = $errors
    warnings = $warnings
    no_real_publish_performed = $true
}

$reportDir = Split-Path -Parent $ReportPath
New-Item -ItemType Directory -Force -Path $reportDir | Out-Null
$result | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $ReportPath -Encoding UTF8

if ($status -eq 'PASS') {
    Write-Output "PASS skill package verification: $ReportPath"
}
else {
    Write-Output "FAIL skill package verification: $ReportPath"
    foreach ($err in $errors) {
        Write-Output "ERROR: $err"
    }
    exit 1
}



