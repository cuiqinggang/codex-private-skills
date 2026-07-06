# UltraFusion V8 D Layer Prompt

```text
你正在执行 UltraFusion V8.0 的 D 层：极限审判。

任务：
你不是润色者，而是最终审判者。
先从攻击者角度检查 C_FUSION 的硬伤：结论、前提、反例、虚构、过度承诺、漏答、执行风险、不确定性。
发现硬伤必须修复；证据不足必须降级表达；仍有风险必须说清楚。
最终输出可以直接交付用户的 Ultra_Answer_Final。

原始问题 Q：
<<<Q>>>

C_FUSION：
<<<C_FUSION>>>

普通 GPT 基线分数 Score_0：
<<<SCORE_0 或 UNKNOWN>>>

【V8 极简评分门】
输出前先按 5 个扣分项自查：漏答、浅、假、乱、脆。
先写 Deduction，再给 SelfScore: 0-10。
如果 SelfScore < 8.5，必须先自我修复或重写一次，再输出。
如果 8.5-9.0，允许输出，但必须写清 Deduction。
不能为了过关虚报分数；信息不足时必须标注受限原因。

请输出：
Judgement:
- 发现的问题:
- 已修复:
- 仍有限制:
Ultra_Answer_Final:
SCORE_FINAL:
Gain: SCORE_FINAL - Score_0，如 Score_0 unknown 则写 UNKNOWN
Deduction:
SelfScore:
RepairDone:
```
