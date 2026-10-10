# ENGINE29 GPT直连与n8n路径初级对照｜现场准备度证据
DATE=2026-10-10
MODE=A_GPT_DCR_VS_B_GPT_N8N
STATUS=CONNECTION_RECON_ONLY
SAME_TASK_BOTH_VALID=NO
WINNER=UNKNOWN
FULL_T_VALID=UNKNOWN

## 同任务拟定合同
同一现有浏览器、相同授权、同一个只读任务（读取已有Chrome CDP版本信息并返回浏览器版本与可复核回执），分别比较：
A 当前GPT CEO→DCR v0.3.1→Windows现有浏览器；B 当前GPT CEO→已有n8n工作流→同一浏览器。
必须有两端同一输出及从任务接受至有效结果的完整时间，计入调度、等待、异常恢复、审核；不可仅比较HTTP单次响应。

## 本轮实时事实
- Desktop Commander Remote v0.3.1 主设备 f6990966-5870-484b-bf79-409bc6fb963e 在线。
- Windows本机端口127.0.0.1:5678监听，n8n /healthz返回HTTP200，单次149ms；/rest/workflows返回HTTP401，当前请求未认证，不能由此推断工作流不存在。
- Windows 127.0.0.1:9223 Chrome CDP /json/version返回HTTP200，首次检查28ms；另一批次三次真实只读访问返回Chrome/151.0.7922.34，分别176ms、1ms、0ms；对应远端PowerShell进程总体耗时531ms。首次调用可能包含初始化/缓存成本，且毫秒计时取整，0ms不表示零成本。
- A已真实从Windows读取CDP元数据3/3有效；B只有n8n健康可用证据，没有已授权工作流触发与回执，因此B业务VALID=UNKNOWN。
- 上述n8n /healthz与Chrome /json/version不是相同业务任务；禁止用149ms vs 28ms定胜负。
- 本轮没有创建浏览器、修改代理、触碰受保护GPT会话、绕开n8n 401认证。

## 决策
初级阶段确认两类服务都在线；A只读执行已有有效回执，B尚需现有已授权工作流入口。不增加新中间件，不绕认证；只有在B合法工作流完成完全相同任务后才能计算A/B总有效时间。当前候选默认A并非已证实速度冠军。
