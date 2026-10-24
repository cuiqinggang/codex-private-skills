# AI 化组织｜限时节点淘汰与重新发布 V1 候选
任务：AIORG-20261024-004/N004/V1；版本性质：规则候选，尚未通过无人值守真实故障演练。
核心：任务持续而节点可替换。无需自动接管旧 GPT 页面；使用现有轻量状态持久化、ECC、DSH、n8n/官方执行入口，不新造调度器。
1. 每个节点发布前持久化 TASK_ID、NODE_ID、GENERATION、质量合同、起点、deadline、进度回执和外部副作用幂等键。线上 GitHub 共同工作区优先，C:\AI\AIORG-Shared 为备用。
2. 先用同合同历史真实完成时间T_valid_baseline和关键路径下界T_phys_lower决定超时预算，而不是所有节点一律固定分钟。建议初始候选 hard_limit=max(3*T_baseline, T_baseline+2*T_recovery_p95)；缺数据则以可检验阶段性checkpoint加短周期健康检查，超时时限须标记待校准，不能臆造物理下界。若超过 hard_limit 但仍有经证据证明的有效不可中断提交，先安全对账。
3. 正常完成且 QA 通过：冻结 CONFIRMED_COMMITTED；不重复已冻结结果。页面未完成、缺进度或超时：本执行代标记 EXPIRED_SUSPECTED，不直接认定业务失败。
4. 先对账预约/邮件/支付等不可逆副作用（CONFIRMED_COMMITTED/CONFIRMED_NOT_EXECUTED/UNKNOWN）；只有确认旧执行权失效（fencing/lease）后才安全终止旧执行者，并以相同 TASK_ID、下一个 GENERATION 发布剩余业务。关闭旧页面是清理动作，不得在未确认新执行已接单时宣称“自动续跑”。
5. 已授权持久执行者的 DISPATCH_ACK + 新节点结果回执才算真实重新发布；若没有执行入口权限，保存 OPEN 与明确阻断和恢复方式，不能说已经自动换页、自动继续，也不宣称任务完成。
6. 计时从原任务启动至最终独立 QA 通过，全部尝试、失败等待、对账、重发及恢复均计入完整 T_VALID。目标 min(T_VALID)；评价时同时记录成功率、超时/未完成次数，不能仅报合格轮时间。
7. 演练门槛：真实节点卡住/超时，验证旧节点撤销、无重复预约、新节点真实接单与继续，完整交付 QA，方能把此规则从候选升级到成熟。现有 INC-002 与 N004 保持 OPEN。
