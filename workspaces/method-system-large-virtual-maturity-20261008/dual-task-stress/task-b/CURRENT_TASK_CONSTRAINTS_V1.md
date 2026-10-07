# TASK_B《当前任务目标与正反约束 第1版》

TASK_ID=DUAL-STRESS-B-H3P1-VIDEO-CONVERGENCE-20261008
CONTRACT_VERSION=1
TYPE=LARGE_MATURE_MOTHER_TASK_REPLAY

目标：完整重放 H3-P1“首个有效图声对”视频极限时间收敛链，从 TASK_ACCEPTED 到本任务 FINAL_VALID，不得缩成一次简单生成。

VALID_SPEC：成年女性正面对镜头挥手，清楚说中文“你好”，有效人声、基本音画同步、最低展示可用，必要 verifier 全 PASS。

必须覆盖：初始 T*=653921.787ms；R1 五阶段剖面；R2 closed-loop runner、publication race、12-step、random seed drift、seed=2026090201、616191.785ms；R3 warm+light verifier、358618.442ms；单 decode、单 ASR、并行 verifier；约263.164s INVALID 不得提升 T*；R4 288281.990ms FINAL_VALID。

并发覆盖层：B 只能写 task-b；与 A 共用同一 persistent ChatGPT browser 控制页但不得启动第二 browser；shared repo writer 只在具体持久化写操作持 lease；B FAIL/回虚不得回滚 A。

DONE_WHEN：完整历史收敛链通过且最终 T*=288281.990ms，FINAL_VALID=YES，无跨 A 状态污染。
