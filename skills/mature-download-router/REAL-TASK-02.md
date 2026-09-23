# REAL-TASK-02 — mature-download-router v0.1.0

```text
【成熟下载工具最短调用路由｜v0.1.0现实认证｜02｜实】

TASK_TIME_ID=AED-20260923T1902+0800
TASK_SEQUENCE=02
METHOD=first-principles-physical-limit-convergence@4.6.0
REALITY_FOUNDATION=local-ai-reality-foundation@1.1.3
SKILL=mature-download-router@0.1.0
GPT_DISPATCH_TIMESTAMP=2026-09-23T21:25:29+08:00
```

## 目标

只认证“智能体下载任务 -> 成熟工具”的最短路由是否现实可用。

禁止重新设计下载器、适配器、队列、状态页、选源算法。
禁止执行 7GB 大文件测试。
禁止修改代理、FlClash、TUN、Windows 代理或注册表。
禁止 git fetch 作为启动依赖。

## 现实工具基线

```text
aria2=1.37.0
GitHub CLI=2.101.0
huggingface_hub=1.32.0
```

第一步只读检查：

```text
aria2c --version
gh --version
hf --version
```

缺失或无法执行时：

```text
VALID_REAL=FAIL
REALITY_DELTA=<具体缺失/版本差异>
ACTION=STOP
RETURN_TO_VIRTUAL=YES
```

不要现场安装或升级。

## 计时

进入任务立刻记录 System.Diagnostics.Stopwatch。

测试根目录：

```text
C:\AI\Mature-Download-Router-Real-Test
```

每个测试使用独立子目录，旧结果若存在则先创建新的 RUN_ID 子目录，不覆盖旧证据。

## R01 — Hugging Face

路由必须是：

```text
HUGGING_FACE -> hf download
```

执行：

```powershell
hf download openai-community/gpt2 config.json --revision 607a30d783dfa663caf39e06633721c8d4cfcd7e --local-dir <ROOT>\R01-hf
```

PASS：

```text
EXIT=0
<ROOT>\R01-hf\config.json EXISTS
SIZE>0
```

记录 R01_T_VALID_MS。

## R02 — GitHub Release

路由必须是：

```text
GITHUB_RELEASE -> gh release download
```

执行：

```powershell
gh release download v2.101.0 -R cli/cli -p gh_2.101.0_checksums.txt -D <ROOT>\R02-gh
```

PASS：

```text
EXIT=0
FILE EXISTS
SHA256=f8bbc37fc5568a6a162d1a67b1e9c1afa9139f7b5a46dcde4a57bdaa0db33b60
```

记录 R02_T_VALID_MS。

## R03 — 普通直链

路由必须是：

```text
DIRECT_URL -> aria2c
```

执行：

```powershell
aria2c --no-conf=true -c -d <ROOT>\R03-aria2 -o README.rst https://raw.githubusercontent.com/aria2/aria2/release-1.37.0/README.rst
```

PASS：

```text
EXIT=0
<ROOT>\R03-aria2\README.rst EXISTS
SIZE>0
```

记录 R03_T_VALID_MS。

## R04 — 多任务现实路由

同时启动以下三个已冻结任务，不增加自定义队列层：

```text
HF task -> hf
GitHub Release task -> gh
Direct URL task -> aria2c
```

允许成熟工具各自管理内部下载行为。

三个输出使用新的 R04 子目录，不能依赖 R01-R03 的已有输出。

PASS：

```text
ROUTE_MATCH=3/3
ALL_COMPLETED=YES
CUSTOM_DOWNLOADER=NO
CUSTOM_ADAPTER=NO
CUSTOM_QUEUE=NO
```

记录 R04_T_VALID_MS。

## 最终

必须输出：

```text
【成熟下载工具最短调用路由｜v0.1.0现实认证｜02｜实】
TASK_TIME_ID=
TASK_SEQUENCE=
ARIA2_VERSION=
GH_VERSION=
HF_VERSION=
R01_ROUTE=
R01=
R01_T_VALID_MS=
R02_ROUTE=
R02=
R02_T_VALID_MS=
R03_ROUTE=
R03=
R03_T_VALID_MS=
R04_ROUTE_MATCH=
R04=
R04_T_VALID_MS=
CUSTOM_DOWNLOADER=
CUSTOM_ADAPTER=
CUSTOM_QUEUE=
TIME_ACCOUNTING_COMPLETE=
VALID_REAL=
REALITY_DELTA=
ACTION=
RETURN_TO_VIRTUAL=
RESULT_ROOT=
【成熟下载工具最短调用路由｜v0.1.0现实认证｜02｜实】
```

只有 R01-R04 全部 PASS：

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
