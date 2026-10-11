# GPT CEO + Codex Ultra 动态并行与统一监控 V4

METHOD_VERSION=V4
VERSION_POLICY=INTEGER_ONLY
ENGINE=28_UNCHANGED
WINDOWS_RUNTIME=3.1.0_UNCHANGED
BUSINESS_FREEZE=POLSIA-MOTHER-V008-F001
BUSINESS_FINAL_VALID=NO

## 组织原则
大型任务维持十个逻辑工作方向：研发、营销、客服、销售、财务、多智能体工作流、监控、恢复、学习、集成。按依赖关系动态派工，遇到单分支阻塞不停止其他独立分支。GPT CEO 负责批准与统一合并；执行分支必须有独立目录、回执和校验，禁止并发覆盖母任务版本指针。

## 并行选择
基于本机原生 PowerShell 7 测试，计算及短文件任务初始并发2，确证净收益后试4；等待型任务初始并发4，确证收益后可试8。十个方向不等于十个本机重型 Codex 进程。Codex 多 Agent 的真实最优并发尚未验证，需同合同公平实测。依据：tasks/POLSIA_CAPABILITY_REPLICATION_20261011/benchmarks/POLSIA_PARALLEL_CAPACITY_20261012.md。

## 统一持续监控
本机目录：C:\AI\Polsia-Unified-V4。原生 Windows 计划任务 Polsia-Unified-Monitor-V4 每分钟采样；桌面 Polsia Codex - Live Status 快捷方式显示单一监控台。采集结果 snapshot.json，历史事件 incidents.jsonl，十方向列表 config.json。显示 RUNNING、WAITING_CEO、READY、BLOCKED、DONE、ERROR、STALE；正常 CEO 审批等待不是故障。即使故障消除，历史事件也不删除。

## 已完成的现实验证
原生计划任务注册与十方向快照 PASS。两项独立并行试点：128项 V008 SHA 校验通过，隔离 Git 测试文件故障检测与恢复通过。监控注入故障出现红色 ALERT，故障移除后状态恢复，DETECTED/CLEARED 历史保留。五份实际 Windows 脚本与配置已经写入 skills/gpt-ceo-codex-ultra-continuation/v4/，GitHub逐一回读一致。

## 自动处理边界
Windows 本地负责持续检测和经许可的隔离安全恢复；ChatGPT 每小时条件巡检检查异常并尽可能诊断与通知。未知业务执行结果不能自动重试；不得自动批准付款、外联、广告发布或生产变更。原 Polsia 业务脚本、原计划任务、浏览器、FlClash、引擎与历史冻结均不变。严格继承先CEO批准、再核对真正Windows NEXT合同、Codex页面定位标签，最后才授权启动的双门规则。

## 未认证项目
真实 Codex 1/2/3路并行容量、复杂跨组件业务闭环、外部主动通知的完整端到端、72小时与断电冷恢复仍待验证。业务母任务 MOTHER_FINAL_VALID=NO。