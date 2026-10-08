# 成熟编排选型虚拟冻结（2026-10-08）
状态：VIRTUAL_DESIGN_FREEZE / REUSE_GATE_PARTIAL / REALITY_NOT_RUN / FINAL_VALID=NO
方法：ENGINE=24，BRAIN=21，NPT=17；方法提交=adbd305305db8696be6242e49b73dded4f99b301。

## 已验证事实
- Windows Desktop Commander 在线设备：DESKTOP-4A1EGTM，当前连接ID f6990966-5870-484b-bf79-409bc6fb963e。
- 读取 C:\AI\CEO-Auto-V1\AUTOMATION_ENGINE_24_REALITY_FREEZE_F011.md：此前真实验收5/5 PASS_FROZEN，五任务串行，总约115.67秒；该结果不等于新框架通过。
- 原实际浏览器入口：C:\AI\Playwright-Native-AI-Browser\skills\playwright-native-ai-browser\scripts\chatgpt-business-entry.js；现有 Node worker 通过 Playwright CDP 9223 连接现有浏览器。
- 原 v24_f010_orchestrator.py 维护 SQLite 状态与调度循环；v24_f010_task_worker.cjs 自行维护文件租约。二者通用编排/租约部分不得升级为正式基线。
- Python 环境未安装 hatchet-sdk、temporalio 或 prefect；Docker Engine 可以响应。

## 成熟候选及选择
优先验证 Hatchet Embedded，备选 Hatchet Lite；Temporal 与 Prefect 作为成熟对照。Hatchet 官方说明嵌入模式可携带本地引擎与PostgreSQL、无需单独Docker运行，对高频单机任务有潜在部署收益。该项尚未在用户本机实测。
官方文档 https://docs.hatchet.run/v1/running-locally ；https://docs.hatchet.run/v1/embedded 。

## 虚拟优化方案
沿用现有合法业务入口，禁止重写浏览器/CDP；采用框架任务、持久化、幂等配置与共享并发键取代现有自建通用编排；只串行实际冲突资源；Worker常驻、复用已有浏览器。对发送结果不确定的外部副作用必须查证后再决策，不允许自动重发。每个任务保留唯一任务标识、不可变Freeze与CEO合并边界。

## 门禁与下一节点
REUSE_GATE：用户指定入口读取=PASS；成熟候选核查=PASS；适配边界设计=PASS_DESIGN；完整T_VALID净收益证据=UNKNOWN。故 REUSE_GATE 尚未全部通过，不进入新增编码或生产Reality。
STOP_GATE：设计候选已收敛，但收益证据尚无，不能声称全局极限已达。下一节点先在隔离环境中采用官方成熟快速入门验证启动/空任务开销和接口可复用性、故障恢复语义；形成可验收Freeze后一次整体Reality，对比原F011的115.67秒及有效性。未通过不得取代旧能力。
没有进行真实新框架安装、任务发送或故障注入。