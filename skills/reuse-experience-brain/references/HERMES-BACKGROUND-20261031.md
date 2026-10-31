# EXP-HERMES-BG-001｜复用原生定时运行与业务接续，不新增调度器
版本：V1；核查：2026-10-31 11:41（北京时间）；分类：CASE/ERROR/SKILL_CANDIDATE；证据：Hermes原生任务执行账本与14项独立QA。

触发：AI组织需要后台定时接单、失效接续与持久历史，优先成熟平台实现，不能令所有即时业务增加调度延迟。
环境：现有Hermes 0.21.5原生cron、原独立订单服务与锁/检查点，使用已有本机Hermes解释器和HERMES_HOME；本次不新建第二个调度器。
LAST_GOOD：已有合法单端任务编号与文件SHA、原服务独立20项验收；FIRST_DELTA：首次测试业务TASK_ID不符合order-test-前缀，修正后外部Python继承Hermes的PYTHONPATH/PYTHONHOME/VIRTUAL_ENV等导致环境冲突。
最小修复：使用合法测试前缀并按原账本核对UNKNOWN/未提交，子进程清理Python继承环境；继续原生cron排程及原业务入口。正常业务和生成后主执行器退出的接续结果各20/20，4文件哈希与mtime未重写；合成简报覆盖4条输入，最终14/14独立检查PASS。一次性测试作业已disabled，原周任务未变。
原生执行时长：正常31.280s、接续31.152s、合成简报102.524s；从计划触发至终态57.897/58.216/158.846s。轮询等开销不可忽略，不能认定比即时直达更快。测试中有工程修复3类、用户故障接管0，不等于无人编排或全流程自修。
适用：定时报告、变化监测、成熟订单有限状态接续。**不适用**：未接入的真实邮箱、购物、证券账户、邮件发送与实际交易；未验整机重启/长期运行；不将合成简报的格式覆盖解释为真实语义分类。
源：C:\Users\A\Documents\DSH-Workspace\aiorg-background-20261031\FREEZE.json、ACCEPTANCE.json、RESULT.md。