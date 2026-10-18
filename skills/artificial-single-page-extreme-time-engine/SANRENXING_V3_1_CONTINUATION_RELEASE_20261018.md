# 《三人行》V3.1｜连续推进最小增量发布（2026-10-18）

VERSION=SANRENXING_V3.1
RELEASE_STATUS=LIMITED_REALITY_PASS
BASELINE=SANRENXING_V3
BASELINE_FREEZE_ID=SRX-V3-F001-20261017
SCOPE=PREMATURE_STOP_AFTER_RECOVERABLE_FAULT
FULL_RUNTIME_RESILIENCE=NOT_CLAIMED

## 正式继承
V3原文件不可变；本增量只在原V3第六节“GPT自主闭环执行”基础上，补充任务终点锁定、故障修复后继续、轻量经验检索原则。
详情：[候选规则原稿](SANRENXING_V3_CONTINUATION_LESSONS_ADDENDUM_20261018.md)。
不重造状态机、调度器或数据库；现有CURRENT及专业技能包经验账本继续沿用。

## 运行最小合同
1. 复杂任务先明确USER_GOAL、DONE_EVIDENCE和NEXT_STEP；简单任务内部规划即可。修复子任务不改变USER_GOAL。
2. 有限故障优先检索成熟经验，修复并做必要回归，然后回到原NEXT_STEP，不因修复成功或中间进度总结停下等待用户“继续”。
3. 仅在原目标验收完成、必需用户授权/外部条件、安全或资源边界、客观不可恢复阻塞时停止。真实掉线后无人值守续跑需另靠已验收的持久执行器。
4. 经验按故障特征归入对应专业技能包的references/LESSONS.md或既有账本，通用规则只留简短索引；记录SYMPTOM/ROOT_CAUSE/FIX/EVIDENCE/SCOPE，未证实方案不记VERIFIED。
5. 继续保持T*=min(T_VALID)、Freeze→Reality、C→A→B、Exactly-once及UNKNOWN对账等全部V3原约束。

## 2026-10-18 有界真实验收
场景：Windows C通道创建CSV并按数值降序排序，故障后无需用户干预继续原目标。
设备：DESKTOP-4A1EGTM；通道C（Remote Desktop Commander 0.2.52）在线。
工作目录：C:\Users\A\AppData\Local\Temp\SRX_V3_CONTINUATION_E2E_20261018
输入：A,3 / B,9 / C,5。
真实故障：首个命令使用嵌套PowerShell调用，引发ParserError（ExpectedValueExpression）。
修复：不用嵌套调用，直接经C通道调用PowerShell语句，成功创建input.csv。
续跑：未征询用户继续指令，生成output.csv并检查三行数值排序9,5,3。
二次独立回读：input.csv、output.csv、acceptance.txt全部存在；输出顺序B,9 / C,5 / A,3。
验收：PASS（单次小任务、当前会话内、单一故障类型）。
证据限制：不宣称通用故障恢复、跨会话自主续跑、执行器规则自动加载、N轮稳定性或10倍加速；首次ParserError与解决动作是本次实际工具执行，不是独立自动调度器的无人值守恢复。
下一项生产能力验收：确认实际执行入口自动读取V3.1规则、跨节点保持USER_GOAL，测试会话中断后的现有持久执行器恢复；未测前一律标UNKNOWN。

## 版本判断
V3.1为最小规则与有界验收增量；V3保留原始冻结，旧任务METHOD_REF不自动变更。新任务只有明确选择V3.1或正式入口后续指向V3.1才使用此版本。
