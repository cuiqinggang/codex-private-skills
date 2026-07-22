[CmdletBinding()]
param(
  [string]$CodexHome = (Join-Path $env:USERPROFILE '.codex'),
  [string]$PluginVersion = '26.602.40724',
  [switch]$VerifyOnly
)

$ErrorActionPreference = 'Stop'
$LogPrefix = '[codex-computer-use-native-pipe-fallback]'

function Write-Log {
  param([string]$Message)
  Write-Host "$LogPrefix $Message"
}

function Resolve-ExistingFile {
  param([string]$Path)
  if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
    throw "missing required file: $Path"
  }
  return (Resolve-Path -LiteralPath $Path).Path
}

function Assert-UnderPath {
  param(
    [string]$Path,
    [string]$Parent
  )
  $full = [System.IO.Path]::GetFullPath($Path)
  $root = [System.IO.Path]::GetFullPath($Parent).TrimEnd('\') + '\'
  if (-not $full.StartsWith($root, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "refusing to modify path outside expected root: $full"
  }
}

function Backup-FileOnce {
  param([string]$Path)
  $backupRoot = Join-Path $CodexHome 'backups\computer-use-native-pipe-fallback'
  New-Item -ItemType Directory -Force -Path $backupRoot | Out-Null
  $stamp = Get-Date -Format 'yyyyMMdd-HHmmss-fff'
  $leaf = Split-Path -Leaf $Path
  $backup = Join-Path $backupRoot "$leaf.$stamp.bak"
  Copy-Item -LiteralPath $Path -Destination $backup -Force
  Write-Log "backup: $backup"
}

function Test-PatchedClient {
  param([string]$Path)
  $text = Get-Content -LiteralPath $Path -Raw
  return (
    $text.Contains('function discoverComputerUsePipePath()') -and
    $text.Contains('function createNativePipeConnection(pipePath)') -and
    $text.Contains('codex-computer-use-*')
  )
}

function Patch-Client {
  param([string]$Path)

  Resolve-ExistingFile $Path | Out-Null
  if (Test-PatchedClient $Path) {
    Write-Log "already patched: $Path"
    return
  }
  if ($VerifyOnly) {
    throw "native pipe fallback is missing from $Path"
  }

  Backup-FileOnce $Path
  $text = Get-Content -LiteralPath $Path -Raw

  if (-not $text.Contains('import { execFileSync } from "node:child_process";')) {
    $text = $text.Replace(
      'import { Buffer } from "node:buffer";',
      "import { Buffer } from `"node:buffer`";`r`nimport { execFileSync } from `"node:child_process`";`r`nimport { connect } from `"node:net`";"
    )
  }

  $oldCreate = @'
    const nativePipe = globalThis.nodeRepl?.nativePipe;
    if (
      nativePipe == null ||
      typeof nativePipe.createConnection !== "function"
    ) {
      throw new Error("Computer Use native pipe is unavailable");
    }

    const pipePath = getComputerUsePipePath();
    let transport = null;
    try {
      const socket = await nativePipe.createConnection(pipePath);
'@
  $newCreate = @'
    const pipePath = getComputerUsePipePath();
    let transport = null;
    try {
      const socket = await createNativePipeConnection(pipePath);
'@
  if ($text.Contains($oldCreate)) {
    $text = $text.Replace($oldCreate, $newCreate)
  }

  if (-not $text.Contains('function createNativePipeConnection(pipePath)')) {
    $insert = @'

function createNativePipeConnection(pipePath) {
  const nativePipe = globalThis.nodeRepl?.nativePipe;
  if (nativePipe != null && typeof nativePipe.createConnection === "function") {
    return nativePipe.createConnection(pipePath);
  }
  return connect(pipePath);
}
'@
    $text = $text.Replace("`r`nfunction getComputerUsePipePath() {", "$insert`r`nfunction getComputerUsePipePath() {")
  }

  $oldThrow = @'

  throw new Error("Computer Use native pipe path is unavailable");
}
'@
  $newThrow = @'

  const discovered = discoverComputerUsePipePath();
  if (discovered) {
    return discovered;
  }

  throw new Error("Computer Use native pipe path is unavailable");
}

function discoverComputerUsePipePath() {
  if (platform() !== "win32") {
    return null;
  }
  try {
    const output = execFileSync(
      "powershell.exe",
      [
        "-NoProfile",
        "-NonInteractive",
        "-Command",
        "(Get-ChildItem -LiteralPath '\\.\pipe\' | Where-Object { $_.Name -like 'codex-computer-use-*' } | Select-Object -First 1 -ExpandProperty FullName)",
      ],
      { encoding: "utf8", windowsHide: true },
    ).trim();
    return output || null;
  } catch {
    return null;
  }
}
'@
  if ($text.Contains($oldThrow)) {
    $text = $text.Replace($oldThrow, $newThrow)
  }

  $encoding = [System.Text.UTF8Encoding]::new($false)
  [System.IO.File]::WriteAllText($Path, $text, $encoding)

  if (-not (Test-PatchedClient $Path)) {
    throw "patch did not apply cleanly: $Path"
  }
  Write-Log "patched: $Path"
}

$cacheClient = Join-Path $CodexHome "plugins\cache\openai-bundled\computer-use\$PluginVersion\scripts\computer-use-client.mjs"
$mirrorClient = Join-Path $CodexHome '.tmp\bundled-marketplaces\openai-bundled\plugins\computer-use\scripts\computer-use-client.mjs'

Assert-UnderPath $cacheClient (Join-Path $CodexHome 'plugins\cache\openai-bundled\computer-use')
Assert-UnderPath $mirrorClient (Join-Path $CodexHome '.tmp\bundled-marketplaces\openai-bundled\plugins\computer-use')

Patch-Client $cacheClient
if (Test-Path -LiteralPath $mirrorClient -PathType Leaf) {
  Patch-Client $mirrorClient
} else {
  Write-Log "mirror client not present, skipped: $mirrorClient"
}

Write-Log 'native pipe fallback verification ok'
