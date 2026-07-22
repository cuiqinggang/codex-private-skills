[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$InputText,
    [switch]$PrepareBrowser,
    [switch]$FinalizeBrowser,
    [string]$SessionId,
    [switch]$ValidateInputOnly,
    [switch]$ConfirmBatch
)

$entry = 'C:\AI\Douyin-Download-Skill\bin\Download-Douyin.ps1'
if (-not (Test-Path -LiteralPath $entry -PathType Leaf)) {
    Write-Error '下载入口不存在：C:\AI\Douyin-Download-Skill\bin\Download-Douyin.ps1'
    exit 2
}

$parameters = @{ InputText = $InputText }
if ($PrepareBrowser) { $parameters.PrepareBrowser = $true }
if ($FinalizeBrowser) { $parameters.FinalizeBrowser = $true }
if ($SessionId) { $parameters.SessionId = $SessionId }
if ($ValidateInputOnly) { $parameters.ValidateInputOnly = $true }
if ($ConfirmBatch) { $parameters.ConfirmBatch = $true }

& $entry @parameters
exit $LASTEXITCODE
