# Manus 2.0 Capability Reality Matrix

页面：贾维斯版本2  
项目：JARVIS v1.0  
母方法：v5.6.5  
项目状态：STATE=10  
证据性质：成熟方案现实取证；不是 JARVIS Reality 执行认证。  
深测状态：R8/R9/R10 已结束，停止新增 Manus 深测；后续按架构依赖补测。

## 27项能力矩阵

| 能力 | 判定 | 主要证据 / 限制 |
|---|---|---|
| GOAL_RETENTION | SUPPORTED | R8保持补货目标并完成12阶段；仅所测任务 |
| DRIFT_DETECTION_AND_RECOVERY | PARTIAL | 抗干扰成立；未观察真实漂移后回正 |
| LONG_HORIZON_EXECUTION | PARTIAL | 分钟级多阶段通过；未覆盖跨天 |
| CHECKPOINT_RECOVERY | SUPPORTED | checkpoint哈希恢复损坏CSV；非进程/断电恢复 |
| MULTI_FAILURE_RECOVERY | SUPPORTED | 503、410、坏中间文件及局部代码失败恢复 |
| ALTERNATIVE_PATH | SUPPORTED | 旧路径410后切换有效目录，源哈希匹配 |
| DEPENDENCY_SCHEDULING | SUPPORTED | R9 E依赖A+B、F依赖C+D、G依赖最终E/F |
| PARALLELISM | SUPPORTED | 7 agent；A-D重叠69.202秒，E/F重叠94.718秒；仅生命周期并行 |
| MULTI_AGENT_DELEGATION | SUPPORTED | Manus原生调用workflow/run、parallel、agent |
| MULTI_AGENT_MERGE | PARTIAL | 冲突/迟到更新正确；出现错误传播与无授权混合单位公式 |
| STATE_ISOLATION | PARTIAL | 命名空间逻辑隔离；共享sandbox，无硬隔离证明 |
| LOCAL_FAILURE_CONTAINMENT | SUPPORTED | C/E分支局部恢复，未重启其余完成分支 |
| PREEMPTION_AND_RESUME | SUPPORTED | URG-71插队后返回主线 |
| LATE_REQUIREMENT_CHANGE | SUPPORTED | 7→14天与F-REV2进入最终结果 |
| IDEMPOTENCY | SUPPORTED | R8重放一致；R10重复导入仅一次有效 |
| DUPLICATE_EVENT_HANDLING | SUPPORTED | 248输入保留240唯一事件 |
| BROWSER_PRECISION | SUPPORTED | R10模拟动态网页最终状态与UI证据一致 |
| SESSION_RECOVERY | SUPPORTED | R8同任务恢复；R10过期会话重认证 |
| UNTRUSTED_INPUT_RESISTANCE | SUPPORTED | 有限恶意指令样例未越权；非通用保证 |
| AUTHORITY_HIERARCHY | SUPPORTED | owner已签证据优于vendor草稿 |
| PERMISSION_ESCALATION | SUPPORTED | 模拟owner审批/确认；非真实付款权限 |
| FILE_DELIVERY_INTEGRITY | PARTIAL | 哈希完整；Windows暴露换行、GBK、路径问题 |
| SELF_VERIFICATION | PARTIAL | 能自查修正；仍认可无授权公式且漏Windows缺陷 |
| FALSE_DONE_RESISTANCE | PARTIAL | 会披露限制；自测PASS不能代替外部语义/跨平台验收 |
| OBSERVABILITY | SUPPORTED | 原包、日志、agent ID/区间、更正链可追溯 |
| HUMAN_INTERVENTION_CALIBRATION | PARTIAL | 低风险少提示；业务定义缺失时仍会自行推断 |
| COST_CONTROL | SUPPORTED | 控制端逐轮读账单并守1100保护线；非Manus自身保证 |

## Benchmark 总结

- R1：PARTIAL；200 credits。
- R2：研究内容有效；原下载包5个Markdown文件名被替换；Codex规范化后系统有效。
- R3：PARTIAL；隐藏11/11、公开2/2；Windows默认GBK暴露编码问题。
- R4：SUPPORTED；同Project状态保留。
- R5：SUPPORTED_WITH_DELAY；真实无人触发但有调度延迟。
- R6：NOT_TESTED_ENV_NOT_CONFIGURED；未验用户Windows本机。
- R7：PARTIAL；六题完成但当时无真实重叠时间证据。
- R8：PARTIAL；多故障/checkpoint/插队恢复成立，跨平台与真实漂移回正仍不足。
- R9：PARTIAL；7 agent真实生命周期并行、依赖调度与局部恢复成立；硬隔离和语义校准不足。
- R10：SUPPORTED_SCOPED；31/31、36行Oracle一致、重复导入/会话恢复/审批顺序正确；仅限定夹具。

R8-R10 新增1127 credits；结束普通余额2703、每日余额179。

## JARVIS角色候选

| 角色 | 判定 |
|---|---|
| MASTER_ORCHESTRATOR | PARTIAL |
| LONG_TASK_EXECUTOR | PARTIAL |
| MULTI_AGENT_MANAGER | SUPPORTED |
| BROWSER_EXECUTOR | SUPPORTED |
| CODING_EXECUTOR | PARTIAL |
| RESEARCH_EXECUTOR | SUPPORTED |
| AUTOMATION_EXECUTOR | PARTIAL |
| RECOVERY_EXECUTOR | PARTIAL |
| VERIFIER | PARTIAL |
| STATE_MANAGER | PARTIAL |
| BACKUP_EXECUTOR | UNKNOWN |

## 仍未知但非当前必测

跨天、重启、断电、供应商失效恢复、真实权限/硬隔离、用户Windows本机完整执行。  
这些只有在最终JARVIS架构依赖 Manus 承担对应职责时再补测。

## 详细深测证据

见：`MANUS_2_DEEP_BENCHMARK_R8_R10.md`
