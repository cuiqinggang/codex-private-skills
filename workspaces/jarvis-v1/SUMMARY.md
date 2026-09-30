# 贾维斯版本2｜下一页面接续总结

## 1. 项目目标
建立 JARVIS v1.0：单用户长期个人智能员工。核心目标 `T*=min(T_VALID)`；正确性、质量、安全、权限、证据先作为 VALID 门。最终需有非单一供应商核心灾备路径。

## 2. 当前正式状态
- PAGE_NAME=贾维斯版本2
- PROJECT=JARVIS v1.0
- PARENT_METHOD=v5.6.5
- STATE=10
- PHASE=前期资料收集 / 成熟方案现实取证 / 完整候选构造前
- VIRTUAL_MATURE=NO
- FREEZE=NO
- 20/30/40/100均未进入

Manus Benchmark 是 STATE=10 的成熟方案现实证据，不是 JARVIS Reality 执行认证。

## 3. Manus 取证已收口
R1-R10 已形成足够的角色级选型证据；R8/R9/R10 深层综合压力测试已结束，不再为覆盖率继续新增测试。

R8=PARTIAL（329 credits）  
R9=PARTIAL（437 credits）  
R10=SUPPORTED_SCOPED（361 credits）  
新增1127 credits；结束普通余额2703、每日余额179，保持1100保护线。

核心新增事实：
- 多故障、checkpoint、抢占后恢复：SUPPORTED。
- 7个原生agent与任务生命周期并行：SUPPORTED。
- 依赖调度、局部故障隔离、迟到变更：SUPPORTED。
- 动态浏览器精确执行、会话恢复、幂等：SUPPORTED（限定夹具）。
- 硬隔离、真实权限、假完成抵抗、自验证、跨平台交付：仍有PARTIAL。
- 跨天、重启、断电、供应商失效恢复、用户Windows本机完整执行：未证实。

详细证据：
- `evidence/MANUS_2_CAPABILITY_REALITY_MATRIX.md`
- `evidence/MANUS_2_CAPABILITY_REALITY_MATRIX.json`
- `evidence/MANUS_2_DEEP_BENCHMARK_R8_R10.md`

## 4. 对最终“99分成熟JARVIS”目标的含义
Manus 的证据已经足够进入 JARVIS 候选构造，但**不能单独证明 JARVIS 已达到最终成熟目标**。

当前缺的不是更多 Manus 测试，而是：
1. 把 Manus、Codex、JEV、n8n、状态存储/恢复、Verifier、非OpenAI灾备等放入一套最小完整职责图。
2. 每个关键职责只保留一个主路径 + 必要备份路径，避免架构膨胀。
3. 对整个 JARVIS 候选做系统级虚拟攻击/失败路径推演。
4. 只有完整候选达到 VIRTUAL_MATURE=YES，才允许 10→20 Freeze→30→40→100。

## 5. Manus后续补测规则
默认：不补测。  
只有最终架构实际依赖以下能力时才补：跨天、重启、断电、供应商失效切换、真实权限/硬隔离、用户Windows本机完整执行。

## 6. 固定规则
- Manus单次正文约3000字符；默认2600~2800字符，超出拆包。
- TEST_MANUS_NOT_HELP_MANUS=YES。
- v5.6.5 三行时间头；N/A非法；异类任务不求共同T*。
- 当前 JARVIS 主状态保持 STATE=10。
- 禁止修改 FlClash / Windows代理网络 / 关键系统配置；禁止新增费用、付款、账号安全修改、删除重要数据。
- LOCAL_FIRST=YES，CLOUD_AS_AUXILIARY=YES。
- 大道至简：不因“还能测”而继续测；只获取会改变架构决策的证据。

## 7. 下一步
**下一步不是 R11。**  
直接进入：`JARVIS 完整候选构造 + 角色分配 + 最小缺口清单`。

完成完整候选后，仍在 STATE=10 内做系统级虚拟成熟；达到成熟门后才进入 STATE=20 / Freeze。
