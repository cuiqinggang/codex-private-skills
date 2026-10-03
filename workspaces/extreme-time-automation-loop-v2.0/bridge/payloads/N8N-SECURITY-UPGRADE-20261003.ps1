$ErrorActionPreference = 'Stop'

$Root = 'C:\AI\n8n'
$TargetVersion = '2.41.6'
$ComposePath = Join-Path $Root 'compose.yml'
$VolumeName = 'n8n-local_n8n_data'
$HealthUrl = 'http://localhost:5678/healthz'
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$backup = Join-Path $Root ("backup\" + $stamp)
$rollbackTag = "n8nio/n8n:etal-rollback-$stamp"
$upgradeStarted = $false
$serviceStoppedForBackup = $false
$oldImageId = $null
$oldVersion = $null
$serviceName = $null

function Get-N8nContainer {
  $ids = @(docker compose ps -q 2>$null)
  foreach ($id in $ids) {
    if (-not $id) { continue }
    try {
      $i = (docker inspect $id | ConvertFrom-Json)[0]
      $name = ($i.Name -replace '^/','')
      $image = $i.Config.Image
      if ($name -match 'n8n' -or $image -match '(^|/)n8n(:|@)' -or $image -match 'n8nio/n8n') {
        return $id.Trim()
      }
    } catch {}
  }
  return $null
}

function Wait-N8nHealth([int]$Seconds = 90) {
  $end = (Get-Date).AddSeconds($Seconds)
  do {
    try {
      $r = Invoke-WebRequest $HealthUrl -UseBasicParsing -TimeoutSec 10
      if ($r.StatusCode -eq 200) { return 200 }
    } catch {}
    Start-Sleep -Seconds 3
  } while ((Get-Date) -lt $end)
  return $null
}

function Emit-Result($obj, [int]$ExitCode = 0) {
  $json = $obj | ConvertTo-Json -Depth 8
  Write-Output $json
  if ($env:RESULT_DIR) {
    try {
      New-Item -ItemType Directory -Force -Path $env:RESULT_DIR | Out-Null
      $json | Set-Content -LiteralPath (Join-Path $env:RESULT_DIR 'n8n-upgrade.json') -Encoding UTF8
    } catch {}
  }
  exit $ExitCode
}

try {
  if (-not (Test-Path -LiteralPath $ComposePath)) { throw "PRECHECK: compose.yml missing at $ComposePath" }
  if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { throw 'PRECHECK: docker command not found' }
  docker version --format '{{.Server.Version}}' | Out-Null

  Push-Location $Root
  $containerId = Get-N8nContainer
  if (-not $containerId) { throw 'PRECHECK: n8n compose container not found' }

  $inspect = (docker inspect $containerId | ConvertFrom-Json)[0]
  $serviceName = $inspect.Config.Labels.'com.docker.compose.service'
  if (-not $serviceName) { throw 'PRECHECK: compose service label missing' }

  $oldImageId = $inspect.Image
  $oldVersion = ((docker exec $containerId n8n --version 2>&1 | Out-String).Trim())
  $oldHealth = Wait-N8nHealth 20
  if ($oldHealth -ne 200) { throw 'PRECHECK: existing n8n health check is not 200; refusing upgrade' }

  docker volume inspect $VolumeName | Out-Null

  $mountData = @($inspect.Mounts | Where-Object { $_.Destination -eq '/home/node/.n8n' })
  $mountArtifacts = @($inspect.Mounts | Where-Object { $_.Destination -eq '/files/artifacts' })
  if ($mountData.Count -lt 1) { throw 'PRECHECK: /home/node/.n8n mount missing' }
  if ($mountArtifacts.Count -lt 1) { throw 'PRECHECK: /files/artifacts mount missing' }

  $composeText = Get-Content -LiteralPath $ComposePath -Raw
  $imageMatches = [regex]::Matches($composeText, 'n8nio/n8n:(?<tag>[^\s\"''\}]+)')
  if ($imageMatches.Count -ne 1) { throw "PRECHECK: expected exactly one n8nio/n8n image declaration, found $($imageMatches.Count)" }
  $currentTag = $imageMatches[0].Groups['tag'].Value

  if ($oldVersion -eq $TargetVersion) {
    Emit-Result ([ordered]@{
      RESULT='ALREADY_CURRENT'
      FROM_VERSION=$oldVersion
      TO_VERSION=$TargetVersion
      HEALTH_STATUS=$oldHealth
      DATA_VOLUME_PRESENT=$true
      ARTIFACT_MOUNT_PRESENT=$true
      COMPOSE_IMAGE_TAG=$currentTag
    }) 0
  }

  New-Item -ItemType Directory -Force -Path $backup | Out-Null
  Copy-Item $ComposePath (Join-Path $backup 'compose.yml.before') -Force
  if (Test-Path (Join-Path $Root '.env')) { Copy-Item (Join-Path $Root '.env') (Join-Path $backup '.env.before') -Force }
  if (Test-Path (Join-Path $Root 'DEPLOYMENT-STATUS.md')) { Copy-Item (Join-Path $Root 'DEPLOYMENT-STATUS.md') (Join-Path $backup 'DEPLOYMENT-STATUS.md.before') -Force }

  [ordered]@{
    timestamp=(Get-Date).ToString('o')
    old_version=$oldVersion
    old_image_id=$oldImageId
    old_image_config=$inspect.Config.Image
    old_image_repo_digests=@((docker image inspect $oldImageId --format '{{json .RepoDigests}}' 2>$null))
    service=$serviceName
    data_mount=@($mountData | Select-Object Type,Source,Destination,Name)
    artifact_mount=@($mountArtifacts | Select-Object Type,Source,Destination,Name)
  } | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $backup 'pre-upgrade.json') -Encoding UTF8

  docker tag $oldImageId $rollbackTag | Out-Null

  # Stop only n8n service for a consistent SQLite/data-volume snapshot.
  docker compose stop $serviceName | Out-Null
  $serviceStoppedForBackup = $true

  docker pull alpine:3.22 | Out-Null
  docker run --rm --mount "type=volume,src=$VolumeName,dst=/data,readonly" --mount "type=bind,src=$backup,dst=/backup" alpine:3.22 sh -lc "cd /data && tar czf /backup/n8n_data.tar.gz ." | Out-Null
  if (-not (Test-Path (Join-Path $backup 'n8n_data.tar.gz'))) { throw 'BACKUP: data volume archive missing' }

  # Freeze this run to the exact target version.
  $newCompose = [regex]::Replace(
    $composeText,
    'n8nio/n8n:[^\s\"''\}]+',
    "n8nio/n8n:$TargetVersion",
    1
  )
  if ($newCompose -eq $composeText -and $currentTag -ne $TargetVersion) { throw 'UPGRADE: compose image replacement failed' }
  Set-Content -LiteralPath $ComposePath -Value $newCompose -Encoding UTF8

  docker pull "n8nio/n8n:$TargetVersion" | Out-Null
  $upgradeStarted = $true
  docker compose up -d | Out-Null
  $serviceStoppedForBackup = $false

  $newContainer = Get-N8nContainer
  if (-not $newContainer) { throw 'VALIDATION: n8n container missing after upgrade' }

  $newVersion = ((docker exec $newContainer n8n --version 2>&1 | Out-String).Trim())
  if ($newVersion -ne $TargetVersion) { throw "VALIDATION: version mismatch $newVersion != $TargetVersion" }

  $health = Wait-N8nHealth 90
  if ($health -ne 200) { throw 'VALIDATION: /healthz did not become HTTP 200' }

  $ni = (docker inspect $newContainer | ConvertFrom-Json)[0]
  $dataOk = @($ni.Mounts | Where-Object { $_.Destination -eq '/home/node/.n8n' }).Count -gt 0
  $artOk = @($ni.Mounts | Where-Object { $_.Destination -eq '/files/artifacts' }).Count -gt 0
  if (-not $dataOk) { throw 'VALIDATION: data mount missing' }
  if (-not $artOk) { throw 'VALIDATION: artifacts mount missing' }

  Emit-Result ([ordered]@{
    RESULT='PASS'
    FROM_VERSION=$oldVersion
    TO_VERSION=$newVersion
    BACKUP_DIR=$backup
    OLD_IMAGE_ID=$oldImageId
    NEW_IMAGE_ID=$ni.Image
    HEALTH_STATUS=$health
    DATA_VOLUME_PRESENT=$dataOk
    ARTIFACT_MOUNT_PRESENT=$artOk
    COMPOSE_FILE=$ComposePath
  }) 0
}
catch {
  $failure = $_.Exception.Message

  try {
    if ($serviceStoppedForBackup -and -not $upgradeStarted) {
      try { docker compose start $serviceName | Out-Null } catch {}
    }

    if ($upgradeStarted) {
      docker compose down | Out-Null
      Copy-Item (Join-Path $backup 'compose.yml.before') $ComposePath -Force

      docker run --rm --mount "type=volume,src=$VolumeName,dst=/data" alpine:3.22 sh -lc "find /data -mindepth 1 -maxdepth 1 -exec rm -rf {} +" | Out-Null
      docker run --rm --mount "type=volume,src=$VolumeName,dst=/data" --mount "type=bind,src=$backup,dst=/backup,readonly" alpine:3.22 sh -lc "cd /data && tar xzf /backup/n8n_data.tar.gz" | Out-Null

      $orig = Get-Content -LiteralPath $ComposePath -Raw
      $orig = [regex]::Replace($orig,'n8nio/n8n:[^\s\"''\}]+',$rollbackTag,1)
      Set-Content -LiteralPath $ComposePath -Value $orig -Encoding UTF8
      docker compose up -d | Out-Null

      $rb = Get-N8nContainer
      $rbVersion = if ($rb) { ((docker exec $rb n8n --version 2>&1 | Out-String).Trim()) } else { $null }
      $rbHealth = Wait-N8nHealth 90

      Emit-Result ([ordered]@{
        RESULT='ROLLED_BACK'
        ERROR=$failure
        BACKUP_DIR=$backup
        ROLLBACK_VERSION=$rbVersion
        ROLLBACK_HEALTH=$rbHealth
        ROLLBACK_IMAGE_TAG=$rollbackTag
      }) 2
    }

    Emit-Result ([ordered]@{
      RESULT='FAIL_NO_UPGRADE'
      ERROR=$failure
      FROM_VERSION=$oldVersion
      BACKUP_DIR=$(if (Test-Path $backup) { $backup } else { $null })
    }) 3
  }
  catch {
    Emit-Result ([ordered]@{
      RESULT='FAIL_ROLLBACK'
      ERROR=$failure
      ROLLBACK_ERROR=$_.Exception.Message
      BACKUP_DIR=$(if (Test-Path $backup) { $backup } else { $null })
    }) 4
  }
}
finally {
  try { Pop-Location } catch {}
}
