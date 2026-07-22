param(
    [string]$Workspace = (Get-Location).Path,
    [int]$TcpTimeoutMs = 2000
)

$ErrorActionPreference = "Stop"

function Add-Result {
    param([string]$Check, [string]$Status, [string]$Detail)
    [PSCustomObject]@{ Check = $Check; Status = $Status; Detail = $Detail }
}

function Test-Command {
    param([string]$Name)
    if (Get-Command $Name -ErrorAction SilentlyContinue) { "present" } else { "missing" }
}

function Test-TcpPortQuick {
    param([string]$HostName, [int]$Port, [int]$TimeoutMs)
    $client = New-Object System.Net.Sockets.TcpClient
    try {
        $async = $client.BeginConnect($HostName, $Port, $null, $null)
        if (-not $async.AsyncWaitHandle.WaitOne($TimeoutMs, $false)) { return $false }
        $client.EndConnect($async) | Out-Null
        return $true
    } catch {
        return $false
    } finally {
        $client.Close()
    }
}

$Workspace = (Resolve-Path -LiteralPath $Workspace).Path
$results = @()

Push-Location $Workspace
try {
    $results += Add-Result "Workspace" "PASS" $Workspace

    if (Test-Path -LiteralPath ".git") {
        $tracked = (& git ls-files | Measure-Object).Count
        $status = (& git status --short | Select-Object -First 20) -join "; "
        if (-not $status) { $status = "clean or all files ignored" }
        $results += Add-Result "Git" "PASS" "tracked=$tracked; status=$status"

        $exclude = Join-Path $Workspace ".git\info\exclude"
        if (Test-Path -LiteralPath $exclude) {
            $blanket = Select-String -LiteralPath $exclude -Pattern '^\*$' -Quiet
            $allowlistCount = (Select-String -LiteralPath $exclude -Pattern '^!' | Measure-Object).Count
            $status = if ($blanket -and $allowlistCount -eq 0) { "WARN" } else { "PASS" }
            $results += Add-Result "GitIgnoreLocal" $status "blanket_ignore=$blanket; allowlist_entries=$allowlistCount; source=$exclude"
        }
    } else {
        $results += Add-Result "Git" "WARN" "no .git directory"
    }

    $manifestPatterns = @("package.json","pyproject.toml","requirements*.txt","pytest.ini","tsconfig.json","go.mod","Cargo.toml","CMakeLists.txt","CMakePresets.json")
    $manifests = foreach ($pattern in $manifestPatterns) {
        Get-ChildItem -LiteralPath $Workspace -Filter $pattern -File -ErrorAction SilentlyContinue
    }
    $results += Add-Result "RootManifests" ($(if ($manifests.Count) { "PASS" } else { "WARN" })) (($manifests | ForEach-Object Name) -join ", ")

    $pyFiles = @()
    $pyFiles += Get-ChildItem -LiteralPath $Workspace -Filter "*.py" -File -ErrorAction SilentlyContinue
    $scriptsDir = Join-Path $Workspace "scripts"
    if (Test-Path -LiteralPath $scriptsDir) {
        $pyFiles += Get-ChildItem -LiteralPath $scriptsDir -Filter "*.py" -File -ErrorAction SilentlyContinue
    }
    if ($pyFiles.Count) {
        $code = @"
import ast, pathlib, sys
errors = []
for item in sys.argv[1:]:
    p = pathlib.Path(item)
    try:
        ast.parse(p.read_text(encoding='utf-8-sig'), filename=str(p))
    except Exception as exc:
        errors.append(f"{p}|{type(exc).__name__}|{exc}")
print(f"files={len(sys.argv)-1}; errors={len(errors)}")
for err in errors:
    print(err)
sys.exit(1 if errors else 0)
"@
        $tmp = New-TemporaryFile
        Set-Content -LiteralPath $tmp -Value $code -Encoding UTF8
        $out = & python $tmp @($pyFiles.FullName) 2>&1
        Remove-Item -LiteralPath $tmp -Force
        $results += Add-Result "PythonAST" ($(if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" })) ($out -join " ")
    }

    $psFiles = @()
    $psFiles += Get-ChildItem -LiteralPath $Workspace -Filter "*.ps1" -File -ErrorAction SilentlyContinue
    if (Test-Path -LiteralPath $scriptsDir) {
        $psFiles += Get-ChildItem -LiteralPath $scriptsDir -Filter "*.ps1" -File -ErrorAction SilentlyContinue
    }
    $parseErrors = @()
    foreach ($f in $psFiles) {
        $tokens = $null; $errors = $null
        [System.Management.Automation.Language.Parser]::ParseFile($f.FullName, [ref]$tokens, [ref]$errors) | Out-Null
        if ($errors.Count) { $parseErrors += "$($f.Name): $(($errors | ForEach-Object Message) -join '; ')" }
    }
    $results += Add-Result "PowerShellParse" ($(if ($parseErrors.Count) { "FAIL" } else { "PASS" })) "files=$($psFiles.Count); errors=$($parseErrors.Count)"

    $healthScript = Join-Path $Workspace "health-check-20s.ps1"
    if (Test-Path -LiteralPath $healthScript) {
        $out = & powershell -ExecutionPolicy Bypass -File $healthScript -TcpTimeoutMs $TcpTimeoutMs 2>&1
        $results += Add-Result "ExistingHealthScript" ($(if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" })) (($out | Select-Object -Last 4) -join " ")
    }

    $tools = "python=$(Test-Command python); node=$(Test-Command node); npm=$(Test-Command npm); cmake=$(Test-Command cmake); poetry=$(Test-Command poetry); pip-audit=$(Test-Command pip-audit)"
    $results += Add-Result "Tools" "PASS" $tools

    $secretFiles = Get-ChildItem -LiteralPath $Workspace -Recurse -File -Force -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -match '(secret|token|key|credential|password|passwd|\.env)' } |
        Select-Object -First 30 -ExpandProperty FullName
    $results += Add-Result "SecretLikeNames" ($(if ($secretFiles.Count) { "WARN" } else { "PASS" })) "count=$($secretFiles.Count); contents_not_read"

    $tcp443 = Test-TcpPortQuick -HostName "openai.com" -Port 443 -TimeoutMs $TcpTimeoutMs
    $results += Add-Result "TCP443" ($(if ($tcp443) { "PASS" } else { "FAIL" })) "openai.com:443 reachable=$tcp443"
} finally {
    Pop-Location
}

Write-Host "=== Weekly Project Health Check ==="
$results | Format-Table -AutoSize
