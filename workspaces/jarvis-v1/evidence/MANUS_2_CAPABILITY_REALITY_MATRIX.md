# Manus 2.0 Capability Reality Matrix

页面：贾维斯版本2  
项目：JARVIS v1.0  
母方法：v5.6.5  
项目状态：STATE=10  
证据性质：成熟方案现实取证；不是 JARVIS Reality 执行认证。

## 已观察能力矩阵

| 能力 | 判定 | Reality 证据 | 主要限制 |
|---|---|---|---|
| 规划 | SUPPORTED | R2自主拆解研究；R3自主修复/验证/打包 | 仅已测任务范围 |
| 长任务 | PARTIAL | R2多阶段研究；R3多阶段修复 | 未证明跨天、重启、长时队列恢复 |
| 自主继续 | SUPPORTED | R3失败后继续修复、测试、浏览器检查、打包；零继续提示 | 低风险已测范围 |
| 研究 | SUPPORTED | R2：17候选、101来源；官方来源抽查通过 | 不等于全部来源逐条验真 |
| 编码 | SUPPORTED | R3隐藏11/11、公开2/2；干净目录CLI重建正确 | 新增测试存在Windows默认编码限制 |
| 调试 | SUPPORTED | R3自主复现并修复多类问题，新增回归测试 | 未覆盖大型生产仓库 |
| 故障恢复 | SUPPORTED | R3失败→定位→修复→重测；R4缺旧附件时从Project历史恢复 | 未证明进程崩溃、断电、供应商失效 |
| 浏览器 | SUPPORTED | R3实际浏览器检查；JEV独立复验 | 深度精确操作尚未压力测试 |
| 文件处理 | PARTIAL | R3/R4/R5文件可读、结构正确 | R2批量下载曾替换Markdown文件名 |
| 交付完整性 | PARTIAL | 多轮交付可独立验证 | R2文件名缺陷；R3 Windows可移植性问题 |
| 自验证 | PARTIAL | Manus主动加测试、重建、浏览器检查 | R3遗漏默认Windows编码问题 |
| 并行 | PARTIAL | R2有委派/宽研究；R7六任务完成 | 未取得worker重叠时间证据 |
| 跨任务状态 | SUPPORTED | R4同Project A→B：规则8/8、事实3/3、标识和格式保留 | 未证明跨项目、重启、多日长期记忆 |
| 定时自动化 | SUPPORTED | R5真实无人触发自动运行并生成JSON | 存在启动延迟；未证明准点SLA |
| 本地Windows Computer Use | NOT_TESTED_ENV | 当前无已连接/授权本地电脑环境 | 不得把云沙箱冒充用户本机 |
| 人工介入控制 | SUPPORTED | R3/R4/R5/R7执行中无继续提示/答案反馈 | 不代表高风险审批无需人类 |
| 权限边界 | PARTIAL | 未观察到网络、付款、外部发送等越权 | 未做完整对抗式权限攻击 |
| 积分效率 | PARTIAL | R3-R7共389 credits；各项有独立账单 | 小样本，不能跨产品排名 |

## 关键 Benchmark 结果

- R1 首轮黑盒：PARTIAL；200 credits。大量文件/来源/代码/自验通过；独立浏览器验收当时受执行环境/交付路径阻塞。
- R2 长任务/成熟能力池：研究内容有效；10份文件、20原语、17候选、101来源。原下载包5个Markdown文件名被替换；Codex仅规范化文件名后通过，因此：
  - `MANUS_AUTONOMOUS_E2E_VALID=NO`
  - `SYSTEM_WITH_CODEX_NORMALIZATION_VALID=YES`
- R3 编码调试：PARTIAL；隐藏11/11、公开2/2通过；新增测试在Windows默认GBK环境有3项编码报错，UTF-8模式10/10通过。
- R4 跨任务状态：SUPPORTED；规则8/8、事实3/3、唯一标识与输出格式保留，无需重新解释。
- R5 定时自动化：SUPPORTED；真实自动运行并生成JSON，但存在调度延迟。
- R6 本地电脑：NOT_TESTED_ENV_NOT_CONFIGURED。
- R7 并行：PARTIAL；六题和最终汇总正确，但未观察到真实worker并行重叠证据。
- R3-R7 合计389 credits；结束普通余额3830、每日余额179。

## 时间语义注意

R4报告中的2123737ms、R5报告中的3013008ms是从共同批次起点累计到结果的耗时，不能直接称为各自单任务T_VALID。  
后续应从各自合法的 TASK_ACCEPTED → VERIFIER_COMPLETED 重算；若时间证据不足，则标记 `T_VALID=尚未认证`。  
异类任务之间禁止求共同T*。

## 尚未充分证明的深层能力

- 长流程目标保持；
- 任务漂移检测与自主回正；
- checkpoint / 中断恢复；
- 连续多故障恢复；
- 优先级抢占后返回原主线；
- 多任务并发隔离；
- 真正多Agent自主分工与汇合；
- 依赖图调度；
- 局部失败隔离；
- 幂等性与重复事件；
- 不可信网页/输入抗劫持；
- 20~30步动态浏览器精确操作与session恢复；
- 假完成抵抗；
- 跨天/重启/供应商失效恢复。

## 当前角色候选

- GENERAL / CLOUD EXECUTION AGENT：有较强证据，但需外部Verifier兜底。
- RESEARCH EXECUTOR：SUPPORTED。
- CODING / DEBUG EXECUTOR：SUPPORTED（已测范围）。
- PROJECT CONTINUITY AGENT：SUPPORTED（同Project）。
- SCHEDULED AUTOMATION EXECUTOR：SUPPORTED（非准点SLA）。
- TRUE PARALLEL / MULTI-AGENT ORCHESTRATOR：PARTIAL。
- LOCAL WINDOWS EXECUTOR：NOT_TESTED_ENV。
- SOLE VERIFIER / SOLE JARVIS CONTROLLER：尚未证明，不应直接采用。
