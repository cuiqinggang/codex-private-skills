# REAL-TASK-04 — mature-download-router v0.1.1

```text
【成熟下载工具最短调用路由｜v0.1.1窄目录现实认证｜04｜实】
TASK_TIME_ID=AED-20260923T1902+0800
TASK_SEQUENCE=04
METHOD=first-principles-physical-limit-convergence@4.6.0
REALITY_FOUNDATION=local-ai-reality-foundation@1.1.4
SKILL=mature-download-router@0.1.1
```

## Reality entry

The Codex session MUST be launched with working directory:

```text
C:\AI\Mature-Download-Router-Real-Test
```

Do not continue if the session reports `directory: ~` or `C:\Users\A`.

## R0
Run a minimal side-effect-free PowerShell process and record Stopwatch timing.
If `SetTokenInformation(TokenDefaultDacl) failed: 1344` occurs in the scoped workdir, retry once using the already-authorized execution channel that previously ran PowerShell 7.6.6 successfully. If that also fails, STOP with `CODEX_WINDOWS_PROCESS_SPAWN_CHANNEL_FAILURE`.

## R1
Read-only:
```text
aria2c --version
hf --version
gh --version   # optional
```
aria2c and hf are hard requirements for this reality test; gh is not.

## R2
```powershell
hf download openai-community/gpt2 config.json --revision 607a30d783dfa663caf39e06633721c8d4cfcd7e --local-dir C:\AI\Mature-Download-Router-Real-Test\<RUN_ID>\R2-hf
```

## R3
```powershell
aria2c --no-conf=true -c -d C:\AI\Mature-Download-Router-Real-Test\<RUN_ID>\R3-aria2 -o README.rst https://raw.githubusercontent.com/aria2/aria2/release-1.37.0/README.rst
```

## R4
Run fresh R2 and R3 tasks concurrently in new subdirectories.
Require:
```text
HF -> hf
Direct URL -> aria2c
ROUTE_MATCH=2/2
ALL_COMPLETED=YES
CUSTOM_DOWNLOADER=NO
CUSTOM_ADAPTER=NO
CUSTOM_QUEUE=NO
CUSTOM_STATUS_UI=NO
```

Use System.Diagnostics.Stopwatch for:
```text
R0_T_MS
R1_T_MS
R2_T_VALID_MS
R3_T_VALID_MS
R4_T_VALID_MS
CODEX_PROCESS_ACTIVE_MS
```

Final output:
```text
【成熟下载工具最短调用路由｜v0.1.1窄目录现实认证｜04｜实】
TASK_TIME_ID=
TASK_SEQUENCE=
WORKDIR=
PROCESS_SPAWN=
R0=
R0_T_MS=
ARIA2_VERSION=
HF_VERSION=
GH_VERSION_OR_NOT_INSTALLED=
R1=
R1_T_MS=
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
CUSTOM_STATUS_UI=
CODEX_PROCESS_ACTIVE_MS=
TIME_ACCOUNTING_COMPLETE=
VALID_REAL=
REALITY_DELTA=
ACTION=
RETURN_TO_VIRTUAL=
RESULT_ROOT=
【成熟下载工具最短调用路由｜v0.1.1窄目录现实认证｜04｜实】
```

PASS only if R0-R4 all pass.
