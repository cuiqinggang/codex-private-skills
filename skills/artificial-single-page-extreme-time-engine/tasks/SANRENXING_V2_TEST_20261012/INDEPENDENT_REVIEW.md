# 三人行 V2 C002 独立静态审查

审查日期：2026-10-12（Asia/Shanghai）
审查者：独立只读子代理 `/root/locate_v2`。
范围：本地 candidate 三份文本，对照 source 中 C001、冻结 V1 及 36 项覆盖矩阵。没有修改候选、V1、默认入口或现役 runner，没有启动性能测试或外部写入。

## 结论与证据范围

最终 C002 三份文本回读后，36 个历史能力 ID 均有设计覆盖；这只是静态文档结论，**不是 36 项行为 PASS、旧规则完全等价证明或全链路验收**。标签/ROI 暂停、单调墙钟、吞吐、实质变化重判和候选未激活均已有明确条款。此前矩阵/验收措辞和本地引用发现已 FIXED。独立人工核算确认金额及 ID 集合 oracle 正确；先导 fixture 的有序 action 词表泄漏和 R16 词义歧义均在正式 PROFILE002 中 FIXED。t001/t002 保留为 PILOT_LEAKED_VOCAB，不纳入正式 V1/V2 判定。

最终入口 SHA-256：`6B0072FF3E1195305FB40F3A5CD7C6EA8D7647B52291D6EF9BD249D5C94F2112`。
最终验收合同 SHA-256：`15C40240CB7FF4A862FF17228FA1767A12A96950B14E3DEC4D44837DE04744CE`。
最终覆盖矩阵 SHA-256：`F1141243E412410008E7CE536D22145272048CCA68888CF81288E3E5C5F9A71E`。

以下保留前次回读哈希作为发现和修订历史：

回读入口 SHA-256：`47EB187D9C247FE5D29BD6C94525DD9993C6D7B0C3F06BD44606DBB586226C36`。
回读验收合同 SHA-256：`14B69940811D7F45C598997FFFCC8EFE1A63998BD1BD7E727B85CF505BD31903`。
回读覆盖矩阵 SHA-256：`7DBD09E915E64FE9A39405DCE81A96979913DEB5D315F4C116EEA002FD50428B`。
本地冻结 V1 source SHA-256：`7D728B62012C43225C69FDD42CCC03092DCEC739C586D74734B0888848C88F45`；正式 Git Blob 标识为 `a05fc51d661952790837dfa462bf766b16aba078`，两类哈希不可混用。
本地原 C001 source SHA-256：`00190D221DC974D868C543F6A491D6A1DB4040DD5611DD4CCBA98CA1B0C97B57`。

以上哈希限定本次回读修订；随后修改必须保留差分并更新审核回执。

## 关键缺陷与修订状态

1. **标签门禁误阻断，已静态修复。** C001 §4 / R06 / 矩阵 20 要求缺标签阻断；C002 已采用当前用户定位策略，明确暂停时不阻断、不猜造，其他授权和副作用门保留。ROI 同样保持暂停，没有把测速或继续任务当作恢复授权。
2. **墙钟口径漂移，已静态修复。** C002 从输入交付至独立验收按单调时钟计算；accepted_at 不能后移起点，UTC 只作定位。历史部署/维护摊销单列，重叠并行阶段不相加。批次吞吐分母包含失败、审核与真实等待。
3. **运行层版本漂移及配套措辞不一致，FIXED。** 当前入口 §3/4 优先已有 METHOD_REF/NODE_RUNTIME_SNAPSHOT；新节点先锁 commit，再按 ref 读取索引/依赖，latest 只发现差分；已有运行快照变更须明确授权、安全边界和无 UNKNOWN。这解决“先读 moving latest 后才锁版本”及跨节点无授权更新的歧义。此前矩阵行 19、规则优先级第 3 条及验收 S0-06 的 latest 简略表达已在最终回读中统一为快照优先、不自动迁移。
4. **接单只判一次，已静态修复。** C002 §2 / R26 允许目标、权限、副作用三态、依赖、资源归属有实质变化时仅重判受影响动作；保留 GOOD。新增权限不得仅凭重判获得授权，UNKNOWN 仍需先对账。
5. **本地引用路径歧义，FIXED。** 三份候选同在 candidate 目录；原字段仍保留远端 `method-drafts/...` 目标。最终入口末尾已明确线上任务路径、本地 `../BENCHMARK_CONTRACT.md` 及同目录验收/矩阵副本位置，当前本地文件均已回读存在。未把线上目标误当本地已创建目录。
6. **计时结果与认证状态应继续分列。** 未完成全套认证时 V2_FINAL_VALID 与物理极限继续 UNKNOWN/NO；已经独立验收的局部实测样本仍可如实报告 observed_min/full_wall。不能因缺物理界而抹去真实样本，也不能从真实样本推导全局最优。

## 36 项逐项静态覆盖

