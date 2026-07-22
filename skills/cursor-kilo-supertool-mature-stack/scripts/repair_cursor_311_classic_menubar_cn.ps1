param(
    [string]$OutputRoot = "$env:USERPROFILE\Documents\Codex\Cursor-Kilo-Localization-Repair-Latest"
)

$ErrorActionPreference = 'Stop'
${REDACTED_SECRET}
$desktopRel = 'out\vs\workbench\workbench.desktop.main.js'
$glassRel = 'out\vs\workbench\workbench.glass.main.js'
$productRel = 'product.json'
$desktop = Join-Path $appRoot $desktopRel
$glass = Join-Path $appRoot $glassRel
$product = Join-Path $appRoot $productRel

foreach ($path in @($desktop, $glass, $product)) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Required Cursor resource not found: $path"
    }
}

$timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$backupRoot = Join-Path $OutputRoot "backup\cursor-app-resources-$timestamp"
$evidenceRoot = Join-Path $OutputRoot 'evidence'
New-Item -ItemType Directory -Path $backupRoot, $evidenceRoot -Force | Out-Null

foreach ($rel in @($desktopRel, $glassRel, $productRel)) {
    $source = Join-Path $appRoot $rel
    $target = Join-Path $backupRoot $rel
    New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force | Out-Null
    Copy-Item -LiteralPath $source -Destination $target -Force
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

$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
$fileResults = @()
foreach ($path in @($desktop)) {
    $text = [System.IO.File]::ReadAllText($path)
    $replacements = [ordered]@{}
    foreach ($entry in $menuMap.GetEnumerator()) {
        $original = $entry.Key
        $label = $entry.Value.label
        $mnemonic = $entry.Value.mnemonic
        $pattern = 'title:\{value:"[^"]*",original:"' + [regex]::Escape($original) + '",mnemonicTitle:(?:S\(\d+,null\)|"[^"]*")\}'
        $replacement = 'title:{value:"' + $label + '",original:"' + $original + '",mnemonicTitle:"' + $label + '(' + $mnemonic + ')"}'
        $count = ([regex]::Matches($text, $pattern)).Count
        if ($count -gt 0) {
            $text = [regex]::Replace($text, $pattern, { param($m) $replacement })
        }
        $replacements[$original] = $count
    }
    [System.IO.File]::WriteAllText($path, $text, $utf8NoBom)
    $fileResults += [pscustomobject]@{
        path = $path
        replacements = $replacements
    }
}

$sha256 = [System.Security.Cryptography.SHA256]::Create()
try {
    $hashBytes = $sha256.ComputeHash([System.IO.File]::ReadAllBytes($desktop))
} finally {
    $sha256.Dispose()
}
$checksum = [Convert]::ToBase64String($hashBytes).TrimEnd('=')

$productText = [System.IO.File]::ReadAllText($product)
$checksumPattern = '("vs/workbench/workbench\.desktop\.main\.js"\s*:\s*")[^"]+("\s*)'
$checksumMatches = [regex]::Matches($productText, $checksumPattern).Count
if ($checksumMatches -ne 1) {
    throw "Expected one desktop checksum entry in product.json, found $checksumMatches"
}
$productText = [regex]::Replace(
    $productText,
    $checksumPattern,
    { param($m) $m.Groups[1].Value + $checksum + $m.Groups[2].Value },
    1
)
[System.IO.File]::WriteAllText($product, $productText, $utf8NoBom)

$verification = @()
foreach ($path in @($desktop)) {
    $text = [System.IO.File]::ReadAllText($path)
    foreach ($entry in $menuMap.GetEnumerator()) {
        $englishSignature = 'original:"' + $entry.Key + '",mnemonicTitle:S('
        $chineseSignature = 'original:"' + $entry.Key + '",mnemonicTitle:"' + $entry.Value.label + '(' + $entry.Value.mnemonic + ')"'
        $englishCount = ([regex]::Matches($text, [regex]::Escape($englishSignature))).Count
        $chineseCount = ([regex]::Matches($text, [regex]::Escape($chineseSignature))).Count
        $verification += [pscustomobject]@{
            path = $path
            menu = $entry.Key
            english_signature_count = $englishCount
            chinese_signature_count = $chineseCount
            pass = ($englishCount -eq 0 -and $chineseCount -ge 1)
        }
    }
}

${REDACTED_SECRET}
$report = [pscustomobject]@{
    timestamp = (Get-Date).ToString('o')
    cursor_version = $cursorVersion
    output_root = $OutputRoot
    backup_root = $backupRoot
    files = $fileResults
    desktop_checksum_sha256_base64_no_padding = $checksum
    verification = $verification
    overall_pass = -not ($verification.pass -contains $false)
    untouched = @(
${REDACTED_SECRET}
${REDACTED_SECRET}
        'API keys',
        'Windows proxy/network settings'
    )
}

$reportPath = Join-Path $OutputRoot 'cursor-menubar-cn-patch-report.json'
$report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $reportPath -Encoding utf8
$report | ConvertTo-Json -Depth 8
