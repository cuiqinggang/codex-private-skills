param(
  [string]$Root = 'C:\AI\n8n',
  [string]$TargetVersion = '2.41.6'
)

$ErrorActionPreference='Stop'
$compose = Join-Path $Root 'compose.yml'
if (-not (Test-Path -LiteralPath $compose)) { throw "compose.yml missing: $compose" }
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { throw 'docker command not found' }

$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$backup = Join-Path $Root ("backup\" + $stamp)
New-Item -ItemType Directory -Force -Path $backup | Out-Null

Copy-Item $compose (Join-Path $backup 'compose.yml.before') -Force
if (Test-Path (Join-Path $Root '.env')) { Copy-Item (Join-Path $Root '.env') (Join-Path $backup '.env.before') -Force }
if (Test-Path (Join-Path $Root 'DEPLOYMENT-STATUS.md')) { Copy-Item (Join-Path $Root 'DEPLOYMENT-STATUS.md') (Join-Path $backup 'DEPLOYMENT-STATUS.md.before') -Force }

Push-Location $Root
try {
  $containerId = (docker compose ps -q | Select-Object -First 1).Trim()
  if (-not $containerId) { throw 'No compose container found' }

  $inspect = docker inspect $containerId | ConvertFrom-Json
  $oldImageId = $inspect[0].Image
  $oldVersion = ((docker exec $containerId n8n --version 2>&1 | Out-String).Trim())
  $rollbackTag = "n8nio/n8n:etal-rollback-$stamp"
  docker tag $oldImageId $rollbackTag | Out-Null

  $volume = 'n8n-local_n8n_data'
  docker volume inspect $volume | Out-Null
  docker run --rm --mount "type=volume,src=$volume,dst=/data,readonly" --mount "type=bind,src=$backup,dst=/backup" alpine:3.22 sh -lc "cd /data && tar czf /backup/n8n_data.tar.gz ." | Out-Null

  $text = Get-Content -LiteralPath $compose -Raw
  if ($text -match 'n8nio/n8n:stable') {
    $text = $text -replace 'n8nio/n8n:stable',("n8nio/n8n:" + $TargetVersion)
    Set-Content -LiteralPath $compose -Value $text -Encoding UTF8
  } elseif ($text -notmatch ("n8nio/n8n:" + [regex]::Escape($TargetVersion))) {
    throw 'Compose image is not stable and not the requested target; refusing implicit migration.'
  }

  docker compose pull
  docker compose up -d

  Start-Sleep -Seconds 8
  $newContainer = (docker compose ps -q | Select-Object -First 1).Trim()
  if (-not $newContainer) { throw 'No container after upgrade' }

  $newVersion = ((docker exec $newContainer n8n --version 2>&1 | Out-String).Trim())
  if ($newVersion -ne $TargetVersion) { throw "Version mismatch: $newVersion != $TargetVersion" }

  $health = Invoke-WebRequest 'http://localhost:5678/healthz' -UseBasicParsing -TimeoutSec 20
  if ($health.StatusCode -ne 200) { throw "Health failed: $($health.StatusCode)" }

  $ni = (docker inspect $newContainer | ConvertFrom-Json)[0]
  $dataOk = @($ni.Mounts | Where-Object { $_.Destination -eq '/home/node/.n8n' }).Count -gt 0
  $artOk = @($ni.Mounts | Where-Object { $_.Destination -eq '/files/artifacts' }).Count -gt 0
  if (-not $dataOk) { throw 'Data mount missing' }
  if (-not $artOk) { throw 'Artifact mount missing' }

  [ordered]@{
    RESULT='PASS'; FROM_VERSION=$oldVersion; TO_VERSION=$newVersion; BACKUP_DIR=$backup;
    OLD_IMAGE_ID=$oldImageId; NEW_IMAGE_ID=$ni.Image; HEALTH_STATUS=$health.StatusCode;
    DATA_VOLUME_PRESENT=$dataOk; ARTIFACT_MOUNT_PRESENT=$artOk
  } | ConvertTo-Json
}
catch {
  $failure=$_.Exception.Message
  try {
    docker compose down | Out-Null
    Copy-Item (Join-Path $backup 'compose.yml.before') $compose -Force

    $volume = 'n8n-local_n8n_data'
    docker run --rm --mount "type=volume,src=$volume,dst=/data" alpine:3.22 sh -lc "rm -rf /data/* /data/.[!.]* /data/..?* 2>/dev/null || true" | Out-Null
    docker run --rm --mount "type=volume,src=$volume,dst=/data" --mount "type=bind,src=$backup,dst=/backup,readonly" alpine:3.22 sh -lc "cd /data && tar xzf /backup/n8n_data.tar.gz" | Out-Null

    $orig = Get-Content -LiteralPath $compose -Raw
    if ($orig -match 'n8nio/n8n:stable') {
      $orig = $orig -replace 'n8nio/n8n:stable',$rollbackTag
      Set-Content -LiteralPath $compose -Value $orig -Encoding UTF8
    }
    docker compose up -d | Out-Null
    Start-Sleep -Seconds 8
    $rb = (docker compose ps -q | Select-Object -First 1).Trim()
    $rbVersion = if ($rb) { ((docker exec $rb n8n --version 2>&1 | Out-String).Trim()) } else { $null }
    $rbHealth = try { (Invoke-WebRequest 'http://localhost:5678/healthz' -UseBasicParsing -TimeoutSec 20).StatusCode } catch { $null }

    [ordered]@{RESULT='ROLLED_BACK'; ERROR=$failure; BACKUP_DIR=$backup; ROLLBACK_VERSION=$rbVersion; ROLLBACK_HEALTH=$rbHealth} | ConvertTo-Json
    exit 2
  } catch {
    [ordered]@{RESULT='FAIL'; ERROR=$failure; ROLLBACK_ERROR=$_.Exception.Message; BACKUP_DIR=$backup} | ConvertTo-Json
    exit 3
  }
}
finally {
  Pop-Location
}
