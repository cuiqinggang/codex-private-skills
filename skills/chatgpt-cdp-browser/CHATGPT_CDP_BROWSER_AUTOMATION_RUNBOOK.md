# ChatGPT CDP 浏览器自动化 — 完整复盘文档

> 执行体：爱马仕数字助手 / Hermes Agent  
> 创建日期：2026-04-25  
> 版本：v1.1（完整版，含全部内嵌命令）  
> 状态：链路已通，v1.1 完整复盘版  
> 搜索关键词：ChatGPT CDP、浏览器自动化、agent-browser、9333、9334、UTF-8 中文

---

## 0. 技能名称

chatgpt-cdp-browser

## 1. 技能用途

本技能用于让爱马仕数字助手接入一个已经登录 GPT Plus 的调试版 Google Chrome，并对 ChatGPT 页面执行连续自动操作。

典型用途：
1. 打开已登录 GPT Plus 的 ChatGPT 页面
2. 通过 Chrome CDP 接入浏览器
3. 读取页面 snapshot
4. 识别输入框
5. 自动输入问题
6. 按 Enter 发送
7. 等待回答
8. 截图留证
9. 连续执行多轮问题

**适合**：需要连续自动操作 ChatGPT 页面时使用。  
**不适合**：只是看截图、识别页面、判断下一步时使用。如果只是识别截图，优先使用多模态视觉模型；如果要连续点击、输入、发送、截图，则使用本技能。

---

## 2. 本次最终成功结论

本次已经成功打通：
```
Windows 调试版 Chrome
→ 9333 原始调试口
→ 9334 Windows/WSL 统一入口
→ WSL / 爱马仕侧访问
→ agent-browser
→ ChatGPT 页面
→ 自动点击输入框
→ 自动输入英文 TEST_OK
→ 自动输入 UTF-8 中文问题
→ 按 Enter 发送
→ 等待回复
→ 截图留证
```

验证结果：
- G01：启动调试版 Chrome，并登录 GPT Plus —— PASS
- G02：打通 9333 → 9334 → WSL 访问 —— PASS
- G03：agent-browser 接入 ChatGPT 页面并读取 snapshot —— PASS
- G04：发送 TEST_OK 并截图 —— PASS
- G05：直接中文输入失败，显示问号 —— FAIL，已定位
- G05-FIX：用 UTF-8 文件方式输入中文 —— PASS

---

## 3. 当前已验证的关键环境

### 3.1 Windows 调试 Chrome 原始端口
`127.0.0.1:9333`

### 3.2 Windows / WSL 统一入口
`0.0.0.0:9334 → 127.0.0.1:9333`

### 3.3 WSL 网关
本次实际检测到：`192.168.128.1`

⚠️ 旧方案里常见的是 `172.28.48.1`，但本次实际是 `192.168.128.1`。  
以后不能死写旧网关，必须每次用命令动态检测：
```bash
ip route show default | awk "{print \$3; exit}"
```

### 3.4 本次成功 Browser WS
`ws://192.168.128.1:9334/devtools/browser/1f1d7ca3-a0bc-445b-b3e7-ec5fe77cfc86`

⚠️ 这个 Browser WS **不是永久固定值**。Chrome 重启后，最后那段 browser UUID 可能变化。  
规则：每次重开调试 Chrome 后，必须重新读取 `/json/version`，获取当前 webSocketDebuggerUrl。

### 3.5 调试 Chrome 专用用户目录
${REDACTED_SECRET}

### 3.6 爱马仕侧关键命令路径
```
agent-browser = /home/u123456/.npm-global/bin/agent-browser
hermes        = /home/u123456/.local/bin/hermes
```

### 3.7 PATH 必须包含
```bash
export PATH="$HOME/.npm-global/bin:$HOME/.local/bin:$PATH"
```
否则会出现：`agent-browser: command not found` / `hermes: command not found`

---

## 4. 标准总流程

```
G01 启动调试版 Chrome
G02 建立并验证 9334 统一入口
G03 爱马仕接入浏览器，读取 snapshot
G04 发送英文 TEST_OK
G05-FIX 发送 UTF-8 中文问题
G06 后续发送真实任务问题
```

---

## 5. G01：启动调试版 Chrome，并登录 GPT Plus

**目标**：启动一个可被爱马仕接管的调试版 Chrome。

