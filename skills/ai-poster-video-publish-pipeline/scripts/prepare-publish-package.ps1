param(
    [string]$DouyinVideo,
    [string]$WechatMomentsVideo,
    [string]$WechatGroupsVideo,
    [string]$DouyinCaption,
    [string]$WechatMomentsCaption,
    [string]$WechatGroupsCaption,
    [string]$CoverImage,
    [string]$GroupWhitelist,
    [string]$OutputRoot = 'publish_package'
)

$ErrorActionPreference = 'Stop'

function Get-SkillRoot {
    return (Split-Path -Parent $PSScriptRoot)
}

function Read-TextArg {
    param(
        [string]$Value,
        [string]$DefaultPath
    )
    if ($Value -and (Test-Path -LiteralPath $Value)) {
        return Get-Content -LiteralPath $Value -Raw -Encoding UTF8
    }
    if ($Value -and $Value.Trim().Length -gt 0) {
        return $Value
    }
    return Get-Content -LiteralPath $DefaultPath -Raw -Encoding UTF8
}

function Copy-Video {
    param([string]$Source, [string]$Destination)
    if (-not $Source -or -not (Test-Path -LiteralPath $Source)) {
        throw "Video file not found: $Source"
    }
    Copy-Item -LiteralPath $Source -Destination $Destination -Force
}

function Write-Cover {
    param([string]$Video, [string]$Destination)
    if ($CoverImage -and (Test-Path -LiteralPath $CoverImage)) {
        Copy-Item -LiteralPath $CoverImage -Destination $Destination -Force
        return
    }
    if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
        return
    }
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        $output = & ffmpeg -y -i $Video -frames:v 1 -q:v 2 $Destination 2>&1
        $code = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $oldPreference
    }
    $output | Set-Content -LiteralPath ($Destination + '.log') -Encoding UTF8
    if ($code -ne 0) {
        throw "cover extraction failed for $Video"
    }
}

function Write-Checklist {
    param([string]$Path, [string]$Platform)
    $content = @"
# $Platform checklist

- [ ] 视频文件存在。
- [ ] 文案文件存在。
- [ ] 封面存在或可从视频首帧生成。
- [ ] 宣传图和能力图已分离。
- [ ] 视频第一张是宣传图。
- [ ] full 版最后再次出现宣传图。
- [ ] 视频稳定静态展示，只允许淡入淡出。
- [ ] 内容审核通过后才允许自动发布。
- [ ] 发布后必须截图留证。
"@
    if ($Platform -eq 'douyin') {
        $content += "`n- [ ] 抖音包无电话、微信、二维码、可微我、加我等导流信息。`n"
    }
    if ($Platform -eq 'wechat_groups') {
        $content += "`n- [ ] 群名在白名单内；禁止群发所有群。`n"
    }
    Set-Content -LiteralPath $Path -Value $content -Encoding UTF8
}

$skillRoot = Get-SkillRoot
$templates = Join-Path $skillRoot 'templates'
$outputFull = [System.IO.Path]::GetFullPath($OutputRoot)
New-Item -ItemType Directory -Force -Path $outputFull | Out-Null

$douyinDir = Join-Path $outputFull 'douyin'
$momentsDir = Join-Path $outputFull 'wechat_moments'
$groupsDir = Join-Path $outputFull 'wechat_groups'
New-Item -ItemType Directory -Force -Path $douyinDir, $momentsDir, $groupsDir | Out-Null

Copy-Video -Source $DouyinVideo -Destination (Join-Path $douyinDir 'video.mp4')
Copy-Video -Source $WechatMomentsVideo -Destination (Join-Path $momentsDir 'video.mp4')
Copy-Video -Source $WechatGroupsVideo -Destination (Join-Path $groupsDir 'video.mp4')

$douyinCaptionText = Read-TextArg -Value $DouyinCaption -DefaultPath (Join-Path $templates 'douyin-caption.txt')
$momentsCaptionText = Read-TextArg -Value $WechatMomentsCaption -DefaultPath (Join-Path $templates 'wechat-moments-caption.txt')
$groupsCaptionText = Read-TextArg -Value $WechatGroupsCaption -DefaultPath (Join-Path $templates 'wechat-moments-caption.txt')

Set-Content -LiteralPath (Join-Path $douyinDir 'caption.txt') -Value $douyinCaptionText -Encoding UTF8
Set-Content -LiteralPath (Join-Path $momentsDir 'caption.txt') -Value $momentsCaptionText -Encoding UTF8
Set-Content -LiteralPath (Join-Path $groupsDir 'caption.txt') -Value $groupsCaptionText -Encoding UTF8

Write-Cover -Video (Join-Path $douyinDir 'video.mp4') -Destination (Join-Path $douyinDir 'cover.png')
Write-Cover -Video (Join-Path $momentsDir 'video.mp4') -Destination (Join-Path $momentsDir 'cover.png')
Write-Cover -Video (Join-Path $groupsDir 'video.mp4') -Destination (Join-Path $groupsDir 'cover.png')

if ($GroupWhitelist -and (Test-Path -LiteralPath $GroupWhitelist)) {
    Copy-Item -LiteralPath $GroupWhitelist -Destination (Join-Path $groupsDir 'group-whitelist.json') -Force
}
else {
    Copy-Item -LiteralPath (Join-Path $templates 'group-whitelist.template.json') -Destination (Join-Path $groupsDir 'group-whitelist.json') -Force
}

Write-Checklist -Path (Join-Path $douyinDir 'checklist.md') -Platform 'douyin'
Write-Checklist -Path (Join-Path $momentsDir 'checklist.md') -Platform 'wechat_moments'
Write-Checklist -Path (Join-Path $groupsDir 'checklist.md') -Platform 'wechat_groups'

$manifest = [pscustomobject]@{
    status = 'PASS'
    output_root = $outputFull
    packages = @{
        douyin = $douyinDir
        wechat_moments = $momentsDir
        wechat_groups = $groupsDir
    }
    note = 'No real publish was performed. Run content review before publish-approved.json.'
}
$manifestPath = Join-Path $outputFull 'publish-package-manifest.json'
$manifest | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $manifestPath -Encoding UTF8
Write-Output "PASS publish package prepared: $manifestPath"