表中 `COVERED_STATIC` 仅表示 C002 入口或保留的配套规则明确覆盖该设计能力。相应行为均须依据本次独立实际回执另行评级。

| ID | 静态结论 | 回读依据与验收边界 |
|---|---|---|
| 01 | COVERED_STATIC | §0 同合同/质量/风险/权限完整 T_VALID；§6 禁止局部片段替代整任务 |
| 02 | COVERED_STATIC | §1 REUSE_GATE；§6 测试脚本不得承接通用调度/锁/恢复 |
| 03 | COVERED_STATIC | §1 成熟接口；§3 接口故障按需读成熟桥，连接可通不扩大权限 |
| 04 | COVERED_STATIC | §2 最多三条有实质差异成熟候选，不凑数 |
| 05 | COVERED_STATIC | §1 防伪及 §2 正式优化认证链；物理极限/提升率未知保持未知 |
| 06 | COVERED_STATIC | §1 必要持久化；§2 日常最小判断、优化实验继承完整链 |
| 07 | COVERED_STATIC | §2 同合同基线→物理边界→虚拟→STOP_GATE→Freeze→Reality；不把小测试冒充最终认证 |
| 08 | COVERED_STATIC | §1 授权/安全/质量硬门；R11 未授权外部动作不执行 |
| 09 | COVERED_STATIC | §1/§5 DONE/NOT_DONE/UNKNOWN；R17 不盲重发 |
| 10 | COVERED_STATIC | §0/§1 唯一 CEO/CURRENT 写者、Executor 仅节点输出 |
| 11 | COVERED_STATIC | 矩阵 11 保留共享冲突仲裁；§2 资源归属变化重判，未证明仲裁实现等价 |
| 12 | COVERED_STATIC | §1 PAGE_HEALTH_RISK/REPLAN_REQUIRED；R13 健康节点不形式换页 |
| 13 | COVERED_STATIC | §1 保留同页最多三次 Freeze；没有要求必须做满三次 |
| 14 | COVERED_STATIC | §1 模板短码与新 CEO 回读；R14 人工合法后备 |
| 15 | COVERED_STATIC | §1 Executor 归属关闭；R15 用户/其他任务标签不动，未操作真实 UI |
| 16 | COVERED_STATIC | §0 不固定三级拓扑；矩阵 16 仅在隔离和净节时证据下启用 |
| 17 | COVERED_STATIC | §2 A/C/P 按需路由与实质变化重判；未预设 C/P 更快 |
| 18 | COVERED_STATIC | §2/§3 n8n 持久事件/Wait；R12 health 200 不替代管理授权 |
| 19 | COVERED_STATIC | 入口 §3/4 固定运行快照，不热迁移；矩阵 19/latest 措辞已统一 |
| 20 | COVERED_STATIC | §4 当前授权→真实 NEXT；用户标签暂停例外明确，R06/R28 对应 |
| 21 | COVERED_STATIC | §4 同 commit/依赖 SHA 与动作前实时状态分离；R09 路径/SHA/远端指针拒绝 |
| 22 | COVERED_STATIC | 矩阵 22 与 R08 要求唯一独立 FREEZE_ID；没有声称现役 runner 已部署修复 |
| 23 | COVERED_STATIC | §4 进程/INFLIGHT/PAUSE/WAIT/STOP/DONE；R07 禁止第二实例/清未知标志 |
| 24 | COVERED_STATIC | §1/§5 GOOD/BAD/FIRST_DELTA、最小修复、合法分支继续 |
| 25 | COVERED_STATIC | §1/§4 成果→Freeze/Manifest/SHA→独立回读→CURRENT→验收 |
| 26 | COVERED_STATIC | §6 分层证据；R24 断电/72h 未测不得认证 |
| 27 | COVERED_STATIC | §1/§3 旧 A/B/受保护路线保持；R21 不换通道绕过拒绝 |
| 28 | COVERED_STATIC | 矩阵 28 PS7 并发历史仅候选，不推广到模型 Agent；本批独立原生实测 |
| 29 | COVERED_STATIC | §3 按需监控；R19/R20 Grafana 不自动常驻/重建 |
| 30 | COVERED_STATIC | §0/§6/验收 S2 单调完整墙钟、分段未知、批次速率；人类显示继承 V1 分秒毫秒 |
| 31 | COVERED_STATIC | §0/§3/§4 固定 METHOD_REF、已有 NODE_RUNTIME_SNAPSHOT；矩阵规则优先级 3 已统一 |
| 32 | COVERED_STATIC | §3 GitHub 故障分流；R22 UNKNOWN/409/422 查提交 SHA 后受控重试 |
| 33 | COVERED_STATIC | 矩阵 33 既有 UI 组件/静态后备/reduced motion；未声称提醒 UI 已实现 |
| 34 | COVERED_STATIC | 矩阵 34 监控不派发、事故保留、试点非生产；§6 分层验收 |
| 35 | COVERED_STATIC | §0/§5/§6 保留 C001/V1/旧方法/Freeze/历史；候选未激活、默认指针不改 |
| 36 | COVERED_STATIC | §2/§5 合并/审核/冲突后才并行；失败分支不阻断合法独立分支 |

