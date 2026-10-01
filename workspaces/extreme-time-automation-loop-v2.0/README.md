# 极限短时间自动化闭环 v2.0

```ini
PROJECT=极限短时间自动化闭环
VERSION=v2.0
PAGE_NAME=极限短时间自动化闭环 v2.0
STATE=10
PHASE=STANDARD_REALITY_BENCHMARK_COMPETITION
VIRTUAL_MATURE=NO
PROJECT_FREEZE=NO
FINAL_VALID=NO

CONSTITUTION_VERSION=v0.3
CONSTITUTION_FREEZE_ID=ETAC-v0.3-FREEZE-R1
OBJECTIVE=T*=min(T_VALID)

CORE_BRAIN=GPT
CODEX=MEASURED_EXECUTOR_CANDIDATE
MANUS_2=BENCHMARK_ONLY
BACKUP_PATH_REQUIRED=YES
```

## 1. 项目目标

建立一组真实、可重复的**极限短时间自动化 Benchmark Cases**。

每个 Case 都来自已经完成的成熟真实任务。

不同成熟路径跑同一题，真实测得 T_VALID，然后：

```text
比较
→ 分析
→ 删除
→ 组合
→ Virtual Mature
→ Reality
→ 持续攻击当前最短有效时间
```

唯一目标始终是：

```text
T* = min(T_VALID)
```

## 2. 固定核心与可替换部分

GPT 是当前固定超级大脑。

Codex、Browser、GitHub、n8n、OpenClaw、API、MCP、CLI 等都是可竞争成熟能力：
- 有完整 T_VALID 收益则保留；
- 无收益则删除；
- 不因为历史使用习惯保护任何执行器。

Manus 2.0 只用现有积分做成熟商业 Benchmark，不进入正式主链。

## 3. 当前标准题

### Case 001
**抖音极速直下 Windows v1.0.0**

适度复杂、用户级 E2E，覆盖 Browser / Windows / fallback / 文件 / 媒体验收。

详见：
- `BENCHMARK_SUITE_R1.md`
- `BENCHMARK_CASE_001_DOUYIN.md`

### Calibration Anchor 000
**JEV Probability Engine P0 v0.4.0**

已认证：
`T_REAL_STAR_MS=560.9819`，30/30 PASS。

它只用于短时计时和攻击方法校准，不替代 Case 001。

## 4. 第一轮 Reality

```text
C0 Direct Mature
→ P1 GPT / Work
→ P2 GPT / Work + Codex
→ B1 Manus 2.0
```

同一轮必须同 Case、同样本、同 FINAL_VALID。

## 5. 两类时间不能混淆

### 物理执行参考
`T_DIRECT_MATURE_REF_CASE_001`

成熟最终方案直接执行的现实参考。

### 智能路径完整时间
`T_VALID_*`

从智能系统可开始推进到 FINAL_VALID 的完整现实时间。

真正路径竞争只比较同边界的 T_VALID。

## 6. 当前现实极限

```text
T_REAL_PHYSICAL_STAR_CASE
= 同一 Case 当前所有已测 VALID 路径中的最短 T_VALID
```

新的成熟路径只要 Reality 更短，就更新当前 Reality Star。

## 7. 下一步

先跑 Case 001 的 C0，重新测最终完成版成熟方案。

旧 Reality 02/03 时间因后续音频 / 播放 VALID 曾重新打开，只保留历史，不作为当前最终基线。

得到 C0 后依次跑 P1 / P2 / B1。

第一轮结束后再进入 Virtual Mature 攻击。

当前仍为 STATE=10。
