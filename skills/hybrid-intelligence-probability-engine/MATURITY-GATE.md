# 混合智能概率引擎 v0.2.0 — 成熟门

## 禁止提前宣布成熟

以下任何一项缺失，均不得写“虚拟成熟完成”：

1. 正向拆解技能包存在且可测试；
2. 形式舒适区规则边界穷举 PASS；
3. 自然语言/复杂任务语义拆解 benchmark 有独立 oracle；
4. 正向拆解耗时进入 T_VALID；
5. Full-GPT baseline 从同一原始任务开始；
6. Hybrid 从同一原始任务开始；
7. 两者使用同一最终 verifier；
8. Virtual-99 给出明确数值 T_VIRTUAL_STAR；
9. 虚拟时间收益和成本收益给出明确数值；
10. Reality runner 冻结；
11. 现实只剩不可虚拟的外部变量。

## Reality 认证

Reality 必须实际得到：

- T_FULL_GPT_REAL_MIN
- T_HYBRID_REAL_MIN
- T_FULL_GPT_REAL_P50
- T_HYBRID_REAL_P50
- E2E_TIME_SPEEDUP_REAL
- E2E_COST_SPEEDUP_REAL
- REAL_COMPILER_TIME
- JEV_TIME
- GPT_RESIDUAL_TIME
- VERIFIER_TIME
- RESULT_SHA256

并满足商业有效门后，才能写：
REALITY_CERTIFIED=YES

## 历史数据规则

JEV v0.4.0 的 560.9819 ms 是概率核心历史现实锚点。

它不得作为：
- 本次混合引擎新收益；
- 完整 Hybrid T_VALID；
- v0.2.0 的升级收益。

旧 v0.3 → v0.4 的 33.2645% / 1.49845x 只属于 JEV 自己的历史升级，不属于本项目本轮收益。
