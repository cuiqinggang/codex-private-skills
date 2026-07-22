$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $Root "scripts\self_test.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
