# EXP-PI-DURABLE-ENTRY-20261113-001｜原生Pi入口持久化接续与GUI限定验收

类别：CASE / ERROR / CANDIDATE_RULE；核查日2026-11-13；证据等级：同一Windows10机器、实际公开Open-Pi.cmd入口、**合成单工作流**的原生回执和独立字段/受控GUI验收。只认证 `VERIFIED_FOR_SCOPE`，不是通用生产事务安全、商业用户交付、24h无人值守或新正式稳定规则。

**触发**：原生Pi+Temporal工作流在心跳超时、worker/service重启、已写入但无回执、已验证结果重复提交、真实合成页面GUI导出与本机Excel读回之间需要核账；必须区分业务产物、确认回执、重试次数和有效签收。

**成熟节点**：原 `C:/Users/A/Documents/DSH-Workspace/pi-capability-enhancement-20261028/Open-Pi.cmd` 公开入口、原生Pi同会话、已有Temporal心跳/持久化状态、原宿主合成账目配方和独立GUI/字段核验。未自建通用调度器、状态数据库或系统恢复内核。

**LAST_GOOD→FIRST_DELTA→原任务修复及回归**：
- 11月13日19:07原`pi-comprehensive-20261113/temporal-heartbeat-restart-r83/RESULT.json`：原存储重开、原worker替换，history activity attempts=[2]、原生Pi attempt=1，业务hash/mtime保留；恢复至验收9.785秒，全段106.883秒，限定字段QA true。
- 20:39—20:41原`pi-durable-entry-r84-r86-normal/ENTRY-ACCEPTANCE.json`、`...fault/ENTRY-ACCEPTANCE.json`：正常组attempt=[1]、elapsed98.823秒；受控中断组attempt=[2]、同一workflow/run、`reused_verified_result=true`、`one_native_pi_attempt=true`、原delivery/checkpoint SHA和mtime **各组内**重试前后相等，恢复12.339秒、elapsed62.821秒。两组耗时不构成可比较加速合同，已复用结果不等于重新完成业务计算。
- **反例**：`...no-receipt/ENTRY-ACCEPTANCE.json`注入了业务副作用但没有确认回执，结果是`FAILED`、`second_execution_blocked=true`。这才是正确的UNKNOWN安全拒绝，不可写作PASS或强制重发。
- 11月13日03:03原`durable-three-route-reality-r1/conductor-mh-r76-result.json`为合成网页GUI独立完成，原数据保持、单自有tab、CSV+工作簿逐格审计与页面刷新 true、214.117秒；20:49`pi-comprehensive-20261113/matt-booking/RESULT.json`既有合成预约GUI→CSV→工作簿限定PASS、全段213.670秒并恢复4次工具错误。两个不同合同不可直接用秒数排名。
- 20:29`BROWSER-READONLY-RECOVERY-20261113.json`仅`browser_tabs/list` PASS、23.385秒，`gui_signed=false`，不能算用户业务交付。

**用途**：下一次遇已验结果与恢复状态冲突，先匹配原workflow/run、原checkpoint和原产物SHA/mtime，核历史attempt和业务唯一写入回执。三态：已证明写入不再重做；确认未写可经原接口重试；已写但回执缺失则UNKNOWN、禁止盲重发，归原项目核账。所有验收必须走原GUI/实际公开入口。

**不适用**：合成单工作流不代表真实多账户高并发、任意崩溃点恰好一次、跨OS重启、ChatGPT网页委派、完全无人值守或真实客户交付。没有相同质量/成本条件的全业务路线对照；完整`T_VALID`与记忆净收益均`NOT_MEASURED`。不将该案例新建为“成熟商业业务配方”。原项目任务约束/Freeze/持久化状态均不修改。

来源均在原C盘`C:/Users/A/Documents/DSH-Workspace/ecc-matt-pi-20261110/`，上述各独立RESULT/ENTRY-ACCEPTANCE原文件及本机Vault`01_DAILY/2026-11-13-DSE-INCREMENTAL.md`。Pi复盘原稿与GPT纠界：`pi-rules-r64-20261108/daily-review-r71/runs/20261113-210402-083610/{RESULT.json,DRAFT.json,SEMANTIC-AUDIT.json}`。分享卡未附原客户数据、凭据或大段聊天。新增稳定规则0、新真实业务配方0、共享EXP下游新采用未观察到；memory_T_VALID_gain=NOT_MEASURED。

