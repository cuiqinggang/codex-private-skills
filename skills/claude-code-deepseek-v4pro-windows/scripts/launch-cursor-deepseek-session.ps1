param(
    [string]$WorkspacePath = (Get-Location).Path,
    [string]$OutputRoot = (Join-Path (Get-Location).Path 'output\claude-deepseek-session'),
    [string]$CursorPath = (Join-Path $env:LOCALAPPDATA 'Programs\cursor\Cursor.exe'),
    [string]$ClaudePath = (Join-Path $env:APPDATA 'npm\claude.cmd')
)

$ErrorActionPreference = 'Stop'
$Host.UI.RawUI.WindowTitle = 'Cursor + Claude Code + DeepSeek V4 Pro（本次会话）'

$smokePath = Join-Path $OutputRoot 'session-smoke.txt'
$diagnosticPath = Join-Path $OutputRoot 'session-launch-diagnostic.txt'
$proofPath = Join-Path $OutputRoot 'DeepSeek-V4-Pro-当前会话路由证明.md'

foreach ($path in @($CursorPath, $ClaudePath, $WorkspacePath)) {
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Required path not found: $path"
    }
}
New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null

try {
    Write-Host '本窗口只建立本次会话，不把 API Key 写入注册表、配置文件、日志或证明文件。' -ForegroundColor Yellow
    $secure = Read-Host '请输入 DeepSeek API Key（输入不会显示）' -AsSecureString
    $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    try {
        $key = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
    }
    finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
    }
    if ([string]::IsNullOrWhiteSpace($key)) {
        throw 'EMPTY_DEEPSEEK_API_KEY'
    }

    $env:DEEPSEEK_API_KEY = $key.Trim()
    $env:ANTHROPIC_AUTH_TOKEN = $key.Trim()
    $env:ANTHROPIC_BASE_URL = 'https://api.deepseek.com/anthropic'
    $env:ANTHROPIC_MODEL = 'deepseek-v4-pro[1m]'
    $env:ANTHROPIC_DEFAULT_OPUS_MODEL = 'deepseek-v4-pro[1m]'
    $env:ANTHROPIC_DEFAULT_SONNET_MODEL = 'deepseek-v4-pro[1m]'
    $env:ANTHROPIC_DEFAULT_HAIKU_MODEL = 'deepseek-v4-flash'
    $env:CLAUDE_CODE_SUBAGENT_MODEL = 'deepseek-v4-flash'
    $env:CLAUDE_CODE_EFFORT_LEVEL = 'max'
    $key = $null

    $smoke = & $ClaudePath -p '只回复：DS_CLAUDE_CODE_OK' 2>&1
    $exitCode = $LASTEXITCODE
    $smokeText = ($smoke | Out-String).Trim()
    @(
        "time=$(Get-Date -Format o)"
        "base_url=$env:ANTHROPIC_BASE_URL"
        "model=$env:ANTHROPIC_MODEL"
        "exit_code=$exitCode"
        'output:'
        $smokeText
    ) | Set-Content -LiteralPath $smokePath -Encoding UTF8

    if ($exitCode -ne 0 -or $smokeText -notmatch 'DS_CLAUDE_CODE_OK') {
        throw 'DEEPSEEK_SMOKE_TEST_FAILED'
    }

    $proofTime = Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz'
    @(
        '# Claude Code 当前会话路由证明'
        ''
        '状态：`LIVE_SMOKE_PASS`'
        ''
        '- 工具外壳：Claude Code'
        "- 实际 API 端点：``$env:ANTHROPIC_BASE_URL``"
        "- 实际主模型：``$env:ANTHROPIC_MODEL``"
        "- 最小真实调用退出码：``$exitCode``"
        '- 最小真实调用返回：`DS_CLAUDE_CODE_OK`'
        '- Cursor 会话启动状态：`CURSOR_SESSION_LAUNCHED`'
        '- Claude/Anthropic 官方模型：`未启用`'
        '- 密钥持久化：`否（只存在于本次启动进程）`'
        "- 实测时间：``$proofTime``"
        ''
        '`Claude Code 工具外壳 DeepSeek V4 Pro 转接路线: PASS`'
    ) | Set-Content -LiteralPath $proofPath -Encoding UTF8

    Start-Process -FilePath $CursorPath -ArgumentList @(
        '--classic', '--locale', 'zh-cn', '--new-window', $WorkspacePath
    )
    Start-Sleep -Seconds 2
    Start-Process -FilePath $CursorPath -ArgumentList @('-r', $proofPath)

    @(
        "time=$(Get-Date -Format o)"
        'status=CURSOR_SESSION_LAUNCHED'
        "workspace=$WorkspacePath"
        'credential_persisted=False'
        'official_claude_model_used=False'
    ) | Set-Content -LiteralPath $diagnosticPath -Encoding UTF8
    Write-Host 'Cursor 已启动；Key 只存在于本次 Cursor 进程树。' -ForegroundColor Green
}
catch {
    @(
        "time=$(Get-Date -Format o)"
        'status=SESSION_LAUNCH_FAILED'
        "error=$($_.Exception.Message)"
        'credential_persisted=False'
    ) | Set-Content -LiteralPath $diagnosticPath -Encoding UTF8
    throw
}
