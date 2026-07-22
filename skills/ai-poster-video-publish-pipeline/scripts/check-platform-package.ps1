param(
    [Parameter(Mandatory = $true)]
    [string]$PackagePath,

    [string]$ReportPath
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $PackagePath)) {
    throw "Publish package path not found: $PackagePath"
}

$packageFull = (Resolve-Path -LiteralPath $PackagePath).Path
if (-not $ReportPath -or $ReportPath.Trim().Length -eq 0) {
    $ReportPath = Join-Path (Join-Path $packageFull '..\reports') 'platform-check.json'
}
$reportDir = Split-Path -Parent $ReportPath
New-Item -ItemType Directory -Force -Path $reportDir | Out-Null

$patterns = @(
    [pscustomobject]@{ name = 'phone'; pattern = '(?<!\d)(1[3-9]\d{9}|0\d{2,3}[- ]?\d{7,8}|\d{3,4}[- ]?\d{7,8})(?!\d)' },
    [pscustomobject]@{ name = 'wechat'; pattern = '微信|VX|vx|V信|v信|WeChat|wechat|wxid|wx' },
    [pscustomobject]@{ name = 'qr_code'; pattern = '二维码|扫码|扫一扫' },
    [pscustomobject]@{ name = 'contact_me'; pattern = '可微我|加我|联系我|私信我|加好友' }
)

function Scan-TextFiles {
    param([string]$Dir)
    $hits = @()
    if (-not (Test-Path -LiteralPath $Dir)) {
        return $hits
    }
    $files = Get-ChildItem -LiteralPath $Dir -Recurse -File | Where-Object {
        $_.Extension -in @('.txt', '.json', '.csv') -and $_.Name -ne 'group-whitelist.json'
    }
    foreach ($file in $files) {
        $text = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
        foreach ($pat in $patterns) {
            if ($text -match $pat.pattern) {
                $hits += [pscustomobject]@{
                    file = $file.FullName
                    rule = $pat.name
                    pattern = $pat.pattern
                }
            }
        }
    }
    return $hits
}

function Test-RequiredPackageFiles {
    param([string]$Dir, [string[]]$Required)
    $missing = @()
    foreach ($name in $Required) {
        $path = Join-Path $Dir $name
        if (-not (Test-Path -LiteralPath $path)) {
            $missing += $path
        }
    }
    return $missing
}

$douyinDir = Join-Path $packageFull 'douyin'
$momentsDir = Join-Path $packageFull 'wechat_moments'
$groupsDir = Join-Path $packageFull 'wechat_groups'

$missing = @()
$missing += Test-RequiredPackageFiles -Dir $douyinDir -Required @('video.mp4', 'caption.txt', 'checklist.md')
$missing += Test-RequiredPackageFiles -Dir $momentsDir -Required @('video.mp4', 'caption.txt', 'checklist.md')
$missing += Test-RequiredPackageFiles -Dir $groupsDir -Required @('video.mp4', 'caption.txt', 'group-whitelist.json', 'checklist.md')

$douyinHits = @(Scan-TextFiles -Dir $douyinDir)
$wechatMomentsHits = @(Scan-TextFiles -Dir $momentsDir)
$wechatGroupsHits = @(Scan-TextFiles -Dir $groupsDir)

$status = 'PASS'
if ($missing.Count -gt 0 -or $douyinHits.Count -gt 0) {
    $status = 'FAIL'
}

$result = [pscustomobject]@{
    status = $status
    package_path = $packageFull
    missing_required_files = $missing
    douyin_contact_hits = $douyinHits
    wechat_moments_contact_markers = $wechatMomentsHits
    wechat_groups_contact_markers = $wechatGroupsHits
    note = 'Scans publish payload text files; checklist and whitelist policy files are existence-checked but not treated as publish text. Video/image OCR still requires content review.'
    required_stop = @(
        '抖音包命中电话、微信、二维码、可微我、加我等内容必须 STOP',
        '微信群只允许白名单群',
        '遇到平台风控、安全验证、违规提示必须停止'
    )
}

$result | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $ReportPath -Encoding UTF8
if ($status -eq 'PASS') {
    Write-Output "PASS platform package check: $ReportPath"
}
else {
    Write-Output "FAIL platform package check: $ReportPath"
    exit 1
}




