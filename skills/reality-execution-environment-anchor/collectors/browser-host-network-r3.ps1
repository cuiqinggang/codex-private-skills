param(
  [Parameter(Mandatory=$true)]
  [string]$OutputDir
)

$ErrorActionPreference = 'SilentlyContinue'
New-Item -ItemType Directory -Force -Path (Join-Path $OutputDir 'raw') | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $OutputDir 'safe') | Out-Null

function Get-TextSha256 {
  param([AllowNull()][string]$Text)
  if ($null -eq $Text) { return $null }
  $bytes = [Text.Encoding]::UTF8.GetBytes($Text)
  $sha = [Security.Cryptography.SHA256]::Create()
  try { return ([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-','').ToLowerInvariant() }
  finally { $sha.Dispose() }
}

function Get-FileSha256Safe {
  param([AllowNull()][string]$Path)
  if ([string]::IsNullOrWhiteSpace($Path) -or -not (Test-Path -LiteralPath $Path)) { return $null }
  try { return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() } catch { return $null }
}

$proxyNames = @('HTTP_PROXY','HTTPS_PROXY','ALL_PROXY','NO_PROXY','http_proxy','https_proxy','all_proxy','no_proxy')
$proxyEnvSafe = @{}
$proxyEnvRaw = @{}
foreach ($name in $proxyNames) {
  $value = [Environment]::GetEnvironmentVariable($name)
  if ($null -ne $value) {
    $proxyEnvRaw[$name] = $value
    $proxyEnvSafe[$name] = @{
      present = $true
      length = $value.Length
      sha256 = Get-TextSha256 $value
    }
  } else {
    $proxyEnvSafe[$name] = @{ present = $false }
  }
}

$winHttp = (& netsh winhttp show proxy 2>&1 | Out-String)
$userInternet = Get-ItemProperty 'HKCU:SoftwareMicrosoftWindowsCurrentVersionInternet Settings'
$userProxyRaw = @{
  ProxyEnable = $userInternet.ProxyEnable
  ProxyServer = $userInternet.ProxyServer
  AutoConfigURL = $userInternet.AutoConfigURL
  AutoDetect = $userInternet.AutoDetect
}
$userProxySafe = @{
  ProxyEnable = $userInternet.ProxyEnable
  ProxyServerPresent = -not [string]::IsNullOrWhiteSpace([string]$userInternet.ProxyServer)
  ProxyServerSha256 = Get-TextSha256 ([string]$userInternet.ProxyServer)
  AutoConfigURLPresent = -not [string]::IsNullOrWhiteSpace([string]$userInternet.AutoConfigURL)
  AutoConfigURLSha256 = Get-TextSha256 ([string]$userInternet.AutoConfigURL)
  AutoDetect = $userInternet.AutoDetect
}

$dns = @(Get-DnsClientServerAddress | Select-Object InterfaceAlias,InterfaceIndex,AddressFamily,ServerAddresses)
$ipConfig = @(Get-NetIPConfiguration | Select-Object InterfaceAlias,InterfaceIndex,IPv4Address,IPv6Address,IPv4DefaultGateway,IPv6DefaultGateway,NetProfile)
$routes = @(Get-NetRoute | Select-Object AddressFamily,DestinationPrefix,NextHop,InterfaceIndex,RouteMetric,Protocol,State)
$adapters = @(Get-NetAdapter | Select-Object Name,InterfaceDescription,ifIndex,Status,MacAddress,LinkSpeed,MediaConnectionState)

$procRaw = @()
$procSafe = @()
$processes = @(Get-CimInstance Win32_Process | Where-Object {
  $_.Name -match '^(chrome|msedge|chromium|node|playwright)(.exe)?$'
})
foreach ($p in $processes) {
  $version = $null
  if ($p.ExecutablePath -and (Test-Path -LiteralPath $p.ExecutablePath)) {
    try { $version = (Get-Item -LiteralPath $p.ExecutablePath).VersionInfo.FileVersion } catch {}
  }
  $procRaw += [ordered]@{
    Name = $p.Name
    ProcessId = $p.ProcessId
    ParentProcessId = $p.ParentProcessId
    ExecutablePath = $p.ExecutablePath
    CommandLine = $p.CommandLine
    FileVersion = $version
    ExecutableSha256 = Get-FileSha256Safe $p.ExecutablePath
  }
  $procSafe += [ordered]@{
    Name = $p.Name
    ProcessId = $p.ProcessId
    ParentProcessId = $p.ParentProcessId
    ExecutableName = if ($p.ExecutablePath) { [IO.Path]::GetFileName($p.ExecutablePath) } else { $p.Name }
    ExecutablePathSha256 = Get-TextSha256 ([string]$p.ExecutablePath)
    CommandLinePresent = -not [string]::IsNullOrWhiteSpace([string]$p.CommandLine)
    CommandLineSha256 = Get-TextSha256 ([string]$p.CommandLine)
    FileVersion = $version
    ExecutableSha256 = Get-FileSha256Safe $p.ExecutablePath
  }
}

$browserPids = @($processes | Where-Object { $_.Name -match '^(chrome|msedge|chromium)(.exe)?$' } | ForEach-Object { [int]$_.ProcessId })
$tcpRaw = @()
if ($browserPids.Count -gt 0) {
  $tcpRaw = @(Get-NetTCPConnection | Where-Object { $browserPids -contains $_.OwningProcess } |
    Select-Object State,LocalAddress,LocalPort,RemoteAddress,RemotePort,OwningProcess)
}
$tcpSafe = @($tcpRaw | ForEach-Object {
  [ordered]@{
    State = $_.State
    LocalPort = $_.LocalPort
    RemotePort = $_.RemotePort
    OwningProcess = $_.OwningProcess
    LocalAddressSha256 = Get-TextSha256 ([string]$_.LocalAddress)
    RemoteAddressSha256 = Get-TextSha256 ([string]$_.RemoteAddress)
  }
})

$dnsSafe = @($dns | ForEach-Object {
  [ordered]@{
    InterfaceAlias = $_.InterfaceAlias
    InterfaceIndex = $_.InterfaceIndex
    AddressFamily = $_.AddressFamily
    ServerAddressCount = @($_.ServerAddresses).Count
    ServerAddressesSha256 = Get-TextSha256 ((@($_.ServerAddresses) -join '|'))
  }
})

$ipConfigSafe = @($ipConfig | ForEach-Object {
  [ordered]@{
    InterfaceAlias = $_.InterfaceAlias
    InterfaceIndex = $_.InterfaceIndex
    IPv4AddressSha256 = Get-TextSha256 ((@($_.IPv4Address | ForEach-Object { [string]$_.IPAddress }) -join '|'))
    IPv6AddressSha256 = Get-TextSha256 ((@($_.IPv6Address | ForEach-Object { [string]$_.IPAddress }) -join '|'))
    IPv4DefaultGatewaySha256 = Get-TextSha256 ((@($_.IPv4DefaultGateway | ForEach-Object { [string]$_.NextHop }) -join '|'))
    IPv6DefaultGatewaySha256 = Get-TextSha256 ((@($_.IPv6DefaultGateway | ForEach-Object { [string]$_.NextHop }) -join '|'))
    NetProfileNameSha256 = Get-TextSha256 ([string]$_.NetProfile.Name)
    NetProfileCategory = $_.NetProfile.NetworkCategory
  }
})

$routesSafe = @($routes | ForEach-Object {
  [ordered]@{
    AddressFamily = $_.AddressFamily
    DestinationPrefixSha256 = Get-TextSha256 ([string]$_.DestinationPrefix)
    NextHopSha256 = Get-TextSha256 ([string]$_.NextHop)
    InterfaceIndex = $_.InterfaceIndex
    RouteMetric = $_.RouteMetric
    Protocol = $_.Protocol
    State = $_.State
  }
})

$adaptersSafe = @($adapters | ForEach-Object {
  [ordered]@{
    Name = $_.Name
    InterfaceDescription = $_.InterfaceDescription
    ifIndex = $_.ifIndex
    Status = $_.Status
    MacAddressSha256 = Get-TextSha256 ([string]$_.MacAddress)
    LinkSpeed = $_.LinkSpeed
    MediaConnectionState = $_.MediaConnectionState
  }
})

$raw = [ordered]@{
  schema_version = '1.0'
  captured_utc = (Get-Date).ToUniversalTime().ToString('o')
  mode = 'READ_ONLY_BROWSER_HOST_NETWORK_R3'
  proxy_environment = $proxyEnvRaw
  winhttp_proxy = $winHttp
  user_internet_settings = $userProxyRaw
  dns = $dns
  ip_configuration = $ipConfig
  routes = $routes
  adapters = $adapters
  browser_node_processes = $procRaw
  browser_tcp_connections = $tcpRaw
}

$safe = [ordered]@{
  schema_version = '1.0'
  captured_utc = $raw.captured_utc
  mode = $raw.mode
  no_outbound_probe = $true
  no_setting_change = $true
  proxy_environment = $proxyEnvSafe
  winhttp_proxy_sha256 = Get-TextSha256 $winHttp
  user_internet_settings = $userProxySafe
  dns = $dnsSafe
  ip_configuration = $ipConfigSafe
  routes = $routesSafe
  adapters = $adaptersSafe
  browser_node_processes = $procSafe
  browser_tcp_connections_safe = $tcpSafe
}

$rawPath = Join-Path $OutputDir 'rawhost-network.json'
$safePath = Join-Path $OutputDir 'safehost-network.json'
$raw | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $rawPath -Encoding UTF8
$safe | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $safePath -Encoding UTF8

$rawHash = (Get-FileHash -LiteralPath $rawPath -Algorithm SHA256).Hash.ToLowerInvariant()
$safeHash = (Get-FileHash -LiteralPath $safePath -Algorithm SHA256).Hash.ToLowerInvariant()
[ordered]@{
  RAW_PATH = $rawPath
  RAW_SHA256 = $rawHash
  SAFE_PATH = $safePath
  SAFE_SHA256 = $safeHash
  REALITY_MUTATION = 'NO'
  OUTBOUND_PROBE = 'NO'
} | ConvertTo-Json -Depth 4
