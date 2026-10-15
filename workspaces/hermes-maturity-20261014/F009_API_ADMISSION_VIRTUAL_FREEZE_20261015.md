# Hermes F009｜API真实准入门：第一性原理差分与冻结
TASK_ID=HERMES-ECO-20261014 | DATE=2026-10-15
METHOD=《三人行》V2（用户仅为Hermes项目指定） + V6桥C→A→B + Hermes原有v2.0专项
FREEZE=HERMES-ECO-F009-20261015 | STATUS=VIRTUAL_MATURE_FROZEN_REALITY_DEPENDENCY_PENDING
Whole_station_FINAL_VALID=NO | 5 consecutive real integrated rounds=0/5

## 目标仅一个
针对已发生 F002 R01 原始POST /v1/runs WebException HTTP400/112ms，完成**旧请求对账、最小合法修复、独立新隔离合同下单次真实准入**；不重装、不改模型、不动代理、不重复派发未知运行。

## GOOD / BAD / FIRST_DELTA
GOOD：2026-10-15 当前Hermes正式CLI DeepSeek V4.1 Flash真实答标记EXIT0、真实读隐藏文件EXIT0；Hermes和OpenWebUI/health此前分别HTTP200；Hermes原生双子代理F008系统manifest两项completed，原生任务级恢复F006真实closed_PASS。
BAD：F002/R01/request-1.json input 被Windows PowerShell对象扩展成含value/PSPath/PSDrive/ReadCount的PSCUSTOMOBJECT，违反官方POST /v1/runs input simple string。该请求当时HTTP400，response-body未保存、无ack/run_id，保留UNKNOWN_RECONCILE_FIRST、不自动重投。
FIRST_DELTA：序列化错误先于模型/工具/Agent运行，是最早责任层。不为此重装Hermes、容器或修改Provider。F004隔离补丁在Get-Content结果显式 [string]、请求JSON非空字符串断言，PowerShell5.1 Parser PASS，既有R01-R05两阶段共10段prompt输入 schema 10/10 PASS，原正式F002脚本SHA保持不变。

## 本轮安全只读HTTP补充
同一Windows C通道对 http://127.0.0.1:8642/v1/capabilities 做**不含凭据、仅GET**的请求，真实得到 HTTP_STATUS=401，进程退出码0/runtime约1.09s。官方Hermes API Server文档指定该接口使用bearer认证（https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server）；401符合受保护接口行为，不是服务宕机，也不能证明任何有鉴权的runs接口成功。
此前通过启动器Get-ApiServerHeaders取得本机授权header的远程执行被平台安全检查拦截。不得尝试绕过、换工具/路由、导出/查看.env/API key或降低认证；此节点当前依赖受信且已获准的官方授权入口，该权限不能从401推断出已有。

## 成熟候选（不造新架构）
1. 最优：已获准的现成Hermes API客户端或现役OpenWebUI内部正式认证入口；它应在设备内以现成授权机制发送合法请求，密钥不进入对话/仓库/工具输出。仅当能够独立确认且使用合法时可作新隔离POST。
2. Open WebUI现有登录网页客户端可验证聊天E2E，但聊天完成不等于原生Runs API已通过；分别报告。
3. 未获准时：只冻结离线补丁、合约测试和当前401证据；停止这个门，不切换执行桥逃避安全限制。
选择停止门：没有可合法访问的认证执行入口，状态 DEPENDENCY_PENDING，不自动派发。C通道在线不等于被授权读取私有凭据。

## Reality协议（仅在依赖成立后）
- 原 F002 request/round-result/LAUNCH/REALITY 不写回不覆盖；先只读验证有没有旧ack/run/业务副作用，UNKNOWN保持未知。
- 新隔离F009或更高新合同目录，新幂等键；冻结请求输入严格字符串、目标model合法别名，source/config/fixture SHA，受信鉴权方式及回滚界限。
- 仅一次 POST /v1/runs；必须获得HTTP状态、原始脱敏错误正文或run_id、GET run状态、终止状态、实际provider/model、总wall、失败证据。授权或安全门失败时立即 STOP，不重试/不改代理。
- 成功只闭合API admission单项，随后回本合同Repair/双子代理/视觉/新会话/完整五轮，不能直接提升整站FINAL_VALID。

## 本次其他子节点可继承
F007 CLI图片识别正确蓝矩形/红圆/绿三角，exit0/runtime56.38s；但无vision_analyze原生完成事件，不把tool_id写成PASS。
F008原生delegate_task批量两子任务，父CLI退出0/runtime74.95s，系统manifest deleg_e6411f32记录 task-0和task-1均completed，审查内容与原代码/测试正确；不等于Repair修复PASS。
F005原Windows批处理用例未真正进入unittest断言，随后同类执行被安全检查拦截；保留BLOCKED，不换路绕过。
同一任务不同负载运行时不能计算提速，历史单样本4.853s warm候选不是正式T*。成熟度观察期7–14天无法靠本次页面立即认证。