## 2026-11-14增量｜原生失败终态、终态后GUI与R134阶段失败分层
R114及R132均为**彼此隔离的合成Louez任务**，不能继承为同一Run。R114原`STATUS.json`为`FAILED`，后来原`G12-INDEPENDENT-READBACK.json`只证明可见GUI相邻订单G12已存并回读，`original_native_terminal=FAILED`、`full_qa=NOT_SIGNED`均未改变。R132原Run于11月14日19:44因`Production app never became healthy`失败；随后隔离实例19:47健康、19:48—19:59的G00–G12在可见GUI局部通过，原`LEDGER-READBACK.json`20:01核实租金300已收、押金500收退净额0、主单原5笔付款不变、新增唯一相邻未付款预订。**原Run仍FAILED，`receipt.json`和整体验收仍缺。** LAST_GOOD=原业务账本；FIRST_DELTA=原应用启动未就绪；后续本地GUI工作属于诊断/局部补验而非原生调度恢复。不得拿终态后补做当原Run有效T_VALID。

新独立任务R134于20:20`DISPATCH.json`正式受理，20:21旧`STATUS.json`为RUNNING；20:26原`INSTALL-STAGE-RECEIPT.json`为安装PASS，但更晚`activity-install.log`记录安装后`taskkill.exe /PID 10296 /F`返回128。上一秒RUNNING快照不能证明当前Run仍运行，也不能仅凭本机清理报错写出调度器已经FAILED；**当前原生终态=UNKNOWN_NEEDS_NATIVE_RECONCILIATION**，下一合法节点为原项目只读核对Run history、阶段回执和PID所属者，禁止复盘重派和改变Freeze。R128另一独立原Run的18:51`STATUS.json`为FAILED，无额外业务签收。

R114额外存在浏览器主线程超时后先核没有提交再恢复页面、原GUI一次提交的受控案例；残留覆盖层`pointer-events`仅为该页面明确已关闭的节点的局部操作，不可变成普遍绕过真实用户GUI或安全遮罩的规则。新的稳定规则0；新已验**商业**成熟节点配方0。原R83/R84/R86负例与历史事实仍保留，完整记忆T_VALID未测。

原始C盘限定来源：`C:/Users/A/Documents/DSH-Workspace/ecc-matt-pi-20261110/pi-comprehensive-20261113/r114-temporal-louez/{STATUS.json,G12-RECOVERY.json,G12-INDEPENDENT-READBACK.json}`、`r132-temporal-louez/{STATUS.json,activity-launch.log,GUI-EVIDENCE.json,LEDGER-READBACK.json}`、`r134-temporal-louez/{DISPATCH.json,STATUS.json,INSTALL-STAGE-RECEIPT.json,activity-install.log}`。原Vault日报`01_DAILY/2026-11-14-DSE-INCREMENTAL.md`和Pi独立限域审核`daily-review-r71/runs/20261114-211106-760704/SEMANTIC-AUDIT.json`；不复制GUI原始聊天与个人信息。


## 2026-11-15增量｜R144原生FAILED与独立证据核账、R154—R157复测边界
- **R144不同Run严禁混同**：原 `r144-temporal-louez` Temporal run `01a1da9a-ca4a-72cd-a96c-bd96147ba44b` 终态仍 **FAILED**；原 `receipt.json`、`HOST-QA.json`虽然局部PASS，不能改原生终态。11月15日00:23的 `R144-LINKED-CORRECTION.json` 为 `POST_TERMINAL_LINKED_EVIDENCE_RECHECK/PASS`、`native_correction_run=NOT_LAUNCHED`，以未变原GUI哈希、两张订单、原五笔付款、邻单零付款、独立DB备份恢复与HOST QA核验。独立 `r144-linked-final` 任务于00:35以**另一**run `01a1dae9-e490-7d34-8ced-951505a6c36c` 终态COMPLETED，`recheck.json`明确 `business_replayed=false`，**只证明事后独立核账，绝非原Run恢复或原完整T_VALID成功**。
- **R154/R156同Run重复限制**：11月15日20:11、20:33的两个隔离RESULT均PASS，相同run_id重派、活动中重派仅返回现状，变化载荷拒绝、`business_writes=1`；不外推跨Run业务去重、多Worker竞争与生产Exactly-once。
- **R157失败须留档**：20:40受控worker-restart原Run `native_status=FAILED,result=FAIL,attempts=[2],business_writes=1`；20:41 **另一Run** worker-resume-recheck `COMPLETED/PASS,attempts=[2],business_writes=1`，service-restart/duplicate各自PASS。后续不同Run复测PASS不能修正首次FAILED、证明根因已修或原Run可靠接续。保留原R84/R86无回执禁止重放负例。
- 原C盘原始限定证据：`C:/Users/A/Documents/DSH-Workspace/ecc-matt-pi-20261110/pi-comprehensive-20261113/{r144-temporal-louez/R144-LINKED-CORRECTION.json,r144-temporal-louez/DB-RESTORE.json,r144-linked-final/STATUS.json,r144-linked-final/recheck.json,r154-dispatch-identity-recheck/RESULT.json,r156-active-duplicate/RESULT.json,r157-worker-restart/RESULT.json,r157-worker-resume-recheck/RESULT.json,r157-service-restart/RESULT.json,r157-duplicate/RESULT.json}`。合同/Freeze不更改，原问题根因UNKNOWN、未证真实生产业务或完整T_VALID；新增稳定规则0。


