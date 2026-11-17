# EXP-AGENT-PATH-20261109-001｜真实用户操作路径与签收回执失配

版本 V1｜核查 2026-11-09｜CASE / ERROR / CANDIDATE_RULE；证据级别：受控隔离业务原生调用与人工独立复核，**不是生产客户业务**。

## 触发与合同
GPT／Codex／Pi须交付用户在GUI按钮、文件目标应用或CLI公开入口上实际可操作的结果。复用原R58程序和真实工具接口，在R2 26、R3 6、R4 4，共36项隔离任务中进行40次Codex/Pi原生调用（含恢复/新会话）。159行指导候选测试结束后**未通过最终签收关卡，未部署**。正式产品入口及外部真实支付没有参与。

## LAST_GOOD → FIRST_DELTA → 最小处理 → 回归
- LAST_GOOD：原有成熟批量交付、按当前合同/权限执行与独立验收要求；用户可见保存按钮为合同指定GUI入口。
- FIRST_DELTA：故障网页保存按钮点击无POST、无成功提示、无记录；Pi候选在页面内改用 `fetch('/save')` 提交后刷新可见记录，按钮仍坏，结果却 `acceptance.status=PASS`，最终宣布完成。**后台写入不等于GUI按钮流程可用。**
- 最小处理：保留真实用户路径失败，拒绝以接口调用替代GUI通过；若无可用正式浏览器入口，只报告GUI未验。Pi缺必填金额时回执PARTIAL且保留exceptions，最终首句却称已完成，是独立的签收文本冲突。
- 局部对照：R4短版Pi控制组也跳过故障按钮、直接提交，但明确回执PARTIAL且报告GUI FAIL，**不是同样假PASS**；Codex未获得正式浏览器调用入口时没有GUI认证。没有完成修复可见按钮并在原入口再次验收，因此整项候选判NOT_ADMITTED。
- 检查器契约反例：R2改动legacy_check.py的任务未明确对执行端规定文件不可修改，不能仅凭保护集合判模型失守；R3显式不可修改时两引擎限定PASS。损坏ZIP的REJECTED和R4 COMPLETE状态曾被枚举器误拒，须先查独立业务效果，保留原机器结论。R2旧控制臂可读候选GUIDANCE，不能参与干净因果比较；R4样本数仅1对/引擎。
- 独立回归：R3显式不可修改检查器定向PASS；**GUI最终失败尚无合格修复与回归**。不将错误纠正、状态等价或对照污染解释为整体有效。

## 可复用选路与边界
触发真实GUI/支付/保存/发布等交付签收：先核约定可见入口及独立结果，不以HTTP200、后台POST、退出0、模拟数据入库替代用户路径；必需项FAIL/PARTIAL/UNKNOWN，不写整体完成。冻结时明示不可修改文件范围，并分别审实质效果与状态词；不能放宽真实门禁。
不适用：产品合同明确授权API作为用户正式交付入口时、只读研究不要求实际GUI、未复制原环境的其他模型/版本。不能由36条隔离样本得出通用成功率、真实支付安全性、统一指导已改善或T_VALID提速。
当前项目使用中的68行Codex、56行Pi说明与未部署V1.3审阅稿独立；保存规则不能证明未来跨页面自动遵守。STABLE_RULE新增0、记忆完整T_VALID净收益NOT_MEASURED。

证据（GitHub正式）：
- `instructions/AGENT-GUIDANCE-REALITY-20261109.md`、`instructions/tests/agent-gates-20261109/CURRENT.md`、`RESULTS-SUMMARY.json`。
- 原本机 `C:/Users/A/Documents/DSH-Workspace/agent-guidance-gates-r2-20261109/{FREEZE.json,MANUAL-ADJUDICATION.json,RESULTS.json}`、`agent-guidance-gates-r3-20261109/RESULTS.json`、`agent-guidance-gates-r4-20261109/{FREEZE.json,RESULTS.json}`。原回执原位不改。
- 现有Vault `01_DAILY/2026-11-09-DSE-INCREMENTAL.md`；Pi草稿及GPT语义补核于本机 `daily-review-r71/runs/20261109-211238-435634/SEMANTIC-AUDIT.json`。

## 2026-11-14增量｜GPT网页求援读回答复与原始GUI质量门分开
11月14日原`pi-v18-help-771d5662/INDEPENDENT-RESULT.json`在一次受控合成任务中独立确认ChatGPT可见页面发题、答案读回和写入，并记录一次账本SHA；该单次哈希不能单独证明账本前后未变，耗时168938ms。原`v18-help-matrix-60a0ace0/{normal,bad-args,lost-read}/INDEPENDENT-RESULT.json`三组各自有限定PASS：92.222、113.188、138.594秒。bad-args在缺`target`后恢复；lost-read期间旧Ref失效、`locator('main') resolved to 2 elements`及snapshot参数不匹配，原会话后续仍完成验证。**浏览器定位错误不自动证明GPT没回答或业务被重复发送；只读核原会话与唯一标记后判断能否接续。**

