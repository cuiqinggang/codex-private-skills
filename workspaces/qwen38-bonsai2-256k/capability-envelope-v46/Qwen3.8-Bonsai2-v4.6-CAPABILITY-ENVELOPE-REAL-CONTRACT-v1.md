# 千问3.8 27B1 — Bonsai 2 27B 本地智能体能力边界｜v4.6 现实验证冻结合同 v1

## 0. 四定位与时间接力

```text
【千问3.8 27B1｜本地智能体能力边界现实验证｜01｜实】
TASK_TIME_ID=QWEN38-27B1-20260923T182700+0800
TIME_RESET=FORBIDDEN
NO_REAL_REDESIGN=YES
```

执行器开头和最后一行必须原样回显同一标签。

Reality 继续同一时间账本；版本变化、FAIL、返虚均不得新建计时起点。

## 1. 角色

```text
GPT=冻结方案 + 最终判断
CODEX=机械执行 runner / 收集现实证据
BONSAI2=被测本地智能体
JEV=可选概率加速器，不是硬依赖
DETERMINISTIC_RUNNER=独立验证器/控制器
```

Codex 不得替 Bonsai 作答，不得修模型输出。

## 2. 冻结资产

```text
BASE_SUITE=Qwen3.8-27B-Bstar-Executor-Cert-Suite-v3.json
PATCH=CAPABILITY-ENVELOPE-PATCH-v4.json
EFFECTIVE_SUITE=运行时由 v3 + patch 确定性生成
RUNNER=BONSAI2-CAPABILITY-ENVELOPE-RUNNER-v2.py
SELFTEST=ZERO-GPU-SELFTEST-v2.json
PLAN=REALITY-BOUNDARY-PLAN-v1.json
```

Reality 开始前必须校验文件 SHA/存在性；缺失即 Reality Delta + STOP，不现场重新生成。

## 3. Reality Foundation

复用：

```text
ROOT=C:\AI\Bonsai2-27B-256K
MODEL=Ternary-Bonsai-2-27B-PQ2_0.gguf
MODEL_BYTES=7206168928
MODEL_SHA256=3907dc1658db1f78a9826bf8d5bcb8dc65db0d466388937af57f2294fae62ec1
CTX=262144
GPU=RTX 2080 Ti
RUNTIME=IvyBridge-compatible / CUDA sm_75 / Prism commit 9a9394a...
PRIMARY_KV=q8_0
```

禁止重新下载、重新编译、换模型、换代理。

## 4. 开始顺序

1. 再跑一次 runner `--self-test`，必须 1018/1018 PASS、GPU=0。
2. 检查 llama-server /health、模型 hash、Runtime、GPU/VRAM、262144。
3. 启动/复用冻结 server；reasoning/cache/context-checkpoint 参数按既有 v4.6 Runtime 合同。
4. 执行 `REALITY-BOUNDARY-PLAN-v1.json`。
5. 先 64 atomic anchors（32 request groups），再进入概率/Thinking/长流程的冻结 ladder。
6. FAIL/ambiguous 只按 suite 中已冻结的邻域 expansion 规则扩展；不得现场发明新题。
7. 写能力边界图、每个 PASS 区域的 `T_VALID/P50/P95`、首个稳定 FAIL 边界。
8. STOP -> GPT final judge。

## 5. 现实最短化

### Atomic

```text
592 full catalog
-> 64 pairwise anchors
-> 32 batched request groups
```

仍覆盖：

```text
800/800 pairwise combinations
```

### 长上下文

使用 nested shared prefix（嵌套共享前缀）：

```text
8K -> 32K -> 64K -> 128K -> 192K -> 224K -> 240-245K -> 252-255K
```

`cache_prompt=true`；每个更大 band 只新增 suffix/delta，不重复从 0 冷 Prefill。

### JEV

外部 JEV adapter 缺失或网络/API 失败：

```text
不是整体 FAIL
-> LOCAL_BONSAI_STRUCTURED_DECISION
```

只有同任务 A/B 证明：

```text
QUALITY_JEV=PASS
AND
T_VALID_JEV < T_VALID_LOCAL
```

才把该类任务路由给 JEV。

## 6. Thinking

```text
OFF          明确确定任务
LOW_512      轻微歧义
MEDIUM_2048  局部失败
HIGH_8192    多回执冲突
GPT          HIGH 后仍不能安全收敛/需要重设计
```

252-255K 档使用总 token 包络；Thinking 越高，prompt payload 自动减小，不允许超过 262144。

## 7. VALID

现实最终不是要求“1018 全 PASS”。

最终有效结果是：

```text
CAPABILITY_ENVELOPE_COMPLETE=YES
PASS_REGIONS_VERIFIED=YES
FAIL_BOUNDARIES_LOCATED=YES
ROUTE_TABLE_FROZEN=YES
TIME_TABLE_FROZEN=YES
NO_FALSE_PASS=YES
NO_SCOPE_ESCAPE=YES
TIME_ACCOUNTING_COMPLETE=YES
```

FAIL 是能力边界数据，不自动等于项目失败。

只有 runner / verifier /计时合同 /现实底座本身失效才是 Reality Delta，需要返虚。

## 8. 输出

必须写：

```text
RESULT.json
CAPABILITY-ENVELOPE.json
ROUTE-TABLE.json
TIME-TABLE.json
REALITY-DELTA.json (无差异则 NONE)
TIME-LEDGER-UPDATE.json
```

并记录至少：

```text
T_CASE_TOTAL
T_PREFILL
T_REASONING
T_DECODE
T_TOOL
T_VERIFY
T_RECOVERY
T_VALID
P50
P95
```

## 9. STOP

Reality 不修方案。

```text
合同本身矛盾/runner故障/现实依赖变化
-> Reality Delta
-> STOP
-> RETURN_TO_VIRTUAL
-> 同一 TASK_TIME_ID
```

模型某任务 FAIL：

```text
-> 记录能力边界
-> 按冻结邻域规则补最少案例
-> 继续，不重设计
```

最终最后一行必须是：

```text
【千问3.8 27B1｜本地智能体能力边界现实验证｜01｜实】
```