**Windows PowerShell 命令**：
```powershell
$ErrorActionPreference = 'Stop'

$chromeCandidates = @(
  "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
  "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
  "$env:LocalAppData\Google\Chrome\Application\chrome.exe"
)

$chrome = $chromeCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1

if (-not $chrome) {
  Write-Host "G01_FAIL_CHROME_NOT_FOUND"
  return
}

$profile = Join-Path $env:USERPROFILE "Desktop\Hermes_CDP_Chrome_Profile"
New-Item -ItemType Directory -Force -Path $profile | Out-Null

Start-Process -FilePath $chrome -ArgumentList @(
  "--remote-debugging-address=127.0.0.1",
  "--remote-debugging-port=9333",
  "--user-data-dir=$profile",
  "--no-first-run",
  "--new-window",
  "https://chatgpt.com/"
)

Start-Sleep -Seconds 3

try {
  $r = Invoke-RestMethod "http://127.0.0.1:9333/json/version"
  Write-Host "G01_PASS"
  Write-Host "BROWSER=$($r.Browser)"
  Write-Host "WIN_WS=$($r.webSocketDebuggerUrl)"
  Write-Host "PROFILE=$profile"
}
catch {
  Write-Host "G01_FAIL_9333_NOT_READY"
  Write-Host $_.Exception.Message
}
```

**本次成功输出**：
```
G01_PASS
BROWSER=Chrome/147.0.7727.102
WIN_WS=ws://127.0.0.1:9333/devtools/browser/1f1d7ca3-a0bc-445b-b3e7-ec5fe77cfc86
${REDACTED_SECRET}
```

**人工动作**：用户在这个调试版 Chrome 中手动登录 GPT Plus。  
通过条件：
1. 打开 https://chatgpt.com/
2. GPT Plus 已登录
3. 能看到聊天输入框

---

## 6. G02：建立并验证 9334 统一入口

**目标**：让 WSL / 爱马仕能通过 9334 访问 Windows 调试 Chrome 的 9333。

**Windows PowerShell 命令**：
```powershell
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

Write-Host "=== CHECK_WSL_TO_9334 ==="

$script = @'
set -e

GW=$(ip route show default | awk "{print \$3; exit}")
echo "WSL_GATEWAY=$GW"

env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY -u all_proxy -u ALL_PROXY -u no_proxy -u NO_PROXY \
curl --noproxy "*" -sS "http://$GW:9334/json/version" > /tmp/hermes_cdp_9334.json

python3 -c 'import json; d=json.load(open("/tmp/hermes_cdp_9334.json")); print("WSL_9334_PASS"); print("WSL_BROWSER="+d.get("Browser","")); print("WSL_WS="+d.get("webSocketDebuggerUrl",""))'
'@

$script | wsl -d Ubuntu-24.04 -u u123456 -e bash -s

Write-Host "G02_DONE"
```

**本次成功输出**：
```
WIN_9333_PASS
WIN_9334_PASS
WSL_GATEWAY=192.168.128.1
WSL_9334_PASS
WSL_BROWSER=Chrome/147.0.7727.102
WSL_WS=ws://192.168.128.1:9334/devtools/browser/1f1d7ca3-a0bc-445b-b3e7-ec5fe77cfc86
G02_DONE
```

**成功判定**：必须同时看到 `WIN_9333_PASS`、`WIN_9334_PASS`、`WSL_9334_PASS`、`G02_DONE`

---

## 7. G03：接入浏览器并读取 snapshot

**目标**：只做接入与读取，不做操作。

G03 不会点击、不会输入、不会发送。它只是：
1. tab：列出当前标签页
2. get url：读取当前地址
3. snapshot -i：读取页面结构

本次 G03 输出里已经识别到 ChatGPT 页面和输入框，例如 `textbox "与 ChatGPT 聊天"`；这证明爱马仕已能读取页面结构，但还没有真正操作页面。

**Windows PowerShell 命令**：
```powershell
$WS = "ws://192.168.128.1:9334/devtools/browser/1f1d7ca3-a0bc-445b-b3e7-ec5fe77cfc86"

$script = @'
set -e
export PATH="$HOME/.npm-global/bin:$HOME/.local/bin:$PATH"

WS="__WS__"

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
'@

$script = $script.Replace("__WS__", $WS)
$script | wsl -d Ubuntu-24.04 -u u123456 -e bash -s
```

**本次成功证据**：
```
AGENT_BROWSER=/home/u123456/.npm-global/bin/agent-browser
→ [t1] ChatGPT - https://chatgpt.com/
CURRENT_URL=https://chatgpt.com/
textbox "与 ChatGPT 聊天" [ref=e144]
SNAPSHOT_FILE=/tmp/hermes_g03_snapshot.txt
G03_DONE
```

