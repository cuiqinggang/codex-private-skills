# EXP-DOCKER-001｜Docker启动卡死后恢复的证据边界
版本V1；核查日期2026-10-27；类型CASE/ERROR；证据层级=本机诊断、暖态恢复和只读探针，未通过下次Windows登录认证。
触发：Docker Desktop显示Starting the Docker Engine，旧健康回执和最近未就绪状态冲突。环境：Windows10 / Docker Engine 29.3.1 / Docker Desktop 4.68 / WSL docker-desktop / 原单一Startup VBS。
LAST_GOOD：原数据盘和容器数据仍在，单一现有Startup VBS存在。FIRST_DELTA：WSL bootstrap未完成数据盘识别/挂载，Engine探针超时；16:48仍为ENGINE_NOT_READY。更深层磁盘首次识别根因未完成独立认证；不能归因于历史ProgramData旧问题。
采用：先读取当前status和旧日志→复用原docker-management技能的V2.0恢复入口做最多2次受控恢复/PID核账/健康检查；UNKNOWN时不盲停系统服务、不重建卷、不改代理。此卡是历史技术路径，不授权复做系统级修改。
真实结果：2026-10-27 17:21 RECOVERED；17:26原status=ENGINE_READY及三个本地端点HTTP200；原暖态包装退出0耗2.827s；20:59只读docker info取到29.3.1。下次Windows登录自动恢复仍PENDING。
适用：同一运行环境、同类Windows+WSL启动故障时指引原项目查首次差异和最新状态。**不适用**：将历史PASS当当前健康、任意Windows机器自动修复、声称真正冷启动/断电/长期无人值守成功。
原始证据：C:\AI\Docker-Autostart-20261027\diagnostic-before.json、recovery-result.json、deployment-result.json、memory-candidate.md；C:\AI\Docker-Autostart-20261024\status.json；2026-10-27-DSE-INCREMENTAL.md。

## 2026-10-28新增｜旧暖态健康不保证下一次启动
- 新证据：2026-10-27 17:26 ENGINE_READY；2026-10-28 15:09 WSL prewarm失败，19:18 WAITING_FOR_ENGINE，19:21:59 bootstrap失败进入受控恢复，19:25:06 AUTOMATIC_RECOVERY_SUCCEEDED / ENGINE_READY；一次恢复，累计374724毫秒。LAST_GOOD=27日晚暖态可用；FIRST_DELTA=28日15:09 prewarm失败。原始证据：C:\AI\Docker-Autostart-20261024\startup.jsonl、status.json。
- 适用：从新旧时刻和现有原始状态发现重复启动失效，并在原任务权限下核对最新受控恢复结果。不适用：声称已证明下次真实登录自动启动、根因永久修复、任何系统都能自动恢复或完整T_VALID提升。不重启、不修改系统服务；保留27日原案例，不覆盖。


## 2026-10-29再发｜历史恢复并非当前在线
原C:\AI\Docker-Autostart-20261024\status.json与startup.jsonl显示2026-10-29 16:23:09+08最新状态REQUIRES_DIAGNOSIS、action=EXCEPTION、prewarmCode=-1、初始进程数0，具体报错Docker WSL prewarm failed；覆盖28日19:25:06历史ENGINE_READY作为当前状态。LAST_GOOD为28日晚本次受控恢复；FIRST_DELTA为29日预热失败。此次每日复盘只读、未执行恢复，不得报道根因已修复或下次登录认证通过。未来按原项目合同和Windows系统权限核账，不在复盘中重新启动/停止Docker。
## 2026-10-30只读状态｜第三次重复预热异常
原项目 C:\AI\Docker-Autostart-20261024\status.json 记载 2026-10-30 10:46:39+08:00，status=REQUIRES_DIAGNOSIS、prewarmCode=-1、Docker WSL prewarm failed。28日19:25历史暖态恢复PASS以及29日16:23失败均保留；LAST_GOOD仅历史窗口，FIRST_DELTA为下一次启动预热异常。30日复盘未执行Docker重启或服务修复，也未做实时Engine健康探针；不能声称当前已经恢复、根因永久解决或跨开机无人值守启动PASS。下次复用务必先核最新原状态，不因本经验自行触碰Windows/WSL底座。

## 2026-10-31最新时点｜重复失败后再次ENGINE_READY
原项目startup.jsonl显示10:47:12+08再次WSL prewarm失败（prewarmCode=-1）；11:05:57原启动流程进入WAITING_FOR_ENGINE，11:07:00.307 status.json为ENGINE_READY、prewarmCode=0、lastProbeCode=0、elapsedMilliseconds=72104。**这是比10月30日旧FAIL更近的真实结果**，但多次晨间预热失败的首要根因、下一次登录成功率及21点实时健康均未独立证明。复盘只读旧回执，未重启Docker/WSL、未修改系统设置。原始证据：C:\AI\Docker-Autostart-20261024\status.json、startup.jsonl；保留10月27—30日全部历史反例。
