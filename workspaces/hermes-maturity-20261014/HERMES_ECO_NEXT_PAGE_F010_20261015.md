# Hermes生态站｜F010直接CLI实际修复成功后的唯一接续
任务HERMES-ECO-20261014；Freeze HERMES-ECO-F010-20261015。
指定总方法：《三人行》第2版（仅Hermes项目显式使用），《GPT直连Windows双路执行桥 V6.0》C>A>B，原Hermes专用 v2.0 不升级不重装。
唯一在线状态：cuiqinggang/codex-private-skills/workspaces/hermes-maturity-20261014/HERMES_ECO_CURRENT_20261015.json。
重要路线修正：过去把自写F002 /v1/runs API验收脚本的HTTP400及读取Bearer认证头被工具阻断，误当成Hermes正常业务成熟化总阻塞。这是验证器独立接口合同问题，非Hermes本体执行障碍。以后优先已经真实运行成功的正式CLI或原有Open WebUI：不用新建API客户端、不读或导出凭据。Runs API仍是独立自动化验收项、旧UNKNOWN不重投。
已通过的真实局部（按前次冻结继承）：CLI模型答标记、CLI读取隐藏本机文件、F006原任务级checkpoint-handoff-resume-closeout、F007图片识别结果正确但工具事件仍未知、F008原生双子代理manifest证实2孩子completed。验收等级不扩大。
本轮F010新的成功：已通过 C通道直接调用原正式CLI ltmvh-hermes-formal.ps1（OpenRouter DeepSeek-V4.1-Flash），在F005_REPAIR隔离目录内修复 invoice.py，Hermes报告修前8项测试失败、修后8项通过；进程退出0、runtime 52.87s。GPT独立重读修复文件、运行现成Python unittest，8/8全部PASS、退出0、进程runtime0.72s。requirements.md、test_invoice.py、run-tests.cmd和原F002/R01/invoice.py SHA均与原冻结保持相同。确实修复了只算paid、int非bool、ValueError规则。原run-tests.cmd（先前安全拦截项）没有运行，也没有绕过。Hermes报告 skill_view 无法找到 hermes-repair-loop-adapter；本轮成功来自CLI原生能力，不可冒充专项skill已加载。
原OpenWebUI http://127.0.0.1:3000/health 当前HTTP200，Chrome进程存在，尚无可核证的GUI实际聊天消息回执；不能把健康200写成实际网页成功。接下来首选F011：如可用获准的当前浏览器交互工具，则在已打开WebUI直接发布一项最小合成任务，独立核验模型回复/工具调用与网页UI；若未授权/没有GUI工具，不另开第二浏览器、不用命令绕过其他安全检查，而是继续使用原CLI验证其他尚缺能力。
全站目标仍未完成：OpenWebUI实际聊天；模型/Provider真实切换与质量；视频/音频实际任务；Hermes会话级恢复、冷开机/热恢复和耐久；明确合同连续5次端到端实测与完整T_VALID；F002原Runs API专用自动化验收。整站FINAL_VALID=NO，综合5轮0/5，不降低质量门。
继续：GOOD vs BAD/FIRST_DELTA→成熟官方机制→虚拟成熟→Freeze→一次合法Reality→独立验收→保留原失败→必要时回虚修复。不触碰FlClash、代理、密钥、Windows权限、其它容器和已有登录浏览器，不重装、不重造系统。