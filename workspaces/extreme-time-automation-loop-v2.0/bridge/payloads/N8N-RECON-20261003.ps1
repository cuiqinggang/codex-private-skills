$ErrorActionPreference = 'Continue'

function Add-Result([hashtable]$h, [string]$k, $v) {
  try { $h[$k] = $v } catch {}
}

$R = [ordered]@{
  timestamp = (Get-Date).ToString("o")
  computer = $env:COMPUTERNAME
  user = $env:USERNAME
  userprofile = $env:USERPROFILE
}

# n8n CLI / npm
try {
  $cmd = Get-Command n8n -ErrorAction SilentlyContinue
  Add-Result $R "n8n_command" $(if ($cmd) { $cmd.Source } else { $null })
  if ($cmd) { Add-Result $R "n8n_cli_version" ((& n8n --version 2>&1 | Out-String).Trim()) }
} catch { Add-Result $R "n8n_cli_error" $_.Exception.Message }

try { Add-Result $R "node_version" ((node --version 2>&1 | Out-String).Trim()) } catch {}
try { Add-Result $R "npm_version" ((npm --version 2>&1 | Out-String).Trim()) } catch {}
try { Add-Result $R "npm_global_n8n" ((npm list -g n8n --depth=0 2>&1 | Out-String).Trim()) } catch {}

# Docker / containers
try {
  $docker = Get-Command docker -ErrorAction SilentlyContinue
  Add-Result $R "docker_present" [bool]$docker
  if ($docker) {
    Add-Result $R "docker_version" ((docker version --format '{{.Server.Version}}' 2>&1 | Out-String).Trim())
    $ps = docker ps -a --format '{{json .}}' 2>&1
    Add-Result $R "docker_ps" @($ps)
    $ids = @(docker ps -aq 2>$null)
    $n8nContainers = @()
    foreach ($id in $ids) {
      try {
        $i = docker inspect $id | ConvertFrom-Json
        $o = $i[0]
        $name = ($o.Name -replace '^/','')
        $image = $o.Config.Image
        $labels = $o.Config.Labels
        if (($name -match 'n8n') -or ($image -match 'n8n')) {
          $entry = [ordered]@{
            id = $id
            name = $name
            image = $image
            status = $o.State.Status
            started_at = $o.State.StartedAt
            compose_project = $labels.'com.docker.compose.project'
            compose_project_dir = $labels.'com.docker.compose.project.working_dir'
            compose_files = $labels.'com.docker.compose.project.config_files'
            mounts = @($o.Mounts | ForEach-Object { [ordered]@{Type=$_.Type;Source=$_.Source;Destination=$_.Destination;Name=$_.Name} })
          }
          try { $entry["runtime_version"] = ((docker exec $id n8n --version 2>&1 | Out-String).Trim()) } catch {}
          $n8nContainers += $entry
        }
      } catch {}
    }
    Add-Result $R "n8n_containers" $n8nContainers
  }
} catch { Add-Result $R "docker_error" $_.Exception.Message }

# Windows services / scheduled tasks likely related to n8n
try {
  Add-Result $R "services_n8n" @(Get-CimInstance Win32_Service | Where-Object { $_.Name -match 'n8n' -or $_.DisplayName -match 'n8n' -or $_.PathName -match 'n8n' } | Select-Object Name,DisplayName,State,StartMode,PathName)
} catch {}
try {
  Add-Result $R "scheduled_tasks_n8n" @(Get-ScheduledTask | Where-Object { $_.TaskName -match 'n8n' -or $_.TaskPath -match 'n8n' } | Select-Object TaskName,TaskPath,State)
} catch {}

# Listening port 5678
try {
  Add-Result $R "port_5678" @(Get-NetTCPConnection -LocalPort 5678 -State Listen -ErrorAction SilentlyContinue | Select-Object LocalAddress,LocalPort,OwningProcess)
} catch {}

# Search likely local workspaces for old skill / deployment manifests.
$roots = @()
if ($env:USERPROFILE) {
  $roots += $env:USERPROFILE
  $roots += (Join-Path $env:USERPROFILE 'Desktop')
  $roots += (Join-Path $env:USERPROFILE 'Documents')
}
$roots = $roots | Select-Object -Unique | Where-Object { Test-Path $_ }

$matches = @()
$rg = Get-Command rg -ErrorAction SilentlyContinue
if ($rg) {
  foreach ($root in $roots) {
    try {
      $lines = & rg -n -S --hidden --glob '*.md' --glob '*.txt' --glob '*.yml' --glob '*.yaml' --glob '*.json' --glob '!AppData/**' --glob '!node_modules/**' --glob '!.git/**' 'n8n 多智能体运行指挥台|多智能体运行指挥台|n8n.*指挥台' $root 2>$null
      if ($lines) { $matches += @($lines | Select-Object -First 200) }
    } catch {}
  }
}
Add-Result $R "skill_text_matches" @($matches | Select-Object -Unique | Select-Object -First 300)

# Find common compose/deployment files mentioning n8n, bounded by likely roots and using rg.
$deployMatches = @()
if ($rg) {
  foreach ($root in $roots) {
    try {
      $lines = & rg -n -S --hidden --glob 'docker-compose*.yml' --glob 'docker-compose*.yaml' --glob 'compose*.yml' --glob 'compose*.yaml' --glob '*.env' --glob '*.ps1' --glob '*.cmd' --glob '*.bat' --glob '!AppData/**' --glob '!node_modules/**' --glob '!.git/**' 'n8n' $root 2>$null
      if ($lines) { $deployMatches += @($lines | Select-Object -First 300) }
    } catch {}
  }
}
Add-Result $R "deployment_text_matches" @($deployMatches | Select-Object -Unique | Select-Object -First 500)

$json = $R | ConvertTo-Json -Depth 8
Write-Output $json

if ($env:RESULT_DIR) {
  try {
    New-Item -ItemType Directory -Force -Path $env:RESULT_DIR | Out-Null
    $json | Set-Content -LiteralPath (Join-Path $env:RESULT_DIR 'n8n-recon.json') -Encoding UTF8
  } catch {}
}

exit 0
