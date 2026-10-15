# Hermes 成熟态 AI 生态站｜F006 下一节点接续
任务：HERMES-ECO-20261014；当前冻结：HERMES-ECO-F006-20261015。
**本任务使用《三人行》第2版与《GPT直连Windows双路执行桥 V6.0》：C 通道优先，A 第二、B 第三；旧 F003 文档的 V5/A 优先已失效。** Windows 当前C设备 f6990966-5870-484b-bf79-409bc6fb963e 可用；连接时应重新检查在线。
方法不改变《三人行》V2全局仍待审查的状态；用户只为本Hermes项目显式指定。Hermes专用 v2.0 及已装真实入口原样继承。

首先读权威资料（仓库 cuiqinggang/codex-private-skills）：
1. workspaces/hermes-maturity-20261014/HERMES_ECO_CURRENT_20261015.json（LATEST）
2. workspaces/hermes-maturity-20261014/F004_HTTP400_DIAGNOSTIC_FREEZE_20261015.md
3. workspaces/hermes-maturity-20261014/F005_REALITY_PROGRESS_20261015.md
4. workspaces/hermes-maturity-20261014/F006_CONTINUITY_REALITY_20261015.md
5. workspaces/hermes-maturity-20261014/F005_REPAIR_NODE_FREEZE_20261015.md
原始 Hermes v2.0技能 C:/Users/A/.hermes/skills/hermes-mature-supertool/SKILL.md。
最新事实：
- 原 F002 R01 HTTP400：JSON请求 input 实际被 PowerShell序列化为对象包含PSPath；Hermes官方 POST /v1/runs 要字符串。本机原脚本SHA不变；F004独立补丁候选和10/10请求离线检查PASS，GitHub回读已验证。**没有重新 POST，也没有原失败run_id，因此0/5, FINAL_VALID=NO**。
- C通道本轮真实 8642/health、3000/health 返回200；CLI v0.21.5+6841。
- 正式Hermes CLI (DeepSeek V4.1 Flash)真实marker回传PASS 38.73s进程runtime；真实读取独立隐藏校验值PASS 29.52s进程runtime。两种负载不等价，不能宣称提速。没有正式T*。
- 原 Hermes 专项连续性脚本本轮真实创建2步任务，checkpoint-1，handoff，独立新进程resume得到 next_step=2/do_not_repeat=[1]，checkpoint-2和close-task，回读 CLOSED_PASS/hash；**仅任务级脚本真实通过**，不是 Gateway重启或模型会话恢复。
- F005_REPAIR 隔离目录已复制原 F002/R01 的 4个固定fixture且源哈希校对；PowerShell初次预期stderr处理失败、cmd /c 引号解析错误，测试没有进入真实 unittest 用例。直接运行 .cmd 被平台安全检查拦截；不得换工具或通道绕过该安全拒绝。Hermes尚未获派该 Repair 任务，不能声称Repair PASS。独立报告已保存。
**唯一优先下一节点 H-ECO-01：** 先安全对账 F002 原始 HTTP400/ack缺失、确认不存在未完成副作用；使用获准的现成认证客户端/官方允许机制，预先冻结新隔离目录、新请求及唯一合法幂等key，仅做一次新API admission真实验证，必须有run_id、status、响应内容和完整时间；任何权限拒绝就BLOCKED，不绕过、不读取秘钥。不直接发送F002旧请求，不擅自重开五轮。
随后按本项目已冻结的独立 Gate 继续：H-ECO-02 Repair 独立业务 unittest真实FAIL→Hermes最小修复→真实PASS+独立Gate；原生双子代理真实回执；H-ECO-03 视觉/视频/音频、Hermes会话级handoff；H-ECO-04浏览器真实对话、冷启动、恢复、性能对照、同合同连续5轮、7~14天观察期。
标准：GOOD/BAD/FIRST_DELTA→成熟机制→虚拟成熟→Freeze→一次授权 Reality→有效验收；无证据不要评分/记PASS。不得修改FlClash、Windows代理、密钥、权限、其它Docker/浏览器任务；不删除或重装、不开旧Watchdog。只有实际验证完成才更新状态机，所有报告放到 workspaces/hermes-maturity-20261014/ 并回读。
