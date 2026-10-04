param([string]$BridgeWorkDir,[string]$TaskFile)
$ErrorActionPreference='Stop'
$runtime='C:\AI\ltmvh-v03-test\skills\long-term-memory-super-virtual-human\runtime'
& 'C:\Program Files\nodejs\node.exe' "$runtime\goal-loop-reality.js"
if($LASTEXITCODE -ne 0){throw 'Goal loop real process fixture failed'}
Write-Output 'LTMVH-V050-FALLBACK-BRIDGE-REAL-COMMAND-PASS'