## 2026-11-17增量｜R170同Run终态与合成GUI局部证据分离
原 `C:/Users/A/Documents/DSH-Workspace/R170/r170-s/GUI-EVIDENCE.json` 在02:39前后记录合成Louez可见GUI G00—G12（原五笔付款及相邻无付款订单）局部PASS；同lane `r170-s/STATUS.json`于02:40:18+08却记原生Temporal `FAILED`，不是整轮业务签收。G10原押金凭据删除被服务端400拒绝，刷新重入后旧凭据仍在；只能证明该隔离样本的拒绝与账目保持。原Run失败原因未核实，不能把GUI有效或事后核账视为native COMPLETED。
原 `R170-PAUSE-STATE.json` 于03:07:24记录r170-t `PAUSED_IN_MEMORY`，G04有200租金及500押金签收，G05取件动作已提交并在03:04及03:07可见“进行中”，但尚无G05签收行：**先核原订单/账本，绝不因签名缺失重放取件**。这证明有已提交动作和签收缺口，未证明重复写入损害发生、当前进程存活或完整接续PASS。
原 `R170-C-OWNER-READBACK.json` 于02:06显示r170-c native task SCHEDULED、原worker不存在但GUI stage子进程当时仍在；原同native task替换租约只是有条件接续方案，必须先重新核阶段所有者、GUI receipt和指纹，不可假称接管已完成、也不得新建第二GUI。沿用R84/R86无回执禁止重放与R144/R157不同Run不能替原FAILED改判两条旧负例。合成局部有效范围=VERIFIED_FOR_SCOPE；完整有效E2E、生产Exactly-once和记忆T_VALID收益仍NOT_MEASURED。原合同/Freeze保持不动。

## 2026-11-20增量｜V124写后无回执唯一写与合同失败
原V124-REMAINING-REALITY-20261121 12:39:28.607一次正式接单，14:00独立HOLD：B fault2成功HTTP200后切断本页回执，原Pi恢复前从独立SQL及用户可见GUI核账，**相同业务键建单一次、未二次创建**的受控能力有证据；但主单已按租金200元completed，G06延期及G07补收100在归还之前均未发生，独立`B2-G06-G07-INDEPENDENT-REWORK.json`明确REWORK。四笔实际流水200租金、500押金、100与400押金退回，均不能代替完整租金合同签收。B fault1在CP1前ECONNRESET，无完整自然接管证据。另C2恢复两单五笔并完成deploy/ledger，但Temporal原生事件23为gui stage失败、`WORKFLOW_EXECUTION_STATUS_FAILED`；CLI rc或已完阶段不覆盖原Run失败。
LAST_GOOD=原冻结与单次账目，FIRST_DELTA=回执丢失和后续合同阶段次序失配；已做最小核账、未重放业务。继续沿原任务、原业务键、原Run核账及GUI验收，不为掩盖时序重开、倒填或改冻结合同；历史辅助交付168:10:054不能替今日失败场的有效T_VALID。原接单至14:00的80:41:949是墙钟，不是T_VALID。原始：`C:/Users/A/Documents/DSH-Workspace/PI-SPECIALS-20261120/audit/V124-REMAINING-REALITY-20261121/{RESULT.md,INDEPENDENT-CHECKPOINT-140010.json,B2-G06-G07-INDEPENDENT-REWORK.json,C2-TERMINAL-NATIVE-HISTORY.json}`；Vault 11月20日日报。**只认证限定建单去重和阶段局部证据；完整业务REWORK/HOLD、生产Exactly-once与净提速均未认证。**

## 2026-11-25 独立审计增量｜受控唤醒不是自动恢复（CASE/PROJECT_STATE，非新稳定规则）

PI-OOL-SEQ-20261121原会话11月21日中断，4天03:05:21.839空档无程序事件。11月25日18:52:09审计端发受控唤醒请求，20:10:24才在同原生会话实际追加，原回执滞后01:18:15.311；automatic_credit=0。监听的daemon units=0，未证明此任务持久登记或跨退出生存。20:31独审R1为REWORK，7/7引用文件指纹复核相符；20:51 WAIT且无新的原生ACK，0/9阶段签收，未启动Stage1，无业务写入。旧PID缺失不证明没有其他执行者，须核同一会话、任务所有权及回执，不重复派工。首缺C0.6：复用现有授权持久服务做本任务独立唤醒登记和原生读回；继而核C0.7独立目标、C0.8浏览器所有权等原合同门。等待计入完整历时一次，不能当自动收益或剔除；完整T_VALID未形成。历史受控唤醒不是新的成熟业务配方，不扩为所有daemon或调度器的结论。
来源：C:/Users/A/Documents/DSH-Workspace/pi-capability-enhancement-20261028/workspace/PI-OOL-SEQ-20261121/{OUTER-RESUME-INTENT-DA2A6F7D.json,STATUS.json,STAGE-0-INDEPENDENT-REVIEW-R1.json,OUTER-AUDIT-20261125-205110.json}；Vault 01_DAILY/2026-11-25-DSE-INCREMENTAL.md；原Pi草稿及独审留本机。

