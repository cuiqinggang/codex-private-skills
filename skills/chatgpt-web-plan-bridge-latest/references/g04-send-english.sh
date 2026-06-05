#!/bin/bash
# G04：发送英文 TEST_OK
# 验证真实浏览器操作：点击、输入、发送、截图

set -e
export PATH="$HOME/.npm-global/bin:$HOME/.local/bin:$PATH"

# 动态获取 WSL 网关和 Browser WS
GW=$(ip route show default | awk "{print \$3; exit}")
WS=$(curl --noproxy "*" -sS "http://$GW:9334/json/version" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("webSocketDebuggerUrl",""))')

if [ -z "$WS" ]; then
  echo "G04_FAIL_NO_WS"
  exit 10
fi

MSG="TEST_OK"
SHOT="/tmp/hermes_g04_test_ok.png"

echo "=== G04 SEND_TEST_OK ==="

echo "=== CURRENT_URL ==="
agent-browser --cdp "$WS" get url

# 必须重新 snapshot 获取输入框 ref
SNAP="/tmp/hermes_g04_snapshot.txt"
agent-browser --cdp "$WS" snapshot -i > "$SNAP"
BOX=$(grep -m1 'textbox "与 ChatGPT 聊天"' "$SNAP" | sed -n 's/.*\[ref=\([^]]*\)\].*/\1/p')
if [ -z "$BOX" ]; then
  BOX=$(grep -m1 'textbox' "$SNAP" | sed -n 's/.*\[ref=\([^]]*\)\].*/\1/p')
fi
if [ -z "$BOX" ]; then
  echo "G04_FAIL_NO_TEXTBOX"
  exit 20
fi

echo "TEXTBOX_REF=$BOX"

echo "=== CLICK_INPUT ==="
agent-browser --cdp "$WS" click "$BOX"

echo "=== FILL_INPUT ==="
agent-browser --cdp "$WS" fill "$BOX" "$MSG"

echo "=== PRESS_ENTER ==="
agent-browser --cdp "$WS" press Enter

echo "=== WAIT_12S ==="
sleep 12

echo "=== SCREENSHOT ==="
agent-browser --cdp "$WS" screenshot "$SHOT"

echo "SCREENSHOT_FILE=$SHOT"
echo "G04_DONE"
