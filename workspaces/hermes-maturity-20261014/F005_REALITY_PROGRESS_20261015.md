# Hermes AI 生态站｜F005 当前现实结果与 Repair 验证阻塞
时间：2026-10-15；项目：HERMES-ECO-20261014
METHOD：《三人行》V2（此项目明示采用） / Windows 执行桥V6.0 C>A>B / Hermes专用技能v2.0
上一冻结：HERMES-ECO-F004-20261015；F005 Repair 虚拟合同：F005_REPAIR_NODE_FREEZE_20261015.md。
**状态：当前模型/文件工具两项现实PASS；F005 Repair现实未通过、待正确的受信执行入口；整站 FINAL_VALID=NO；F002五轮仍0/5。**

## 1. 本轮真实生产路径限定结果（2026-10-15）
已授权的 C 通道设备 DESKTOP-4A1EGTM 在线，实际运行 PowerShell 读取 Hermes CLI 版本：
Hermes Agent v0.21.5+6841.g8b66a51 (2026.9.24) · upstream 8b66a510；没有因此升级或重装。
本机无鉴权健康请求：127.0.0.1:8642/health HTTP200；127.0.0.1:3000/health HTTP200。只证明服务可达。
Hermes 正式 CLI `C:/Users/A/AppData/Local/hermes/bin/ltmvh-hermes-formal.ps1` 原样继承：
- 真实模型 marker smoke，输出精确 `HERMES_F004_CLI_OK`，退出码0；远程终端报告进程runtime=38.73s。
- 独立本机原生 read_file 测试：先用 C 通道写入 `C:/Users/A/.hermes/skills/hermes-mature-supertool/evidence/HERMES-ECO-20261014/F004_CANDIDATE/F005-read-fixture.txt`，其中内容含未给模型的 `TRACE_TOKEN=ECO_READ_PROBE_20261015_C7D2F1A9B4E68C03`；随后只把文件路径交给正式CLI，并明确要求真实读取。模型准确返回 `ECO_READ_PROBE_20261015_C7D2F1A9B4E68C03`，退出码0，runtime=29.52s。此项构成文件信息取回的真实闭环强证据；本轮没有保存工具原生事件轨迹，不能单凭终端回答断言某个特定内部工具调用细节。
以上时间均是远程执行工具的进程runtime，不含全部任务接续/冻结、审查开销，不作为整站 T_VALID、正式冷暖 T* 或提速比例。两项负载不同，不做速度A/B对比。

## 2. F005 Repair 最小现实阶段
按 F005 虚拟成熟合同，在 `C:/Users/A/.hermes/skills/hermes-mature-supertool/evidence/HERMES-ECO-20261014/F005_REPAIR/` 新建隔离副本，复制原 F002/R01 的 invoice.py、test_invoice.py、requirements.md、run-tests.cmd，复制后逐文件 SHA256 相等。未改原F002。
发票既有 fixture 中 `total_paid_cents` 使用 `sum(row["cents"] for row in rows)`；按要求应只计 `status == 'paid'`、必须为非 bool 整数、非法输入ValueError。静态差异明显，但必须真实执行同项 unittest 才能标记业务基线FAIL。
首次 PowerShell 控制器对预期错误的 unittest stderr 使用 ErrorActionPreference=Stop，出现 NativeCommandError，生成的可观察 runner 失败退出码1；未形成有效业务测试回执。
第二次尝试通过 cmd /c 包裹现有 run-tests.cmd，得到 `ImportError: Start directory is not importable`；stderr 显示测试发现参数被带入了目录字符串，表明这次是 Windows cmd 引号/命令调用合同问题，而不是 invoice.py 业务断言已失败。
随后拟通过 PowerShell 直接调用现有 .cmd 文件修正入口，工具调用被平台安全检查屏蔽。**停止进一步远程执行同等命令，不绕过安全检查。**
因此：当前 F005 baseline 未验证业务 FAIL；Hermes 尚未获派代码修复任务；外部 unittest AFTER 未执行；真实 Repair Loop=NOT_PASSED/EXECUTION_BLOCKED；不得用静态推理冒充 Repair 运行通过。
保留 F005 虚拟方法与隔离文件，避免后续重新复制或重置。

## 3. F002 / Runs API
官方：https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server/
POST /v1/runs 接受简单 input 字符串，原 F002 R01/request-1.json 实际 input 为 PSCustomObject（含PSPath等）；本机离线对照加 [string] 后输入回到字符串，F004隔离补丁 Parser5.1 PASS、原10段固定prompt 10/10 JSON 合同PASS，旧源 SHA未变。
本轮从授权 HTTP 接口取实时详细信息的远程脚本被安全检查拦截。不能绕过查阅密钥/隐私文件；没有重新POST原请求，不可虚报API admission完成。F002 既有 HTTP400 112ms依然为原始FAIL；ack/run/grade仍无，状态0/5。

## 4. 后续优先级与停止规则
- H-ECO-01：F004 JSON合同修复候选已完成离线验证；先用正式允许的受信 API 客户端或人工批准的既有入口取得一次合法新的 isolated admission 回执（run_id + 终态）；不得绕过当前平台安全阻止的动作或读取凭据，不重发未知F002。
- H-ECO-02：保留 F005_REPAIR 原四文件和错误回执，解决Windows脚本调用格式，并通过正式允许的运行途径做基线真实 unittest；成功见到业务测试失败后才一次性调用 Hermes 的成熟 Repair 机制，独立同项复验。无法执行则阻断该节点，不造PASS。
- H-ECO-03：视觉、视频、音频、跨新会话 checkpoint/handoff/resume，依靠各自现有技能的独立实际回执。
- H-ECO-04：Open WebUI实际前后端交互、开机冷启、长时观察、五轮一致合同和完整时间性能。
任何失败回到 FIRST_DELTA / GOOD vs BAD / 最小合法修复 / Freeze / Reality；无有效新现实证据不改变 Gate。
依照原SOP，若需7-14天的持续成熟认证，不能用单次当前会话冒充观察期结束。旧8月注册表成功仅历史限定，不复制为本阶段通过。