⚠️ 输入框 ref 不是固定值。本次曾出现 e144、e151、e161。每次页面变化后必须重新 snapshot。

---

## 8. G04：发送英文 TEST_OK

**目标**：验证真实浏览器操作：点击、输入、发送、截图。

**Windows PowerShell 命令**：
```powershell
$WS = "ws://192.168.128.1:9334/devtools/browser/1f1d7ca3-a0bc-445b-b3e7-ec5fe77cfc86"

$script = @'
set -e
export PATH="$HOME/.npm-global/bin:$HOME/.local/bin:$PATH"

WS="__WS__"
MSG="TEST_OK"
SHOT="/tmp/hermes_g04_test_ok.png"

echo "=== G04 SEND_TEST_OK ==="

echo "=== CURRENT_URL ==="
agent-browser --cdp "$WS" get url

echo "=== CLICK_INPUT ==="
agent-browser --cdp "$WS" click e144

echo "=== FILL_INPUT ==="
agent-browser --cdp "$WS" fill e144 "$MSG"

echo "=== PRESS_ENTER ==="
agent-browser --cdp "$WS" press Enter

echo "=== WAIT_12S ==="
sleep 12

echo "=== SCREENSHOT ==="
agent-browser --cdp "$WS" screenshot "$SHOT"

echo "SCREENSHOT_FILE=$SHOT"
echo "G04_DONE"
'@

$script = $script.Replace("__WS__", $WS)
$script | wsl -d Ubuntu-24.04 -u u123456 -e bash -s
```

**本次成功输出**：
```
=== CLICK_INPUT ===
✓ Done
=== FILL_INPUT ===
✓ Done
=== PRESS_ENTER ===
✓ Done
=== SCREENSHOT ===
✓ Screenshot saved to /tmp/hermes_g04_test_ok.png
SCREENSHOT_FILE=/tmp/hermes_g04_test_ok.png
G04_DONE
```

**页面验证**：页面出现 TEST_OK，GPT 回复"TEST_OK 已收到"。

---

## 9. G05：直接中文输入失败

**目标**：发送中文短问题：请用三句话说明：什么是昨日重现法？

**失败现象**：命令执行成功（click/fill/press/screenshot 全部 ✓ Done），但页面和命令行里中文变成：`?????????????????`

**失败判断**：浏览器操作没问题；失败点是 PowerShell → WSL → bash 传中文时编码损坏。

**不能再用的方式**：
```bash
MSG="请用三句话说明：什么是昨日重现法？"
agent-browser --cdp "$WS" fill "$BOX" "$MSG"
# 这会在某些 PowerShell / WSL 组合里变成问号。
```

---

## 10. G05-FIX：UTF-8 文件方式解决中文输入

**核心思路**：不要直接从 PowerShell here-string 里传中文。改用 Python Unicode 转义生成 UTF-8 文件 → WSL 内读取 UTF-8 文件 → agent-browser fill。

**Windows PowerShell 命令**：
```powershell
$WS = "ws://192.168.128.1:9334/devtools/browser/1f1d7ca3-a0bc-445b-b3e7-ec5fe77cfc86"

$script = @'
set -e
export PATH="$HOME/.npm-global/bin:$HOME/.local/bin:$PATH"

WS="__WS__"
SNAP="/tmp/hermes_g05_fix_snapshot.txt"
MSGFILE="/tmp/hermes_g05_fix_msg.txt"
SHOT="/tmp/hermes_g05_fix_chinese_utf8.png"

echo "=== G05_FIX_SEND_UTF8_CHINESE ==="

echo "=== WRITE_UTF8_MESSAGE ==="
python3 - <<'PY' > /tmp/hermes_g05_fix_msg.txt
print("\u8bf7\u7528\u4e09\u53e5\u8bdd\u8bf4\u660e\uff1a\u4ec0\u4e48\u662f\u6628\u65e5\u91cd\u73b0\u6cd5\uff1f")
PY

echo "=== VERIFY_MESSAGE_HEX ==="
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
'@

$script = $script.Replace("__WS__", $WS)
$script | wsl -d Ubuntu-24.04 -u u123456 -e bash -s
```

**本次成功输出**：
```
MSG_BYTES_LEN=52
MSG_TEXT=请用三句话说明：什么是昨日重现法？
TEXTBOX_REF=e161
✓ Done
✓ Screenshot saved to /tmp/hermes_g05_fix_chinese_utf8.png
G05_FIX_DONE
```

