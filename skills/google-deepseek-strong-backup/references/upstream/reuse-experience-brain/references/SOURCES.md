# 成熟方法与本次取舍｜2026-10-27
- Anthropic官方Memory tool：https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool 。模式：跨会话外部持久文件、任务前查看入口、按需读相关记忆；具体存储由应用控制。本次复用已有文件与GitHub接口，不安装Claude工具。
- LangChain官方Memory overview：https://docs.langchain.com/oss/python/concepts/memory 。区分事实/经历/程序性规则，并讨论任务路径与后台更新；本次映射为原事实/案例卡/已验证规则，并沿用任务收尾+21点任务，不安装LangGraph。
- 这两份文档支持设计模式，不证明本机已经提速。原始执行规则仍继承现有V4.2、执行大脑25与专业包。
