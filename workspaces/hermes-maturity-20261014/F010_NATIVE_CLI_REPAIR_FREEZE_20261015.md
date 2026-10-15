# Hermes F010｜直接调用正式 CLI 修复现有隔离业务任务（虚拟成熟冻结）
日期：2026-10-15；TASK_ID=HERMES-ECO-20261014；NODE=F010_NATIVE_CLI_REPAIR
方法：《三人行》V2（本项目用户明确指定）→ 已有Hermes专用v2.0/Repair Loop → V6桥 C>A>B。
状态：VIRTUAL_MATURE_FROZEN，Reality一轮；不修改 F002/历史冻结、模型、代理、密钥、浏览器、Docker。
本节点是用户明确选择的“直接把任务交给爱马仕执行”的路径，不以自写的HTTP /v1/runs验收客户端作为前置条件。
本机已确认 Open WebUI http://127.0.0.1:3000/health 返回200，Chrome进程存在。服务健康≠网页已登录或已经发布任务。
当前正式CLI（此前已实际多次跑通）：
C:/Users/A/AppData/Local/hermes/bin/ltmvh-hermes-formal.ps1
Hermes 真实 provider/model=openrouter/deepseek-v4.1-flash，固定原业务输入。
仅在已有 F005_REPAIR 隔离目录内执行：
C:/Users/A/.hermes/skills/hermes-mature-supertool/evidence/HERMES-ECO-20261014/F005_REPAIR/
输入三文件：requirements.md，invoice.py（目前原始缺陷为对所有rows无条件求和），test_invoice.py（原始真实测试不修改）；另有 run-tests.cmd，但上一轮此脚本由远程任意命令执行被安全检查阻断，不能通过借另一路工具隐蔽重放同一被拦的命令。
目标：Hermes使用自己成熟原生 file/terminal/Repair 能力，读取现有需求与源代码，局限于 invoice.py 的最小修复；遵守工具批准和安全检查；能合法执行官方Python unittest时跑一次前后同项完整测试，否则诚实报告无法实际验证。原始 F002 不修改。用户明确授权本任务正常的Hermes执行过程，不授权绕过工具安全拦截。
要求产物：Hermes原生响应、旧源与修复差分、对原需求与测试文件SHA256原样保持的独立审查、真实unittest失败/成功记录（如允许），完整进程退出/时间；独立测试未执行时不可写完整 Repair PASS。
停止：若Hermes本机任务等待批准、运行中不明或安全拒绝，则停止，不自动再派，不以另一路通道绕过。若成功只记该节点真实PASS，既有F002 HTTP400仍独立待修，整站0/5/FINAL_VALID=NO。
