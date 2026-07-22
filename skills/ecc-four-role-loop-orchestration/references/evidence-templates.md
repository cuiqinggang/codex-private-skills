# 中文证据模板

机器文件使用英文键名，键名后面的说明以中文为准。不得把下面模板填成一堆“是／否”而没有路径、校验值、命令和独立角色。

本文件的十五个模板小节只是证据文件分类，不是新增层级；正式运行仍只有固定十二层。机器枚举值必须保持下面给出的纯英文值，中文解释写在注释或相邻正文中，不能把`PASS通过`之类中英文拼接值写进机器字段。

## 一、运行配置

```yaml
task_id: 任务编号
project_affiliation: 项目归属
task_type: production  # 可选：production真实生产、optimization开放式优化、endurance耐力验证、preparation准备
operation_type: 操作类型
size_tier: 任务规模
active_harnesses: 实际执行环境
formal_workspace: 正式工作区
shadow_workspace: 影子工作区
evidence_workspace: 证据工作区
formal_modification_authorized: 是否允许正式修改
production_goal_requires_writes: 生产目标是否需要正式写入
real_multi_agent_required: true
real_multi_agent_available: true
multi_agent_unavailable_reason: 仅准备任务无法启动真实多智能体时填写中文原因
logical_isolation_can_satisfy_gate: false
required_roles: [control, materials, execution, audit]  # 中文：控制、资料、执行、审计
time_budget_minutes: 时间预算
minimum_runtime_minutes: 仅耐力验证填写
checkpoint_interval_minutes: 仅耐力验证填写
expected_duration_lower_minutes: 有可靠同类历史数据时填写预计下界；没有时填写0并执行首次运行保守复核
max_repair_rounds: 默认3
negative_case_required: true
optimization_stop_contract: 仅开放式优化填写；包括基线、目标、候选、无收益轮数、风险上限、最长窗口和独立停止审计者
authority_drive: C
h_drive_mode: history_only  # 仅历史
k_drive_mode: disabled  # 可选：disabled禁用、user_approved_backup_only用户批准后仅备份
k_drive_user_approval_evidence_id: 启用K盘备份时的用户批准证据编号
mature_component_review_required: 是否触发成熟组件比较
mature_component_review:
  routes_compared: [直接采用, 小幅适配, 自研]
  selected_route: ADAPT_LIGHTLY  # 示例：小幅适配；也可按标准选择其他纯英文路线值
  reason: 中文理由
  build_from_scratch_reason: 仅选择BUILD_FROM_SCRATCH（从零自研）时填写
model_tool_route:
  planned: 计划模型、工具和执行环境
  actual: 实际模型、工具和执行环境
  fallback_allowed: 是否允许回退
  fallback_used: 是否发生回退
  change_authorization_evidence_id: 路线变化时必须引用证据索引中的批准证据编号
```

## 二、十二层实例

十二项逐层填写，固定层名见`twelve-layer-standard.md`：

```yaml
layer_number: 层号
english_name: 固定英文名
chinese_name: 固定中文名
status: PASS  # 可选：PASS通过、PARTIAL部分完成、BLOCKED阻塞、REJECTED拒绝
skippable: false
positioning: 本层定位
purpose: 本层目的
inputs: 本层输入
actions: 本层动作
artifacts: 本层产物
file_requirements: 本层文件要求
content_requirements: 本层内容要求
prohibitions: 本层禁止事项
time_policy: 本层时间关联
multi_agent_requirements: 本层多智能体要求
verification_method: 本层验证方法
failure_return: 失败返回
evidence_paths: 证据路径
next_layer_condition: 下一层条件
task_application: 本任务具体应用
```

## 三、已声明要求和完成台账

```yaml
# declared-requirements.json
requirement_id: REQ-001
description_chinese: 用户要求的中文原意
critical: true
acceptance_criteria: 可观察验收标准
source: 用户消息或授权位置

# completion-ledger.json
requirement_id: REQ-001
status: ACCEPTED  # 可选：ACCEPTED接受、WAIVED用户豁免、BLOCKED阻塞、REJECTED拒绝
evidence_ids: [E-001]
accepted_by_agent_id: 仅填写已登记的独立审计角色编号
chinese_conclusion: 中文结论
```

## 四、资料置信度

```yaml
source_id: SRC-001
project_affiliation: 当前项目
claim: 关键断言
confidence: VERIFIED  # 可选：VERIFIED已核实、ESTIMATE估计值、SPECULATION推测
evidence: 来源或复算
evidence_ids: [E-SOURCE-001]
used_in_final: 是否进入正式产物
explicitly_labeled: 是否显式标注
downstream_use_approved: 下游是否批准使用
uncertainty: 估计值的不确定性
```

