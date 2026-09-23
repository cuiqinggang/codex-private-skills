# 混合智能概率引擎 v0.2.0 — 完整任务计时合同

## 比较对象

Full-GPT 与 Hybrid 必须从完全相同的原始任务开始。

禁止给任一路径预先提供：
- CODE/JEV/GPT 路由标签；
- 预拆节点；
- 隐藏 oracle；
- 预计算答案。

## Full-GPT

T0
→ 读取同一原始任务
→ GPT 完成任务
→ 必要确定性动作/结果物化
→ 同一独立 verifier
→ 最终结果落盘
→ T1

`T_FULL_GPT_E2E = T1 - T0`

## Hybrid

T0
→ 读取同一原始任务
→ JEV 舒适区导向正向拆解/编译
→ 确定性路由门
→ CODE / JEV / GPT residual
→ 合法并行与依赖解锁
→ deterministic executor
→ 同一独立 verifier
→ 最终结果落盘
→ T1

`T_HYBRID_E2E = T1 - T0`

## 必须计入

- 原始输入读/解析；
- 正向拆解/编译；
- 路由校验；
- 序列化；
- 所有模型网络调用；
- response parse；
- CODE；
- JEV；
- GPT residual；
- scheduler；
- dependency wait；
- verifier；
- 最终结果写入。

## 禁止计入 T_VALID 的准备

仅允许在 T0 前准备通用、与具体 benchmark 内容无关的基础设施，例如：
- 进程启动；
- 通用连接池；
- 通用模型/endpoint 常量；
- 不含 benchmark 内容的认证探针。

不得在 T0 前读取或缓存具体任务、答案、路由或 oracle。

## 极限时间

虚阶段必须产生：

`T_VIRTUAL_STAR = min(T_VALID_E2E) subject to COMMERCIAL_GATE=PASS`

现实阶段必须测：

`T_REAL_STAR = min(T_VALID_E2E_REAL)`

现实只认证冻结的虚拟冠军，不现场改设计。

## 现实统计

默认：
- 3 warmup；
- 30 measured；
- 全部有效；
- 报告 min / P50 / P95 / max；
- 0 timed retry。

完整收益：

`S_E2E_TIME = T_FULL_GPT_REAL_STAR / T_HYBRID_REAL_STAR`

`S_E2E_COST = COST_FULL_GPT / COST_HYBRID`

没有这两个真实数值，不允许宣布完整任务收益。
