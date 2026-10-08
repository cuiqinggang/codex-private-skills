# V27 连接开销、浏览器资源与故障恢复：第二版可重放成绩
状态：条件性资源时序模型已运行；VIRTUAL_MATURE=NO；STOP_GATE=NO；REALITY_NOT_RUN；FINAL_VALID=NO
方法 ENGINE=27 / BRAIN=24 / NPT=17。

## 真实证据
Windows在线执行桥已读取 C:\AI\CEO-Auto-V1\v24_f010_T1.json至T5.json。
F011批次现实T_BASE_REAL=115.670s（5/5 PASS），其五单任务耗时之和110.906s。
本机n8n 2.38.7，127.0.0.1:5678/healthz 20次只读请求全部HTTP200，本机往返中位4.634ms，样本最大55.078ms。注意这只是n8n局部HTTP健康检查，不是n8n MCP Client→Supergateway→MCP→浏览器完整开销。
本机 npm -g supergateway检查为空；Supergateway 尚未安装，未运行真实MCP链路。原已登录浏览器CDP端口9223仍监听，没有通过本轮测试发送消息，也没有启动第二浏览器/改代理。

## 真正运行的可重放模型
脚本 C:\AI\Hatchet-Isolated-V1\v27_resource_recovery_model.py
输出 C:\AI\Hatchet-Isolated-V1\v27_resource_recovery_model.json
从F011发送确认与回复完成时间戳读取任务阶段，穷举120个排序。每个SEND前阶段保守当作需要独占浏览器，等待及收尾允许和下一任务准备重叠；验证模拟写锁区间零重叠。
模型最佳排序T1,T2,T3,T5,T4，零新增开销情况下完成76.824s，相对原现实115.670s减少38.846s，即33.583%，1.506倍。该值只是一种条件虚拟数学成绩，不是新整套方案T_VIRTUAL_BEST的验证成绩。
假设仅加入每任务一次本地n8n健康往返中位4.634ms，模拟76.847s；以健康往返样本最大55.078ms代入为77.099s。两者不含真实Supergateway/MCP/浏览器调用开销。
假设完整新增MCP开销每任务100ms：77.324s；500ms：79.324s；2000ms：86.824s。全部是假设而非实测。
模型单次发送前故障+15秒恢复：91.824s；单次T1等待阶段+30秒恢复：76.824s（因T1非关键路径，未改变最大完成时间）。30秒附加失败率1%、5%、20%的简单期待时间估算分别是77.124/78.324/82.824s；仅属假设，与现实故障分布不同。
不持久解锁而整段占浏览器写入槽的模型，110.906s，不包括原批次开销4.764s。

## 反例与门禁
模型校验写独占区间无重叠=PASS_DETERMINISTIC；一旦SEND结果UNKNOWN，停止自动重发=PASS_DETERMINISTIC。它们不是现实的浏览器隔离/重启恢复认证。
没有真实Supergateway安装及n8n MCP Client调用数据，且正式Playwright MCP单实例 ownership、页面重附着、跨进程崩溃恢复、实际VALID均未验证。
所以第27版要求的完整可复核T_VIRTUAL_BEST仍为UNKNOWN；76.824s是条件乐观下界之一，不允许以其33.583%宣称正式优化成熟完成。
物理极限不能从F011五任务耗时唯一确定。

## 继续路径
复用现成授权Playwright STDIO MCP，先通过官方受支持的连接器（n8n MCP Client与成熟协议桥）完成无发送tools/list、单进程归属、测量真实MCP调用开销，再将测值回填模型；必须能证明安全释放写锁与任务会话恢复，否则选择保守串行或回第25版三强对比。完整条件都通过才按Freeze→Reality once进行五任务完整对比。不得因此开发HTTP调度服务、另开浏览器或修改代理。
