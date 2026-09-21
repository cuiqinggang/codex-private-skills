# 【Qwen3.8/Bonsai2-27B｜Runtime R1 60秒现实验证｜3｜现实验证】
# CURRENT_STEP=3
# DESIGN_FROZEN=YES
# ONLY_CANDIDATE=R1_SAME_RELEASE_CPU_BACKEND_GRAFT
# T_VALID_GATE_MS=60000
# 禁止现场编译、禁止模型下载、禁止切 R2/R3、禁止修改代理/网络设置。

$ErrorActionPreference = 'Stop'

$RuntimeDir = 'C:\AI\Bonsai2-27B-256K\Bonsai-demo\bin\cuda'
$Server = Join-Path $RuntimeDir 'llama-server.exe'
$CpuTarget = Join-Path $RuntimeDir 'ggml-cpu.dll'
$OmpTarget = Join-Path $RuntimeDir 'libomp140.x86_64.dll'

$AssetName = 'llama-prism-b10709-9a9394a-bin-win-cpu-x64.zip'
$AssetUrl = 'https://github.com/PrismML-Eng/llama.cpp/releases/download/prism-b10709-9a9394a/' + $AssetName
$ExpectedBytes = 18785841
$ExpectedSha256 = '92cd4d1cee11107593ff87d77eb57b02d804c86dd4b13224e18ba963a4271ad8'
$TimeGateMs = 60000

$Root = 'C:\AI\Bonsai2-27B-256K'
$Stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$EvidenceDir = Join-Path $Root ('evidence\runtime-r1-' + $Stamp)
$StageDir = Join-Path $Root ('downloads\staging\runtime-r1-' + $Stamp)
$ZipPath = Join-Path $StageDir $AssetName

New-Item -ItemType Directory -Path $EvidenceDir -Force | Out-Null
New-Item -ItemType Directory -Path $StageDir -Force | Out-Null

$StartTime = Get-Date
$SelectedProxy = $null
$ProxyFingerprint = $null
$CandidateCount = 0
$SwapStarted = $false
$HadOmp = Test-Path -LiteralPath $OmpTarget -PathType Leaf
$CpuBackup = Join-Path $EvidenceDir 'ggml-cpu.dll.original'
$OmpBackup = Join-Path $EvidenceDir 'libomp140.x86_64.dll.original'
$Status = 'RUNTIME_R1_FAIL_UNKNOWN'
$Failure = $null
$VersionExit = $null
$DevicesExit = $null
$VersionText = ''
$DevicesText = ''
$ElapsedMs = $null
$OriginalCpuSha256 = $null
$CandidateCpuSha256 = $null

function Restore-Runtime {
    if ($script:SwapStarted) {
        if (Test-Path -LiteralPath $script:CpuBackup -PathType Leaf) {
            Copy-Item -LiteralPath $script:CpuBackup -Destination $script:CpuTarget -Force
        }
        if ($script:HadOmp) {
            if (Test-Path -LiteralPath $script:OmpBackup -PathType Leaf) {
                Copy-Item -LiteralPath $script:OmpBackup -Destination $script:OmpTarget -Force
            }
        } else {
            Remove-Item -LiteralPath $script:OmpTarget -Force -ErrorAction SilentlyContinue
        }
    }
}

