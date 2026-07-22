param(
  [string]$BaseUrl = "http://127.0.0.1:8188",
${REDACTED_SECRET}
)

$ErrorActionPreference = "Stop"
$Logs = Join-Path $TaskRoot "logs"
New-Item -ItemType Directory -Force -Path $Logs | Out-Null

$result = [ordered]@{
  base_url = $BaseUrl
  checked_at = (Get-Date).ToString("s")
  system_stats = $false
  manager = $false
  ultimate_sd_upscale = $false
  cuda_device = $null
  comfyui_version = $null
  manager_version = $null
  ultimate_nodes = @()
  errors = @()
}

try {
  $stats = Invoke-RestMethod -Uri "$BaseUrl/system_stats" -TimeoutSec 10
  $result.system_stats = $true
  $result.comfyui_version = $stats.system.comfyui_version
  if ($stats.devices.Count -gt 0) {
    $result.cuda_device = $stats.devices[0].name
  }
} catch {
  $result.errors += "system_stats: $($_.Exception.Message)"
}

try {
  $manager = Invoke-WebRequest -Uri "$BaseUrl/v2/manager/version" -TimeoutSec 10 -UseBasicParsing
  if ($manager.StatusCode -eq 200) {
    $result.manager = $true
    $result.manager_version = [string]$manager.Content
  }
} catch {
  $result.errors += "manager: $($_.Exception.Message)"
}

try {
  $obj = Invoke-RestMethod -Uri "$BaseUrl/object_info" -TimeoutSec 30
  $names = $obj.PSObject.Properties.Name
  $matches = @($names | Where-Object { $_ -match "UltimateSDUpscale" } | Sort-Object)
  $result.ultimate_nodes = $matches
  $result.ultimate_sd_upscale = $matches -contains "UltimateSDUpscale"
} catch {
  $result.errors += "object_info: $($_.Exception.Message)"
}

$path = Join-Path $Logs "skill-verify-comfyui.json"
$json = ($result | ConvertTo-Json -Depth 6)
$json | Set-Content -LiteralPath $path -Encoding UTF8
$json

if ($result.system_stats -and $result.manager -and $result.ultimate_sd_upscale) {
  exit 0
}
exit 1
