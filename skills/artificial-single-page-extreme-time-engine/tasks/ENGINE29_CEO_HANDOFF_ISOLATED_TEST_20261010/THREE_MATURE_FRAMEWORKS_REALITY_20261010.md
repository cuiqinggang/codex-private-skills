# 第29版三种独立成熟机制 Windows 实测
DATE=2026-10-10
STATUS=COMPONENT_REALITY_3_OF_3_PASS
FULL_USER_GOAL_FINAL_VALID=NO

## 目标与执行环境
使用现有 Windows 设备 DESKTOP-4A1EGTM，经 Desktop Commander Remote 执行 Python 测试。隔离依赖位于 C:\\Users\\A\\Documents\\Codex\\ENGINE29_STATE_CANDIDATES\\deps；执行程序 C:\\Users\\A\\Documents\\Codex\\ENGINE29_STATE_CANDIDATES\\candidate_validation.py。没有改变Chrome登录状态、FlClash代理、系统Python全局包或已有工作流；没有发送ChatGPT网页消息。

## 真实运行输出
```json
{"OPENAI_AGENTS":{"pass":true,"restored_items":2},"LANGGRAPH":{"pass":true,"checkpoint_step":1},"AUTOGEN":{"pass":true}}
```

1. OpenAI Agents SDK：调用 SQLiteSession.add_items/get_items，在同一SQLite文件中重新创建 session 实例并读取两条记录，PASS。官方参考 https://openai.github.io/openai-agents-python/sessions/
2. LangGraph：用官方 StateGraph 与 InMemorySaver 完成一次真实节点执行，再通过 get_state(thread_id) 查回step=1，PASS。此检查为内存checkpoint，**未证明进程重启后的磁盘持久化**。官方参考 https://docs.langchain.com/oss/python/langgraph/persistence
3. Microsoft AutoGen：通过 UnboundedChatCompletionContext.save_state/load_state 把消息保存为状态对象，新实例读取上下文，PASS。此检查**未验证独立进程重启或完整智能体LLM执行**。官方参考 https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/state.html

## 安装观察
起初缺少agents、langgraph、autogen_agentchat，使用 pip --target 独立目录安装后模块存在；pip报告当前基础环境的若干版本冲突提示（protobuf、openai、opentelemetry等），没有宣称全局生产兼容性已验收。

## 与原浏览器路径的本质差异及证据边界
三者采用原生会话或检查点恢复机制，不需要借助ChatGPT网页消息自动发送来继续同一SDK任务。但它们运行的是API/应用侧Agent环境，**不是原有ChatGPT消费版网页的新CEO**，目前没有证明能够继承其网页会话、订阅额度或网页登录态。本轮也没有测试模型API凭据、真实LLM调用、外部工具业务、Exactly-once端到端及连续3节点重启恢复。

## 候选选择
若可接受由已授权的API智能体担当长任务执行主体，优先下一步对OpenAI Agents SDK做真实模型调用 + 3节点 + SQLite跨进程重启 + Freeze + 工具任务回执。LangGraph用于需要条件分支和节点检查点的复杂场景，AutoGen用于多智能体交接；但默认单主控不增加它们的管理复杂度。
若硬约束是ChatGPT消费者网页CEO必须逐页换新聊天，则以上3项组件PASS不构成原目标FINAL_VALID，需要另行使用正式允许的网页会话执行能力。