try {
    if (-not (Test-Path -LiteralPath $Server -PathType Leaf)) { throw 'LLAMA_SERVER_MISSING' }
    if (-not (Test-Path -LiteralPath $CpuTarget -PathType Leaf)) { throw 'GGML_CPU_DLL_MISSING' }
    if (Get-Process -Name 'llama-server' -ErrorAction SilentlyContinue) { throw 'LLAMA_SERVER_ALREADY_RUNNING' }
    if (-not (Get-Command curl.exe -ErrorAction SilentlyContinue)) { throw 'CURL_MISSING' }

    # 只读发现 FlClashCore exact-PID loopback LISTEN sockets；禁止猜端口、禁止扫描全部端口。
    $Fl = @(Get-Process -Name 'FlClashCore' -ErrorAction SilentlyContinue)
    if ($Fl.Count -eq 0) { throw 'FLCLASHCORE_NOT_FOUND' }

    $Candidates = @()
    foreach ($P in $Fl) {
        $Conns = @(Get-NetTCPConnection -OwningProcess $P.Id -State Listen -ErrorAction Stop |
            Where-Object { $_.LocalAddress -eq '127.0.0.1' -or $_.LocalAddress -eq '::1' })
        foreach ($C in $Conns) {
            if ($C.LocalAddress -eq '::1') {
                $Candidates += ('http://[::1]:' + $C.LocalPort)
            } else {
                $Candidates += ('http://127.0.0.1:' + $C.LocalPort)
            }
        }
    }
    $Candidates = @($Candidates | Sort-Object -Unique)
    $CandidateCount = $Candidates.Count
    if ($CandidateCount -eq 0) { throw 'NO_FLCLASH_LOOPBACK_LISTENER' }

    # 小流量固定 release probe，只选真实能工作的既有 listener。
    foreach ($Ep in $Candidates) {
        $ProbeArgs = @(
            '-L','--silent','--show-error','--fail',
            '--connect-timeout','5','--max-time','20',
            '--proxy',$Ep,
            '--range','0-1048575',
            '-o','NUL',
            '-w','%{http_code}|%{size_download}|%{time_total}',
            $AssetUrl
        )
        $ProbeOut = & curl.exe @ProbeArgs
        $ProbeExit = $LASTEXITCODE
        if ($ProbeExit -eq 0 -and $ProbeOut) {
            $Parts = [string]$ProbeOut -split '\|'
            if ($Parts.Count -ge 3) {
                $Http = [int]$Parts[0]
                $Bytes = [double]$Parts[1]
                if ($Http -ge 200 -and $Http -lt 400 -and $Bytes -gt 0) {
                    $SelectedProxy = $Ep
                    break
                }
            }
        }
    }
    if (-not $SelectedProxy) { throw 'EXISTING_PROXY_TRANSPORT_FAIL' }

    # 只在内存中计算 endpoint fingerprint；不持久化 raw endpoint。
    $EpBytes = [System.Text.Encoding]::UTF8.GetBytes($SelectedProxy)
    $EpHash = [System.Security.Cryptography.SHA256]::HashData($EpBytes)
    $ProxyFingerprint = [System.Convert]::ToHexString($EpHash).ToLowerInvariant()

    # R1 唯一新增下载：exact same release 的 CPU x64 小包。
    $DownloadArgs = @(
        '-L','--silent','--show-error','--fail',
        '--connect-timeout','5','--max-time','30',
        '--proxy',$SelectedProxy,
        '-o',$ZipPath,
        $AssetUrl
    )
    & curl.exe @DownloadArgs
    if ($LASTEXITCODE -ne 0) { throw 'CPU_ASSET_DOWNLOAD_FAIL' }

    $ActualBytes = (Get-Item -LiteralPath $ZipPath).Length
    if ($ActualBytes -ne $ExpectedBytes) { throw ('CPU_ASSET_SIZE_FAIL actual=' + $ActualBytes) }
    $ActualSha = (Get-FileHash -LiteralPath $ZipPath -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($ActualSha -ne $ExpectedSha256) { throw ('CPU_ASSET_SHA256_FAIL actual=' + $ActualSha) }

    $ExtractDir = Join-Path $StageDir 'extract'
    Expand-Archive -LiteralPath $ZipPath -DestinationPath $ExtractDir -Force

    $Sandy = @(Get-ChildItem -LiteralPath $ExtractDir -Recurse -File -Filter 'ggml-cpu-sandybridge.dll')
    $Omp = @(Get-ChildItem -LiteralPath $ExtractDir -Recurse -File -Filter 'libomp140.x86_64.dll')
    if ($Sandy.Count -ne 1) { throw ('SANDYBRIDGE_DLL_COUNT=' + $Sandy.Count) }
    if ($Omp.Count -ne 1) { throw ('LIBOMP_DLL_COUNT=' + $Omp.Count) }

    $OriginalCpuSha256 = (Get-FileHash -LiteralPath $CpuTarget -Algorithm SHA256).Hash.ToLowerInvariant()
    $CandidateCpuSha256 = (Get-FileHash -LiteralPath $Sandy[0].FullName -Algorithm SHA256).Hash.ToLowerInvariant()

    Copy-Item -LiteralPath $CpuTarget -Destination $CpuBackup -Force
    if ($HadOmp) {
        Copy-Item -LiteralPath $OmpTarget -Destination $OmpBackup -Force
    }

    $SwapStarted = $true
    Copy-Item -LiteralPath $Sandy[0].FullName -Destination $CpuTarget -Force
    Copy-Item -LiteralPath $Omp[0].FullName -Destination $OmpTarget -Force

    # 确定性 readback。
    $ReadbackCpuSha256 = (Get-FileHash -LiteralPath $CpuTarget -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($ReadbackCpuSha256 -ne $CandidateCpuSha256) { throw 'CPU_DLL_READBACK_HASH_FAIL' }

    $VersionText = (& $Server --version 2>&1 | Out-String).Trim()
    $VersionExit = $LASTEXITCODE
    if ($VersionExit -ne 0) { throw ('VERSION_GATE_FAIL exit=' + $VersionExit) }

    $DevicesText = (& $Server --list-devices 2>&1 | Out-String).Trim()
    $DevicesExit = $LASTEXITCODE
    if ($DevicesExit -ne 0) { throw ('LIST_DEVICES_GATE_FAIL exit=' + $DevicesExit) }
    if ($DevicesText -notmatch 'CUDA') { throw 'CUDA_DEVICE_NOT_LISTED' }
    if ($DevicesText -notmatch '2080 Ti') { throw 'RTX2080TI_NOT_LISTED' }

    $Span = (Get-Date) - $StartTime
    $ElapsedMs = [long]$Span.TotalMilliseconds

    if ($ElapsedMs -gt $TimeGateMs) {
        $Status = 'RUNTIME_R1_FAIL_TIME_MODEL'
        $Failure = 'QUALITY_PASS_BUT_T_VALID_GT_60000MS'
        Restore-Runtime
    } else {
        $Status = 'RUNTIME_R1_REALITY_CERTIFIED'
    }
}
catch {
    $Failure = $_.Exception.Message
    $Span = (Get-Date) - $StartTime
    $ElapsedMs = [long]$Span.TotalMilliseconds
    Restore-Runtime
    if ($Failure -match 'VERSION_GATE_FAIL') {
        $Status = 'RUNTIME_R1_FAIL_VERSION'
    } elseif ($Failure -match 'CUDA_DEVICE|RTX2080TI|LIST_DEVICES') {
        $Status = 'RUNTIME_R1_FAIL_CUDA_GATE'
    } elseif ($Failure -match 'DOWNLOAD|TRANSPORT|PROXY|FLCLASH') {
        $Status = 'RUNTIME_R1_FAIL_TRANSPORT'
    } else {
        $Status = 'RUNTIME_R1_FAIL_RUNTIME'
    }
}

$Result = [ordered]@{
    schema_version = 1
    current_step = 3
    candidate = 'R1_SAME_RELEASE_CPU_BACKEND_GRAFT'
    virtual_target_ms = 60000
    t_valid_real_ms = $ElapsedMs
    status = $Status
    failure = $Failure
    source_release = 'prism-b10709-9a9394a'
    source_commit = '9a9394a895b96003ca842a6041cb28ac49a108f7'
    asset = $AssetName
    asset_expected_bytes = $ExpectedBytes
    asset_expected_sha256 = $ExpectedSha256
    proxy_source = 'FlClashCore_exact_pid_loopback_listener'
    proxy_candidate_count = $CandidateCount
    proxy_endpoint_fingerprint = $ProxyFingerprint
    raw_proxy_endpoint_persisted = $false
    original_cpu_sha256 = $OriginalCpuSha256
    candidate_cpu_sha256 = $CandidateCpuSha256
    version_exit = $VersionExit
    version_output = $VersionText
    list_devices_exit = $DevicesExit
    list_devices_output = $DevicesText
    model_downloads = 0
    compilation = $false
    r2_r3_fallback = $false
    system_proxy_modified = $false
    git_proxy_modified = $false
    flclash_modified = $false
    network_modified = $false
    registry_modified = $false
    next_action = 'RETURN_TO_GPT'
    stop = $true
}
$Json = $Result | ConvertTo-Json -Depth 6
$JsonPath = Join-Path $EvidenceDir 'RESULT.json'
$TextPath = Join-Path $EvidenceDir 'RESULT.txt'
$Json | Set-Content -LiteralPath $JsonPath -Encoding utf8
@(
    'RUNTIME_R1_RESULT'
    ('STATUS=' + $Status)
    ('T_VALID_REAL_MS=' + $ElapsedMs)
    'T_VALID_VIRTUAL_TARGET_MS=60000'
    ('FAILURE=' + [string]$Failure)
    ('VERSION_EXIT=' + [string]$VersionExit)
    ('LIST_DEVICES_EXIT=' + [string]$DevicesExit)
    ('EVIDENCE=' + $EvidenceDir)
    'MODEL_DOWNLOADS=0'
    'COMPILATION=false'
    'R2_R3_FALLBACK=false'
    'NEXT_ACTION=RETURN_TO_GPT'
    'STOP=true'
) | Set-Content -LiteralPath $TextPath -Encoding utf8

Get-Content -LiteralPath $TextPath
