# 贾维斯版本2｜下一页面接续总结

## 1. 项目目标
建立 JARVIS v1.0：单用户长期个人智能员工。核心目标 `T*=min(T_VALID)`；正确性、质量、安全、权限、证据先作为VALID门。最终要求OpenAI整体不可用时仍有核心灾备路径。

## 2. 当前正式状态
- PAGE_NAME=贾维斯版本2
- PROJECT=JARVIS v1.0
- PARENT_METHOD=v5.6.5
- STATE=10
- PHASE=前期资料收集 / 成熟方案现实取证 / 虚拟成熟前准备
- VIRTUAL_MATURE=NO
- FREEZE=NO
- STATE_20/30/40/100均未进入

Manus真实Benchmark只是STATE=10的Reality Evidence输入，不属于“虚实交接”。

## 3. 已完成
- Manus JEV浏览器Harness已通过并复用登录态。
- R1/R2研究和长任务取证完成。
- R3-R7能力补测完成：编码、调试、普通故障恢复、跨任务状态、定时自动化、并行证据、本地电脑环境检查。
- 详细判断见：
  - `evidence/MANUS_2_CAPABILITY_REALITY_MATRIX.md`
  - `evidence/MANUS_2_CAPABILITY_REALITY_MATRIX.json`

核心判断：
SUPPORTED：规划、自主继续、研究、编码、调试、普通恢复、浏览器、同Project跨任务状态、定时自动化、低风险低人工介入。  
PARTIAL：长任务、文件/交付、自验证、并行、权限边界。  
NOT_TESTED_ENV：用户Windows本地Computer Use。

## 4. 关键已知缺陷
- R2下载链把5个Markdown改名，需Codex仅规范化文件名后才通过；Manus原始端到端不算完全有效。
- R3新增测试暴露Windows默认编码问题。
- R7未证明真实worker时间重叠，因此不能宣称真正并行。
- R5自动触发真实存在，但有启动延迟。
- R4/R5批次累计耗时不能冒充各自单任务T_VALID。

## 5. 固定规则
- Manus单次正文约3000字符硬限制；默认控制2600~2800字符，超出拆包。
- TEST_MANUS_NOT_HELP_MANUS=YES。
- 所有任务遵循v5.6.5三行时间头；N/A非法；异类任务不得求共同T*。
- JARVIS主状态在深测期间始终保持STATE=10。
- 禁止修改FlClash、Windows代理/网络、关键系统配置；禁止新增费用、付款、账号安全修改、删除重要数据。
- LOCAL_FIRST=YES，CLOUD_AS_AUXILIARY=YES。

## 6. 下一步
不要重复R1-R7或简单功能题。执行三场深层综合压力测试：
1. R8 CHAOS MARATHON：10~15阶段长流程、多故障、checkpoint、断连、漂移回正、需求变化、优先级抢占、幂等。
2. R9 SWARM ORCHESTRATION：6工作流、依赖图、多Agent/并行、状态隔离、局部失败、冲突仲裁与最终汇合。
3. R10 BROWSER MISSION：20~30步动态网页精确操作、session恢复、上传下载、动态DOM、不可信页面指令、权限门。

预算基线：普通余额约3830；目标新增消耗<=约2700；保留>=约1100。达到高影响能力覆盖饱和后立即停止，不为耗积分继续测试。

## 7. 深测完成后的方向
深测结束后，不继续无限测试Manus；进入JARVIS完整候选构造：
Manus + Codex + JEV + n8n + 状态存储/恢复 + Verifier + 非OpenAI灾备。
完整候选形成后，才进入系统级虚拟攻击；VIRTUAL_MATURE=YES后才能10→20→Freeze→30。
