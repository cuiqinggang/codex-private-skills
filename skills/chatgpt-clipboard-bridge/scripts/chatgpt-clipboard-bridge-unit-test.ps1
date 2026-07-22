param(
    [string]$ScriptPath = (Join-Path $PSScriptRoot "chatgpt-clipboard-bridge.ps1")
)

$ErrorActionPreference = "Stop"

$resolvedScriptPath = (Resolve-Path -LiteralPath $ScriptPath)
$bytes = [System.IO.File]::ReadAllBytes($resolvedScriptPath)
if ($bytes.Length -lt 3 -or $bytes[0] -ne 0xEF -or $bytes[1] -ne 0xBB -or $bytes[2] -ne 0xBF) {
    throw "Bridge script must be UTF-8 with BOM so Windows PowerShell parses Chinese UI strings correctly."
}

$scriptText = [System.IO.File]::ReadAllText($resolvedScriptPath, [System.Text.Encoding]::UTF8)
$copyZh = -join ([char]0x590D, [char]0x5236)
$copyResponseZh = -join ([char]0x590D, [char]0x5236, [char]0x56DE, [char]0x590D)
$copyMessageZh = -join ([char]0x590D, [char]0x5236, [char]0x6D88, [char]0x606F)
$mojibakeCopy = -join ([char]0x6F6C, [char]0x5D76, [char]0x5D17, [char]0x57D7)

if (-not $scriptText.Contains($copyZh)) {
    throw "Bridge script must recognize Chinese ChatGPT copy buttons."
}

if ($scriptText.Contains($mojibakeCopy)) {
    throw "Bridge script contains mojibake in UI matching strings."
}

if (-not $scriptText.Contains($copyMessageZh)) {
    throw "Bridge script must explicitly distinguish user-message copy buttons from assistant-answer copy buttons."
}

if (-not $scriptText.Contains($copyResponseZh)) {
    throw "Bridge script must use assistant-answer copy buttons as the completion signal."
}

if ($scriptText -notmatch "\^\(复制\|复制回复\|Copy\|Copy response\)\$") {
    throw "Bridge script must recognize current ChatGPT answer copy button labels."
}

if ($scriptText -notmatch "InvokePattern") {
    throw "Bridge script must invoke UIA buttons directly before falling back to coordinate clicks."
}

if ($scriptText -notmatch "Clipboard\]::Clear") {
    throw "Bridge script must clear the clipboard without Set-Clipboard empty string."
}

if ($scriptText -match 'Get-Content\s+-Raw\s+-LiteralPath\s+\$PromptPath') {
    throw "Bridge script must read prompt files with explicit UTF-8 decoding, not Windows PowerShell default encoding."
}

if ($scriptText -notmatch "ReadAllText\(.+\[System\.Text\.Encoding\]::UTF8") {
    throw "Bridge script must use explicit UTF-8 when reading prompt files."
}

if ($scriptText -notmatch '\[string\]\$TaskId') {
    throw "Bridge script must accept or generate a TASK_ID."
}

if ($scriptText -notmatch "TASK_ID:") {
    throw "Bridge script must inject TASK_ID into the prompt sent to ChatGPT."
}

if ($scriptText -notmatch '\$answer\.Contains\(\$TaskId\)') {
    throw "Bridge script must stop when the copied answer does not contain TASK_ID."
}

if ($scriptText -notmatch "answer_raw\.md") {
    throw "Bridge script should save the raw ChatGPT answer as answer_raw.md by default."
}

if ($scriptText -notmatch '\[int\]\$CompletionGraceSec') {
    throw "Bridge script must support a completion grace wait for delayed Copy response buttons."
}

if ($scriptText -notmatch "Reveal-CopyResponseControls") {
    throw "Bridge script must try to reveal delayed Copy response controls without reading page text."
}

if ($scriptText -notmatch '\[switch\]\$OpenFreshWindow') {
    throw "Bridge script must support opening a fresh logged-in ChatGPT window."
}

if ($scriptText -notmatch '\[switch\]\$NoRealInput') {
    throw "Bridge script must support a no-real-mouse-keyboard mode."
}

if ($scriptText -notmatch '\[switch\]\$AllowRealInput') {
    throw "Bridge script must require explicit opt-in before using real Windows input."
}

if ($scriptText -notmatch '-not \[bool\]\$AllowRealInput') {
    throw "Bridge script must disable real Windows input by default."
}

if ($scriptText -notmatch '\[string\]\$TracePath') {
    throw "Bridge script must support a concise operation trace path."
}

if ($scriptText -notmatch "Open-FreshChatGptWindow") {
    throw "Bridge script must implement the fresh ChatGPT window path."
}

if ($scriptText -notmatch "Assert-RealInputAllowed") {
    throw "Bridge script must gate coordinate clicks behind an explicit real-input allowance."
}

if ($scriptText -notmatch "NoRealInput enabled and no semantic ChatGPT textbox was found") {
    throw "Bridge script must refuse coordinate input fallback in NoRealInput mode."
}

if ($scriptText -notmatch "ERROR:") {
    throw "Bridge script must record terminating errors in the operation trace."
}

if ($scriptText -notmatch '\$initialCopyButtons = @\(Get-CopyButtons \$root\)') {
    throw "Bridge script must preserve copy button collections when exactly one button exists."
}

if ($scriptText -match "CDP|page text|assistant message text|document\.body|innerText|OCR") {
    throw "Bridge script must not add CDP/OCR/page-text fallbacks."
}

Write-Host "[chatgpt-bridge-test] UI text encoding checks passed"
