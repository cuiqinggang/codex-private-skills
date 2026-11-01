# EXP-PI-LONGFLOW-001｜Pi原生RPC长流程与真实中断恢复边界
版本V1；核查日期2026-11-01；类别CASE/ERROR/CANDIDATE_RULE；证据等级=官方OMP配置、原生事件及限定合成订单独立验收。

触发：Pi普通一次性入口不能自动推进多回合目标，拟恢复运行时已经具备的原生长流程而不另造调度器。环境：Pi增强版V3、官方OMP 18.13.3、原DeepSeek提供方，Windows本地RPC goal。
LAST_GOOD：现有官方runtime及成熟订单生成器/20项校验器。FIRST_DELTA-R1：等待所有非必需MCP连接导致原生RPC首就绪帧90秒超时，尚未派发任务；FIRST_DELTA-R2：测试包装器将冻结的中文报表标题改成英文，原QA拒绝。
最小修复：遵循官方有限250毫秒MCP发现窗口、保持原冻结业务标题/QA20不变，在隔离R3测试区重测；启用RPC goal自动续行、原session保存/恢复、自动压缩后继续、有限请求重试和原生异步结果，宿主只负责边界与核账不逐轮喂继续。
真实结果：正常/受控本地进程树中断两个场景，每场3个不同合成订单包各QA20/20，27/27独立核验及7/7身份/异常退出负例PASS；原session/goal/cwd继续、第一批已完成文件SHA及mtime不变。短程测试03:48:879，原冻结至发布26:28:496，不是全部建设T_VALID。
适用：原Pi/OMP、本地受控进程退出后安全确认旧树结束且合同相同的原会话接续。**不适用**：未跑的8小时耐力、真实断电/重启、Google/浏览器提交UNKNOWN、提供方断连或强制上下文溢出恢复；配置已启用≠该故障实测。
原始证据：C:\Users\A\Documents\DSH-Workspace\pi-native-longflow-20261101\CURRENT.json、FREEZE.json、INDEPENDENT-ACCEPTANCE.json、GUARD-ACCEPTANCE.json、README.md。原项目没有单独TASK_ID，不得补造。
