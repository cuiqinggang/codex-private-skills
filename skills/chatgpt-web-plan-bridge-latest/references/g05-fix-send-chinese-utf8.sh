#!/bin/bash
# G05-FIX：用 UTF-8 文件方式发送中文问题
# 核心思路：不要直接从 PowerShell 传中文变量，改用 Python Unicode 转义生成 UTF-8 文件

set -e
export PATH="$HOME/.npm-global/bin:$HOME/.local/bin:$PATH"

# 动态获取 WSL 网关和 Browser WS
GW=$(ip route show default | awk "{print \$3; exit}")
WS=$(curl --noproxy "*" -sS "http://$GW:9334/json/version" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("webSocketDebuggerUrl",""))')

if [ -z "$WS" ]; then
  echo "G05_FIX_FAIL_NO_WS"
  exit 10
fi

SNAP="/tmp/hermes_g05_fix_snapshot.txt"
MSGFILE="/tmp/hermes_g05_fix_msg.txt"
SHOT="/tmp/hermes_g05_fix_chinese_utf8.png"

echo "=== G05_FIX_SEND_UTF8_CHINESE ==="

echo "=== WRITE_UTF8_MESSAGE ==="
# ⚠️ 这里用 Python Unicode 转义写中文，避免 PowerShell/WSL 编码问题
# 修改下面这行来更换发送的中文内容：
python3 - <<'PY' > /tmp/hermes_g05_fix_msg.txt
print("\u8bf7\u7528\u4e09\u53e5\u8bdd\u8bf4\u660e\uff1a\u4ec0\u4e48\u662f\u6628\u65e5\u91cd\u73b0\u6cd5\uff1f")
PY

echo "=== VERIFY_MESSAGE ==="
python3 - <<'PY'
from pathlib import Path
p = Path("/tmp/hermes_g05_fix_msg.txt")
b = p.read_bytes()
print("MSG_BYTES_LEN=" + str(len(b)))
print("MSG_UTF8_HEX_HEAD=" + b[:80].hex())
print("MSG_TEXT=" + p.read_text(encoding="utf-8").strip())
PY

echo "=== CURRENT_URL ==="
agent-browser --cdp "$WS" get url

echo "=== SNAPSHOT_REFRESH ==="
agent-browser --cdp "$WS" snapshot -i > "$SNAP"

BOX=$(grep -m1 'textbox "与 ChatGPT 聊天"' "$SNAP" | sed -n 's/.*\[ref=\([^]]*\)\].*/\1/p')
if [ -z "$BOX" ]; then
  BOX=$(grep -m1 'textbox' "$SNAP" | sed -n 's/.*\[ref=\([^]]*\)\].*/\1/p')
fi

if [ -z "$BOX" ]; then
  echo "G05_FIX_FAIL_NO_TEXTBOX"
  echo "SNAPSHOT_FILE=$SNAP"
  exit 20
fi

echo "TEXTBOX_REF=$BOX"

echo "=== CLICK_INPUT ==="
agent-browser --cdp "$WS" click "$BOX"

echo "=== FILL_UTF8_CHINESE ==="
agent-browser --cdp "$WS" fill "$BOX" "$(cat "$MSGFILE")"

echo "=== PRESS_ENTER ==="
agent-browser --cdp "$WS" press Enter

echo "=== WAIT_20S ==="
sleep 20

echo "=== SCREENSHOT ==="
agent-browser --cdp "$WS" screenshot "$SHOT"

echo "MSG_FILE=$MSGFILE"
echo "SNAPSHOT_FILE=$SNAP"
echo "SCREENSHOT_FILE=$SHOT"
echo "G05_FIX_DONE"
