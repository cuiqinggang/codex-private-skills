param(
    [string]$OutputRoot = (Join-Path (Get-Location).Path 'output\cursor-menubar-cn'),
    [string]$CursorInstallRoot = (Join-Path $env:LOCALAPPDATA 'Programs\cursor')
)

$ErrorActionPreference = 'Stop'
$appRoot = Join-Path $CursorInstallRoot 'resources\app'
$desktopRel = 'out\vs\workbench\workbench.desktop.main.js'
$productRel = 'product.json'
$desktop = Join-Path $appRoot $desktopRel
$product = Join-Path $appRoot $productRel
$cursorExe = Join-Path $CursorInstallRoot 'Cursor.exe'

foreach ($path in @($desktop, $product, $cursorExe)) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Required Cursor file not found: $path"
    }
}

$cursorVersion = (Get-Item -LiteralPath $cursorExe).VersionInfo.FileVersion
if ($cursorVersion -ne '3.13.10') {
    throw "Unsupported Cursor version: $cursorVersion"
}

$menuMap = [ordered]@{
    'File' = @{ label = '\u6587\u4ef6'; mnemonic = 'F' }
    'Edit' = @{ label = '\u7f16\u8f91'; mnemonic = 'E' }
    'Selection' = @{ label = '\u9009\u62e9'; mnemonic = 'S' }
    'View' = @{ label = '\u67e5\u770b'; mnemonic = 'V' }
    'Go' = @{ label = '\u8f6c\u5230'; mnemonic = 'G' }
    'Terminal' = @{ label = '\u7ec8\u7aef'; mnemonic = 'T' }
    'Help' = @{ label = '\u5e2e\u52a9'; mnemonic = 'H' }
}

$text = [System.IO.File]::ReadAllText($desktop)
$planned = [ordered]@{}
$patterns = [ordered]@{}
foreach ($entry in $menuMap.GetEnumerator()) {
    $pattern = 'title:\{value:"[^"]*",original:"' +
        [regex]::Escape($entry.Key) +
        '",mnemonicTitle:(?:[A-Za-z_$][A-Za-z0-9_$]*\(\d+,null\)|"[^"]*")\}'
    $planned[$entry.Key] = ([regex]::Matches($text, $pattern)).Count
    $patterns[$entry.Key] = $pattern
}
$invalid = @($planned.GetEnumerator() | Where-Object Value -ne 1)
if ($invalid.Count -gt 0) {
    throw ('Pre-write gate failed: ' + (($invalid | ForEach-Object { "$($_.Key)=$($_.Value)" }) -join ', '))
}

$timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$backupRoot = Join-Path $OutputRoot "backup\cursor-app-resources-$timestamp"
foreach ($rel in @($desktopRel, $productRel)) {
    $source = Join-Path $appRoot $rel
    $target = Join-Path $backupRoot $rel
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $target) | Out-Null
    Copy-Item -LiteralPath $source -Destination $target -Force
}

foreach ($entry in $menuMap.GetEnumerator()) {
    $replacement = 'title:{value:"' + $entry.Value.label +
        '",original:"' + $entry.Key +
        '",mnemonicTitle:"' + $entry.Value.label + '(' + $entry.Value.mnemonic + ')"}'
    $text = [regex]::Replace($text, $patterns[$entry.Key], { param($match) $replacement }, 1)
}

$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
[System.IO.File]::WriteAllText($desktop, $text, $utf8NoBom)
$sha256 = [System.Security.Cryptography.SHA256]::Create()
try {
    $checksum = [Convert]::ToBase64String(
        $sha256.ComputeHash([System.IO.File]::ReadAllBytes($desktop))
    ).TrimEnd('=')
}
finally {
    $sha256.Dispose()
}

$productText = [System.IO.File]::ReadAllText($product)
$checksumPattern = '("vs/workbench/workbench\.desktop\.main\.js"\s*:\s*")[^"]+("\s*)'
$checksumCount = ([regex]::Matches($productText, $checksumPattern)).Count
if ($checksumCount -ne 1) {
    throw "Expected one desktop checksum entry, found $checksumCount"
}
$productText = [regex]::Replace(
    $productText,
    $checksumPattern,
    { param($match) $match.Groups[1].Value + $checksum + $match.Groups[2].Value },
    1
)
[System.IO.File]::WriteAllText($product, $productText, $utf8NoBom)

$verifyText = [System.IO.File]::ReadAllText($desktop)
$verification = foreach ($entry in $menuMap.GetEnumerator()) {
    $signature = 'original:"' + $entry.Key + '",mnemonicTitle:"' +
        $entry.Value.label + '(' + $entry.Value.mnemonic + ')"'
    $count = ([regex]::Matches($verifyText, [regex]::Escape($signature))).Count
    [pscustomobject]@{
        menu = $entry.Key
        chinese_signature_count = $count
        pass = ($count -eq 1)
    }
}

$report = [pscustomobject]@{
    timestamp = (Get-Date).ToString('o')
    cursor_version = $cursorVersion
    backup_root = $backupRoot
    prewrite_matches = $planned
    checksum_entry_count = $checksumCount
    checksum_sha256_base64_no_padding = $checksum
    verification = $verification
    overall_pass = -not ($verification.pass -contains $false)
    untouched = @('Kilo configuration','Claude Code configuration','DeepSeek configuration','API keys','Windows proxy/network settings')
}
New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null
$report | ConvertTo-Json -Depth 8 |
    Set-Content -LiteralPath (Join-Path $OutputRoot 'cursor-menubar-cn-patch-report.json') -Encoding UTF8
$report | ConvertTo-Json -Depth 8
if (-not $report.overall_pass) {
    throw 'Post-write verification failed'
}
