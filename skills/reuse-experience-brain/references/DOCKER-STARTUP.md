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

## 2026-11-01最新时点｜16:30再度受控恢复
原startup.jsonl：2026-11-01 16:23:33+08进入WAITING_FOR_ENGINE，16:26:45确认WSL/Docker bootstrap失败、仅本次原业务流程进入RECOVERING；16:30:33为AUTOMATIC_RECOVERY_SUCCEEDED与ENGINE_READY，status.json记录prewarmCode=0、lastProbeCode=0、elapsedMilliseconds=427102（07:07:102）。相比10月31日11:07的旧READY，这是更新的时点状态，但旧恢复不等于未来启动恒可靠，更深首次差异和跨多日无人值守仍未认证。复盘本身没有操作Docker、服务或系统配置。原始证据：C:\AI\Docker-Autostart-20261024\startup.jsonl、status.json。仅作为同类故障历史经验与下一次只读诊断入口。


## 2026-11-02最新时点｜20:08再次失效（只读）
原C:\AI\Docker-Autostart-20261024\status.json于2026-11-02 20:08:28+08:00写明REQUIRES_DIAGNOSIS、action=EXCEPTION、prewarmCode=-1、Docker WSL prewarm failed、initialProcessCount=0。LAST_GOOD=11月1日16:30:33的受控ENGINE_READY，FIRST_DELTA=11月2日20:08:28新的WSL预热失败。**最新原回执是异常，历史READY不可当当前健康**；此时重复触发的根因、跨登录无人值守和恢复是否成功均UNKNOWN。2026-11-02复盘没有重启Docker、WSL或修改Windows系统/代理。原始回执保留原路径，本卡仅指向核账，不授权系统操作。

## 2026-11-03最新时点｜19:13同一预热故障再现
原C:\\AI\\Docker-Autostart-20261024\\status.json于2026-11-03 19:13:14.661+08:00记录REQUIRES_DIAGNOSIS、EXCEPTION、prewarmCode=-1、Docker WSL prewarm failed、initialProcessCount=0；startup.jsonl末项同值。继承11月2日20:08故障和更早11月1日16:30 ENGINE_READY，**最新可读原回执依旧是故障**。复盘只读，没有重启/修复WSL或Docker，没有最新成功回归；根因及下次登录可靠性UNKNOWN。仅为旧EXP-DOCKER-001的同指纹新日期证据，不新建卡；采用时必须重新核对现时状态和原授权边界。

## 2026-11-05最新原始只读状态｜00:18成功，15:51再次故障
Windows收费A本次独立读取原`C:\AI\Docker-Autostart-20261024\startup.jsonl`末18条及`status.json`：11月4日22:02:54预热失败；11月5日00:13:53等待后00:17:01受控恢复，00:18:51.542原回执FINAL=ENGINE_READY、prewarmCode=0、elapsedMilliseconds=303395；**同日15:51:13.283最新status.json为REQUIRES_DIAGNOSIS、EXCEPTION、prewarmCode=-1，错误仍为Docker WSL prewarm failed、initialProcessCount=0**。LAST_GOOD=00:18历史恢复；FIRST_DELTA=15:51再次预热失败；本次最小修复/回归=NOT_PERFORMED，根因=UNKNOWN。较晚的失败是本轮最新状态，不用00:18的历史PASS覆盖它。复盘未改Windows系统、WSL/Docker或代理。此卡仅增加可复用的日期边界，不重建技能/任务或授权自动重启；下一次必须先读原状态再按原合同处理。

## 2026-11-06｜09:33原启动流程再次受控恢复（取代5日当前故障状态）

Windows收费A只读原C:\AI\Docker-Autostart-20261024\status.json及startup.jsonl末12条：11月5日15:51:13为REQUIRES_DIAGNOSIS；11月6日09:28:18进入WAITING_FOR_ENGINE，09:31:24确认启动失效开始原受控RECOVERING，**09:33:02.607最终ENGINE_READY、prewarmCode=0、lastProbeCode=0、recoveryAttempt=1、elapsedMilliseconds=289770**。LAST_GOOD为5日00:18历史成功，FIRST_DELTA为5日15:51重复预热失败，最小修复/回归来自**原启动任务**，本每日复盘只读并未操作Docker。较新09:33已覆盖5日故障作为原项目最新文件状态；不证明21:00实时服务探针、下一次真实登录自动启动成功率或根因永久消失。方法与Freeze不变，T_VALID记忆净改善NOT_MEASURED。


## 2026-11-07 18:03最新原回执｜昨日恢复后同指纹再次失败
原C:\AI\Docker-Autostart-20261024\status.json与startup.jsonl最新一项为2026-11-07T18:03:23.5073525+08:00：REQUIRES_DIAGNOSIS、EXCEPTION、prewarmCode=-1、lastProbeCode=-1、initialProcessCount=0、Docker WSL prewarm failed。LAST_GOOD=2026-11-06 09:33:02.607的ENGINE_READY（历史成功）；FIRST_DELTA=2026-11-07 18:03重复预热异常。2026-11-07 21点复盘只读，没有维修/重启、更晚成功回归或独立引擎探针；根因、跨登录长期自动恢复和服务此刻在线均UNKNOWN。旧成功/失败原位保留，仅按最新原文件状态纠正当前判断。本卡不授权修改Windows/WSL/Docker或代理，记忆净完整T_VALID NOT_MEASURED。

