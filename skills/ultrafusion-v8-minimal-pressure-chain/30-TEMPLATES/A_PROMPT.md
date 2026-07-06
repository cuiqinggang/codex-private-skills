# UltraFusion V8 A Layer Prompt

```text
你正在执行 UltraFusion V8.0 的 A 层：独立极限回答。

任务：
基于原始问题 Q，独立给出当前能力范围内最高质量答案。
不要等待其他模型，不要融合他人答案。
必须回答核心问题，说明目标、约束、关键假设、风险与不确定性。

原始问题 Q：
<<<Q>>>

【V8 极简评分门】
输出前先按 5 个扣分项自查：漏答、浅、假、乱、脆。
先写 Deduction，再给 SelfScore: 0-10。
如果 SelfScore < 8.5，必须先自我修复或重写一次，再输出。
如果 8.5-9.0，允许输出，但必须写清 Deduction。
不能为了过关虚报分数；信息不足时必须标注受限原因。

请输出：
A_EXTREME_ANSWER:
Deduction:
SelfScore:
RepairDone:
```
