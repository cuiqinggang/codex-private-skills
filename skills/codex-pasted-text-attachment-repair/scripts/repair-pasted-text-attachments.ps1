param(
  [switch]$Repair,
  [switch]$KeepTestFiles
)

$ErrorActionPreference = "Stop"

function Add-Result {
  param(
    $Results,
    [string]$Name,
    $Value
  )
  $Results[$Name] = $Value
}

function Test-WriteRead {
  param(
    [string]$Root,
    [switch]$Keep
  )

  $testDir = Join-Path $Root ("codex-paste-selftest-" + [guid]::NewGuid().ToString("N"))
  $testFile = Join-Path $testDir "pasted-text-test.txt"
  $payload = "codex pasted text attachment self-test " + (Get-Date).ToString("s")

  New-Item -ItemType Directory -Force -Path $testDir | Out-Null
  Set-Content -Path $testFile -Value $payload -Encoding UTF8
  $readBack = Get-Content -Path $testFile -Raw
  $ok = $readBack.Trim() -eq $payload

  if (-not $Keep) {
    Remove-Item -Path $testDir -Recurse -Force -ErrorAction SilentlyContinue
  }

  return @{
    ok = $ok
    testFile = $testFile
  }
}

function Test-NodeWriteRead {
  param(
    [string]$Root,
    [switch]$Keep
  )

  $node = Get-Command node -ErrorAction SilentlyContinue
  if ($null -eq $node) {
    return @{
      ok = $null
      skipped = $true
      reason = "node not found on PATH"
    }
  }

  $keepText = if ($Keep) { "true" } else { "false" }
  $script = @"
const fs = require("fs");
const path = require("path");
const root = process.env.CODEX_PASTE_ATTACHMENT_TEST_ROOT;
if (!root) {
  console.error("missing CODEX_PASTE_ATTACHMENT_TEST_ROOT");
  process.exit(3);
}
const dir = path.join(root, "codex-node-paste-selftest-" + Date.now());
const file = path.join(dir, "sample.txt");
const payload = "node attachment write ok " + new Date().toISOString();
fs.mkdirSync(dir, { recursive: true });
fs.writeFileSync(file, payload, "utf8");
const readBack = fs.readFileSync(file, "utf8");
if ($keepText !== true) fs.rmSync(dir, { recursive: true, force: true });
if (readBack !== payload) {
  console.error("readback mismatch");
  process.exit(2);
}
console.log(JSON.stringify({ ok: true, testFile: file }));
"@

  $oldRoot = $env:CODEX_PASTE_ATTACHMENT_TEST_ROOT
  $tempScript = Join-Path $env:TEMP ("codex-paste-attachment-test-" + [guid]::NewGuid().ToString("N") + ".js")
  try {
    $env:CODEX_PASTE_ATTACHMENT_TEST_ROOT = $Root
    Set-Content -Path $tempScript -Value $script -Encoding UTF8
    $output = & $node.Source $tempScript
    if ($LASTEXITCODE -ne 0) {
      return @{
        ok = $false
        skipped = $false
        output = ($output -join "`n")
      }
    }
  } finally {
    $env:CODEX_PASTE_ATTACHMENT_TEST_ROOT = $oldRoot
    Remove-Item -Path $tempScript -Force -ErrorAction SilentlyContinue
  }

  return @{
    ok = $true
    skipped = $false
    output = ($output -join "`n")
  }
}

$results = [ordered]@{}
$codexHome = if ($env:CODEX_HOME -and $env:CODEX_HOME.Trim().Length -gt 0) {
  $env:CODEX_HOME
} else {
  Join-Path $env:USERPROFILE ".codex"
}
$attachmentsRoot = Join-Path $codexHome "attachments"
$sentryScope = Join-Path $env:APPDATA "Codex\web\Codex\sentry\scope_v3.json"

Add-Result $results "codexHome" $codexHome
Add-Result $results "attachmentsRoot" $attachmentsRoot
Add-Result $results "repairRequested" ([bool]$Repair)
Add-Result $results "attachmentsRootExistsBefore" (Test-Path -Path $attachmentsRoot)

if (-not (Test-Path -Path $attachmentsRoot)) {
  if ($Repair) {
    New-Item -ItemType Directory -Force -Path $attachmentsRoot | Out-Null
  }
}

Add-Result $results "attachmentsRootExistsAfter" (Test-Path -Path $attachmentsRoot)

if (Test-Path -Path $attachmentsRoot) {
  $item = Get-Item -Path $attachmentsRoot
  Add-Result $results "attachmentsRootAttributes" $item.Attributes.ToString()
  try {
    Add-Result $results "acl" ((Get-Acl -Path $attachmentsRoot).AccessToString)
  } catch {
    Add-Result $results "aclError" $_.Exception.Message
  }

  try {
    Add-Result $results "powershellWriteRead" (Test-WriteRead -Root $attachmentsRoot -Keep:$KeepTestFiles)
  } catch {
    Add-Result $results "powershellWriteRead" @{
      ok = $false
      error = $_.Exception.Message
    }
  }

  try {
    Add-Result $results "nodeWriteRead" (Test-NodeWriteRead -Root $attachmentsRoot -Keep:$KeepTestFiles)
  } catch {
    Add-Result $results "nodeWriteRead" @{
      ok = $false
      error = $_.Exception.Message
    }
  }
}

if (Test-Path -Path $sentryScope) {
  try {
    $matches = Select-String -Path $sentryScope -Pattern "Failed to load pasted text excerpts","Pasted text attachment","create-pasted-text-attachment","os error 3" -SimpleMatch -ErrorAction Stop
    Add-Result $results "recentPastedTextLogHints" (@($matches).Count)
  } catch {
    Add-Result $results "recentPastedTextLogHintsError" $_.Exception.Message
  }
} else {
  Add-Result $results "sentryScopeExists" $false
}

$results | ConvertTo-Json -Depth 8