推测不得进入正式结论。估计值进入正式产物前必须显式标注、不确定性完整并通过下游关口。

## 五、工具清单

```yaml
tool_name: 工具名
source: 工具来源
stateful: 是否保存状态
auth_required: 是否需要认证
context_cost: 上下文成本
secret_exposure_risk: 密钥暴露风险
enabled_for_stage: 允许使用的阶段
reason: 中文理由
```

如果工具清单确实不适用，可以保留空数组，但必须在`run-config.json`填写`tool_inventory_not_applicable_reason`（工具清单不适用的中文原因）。

只记录密钥是否存在、是否脱敏和风险，绝不记录真实密钥值。

## 六、真实智能体

```yaml
agent_id: 唯一编号
parent_agent_id: 父级编号
role: execution  # 可选：control控制、materials资料、execution执行、audit审计
context_id: 独立上下文
workspace: 独立工作空间
responsibility: 有边界责任
allowed_tools: 允许工具
forbidden_scope: 禁止范围
required_skills: 必需技能
runtime_start_receipt: 系统启动回执
runtime_return_receipt: 系统回传回执
runtime_receipt_source: platform_event_log  # 可选：system_trace系统追踪、runtime_api运行接口、platform_event_log平台事件日志
runtime_receipt_evidence_id: 回执原始证据编号
platform_run_id: 平台运行编号
parent_platform_run_id: 父级平台运行编号；根主控为空
started_at: 真实开始时间
returned_at: 真实回传时间
work_evidence: 实际工作和产物
measured_benefit: 时间或质量收益
merge_cost: 合并成本
orchestrator_receipt: 主控接收记录
```

回执证据文件必须来自系统追踪、运行接口或平台事件日志，并至少包含：运行来源、智能体编号、上下文编号、父级编号、启动事件、回传事件、平台运行编号、父级平台运行编号、真实起止时间、`RETURNED`（已经回传）状态和平台导出标记。结构校验不能证明文件一定由平台签发；第9层还要与平台界面或受信接口核对事件编号。

## 七、工作包

```yaml
work_package_id: WP-001
goal: 可观察目标
declared_requirement_ids: [REQ-001]
inputs: 输入和版本
dependencies: 依赖
required_skills: 必需技能
skill_use_evidence:
  - skill: 技能名
    used: true
    evidence_id: E-SKILL-001
    evidence: 读取、调用及产物符合证据
executor_agent_id: 执行智能体
auditor_agent_id: 审计智能体
write_owner_scope: 唯一写入范围
acceptance_criteria: 关键验收标准
verification_evidence: [CHECK-001]  # 必须引用deterministic-checks.json中的真实检查编号
negative_cases: 错误案例
rollback: 回滚方式
stop_condition: 停止条件
audit_accepted: 审计是否接受
status: 当前状态
```

技能证据编号必须进入证据索引并指向运行工具导出的独立事件文件。事件文件至少记录技能名、工作包、调用智能体、读取事件、使用事件、真实时间和运行导出标记；工作包里的`used: true`（已经使用）不能单独证明真实使用。

## 八、执行声明和产物清单

```yaml
# execution-claims.json
claim_id: CLAIM-001
work_package_id: WP-001
executor_agent_id: 执行智能体
statement_chinese: 执行声明中文正文
artifact_ids: [ART-001]
declared_requirement_ids: [REQ-001]
skill_evidence_ids: [E-SKILL-001]
source_ids: [SRC-001]

# artifact-manifest.json
artifact_id: ART-001
work_package_id: WP-001
path: 产物路径
evidence_copy_path: 证据目录内的产物副本相对路径
sha256: 校验值
produced_by_agent_id: 执行智能体
kind: 代码 | 报告 | 模型 | 配置 | 影子候选
disposition: 已验证 | 待部署 | 已回滚 | 已隔离
```

## 九、确定性检查

```yaml
check_id: CHECK-001
work_package_id: WP-001
check_type: SUCCESS  # 可选：SUCCESS成功、NEGATIVE错误案例、STRUCTURE结构、SAFETY安全
command_or_method: 命令或可重复方法
expected: 预期
observed: 观察
exit_code: 退出码或不适用
result: PASS  # 可选：PASS符合预期、FAIL不符合预期
evidence_id: E-CHECK-001
```

## 十、声明验收矩阵和交付复检

```yaml
# claim-acceptance-matrix.json
claim_id: CLAIM-001
auditor_agent_id: 独立审计智能体
decision: ACCEPT  # 可选：ACCEPT接受、REJECT拒绝
reason_chinese: 中文理由
evidence_ids: [E-AUDIT-001]
fact_recheck_complete: true
delivery_recheck_complete: true
repair_target_layer: 拒绝时返回层

# delivery-safety-check.json
auditor_agent_id: 独立审计智能体
metadata_checked: true
secrets_checked: true
internal_paths_checked: true
temporary_materials_checked: true
attachments_checked: true
references_checked: true
accepted: true
chinese_conclusion: 中文结论
unavailable_reason: 仅准备任务因真实多智能体不可用而未执行复检时填写
```

