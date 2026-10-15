# F021｜跨Hermes新进程的冻结成果接续与SHA证明｜Reality前冻结
日期2026-10-16｜TASK HERMES-ECO-20261014｜承接动态 CURRENT=HERMES-ECO-F020-20261016｜状态VIRTUAL_MATURE_FROZEN
路由：《三人行》V2仅Hermes项目，本机Windows桥V7 C优先/B备用/A暂停。继续使用正式CLI/原OpenRouter deepseek/deepseek-v4.1-flash，不重新部署、不修改服务/网络/凭据/浏览器。
## 现实缺口与成熟路线
历史F006只验证了独立任务脚本的checkpoint/handoff/new process，并非Hermes真实模型在新原生会话从上个冻结状态接续。F019真实Repair外部Gate23/23 PASS；F020真实双子生命周期PASS但整体审查UNKNOWN；新任务不应重复他们。FIRST_DELTA是任务交接证据至真实模型新会话的完整信任链仍无直接实证。
成熟方案：Hermes原生正式一次性CLI新进程＋C盘独立不可变JSON交接文件＋独立SHA256与外部schema Gate；不自研session后端，不重启Hermes Gateway，不读取私人Session数据库，不假装进程重启就是持久原生会话恢复。
## 不变量及DONE_WHEN
外部先新建隔离 F021_RESUME 目录（在当前Hermes母技能evidence之下）与 handoff.json，明确{task_id,prior_freeze,completed_f019,pending_f020,required_files}，并保存 SHA256；F019退款算法、需求、测试与独立Gate文件全部已有合法冻结，输入只读。
然后只在现有正式CLI调用**一个全新Hermes模型会话进程**，命令行中只给handoff路径，不在提示词中透露其验收用的隐藏随机标记/此前F019源码哈希。模型必须真实读取 handoff.json 与 prior F019 repair_state.json、f019-independent-gate.json、refunds.py 并计算哈希，生成唯一F021_RESUME/resume_ack.json，准确区分已完成F019与尚未完成F020，只能对新的resume_ack文件写入。不得修改原source、配置或F019/F020状态。
独立GPT通过C读取/程序验证输出：handoff源SHA不变、动态JSON字段正确、回填的F019来源SHA与现场一致、F019 23/23 PASS和F020 UNKNOWN准确转移、写入产物的非复用真实随机标记必须与handoff值相同、原F019实现/测试SHA不变。仅在外部全部成立时宣称SCOPED_HANDOFF_FRESH_CLI_PROCESS_PASS。
用Hermes原生usage文件的session_id与F019 usage.session_id做仅本机相等性比较，不打印私人会话ID；如相等或缺失则NEW_SESSION_UNVERIFIED，不伪造。
本任务不测试Windows重启、Hermes原生历史会话恢复、OpenWebUI UI会话，也不完整认证整站五轮；整个wall-clock含模型进程、远程传输、独立Gate成本，若无全程表计不冒充精确T_VALID或物理极限。
攻击树：既有CLI/只读证据/JSON＋SHA Gate=KEEP候选；构建新持久会话数据库/替换旧F006=ABANDONED；GUI/音视频/F002 UNKNOWN=NOT_APPLICABLE。
