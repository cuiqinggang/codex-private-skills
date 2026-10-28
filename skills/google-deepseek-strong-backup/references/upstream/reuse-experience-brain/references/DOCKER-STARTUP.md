# EXP-DOCKER-001｜Docker启动卡死后恢复的证据边界
版本V1；核查日期2026-10-27；类型CASE/ERROR；证据层级=本机诊断、暖态恢复和只读探针，未通过下次Windows登录认证。
触发：Docker Desktop显示Starting the Docker Engine，旧健康回执和最近未就绪状态冲突。环境：Windows10 / Docker Engine 29.3.1 / Docker Desktop 4.68 / WSL docker-desktop / 原单一Startup VBS。
LAST_GOOD：原数据盘和容器数据仍在，单一现有Startup VBS存在。FIRST_DELTA：WSL bootstrap未完成数据盘识别/挂载，Engine探针超时；16:48仍为ENGINE_NOT_READY。更深层磁盘首次识别根因未完成独立认证；不能归因于历史ProgramData旧问题。
采用：先读取当前status和旧日志→复用原docker-management技能的V2.0恢复入口做最多2次受控恢复/PID核账/健康检查；UNKNOWN时不盲停系统服务、不重建卷、不改代理。此卡是历史技术路径，不授权复做系统级修改。
真实结果：2026-10-27 17:21 RECOVERED；17:26原status=ENGINE_READY及三个本地端点HTTP200；原暖态包装退出0耗2.827s；20:59只读docker info取到29.3.1。下次Windows登录自动恢复仍PENDING。
适用：同一运行环境、同类Windows+WSL启动故障时指引原项目查首次差异和最新状态。**不适用**：将历史PASS当当前健康、任意Windows机器自动修复、声称真正冷启动/断电/长期无人值守成功。
原始证据：C:\AI\Docker-Autostart-20261027\diagnostic-before.json、recovery-result.json、deployment-result.json、memory-candidate.md；C:\AI\Docker-Autostart-20261024\status.json；2026-10-27-DSE-INCREMENTAL.md。