**最终结论**：中文输入问题已解决。以后中文内容必须优先采用 UTF-8 文件方式。

---

## 11. 中间犯过的错误与纠正

### 错误 1：把旧方案里的"小龙虾/OpenClaw"继续当执行体
- **现象**：旧文档中写的是：小龙虾 / OpenClaw
- **纠正**：当前迁移后统一改为：爱马仕数字助手 / Hermes Agent
- **新规则**：以后所有 GPT 页面自动化，默认执行体是爱马仕。

### 错误 2：误以为可以直接复用旧登录状态
- **现象**：一开始按旧方案倾向于"先复用旧登录状态"
- **纠正**：正确成熟流程是：先打开调试版 Chrome → 用户登录 GPT Plus → 爱马仕接入这个已登录调试浏览器
- **新规则**：默认先启动调试版 Chrome，并由用户登录 GPT Plus。不要默认旧状态一定可复用。

### 错误 3：第一次 G02 使用复杂嵌套引号导致 bash 解析失败
- **报错**：`unexpected EOF while looking for matching ')'`
- **原因**：PowerShell + bash -lc + 嵌套引号太复杂
- **纠正**：改成 PowerShell here-string → 通过管道送入 WSL bash -s。以后复杂脚本都用这个方式。

### 错误 4：G03 初次发现 agent-browser 缺失
- **报错**：`AGENT_BROWSER_MISSING`
- **原因**：WSL 中没有可执行的 agent-browser 命令
- **纠正**：安装：`npm install -g agent-browser`

### 错误 5：npm 安装后仍然找不到 agent-browser / hermes
- **报错**：`bash: hermes: command not found` / `AGENT_BROWSER_STILL_MISSING`
- **原因**：当前非交互 WSL shell 没加载 PATH
- **纠正**：每次脚本开头加入：`export PATH="$HOME/.npm-global/bin:$HOME/.local/bin:$PATH"`

### 错误 6：hermes config get toolsets 不支持
- **报错**：`hermes config: error: argument config_command: invalid choice: 'get'`
- **原因**：当前 Hermes 版本没有 config get 子命令
- **纠正**：不要使用 `hermes config get toolsets`，改用 `hermes config show`

### 错误 7：G03 只是读取页面，不是操作页面
- **现象**：用户看到终端输出很多 snapshot 内容，但浏览器没有动作
- **原因**：G03 只做 tab / get url / snapshot -i，都是读取动作
- **纠正**：真正操作从 G04 开始：click / fill / press Enter / screenshot

### 错误 8：直接中文输入变成问号
- **现象**：页面显示 `?????????????????`，命令行显示 `QUESTION=?????????????????`
- **原因**：PowerShell here-string 到 WSL/bash 的中文编码被破坏
- **纠正**：用 Python Unicode 转义写入 UTF-8 文件，再 cat 文件 fill

---

## 12. 固定执行原则

### 12.1 每次都要动态获取
1. WSL_GATEWAY
2. WSL_WS
3. 输入框 ref

不要长期死用：`172.28.48.1`、`e144`、旧 Browser WS

### 12.2 每次发送前必须 snapshot
原因：ChatGPT 页面一变化，输入框 ref 就可能变化。本次 ref 变化例子：e144、e151、e161。

### 12.3 中文输入必须用 UTF-8 文件方式
不要直接在 PowerShell 里写中文变量传给 WSL。

### 12.4 一次只发一条消息
不要一条命令连续发多条。先发一条，等待返回，截图留证，再进入下一条。

### 12.5 失败立即停止
不要补丁式乱试。停止条件：
1. 9333 不通
2. 9334 不通
3. agent-browser 找不到
4. 当前 URL 不是 chatgpt.com
5. snapshot 看不到 textbox
6. click/fill/press 失败
7. 中文变问号
8. 截图失败

---

## 13. 成功回报格式

每次任务完成后，必须按这个格式回报：

```
《ChatGPT CDP 自动化任务回报》

1. 调试 Chrome：
- G01：通过/失败
- Browser：
- WIN_WS：
- Profile：

2. 统一入口：
- G02：通过/失败
- WSL_GATEWAY：
- WSL_WS：

3. 接入浏览器：
- G03：通过/失败
- 当前 URL：
- snapshot 文件：
- 输入框 ref：

4. 消息发送：
- G04/G05：通过/失败
- 发送内容：
- click 输出：
- fill 输出：
- press Enter 输出：

5. 中文编码：
- 是否使用 UTF-8 文件方式：
- MSG_TEXT：
- 是否出现问号：

6. 截图留证：
- screenshot 输出：
- 截图路径：

7. 本次总结果：
- PASS / FAIL
- 失败停在哪一关：
```

