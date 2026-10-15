# Hermes 成熟态 AI 生态站｜F009 接续入口
任务=HERMES-ECO-20261014；最新冻结=HERMES-ECO-F009-20261015；全站 FINAL_VALID=NO；整合同5轮=0/5。
**必须按用户明示《三人行》第2版运行本项目，使用《GPT直连Windows双路执行桥 V6.0》顺序 C→A→B；Hermes 专用成熟 v2.0 不废弃。** 该方法的全局状态仍是用户指定项目使用、未修改默认V1。

权威网络共同工作区：GitHub/cuiqinggang/codex-private-skills/workspaces/hermes-maturity-20261014/
首先读取 HERMES_ECO_CURRENT_20261015.json、F009_API_ADMISSION_VIRTUAL_FREEZE_20261015.md；其余从以下报告按需读取：F004_HTTP400_DIAGNOSTIC_FREEZE_20261015.md、F005_REALITY_PROGRESS_20261015.md、F006_CONTINUITY_REALITY_20261015.md、F007_VISION_REALITY_20261015.md、F008_DELEGATION_REALITY_20261015.md。
正式Hermes技能：C:/Users/A/.hermes/skills/hermes-mature-supertool/SKILL.md v2.0。

已经完整真实证明的局部：正式CLI DeepSeek模型真实回复(exit0/38.73s进程runtime)；CLI依据只给路径读取隐藏文件并回传准确值(exit0/29.52s)；原有连续性脚本新进程checkpoint→handoff→resume→closeout CLOSED_PASS；F007合成图片识别完全正确(exit0/56.38s，尚缺独立vision_analyze tool.completed证据)；F008原生delegate_task两独立孩子分工/完成，manifest deleg_e6411f32 独立回读两项completed，代码FAIL+测试覆盖PASS，父CLI exit0/74.95s。
注意所有任务负载不等价，禁止拿这些秒数互相计算提速。
F002原始 HTTP400根因高置信：PowerShell把 input 字符串包装成PSCustomObject含PSPath，F004隔离修复后10/10 JSON合同离线过；**旧F002请求仍无ack/run id/grade，不重新派发**。F009当前无凭据 GET /v1/capabilities HTTP401，符合官方Bearer鉴权，证明保护启用、不能证明合法Runs API成功。先前使用启动器提取授权headers的远程命令被平台安全拦截：不能绕过、改通道、读取.env/密钥。
F005真实Repair业务测试未完成；原cmd/unittest入口被引号与NativeCommandError困扰，后来同类脚本操作被安全拦截，不能通过改执行通道绕过；已冻结现有fixture。不要冒称Child A发现BUG就是Repair真实回归通过。
NEXT_ONLY：H-ECO-01 用**已有合法受信、可获准的Hermes API客户端**对账旧结果并按F009 frozen contract对新隔离任务做一次Runs admission；如果无获准权限保持BLOCKED，不打新POST。仅此过后再继续F005 Repair独立真实测试/修复/同项回归、Hermes网页聊天/多模态/模型路由/Gateway恢复与冷启动、固定合同连续5轮和7-14天成熟观察期。
安全边界：不改FlClash/系统代理、凭据、Windows ACL、Docker卷、已登录浏览器，不重装、不启动旧Watchdog，不干涉其他任务，不为凑分重复简单测试。原有PASS逐项继承，未知保持UNKNOWN，现实失败保留。GOOD/BAD/FIRST_DELTA→成熟官方机制→虚拟成熟→Freeze→一次合法Reality→外部接受/回虚Repair；T_VALID必须按相同质量、同合同、完整端到端墙钟计算。
