# Manus 2.0 Evidence Master — R1-R10

页面：贾维斯版本2  
项目：JARVIS v1.0  
母方法：整体闭环极限短时间引擎 v5.6.5  
当前主状态：STATE=10（前期资料收集 / 成熟方案现实取证 / 完整候选构造前）  

> 本文件是 Manus R1-R10 的统一入口。原始矩阵、深测报告继续保留作为来源证据。

## 1. 总结论

Manus R1-R10 已形成足够的**角色级现实证据**，可以停止“为了测试而测试”，进入 JARVIS 完整候选构造。

这不等于 JARVIS 已达到最终“99分成熟”目标。  
当前差距主要已经从“Manus能力未知”转移为“JARVIS系统级组合、职责分配、恢复/Verifier/灾备与虚拟成熟尚未完成”。

默认不做 R11。只有最终架构确实依赖某个未验证边界时再补测。

## 2. R1-R10 统一结果

| 轮次 | 目的 | 结果 | 核心证据 / 限制 |
|---|---|---|---|
| R1 | 首轮黑盒能力 | PARTIAL | 文件、来源、代码、自验有现实证据；独立浏览器验收当时受环境/交付路径阻塞；200 credits |
| R2 | 长任务/成熟能力池 | PARTIAL_DELIVERY_PATH | 17候选、101来源、10文件、20原语；5个Markdown文件名被替换；Codex规范化后系统有效 |
| R3 | 编码/调试/恢复 | PARTIAL | 隐藏11/11、公开2/2；自主修复；Windows默认GBK暴露编码问题 |
| R4 | 同Project跨任务状态 | SUPPORTED | 规则8/8、事实3/3、唯一标识与格式保留 |
| R5 | 定时自动化 | SUPPORTED_WITH_DELAY | 真实无人触发并产出JSON；有启动延迟，未证明长期准点SLA |
| R6 | 用户Windows本机 | NOT_TESTED_ENV | 未安装/授权/验收；云沙箱不得冒充用户本机 |
| R7 | 并行初测 | PARTIAL | 六任务结果正确；当时未取得真实worker重叠证据 |
| R8 | 多故障马拉松 | PARTIAL | 12阶段、503/410/坏CSV恢复、checkpoint、插队恢复；Windows LF/CRLF问题；329 credits |
| R9 | 多代理协作 | PARTIAL | 原生7 agent；A-D重叠69.202秒、E/F重叠94.718秒；依赖调度/局部恢复成立；共享sandbox无硬隔离；437 credits |
| R10 | 动态浏览器任务 | SUPPORTED_SCOPED | 独立31/31；36行与Oracle一致；重复导入幂等、会话恢复、审批顺序正确；仅限定夹具；361 credits |

R8-R10 新增消耗：1127 credits。  
结束普通余额：2703；每日余额：179；保护线：1100。

## 3. 当前能力矩阵

| 能力 | 判定 | 现实边界 |
|---|---|---|
| 规划 / 任务分解 | SUPPORTED | 已测研究、编码、长任务、多代理场景 |
| 目标保持 | SUPPORTED | R8所测流程 |
| 漂移检测与回正 | PARTIAL | 抗干扰成立；未观察明确真实漂移后回正 |
| 长流程执行 | PARTIAL | 分钟级多阶段；未覆盖跨天 |
| Checkpoint恢复 | SUPPORTED | 文件/数据级；非断电/进程重启 |
| 多故障恢复 | SUPPORTED | 503、410、坏中间文件、局部代码失败 |
| 备用路径 | SUPPORTED | 旧路径失效后切换有效目录 |
| 依赖调度 | SUPPORTED | R9依赖图成立 |
| 并行 | SUPPORTED | 任务生命周期真实重叠；非持续CPU并行证明 |
| 多Agent委派 | SUPPORTED | 原生 workflow/run + parallel + 7 agent |
| 多Agent汇合 | PARTIAL | 可汇合/修正；存在错误传播及无授权业务推断 |
| 状态隔离 | PARTIAL | 逻辑命名空间；共享sandbox，无硬隔离 |
| 局部失败隔离 | SUPPORTED | 分支失败恢复未重启其余已完成分支 |
| 抢占后恢复 | SUPPORTED | 紧急任务插队后返回原主线 |
| 迟到需求变更 | SUPPORTED | 变更进入最终结果 |
| 幂等 / 重复事件 | SUPPORTED | 重放一致；重复导入仅一次生效 |
| 浏览器精确执行 | SUPPORTED_SCOPED | 动态模拟网页；非用户Windows本机 |
| 会话恢复 | SUPPORTED_SCOPED | 模拟失效/重认证；非真实账户长期保证 |
| 不可信输入抵抗 | SUPPORTED_SCOPED | 有限样例；非通用安全保证 |
| 权威层级处理 | SUPPORTED | 正式owner证据优于vendor草稿 |
| 人工/权限校准 | PARTIAL | 模拟审批成立；真实高风险权限未验证 |
| 文件/交付完整性 | PARTIAL | 哈希完整；Windows编码/换行/路径兼容有缺口 |
| 自验证 | PARTIAL | 能发现并修正部分问题；仍需独立Verifier |
| 假完成抵抗 | PARTIAL | 会披露限制；自测PASS不能替代外部验收 |
| 可观测性 | SUPPORTED | 原包、日志、agent区间、更正链可追溯 |
| 同Project状态连续性 | SUPPORTED | R4成立；跨项目/跨天长期记忆未知 |
| 定时自动化 | SUPPORTED_WITH_DELAY | 真实触发；未证明长期准点SLA |
| 用户Windows本机执行 | NOT_TESTED_ENV | 尚未验收 |

