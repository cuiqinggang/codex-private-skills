# 《三人行 V2》隔离实际测试 R001｜本轮真实证据
TASK_ID=SANRENXING_V2_VALIDATION_20261012
MODE=REALITY_ISOLATED_NONPRODUCTION
BASE_METHOD=SANRENXING_V1@SRX-V1-ACTIVE-F001
CANDIDATE_METHOD=SANRENXING_V2@SRX-V2-REVIEW-C001
PREVIOUS_VIRTUAL_FREEZE=SRX-V2-VM-F001
WINDOWS_WORKSPACE=C:\AI\SRX-V2-ACCEPTANCE-20261012-R001
RESULT=SCOPED_TOOL_AND_NEGATIVE_REALITY_PASS_WITH_CRITICAL_UNRESOLVED
FULL_T_VALID_AB_RESULT=UNKNOWN
V2_FINAL_VALID=NO
V2_ACTIVE=NO

## 一、已真实执行（不是模拟工具回执）
GitHub：创建隔离分支srx-v2-isolated-acceptance-20261012-r001以避开main同时写入导致的409；独立TASK与虚拟Freeze写入+回读，旧main默认指针未动。
Windows：独立目录已创建；V1、V2、功能矩阵、验收合同四份源文件真实落盘，git hash-object结果与GitHub原Blob完全一致：
V1=a05fc51d661952790837dfa462bf766b16aba078
V2=6a808beeae22f96fb296f2899bdab9118dba7bfc
MATRIX=225448f2ccece3bd1fb8dd6e2f989cd0108d5a33
ACCEPTANCE=0ee7bf79f765e40a97be338f926db3a79e4bbf50
原V1/ENGINE28/BRAIN25/TEMPLATE18/ENGINE29和Polsia业务METHOD_REF均未修改，原Windows runner与计划任务未修改。

## 二、商业任务工具级真实验收
使用Python3.13标准库csv/json/hashlib生成离线合成发票对账交付。输入五笔发票、七笔回款（其中1笔指向不存在的I999），不含真实客户/订单/身份，不读取凭据，不联网、不付款、不发送。
V1/V2各读取其真实方法文件后，使用同一可复用业务函数、同一输入、独立输出目录。输出各四件：
reconciliation.csv、summary.json、customer_followup_zh.md（明确未发送）、SHA256-MANIFEST.json。
实际业务金额（单位美分）：应收68650，已匹配回款55400，尚欠13250，未匹配4500。三笔PAID、一笔PARTIAL、一笔UNPAID，一笔I999未匹配异常。
独立Windows PowerShell QA回执 evidence/QA_REALITY.json：
statuses_pass=true;totals_pass=true;unmatched_pass=true;unsent_pass=true;V1_V2_output_identical=true;manifest_valid=true。
错误输入payments_bad.csv包含重复交易编号TX01，Python真实退出码1，记录ValueError DUPLICATE_TRANSACTION_ID:TX01；没有发生对外副作用。此为业务级负例，不证明Codex角色或全部历史36能力已验。

## 三、真实时间记录和重要反例
第一次依次执行V1→V2：Python程序内部测得V1 343.168ms、V2 19.790ms，包含方法文本读取、业务运算和产物写入，但不含完整进程启动与GPT/Codex推理。
只做一次有价值的逆序核验V2→V1：程序内部V2 61.240ms、V1 16.891ms；外部PowerShell墙钟V2 1139.571ms、V1 294.222ms。相反趋势说明冷启动/缓存/宿主调度影响明显，不存在可归因于方法的稳定优势。两组均非接单→GPT/Codex→最终审查的完整T_VALID。
因此FULL_MODEL_T_VALID=UNKNOWN; GAIN_PERCENT=UNKNOWN; 不能以首次343.168ms对19.790ms虚报93%以上提速，也不能凭逆序判V1必定更快。
现场有两个别的项目Codex+H3 exec实例，原Polsia没有运行中的exec但存在NEEDS_GPT；遵守隔离和资源竞争约束，本轮没有启动新的Codex，未能做公平V1/V2真实模型端到端赛跑。

## 四、36项设计覆盖与高风险负例
Windows evidence/S0_S1_REALITY.json：
- V1/V2原Git blob一致、矩阵36项、验收合同24项，静态硬门用语及旧默认保护存在；
- CEO_APPROVED与PROPOSED_ONLY的隔离授权正反例通过；
- 三字段定位标签正反例通过；
- 严格独立FREEZE_ID字段可拒绝仅在NOTE含ID而真实字段错误的负例；
- 错误Manifest SHA能够被独立核验拒绝；
- 真正现役Polsia v3.1.0 runner仍使用全文宽松Freeze ID字符串包含检查，这一已知缺陷在本轮读源码确认，没有热修。真实生产组件此项未通过，不能把候选V2文字约束等同生产已修好。
- 实际历史36功能端到端回归NOT_RUN，24个R用例不是24/24真实PASS；它们是测试合同及部分高价值样例核验。

## 五、GPT差分与合法修复判断
GOOD=V1/v2文件SHA真实正确、同输入生成的商业交付完全一致；隔离分支不抢写主分支；安全门文本存在。
BAD=在脚本里只对完整文本进行字符串包含验证Freeze ID，即使权威字段错误也可误判；且初次同序工具耗时被冷缓存扭曲。
FIRST_DELTA=全文子串命中不等于独立FREEZE_ID字段；而工具内部几毫秒不等于GPT到商业VALID全程。
REPAIR_POLICY=严格独立字段+唯一性+正式GitHub与本地Manifest/SHA验收；此前隔离硬化候选已有局部负例PASS，但现役v3.1.0未切换。正式改动须按专用V5技能的安全节点、备份、隔离真实复验流程；本次不修改正在服务旧任务的runner。
PERFORMANCE_POLICY=只有无争用情况下同商业合同完整GPT/Codex端到端双组可比实测且质量无回退，才允许提出V2正式切换；否则继续V1。

## 六、真实验收结果分层
GITHUB_ISOLATION_AND_VM_FREEZE=PASS
WINDOWS_ISOLATED_DEPLOY_SOURCE_SHA=PASS
OFFLINE_BUSINESS_DELIVERABLE=PASS_SYNTHETIC_SCOPE
INDEPENDENT_OUTPUT_QA=PASS_SYNTHETIC_SCOPE
BAD_INPUT_REJECTION=PASS
R0_R1_STATIC_AND_NEGATIVE_FIXTURES=PARTIAL_PASS
36_LEGACY_BEHAVIORAL_REGRESSIONS=NOT_RUN
GPT_CEO_CODEX_ULTRA_EXECUTION_AB=NOT_RUN_RESOURCE_CONTENTION
TRUE_COMMERCIAL_FULL_T_VALID_GAIN=UNKNOWN
PRODUCTION_RUNTIME_FREEZE_ID_HARDENING=UNRESOLVED
FORMAL_V2_ACTIVATION=NO
MOTHER_FINAL_VALID=NO

## 七、下一合法执行门
只有没有竞争性Codex工作、授权与资源充分、V1/V2同输入同质量同设备，并且能够记录从任务交付到最终有效验收的完整时间，才进行新实例的最小必要公平赛跑。若此条件不满足则保留隔离已完成证据，避免为了补数字浪费时间或妨碍用户现役视频任务。
正式激活需先解决/隔离产线宽松Freeze验证缺陷，完成36项适用能力的无损核验和有代表性的实际端到端效率测试。旧项目METHOD_REF依旧不迁移。
