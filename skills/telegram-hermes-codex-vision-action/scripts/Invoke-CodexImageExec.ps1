[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$RepoPath,

    [Parameter(Mandatory = $true)]
    [string]$Task,

    [Parameter(Mandatory = $true)]
    [string[]]$ImagePaths,

    [string]$TaskId,
    [string]$OutputRoot,
    [string]$CodexCommand = "codex",
    [int]$TimeoutSec = 900,
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$script:OutDir = $null

function Redact-SecretText {
    param([AllowNull()][string]$Text)
    if ($null -eq $Text) { return "" }
    $redacted = $Text -replace '([0-9]{8,12}:[A-Za-z0-9_-]{20,})', '<REDACTED_TELEGRAM_TOKEN>'
    $redacted = $redacted -replace '(sk-[A-Za-z0-9_-]{10,})', '<REDACTED_API_KEY>'
    return $redacted
}

function Write-TaskFailure {
    param(
        [string]$Code,
        [string]$Message
    )
    $safeMessage = Redact-SecretText $Message
    if ($script:OutDir -and (Test-Path -LiteralPath $script:OutDir)) {
        $resultPath = Join-Path $script:OutDir "result.txt"
        @(
            $Code
            $safeMessage
        ) | Set-Content -LiteralPath $resultPath -Encoding UTF8
    }
    throw "$Code $safeMessage"
}

function Resolve-ExistingPath {
    param(
        [string]$Path,
        [string]$Code
    )
    if (-not (Test-Path -LiteralPath $Path)) {
        Write-TaskFailure -Code $Code -Message "Missing path: $Path"
    }
    return (Resolve-Path -LiteralPath $Path).ProviderPath
}

function New-SafeTaskId {
    param([string]$Prefix)
    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $short = [guid]::NewGuid().ToString("N").Substring(0, 8)
    return "$Prefix-$stamp-$short"
}

function Normalize-TaskId {
    param([string]$Value, [string]$Prefix)
    if ([string]::IsNullOrWhiteSpace($Value)) {
        $Value = New-SafeTaskId -Prefix $Prefix
    }
    $safe = $Value -replace '[^A-Za-z0-9_.-]', '-'
    if ([string]::IsNullOrWhiteSpace($safe)) {
        Write-TaskFailure -Code "STOP_TASK_ID_INVALID" -Message "TaskId is empty after sanitizing."
    }
    return $safe
}

function ConvertTo-ProcessArguments {
    param([string[]]$Arguments)
    $quoted = foreach ($arg in $Arguments) {
        $value = [string]$arg
        if ($value.Length -eq 0) {
            '""'
        } elseif ($value -notmatch '[\s"]') {
            $value
        } else {
            '"' + ($value -replace '"', '\"') + '"'
        }
    }
    return ($quoted -join " ")
}

function Invoke-ExternalProcess {
    param(
        [string]$FilePath,
        [string[]]$Arguments,
        [string]$WorkingDirectory,
        [int]$TimeoutSec
    )

    $psi = [System.Diagnostics.ProcessStartInfo]::new()
    $psi.FileName = $FilePath
    $psi.WorkingDirectory = $WorkingDirectory
    $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.Arguments = ConvertTo-ProcessArguments -Arguments $Arguments

    $process = [System.Diagnostics.Process]::new()
    $process.StartInfo = $psi
    try {
        [void]$process.Start()
    } catch {
        return [pscustomobject]@{
            TimedOut = $false
            ExitCode = -1
            StdOut = ""
            StdErr = $_.Exception.Message
        }
    }

    $completed = $process.WaitForExit($TimeoutSec * 1000)
    if (-not $completed) {
        try { $process.Kill() } catch {}
        return [pscustomobject]@{
            TimedOut = $true
            ExitCode = -1
            StdOut = Redact-SecretText $process.StandardOutput.ReadToEnd()
            StdErr = "Timed out after $TimeoutSec seconds."
        }
    }

    return [pscustomobject]@{
        TimedOut = $false
        ExitCode = $process.ExitCode
        StdOut = Redact-SecretText $process.StandardOutput.ReadToEnd()
        StdErr = Redact-SecretText $process.StandardError.ReadToEnd()
    }
}

$repo = Resolve-ExistingPath -Path $RepoPath -Code "STOP_REPO_MISSING"
$gitPath = Join-Path $repo ".git"
if (-not (Test-Path -LiteralPath $gitPath)) {
    Write-TaskFailure -Code "STOP_REPO_GIT_MISSING" -Message "RepoPath must contain .git: $repo"
}

if ([string]::IsNullOrWhiteSpace($Task)) {
    Write-TaskFailure -Code "STOP_TASK_EMPTY" -Message "Task cannot be empty."
}

$allowedImageExtensions = @(".png", ".jpg", ".jpeg", ".webp")
$resolvedImages = New-Object System.Collections.Generic.List[string]
foreach ($imagePath in $ImagePaths) {
    $resolved = Resolve-ExistingPath -Path $imagePath -Code "STOP_IMAGE_MISSING"
    $ext = [System.IO.Path]::GetExtension($resolved).ToLowerInvariant()
    if ($allowedImageExtensions -notcontains $ext) {
        Write-TaskFailure -Code "STOP_IMAGE_TYPE_UNSUPPORTED" -Message "Unsupported image extension '$ext' for $resolved"
    }
    [void]$resolvedImages.Add($resolved)
}

if ($resolvedImages.Count -eq 0) {
    Write-TaskFailure -Code "STOP_IMAGE_EMPTY" -Message "At least one image is required."
}

$safeTaskId = Normalize-TaskId -Value $TaskId -Prefix "TGIMG"
if ([string]::IsNullOrWhiteSpace($OutputRoot)) {
    $OutputRoot = Join-Path $repo "output"
}
New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null
$script:OutDir = Join-Path $OutputRoot "CODEX-TELEGRAM-VISION-$safeTaskId"
New-Item -ItemType Directory -Force -Path $script:OutDir | Out-Null

$taskPath = Join-Path $script:OutDir "task.txt"
$resultPath = Join-Path $script:OutDir "result.txt"
$manifestPath = Join-Path $script:OutDir "media-manifest.json"
$commandPath = Join-Path $script:OutDir "codex-command.json"

$Task | Set-Content -LiteralPath $taskPath -Encoding UTF8

$media = foreach ($image in $resolvedImages) {
    $item = Get-Item -LiteralPath $image
    [pscustomobject]@{
        type = "image"
        path = $item.FullName
        name = $item.Name
        extension = $item.Extension.ToLowerInvariant()
        length = $item.Length
        sha256 = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash
    }
}

$manifest = [pscustomobject]@{
    taskId = $safeTaskId
    kind = "image"
    repoPath = $repo
    outputDir = $script:OutDir
    createdAt = (Get-Date).ToString("o")
    dryRun = [bool]$DryRun
    media = @($media)
}
$manifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $manifestPath -Encoding UTF8

$codexArgs = New-Object System.Collections.Generic.List[string]
foreach ($image in $resolvedImages) {
    [void]$codexArgs.Add("--image")
    [void]$codexArgs.Add($image)
}
[void]$codexArgs.Add($Task)

[pscustomobject]@{
    command = $CodexCommand
    args = @($codexArgs)
    workingDirectory = $repo
    timeoutSec = $TimeoutSec
    dryRun = [bool]$DryRun
} | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $commandPath -Encoding UTF8

if ($DryRun) {
    @(
        "DRY_RUN_NO_CODEX_INVOCATION"
        "taskId=$safeTaskId"
        "imageCount=$($resolvedImages.Count)"
        "outputDir=$script:OutDir"
    ) | Set-Content -LiteralPath $resultPath -Encoding UTF8
    [pscustomobject]@{
        status = "DRY_RUN_NO_CODEX_INVOCATION"
        taskId = $safeTaskId
        outputDir = $script:OutDir
        resultPath = $resultPath
        mediaCount = $resolvedImages.Count
    } | ConvertTo-Json -Compress
    return
}

$run = Invoke-ExternalProcess -FilePath $CodexCommand -Arguments @($codexArgs) -WorkingDirectory $repo -TimeoutSec $TimeoutSec
$resultLines = @(
    "CODEX_EXIT_CODE=$($run.ExitCode)"
    "CODEX_TIMED_OUT=$($run.TimedOut)"
    ""
    "STDOUT:"
    $run.StdOut
    ""
    "STDERR:"
    $run.StdErr
)
$resultLines | Set-Content -LiteralPath $resultPath -Encoding UTF8

if ($run.TimedOut) {
    Write-TaskFailure -Code "STOP_CODEX_TIMEOUT" -Message "Codex timed out after $TimeoutSec seconds. Result: $resultPath"
}
if ($run.ExitCode -ne 0) {
    Write-TaskFailure -Code "STOP_CODEX_FAILED" -Message "Codex exited with $($run.ExitCode). Result: $resultPath"
}

[pscustomobject]@{
    status = "CODEX_IMAGE_EXEC_PASS"
    taskId = $safeTaskId
    outputDir = $script:OutDir
    resultPath = $resultPath
    mediaCount = $resolvedImages.Count
} | ConvertTo-Json -Compress