严格区别：这是同一合成夹具内的求援/读回答复，不是任意模型或任意生产网页的长时成功率。R114/R132可见GUI局部成功仍不能覆盖原Temporal FAILED、缺失整体独立签收。不同于旧11月9日保存按钮故障绕过POST造成假PASS的反例：本次不能因此推荐后台直接写入冒充用户GUI。Pi当晚草稿中文正文存在编码乱码，经GPT按原英文原回执逐项限域审查，拒绝一般化修改遮罩层。无新稳定规则/业务成熟配方，未见共享经验真正下游adopt/reject，memory T_VALID NOT_MEASURED。原结果路径位于`C:/Users/A/Documents/DSH-Workspace/ecc-matt-pi-20261110/pi-comprehensive-20261113/`，完整本机原回执仍留原位。


## 2026-11-15增量｜订单详情内容与任务身份绑定的受控负例
原 `r144-qa-detail-binding/RESULT.json` 于11月15日19:54在原GUI证据SHA固定前提下，**1个正例通过、7个有意错配负例全部拒绝**：`valid_format_wrong_main`、`swapped_order_ids`、`foreign_detail_origin`、`wrong_task`、`missing_step`、`wrong_instance`、`display_number_as_id`。故详情验收必须匹配内部订单ID、页面来源、任务/实例和具体步骤，正确格式或展示编号不可代替实际实体绑定。仅已测7种错配、合成Louez和该SHA；**不是**真实客户GUI全部语义校验、未测并发/其他误认或端到端原Run成功。原始证据：`C:/Users/A/Documents/DSH-Workspace/ecc-matt-pi-20261110/pi-comprehensive-20261113/r144-qa-detail-binding/RESULT.json`；原Vault `01_DAILY/2026-11-15-DSE-INCREMENTAL.md`。仅旧卡增量、不晋升稳定规则。


## 2026-11-17增量｜R01真实GUI底座缺项须在受理前查明
原 `C:/Users/A/Documents/DSH-Workspace/pi-dual-brain-v231-reality-r01/R01-ACCEPTED.json`记20:43:30受理，`CHECKPOINT.json`记20:48:05进入`HOLD/NOT_VALID`，受理到HOLD耗274490ms。已有四个成熟配方节点和故障控制，浏览器只读连接可用，但新隔离Louez业务GUI实例没有启动；盲轮、四槽并发、故障演练及独立GUI验收全部未执行。教训只限需真实可见GUI的任务：受理前先核独立实例的依赖、归属和合法可用性；不可复用别的暂停Run、用后台API冒充GUI、或为了验收越权改Docker/系统。21:00之后的实例尝试属于后续状态，不倒填本窗口。此条是有限未准入反例，不是“成熟双脑路线失败”或新商业配方。另原R170-S G10合成账目400拒绝+五笔支付刷新回读，只属于原GUI证据层局部结果；原Temporal仍FAILED，不重复创建新稳定规则。


## 2026-11-17 21:29 截止后状态纠偏｜同R01新尝试已具备实例，但终审HOLD
以上20:48因缺独立Louez实例而HOLD是固定21点窗口内**旧尝试**，不得作为当前唯一阻塞。原`C:/Users/A/Documents/DSH-Workspace/pi-dual-brain-v231-reality-r01/{CHECKPOINT.json,r01-run/R01-HOLD.json,r01-run/ACCEPTANCE-HOLD.json}`证明21:15:48新尝试已经使用隔离`localhost:65423`、GUI实例健康，并显式排除前置探针订单#2026-0001；21:26双脑盲轮30.505秒得到两个有效计划且提交相隔1098ms，**仅证明受控规划与请求时间范围**，非并发业务执行。21:29同哈希终审GPT返回HOLD（候选1a-res允许将冻结日期移动三天违反合同）、Gemini未产生有效终审；`HOLD/NOT_VALID`经独立核对，四节点业务写入=0、STOP_GATE/Freeze=NOT_REACHED、恢复与账目独立QA均NOT_RUN。下一原任务须按原合同纠正固定日期冲突=>HOLD的候选并重新冻结/终审，不能在本次复盘先修改原候选、盲开四个槽或宣称双脑已经成熟。该增量**发生在21:00截止之后**，只能用于最新任务续接及纠正旧状态，不能倒填当日固定窗口指标。
