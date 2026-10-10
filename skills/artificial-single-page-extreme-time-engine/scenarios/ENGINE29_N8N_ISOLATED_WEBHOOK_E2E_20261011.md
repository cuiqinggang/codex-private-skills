# ENGINE29 n8n 原生Webhook最小闭环｜2026-10-11 实测
MODE=WINDOWS_DCR_V032_N8N_ISOLATED
STATUS=MINIMAL_E2E_PASS
ORIGINAL_F002_FINAL_VALID=NO
TASK_CONTRACT=tasks/N8N_MCP_SHARED_20261009/CURRENT_TASK_CONSTRAINTS_V1.md
TASK_FREEZE=tasks/N8N_MCP_SHARED_20261009/freezes/CURRENT_TASK_FREEZE_V2.md
ENGINE=28
BRAIN=25
TEMPLATE=18

## 真实环境与隔离
Windows DESKTOP-4A1EGTM 经 Desktop Commander Remote 0.2.52 执行；原常驻容器 n8n-local 为Up/healthy，共有7个既存工作流，本次均未改写。读取既有n8nNativeE2E01发现其会调用Reasonix 8788，故不盲用。另以同一n8nio/n8n:stable镜像创建一次性容器engine29-n8n-isolated，宿主仅绑定127.0.0.1:15678，测试结果取回后已docker rm -f清理，原n8n-local健康仍PASS。

## 实测节点
独立工作流 E29N8NISOLATED01：POST /webhook/engine29-e2e-isolated → Code验证taskId和输入 → 计算 7*3 → Respond to Webhook 返回JSON。所有节点均为独立测试，不调用本机Reasonix、无ChatGPT自动消息发送和浏览器业务副作用。

## 实际运行回执
首次HTTP请求返回404，日志显示webhook尚未注册，随后n8n启动日志显示1 published workflow及Activated workflow；在确认其注册以后重新用相同只读/纯计算测试任务调用：
HTTP 200
```json
{"taskId":"E29-TEST-001","input":7,"output":21,"validated":true,"stage":"FINAL_VALID"}
```
负例：taskId=WRONG-TASK，得到HTTP 500 {"message":"Error in workflow"}，属于合同校验拒绝，不是有效业务回执。
生产n8n-local后续再查Up/healthy。
测试源：C:\Users\A\Documents\Codex\ENGINE29_STATE_CANDIDATES\n8n_isolated_webhook.json
负例脚本：C:\Users\A\Documents\Codex\ENGINE29_STATE_CANDIDATES\n8n_webhook_negative.py

## 边界
这个FINAL_VALID只属于纯计算最小测试合同，不能表示N8N-MCP-SHARED-F002全部通过，不证明ChatGPT网页CEO真实换页、跨客户端同资源冲突仲裁、不同目标实际并发、UNKNOWN对账、完整生产业务T_VALID。F002原合同及冻结保持不变。原ENGINE29_UNIFIED任务存在独立合同/F001，不能将其与F002混写。
