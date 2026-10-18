# 《三人行》第3版｜任务终点锁定与经验复用最小增补（2026-10-18）

STATUS=RULES_DRAFT_NOT_RUNTIME_VERIFIED
BASELINE=SANRENXING_V3
BASELINE_FREEZE_ID=SRX-V3-F001-20261017
SCOPE=TASK_CONTINUATION_AND_LESSON_REUSE
NO_NEW_ORCHESTRATOR=TRUE

## 目的
只处理一个已经反复出现的故障：GPT完成了局部修复或阶段任务，却未经允许把局部完成当作整体完成，停下等待用户再次说“继续”。继承V3原有虚拟成熟、Freeze、Reality、证据验收与Windows执行桥路由，不增加第二套调度/状态机。

## 执行契约（复杂任务必须先规划，简单任务最短形式）
在任务开始一次性确定：USER_GOAL（用户原始终点）、DONE_EVIDENCE（终验收证据）、NEXT_STEP（最小下一步）、STOP_REASONS（合法停止原因）、CURRENT_REF（现有CURRENT/任务状态引用）。简单任务可在内部完成契约；涉及多节点、跨工具、故障恢复时须写入现有任务CURRENT。不得把修复子步骤改写为新USER_GOAL。

## 连续推进与停止门
- 每完成一步：依据原USER_GOAL检查是否已有终验证据；若无，立即继续NEXT_STEP，不以阶段总结替代推进。
- 故障：保留原USER_GOAL与CURRENT_REF → 读取最相关的已验证经验 → GOOD/BAD/FIRST_DELTA → 最小修复 → 必要回归 → 回到原未完成NEXT_STEP。
- 必须停下仅限：终验收完成；用户授权/选择确实不可代替；安全边界、外部权限、资源预算或不可恢复阻塞；会话/工具的客观限制。其他情况禁止自主提前宣告结束。
- 仅在合法阻塞时输出阻塞证据、已完成事实和可复制的下一页续跑指令；不得假装后台仍在执行。
- UNKNOWN先核对再重试；幂等/Exactly-once与原有安全限制不变。不得无限循环自动重试。
- 跨会话/实际掉线自动续跑依赖已运行的持久执行器和状态恢复机制；单靠提示词或本文件不能保证，须另行真实验收。

## 经验存放与检索：沿用仓库，不建数据库
入口：本增补文件 + 原V3 + 任务CURRENT。经验正文优先归属于对应专业技能包的现有references/失败账本；没有现成账本时在相应技能目录新增单个 `references/LESSONS.md`。跨项目通用经验在本文件保留短索引，指向唯一权威正文，不复制全文。
每条经验建议最多6项：KEY（故障特征词）、SYMPTOM、ROOT_CAUSE、VERIFIED_FIX、VERIFICATION_EVIDENCE、SCOPE/LIMIT。只有实际通过验证的修复进入 VERIFIED；未经验证的想法标 CANDIDATE，不自动套用。
开始时根据任务领域/错误特征检索少量最相关条目，先适用性验证再复用；不把整个历史知识库注入上下文。新增经验先查重，复用原记录并补验证证据。

## 首条跨项目经验索引（已有V3规则，未证实自动运行）
KEY=PREMATURE_STOP_AFTER_REPAIR
SYMPTOM=中途修好工具/连接/插件后提前结束，没有返回用户原目标
ROOT_CAUSE=执行规则与实际入口未形成可验收的终点约束
FIX_POLICY=保存USER_GOAL与NEXT_STEP；修复后恢复原NEXT_STEP；只有合法停止门允许结束
VERIFICATION_STATUS=RULE_DEFINED_RUNTIME_NOT_YET_VERIFIED
SOURCE=SANRENXING_V3.md 第六节

## 最小真实验收（尚未执行）
选一项有2个以上真实节点、可安全插入可恢复故障的业务：
1. 记录原目标、终验收、起始CURRENT和NEXT_STEP。
2. 在中途引入一个已知可恢复的非破坏性故障。
3. 验证执行器自行修复后，**不等用户说继续**，返回原NEXT_STEP并推进到终验收。
4. 中断/恢复另单独检验；只有实际具备持久执行器时才声称跨会话无人值守恢复。
5. 对比同合同完整T_VALID，未通过则保持规则草案状态，不宣称10倍加速。

## 集成边界
本文件是V3规则的候选增量说明，并不改动冻结V3，不代表已接入各执行入口，更不表示真实连续执行已验收。待最小业务验收通过后，再依既有版本流程决定是否正式纳入新版本。
