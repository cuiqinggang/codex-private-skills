# UltraFusion 极限有效时间竞速合同（候选补丁，2026-10-19）

状态：DESIGN_AND_TEST_CANDIDATE；禁止在三模型同合同真实验收前声明生产冻结。

## 1. 必须继承
保留 UltraFusion 6.1B 的普通问题 GPT 直答与高价值问题升级两档规则。
GPT 官网、DeepSeek 官网、Qwen 官网作为历史基线；新增候选 GPT + Gemini + DeepSeek；Qwen 保留备用，不覆盖原文件。
仅在本地真实取得 V15_Guard_Prefix + V15_FULL + 层模板 + 用户问题后，允许标记 V15_FULL_RUN。未找到则标记 NON_V15。

## 2. 第一性原理总目标
对于事先固定质量底线 Q_min、成本上限 C_max 和同任务合同的候选路线，选择 T_effective 最小者：
T_effective = 开始到质量验收通过的墙钟时间（含生成、调度、等待、操作、工具调用、执行、失败重试、返工与验收；并行段只计一次墙钟）。
未达标或失败任务必须记录失败、耗时、重试与成本，不得从样本中剔除。
评分上升不是 PASS；只有质量达标、成本受控且统计上稳定缩短完整有效时间才可进入默认执行路由。
为避免高质量但与任务无关的过度优化，使用预注册质量门槛，不临时降低合同。
如融合产生额外质量但无端到端时间净收益，仅保存为特殊质量要求场景可选，不进入默认路由。

## 3. 候选路线
A0: GPT 独立极限提示词执行全任务。
B1: GPT、Gemini、DeepSeek 并行用相同完整 V15 核心协议独立应答，然后 GPT 提取强点、定向攻击、融合、验收。
B2: GPT 基线+按需单模型协助，额外模型仅当预计净时间收益>额外耗时才启用（可选）。
与原历史 Qwen 路线并存。

## 4. 验收样本
预注册至少 12 个异质真实任务：代码修复×3、资料核验×3、信息整理×3、故障诊断×3；每题固定素材、验收脚本或人工合格门槛和禁止偷换的执行范围。
每任务两路线至少各 3 次有效独立重复，并随机交叉先后顺序，冷/热启动分层记录，防止缓存和顺序优势。
除模型与策略外，其余硬件、网络、工具、输入资料、时间窗口和质量底线保持一致。
计时为每路任务实际 start/end 单调墙钟；额外记录模型调用、融合、操作、故障、验收的耗时及新增费用。
在不具备官网合法自动化或真实回答证据时，该路线为 NOT_RUN，绝不填估计时间。

## 5. 数据表字段
task_id,task_type,run_id,route,model,version,prompt_sha,v15_status,started_at,ended_at,wall_seconds,quality_gate_pass,success,repair_seconds,retries,marginal_cost,artifacts,evidence_paths,notes

## 6. STOP_GATE
质量不足=STOP；成本超额=STOP；明显错误=STOP。
比较质量达标样本的全链路时长、成功率与失败成本；逐题报告 ΔT=T_baseline−T_fusion，speedup=T_baseline/T_fusion。
默认升级门槛：12/12任务都有完整配对数据；至少 9/12 任务融合更快；配对任务的中位净时间收益至少 15%；总体有效完成率不低于基线；边际成本未越预算。失败任务不得隐去；报告冷/热启动和置信区间。
上述门槛是本轮预注册的工程验收建议，不是历史已验证规则。
如果没有可复现净收益，停止增加融合层，保留 GPT 单模型默认路径。

## 7. 状态纪律
DESIGN_ONLY → ENVIRONMENT_PASS → BASELINE_MEASURED → FUSION_MEASURED → PAIRWISE_VALIDATED → FREEZE_APPROVED。
C 桥优先，C 经日志证实不可用才允许 A/B；不改变 FlClash 和系统代理。
未经三模型真实调用及完整交付验收，禁止写 PASS、FINAL、FROZEN。
