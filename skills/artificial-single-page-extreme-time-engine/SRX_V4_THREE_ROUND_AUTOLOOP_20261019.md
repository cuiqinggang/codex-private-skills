# SRX V4 — 三轮自动虚拟成熟闭环（规范增补）
VERSION=SRX-V4-AUTOLOOP-20261019
PARENT=SANRENXING_V4.md
STATUS=RULE_ADDITION_PENDING_E2E_ACCEPTANCE
MAX_OPTIMIZATION_ROUNDS=3
DEFAULT_EXECUTOR=GPT
WINDOWS_ROUTE=C_THEN_A_THEN_B_V10
NO_NEW_ORCHESTRATOR=true

## 目标与不变量
一项自然任务原则上连续执行至 DONE/STOP_GATE/人工必要授权，避免把一个完整任务拆为十多次对话批准。执行用最简可持久化状态记录，不另造锁、调度器、浏览器控制器。复用现有成熟技能与执行入口。不改 FlClash、代理或用户浏览器 Profile；不破坏已冻结历史成果。
T* = min(T_VALID)：时间只比较任务完成、质量验收通过、计时口径统一的完整有效样本。预检、失败、部分生成、画质降级均不得替代基线。
C 通道先检查并留下探测日志，C 未证实不可用不得改走 A；A 失效才考虑 B。

## 固定执行状态（最多 3 次优化回合）
S0 READ_CONTRACT: 读取现有技能包、任务目标、约束、质量准则、DONE_WHEN、证据位置、历史基线；任何高风险/不可逆操作需权限门。
S1 REAL_BASELINE: 优先复用可验证、同口径的已有本机完整运行；否则在安全与预算允许下按常规方案运行一次，记录 T0、硬件、输入、环境、质量、总时长分段。
S2 PHYSICAL_BOUND: 以必要步骤、数据量、硬件吞吐、IO/带宽/延迟、依赖的关键路径计算有证据的下界 T_phys（若未知给出区间与假设，不得声称严格数学极限）。禁止把理想并行加速直接当现实可达。
S3 BROAD_MATURE_3: 找三条可实际部署的广域成熟路径，每条记录出处/适用边界/兼容性/端到端 T_ref/质量/资源/复用成本；不满三条时说明证据不足，不编造。
S4 COMPOSE: 选成熟 BASELINE，基于约束组合互不冲突的机制，拒绝未经验证的叠加收益；标记风险和瓶颈。
S5 ATTACK: 每轮只选净收益最大的可控瓶颈，寻找最多三种成熟解法，计算优化收益上界、集成成本与失败概率，再选择一条或兼容组合；搜索止于能决策，不无限探索。
S6 VIRTUAL_MATURE: 产出 T_virt 区间、质量风险、关键路径、依据，并与 T_phys、三条 T_ref 同口径比较；虚拟预测不是实测结论。
S7 MINIMAL_VALIDATION: 用最小但具有判别力的现实检查排除不兼容、缺模型、资源不足、画质不足、耗时不优；可执行批量最小测试而非逐组重启。涉及唯一完整 Reality 时遵守原冻结合同。
S8 RECOVER_OR_ITERATE: 可诊断、可逆且在授权范围内的故障先自动定位、修复、重测；失败记录原因并回到 S4/S5 进入下一回合。每次优化循环 round +=1，最多3。修复重试不允许造成重复付费/提交/发送。
S9 STOP_GATE: 达标或增益不值得成本、缺乏可信成熟候选、3轮用尽、现实禁令/资源障碍不可安全解除，停止攻击；输出已证实成果、与 T_phys/T_ref 的差距、原因、下一可行动作。优选方案满足质量后才能 Freeze；未验收只可冻结方法或候选，不宣称生产 PASS。

## 自动继续与状态持久化
单页/单次运行状态最少保存 TASK_ID, METHOD_REF, BRIDGE_ROUTE, CURRENT_STATE, ROUND, QUALITY_GATE, T0, T_phys_range, T_ref[3], T_virt_range, T_valid, ARTIFACTS, FAILURE_CAUSE, RESTART_ACTION, DONE_WHEN, LAST_COMMIT。
每个阶段结束写一次轻量 checkpoint。重进任务时先读取 checkpoint 并核对现实副作用；CONFIRMED_COMMITTED 不重做，CONFIRMED_NOT_EXECUTED 可执行，UNKNOWN 必须查询对账，禁止盲重试。
一轮内部自主继续，无需用户逐步指点；只有真实需要用户授权、不可逆风险、凭证缺失、预算越界或无法自愈的外部阻断才请求用户。不得通过无限重试掩盖问题。
切换页面/会话时 NEXT_PAGE_PROMPT 只携带任务当前状态、文件指针和唯一下一动作，不以聊天上下文作为持久化状态唯一来源。

## 速度与质量
总有效耗时 = 实际执行 + 加载/准备 + 传输/调度 + 质量验证 + 必要恢复；不能只报采样或核心算子时间。
并行仅在资源可用、互不干扰、无需重建流程时采用；默认 GPT 自执行。Gemini 仅在现有入口已验证且净收益为正时并行；Codex 仅适于复杂长流程或具明确收益的执行段。
T_phys 只作目标下界，T_ref 作外部成熟可达参照；接近程度以 gap_phys = T_valid/T_phys 与 gap_ref = T_valid/min(comparable T_ref) 记录，同时披露 T_phys 的不确定性。
禁止质量门槛下降换取虚假极限时间；不能因为虚拟结果好就覆盖历史现实基线。

## 验收合同
A. 状态 S0→S9 的无人工逐步审批 dry-run；
B. 人工注入可恢复故障：自动修复后继续，而非结束；
C. 人工注入不可安全修复阻断：保留 checkpoint、停止有副作用操作并报告；
D. 第三轮严格终止，不触发第四轮；
E. 重新进入已提交操作不重复执行；
F. 输出五类时间比较及质量证据。
上述端到端测试未完成前，标记 RULE_ADDITION_PENDING_E2E_ACCEPTANCE，不得宣称自动运行闭环已上线。