## 十一、返修轮次

```yaml
work_package_id: WP-001
round: 0  # 0是第一版；1、2、3分别是三次返修
executor_agent_id: 执行智能体
auditor_agent_id: 审计智能体
hypothesis: 本轮假设
strategy_changed: 第1轮起必须为true
meaningful_delta: 本轮真实变化
checks_rerun: 重新运行的检查
audit_rerun: 独立复审证据
decision: ACCEPT  # 可选：ACCEPT接受、REJECT拒绝、CONTINUE继续返修、BLOCKED阻塞
```

轮次从0开始连续；任何返修轮都要有新策略，不能跳号、重复或超过上限。

## 十二、检查点

```yaml
checkpoint_id: CP-001
timestamp: 真实时间
scheduled_for: 仅耐力任务填写计划时间
late_reason: 晚检查点真实原因
layer_number: 当前层
work_package_ids: [WP-001]
meaningful_progress: 中文真实进展
artifact_delta: 产物差异
command_or_test: 命令或测试
audit_decision: 审计决定
evidence_ids: [E-CP-001]
is_final: 是否最终检查点
```

## 十三、交接和证据索引

```yaml
# handoff.json
verified_facts: 已验证事实
completed_items: 已完成项目
skipped_items: 跳过项目及理由
open_rejections: 开放拒绝
open_blockers: 开放阻塞
recovery_entry: 恢复入口
next_resume_path: 下一恢复路径
remaining_risks: 剩余风险
agent_receipts_summary: 智能体回执摘要
skill_status: 技能状态
round_status: 返修状态
session_snapshot_summary: 会话快照摘要
tool_inventory_summary: 工具清单摘要
workspace_lifecycle_summary: 工作空间生命周期摘要
file_alias_map: 原ECC产物名与当前文件对应

# evidence-index.json
aliases: 原产物名与当前文件名映射
items:
  - evidence_id: E-001
    kind: 证据类型
    path: 证据路径
    sha256: 校验值
```

## 十四、异常早完复核

```yaml
early_completion_assessment:
  auditor_agent_id: 独立审计智能体
  reliable_history_available: 是否有可靠同类历史范围
  history_basis_evidence_ids: 有可靠历史时填写依据证据编号
  expected_duration_lower_minutes: 可靠历史下界；无历史填0
  is_anomalously_early: 本次是否按历史或首次运行规则进入异常复核
  goal_count: 目标数量
  work_package_count: 工作包数量
  artifact_count: 产物数量
  check_count: 实际检查数量
  basis_chinese: 中文判断理由
early_completion_review_accepted: true
early_completion_review:
  auditor_agent_id: 独立审计智能体
  goal_coverage_complete: true
  all_work_packages_handled: true
  required_skills_used: true
  multi_agent_receipts_complete: true
  real_outputs_present: true
  deterministic_checks_run: true
  negative_cases_run: true
  no_skipped_items: true
  independent_audit: true
  decision: ACCEPT
  chinese_reason: 中文理由
```

## 十五、双份最终验收

`final-acceptance.json`至少包含：

```yaml
final_status: PASS  # 可选：PASS通过、PARTIAL部分完成、BLOCKED阻塞、REJECTED拒绝
status_code: 机器状态码
status_code_chinese: 中文解释
status_code_evidence_ids: [E-FINAL-001]
elapsed_minutes: 实际用时
final_signer_agent_id: 控制角色编号
twelve_layers_complete: 十二层完整
declared_requirements_complete: 要求台账完整
real_multi_agent_accepted: 真实多智能体接受
skill_use_gates_accepted: 技能使用接受
independent_audit_accepted: 独立审计接受
delivery_safety_accepted: 交付安全接受
handoff_accepted: 交接接受
open_rejections: 开放拒绝数量
open_blockers: 开放阻塞
final_document_path: final-acceptance.md
final_report_path: final-report.md

# 仅endurance（耐力验证）任务需要
original_started_at: 带时区的原始开始时间
ended_at: 带时区的结束时间
runtime_driver_evidence: 持续运行驱动证据编号或可核对记录
interrupted: false
recovery_events: []  # interrupted为true时必须记录中断与恢复事件
```

`final-acceptance.md`和`final-report.md`必须用中文写原目标、证据、已完成、未完成、拒绝、阻塞、风险和最终状态，不能只返回文件夹路径。
