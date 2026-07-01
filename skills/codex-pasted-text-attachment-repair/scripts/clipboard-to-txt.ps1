param(
    [string]$OutputDirectory = "$env:USERPROFILE\.codex\manual-paste-attachments",
    [string]$Prefix = "codex-pasted-text"
)

$ErrorActionPreference = "Stop"

New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null

$text = Get-Clipboard -Raw -Format Text
if ([string]::IsNullOrWhiteSpace($text)) {
    throw "Clipboard has no text. Copy long text first, then run this script."
}

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$fileName = "$Prefix-$timestamp.txt"
$path = Join-Path $OutputDirectory $fileName

[System.IO.File]::WriteAllText($path, $text, [System.Text.UTF8Encoding]::new($false))
Set-Clipboard -Value $path

[pscustomobject]@{
    status = "OK"
    file = $path
    chars = $text.Length
    bytes = (Get-Item -LiteralPath $path).Length
    copiedToClipboard = $true
    nextStep = "Attach the generated .txt file in Codex. The file path has been copied to clipboard."
} | ConvertTo-Json -Depth 4
