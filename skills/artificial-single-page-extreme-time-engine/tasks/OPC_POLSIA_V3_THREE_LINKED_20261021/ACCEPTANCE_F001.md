# Polsia V3 × 三人行 V5 三关联业务工作项：真实隔离联测 F001
TASK_ID=OPC_POLSIA_V3_THREE_LINKED_20261021
METHOD=SANRENXING_V5
STATUS=PARTIAL: POLSIA_P2_SYNTHETIC_JOURNEY_PASS / MULTI_AGENT_DISPATCH_E2E_UNVERIFIED
CONTRACT_VERSION=1
FREEZE_VERSION=1

## 目标与正反约束
本轮目标是在不改FlClash、代理、真实账户/交易和已有生产服务前提下，复用Polsia V3现有工作流与三人行V5 GPT主执行路线，验收三个相互关联的业务工作项（客服需求→销售报价→财务核账），包括真实运行现有代码中的失败、修复、回执和独立判定，并检查下游运营、工程经验复用。不得将内存SQL/合成支付/模拟运营结果冒充真实商业业务或多AI模型协调成功。UNKNOWN不盲发。当前阶段未取得真实7–8任务并发净收益依据，不自动扩容。

## 验收对象与证据
源：C:\AI\PolsiaP2V3F3-20261020（现有V3候选）。
已阅读冻结技能 C:\Users\A\.codex\skills\polsia-clone-local-foundation-v3\SKILL.md；复用现有 scripts/test-sim-company-journey.ts（原注释为V24合成公司旅程）。
实际调用：node --experimental-test-module-mocks --import tsx scripts/test-sim-company-journey.ts
2026-10-21执行：Node进程退出码0；输出开头 scenarioId=V24, passed=true，输出末尾 crossCompanyReadDenied=true, actualDatabaseAccess=false,browserAcceptance=false,networkAccess=false,effectImprovementVerified=false。
原始输出：C:\AI\PolsiaP2V3F3-20261020\opc-three-linked-realtest-20261021.json（PowerShell UTF16编码且存在不合法JSON字符，不能冒充完整可解析JSON）；stderr 同目录 .err。已用源码和关键片段核对，不基于损坏的JSON完整解析作出任何虚假统计。
两家公司案例（社区烘焙店、独立书店）各自贯通：support→sales→finance→marketing→bounded-plan→engineering-learning。覆盖客服需要审批后解决、销售预算不足失败并修订、合成接受才进入财务、财务拒绝后返修，营销等待财务依赖、UNKNOWN受控对账、工程修复与学习规则在下一项被匹配，重复命令回执保持幂等。原始日志关键不变量包括originalFailuresUnchanged=true, realExternalActions=0, crossCompanyReadDenied=true。
这是已存在的成熟测试脚本实际运行，不是本轮从零构造了真实客户或真实收款业务。

## 结论
P2隔离业务工作流中3个以上依赖岗位联测PASS。GPT指挥3个独立真实执行代理，各自接单/反馈并被GPT独立评审/返修的控制面E2E仍未实现和验收：PARTIAL。没有完成到7–8项的扩容测试；同质量完整时间、额外协调成本和提升率未取得有效成对样本：UNKNOWN。

## NEXT
先复用V5现有派单身份和Loop/ECC/n8n可用触发，完成三个独立WORK_ITEM的派发→真实工作执行回执→GPT验收→至少一个退回修改→再次验收→母任务汇总；无证据不得升级生产并发上限。经验候选：Windows PowerShell重定向Node大量JSON输出可能采用UTF16且损坏控制字符，应检查原进程退出码并将日志按合规编码产生，不能把解析异常冒充业务失败。验收材料下次可从本合同恢复。