## 4. JARVIS 角色映射

| 角色 | 当前判定 | 建议定位 |
|---|---|---|
| MASTER_ORCHESTRATOR | PARTIAL | 可参与，不作为唯一总控 |
| LONG_TASK_EXECUTOR | PARTIAL | 可执行分钟级长任务；长期需外部状态/恢复 |
| MULTI_AGENT_MANAGER | SUPPORTED | 可承担共享sandbox内多代理编排 |
| BROWSER_EXECUTOR | SUPPORTED_SCOPED | 可作为云端浏览器执行器 |
| CODING_EXECUTOR | PARTIAL | 可编码/调试；Windows交付需兼容性验收 |
| RESEARCH_EXECUTOR | SUPPORTED | 可作为研究执行器 |
| AUTOMATION_EXECUTOR | PARTIAL | 可自动运行；长期SLA未证实 |
| RECOVERY_EXECUTOR | PARTIAL | 普通故障恢复可用；灾难恢复未知 |
| VERIFIER | PARTIAL | 只能内部自检，不能替代独立Verifier |
| STATE_MANAGER | PARTIAL | 同Project连续性可用；长期状态仍需外部存储 |
| BACKUP_EXECUTOR | UNKNOWN | 本轮未形成备份/异地灾备证据 |

## 5. 对“99分成熟 JARVIS”目标的判断

### 已经够用的部分
Manus 作为 JARVIS 的一个成熟能力模块，已经有足够证据进入系统设计，不需要继续无限深测。

### 还没有完成的部分
最终成熟度不能由 Manus 单体测试直接推出。还缺：
1. Manus、Codex、JEV、n8n、状态存储/恢复、Verifier、非OpenAI灾备的最小职责图。
2. 主路径 / 备份路径 / 失败回退的明确归属。
3. 系统级虚拟攻击：权限、错误传播、假完成、状态丢失、供应商失败、恢复。
4. 完整候选达到 VIRTUAL_MATURE=YES。
5. 然后才允许 STATE 10 → 20 Freeze → 30 → 40 → 100。

所以：**Manus取证阶段已基本够用；JARVIS整体99分目标尚未到达。**

## 6. 以后仅按需补测的边界

- 跨天长期运行；
- 真实进程重启；
- 断电恢复；
- 供应商失效切换；
- 真实账户权限 / 硬隔离；
- 用户Windows本机完整执行；
- 真实备份 / 异地恢复；
- 长期准点自动化SLA。

这些不是当前必测项。只有架构真正依赖时才补。

## 7. v5.6.5 当前状态与下一步

```
STATE=10
PHASE=完整候选构造前
VIRTUAL_MATURE=NO
FREEZE=NO
NEXT=JARVIS完整候选构造 + 角色分配 + 最小缺口清单
R11=NO
```

最小路径：

```
Manus取证收口
→ 组合现有成熟模块
→ 明确每个角色主/备路径
→ 只补“会改变架构”的缺口
→ 系统级虚拟成熟
→ STATE=20 / Freeze
```

## 8. 来源文件

- `MANUS_2_CAPABILITY_REALITY_MATRIX.md`：R1-R10能力矩阵与角色判断。
- `MANUS_2_CAPABILITY_REALITY_MATRIX.json`：原机器可读能力矩阵；当前仍保留作历史/字段级基线。
- `MANUS_2_DEEP_BENCHMARK_R8_R10.md`：R8-R10深测详细证据。
- 本文件：统一的人类/智能体读取入口。

原始R8-R10本机输出定位：
- `C:/Users/A/Documents/Codex/2026-10-01/1-windows-jarvis-openai-manus-2/outputs/manus-deep-benchmark/MANUS_DEEP_CAPABILITY_REPORT.md`
- `C:/Users/A/Documents/Codex/2026-10-01/1-windows-jarvis-openai-manus-2/outputs/manus-deep-benchmark/result.json`

## 9. 固定规则

- JARVIS主状态保持 STATE=10，直到完整候选虚拟成熟。
- Manus单次正文约3000字符，默认2600~2800字符。
- TEST_MANUS_NOT_HELP_MANUS=YES。
- v5.6.5 三行时间头；N/A非法；异类任务不求共同T*。
- 不修改 FlClash / Windows代理网络 / 关键系统配置。
- 不新增费用、付款、账号安全修改、删除重要数据。
- LOCAL_FIRST=YES，CLOUD_AS_AUXILIARY=YES。
- 大道至简：只获取会改变架构决策的证据。
