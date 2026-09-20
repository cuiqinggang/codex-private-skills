# UPDATE PROTOCOL

目的：以后改变时更新，不覆盖今天的依据。

## 版本

MAJOR：改变三核心、唯一目标、COMMERCIAL_GATE、T0/T1 或 E=(C,P,S,V)。
MINOR：改变 P0 任务、Jev 主版本、基本原语或依赖结构，导致 D_MIN/T_PHY 重算。
PATCH：非语义修正或证据补充。

## 每次更新必须记录

CHANGE_ID
DATE
OLD_VERSION
NEW_VERSION
TRIGGER
NEW_EVIDENCE
AFFECTED_INVARIANTS
AFFECTED_FILES
RECALCULATE_D_MIN=YES/NO
RECALCULATE_T_PHY=YES/NO
REMEASURE_T_REAL_STAR=YES/NO
RERUN_REAL_P0=YES/NO
BACKWARD_COMPATIBLE=YES/NO
SUPERSEDES

## 必须触发更新

Jev 版本或 Provider 变化；
机器、网络、代理、动作后端、verifier 改变并影响现实时间；
发现成熟结构能减少关键路径；
COMMERCIAL_GATE 不足以覆盖真实生产要求；
新普通任务暴露底层缺失的基本原语；
发现伪依赖、oracle 泄露或 benchmark 作弊风险。

## 禁止

直接覆盖旧冻结结果；
为了更快而降低门槛；
把现实数值变化误写成理论结构变化；
拿社区 benchmark 替代当前环境实测；
重新引入成本分、成熟度分等第二主指标。

## 固定更新流程

新事实
→ 判断影响层
→ 从旧版复制为新版本
→ 最小修改
→ 重算受影响物理量
→ 必要现实复测
→ 新 freeze
→ 更新 CURRENT_STATE 与 HISTORY/CHANGELOG
→ 保留旧版。