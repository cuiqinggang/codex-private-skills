param(
  [string]$KeybindingsPath = "$env:APPDATA\Cursor\User\keybindings.json"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function ConvertTo-HashtableArray {
  param([object[]]$Items)
  $out = @()
  foreach ($item in $Items) {
    $h = [ordered]@{}
    foreach ($prop in $item.PSObject.Properties) {
      $h[$prop.Name] = $prop.Value
    }
    $out += [pscustomobject]$h
  }
  return $out
}

$dir = Split-Path -Parent $KeybindingsPath
New-Item -ItemType Directory -Force -Path $dir | Out-Null

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
if (Test-Path -LiteralPath $KeybindingsPath) {
  Copy-Item -LiteralPath $KeybindingsPath -Destination "$KeybindingsPath.bak-$timestamp" -Force
  $raw = Get-Content -LiteralPath $KeybindingsPath -Raw
  if ([string]::IsNullOrWhiteSpace($raw)) {
    $entries = @()
  } else {
    $parsed = $raw | ConvertFrom-Json
    if ($parsed -is [array]) {
      $entries = @(ConvertTo-HashtableArray -Items $parsed)
    } else {
      throw "keybindings.json must contain a JSON array."
    }
  }
} else {
  $entries = @()
}

$required = @(
  [pscustomobject]@{
    key = "ctrl+v"
    command = "workbench.action.terminal.paste"
    when = "terminalFocus && terminalProcessSupported"
  },
  [pscustomobject]@{
    key = "shift+insert"
    command = "workbench.action.terminal.paste"
    when = "terminalFocus && terminalProcessSupported"
  }
)

foreach ($item in $required) {
  $exists = $false
  foreach ($entry in $entries) {
    if ($entry.key -eq $item.key -and $entry.command -eq $item.command -and $entry.when -eq $item.when) {
      $exists = $true
      break
    }
  }
  if (-not $exists) {
    $entries += $item
  }
}

$json = $entries | ConvertTo-Json -Depth 10
Set-Content -LiteralPath $KeybindingsPath -Value $json -Encoding UTF8

$null = Get-Content -LiteralPath $KeybindingsPath -Raw | ConvertFrom-Json
[pscustomobject]@{
  Status = "TERMINAL_PASTE_KEYBINDINGS_WRITTEN"
  Path = $KeybindingsPath
  Entries = @($entries).Count
  Backup = if (Test-Path -LiteralPath "$KeybindingsPath.bak-$timestamp") { "$KeybindingsPath.bak-$timestamp" } else { "" }
}
