# G02：建立并验证 9334 统一入口
# 从 WSL 通过 /init 桥接执行（仅 Windows 侧 PowerShell 部分）
# WSL 侧操作需单独在 WSL bash 中执行

$ErrorActionPreference = 'Stop'

Write-Host "=== G02 REBUILD_AND_VERIFY_9334 ==="

Write-Host "=== CHECK_WINDOWS_9333 ==="
try {
    $win9333 = Invoke-RestMethod "http://127.0.0.1:9333/json/version"
    Write-Host "WIN_9333_PASS"
    Write-Host "WIN_BROWSER=$($win9333.Browser)"
    Write-Host "WIN_WS=$($win9333.webSocketDebuggerUrl)"
}
catch {
    Write-Host "WIN_9333_FAIL"
    Write-Host $_.Exception.Message
    return
}

Write-Host "=== RESET_PORTPROXY_9334_TO_9333 ==="
cmd /c "netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=9334 >nul 2>nul"
cmd /c "netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=9334 connectaddress=127.0.0.1 connectport=9333"

Write-Host "=== FIREWALL_9334 ==="
$ruleName = "Hermes Chrome CDP 9334"
$rule = Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue
if (-not $rule) {
    New-NetFirewallRule -DisplayName $ruleName -Direction Inbound -Action Allow -Protocol TCP -LocalPort 9334 | Out-Null
    Write-Host "FIREWALL_RULE_CREATED"
}
else {
    Set-NetFirewallRule -DisplayName $ruleName -Enabled True -Action Allow | Out-Null
    Write-Host "FIREWALL_RULE_EXISTS"
}

Write-Host "=== CHECK_WINDOWS_9334 ==="
try {
    $win9334 = Invoke-RestMethod "http://127.0.0.1:9334/json/version"
    Write-Host "WIN_9334_PASS"
    Write-Host "WIN_9334_WS=$($win9334.webSocketDebuggerUrl)"
}
catch {
    Write-Host "WIN_9334_FAIL"
    Write-Host $_.Exception.Message
    return
}

Write-Host "G02_PS_DONE"
Write-Host "=== WSL侧需单独执行以下验证 ==="
Write-Host "GW=$(ip route show default | awk '{print $3; exit}')"
Write-Host "curl --noproxy '*' -sS http://$GW:9334/json/version"
