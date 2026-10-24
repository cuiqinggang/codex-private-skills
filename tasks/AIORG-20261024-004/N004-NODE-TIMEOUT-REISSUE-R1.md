# AIORG-20261024-004/N004/V1｜限时节点淘汰与重新执行 R1
日期 2026-10-24
主控流程无需自动换页、无人值守或长期新调度器：超时判断→安全淘汰子进程→从持久化检查点新一代执行→业务QA。
## 真实执行回执
Windows 主机执行 Python 子进程：Gen1 写 FIRST_COMMITTED 检查点及一次副作用标记后进入90秒等待；主控设定3秒deadline，于3.0206秒触发真实进程kill，确认旧PID终止。新一代Gen2从检查点恢复既有name,amount CSV真实文件业务，确认原结果未重复提交，业务排序、金额总和、ID唯一性、输出一致性QA通过。总运行墙钟3.1765秒，新进程退出0，模拟副作用计数1。
第一次回归因为脚本编码参数utf8-sig拼写错误而失败，定位错误后改为utf-8-sig并重测成功。失败探索和修复耗时未被包含在3.1765秒内，故3.1765秒不是原任务完整T_VALID。
## 原预约业务核对
已通过Tymeslot数据库只读查询核实此前改期补测的合成预约ID 2b9283c3-ae01-48d9-98fa-6e6764c2f4f2 的持久状态为cancelled，记录数1。这是先前业务清理回读，不代表本轮对Tymeslot进行了超时后重复预约提交测试。
## 边界
R1 PASS范围仅为主控限时+Windows子进程真实杀死与重发+CSV持久化业务QA。未验证真实GPT页终止、新页再投递、Tymeslot预约写入故障切换及跨页Exactly-once；不能宣称N004全合同或INC-002全面PASS。
证据 C:\AI\AIORG-Shared\tasks\AIORG-20261024-004\N004-TIMEBOX-REISSUE-REAL.py, N004-TIMEBOX-REISSUE-RESULT.json。
结论：限时节点淘汰方案通过限定Reality，保持候选。N004=PARTIAL_COMMITTED，INC-002=OPEN，FINAL_PASS=false。
