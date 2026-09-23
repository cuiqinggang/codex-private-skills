# 千问3.8 27B1 — v4.7.1 虚拟成熟最终冻结

TASK_TIME_ID=QWEN38-27B1-20260923-182700+0800
METHOD=first-principles-physical-limit-convergence v4.7.1
PAGE=千问3.8 27B1

目标：建立 Bonsai 2 27B 本地智能体能力边界，并对所有现实 PASS 能力格唯一优化 min T_VALID；JEV 为可选概率加速器，缺失/失败立即回本地；Thinking 按 OFF/512/2048/8192 路由。

已闭合：
- 历史 1018 题库保留；
- 16 个旧 252-255K + HIGH_8192 超窗矛盾改为总上下文预算；
- 现实首轮冻结为 64 个原子覆盖锚点，保持 800/800 两两组合；
- 24 个结构化概率边界题；
- 四档 Thinking；
- 50/100/200 长流程边界；
- 文件/PowerShell/Git/HTTP/Browser/Local Service/Hash/Multi-tool 全部存在确定绑定；
- 本地模型调用、工具回执回灌、确定性验证、能力边界记录、min T_VALID 记录均进入现实 runner；
- JEV 是可选加速器，不是现实启动单点依赖；
- REAL 中禁止重新设计，失败只回最小 Reality Delta。

零 GPU runner 自检：
SELF_TEST=PASS
ANCHORS=64
PAIRWISE=800/800
EXECUTION_CHAIN_CLOSED=PASS
EXTERNAL_DEPENDENCIES_CLOSED=PASS
REAL_HANDOFF_SELF_CONTAINED=YES
RUNNER_SHA256=d727112ac292f166f7509553bc96dea321025cec72d28916e78049c00e25e6f0

v4.7.1 原子发布门：
FREEZE_GATES_ALL_PASS=YES
NEXT_SEQUENCE_ASSIGNED=01
REAL_HANDOFF_SELF_CONTAINED=YES
TIME_LEDGER_CONTINUITY=PASS
REAL_COMMAND_EMITTED=YES (same GPT turn; inline bootstrap is the authority)
VIRTUAL_COMPLETE=YES
CURRENT_PHASE=REAL

Reality FAIL：
最小 Reality Delta -> STOP -> 同一 TASK_TIME_ID 回虚；时间不清零；序号不清零；下一现实命令序号=02。
