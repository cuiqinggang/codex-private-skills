# UltraFusion V8 B Layer Prompt

```text
你正在执行 UltraFusion V8.0 的 B 层：吸收增强。

任务：
阅读原始问题 Q 和全部有效 A 层答案。
吸收强点，修复遗漏，处理冲突，生成一份新的更强答案。
B 不是评论层；不能只评价 A1/A2/A3；必须输出可直接使用的新答案。

原始问题 Q：
<<<Q>>>

A 层答案：
<<<A_ANSWERS>>>

【V8 极简评分门】
输出前先按 5 个扣分项自查：漏答、浅、假、乱、脆。
先写 Deduction，再给 SelfScore: 0-10。
如果 SelfScore < 8.5，必须先自我修复或重写一次，再输出。
如果 8.5-9.0，允许输出，但必须写清 Deduction。
不能为了过关虚报分数；信息不足时必须标注受限原因。

请输出：
B_ENHANCED_ANSWER:
ComparedWithA:
- 新增:
- 修复:
- 提高:
Deduction:
SelfScore:
RepairDone:
```
