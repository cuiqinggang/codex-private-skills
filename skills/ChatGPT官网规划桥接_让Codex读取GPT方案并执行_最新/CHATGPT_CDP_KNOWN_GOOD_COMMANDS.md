# ChatGPT CDP 已验证可用命令索引

> 最后更新：2026-04-26  
> 版本：v1.1  
> 搜索关键词：ChatGPT CDP 命令、agent-browser 命令、CDP 已验证命令

---

## 1. 动态获取关键值

### 获取 WSL 网关
```bash
ip route show default | awk "{print \$3; exit}"
```
本次结果：`192.168.128.1`

### 获取 Browser WebSocket URL
```bash
GW=$(ip route show default | awk "{print \$3; exit}")
curl --noproxy "*" -sS "http://$GW:9334/json/version" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("webSocketDebuggerUrl",""))'
```

---

## 2. agent-browser 核心命令

### 列出标签页
```bash
agent-browser --cdp "$WS" tab
```

### 获取当前 URL
```bash
agent-browser --cdp "$WS" get url
```

### 读取页面 snapshot
```bash
agent-browser --cdp "$WS" snapshot -i
```

### 点击元素
```bash
agent-browser --cdp "$WS" click "$REF"
```

### 输入文本（填入输入框）
```bash
agent-browser --cdp "$WS" fill "$REF" "$TEXT"
```

### 按 Enter 发送
```bash
agent-browser --cdp "$WS" press Enter
```

### 截图
```bash
agent-browser --cdp "$WS" screenshot "$PATH"
```

---

## 3. 中文输入的 UTF-8 文件方式

### 生成中文 UTF-8 文件
```bash
python3 - <<'PY' > /tmp/hermes_msg.txt
print("\u8bf7\u7528\u4e09\u53e5\u8bdd\u8bf4\u660e\uff1a\u4ec0\u4e48\u662f\u6628\u65e5\u91cd\u73b0\u6cd5\uff1f")
PY
```

### 用 UTF-8 文件内容填入输入框
```bash
agent-browser --cdp "$WS" fill "$BOX" "$(cat /tmp/hermes_msg.txt)"
```

⚠️ Unicode 转义对照：
- `\u8bf7\u7528\u4e09\u53e5\u8bdd\u8bf4\u660e\uff1a\u4ec0\u4e48\u662f\u6628\u65e5\u91cd\u73b0\u6cd5\uff1f`
- = `请用三句话说明：什么是昨日重现法？`

### 验证文件内容
```bash
python3 -c 'from pathlib import Path; p=Path("/tmp/hermes_msg.txt"); b=p.read_bytes(); print("LEN="+str(len(b))); print("HEX="+b[:80].hex()); print("TEXT="+p.read_text("utf-8").strip())'
```

---

## 4. 动态获取输入框 ref

```bash
SNAP="/tmp/hermes_snapshot.txt"
agent-browser --cdp "$WS" snapshot -i > "$SNAP"

BOX=$(grep -m1 'textbox "与 ChatGPT 聊天"' "$SNAP" | sed -n 's/.*\[ref=\([^]]*\)\].*/\1/p')
if [ -z "$BOX" ]; then
  BOX=$(grep -m1 'textbox' "$SNAP" | sed -n 's/.*\[ref=\([^]]*\)\].*/\1/p')
fi
echo "TEXTBOX_REF=$BOX"
```

---

## 5. Windows PowerShell 关键命令

### 启动调试 Chrome（从 WSL 通过 /init 桥接）
```powershell
$chrome = "$env:ProgramFiles\Google\Chrome\Application\chrome.exe"
$profile = Join-Path $env:USERPROFILE "Desktop\Hermes_CDP_Chrome_Profile"
Start-Process -FilePath $chrome -ArgumentList @(
  "--remote-debugging-address=127.0.0.1",
  "--remote-debugging-port=9333",
  "--user-data-dir=$profile",
  "--no-first-run",
  "--new-window",
  "https://chatgpt.com/"
)
```

### 建立 portproxy 9334→9333
```powershell
cmd /c "netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=9334 >nul 2>nul"
cmd /c "netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=9334 connectaddress=127.0.0.1 connectport=9333"
```

### 防火墙放行 9334
```powershell
$ruleName = "Hermes Chrome CDP 9334"
$rule = Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue
if (-not $rule) {
  New-NetFirewallRule -DisplayName $ruleName -Direction Inbound -Action Allow -Protocol TCP -LocalPort 9334 | Out-Null
}
```

### 验证 9333/9334
```powershell
Invoke-RestMethod "http://127.0.0.1:9333/json/version"
Invoke-RestMethod "http://127.0.0.1:9334/json/version"
```

---

## 6. 从 WSL 调 PowerShell 的正确方式

```bash
/init /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -Command "Get-Process chrome | Select-Object -First 1"
```

⚠️ 不能直接调 `powershell.exe`（会报 Exec format error）。  
⚠️ 混合脚本（PS+WSL）必须拆分执行。  
详见 skill `wsl-init-powershell`。

---

## 7. PATH 修复（每个 WSL 脚本开头必加）

```bash
export PATH="$HOME/.npm-global/bin:$HOME/.local/bin:$PATH"
```

---

## 8. 完整发送一条中文消息的最小命令序列

```bash
export PATH="$HOME/.npm-global/bin:$HOME/.local/bin:$PATH"

# 1. 获取 WS
GW=$(ip route show default | awk "{print \$3; exit}")
WS=$(curl --noproxy "*" -sS "http://$GW:9334/json/version" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("webSocketDebuggerUrl",""))')

# 2. Snapshot 获取输入框 ref
agent-browser --cdp "$WS" snapshot -i > /tmp/snap.txt
BOX=$(grep -m1 'textbox "与 ChatGPT 聊天"' /tmp/snap.txt | sed -n 's/.*\[ref=\([^]]*\)\].*/\1/p')

# 3. 写中文消息到 UTF-8 文件
python3 -c 'print("\u4f60\u597d")' > /tmp/msg.txt

# 4. 点击、输入、发送
agent-browser --cdp "$WS" click "$BOX"
agent-browser --cdp "$WS" fill "$BOX" "$(cat /tmp/msg.txt)"
agent-browser --cdp "$WS" press Enter

# 5. 等待、截图
sleep 15
agent-browser --cdp "$WS" screenshot /tmp/result.png
```
