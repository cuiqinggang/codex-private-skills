# 长期记忆超级虚拟人｜成熟能力吸收 R1

## 来源

1. Reasonix Recovery Kit（历史能力状态 96/100）
2. ECC v3.1.1
3. Playwright Native AI Browser
4. 极限短时间自动化闭环 v2.0

## 原则

不复制“评分”，复制成熟机制；不复制环境专属实现，保留最小通用运行骨架。

## DIRECT_COPY｜直接吸收为通用原则

- 轻入口 + 重资料库分离
- Capability/Skill Registry
- TASK_CONTRACT / Source of Truth
- checkpoint → handoff → resume
- Gate Review → Repair → Re-Gate
- 修复后必须 Reality 复验
- yesterday replay / 先查成熟资产，避免重复造轮
- health check / runtime verify
- evidence-first
- 故障先恢复业务，再修故障源
- action ledger / lease / fencing（长流程）
- 多智能体只在可并行且可降低完整 T_VALID 时启用

## LIGHT_ADAPT｜轻适配后吸收

### Reasonix model-router
保留：
- 显式目标优先
- 复杂度分层
- 失败升级
- 媒体专用模型
- 会话黏性

不复制：
- 固定 Flash/Pro/GLM/Qwen 型号
- 固定 0-3/4-7/8+ 评分作为永久真理
- 固定 provider

替换为：
- 当前可用模型/额度/成本/Reality 驱动
- ChatGPT UI Controller + API/外部执行器双控制面

### Context fallback
吸收：
```text
收敛 → checkpoint → handoff → 新会话恢复
```
并加入外部 watchdog，不能依赖当前 GPT 自己发现自己失联。

### Recovery Kit
吸收：
- 快速诊断
- 不先重装
- 备份配置
- 最小修复
- 同一故障复现 → 修复 → 同一 Reality 复验
- 版本/路径/入口分离

## REFERENCE_ONLY｜只作为资料，不进入默认运行

- Reasonix 96/100 历史评分
- 绝对路径与旧模型名
- 旧 Kilo/Hermes 专属绑定
- 固定 30/64 worker 数
- 旧安全/代理规则中与当前用户硬边界冲突的部分
- Reasonix “C盘唯一权威、K/H 不回填”等环境专属规则

## EXISTING_MATURE_MODULES｜直接调用，不重造

- ECC v3.1.1：长流程、lease/fencing、Gate/Repair、故障注入、耐力/恢复
- Playwright Native AI Browser：ChatGPT 持久浏览器身份、exactly-once、页面恢复、结果提取
- Desktop Commander Remote：Windows 交互用户文件/进程/命令
- GitHub self-hosted runner：Windows 低相关服务执行面
- Mature AI Coding SuperTool Ecosystem Station：复杂多工具/多智能体重任务按需唤醒

## v1.0 毕业门槛

以下必须有新 Reality：
1. DCR 注销/重登录自动恢复 PASS
2. ChatGPT model/effort 自动切换 + 读回确认 PASS
3. ChatGPT 页面卡死/无响应 → 新会话恢复 PASS
4. GPT 服务不可用 → 独立备脑接管 PASS
5. lease/fencing 防脑裂 PASS
6. K盘/GitHub 双状态源恢复 PASS
7. 一组真实任务证明 v0.2 不比 v0.1 增加无效层级

未满足前保持 0.x，不用历史 96 分直接换算成虚拟人 1.0。
