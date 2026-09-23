# v0.1.2 Reality Certification

```text
REAL_CERTIFIED=NO
STATUS=PENDING_CODEX_REAL_TEST
TASK_TIME_ID=AED-20260923T1902+0800
```

## R0 — Executor Entry

工作目录必须是：

```text
C:\AI\Mature-Download-Router-Real-Test
```

该目录在 REAL 04 已得到 `PROCESS_SPAWN=PASS`，因此本轮只确认没有回归。

## R1 — Tool + Network Context

只读确认：

```text
aria2c --version
hf --version
gh --version  # optional
```

已知 REAL 04：

```text
aria2c=1.37.0
hf=1.19.0
gh=2.92.0
```

然后只读解析当前已经存在的网络上下文：
- process HTTP_PROXY / HTTPS_PROXY / ALL_PROXY；
- Git 已有 http.proxy / https.proxy；
- Reality Foundation 已记录候选 `http://127.0.0.1:7890`。

禁止扫描端口、禁止猜新端口、禁止修改任何代理设置。

对候选 endpoint 只做最小可达性检查。找到当前可工作的既有 endpoint 后，冻结为本轮 `CURRENT_NETWORK_CONTEXT`。

若全部已有 endpoint 都不可用且直连也不可用：
```text
VALID_REAL=FAIL
REALITY_DELTA=NO_CURRENT_DOWNLOAD_NETWORK_PATH
STOP
```

## R2 — HF small file

在同一个命令进程中仅设置 process-local：

```text
HTTP_PROXY=<CURRENT_NETWORK_CONTEXT>
HTTPS_PROXY=<CURRENT_NETWORK_CONTEXT>
```

然后：

```powershell
hf download openai-community/gpt2 config.json --revision 607a30d783dfa663caf39e06633721c8d4cfcd7e --local-dir <RUN>\R2-hf
```

PASS = exit 0 + config.json exists + size > 0。

## R3 — aria2 small file

```powershell
aria2c --no-conf=true -c --all-proxy=<CURRENT_NETWORK_CONTEXT> -d <RUN>\R3-aria2 -o README.rst https://raw.githubusercontent.com/aria2/aria2/release-1.37.0/README.rst
```

若本轮冻结的网络上下文是 DIRECT，则不传 `--all-proxy`。

PASS = exit 0 + README.rst exists + size > 0。

## R4 — Mixed two-task route

使用新目录，提交：
```text
HF -> hf + same frozen network context
Direct URL -> aria2c + same frozen network context
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

必须有一个覆盖本轮 R0-R4 的外层 `System.Diagnostics.Stopwatch`，并可另记录阶段局部时间。

最终至少：
```text
R0_T_MS
R1_T_MS
R2_T_VALID_MS
R3_T_VALID_MS
R4_T_VALID_MS
CODEX_PROCESS_ACTIVE_MS
TIME_ACCOUNTING_COMPLETE=PASS
```

## PASS

只有 R0-R4 全部 PASS 才允许 `REAL_CERTIFIED=YES`。

任何失败只返回最小 Reality Delta，不现场重新设计路由或代理。
