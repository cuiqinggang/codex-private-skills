param(
  [Parameter(Mandatory = $true)]
  [string]$Path,

  [int]$TimeoutSec = 15
)

$ErrorActionPreference = 'Continue'

if (-not (Test-Path -LiteralPath $Path)) {
  Write-Error "File not found: $Path"
  exit 2
}

$content = Get-Content -LiteralPath $Path -Raw
$urls = [regex]::Matches($content, 'https?://[^\s\)]+') |
  ForEach-Object { $_.Value.TrimEnd('.', ',', ';') } |
  Sort-Object -Unique

$results = foreach ($url in $urls) {
  $status = 'UNKNOWN'
  $code = ''
  $message = ''
  try {
    $response = Invoke-WebRequest -Uri $url -Method Head -MaximumRedirection 5 -TimeoutSec $TimeoutSec -UseBasicParsing
    $status = 'OK'
    $code = [string][int]$response.StatusCode
  } catch {
    try {
      $response = Invoke-WebRequest -Uri $url -Method Get -MaximumRedirection 5 -TimeoutSec $TimeoutSec -UseBasicParsing
      $status = 'OK_GET'
      $code = [string][int]$response.StatusCode
    } catch {
      $status = 'CHECK_FAILED'
      $message = $_.Exception.Message
      if ($_.Exception.Response -and $_.Exception.Response.StatusCode) {
        $code = [string][int]$_.Exception.Response.StatusCode
      }
    }
  }

  [pscustomobject]@{
    Status = $status
    Code = $code
    Url = $url
    Message = $message
  }
}

$results | Format-Table -AutoSize

$failed = @($results | Where-Object { $_.Status -eq 'CHECK_FAILED' })
if ($failed.Count -gt 0) {
  Write-Host ""
  Write-Host "Some links failed automated checks. For Bilibili and domestic platforms, verify manually before removing."
  exit 1
}

exit 0