---

## 14. 本次最终状态摘要

当前链路已通。爱马仕已经能操作已登录 GPT Plus 的调试版 Chrome。
- 英文 TEST_OK 已验证通过。
- 中文 UTF-8 问题已验证通过。

当前成功截图：
```
/tmp/hermes_g04_test_ok.png
/tmp/hermes_g05_fix_chinese_utf8.png
```

当前关键入口：
```
Chrome 9333：127.0.0.1:9333
统一入口：0.0.0.0:9334 → 127.0.0.1:9333
本次 WSL 网关：192.168.128.1
本次 WSL_WS：ws://192.168.128.1:9334/devtools/browser/1f1d7ca3-a0bc-445b-b3e7-ec5fe77cfc86
```

当前关键命令：
```
agent-browser=/home/u123456/.npm-global/bin/agent-browser
hermes=/home/u123456/.local/bin/hermes
```

关键修复：
- 每个 WSL 脚本开头必须加：`export PATH="$HOME/.npm-global/bin:$HOME/.local/bin:$PATH"`
- 中文修复：不要直接传中文变量，用 Python Unicode 写 UTF-8 文件，再 cat 文件 fill。

---

## 16. 最短昨日重现口令

以后需要重新启用这套路径时，对爱马仕说：

> 加载 chatgpt-cdp-browser skill。按昨日重现法启动调试版 Chrome，确认 GPT Plus 已登录，打通 9333→9334→WSL，读取当前 WSL_WS，snapshot 获取输入框 ref，然后用 UTF-8 文件方式发送一条中文测试消息并截图留证。禁止使用旧 WS，禁止跳过 snapshot，禁止直接从 PowerShell 传中文。

---

## 15. 保存验收要求

每次更新本技能包后，必须保存以下 4 个文件并执行验收：

| 序号 | 文件 | 用途 |
|------|------|------|
| 1 | `~/.hermes/skills/chatgpt-cdp-browser/SKILL.md` | Hermes 可加载技能 |
| 2 | `~/.hermes/workspace/memory/03_projects/hermes/CHATGPT_CDP_BROWSER_AUTOMATION_RUNBOOK.md` | 本复盘文档 |
| 3 | `~/.hermes/workspace/memory/03_projects/hermes/ACTIVE_CHATGPT_CDP_STATUS.md` | 当前状态摘要 |
| 4 | `~/.hermes/workspace/memory/03_projects/hermes/CHATGPT_CDP_KNOWN_GOOD_COMMANDS.md` | 命令索引 |

验收命令：
```bash
ls -lh ~/.hermes/skills/chatgpt-cdp-browser/SKILL.md \
      ~/.hermes/workspace/memory/03_projects/hermes/CHATGPT_CDP_BROWSER_AUTOMATION_RUNBOOK.md \
      ~/.hermes/workspace/memory/03_projects/hermes/ACTIVE_CHATGPT_CDP_STATUS.md \
      ~/.hermes/workspace/memory/03_projects/hermes/CHATGPT_CDP_KNOWN_GOOD_COMMANDS.md

sha256sum ~/.hermes/skills/chatgpt-cdp-browser/SKILL.md \
          ~/.hermes/workspace/memory/03_projects/hermes/CHATGPT_CDP_BROWSER_AUTOMATION_RUNBOOK.md \
          ~/.hermes/workspace/memory/03_projects/hermes/ACTIVE_CHATGPT_CDP_STATUS.md \
          ~/.hermes/workspace/memory/03_projects/hermes/CHATGPT_CDP_KNOWN_GOOD_COMMANDS.md

head -n 20 ~/.hermes/skills/chatgpt-cdp-browser/SKILL.md
```

回报格式：
```
文件1: 路径 | 大小 | 前20行摘要
文件2: 路径 | 大小 | 前20行摘要
文件3: 路径 | 大小 | 前20行摘要
文件4: 路径 | 大小 | 前20行摘要
最终: PASS / FAIL
```

---

## 最终一句话

这次真正打通的是：爱马仕 + agent-browser + Chrome CDP + GPT Plus 调试浏览器自动操作链路。
最大坑有三个：9334/WSL 网关不能死写、agent-browser/hermes PATH 必须补齐、中文必须用 UTF-8 文件方式输入。