## 2026-11-08 16:37新时点｜WSL预热同指纹仍失败
原C:\AI\Docker-Autostart-20261024\status.json只读回执时间2026-11-08T16:37:49.3458641+08:00，status=REQUIRES_DIAGNOSIS、action=EXCEPTION、prewarmCode=-1、lastProbeCode=-1、错误Docker WSL prewarm failed。LAST_GOOD=11月6日09:33历史ENGINE_READY；FIRST_DELTA=11月7日18:03相同故障，11月8日16:37再次失败；本轮无修复或回归，也未做实时Engine探针。21点复盘只读，不能宣布当前健康、根因已解或长期自动恢复成功。原任务下一合法节点是只读核账与授权边界审查，禁止用经验卡自行重启或改动Windows/WSL/Docker。

## 2026-11-09 17:03新时点｜重复预热故障仍未修复

2026-11-09原本机只读 `C:\AI\Docker-Autostart-20261024\status.json` 回执：`time=2026-11-09T17:03:40.4098494+08:00`、`status=REQUIRES_DIAGNOSIS`、`action=EXCEPTION`、`prewarmCode=-1`、`initialProcessCount=0`、`exception=Docker WSL prewarm failed`。LAST_GOOD仍是11月6日09:33原启动流程历史ENGINE_READY；FIRST_DELTA为11月7日18:03重新出现预热失败，8日16:37与9日17:03连续新增相同指纹。此复盘未做系统修复/重启、没有当次恢复或现场Engine健康回归，根因与下次自动登录可靠性UNKNOWN。只对原卡补最新时点，不重复创建技能或放宽Windows/代理边界；现时状态使用前必须再读最新原任务回执。记忆完整业务T_VALID净收益NOT_MEASURED。

## 2026-11-10｜15:39启动预热失败；20:29普通打开后Engine可访问（不同合同）

原本机只读 C:/AI/Docker-Autostart-20261024/status.json 事件2026-11-10T15:39:51.4960185+08:00：REQUIRES_DIAGNOSIS、EXCEPTION、prewarmCode=-1、Docker WSL prewarm failed。原启动流程仍有与11月9日同指纹的自动预热问题，11月6日09:33 ENGINE_READY只是更早历史回执。另有不同任务ECC-MATT-LONG-20261110-01的 LONG-ENVIRONMENT-20261110.json，于20:29记录用户正常启动现有Docker Desktop后docker --context desktop-linux ps退出码0、现有业务实例仍在。**普通启动后Engine当前可访问，不等于自动启动预热失败被修复，亦不证明长期无人值守。** 本每日复盘未改Windows/WSL/代理、未重启服务，重复故障根因UNKNOWN，自动登录恢复回归NOT_MEASURED。下一次先核项目原status/startup和是否手动打开，再按原授权边界判断，避免以不同健康层次覆盖历史失败。

## 2026-11-11 19:36原启动流程最新受控恢复（不是21点复盘维修）
原C:/AI/Docker-Autostart-20261024/status.json于2026-11-11T19:36:55.8431257+08:00记录ENGINE_READY、action=FINAL、prewarmCode=0、lastProbeCode=0、recoveryAttempt=1、elapsedMilliseconds=381269（06:21:269），比11月10日15:39 WSL prewarm故障及20:29另一业务普通开启后Engine可访问更近。LAST_GOOD=前次普通启动可用；FIRST_DELTA=历史登录自动预热重复失败；本次原启动任务自身受控恢复成功，不是本次只读复盘重启或改变系统。未来真实自然开机恢复概率、根因、复盘时独立GUI探针仍UNKNOWN；此卡不授权修改WSL、Docker服务、ACL或代理，不把单次恢复当长期稳定。完整记忆净T_VALID=NOT_MEASURED。

## 2026-11-12 18:07状态转为预热完成后引擎探针失败（不同故障指纹）
实际只读原`C:/AI/Docker-Autostart-20261024/status.json`：`time=2026-11-12T18:07:59.8915252+08:00`、`status=REQUIRES_DIAGNOSIS`、`action=FINAL`、`prewarmCode=0`、`lastProbeCode=-1`、`elapsedMilliseconds=263476`、`initialProcessCount=0`。LAST_GOOD为11月11日19:36受控恢复ENGINE_READY/prewarmCode=0/lastProbeCode=0，FIRST_DELTA是11月12日晚新故障。**区别于此前prewarmCode=-1的WSL预热中断，本次预热码为0但最后Engine探针未通过；具体根因未核实**，也不能由这两个返回码直接判定进程不存在。复盘没有重启Docker、WSL、修改代理或系统设置；仅由原启动项目核对应时间`startup.jsonl`、第一次失败与原权限合同再定向处理，真实自然开机稳定性仍UNKNOWN。不是永久修复回归，也不是记忆T_VALID净提速。


## 2026-11-13 18:49｜预热中断再次发生，区别于12日探针失败
原 `C:/AI/Docker-Autostart-20261024/status.json` 只读记录`time=2026-11-13T18:49:29.9023977+08:00`，`REQUIRES_DIAGNOSIS`、`action=EXCEPTION`、`prewarmCode=-1`、`lastProbeCode=-1`、`Docker WSL prewarm failed`、`recoveryAttempt=1`；原`startup.jsonl`同一任务历史继续保留。11月12日18:07较早的`prewarmCode=0,lastProbeCode=-1`是另一故障指纹，11月11日19:36 READY更早。最新原状态为失败；具体首次差异和根因UNKNOWN，不宣称21点实时Engine单独探针、下次开机恢复或自动修复。每日复盘只读，不启动/停止Docker/WSL、不更改系统/ACL/代理。只在原EXP-DOCKER-001旧卡追加时间，不新建重复卡；记忆完整T_VALID净收益NOT_MEASURED。
