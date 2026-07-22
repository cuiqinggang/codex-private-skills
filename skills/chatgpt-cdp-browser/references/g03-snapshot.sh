#!/bin/bash
# G03：接入浏览器并读取 snapshot
# 只做接入与读取，不做操作

set -e
export PATH="$HOME/.npm-global/bin:$HOME/.local/bin:$PATH"

# 动态获取 WSL 网关和 Browser WS
GW=$(ip route show default | awk "{print \$3; exit}")
WS=$(curl --noproxy "*" -sS "http://$GW:9334/json/version" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("webSocketDebuggerUrl",""))')

if [ -z "$WS" ]; then
  echo "G03_FAIL_NO_WS"
  exit 10
fi

echo "=== G03 HERMES_BROWSER_ATTACH_CHECK ==="

echo "=== CHECK_AGENT_BROWSER ==="
echo "AGENT_BROWSER=$(command -v agent-browser || echo MISSING)"

echo "=== TAB ==="
agent-browser --cdp "$WS" tab

echo "=== CURRENT_URL ==="
agent-browser --cdp "$WS" get url

echo "=== SNAPSHOT_HEAD_160 ==="
agent-browser --cdp "$WS" snapshot -i | tee /tmp/hermes_g03_snapshot.txt | head -n 160

echo "SNAPSHOT_FILE=/tmp/hermes_g03_snapshot.txt"
echo "G03_DONE"
