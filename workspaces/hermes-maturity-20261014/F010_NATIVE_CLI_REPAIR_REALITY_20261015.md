# Hermes F010｜正式 CLI 直接修复，独立单测验收

日期：2026-10-15。任务：HERMES-ECO-20261014。冻结前置：F010_NATIVE_CLI_REPAIR_FREEZE_20261015.md。
方法：《三人行》V2 本项目显式使用；桥 V6.0：C>A>B；Hermes 专用 v2.0；原正式 CLI 和原 Provider/Model。
状态：F010_SCOPED_RUNTIME_PASS；原 F002 整站综合五轮仍 0/5；FINAL_VALID=NO。

## 路线纠正
F002 的 /v1/runs HTTP 400 是自写验收客户端将 input 字符串误序列化为含 PSPath 的对象，不代表 Hermes 自身业务能力不可用。Hermes 官方 -z oneshot CLI 可以直接执行真实任务，无需外部新建 Runs API 客户端。Open WebUI 3000/health 当前返回200，Chrome进程存在，但未验证 GUI 登录及聊天。

## F010 实际执行
通过 C 通道调用原有 C:/Users/A/AppData/Local/hermes/bin/ltmvh-hermes-formal.ps1，Provider=openrouter、Model=deepseek/deepseek-v4.1-flash。
唯一可写目录 C:/Users/A/.hermes/skills/hermes-mature-supertool/evidence/HERMES-ECO-20261014/F005_REPAIR/，只允许修改 invoice.py，禁止改 requirements.md、test_invoice.py、run-tests.cmd，禁止凭据/代理/浏览器/服务变更。
Hermes 正式进程 PID=53760，成功结束 exit 0，完整该进程 runtime 52.87 s，一次自然任务无盲目重派。
Hermes 报告前置 Python unittest 实际8项失败，exit1；随后修复 invoice.py：只累计 status 正好为 paid 且 cents 是 int 而非 bool 的金额，缺失/非法 cents 抛 ValueError；负数和任意大整数允许，空输入0；最后同项 Python unittest 8项通过exit0。前置测试的退出与统计由 Hermes 本轮回执提供，未取得独立保存的测试前事件流。
Hermes 本轮提示 skill_view 无法找到 hermes-repair-loop-adapter，因此实际完成依赖正式CLI现有能力，不可宣称模型本轮已经成功加载该技能。

## 外部独立验收
GPT 在同一设备重新读取修复后 invoice.py 源码，并独立以现有 venv Python（不是被安全检查拦截的 .cmd）直接执行 python -m unittest discover -s <F005_REPAIR> -p test_invoice.py -v。
真实观察八项全部 ok，Ran 8 tests in 0.001s，OK；独立进程 exit0，runtime0.72s。测试框架的0.001s不是任务墙钟。
SHA256 ：
F005_REPAIR/invoice.py 新=BC5CFB8515D7FBF3F158F310FA6C2970E2BCBCBC82E8FB74928C07809A9F3967。
F005_REPAIR/test_invoice.py=E824203E6987D79697869C90C1B645BCD6898B216038B7023A7A1A31CF478FB9（原始不变）。
F005_REPAIR/requirements.md=FC2A5F9E9C4C97CBAEFF10E06E919BBD46DAFC484838F07BB9223159AD25D8F3（原始不变）。
F005_REPAIR/run-tests.cmd=776771515BE2989D9A4A880D51C48E70168E45764364D6D31FA3FE6A2860FED9（原始不变，未执行）。
F002/R01/invoice.py=38F6E302C0F8C40A038DA9BC12722131E412861CBDDD05B1BDFC7A3B1E1E69DC（旧失败证据完整不变）。

## 结论与边界
本轮真正证明原 Hermes CLI 能自主做最小代码Repair，并由GPT独立执行8/8单元测试验证。原F002/Runs API、网页实际聊天、音视频、多模型、长期耐久、真实全五轮仍未验收。不把52.87s跟不同负载样本比较提速。
下一节点优先现有Open WebUI GUI实际聊天与原CLI业务能力成熟化；将原F002 Runs API当成独立外部自动化接口合同，不能阻断正常Hermes业务。不开第二浏览器，不拿健康200充当WebUI端到端。