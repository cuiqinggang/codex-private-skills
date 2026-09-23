# v0.1.1 Reality Certification

```text
REAL_CERTIFIED=NO
STATUS=PENDING_CODEX_REAL_TEST
TASK_TIME_ID=AED-20260923T1902+0800
```

## R0 — Executor Entry

先运行一个最小无副作用命令。

若默认 Codex Windows 执行通道返回：

```text
SetTokenInformation(TokenDefaultDacl) failed: 1344
```

则只重试一次“同一环境中已经存在、已授权、上一现实会话曾成功运行 PowerShell 7.6.6”的替代执行通道。

替代通道也不能创建进程：

```text
VALID_REAL=FAIL
REALITY_DELTA=CODEX_WINDOWS_PROCESS_SPAWN_CHANNEL_FAILURE
STOP
```

不得写成 DOWNLOAD_TOOL_MISSING。

## R1 — Reality Tool Check

成功进入命令宿主后：

```text
aria2c --version
hf --version
```

已有现实证据表明二者存在，本次只确认当前版本与可执行性。

`gh` 只做可选检查，不作为 PASS 硬门。

## R2 — HF Small Download

```text
openai-community/gpt2
config.json
revision=607a30d783dfa663caf39e06633721c8d4cfcd7e
-> hf download
```

PASS = 命令成功 + 文件存在 + size>0。

## R3 — Direct URL Small Download

```text
https://raw.githubusercontent.com/aria2/aria2/release-1.37.0/README.rst
-> aria2c
```

PASS = 命令成功 + 文件存在 + size>0。

## R4 — Two-task Mixed Download

同时提交新的两个独立小任务：

```text
HF -> hf
Direct URL -> aria2c
```

不建立自定义下载队列。

PASS：

```text
ROUTE_MATCH=2/2
ALL_COMPLETED=YES
CUSTOM_DOWNLOADER=NO
CUSTOM_ADAPTER=NO
CUSTOM_QUEUE=NO
```

## Time

使用 System.Diagnostics.Stopwatch：

```text
R0_T_MS
R1_T_MS
R2_T_VALID_MS
R3_T_VALID_MS
R4_T_VALID_MS
CODEX_PROCESS_ACTIVE_MS
```

## Final PASS

```text
R0=PASS
R1=PASS
R2=PASS
R3=PASS
R4=PASS
TIME_ACCOUNTING_COMPLETE=PASS
=> REAL_CERTIFIED=YES
```

任何失败只返回最小 Reality Delta，不现场重做方案。