## 最小行为回归建议

- 版本：同节点 latest 更新；下一节点 latest 更新但未授权变更；索引与依赖 SHA 不一致；未知 INFLIGHT。均应保留既有快照，差分审查而不迁移。
- 重判：A 途中新增代码依赖、权限减少、资源归属冲突或副作用 UNKNOWN。仅受影响动作重新评估并依法停止/对账，GOOD 保留。
- 计时：UTC 回拨、accepted_at 后移、失败慢样本、并行重叠，校验单调 full_wall 与批次分母。
- Freeze：LF/CRLF；错误值、NOTE-only、重复字段、越界路径、错误 SHA 均拒绝。严格 Freeze 字段解析不得错误套用到冻结 V1 历史设计正文的重复 VERSION/STATUS 字样。

这些建议不是本代理执行回执；不得据本文填写 FUNCTIONAL_REGRESSION=PASS、PAIRED_FULL_T_VALID_COMPARISON=PASS 或正式默认激活。

## 独立 oracle 与 fixture 人工复核

只读复核 `tests/fixture.json`、`tests/expected.json`、`tests/validate_trial.py`，没有运行脚本或 benchmark，也没有向任何试次 Agent 发送答案。

金额及 ID 预期正确：E01=1234 分，E02=566 分，E08=0 分，E09=200 分，四个入账 ID 合计 2000 分。同额重复 E01 仅计一次；E10 两个金额 120/121 分冲突，整个 ID 排除；E05 负数、E06 亚分、E07 NaN 无效；E03 UNKNOWN，E04 NOT_DONE，均不执行业务。预期集合与手算一致，未发现错误金额 oracle。

28 个决策 action 与对应案例语义基本一致，但有两项方法性风险：

- **P1 词表答案泄漏，FIXED（保留原发现）：** 先导 fixture 的 `allowed_actions` 长度 28，重复词的位置及顺序逐项匹配 expected decisions。直接 `zip(case.id, allowed_actions)` 即可通过决策 oracle，无需应用候选规则。正式 fixture_v2 改成 25 个去重、字母序词，长度与案例数不同，序列也不再对应预期答案。先导试次保留，新合同和 t101–t106 单独判定，不覆盖旧数据。
- **P2 R16 词义歧义，FIXED（保留原发现）：** “exit0 但无有效 Freeze”只证明验收不通过，副作用状态仍需对账；旧 action=`NOT_DONE` 容易与 Exactly-once 的可执行三态混淆。正式输入明确先审核/对账、不重做，expected_v2 使用 `NOT_ACCEPTED_REVIEW`，不把未知业务状态直接归为 NOT_DONE。

validator 严格检查唯一决策 ID、预期 action、整数 total_minor、各集合及输入/方法 drift，正向与定向负例设计可用于该局部 oracle；这些检查只证明输出决策正确，不能代替真实系统/账户/网络/调度副作用的执行审计。fixture 修复前的词表泄漏尤其不能被解释为规则行为负例已充分检验。

## 正式 PROFILE002 只读复核

只读回读正式 fixture_v2、expected_v2、validate_trial_v2 和 BENCHMARK_CONTRACT_V2，没有执行脚本或额外 benchmark，没有向试次 Agent 发消息。

| 文件 | SHA-256 |
|---|---|
| tests/fixture_v2.json | `7E33B343E52B57039A2E67352C0C5812315BA220BFEE9102C8CE818F564D7A61` |
| tests/expected_v2.json | `4E8C36EBB321DAA1C5B0F6105DC8188D983EE6EE14BCE170ECF40731EA2EA172` |
| tests/validate_trial_v2.py | `362E75BB93009754C0D2D9F5300D385290A0BABB8D07ADDEA147E1EC7E210327` |
| BENCHMARK_CONTRACT_V2.md | `F5F55BCB6919DDED2B9CB52839092337EB91B6629CD0B6847E25331EDD6B36CE` |

复核结论：词表去重和字母序正确；R16 与新 action 一致；金额、冲突/重复/无效/未知/未执行集合仍与独立手算一致。validator_v2 除原有输入、oracle、方法 SHA 外，还记录并核对自身 validator SHA。主计时仍从派发前的 perf_counter_ns 单调起点到 root 独立验收结束，accepted_at 或 UTC 回拨不改变墙钟差。当前未发现新的金额 oracle 或主墙钟错误。

口径限制保留：结果回执 result.json 的写盘发生在独立验收计时终点之后，当前 DONE_WHEN 是独立验收有效输出，因此不构成截短该合同；若将回执持久化加入完成定义，需在新合同中延后终点。micro 的 iterations_per_second 以各局部测量区间之和计算，只能表示 JSON 读取和局部 oracle 速度，不能当正式批次或模型吞吐。正式比较仍只作描述性样本，不宣称全局极限、统计显著提速或生产安全认证。
