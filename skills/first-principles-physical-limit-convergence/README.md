# 第一性原理极限短时间引擎 v4.0.0

## 当前方法：一虚一实

```text
虚拟成熟
→ 冻结唯一方案 S*
→ 实际验证
→ PASS：冻结现实最优
→ FAIL：Reality Delta → STOP → 回虚拟成熟
```

只有两步。

### 虚拟成熟

负责“想清楚并冻结”：
- 读取本地 AI 现实底座 / Exact Reality Twin；
- 动态重新检索成熟方案，不把旧方案当永久最佳；
- 组合、删除、冲突消解、攻击、模拟、验证；
- 只保留 HARD_GATES=PASS 的方案；
- 以预测 `T_VALID` 最短为唯一比较标准；
- 输出唯一冻结合同。

### 实际验证

负责“实打实证明”：
- Codex / Reasonix / 本地执行器只执行冻结合同；
- 记录现实 `T_VALID`；
- verifier 判定 VALID；
- 失败只记录 Reality Delta 并停止；
- 不在现实端自行修复。

## 唯一锚定物

```text
T_VALID = 从任务开始到第一个 VALID 现实结果
T* = min(T_VALID)
```

极限短时间就是极限效率。
质量、正确性、安全、成本、资源等是 HARD GATES，不是并列评分。

## v4 为什么是重大版本

v3.1.9 的当前方法是：
```text
极限短时间
→ 成熟方案集群
→ 高智能虚拟成熟
→ 现实验证
```

v4.0.0 把“极限短时间”提升为全流程唯一锚定，把“成熟方案池 + Reality Twin”变成虚拟成熟的永久输入资产，因此当前执行方法只剩：

```text
一虚一实
```

## 底层永久资产

入口：

```text
skills/local-ai-reality-foundation/
```

它维护 Reality Fingerprint、Exact Twin、浏览器、网络、本地 GPU/LLM、ComfyUI/视觉、本地自动化等现实资产索引。
只在漂移或缺证据时增量更新，不每次全量锚定。

## 历史兼容

v1.x–v3.1.9 不删除。
旧分支、旧证据、旧失败、旧 Reality baseline 全部保留。

当前权威历史索引：

```text
skills/first-principles-physical-limit-convergence/HISTORY-v1-v3.1.9.md
```

正式 v4 分支：

```text
codex/first-principles-physical-limit-convergence-v4.0.0
```
