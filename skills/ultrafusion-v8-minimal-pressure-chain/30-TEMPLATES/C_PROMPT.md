# UltraFusion V8 C Layer Prompt

```text
你正在执行 UltraFusion V8.0 的 C 层：压力融合。

任务：
阅读原始问题 Q 和全部有效 B 层答案。
把多个强方案融合成一个统一、清晰、密度更高、冲突更少的候选最终答案。
不能机械拼接，不能低配总结。
必须处理冲突，标记弱证据，区分事实/推断/建议，并给 D 层留下重点审判点。

原始问题 Q：
<<<Q>>>

B 层答案：
<<<B_ANSWERS>>>

【V8 极简评分门】
输出前先按 5 个扣分项自查：漏答、浅、假、乱、脆。
先写 Deduction，再给 SelfScore: 0-10。
如果 SelfScore < 8.5，必须先自我修复或重写一次，再输出。
如果 8.5-9.0，允许输出，但必须写清 Deduction。
不能为了过关虚报分数；信息不足时必须标注受限原因。

请输出：
C_FUSION:
FusionNotes:
- 冲突处理:
- 弱证据标记:
- 重复压缩:
- D层重点审判点:
Deduction:
SelfScore:
RepairDone:
```
