# 贾维斯版本2｜下一页面接续总结

## 1. 项目目标
建立 JARVIS v1.0：**个人长期超级助手**，不是新的通用执行器。

当前核心定义：

```text
JARVIS = MEMORY
       + RELIABLE_AUTOMATION
       + EXTREME_TIME_CONVERGENCE
```

- MEMORY：个人长期记忆 + 项目记忆 + 经验/教训 + 世界已解决问题的可检索外部记忆。
- RELIABLE_AUTOMATION：短任务、8小时、跨周、跨月任务使用同一自动化思想；持续时间只是参数，要求可持续、可恢复、可验证。
- EXTREME_TIME_CONVERGENCE：整体闭环极限短时间引擎 v5.6.5，保持 `T*=min(T_VALID)`。

执行器、浏览器、模型、工作流平台都属于可替换资源池，不等于 JARVIS 本身。

核心方法技能入口：
- `skills/jarvis-long-term-super-assistant-core/SKILL.md`
- `skills/jarvis-long-term-super-assistant-core/CURRENT_PROFILE.md`
- `skills/jarvis-long-term-super-assistant-core/ACCEPTANCE.md`

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

## 3. Manus R1-R10 已统一收口
统一总入口：
- `evidence/MANUS_2_EVIDENCE_MASTER_R1_R10.md`
- `evidence/MANUS_2_EVIDENCE_MASTER_R1_R10.json`

来源证据保留：
- `evidence/MANUS_2_CAPABILITY_REALITY_MATRIX.md`
- `evidence/MANUS_2_CAPABILITY_REALITY_MATRIX.json`
- `evidence/MANUS_2_DEEP_BENCHMARK_R8_R10.md`

R8=PARTIAL（329 credits）  
R9=PARTIAL（437 credits）  
R10=SUPPORTED_SCOPED（361 credits）  
新增1127 credits；结束普通余额2703、每日余额179，保持1100保护线。

关键结论：
- 多故障、checkpoint、抢占后恢复：SUPPORTED。
- 7个原生agent与任务生命周期并行：SUPPORTED。
- 依赖调度、局部故障隔离、迟到变更：SUPPORTED。
- 动态浏览器精确执行、会话恢复、幂等：SUPPORTED（限定夹具）。
- 硬隔离、真实权限、假完成抵抗、自验证、跨平台交付：仍有PARTIAL。
- 跨天、重启、断电、供应商失效恢复、用户Windows本机完整执行：未证实。

当前结论：**Manus 证据足够，不做 R11；Manus 默认退出 JARVIS Runtime，仅作为成熟能力参照。**

## 4. 当前架构判断
JARVIS 不应再造另一个 Codex / Manus / Reasonix。

当前长期价值来自：
1. **广义记忆**：正确恢复用户、项目、经验和世界成熟解决方案。
2. **可靠自动化**：无论任务持续多久都能保存状态、中断续接、失败恢复、现实验证。
3. **极限短时间收敛**：每个现实阶段由 v5.6.5 根据第一性原理在 VALID 候选中选择最短有效路径。
4. **能力池过剩，运行路径最小**：能力可以很多，但单任务只启用必要的最小组合。
5. **执行器可替换**：当前默认长流程骨架为 Codex + n8n；Reasonix、JEV/Playwright、pywinauto、Skills 等按任务调用。

历史 `mature-replication-four-column` / 四列法不再参与当前 JARVIS 方法体系；其有效思想已被后续极限短时间方法吸收。

## 5. Manus后续补测规则
默认：不补测，不做 R11。  
只有未来重新决定让 Manus 承担某个实际 Runtime 职责，且该职责依赖未验证边界时，才考虑针对性补证。

当前不因 JARVIS 运行而使用 Manus 付费资源。

## 6. 固定规则
- v5.6.5 三行时间头；N/A非法；异类任务不求共同T*。
- 当前 JARVIS 主状态保持 STATE=10。
- 禁止修改 FlClash / Windows代理网络 / 关键系统配置；禁止新增费用、付款、账号安全修改、删除重要数据。
- LOCAL_FIRST=YES，CLOUD_AS_AUXILIARY=YES。
- 第一性原理高于历史设计；任务高于路径。
- 能力池可以持续增加，但运行主链不能因此膨胀。
- 合理时间无有效进展时，应恢复、换路或重新 Virtual Mature，而不是无限等待。
- 长期记忆必须脱离单一聊天页面存在；只加载当前任务真正相关的记忆。

## 7. 当前执行资源
当前优先复用既有成熟能力，不再开发通用 Agent 执行器：
- GPT / OpenAI：超级大脑、分析、Virtual Mature、纠偏、验收；
- Codex：工程与现实执行；
- n8n：持续自动化与长流程骨架；
- Reasonix：低成本/高性价比智能执行资源；
- JEV-native / Playwright：网页执行；
- pywinauto：Windows GUI；
- 共同 GitHub Skills / Evidence：成熟能力和长期共同事实源。

## 8. 下一步
停止继续扩展抽象架构。

下一阶段只推进四件实际工作：

```text
最小长期记忆现实形态
→ 可靠自动化持久状态 / 续接
→ v5.6.5 从能力池选择最小有效组合
→ 一个真实单任务端到端 Reality + 经验回流
```

完成完整候选并达到系统级 Virtual Mature 后，才进入 STATE=20 / Freeze。
