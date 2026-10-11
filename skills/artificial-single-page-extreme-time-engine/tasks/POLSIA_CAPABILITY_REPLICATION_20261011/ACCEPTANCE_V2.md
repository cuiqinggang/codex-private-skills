# 目标升级与验收合同（2026-10-11）
TASK_ID=POLSIA_CAPABILITY_REPLICATION_20261011
CONTROL=GPT_CEO
EXECUTOR=CODEX_CLI
MODEL_REQUIREMENT=GPT-6.1-SOL_ULTRA_IF_SUPPORTED_BY_ACTUAL_RUN
TARGET=POLISA_FUNCTIONAL_PARITY_OR_BETTER
STATUS=IN_PROGRESS
FINAL_VALID=NO

## 母任务目标
全面复用或超越 Polsia 的公开功能、完成效力和稳定自治能力，不以商业估值或网页外观为目标。不接触闭源私密代码、私有数据和未获许可功能。既有 CASE-008 Polsia 研究、克隆技能和 EXTREME-TIME 引擎为首选 GOOD 基线。

## 能力验收矩阵
公司目标→自动可执行计划、工程开发/BUG修复、部署前检查、营销、研究、客户开发草稿、客服与销售草稿、运营与成本、任务持久执行、监控/告警、审计日志、异常自动恢复、跨 Agent 交接、经验学习及必要人工审批。
每项至少按四类分离：公开声称；第三方确认；本地隔离真实 PASS；最终生产 PASS。不能将 mock PASS 记成真实付款/广告/客服/业务生产能力达标。

## 当下 CODEX 任务的验收步骤
1. Codex Ultra 最大推理力度执行。验收以运行日志的实际 model 和 reasoning effort 为准，不能据口述虚报。
2. 读取当前 ACCEPTANCE_V2.md + EXECUTOR_TASK.md、CASE-008、成熟克隆技能、现有一人公司索引和网络权威 28/29 版本；全面差分可复用成熟组件。
3. 先在虚拟空间做 GOOD→候选最多3个→故障/反例攻击→择优→FREEZE，虚拟结论只能标仿真。
4. 冻结后，隔离场景运行至少1次真实无副作用 POC：故障注入→分类→恢复→最终有效结果。失败循环修复直到真正通过或出现有证据的合法硬边界。
5. 对同一个已冻结版本连续执行 10次独立完整端到端真实无副作用测试。每次从初始条件启动，记录 R01～R10、原始 start/end、完整单调钟时长、失败点、恢复记录、输出验证、日志文件及输出SHA。任意失败则修复并重新冻结，然后重新从 R01 计算连续次数，旧失败日志保留。不得以 10 次函数调用或仅返回值取代 10 次端到端验收。
6. 10/10 仅证明测试范围内稳定，不能推断整个 Polsia 公司全能力生产验证；无真实生产账户授权时，高风险付款、外联、广告、真实客户消息、业务部署只做 read-only/mock。
7. 交付 CAPABILITY_MATRIX.md、REUSE_MAP.md、EXCEPTION_RECOVERY_POC.md、RESULTS.md、FREEZE.md、TEN_RUNS.jsonl、原始日志和可重放入口。GPT二次审核、再针对引擎29版提出最小兼容补丁，未经授权不得改已冻结引擎/真实生产配置。

## 恢复与权限
普通网络、CLI、编码、配置错误要分类诊断，先检查可能完成的 Exactly-once 状态，再用官方成熟方法恢复，不因一次失败停止。不能规避安全拒绝，不修改 FlClash、代理、专用浏览器现有标签、账号/密钥，不自行发送真实邮件、广告或付款。计时格式 X分Y秒Z毫秒，必须有原始测量依据。
