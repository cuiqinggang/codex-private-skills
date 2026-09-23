# v0.1.0 Reality Certification

当前状态：

```text
REAL_CERTIFIED=NO
STATUS=PENDING_CODEX_REAL_TEST
```

## 原则

不再用 7GB 文件测试路由本身。路由节点只需要证明：能把代表性小任务正确交给成熟工具，并成功得到有效输出。

## 最小现实测试

### R01 — Hugging Face 小文件

```text
source = Hugging Face
task = 下载公开仓库中的小文件
expected route = hf download
gate = 文件实际存在且命令成功
```

### R02 — GitHub Release 小资产

```text
source = GitHub Release
task = 下载公开 release 的小 checksum/text asset
expected route = gh release download
gate = 文件实际存在且命令成功
```

### R03 — 普通直链

```text
source = 普通 HTTPS 直链
task = 下载一个小型公开文本/二进制文件
expected route = aria2c
gate = 文件实际存在且命令成功
```

### R04 — 多任务

同时提交：

```text
1 个 Hugging Face 小文件
1 个 GitHub Release 小资产
1 个普通 HTTPS 小文件
```

要求：

```text
HF -> hf
GitHub Release -> gh
Direct URL -> aria2c
CUSTOM_QUEUE=NO
ALL_COMPLETED=YES
```

## 计时

沿用外层 v4.6.0 TASK_TIME_ID。

至少记录：

```text
T_ROUTE_DECISION_MS
T_TOOL_START_MS
T_VALID_PER_TASK
T_VALID_MULTI_TASK
```

现实测试只比较有效完成时间，不把下载工具内部实现重新纳入研发。

## PASS

只有：

```text
R01=PASS
R02=PASS
R03=PASS
R04=PASS
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