## 2026-11-26 反例增量｜共享入口换版与旧会话/日常任务路由（CASE/ERROR，非新稳定规则）
LAST_GOOD：11月25日原日常Pi复盘10源、5候选；旧顺序实测同一原会话曾受控唤醒。FIRST_DELTA：11月26日14:24原PI-OOL-SEQ-20261121独审记录入口指纹改变，commercial_entry.route把旧 --resume 送至商业合同校验分支，原任务缺该分支要求的pi-commercial-request.json；19:50原会话及五份合同/状态/独审指纹不变，daemon units=0，匹配执行者PID未见（限定查询），未接续、未重派、0/9签收、automatic_credit=0，首缺仍C0.6。另当日截止后21:01:38实际调用原pi_daily_review.py，原PI-OUTPUT.jsonl返回PI-COMMERCIAL-GATE/1、DENY/BLOCKED、reason=TASK_SCOPE，退出1、未生成DRAFT/RESULT。两现象同现但同一内部根因未证。仅限原任务与实际入口；不得以网络恢复或历史成功替代当前接口验证，也不得为通过而放宽商业门控、伪造合同、绕路重派。原维护者应核合法任务类型/旧resume的兼容入口，保留拒绝负例并回归原合法复盘与同会话接续；本轮只读及GPT备用复盘，未修复、无新成熟商业配方、完整T_VALID未形成。
来源：C:/Users/A/Documents/DSH-Workspace/pi-capability-enhancement-20261028/workspace/PI-OOL-SEQ-20261121/OUTER-AUDIT-20261126-{142428,195039}.json；pi-rules-r64-20261108/daily-review-r71/runs/20261126-210138-204577/PI-OUTPUT.jsonl；Vault 01_DAILY/2026-11-26-DSE-INCREMENTAL.md。

## 2026-11-27 修复回归｜每日复盘接回 Pi 记忆运行时

共享启动器先走 `commercial_entry.route`，再解析原 Pi 参数。旧复盘调用的固定目录触发 `TASK_SCOPE`。旧 `--resume` 在同一分流点触发 `COMMERCIAL_CONTRACT_REQUIRED`，对应另一原任务，接续依它的合同、登记与执行所有权。

原 21:00 定时任务仍调用原 `pi_daily_review.py`。复盘器用现有 Pi 运行时处理清单，模型工具只有读写，写范围固定为本轮目录。证据截止取清单原定 21:00，手动补验保留实际运行时间。GPT 独立核对语义、引文和重复项后才写经验。

11 月 27 日手动补验真实生成 5 条候选，5 份原件的 12 处引文均可核，5 条候选与历史记录去重。重复输入得到 `NO_NEW_SOURCES` 且没有再次调用模型。独立新 Pi 会话从原索引找到本机案例并读回复盘路径、数量及边界。商业范围反例实际退出 3，原发布完整性校验通过。原调度配置已读回，北京时间每日 21:00 启用。首次自然触发后的完成回执待核对。

原证据见 `daily-review-r71/runs/20261127-163104-953807/{RESULT.json,SEMANTIC-AUDIT.json,PI-RECALL-RESULT.json}`、Vault `09_DEPLOYMENT_LOGS/2026-11-27-PI-DAILY-REVIEW-COMPAT.md`。这是日常复盘修复案例，旧业务未启动，新增稳定规则 0，完整业务记忆提速未测。

### 2026-11-27 21点复盘｜资源准入未通过（不重复创建案例）
本轮原21点清单已保存；实际启动前CPU采样100%，本轮资源守卫返回HIGH_LOAD_WAIT，未调用Pi复盘器、无本窗口Pi RESULT。GPT在原Vault按5份显式来源独立核证，不能把下午手动补验当作自然触发完成，也不能把资源等待认作TASK_SCOPE复发。原旧业务未接续；PI-OOL-SEQ 19:42独审仍C0.6/0/9，原任务所有权不变。首次自然Pi成功仍待证。原修复案例不重复入库，完整记忆净T_VALID未测。来源：原Vault 01_DAILY/2026-11-27-DSE-INCREMENTAL.md及daily-review-r71/MANIFEST-20261127-2100.json。
