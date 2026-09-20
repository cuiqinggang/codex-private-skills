# UPDATE PROTOCOL — 更新而不丢历史

本文件解决：以后现实环境、Jev、任务结构或方法发生变化时，如何更新而不是覆盖今天的依据。

## 1. 真值优先级
1. 当前版本 freeze / Virtual-99 freeze。
2. CURRENT_STATE.md。
3. CHANGELOG.md 与对应版本历史。
4. 原始来源/实验记录。

旧版本不删除，只声明被哪个版本替代以及原因。

## 2. 版本规则
- MAJOR：改变三核心、唯一目标、COMMERCIAL_GATE、T0/T1 或 E=(C,P,S,V) 核心抽象。
- MINOR：新增/替换 P0 任务、Jev 主版本、状态/动作原语，或改变最小依赖结构/关键屏障。
- PATCH：文字、证据补充、非语义错误修正。

## 3. 每次更新必须记录
```text
CHANGE_ID=
DATE=
OLD_VERSION=
NEW_VERSION=
TRIGGER=
NEW_EVIDENCE=
AFFECTED_INVARIANTS=
AFFECTED_FILES=
RECALCULATE_MODEL_BARRIER=YES/NO
RECALCULATE_ACTION_DEPENDENCY=YES/NO
RECALCULATE_T_PHY=YES/NO
REMEASURE_T_REAL_STAR=YES/NO
RERUN_REAL_P0=YES/NO
BACKWARD_COMPATIBLE=YES/NO
SUPERSEDES=
```

## 4. 必须触发更新的事件
- Jev 版本、Provider 或 API 语义变化。
- 网络、机器、代理、动作后端、Verifier 改变且影响现实时间。
- 发现更成熟结构能减少关键路径。
- COMMERCIAL_GATE 不能覆盖生产要求。
- 新普通任务暴露缺失基本原语。
- 发现伪依赖、oracle 泄露或 benchmark 作弊风险。

## 5. 不允许
- 直接改旧冻结结果，让历史看起来从未变化。
- 为迁就更快结果降低门槛。
- 把现实数值变化误写成理论结构变化。
- 用社区 benchmark 覆盖当前现实锚定。
- 新增成本分、成熟度分等并列主指标。

## 6. 更新流程
新事实 → 识别受影响层 → 旧版为新版本起点 → 最小修改 → 重算受影响物理量 → 必要现实复测 → 新 freeze → CURRENT_STATE/CHANGELOG → 旧版永久保留。

## 7. 0.2.0 起必须分离屏障类型
不得用一个裸 D_MIN 同时代表全部依赖。至少区分：
- MODEL_BARRIER_DEPTH：必须串行等待的概率/模型波次。
- ACTION_DEPENDENCY_DEPTH：真实动作/receipt 的因果层数。
- FINAL_VERIFY_BARRIERS：无法与动作隐藏的最终验证屏障。

若 speculative precompute 可以消除模型等待，应重算 model barrier；但不能因此提前提交依赖真实结果的动作。
