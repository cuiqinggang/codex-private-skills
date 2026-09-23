# Qwen3.8 / Bonsai 2 27B — 千问3.8 27B1 当前唯一入口（v4.6 能力边界）

```text
PAGE=千问3.8 27B1
TASK_TIME_ID=QWEN38-27B1-20260923T182700+0800
METHOD=极限短时间引擎 v4.6.0
CURRENT_PHASE=实（待现实执行）
VIRTUAL_COMPLETE=YES
REAL_ENTRY=READY
NEXT_SEQUENCE=01
TIME_RESET=FORBIDDEN
```

## 当前目标

不再把项目定义成“单独 256K 收尾”。

唯一产品目标：

```text
本地 Bonsai 2 27B 智能体
+ 可选 JEV 概率判断加速器
+ 自适应 Thinking
+ 独立 deterministic verifier
=> 能力边界图 + 每个 PASS 区域的 min T_VALID
```

## 已完成的虚

- 旧 1018 全量测试宇宙保留；
- 原 16 个 252-255K × HIGH_8192 硬冲突修复；
- 加入显式工具/输出余量后发现的 16 个 MEDIUM 潜在冲突同步 clamp；
- 总 token 溢出 = 0；
- runner + fixture + verifier 绑定完成；
- 1018/1018 零 GPU 自检 PASS；
- 592 原子题压缩为 64 reality anchors，仍覆盖 800/800 pairwise；
- 240 概率题压缩为 24 anchors，仍覆盖 57/57 pairwise；
- Reality runner 假服务器控制链 smoke PASS；
- 现实失败与“能力 FAIL”语义分离：模型 FAIL 用于画边界，只有基础设施/合同矛盾才返虚。

## 冻结资产

目录：

```text
workspaces/qwen38-bonsai2-256k/capability-envelope-v46/
```

权威：

```text
CAPABILITY-ENVELOPE-PATCH-v4.json
BONSAI2-CAPABILITY-ENVELOPE-RUNNER-v2.py
MATERIALIZE-CAPABILITY-ENVELOPE-v1.ps1
ZERO-GPU-SELFTEST-v2.json
ZERO-GPU-RUNNER-BINDING-SMOKE-v1.json
REALITY-BOUNDARY-PLAN-v1.json
Qwen3.8-Bonsai2-v4.6-CAPABILITY-ENVELOPE-VIRTUAL-FREEZE-v1.md
Qwen3.8-Bonsai2-v4.6-CAPABILITY-ENVELOPE-REAL-CONTRACT-v1.md
TIME-LEDGER-v4.6.json
VIRTUAL-FREEZE-AUDIT-v1.md
```

基础 1018 suite 继续复用：

```text
Qwen3.8-27B-Bstar-Executor-Cert-Suite-v3.json
```

运行时由：

```text
v3 suite + CAPABILITY-ENVELOPE-PATCH-v4
```

确定性生成有效 v4 suite，不复制 1.8MB 题库。

## Reality 规则

四定位：

```text
【千问3.8 27B1｜本地智能体能力边界现实验证｜01｜实】
```

现实禁止现场设计。合同/runner/现实底座矛盾：

```text
Reality Delta -> STOP -> 同一 TASK_TIME_ID 返虚
```

模型某一任务失败：

```text
不是 Reality Delta
-> 按冻结邻域规则定位能力边界
-> 记录 FAIL 区域
-> 继续
```

版本变化、现实失败、返虚都不得重置时间。