# v0.1.0 Reality Certification

当前状态：

```text
REAL_CERTIFIED=NO
STATUS=PENDING_CODEX_REAL_TEST
```

## 1. 原则

不再用 7GB 文件测试路由本身。路由节点只需要证明：能把代表性小任务正确交给成熟工具，并成功得到有效输出。

冻结工具版本基线：

```text
aria2=1.37.0
GitHub CLI=2.101.0
huggingface_hub=1.32.0
```

现实开始先只读检查本机版本。工具已存在但版本不同，不得现场重构方案；记录实际版本。工具缺失则返回最小 Reality Delta，不伪造 PASS。

## 2. 固定现实测试

测试根目录：

```text
C:\AI\Mature-Download-Router-Real-Test
```

### R01 — Hugging Face 单文件

固定公开资源：

```text
repo=openai-community/gpt2
revision=607a30d783dfa663caf39e06633721c8d4cfcd7e
file=config.json
route=hf download
```

调用：

```powershell
hf download openai-community/gpt2 config.json --revision 607a30d783dfa663caf39e06633721c8d4cfcd7e --local-dir <ROOT>\hf
```

PASS：

```text
TOOL=hf
EXIT=0
OUTPUT=<ROOT>\hf\config.json EXISTS
```

### R02 — GitHub Release 小资产

固定公开资源：

```text
repo=cli/cli
release=v2.101.0
asset=gh_2.101.0_checksums.txt
expected_sha256=f8bbc37fc5568a6a162d1a67b1e9c1afa9139f7b5a46dcde4a57bdaa0db33b60
route=gh release download
```

调用：

```powershell
gh release download v2.101.0 -R cli/cli -p gh_2.101.0_checksums.txt -D <ROOT>\gh
```

PASS：

```text
TOOL=gh
EXIT=0
OUTPUT EXISTS
SHA256=expected
```

### R03 — 普通 HTTPS 直链

固定公开资源：

```text
url=https://raw.githubusercontent.com/aria2/aria2/release-1.37.0/README.rst
route=aria2c
```

调用：

```powershell
aria2c --no-conf=true -c -d <ROOT>\aria2 -o README.rst https://raw.githubusercontent.com/aria2/aria2/release-1.37.0/README.rst
```

PASS：

```text
TOOL=aria2c
EXIT=0
OUTPUT=<ROOT>\aria2\README.rst EXISTS
OUTPUT_LENGTH>0
```

### R04 — 多任务

同时启动 R01、R02、R03 三个独立成熟工具任务。

要求：

```text
HF -> hf
GitHub Release -> gh
Direct URL -> aria2c
CUSTOM_QUEUE=NO
CUSTOM_ADAPTER=NO
ALL_COMPLETED=YES
```

这里验证的是“混合任务仍只做确定性分发”，不是重新制造统一下载队列。

## 3. 计时

沿用外层：

```text
TASK_TIME_ID=AED-20260923T1902+0800
```

至少记录：

```text
T_ROUTE_DECISION_MS
R01_T_VALID_MS
R02_T_VALID_MS
R03_T_VALID_MS
R04_T_VALID_MS
CODEX_PROCESS_ACTIVE_MS
```

持续时间使用 System.Diagnostics.Stopwatch。

不把用户等待时间伪装成智能体有效工作时间。

## 4. PASS

只有：

```text
R01=PASS
R02=PASS
R03=PASS
R04=PASS
ROUTE_MATCH=4/4
OUTPUT_VALID=PASS
TIME_ACCOUNTING_COMPLETE=PASS
```

才允许升级：

```text
REAL_CERTIFIED=YES
```

任何失败：

```text
REALITY_DELTA=<最小差异>
ACTION=STOP
RETURN_TO_VIRTUAL=YES
```

禁止在 REAL 阶段修改路由规则、换 benchmark 或自建下载组件。
