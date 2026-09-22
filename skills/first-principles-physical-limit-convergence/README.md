# 极限短时间引擎 v4.2.0

唯一一句话：先过 VALID，再只比较 T_VALID。

T*=min(T_VALID)

这不是提醒，而是虚和实中每一次实质判断的唯一决策律。

一虚一实：
虚 = 算出并冻结当前最短有效方案
实 = 在物理现实中量出它的真实 T_VALID

现实失败只走：实 -> Reality Delta -> STOP -> 虚。

防漂移硬门：
虚结束必须有 PREDICTED_T_VALID。
实结束必须有 VALID=PASS 和 T_VALID_REAL。
没有时间就没有完成。

正式显示名：极限短时间引擎。
机器兼容 ID 保持 first-principles-physical-limit-convergence。
第一性原理保留为内部推导方法，不再放进主名称。

当前状态：v4.2.0 仍在讨论成熟期；不本地部署；不提前自动化。
v4 mature freeze 前，JEV 必须完成自身极限适用度/极限时间成熟，并接入虚作为可选加速能力。