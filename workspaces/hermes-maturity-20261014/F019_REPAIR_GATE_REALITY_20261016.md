# F019｜Hermes Repair Loop 故障注入＋同项独立Gate Reality
日期：2026-10-16；TASK HERMES-ECO-20261014；节点 F019；承接冻结 HERMES-ECO-F018-20261016。
前置虚冻结：F019_REPAIR_GATE_VIRTUAL_FREEZE_20261016.md，GitHub commit 63e44e4b66007017d346f4ba4a522525e9862131。
Windows V7：只使用C=Remote_Desktop_Commander；B无需接入；A=PAUSED_BY_USER未触碰。Hermes原有正式CLI wrapper、Provider=openrouter、Model=deepseek/deepseek-v4.1-flash。未重装、更改代理、运行API旧请求或操作浏览器。

## 固定合同与原始BAD
新合成夹具路径（用户本机，不上传业务/敏感正文）：
C:/Users/A/.hermes/skills/hermes-mature-supertool/evidence/HERMES-ECO-20261014/F019_REPAIR/
requirements.md、refunds.py（预置故障）、test_refunds.py组成独立合同（不同于已完成的F005发票案例）。符合的函数对settled/refund严格筛选、金额/ID类型校验、重复冲突拒绝、去重、纯函数和任意大整数。固定 unittest 23例。
源哈希：requirements.md=CD8E65EBEF9FEB323B365378048480AFD304A25C6E01452AB7671039080979F8；
test_refunds.py=B3B5413EF57677B82A776318EA3F6B5C56C21432E0D4B3322A518FE0E9A17E5B；
refunds.py BEFORE=C70F97C7735BEB35616D0F200B62E5F2A3534572CC72CF632AC6123B31A1449B。
Windows Python baseline通过官方 PowerShell Start-Process 标准错误隔离执行，exit1，Ran 23 tests, FAILED (failures=14, errors=3)，独立预检进程约1073ms。首次尝试捕获stderr的PS5.1管道被NativeCommandError终止，不误记为业务测试；未修改夹具，改为成熟Start-Process重现相同失败。

## 一次真实模型Repair
实际 C start_process 正式 CLI PID49676，仅运行一次自然模型任务，Hermes exit0、模型CLI墙钟158718ms，外层远程工具runtime159.35s。没有盲重派。
Hermes返回F019_REPAIR_CLI_TASK_DONE，报告原生 skill_view(hermes-repair-loop-adapter) SUCCESS、技能v2.0可用；本节点外部未单独读取其原生tool.completed事件，仅证实模型本轮报告及此前F018单独原生可用性。因此精确记为 SKILL_VIEW_SELF_REPORT_SUCCESS/INDEPENDENT_TOOL_EVENT_UNVERIFIED，不能夸大原生联动的可审计性。
Hermes模型报告已真实在终端重现原23例的14F/3E，FIRST_DELTA=缺kind/status过滤，并补足输入类型/字段校验/同ID去重。仅修 refunds.py；创建 repair_state.json，round1、status=RESOLVED、regression_result=PASS，未超过3轮。
CLI usage（本次隔离输出，不含密钥）：api_calls=7；input_tokens=37832, output_tokens=3638, cache_read_tokens=143488, total_tokens=184958（含cache read，不是全部新增输入）；估计费用USD0.0042113664，属估算非账单；模型是原OpenRouter DeepSeek V4.1 Flash。

## 外部独立 FINAL_VALID（限定范围）
GPT通过C独立启动原Windows Python的 unittest discover，exit0，Ran 23 tests, OK，外部测试进程墙钟1079ms。
实施后 refunds.py SHA256=E796F499E5F9B222AAABF89F09AB5CD434BA6C7224F568F4582B20B3D860C243（与故障源不同）；requirements.md和test_refunds.py哈希与前值逐字一致。生成 f019-independent-gate.json 证据，gate_pass=true、repair_state_exists=true。旧 F002、F005、F018文件未授权修改；本轮仅更新独立 F019 夹具与同目录输出。
原Hermes v2.0静态检查器经 F019 后再次实测18/18 PASS，FAIL=0；未放宽规则。
当前可冻结的精确结论：F019_BOUNDED_REPAIR_FUNCTIONAL_GATE_PASS（预置错误真实复现→模型一次Repair→外部同项23/23与SHA Gate通过）。**原生skill_view执行事件尚未被独立提取，自动Repair触发机制未单独证明；不能因此宣称整站Repair自动闭环全部成熟。**

## T_VALID与停止
本轮模型自然任务CLI真实158.718s、外部独立Gate1.079s、baseline重现1.073s，尚不含GPT派发/远程C传输/报告存档的全墙钟。因此完整TASK_ACCEPTED→FINAL_VALID未知，不能仅相加认定全T_VALID，更不能用F005/F017等不同合同秒数宣称提速或物理极限。
本任务第一轮通过，重复同一夹具5轮没有必要，停止。不修改已有成功代码；后续优先F020对修后同项做独立原生delegate_task Gate / 子任务证据或选择其他实质缺口。
整站FINAL_VALID仍NO，独立综合5轮=0/5，F002原未知Runs请求不得重放，GUI、多模态、跨重启、长稳仍PENDING。
