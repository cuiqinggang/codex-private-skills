# REAL-TASK-03 — mature-download-router v0.1.1

```text
【成熟下载工具最短调用路由｜v0.1.1最小现实认证｜03｜实】
TASK_TIME_ID=AED-20260923T1902+0800
TASK_SEQUENCE=03
METHOD=first-principles-physical-limit-convergence@4.6.0
REALITY_FOUNDATION=local-ai-reality-foundation@1.1.4
SKILL=mature-download-router@0.1.1
```

## 启动要求（重要）

这次不要从 `~` / `C:\Users\A` 启动 workspace-write。

先建立并把 Codex 工作目录固定为：

```text
C:\AI\Mature-Download-Router-Real-Test
```

现实依据：当前 Codex Windows 已知可在 Home workspace 出现 `SetTokenInformation(TokenDefaultDacl) failed: 1344`；该错误发生在目标命令真正启动之前，不得归因给 aria2/hf。

## R0 — Executor Entry

在上述窄工作目录启动后，先执行一个最小无副作用 PowerShell 命令。

PASS：
```text
PROCESS_SPAWN=PASS
```

如果仍为同类 1344：
只允许重试一次上一现实会话已授权且曾成功运行 PowerShell 7.6.6 的执行通道。

仍失败：
```text
VALID_REAL=FAIL
REALITY_DELTA=CODEX_WINDOWS_PROCESS_SPAWN_CHANNEL_FAILURE
ACTION=STOP
RETURN_TO_VIRTUAL=YES
```

## R1 — Tool Check

只读：

```text
aria2c --version
hf --version
```

`gh` 只记录（若存在），不是硬门。

上一现实证据已经确认 aria2c 与 hf 存在；本轮只验证“当前可执行 + 精确版本”。

## R2 — HF 小文件

```powershell
hf download openai-community/gpt2 config.json --revision 607a30d783dfa663caf39e06633721c8d4cfcd7e --local-dir C:\AI\Mature-Download-Router-Real-Test\R2-hf
```

PASS：
```text
EXIT=0
config.json exists
size>0
```

## R3 — aria2 小文件

```powershell
aria2c --no-conf=true -c -d C:\AI\Mature-Download-Router-Real-Test\R3-aria2 -o README.rst https://raw.githubusercontent.com/aria2/aria2/release-1.37.0/README.rst
```

PASS：
```text
EXIT=0
README.rst exists
size>0
```

## R4 — 两任务同时路由

使用新的子目录，同时提交：

```text
HF public small file -> hf
Direct HTTPS small file -> aria2c
```

要求：

```text
ROUTE_MATCH=2/2
ALL_COMPLETED=YES
CUSTOM_DOWNLOADER=NO
CUSTOM_ADAPTER=NO
CUSTOM_QUEUE=NO
```

## Timing

使用 System.Diagnostics.Stopwatch 记录：

```text
R0_T_MS
R1_T_MS
R2_T_VALID_MS
R3_T_VALID_MS
R4_T_VALID_MS
CODEX_PROCESS_ACTIVE_MS
```

## 最终输出

```text
【成熟下载工具最短调用路由｜v0.1.1最小现实认证｜03｜实】
TASK_TIME_ID=
TASK_SEQUENCE=
WORKDIR=
PROCESS_SPAWN=
ARIA2_VERSION=
HF_VERSION=
GH_VERSION_OR_NOT_INSTALLED=
R2_ROUTE=
R2=
R2_T_VALID_MS=
R3_ROUTE=
R3=
R3_T_VALID_MS=
R4_ROUTE_MATCH=
R4=
R4_T_VALID_MS=
CUSTOM_DOWNLOADER=
CUSTOM_ADAPTER=
CUSTOM_QUEUE=
TIME_ACCOUNTING_COMPLETE=
VALID_REAL=
REALITY_DELTA=
ACTION=
RETURN_TO_VIRTUAL=
RESULT_ROOT=
【成熟下载工具最短调用路由｜v0.1.1最小现实认证｜03｜实】
```

只有 R0-R4 全 PASS 才：
```text
VALID_REAL=PASS
ACTION=STOP_RETURN_TO_GPT_FOR_FINAL_VALIDATION
RETURN_TO_VIRTUAL=NO
```

否则：
```text
VALID_REAL=FAIL
ACTION=STOP
RETURN_TO_VIRTUAL=YES
```
