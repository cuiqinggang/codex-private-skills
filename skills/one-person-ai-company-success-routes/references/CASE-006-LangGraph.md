# CASE-006 - LangGraph

## 项目定位

LangGraph 是长运行、有状态 agent workflow 的底层编排框架。对一人 AI 公司最有价值的不是“多几个角色”，而是 durable execution、persistence、interrupt/human-in-the-loop、memory、streaming、failure recovery 等运行级能力。

## 证据

- Raw README 快照：`H:\AI\_explore\one-person-ai-company-success-routes-20260528\sources\web\LangGraph-README.md`。
- 官方/源码 URL：`https://github.com/langchain-ai/langgraph`，README raw URL `https://raw.githubusercontent.com/langchain-ai/langgraph/main/README.md`。
- License：README badge 显示 MIT/PyPI license。
- 关键 README 位置：`LangGraph-README.md:24` long-running stateful agents；`LangGraph-README.md:37-43` durable execution/HITL/memory/LangSmith debugging/deployment；`LangGraph-README.md:54-57` Deep Agents/LangSmith/Studio；`LangGraph-README.md:72` streaming/memory/persistence guides。
- 本轮验证方式：raw README + 官方文档检索，不安装包、不运行 graph。

## 重点机制

- Durable execution：失败或长时间运行后从中断点恢复，而不是整条链重跑。
- Persistence：把状态保存在 checkpointer/store 中，便于审计和重放。
- Human-in-the-loop：通过 interrupt 暂停，允许人检查/修改状态后继续。
- Memory：短期工作记忆和长期持久记忆分层。
- Streaming：长任务运行时持续暴露中间事件，减少黑箱。
- Failure recovery：失败不是异常结尾，而是可恢复状态。

## 可吸收机制

| LangGraph 机制 | 本地吸收方式 |
|---|---|
| durable execution | 运行报告必须记录 checkpoint / resume point |
| persistence | `reports/periodic-updates/`、run history、case study 版本化 |
| interrupt/HITL | 审批门、Level 3 stop gate、发送前人工确认 |
| memory | ECC 复盘、技能包更新、WATCHLIST 的长期记忆 |
| streaming events | AICompany Dashboard 的 run timeline |
| failure recovery | 每个 route 必须有 rollback path 和 stop reason |

## 风险

- LangGraph 是底层框架，直接使用需要工程投入；不适合先于控制台原型重构现有体系。
- 与 LangSmith/Deployment 生态结合紧密，SaaS 能力需分离吸收。
- 如果只学 graph 结构而不做状态持久化，价值会大幅降低。

## 是否进入技能包

进入。必须吸收 durable execution、HITL、memory、streaming、failure recovery 作为本技能包治理核心；暂缓真实代码集成。
