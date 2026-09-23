# REAL-TASK-05 — mature-download-router v0.1.2

```text
【成熟下载工具最短调用路由｜v0.1.2网络继承现实认证｜05｜实】
TASK_TIME_ID=AED-20260923T1902+0800
TASK_SEQUENCE=05
METHOD=first-principles-physical-limit-convergence@4.6.0
REALITY_FOUNDATION=local-ai-reality-foundation@1.1.5
SKILL=mature-download-router@0.1.2
```

## 0. 只做冻结方案现实认证

禁止：
- 自建下载器/适配器/队列/状态页；
- 修改 Windows / FlClash / Git 持久代理配置；
- 扫描未知端口或猜代理；
- 安装/升级工具；
- 重新设计路由。

工作目录：
```text
C:\AI\Mature-Download-Router-Real-Test
```

进入任务立刻启动一个覆盖 R0-R4 的外层 `System.Diagnostics.Stopwatch`。

## R0 — Executor

运行最小无副作用命令。

要求：
```text
PROCESS_SPAWN=PASS
```

## R1 — Tool + existing network context

只读记录：

```text
aria2c --version
hf --version
gh --version  # optional
```

已知上轮：
```text
aria2c=1.37.0
hf=1.19.0
gh=2.92.0
```

只读读取现有：
- process HTTP_PROXY / HTTPS_PROXY / ALL_PROXY
- git config --get http.proxy
- git config --get https.proxy

并包含 Reality Foundation 已知候选：
```text
http://127.0.0.1:7890
```

禁止扫描其他端口。

对这些“已有候选”做最小连通性验证，选择当前能工作的一个作为：

```text
CURRENT_NETWORK_CONTEXT
```

如果直连可用，也允许：
```text
CURRENT_NETWORK_CONTEXT=DIRECT
```

如果已有候选都不可用且直连也不可用：

```text
VALID_REAL=FAIL
REALITY_DELTA=NO_CURRENT_DOWNLOAD_NETWORK_PATH
ACTION=STOP
RETURN_TO_VIRTUAL=YES
```

## R2 — Hugging Face small file

创建新 RUN_ID 目录。

若 CURRENT_NETWORK_CONTEXT != DIRECT，在同一个 PowerShell 命令进程中临时设置：

```powershell
$env:HTTP_PROXY='<CURRENT_NETWORK_CONTEXT>'
$env:HTTPS_PROXY='<CURRENT_NETWORK_CONTEXT>'
```

然后执行：

```powershell
hf download openai-community/gpt2 config.json --revision 607a30d783dfa663caf39e06633721c8d4cfcd7e --local-dir C:\AI\Mature-Download-Router-Real-Test\<RUN_ID>\R2-hf
```

PASS：
```text
EXIT=0
config.json EXISTS
SIZE>0
```

不得修改持久环境变量。

## R3 — aria2 small file

若 CURRENT_NETWORK_CONTEXT != DIRECT：

```powershell
aria2c --no-conf=true -c --all-proxy='<CURRENT_NETWORK_CONTEXT>' -d C:\AI\Mature-Download-Router-Real-Test\<RUN_ID>\R3-aria2 -o README.rst https://raw.githubusercontent.com/aria2/aria2/release-1.37.0/README.rst
```

若 DIRECT，则去掉 `--all-proxy`。

PASS：
```text
EXIT=0
README.rst EXISTS
SIZE>0
```

## R4 — two-task mixed route

使用全新子目录，同时提交：

```text
HF -> hf + CURRENT_NETWORK_CONTEXT
Direct URL -> aria2c + CURRENT_NETWORK_CONTEXT
```

要求：

```text
ROUTE_MATCH=2/2
ALL_COMPLETED=YES
CUSTOM_DOWNLOADER=NO
CUSTOM_ADAPTER=NO
CUSTOM_QUEUE=NO
CUSTOM_STATUS_UI=NO
```

## Timing

记录：

```text
R0_T_MS
R1_T_MS
R2_T_VALID_MS
R3_T_VALID_MS
R4_T_VALID_MS
CODEX_PROCESS_ACTIVE_MS
```

外层 Stopwatch 从 R0 前启动，到最终结果输出前停止：

```text
TIME_ACCOUNTING_COMPLETE=PASS
```

## Final output

```text
【成熟下载工具最短调用路由｜v0.1.2网络继承现实认证｜05｜实】
TASK_TIME_ID=
TASK_SEQUENCE=
WORKDIR=
PROCESS_SPAWN=
ARIA2_VERSION=
HF_VERSION=
GH_VERSION_OR_NOT_INSTALLED=
CURRENT_NETWORK_CONTEXT=
R0=
R0_T_MS=
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
【成熟下载工具最短调用路由｜v0.1.2网络继承现实认证｜05｜实】
```

Only if R0-R4 all PASS:
```text
VALID_REAL=PASS
ACTION=STOP_RETURN_TO_GPT_FOR_FINAL_VALIDATION
RETURN_TO_VIRTUAL=NO
```

Else:
```text
VALID_REAL=FAIL
ACTION=STOP
RETURN_TO_VIRTUAL=YES
```
